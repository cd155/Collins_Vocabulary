# Collins Star Vocabulary · 柯林斯星级词汇

English word lists grouped by their Collins star level, with phonetic and a short Chinese definition, as plain
text, CSV, JSON and Anki decks.

按柯林斯星级分组的英语词汇表，附音标和简短中文释义，提供 TXT、CSV、JSON 和 Anki 卡组。

[中文说明](#中文说明)

## Collins star levels

The Collins English Dictionary rates how common a word is with one to five stars. Five-star words are the most
frequent, so learners usually start there and work down.

| Level | Words | Text | Anki |
|---|---:|---|---|
| ★★★★★ | 630 | [collins_5_star.txt](lists/collins_5_star.txt) | [collins_5_star.apkg](lists/collins_5_star.apkg) |
| ★★★★ | 1,009 | [collins_4_star.txt](lists/collins_4_star.txt) | [collins_4_star.apkg](lists/collins_4_star.apkg) |
| ★★★ | 1,418 | [collins_3_star.txt](lists/collins_3_star.txt) | [collins_3_star.apkg](lists/collins_3_star.apkg) |
| ★★ | 3,036 | [collins_2_star.txt](lists/collins_2_star.txt) | [collins_2_star.apkg](lists/collins_2_star.apkg) |
| ★ | 7,540 | [collins_1_star.txt](lists/collins_1_star.txt) | [collins_1_star.apkg](lists/collins_1_star.apkg) |
| All | 13,633 | [collins.csv](lists/collins.csv) · [collins.json](lists/collins.json) | |

## Formats

- **`.txt`**: one word per line, tab-separated: `word`, `[phonetic]`, `definition`.

  ```text
  about	[ә'baut]	prep. 在...周围, 大约, 有关, 关于; adv. 大约, 四处, 在附近, 周围
  ```

- **`collins.csv`** and **`collins.json`**: every level, with the fields `word`, `stars`, `phonetic` and
  `translation`.
- **`.apkg`**: an Anki deck per level. In Anki, choose **File → Import** and pick the file. Each card shows the
  word and phonetic on the front and the definition on the back. Importing a newer version updates the cards
  instead of adding duplicates.

Definitions keep the first few senses of each part of speech. About 150 words, mostly technical or rare, have
only a field-tagged definition such as `[医]` (medicine) or `[计]` (computing).

## Source

The star levels, phonetics and definitions come from [ECDICT](https://github.com/skywind3000/ECDICT) (MIT
license), an open English–Chinese dictionary. Corrections to a word belong there; this repo regenerates its lists
from it.

## Rebuilding the lists

```bash
mkdir -p data
curl -L -o data/ecdict.csv https://raw.githubusercontent.com/skywind3000/ECDICT/master/ecdict.csv
pip install -r requirements.txt
python build.py
```

`build.py` writes everything in `lists/`.

## Dictation

To practise dictation, paste words from a list into a text-to-speech site such as
[ttsreader.com](https://ttsreader.com/) and write down what you hear.

---

## 中文说明

柯林斯英语词典用一到五颗星标注单词的常用程度，五星词最常用，学习者通常从五星词开始逐级往下学。

| 星级 | 词数 |
|---|---:|
| 五星 | 630 |
| 四星 | 1,009 |
| 三星 | 1,418 |
| 二星 | 3,036 |
| 一星 | 7,540 |
| 合计 | 13,633 |

**文件格式**

- `lists/collins_N_star.txt`：每行一个单词，以制表符分隔：单词、`[音标]`、释义。
- `lists/collins.csv`、`lists/collins.json`：全部星级，字段为 `word`、`stars`、`phonetic`、`translation`。
- `lists/collins_N_star.apkg`：每个星级一个 Anki 卡组。在 Anki 中选择「文件 → 导入」即可。卡片正面为单词和音标，背面为释义；导入新版本会更新已有卡片，不会重复添加。

释义保留每个词性的前几个义项。约 150 个生僻或专业词汇只有带领域标记的释义，如 `[医]`（医学）、`[计]`（计算机）。

**数据来源**：星级、音标和释义均来自开源英汉词典 [ECDICT](https://github.com/skywind3000/ECDICT)（MIT 许可）。如发现单词有误，请到 ECDICT 反馈；本仓库的词表由它重新生成。

**听写练习**：把词表中的单词粘贴到 [ttsreader.com](https://ttsreader.com/) 等朗读网站，边听边写。
