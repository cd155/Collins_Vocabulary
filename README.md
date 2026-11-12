# 柯林斯星级词汇 · Collins Star Vocabulary

按柯林斯星级分组的 13,633 个英语单词，附音标和简短中文释义，提供 TXT、CSV、JSON 和 Anki 卡组。

13,633 English words grouped by their Collins star level, with phonetic and a short Chinese definition, as plain
text, CSV, JSON and Anki decks.

在线查询 · Browse online: **<https://cd155.github.io/collins-vocabulary/>**

[English](#english)

| 星级 Level | 词数 Words | 文本 Text | Anki | AnkiWeb |
|---|---:|---|---|---|
| ★★★★★ 五星 | 630 | [collins_5_star.txt](lists/collins_5_star.txt) | [collins_5_star.apkg](lists/collins_5_star.apkg) | [1403111213](https://ankiweb.net/shared/info/1403111213) |
| ★★★★ 四星 | 1,009 | [collins_4_star.txt](lists/collins_4_star.txt) | [collins_4_star.apkg](lists/collins_4_star.apkg) | [1544157144](https://ankiweb.net/shared/info/1544157144) |
| ★★★ 三星 | 1,418 | [collins_3_star.txt](lists/collins_3_star.txt) | [collins_3_star.apkg](lists/collins_3_star.apkg) | [1539836752](https://ankiweb.net/shared/info/1539836752) |
| ★★ 二星 | 3,036 | [collins_2_star.txt](lists/collins_2_star.txt) | [collins_2_star.apkg](lists/collins_2_star.apkg) | [459912606](https://ankiweb.net/shared/info/459912606) |
| ★ 一星 | 7,540 | [collins_1_star.txt](lists/collins_1_star.txt) | [collins_1_star.apkg](lists/collins_1_star.apkg) | [1163764613](https://ankiweb.net/shared/info/1163764613) |
| 合计 All | 13,633 | [collins.csv](lists/collins.csv) · [collins.json](lists/collins.json) | | |

## 柯林斯星级

柯林斯英语词典用一到五颗星标注单词的常用程度，五星词最常用，学习者通常从五星词开始逐级往下学。

## 文件格式

- **`.txt`**：每行一个单词，以制表符分隔：单词、`[音标]`、释义。

  ```text
  about	[ә'baut]	prep. 在...周围, 大约, 有关, 关于; adv. 大约, 四处, 在附近, 周围
  ```

- **`collins.csv`**、**`collins.json`**：全部星级，字段为 `word`、`stars`、`phonetic`、`translation`，以及：
  - `tags`：收录该词的考试，取值为 `zk`（中考）、`gk`（高考）、`cet4`（四级）、`cet6`（六级）、`ky`（考研）、`toefl`（托福）、`ielts`（雅思）、`gre`。
  - `bnc`、`frq`：该词在英国国家语料库和当代语料库中的词频排名，1 为最常用；没有排名时为空。
- **`.apkg`**：每个星级一个 Anki 卡组。在 Anki 中选择「文件 → 导入」即可。卡片正面为单词和音标，背面为释义；导入新版本会更新已有卡片，不会重复添加。每张卡片带有
  上述考试标签，可在 Anki 中按标签筛选，例如只学五星词中的四级词汇。

释义保留每个词性的前几个义项。约 150 个生僻或专业词汇只有带领域标记的释义，如 `[医]`（医学）、`[计]`（计算机）。

`Vocabulary_Lists/` 是词表原来的路径，为了让旧链接继续可用而保留，内容与 `lists/` 中的 `.txt` 相同。

## 数据来源

星级、音标和释义均来自开源英汉词典 [ECDICT](https://github.com/skywind3000/ECDICT)（MIT 许可）。如发现单词有误，请到 ECDICT
反馈；本仓库的词表由它重新生成。

## 听写练习

把词表中的单词粘贴到 [ttsreader.com](https://ttsreader.com/) 等朗读网站，边听边写。

---

## English

### Collins star levels

The Collins English Dictionary rates how common a word is with one to five stars. Five-star words are the most
frequent, so learners usually start there and work down. The table at the top links each level's files.

### Formats

- **`.txt`**: one word per line, tab-separated: `word`, `[phonetic]`, `definition`.
- **`collins.csv`** and **`collins.json`**: every level, with the fields `word`, `stars`, `phonetic`,
  `translation`, and:
  - `tags`: the exams whose syllabus has the word: `zk` (Zhongkao), `gk` (Gaokao), `cet4`, `cet6`, `ky`
    (postgraduate entrance exam), `toefl`, `ielts`, `gre`.
  - `bnc`, `frq`: the word's frequency rank in the British National Corpus and in a contemporary corpus. 1 is
    the most frequent; empty when there is no rank.
- **`.apkg`**: an Anki deck per level. In Anki, choose **File → Import** and pick the file. Each card shows the
  word and phonetic on the front and the definition on the back. Importing a newer version updates the cards
  instead of adding duplicates. Each note carries the exam tags above as Anki tags, so you can study, say, only
  the CET-4 words of the five-star deck.

Definitions keep the first few senses of each part of speech. About 150 words, mostly technical or rare, have
only a field-tagged definition such as `[医]` (medicine) or `[计]` (computing).

`Vocabulary_Lists/` is where the lists used to be. It is kept so old links still work, and holds the same content
as the `.txt` files in `lists/`.

### Source

The star levels, phonetics and definitions come from [ECDICT](https://github.com/skywind3000/ECDICT) (MIT
license), an open English–Chinese dictionary. Corrections to a word belong there; this repo regenerates its lists
from it.

### Rebuilding the lists

```bash
mkdir -p data
curl -L -o data/ecdict.csv https://raw.githubusercontent.com/skywind3000/ECDICT/master/ecdict.csv
pip install -r requirements.txt
python build.py
```

`build.py` writes everything in `lists/` and `Vocabulary_Lists/`.

`python site.py` builds the website from `lists/collins.json` into `_site/`. A workflow deploys it to GitHub Pages
on every push to `master` that changes the lists.

### Dictation

To practise dictation, paste words from a list into a text-to-speech site such as
[ttsreader.com](https://ttsreader.com/) and write down what you hear.

## License

[MIT](LICENSE)
