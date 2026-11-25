"""A patch note that fixes human sleep, written out by this script.

The note itself is frozen: one fixed string, checked by a set of
small named guards, then saved to /output/entry.txt. The guards
cover the topic, the size, the shape of the text, and how many
sentences it holds, and any failure ends the run with exit code
1 before anything is written. No input, no clock, no network,
no randomness -- the same bytes come out every time.
"""

import sys
from pathlib import Path

ENTRY = "Fixed: human sleep now installs on the first try. Known issue: Mondays still load slowly."
BOUND = 160
GOAL = Path("/output/entry.txt")


def reject_entry(msg):
    print(f"rejected: {msg}", file=sys.stderr)
    raise SystemExit(1)


def guard_sleep_word(text):
    if "sleep" not in text:
        reject_entry("entry is off topic")


def guard_sentence_count(text):
    if text.count(".") > 2:
        reject_entry("entry has too many sentences")


def guard_size(text):
    if len(text) > BOUND:
        reject_entry("entry is longer than the limit")


def guard_present(text):
    if not text or not text.strip():
        reject_entry("entry is empty")


def guard_printable(text):
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        reject_entry("entry has control characters")


def guard_layout(text):
    if text != text.strip() or "  " in text or "\n" in text or "\r" in text:
        reject_entry("entry has ragged edges or line breaks")


def guard_final_mark(text):
    if not text or text[-1] not in ".!?":
        reject_entry("entry must end with . ! or ?")


def guard_letters(text):
    if not any(ch.isalpha() for ch in text):
        reject_entry("entry has no letters")


def guard_not_digits(text):
    if text.isdigit():
        reject_entry("entry is only digits")


def guard_not_punct(text):
    if not any(ch.isalnum() for ch in text):
        reject_entry("entry is only punctuation")


def guard_no_url(text):
    if "http://" in text or "https://" in text or "www." in text:
        reject_entry("entry contains a web address")


SENTRIES = (
    guard_no_url,
    guard_sleep_word,
    guard_sentence_count,
    guard_size,
    guard_present,
    guard_printable,
    guard_layout,
    guard_final_mark,
    guard_letters,
    guard_not_digits,
    guard_not_punct,
)


def check_all(text):
    for sentry in SENTRIES:
        sentry(text)


def main():
    check_all(ENTRY)
    GOAL.parent.mkdir(parents=True, exist_ok=True)
    GOAL.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
