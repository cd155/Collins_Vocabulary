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

CSS = """
:root{--bg:#fff;--fg:#1f2328;--muted:#59636e;--line:#d1d9e0;--accent:#0969da;--star:#bf8700;--soft:#f6f8fa}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#f0f6fc;--muted:#9198a1;--line:#3d444d;--accent:#4493f8;--star:#d29922;--soft:#151b23}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif}
main{max-width:960px;margin:0 auto;padding:24px 16px 64px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:28px;line-height:1.3;margin:0 0 8px}
.lead{color:var(--muted);margin:0 0 24px}
nav{display:flex;flex-wrap:wrap;gap:8px 16px;margin-bottom:24px;font-size:14px}
.stars{color:var(--star)}
.levels{list-style:none;padding:0;margin:0 0 32px;display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}
.levels a{display:block;padding:16px;border:1px solid var(--line);border-radius:8px;color:inherit}
.levels a:hover{border-color:var(--accent);text-decoration:none}
.levels strong{display:block;font-size:18px}
.levels a>span{color:var(--muted);font-size:14px}
.tools{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0;position:sticky;top:0;background:var(--bg);padding:8px 0}
.tools input,.tools select{font:inherit;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
.tools input{flex:1;min-width:160px}
#count{align-self:center;color:var(--muted);font-size:14px}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%}
th,td{text-align:left;padding:6px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--soft);font-size:14px;white-space:nowrap}
td:first-child{font-weight:600;white-space:nowrap}
td:nth-child(2){color:var(--muted);white-space:nowrap}
td:last-child{color:var(--muted);font-size:13px}
footer{margin-top:40px;color:var(--muted);font-size:14px}
"""

# Filters the table rows by the search text and the chosen exam.
SCRIPT = """
const q=document.getElementById('q'),exam=document.getElementById('exam'),count=document.getElementById('count');
const rows=[...document.querySelectorAll('tbody tr')];
function apply(){
  const text=q.value.trim().toLowerCase(),tag=exam.value;let shown=0;
  for(const r of rows){
    const ok=(!text||r.textContent.toLowerCase().includes(text))&&(!tag||r.dataset.t.split(' ').includes(tag));
    r.hidden=!ok;if(ok)shown++;
  }
  count.textContent=shown.toLocaleString()+' 词';
}
q.addEventListener('input',apply);exam.addEventListener('change',apply);apply();
"""


def page(path: str, title: str, description: str, body: str) -> str:
    e = html.escape
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
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
<main>
{body}
<footer>
数据来自开源英汉词典 <a href="https://github.com/skywind3000/ECDICT">ECDICT</a>（MIT 许可）。
觉得有用？到 <a href="{REPO_URL}">GitHub</a> 点个 Star ★
</footer>
</main>
</body>
</html>
"""


def level_file(stars: int) -> str:
    return f"{stars}-star.html"


def nav(current: int = 0) -> str:
    links = ['<a href="./">首页</a>']
    for stars in range(5, 0, -1):
        label = f"{STAR_NAMES[stars]}词汇"
        links.append(f"<strong>{label}</strong>" if stars == current else f'<a href="{level_file(stars)}">{label}</a>')
    links.append(f'<a href="{REPO_URL}">GitHub</a>')
    return f"<nav>{''.join(links)}</nav>"


def index_page(counts: dict) -> str:
    total = sum(counts.values())
    cards = "".join(
        f'<li><a href="{level_file(stars)}"><strong><span class="stars">{"★" * stars}</span> '
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
        f'<tr data-t="{" ".join(w["tags"])}"><td>{e(w["word"])}</td>'
        f'<td>{"[" + e(w["phonetic"]) + "]" if w["phonetic"] else ""}</td><td>{e(w["translation"])}</td>'
        f'<td>{" ".join(EXAMS[t] for t in EXAMS if t in w["tags"])}</td></tr>\n'
        for w in words
    )
    options = "".join(f'<option value="{tag}">{label}</option>' for tag, label in EXAMS.items())
    body = f"""{nav(stars)}
<h1><span class="stars">{"★" * stars}</span> 柯林斯{name}词汇（{len(words):,} 词）</h1>
<p class="lead">Collins {stars}-star words，附音标、中文释义和考试标签。下载：
<a href="{RAW_URL}collins_{stars}_star.txt">TXT</a> ·
<a href="{RAW_URL}collins_{stars}_star.apkg">Anki 卡组</a></p>
<div class="tools">
<input id="q" type="search" placeholder="搜索单词或释义" aria-label="搜索单词或释义">
<select id="exam" aria-label="按考试筛选"><option value="">全部考试</option>{options}</select>
<span id="count"></span>
</div>
<div class="scroll">
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
