"""Build the Collins star word lists in lists/ from ECDICT.

ECDICT (https://github.com/skywind3000/ECDICT, MIT license) records each word's
Collins star level. Download its ecdict.csv into data/ first:

    curl -L -o data/ecdict.csv https://raw.githubusercontent.com/skywind3000/ECDICT/master/ecdict.csv
    pip install -r requirements.txt
    python build.py
"""

import csv
import html
import json
import re
import shutil
from pathlib import Path
from typing import Optional

import genanki

ROOT = Path(__file__).parent
SOURCE = ROOT / "data" / "ecdict.csv"
OUT = ROOT / "lists"

# Where the text lists were before they moved to lists/. Search engines and old
# links still point at these paths, so each one gets a copy of the current list.
LEGACY = ROOT / "Vocabulary_Lists"
LEGACY_NAMES = {
    5: "five_star.txt",
    4: "four_star.text",
    3: "three_star.txt",
    2: "two_star.txt",
    1: "one_star.txt",
}

MAX_POS_LINES = 3  # part-of-speech lines kept per word
MAX_SENSES = 4  # senses kept per part-of-speech line
POS_LINE = re.compile(r"^[a-z]+\.")

# Fixed ids so re-importing a deck updates it in Anki instead of duplicating it.
MODEL_ID = 1735061101
DECK_ID_BASE = 1735061110


def split_senses(text: str) -> list[str]:
    """Split on commas and semicolons that are not inside brackets."""
    parts, current, depth = [], "", 0
    for ch in text:
        if ch in "(（[【<《":
            depth += 1
        elif ch in ")）]】>》":
            depth = max(depth - 1, 0)
        if depth == 0 and ch in ",，;；":
            parts.append(current.strip())
            current = ""
        else:
            current += ch
    parts.append(current.strip())
    return [p for p in parts if p]


def short_translation(raw: str) -> str:
    """Keep the first few senses of the first few part-of-speech lines.

    Senses tagged with a field such as [计] (computing) or [医] (medicine) are
    rarely the meaning a learner needs, so they are used only when a word has
    nothing else.
    """
    lines = [line.strip() for line in re.split(r"\\r\\n|\\n", raw) if line.strip()]
    general, tagged = [], []
    for line in lines:
        pos, _, senses = line.partition(" ") if POS_LINE.match(line) else ("", "", line)
        parts = split_senses(senses)
        plain = [s for s in parts if not s.startswith("[")]
        if plain and not senses.startswith("["):
            general.append((pos, plain))
        else:
            tagged.append((pos, parts))

    with_pos = [entry for entry in general if entry[0]]
    chosen = with_pos or general[:1] or tagged
    return "; ".join(
        f"{pos} {', '.join(parts[:MAX_SENSES])}".strip() for pos, parts in chosen[:MAX_POS_LINES]
    )


def rank(value: str) -> Optional[int]:
    """A frequency rank, or None when ECDICT has none (empty or 0)."""
    return int(value) if value and value != "0" else None


def load_words() -> list[dict]:
    words = []
    with SOURCE.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            stars = row["collins"]
            if not stars or stars == "0":
                continue
            words.append(
                {
                    "word": row["word"],
                    "stars": int(stars),
                    "phonetic": row["phonetic"],
                    "translation": short_translation(row["translation"]),
                    # Exams whose syllabus has the word: zk, gk, cet4, cet6, ky, toefl, ielts, gre.
                    "tags": row["tag"].split(),
                    # Rank in the British National Corpus and in a contemporary corpus; 1 is the most frequent.
                    "bnc": rank(row["bnc"]),
                    "frq": rank(row["frq"]),
                }
            )
    words.sort(key=lambda w: (-w["stars"], w["word"].lower(), w["word"]))
    return words


def write_txt(words: list[dict], stars: int) -> None:
    path = OUT / f"collins_{stars}_star.txt"
    with path.open("w", encoding="utf-8") as f:
        for w in words:
            phonetic = f"[{w['phonetic']}]" if w["phonetic"] else ""
            f.write(f"{w['word']}\t{phonetic}\t{w['translation']}\n")
    shutil.copyfile(path, LEGACY / LEGACY_NAMES[stars])


def write_apkg(words: list[dict], stars: int, model: genanki.Model) -> None:
    deck = genanki.Deck(DECK_ID_BASE + stars, f"Collins {stars} Star")
    for w in words:
        deck.add_note(
            genanki.Note(
                model=model,
                fields=[html.escape(w["word"]), html.escape(w["phonetic"]), html.escape(w["translation"]), "★" * stars],
                guid=genanki.guid_for(w["word"], stars),
                tags=w["tags"],
            )
        )
    genanki.Package(deck).write_to_file(OUT / f"collins_{stars}_star.apkg")


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing {SOURCE}. See the download command at the top of build.py.")
    OUT.mkdir(exist_ok=True)
    LEGACY.mkdir(exist_ok=True)
    words = load_words()

    with (OUT / "collins.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["word", "stars", "phonetic", "translation", "tags", "bnc", "frq"])
        writer.writeheader()
        writer.writerows({**w, "tags": " ".join(w["tags"])} for w in words)
    with (OUT / "collins.json").open("w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=1)
        f.write("\n")

    model = genanki.Model(
        MODEL_ID,
        "Collins Word",
        fields=[{"name": "Word"}, {"name": "Phonetic"}, {"name": "Translation"}, {"name": "Stars"}],
        templates=[
            {
                "name": "Word → Translation",
                "qfmt": '<div class="word">{{Word}}</div><div class="phonetic">{{#Phonetic}}[{{Phonetic}}]{{/Phonetic}}</div>',
                "afmt": '{{FrontSide}}<hr id="answer"><div class="translation">{{Translation}}</div><div class="stars">{{Stars}}</div>',
            }
        ],
        css=(
            ".card{font-family:sans-serif;text-align:center;font-size:22px}"
            ".word{font-size:34px;font-weight:bold}.phonetic{color:#666}"
            ".translation{margin-top:12px}.stars{color:#c90;margin-top:8px}"
        ),
    )

    for stars in range(5, 0, -1):
        level = [w for w in words if w["stars"] == stars]
        write_txt(level, stars)
        write_apkg(level, stars, model)
        print(f"{stars}★ {len(level)} words")
    print(f"total {len(words)} words")


if __name__ == "__main__":
    main()
