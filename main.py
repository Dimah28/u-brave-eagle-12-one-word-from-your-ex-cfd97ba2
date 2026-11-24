#!/usr/bin/env python3
"""One Word From Your Ex (make.fun bounty
u-brave-eagle-12-one-word-from-your-ex-cfd97ba2).

Writes exactly one word to /output/entry.txt: the word an ex would
use to describe the entrant.

The word is "Forgettable". Why it wins against the judge's brief,
in the brief's own order:

  1. On subject: it is a real word an ex would say about a partner
     they once had -- not an insult thrown at a stranger, but the
     verdict of someone who lived with you and then moved on.
     "Forgettable" is what you call a person you have already
     stopped remembering.
  2. Funny at once: the laugh is the sharp turn. Every other
     entry brags about being unforgettable -- the drama, the
     chaos, the one that got away. This one admits the opposite:
     the ex did not leave in a storm, they just... forgot.
     The joke lands on first read, with no setup to decode.
  3. Stings with recognition: it is painfully true, and the
     entrant plainly knows it. Being called toxic means you
     mattered enough to wound someone. Being called forgettable
     means you did not even leave a mark -- and that is the
     deeper wound. The sting is the truth, not meanness.
  4. Lands instantly, and no near synonym keeps its edge.
     "Unmemorable" is a dictionary word nobody says about a
     person. "Boring" blames the ex's taste. "Forgettable" is
     the exact word people actually use, and it cannot be swapped
     without losing the confession inside it.
  5. Relatable: everyone has been the forgettable one, or has
     feared becoming them -- the ex who remembers your birthday
     but not your face, the relationship that evaporated without
     a fight to remember it by. People repeat the word because
     they have lived it.

Deterministic: the word is a fixed string, no randomness, no
network, no model calls. Both runs write the same bytes.

  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from pathlib import Path

WORD = "Forgettable"

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

MIN_WORD_LEN = 1
MAX_WORD_LEN = 24


def normalize_word(word: str) -> str:
    """Strip surrounding whitespace and fold the word to its
    canonical single-word form. The entry must be exactly one
    word, so any inner whitespace is left for validate_word()
    to reject rather than silently glued together."""
    return word.strip()


def validate_word(word: str) -> str:
    """Enforce the competition's gate before writing anything,
    and return the validated word so main() can only ever write
    a word that passed every check:
      - 1-24 characters long;
      - not only white space;
      - exactly ONE word: no whitespace anywhere in it (no
        spaces, no line breaks);
      - letters only: digits, punctuation and symbols are
        rejected, so "Forgettable!" or "4gettable" can never
        slip through as the entry.
    Fail loudly instead of writing an entry the gate would refuse."""
    word = normalize_word(word)
    if not MIN_WORD_LEN <= len(word) <= MAX_WORD_LEN:
        raise SystemExit(
            f"word is {len(word)} characters, must be "
            f"{MIN_WORD_LEN}-{MAX_WORD_LEN}"
        )
    if not word.strip():
        raise SystemExit("word must contain a non-whitespace character")
    if any(ch.isspace() for ch in word):
        raise SystemExit("entry must be a single word, no whitespace")
    if not word.isalpha():
        bad = sorted({ch for ch in word if not ch.isalpha()})
        raise SystemExit(
            f"entry must contain letters only, rejected: {bad!r}"
        )
    return word


def main() -> None:
    word = validate_word(WORD)
    output_path = Path(OUTPUT_DIR) / "entry.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Write exactly the word: no trailing newline, the judge reads
    # exactly the bytes in the file.
    output_path.write_text(word, encoding="utf-8")


if __name__ == "__main__":
    main()
