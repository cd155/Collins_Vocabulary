"""Build the GitHub Pages site in _site/ from lists/collins.json.

    python site.py

Standard library only, so the deploy workflow runs it without installing anything.
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "lists" / "collins.json"
OUT = ROOT / "_site"

SITE_URL = "https://cd155.github.io/Collins_Vocabulary/"
REPO_URL = "https://github.com/cd155/Collins_Vocabulary"
RAW_URL = f"{REPO_URL}/raw/master/lists/"

STAR_NAMES = {5: "五星", 4: "四星", 3: "三星", 2: "二星", 1: "一星"}
# ECDICT's exam tags, in the order a learner meets the exams.
EXAMS = {
    "zk": "中考",
    "gk": "高考",
    "cet4": "四级",
    "cet6": "六级",
    "ky": "考研",
    "toefl": "托福",
    "ielts": "雅思",
    "gre": "GRE",
}

# The colors and shapes follow QuantNote's web app: an off-white or black page,
# cards with a 16px radius and a hairline border, pill-shaped chips, and the
# system font. The theme follows the device, like there. Every text pair meets
# WCAG AA (4.5:1) in both themes.
CSS = """
:root{color-scheme:light dark;--background:#FCFCFB;--foreground:#000;--card-bg:#fff;--card-border:#F0F2F1;--line:#E0E2E1;
--muted:#3B4340;--primary:#005FC8;--star:#7A6A00;--cta-bg:#000;--cta-fg:#FCFCFB;--cta-button-bg:#FCFCFB;--cta-button-fg:#000;--bar:rgba(255,255,255,.9)}
@media(prefers-color-scheme:dark){:root{--background:#000;--foreground:#F0F2F1;--card-bg:#1A1C1B;--card-border:#2B2D2C;--line:#2B2D2C;
--muted:#B0B2B1;--primary:#4DA3FF;--star:#D4C04A;--cta-bg:#1A1C1B;--cta-fg:#F0F2F1;--cta-button-bg:#F0F2F1;--cta-button-fg:#000;--bar:rgba(26,28,27,.9)}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--background);color:var(--foreground);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;overscroll-behavior-y:contain}
a{color:var(--primary);text-decoration:none}
a:hover{text-decoration:underline}
header{position:sticky;top:0;z-index:20;height:52px;background:var(--bar);border-bottom:1px solid var(--card-border);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);padding:0 max(16px,env(safe-area-inset-right)) 0 max(16px,env(safe-area-inset-left))}
.bar{max-width:960px;height:100%;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px}
.brand{color:var(--foreground);font-weight:700}
.brand:hover{text-decoration:none}
main{max-width:960px;margin:0 auto;padding:16px max(16px,env(safe-area-inset-right)) calc(48px + env(safe-area-inset-bottom)) max(16px,env(safe-area-inset-left))}
h1{font-size:24px;line-height:1.3;margin:16px 0 8px}
h2{font-size:18px;margin:32px 0 8px}
p{margin:0 0 12px}
.lead{color:var(--muted);margin-bottom:20px}
.stars{color:var(--star)}
.pills{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin:0 -16px;padding:0 16px}
.pills::-webkit-scrollbar{display:none}
.pill{flex:none;font:inherit;font-size:14px;font-weight:500;line-height:1.4;white-space:nowrap;padding:6px 16px;border-radius:999px;border:1px solid var(--card-border);background:var(--card-bg);color:var(--foreground);cursor:pointer}
.pill:hover{border-color:var(--muted);text-decoration:none}
.pill.on,.pill[aria-pressed=true]{background:var(--foreground);border-color:var(--foreground);color:var(--background)}
.card{border:1px solid var(--card-border);border-radius:16px;background:var(--card-bg)}
.levels{list-style:none;padding:0;margin:0;display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}
.levels a{display:block;padding:16px;color:inherit}
.levels a:hover{border-color:var(--muted);text-decoration:none}
.levels strong{display:block;font-size:17px}
.levels a>span{color:var(--muted);font-size:14px}
.tools{position:sticky;top:52px;z-index:10;background:var(--background);padding:12px 0;display:grid;gap:10px}
.tools input{width:100%;font:inherit;padding:10px 14px;border:1px solid var(--card-border);border-radius:16px;background:var(--card-bg);color:var(--foreground);outline:none}
.tools input:focus{border-color:var(--muted)}
.tools input::placeholder{color:var(--muted)}
#count{color:var(--muted);font-size:14px;margin:0 0 8px}
.words{overflow:hidden}
table{border-collapse:collapse;width:100%}
th,td{text-align:left;padding:10px 16px;vertical-align:top}
th{color:var(--muted);font-size:13px;font-weight:500;white-space:nowrap;border-bottom:1px solid var(--line)}
tbody tr+tr td{border-top:1px solid var(--line)}
tbody tr[hidden]{display:none}
.w{font-weight:600;white-space:nowrap}
.p{color:var(--muted);white-space:nowrap}
.x{min-width:150px}
.x span{display:inline-block;margin:2px 4px 2px 0;padding:1px 8px;border-radius:999px;background:var(--card-border);color:var(--muted);font-size:12px;white-space:nowrap}
.cta{margin-top:32px;padding:24px;border-radius:16px;background:var(--cta-bg);color:var(--cta-fg);border:1px solid var(--card-border);text-align:center}
.cta p{margin:0 0 14px}
.cta a{display:inline-block;padding:8px 20px;border-radius:999px;background:var(--cta-button-bg);color:var(--cta-button-fg);font-weight:600;font-size:14px}
.cta a:hover{text-decoration:none;opacity:.9}
footer{margin-top:24px;color:var(--muted);font-size:13px;text-align:center}
@media(max-width:640px){
h1{font-size:21px}
thead{display:none}
table,tbody{display:block}
tbody tr{display:grid;grid-template-columns:auto 1fr;column-gap:8px;padding:12px 16px}
tbody tr+tr{border-top:1px solid var(--line)}
tbody tr+tr td{border-top:0}
td{display:block;padding:0}
.w{font-size:17px}
.p{white-space:normal;align-self:center;font-size:14px}
.d,.x{grid-column:1/-1}
.x{min-width:0}
.x:empty{display:none}
.x span{margin-top:6px}
}
"""

# Filters the table rows by the search text and the chosen exam.
SCRIPT = """
const q=document.getElementById('q'),chips=[...document.querySelectorAll('#exams button')],count=document.getElementById('count');
const rows=[...document.querySelectorAll('tbody tr')];
let tag='';
function apply(){
  const text=q.value.trim().toLowerCase();let shown=0;
  for(const r of rows){
    const ok=(!text||r.textContent.toLowerCase().includes(text))&&(!tag||r.dataset.t.split(' ').includes(tag));
    r.hidden=!ok;if(ok)shown++;
  }
  count.textContent=shown.toLocaleString()+' 词';
}
for(const c of chips)c.addEventListener('click',()=>{
  tag=c.dataset.tag;
  for(const o of chips)o.setAttribute('aria-pressed',o===c);
  apply();
});
q.addEventListener('input',apply);apply();
"""


def page(path: str, title: str, description: str, body: str) -> str:
    e = html.escape
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#FCFCFB">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#000000">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="manifest" href="manifest.webmanifest">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}{path}">
<style>{CSS}</style>
</head>
<body>
<header><div class="bar"><a class="brand" href="./">柯林斯星级词汇</a><a href="{REPO_URL}">GitHub</a></div></header>
<main>
{body}
<div class="cta">
<p>觉得有用？在 GitHub 点个 Star，让更多人看到。</p>
<a href="{REPO_URL}">★ Star on GitHub</a>
</div>
<footer>数据来自开源英汉词典 <a href="https://github.com/skywind3000/ECDICT">ECDICT</a>（MIT 许可）</footer>
</main>
</body>
</html>
"""


# The letter C around a four-point star, off-white on the site's blue.
ICON_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#005FC8"/>'
    '<path d="M43.2 17.6A17 17 0 1 0 43.2 46.4" fill="none" stroke="#FCFCFB" stroke-width="6" stroke-linecap="round"/>'
    '<path d="M34 23.5Q35.4 30.6 42.5 32Q35.4 33.4 34 40.5Q32.6 33.4 25.5 32Q32.6 30.6 34 23.5Z" fill="#FCFCFB"/></svg>\n'
)


MANIFEST = {
    "name": "柯林斯星级词汇",
    "short_name": "柯林斯词汇",
    "lang": "zh-CN",
    "start_url": ".",
    "scope": ".",
    "display": "standalone",
    "background_color": "#FCFCFB",
    "theme_color": "#FCFCFB",
    "icons": [{"src": "icon.svg", "sizes": "any", "type": "image/svg+xml"}],
}


def level_file(stars: int) -> str:
    return f"{stars}-star.html"


def nav(current: int = 0) -> str:
    pills = "".join(
        f'<a class="pill{" on" if stars == current else ""}" href="{level_file(stars)}"'
        f'{" aria-current=page" if stars == current else ""}>{STAR_NAMES[stars]}词汇</a>'
        for stars in range(5, 0, -1)
    )
    return f'<nav class="pills" aria-label="星级">{pills}</nav>'


def index_page(counts: dict) -> str:
    total = sum(counts.values())
    cards = "".join(
        f'<li><a class="card" href="{level_file(stars)}"><strong><span class="stars">{"★" * stars}</span> '
        f"柯林斯{STAR_NAMES[stars]}词汇</strong><span>{counts[stars]:,} 词 · Collins {stars}-star words</span></a></li>"
        for stars in range(5, 0, -1)
    )
    body = f"""{nav()}
<h1>柯林斯星级词汇 · Collins Star Vocabulary</h1>
<p class="lead">按柯林斯星级分组的 {total:,} 个英语单词，附音标、中文释义和考试标签（四级、六级、考研、托福、雅思、GRE 等）。
可在线查询，也可下载 TXT、CSV、JSON 和 Anki 卡组。</p>
<ul class="levels">{cards}</ul>
<h2>什么是柯林斯星级？</h2>
<p>柯林斯英语词典用一到五颗星标注单词的常用程度，五星词最常用。学习者通常从五星词开始，逐级往下学。</p>
<h2>下载</h2>
<p>全部词汇：<a href="{RAW_URL}collins.csv">collins.csv</a> · <a href="{RAW_URL}collins.json">collins.json</a>。
各星级的 TXT 和 Anki 卡组见每个星级的页面，或到 <a href="{REPO_URL}">GitHub 仓库</a>查看。</p>"""
    return page(
        "",
        f"柯林斯星级词汇表：{total:,} 个一至五星英语单词（音标、释义、Anki）",
        f"柯林斯一星到五星词汇共 {total:,} 词，附音标、中文释义和四六级、考研、托福、雅思、GRE 标签，可在线查询并下载 TXT、CSV、JSON、Anki 卡组。",
        body,
    )


def level_page(stars: int, words: list) -> str:
    e = html.escape
    name = STAR_NAMES[stars]
    rows = "".join(
        f'<tr data-t="{" ".join(w["tags"])}"><td class="w">{e(w["word"])}</td>'
        f'<td class="p">{"[" + e(w["phonetic"]) + "]" if w["phonetic"] else ""}</td><td class="d">{e(w["translation"])}</td>'
        f'<td class="x">{"".join(f"<span>{EXAMS[t]}</span>" for t in EXAMS if t in w["tags"])}</td></tr>\n'
        for w in words
    )
    chips = "".join(
        f'<button class="pill" type="button" data-tag="{tag}" aria-pressed="false">{label}</button>'
        for tag, label in EXAMS.items()
    )
    body = f"""{nav(stars)}
<h1><span class="stars">{"★" * stars}</span> 柯林斯{name}词汇（{len(words):,} 词）</h1>
<p class="lead">Collins {stars}-star words，附音标、中文释义和考试标签。下载：
<a href="{RAW_URL}collins_{stars}_star.txt">TXT</a> ·
<a href="{RAW_URL}collins_{stars}_star.apkg">Anki 卡组</a></p>
<div class="tools">
<input id="q" type="search" placeholder="搜索单词或释义" aria-label="搜索单词或释义">
<div class="pills" id="exams" role="group" aria-label="按考试筛选">
<button class="pill" type="button" data-tag="" aria-pressed="true">全部</button>{chips}
</div>
</div>
<p id="count" aria-live="polite"></p>
<div class="card words">
<table>
<thead><tr><th>单词</th><th>音标</th><th>释义</th><th>考试</th></tr></thead>
<tbody>
{rows}</tbody>
</table>
</div>
<script>{SCRIPT}</script>"""
    return page(
        level_file(stars),
        f"柯林斯{name}词汇表（{len(words):,} 词，含音标和释义）",
        f"柯林斯{name}词汇共 {len(words):,} 词，附音标、中文释义和考试标签，可按四六级、考研、托福、雅思、GRE 筛选，并下载 TXT 和 Anki 卡组。",
        body,
    )


def main() -> None:
    words = json.loads(SOURCE.read_text(encoding="utf-8"))
    by_level = {stars: [w for w in words if w["stars"] == stars] for stars in STAR_NAMES}
    OUT.mkdir(exist_ok=True)

    (OUT / "index.html").write_text(index_page({s: len(ws) for s, ws in by_level.items()}), encoding="utf-8")
    for stars, level in by_level.items():
        (OUT / level_file(stars)).write_text(level_page(stars, level), encoding="utf-8")

    (OUT / "icon.svg").write_text(ICON_SVG, encoding="utf-8")
    (OUT / "manifest.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    urls = [SITE_URL] + [SITE_URL + level_file(stars) for stars in STAR_NAMES]
    sitemap = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sitemap}</urlset>\n',
        encoding="utf-8",
    )
    print(f"wrote {len(urls)} pages to {OUT}")


if __name__ == "__main__":
    main()
