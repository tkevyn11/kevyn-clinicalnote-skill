#!/usr/bin/env python3
"""Read-only validator for a Kevyn vault note.

Runs the eleven checks described in ../reference/validation.md and reports every
problem it finds. It never edits a file.

    python validate_note.py path/to/note.md
    python validate_note.py path/to/note.md --vault /path/to/vault

Exit code 0 means a clean run. Exit code 1 means at least one problem.
"""

import argparse
import collections
import os
import re
import sys

REQUIRED_KEYS = ["id", "title", "type", "created", "updated", "status", "tags", "sources"]

REQUIRED_SECTIONS = [
    "## Core Idea",
    "## Mental Models",
    "## Anti-patterns",
    "## Worked Example",
    "## Key Takeaways",
    "## Open Questions / Source Defects",
    "## Related Notes",
    "## Sources",
]

PLACEHOLDERS = ["TODO", "FIXME", "None yet", "not supplied yet", "Pending", "placeholder"]

# Patterns that bulk edits have corrupted in this vault before. Extend as new ones appear.
TYPO_PATTERNS = [r"clarify-is-key", r"integating-", r"from-discovery-to-decisions"]

LEDGER_HEADING = "## Open Questions / Source Defects"
LEDGER_END = "## Related Notes"

MARKER_GLYPHS = "\u2b50\u26a0\ufe0f"  # star, warning sign, variation selector


def find_vault(note_path):
    """Walk up from the note until a directory named 'vault' is found."""
    current = os.path.dirname(os.path.abspath(note_path))
    while True:
        if os.path.basename(current) == "vault":
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def index_vault(vault):
    """Return (set of vault-relative paths, counter of filenames) for link resolution."""
    paths, stems = set(), collections.Counter()
    for root, _dirs, files in os.walk(vault):
        for name in files:
            if name.lower().endswith(".md"):
                full = os.path.join(root, name)
                rel = os.path.relpath(full, vault).replace("\\", "/")[:-3]
                paths.add(rel)
                stems[name[:-3]] += 1
    return paths, stems


def split_units(text):
    """Yield the units a bold span must not cross: table rows, quote paragraphs, paragraphs.

    Consecutive blockquote lines join into one unit, because a quoted source's own
    emphasis wraps across lines and each span still has to balance inside the quote.
    A bare '>' line ends the quote paragraph.
    """
    units = []
    buffer = []

    def flush():
        if buffer:
            units.append(" ".join(buffer))
            buffer.clear()

    for line in text.split("\n"):
        if line.startswith("|"):
            flush()
            units.append(line)
        elif line.startswith(">"):
            if line.strip() == ">":
                flush()
            else:
                buffer.append(line)
        elif line.startswith("#") or line.strip() == "":
            flush()
        else:
            buffer.append(line)
    flush()
    return units


def flat_bold_problems(unit):
    """Return the flat-bold faults inside one unit (parity, then nesting)."""
    problems = []
    if unit.count("**") % 2:
        problems.append(("bold parity", unit[:110]))
    open_span = False
    i = 0
    while i < len(unit) - 1:
        if unit[i:i + 2] == "**":
            if open_span:
                following = unit[i + 2:i + 3]
                if following and (following.isalnum() or following in MARKER_GLYPHS):
                    problems.append(("nested bold", unit[max(0, i - 70):i + 70]))
                open_span = False
            else:
                open_span = True
            i += 2
        else:
            i += 1
    return problems


def validate(note_path, vault):
    problems = []
    with open(note_path, encoding="utf-8") as handle:
        text = handle.read()
    lines = text.split("\n")
    name = os.path.basename(note_path)

    def report(check, detail):
        problems.append((check, detail))

    # 1. frontmatter and structure
    if not lines or lines[0].strip() != "---":
        report("frontmatter", "no opening ---")
        body = lines
    else:
        try:
            end = lines.index("---", 1)
        except ValueError:
            report("frontmatter", "no closing ---")
            end = 0
        keys = [l.split(":")[0] for l in lines[1:end] if re.match(r"^[a-z_]+:", l)]
        if keys != REQUIRED_KEYS:
            report("frontmatter", f"key order is {keys}")
        body = lines[end + 1:]

    h1 = [l for l in body if l.startswith("# ") and not l.startswith("## ")]
    if len(h1) != 1:
        report("structure", f"H1 count is {len(h1)}")
    for section in REQUIRED_SECTIONS:
        if section not in body:
            report("structure", f"missing section {section}")

    # 2. wikilinks resolve
    paths, stems = index_vault(vault) if vault else (set(), collections.Counter())
    for match in re.finditer(r"\[\[([^\]|]+)(\|[^\]]*)?\]\]", text):
        target = match.group(1).strip()
        if target in paths or target.split("/")[-1] in stems:
            continue
        report("wikilink", f"[[{target}]]")

    # 3. embedded figures exist
    if vault:
        for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
            candidate = os.path.join(vault, match.group(1).replace("/", os.sep))
            if not os.path.exists(candidate):
                report("figure", match.group(1))

    # 4. defect numbering
    ledger = ""
    if LEDGER_HEADING in text and LEDGER_END in text:
        ledger = text.split(LEDGER_HEADING, 1)[1].split(LEDGER_END, 1)[0]
        numbers = [int(m.group(1)) for m in re.finditer(r"^(\d+)\. ", ledger, re.M)]
        if numbers != list(range(1, len(numbers) + 1)):
            report("ledger numbering", f"{numbers}")
        duplicates = [n for n, c in collections.Counter(numbers).items() if c > 1]
        if duplicates:
            report("ledger duplicates", f"{duplicates}")
        for match in re.finditer(r"defects? (\d+)", text):
            if int(match.group(1)) > len(numbers):
                report("dangling defect ref", f"{match.group(1)} (max {len(numbers)})")
    else:
        report("ledger", "section not found, numbering not checked")

    # 5. placeholder text
    for token in PLACEHOLDERS:
        if token in text:
            report("placeholder", token)

    # 6. Related Notes hygiene
    if LEDGER_END in text and "## Sources" in text:
        related = text.split(LEDGER_END, 1)[1].split("## Sources", 1)[0]
        links = [m.group(1) for m in re.finditer(r"^\s*-\s*\[\[([^\]|]+)", related, re.M)]
        duplicated = [k for k, c in collections.Counter(links).items() if c > 1]
        if duplicated:
            report("related duplicates", f"{duplicated}")
        if any(l.split("/")[-1] == name[:-3] for l in links):
            report("related self-link", name)

    # 7. blank-line separation
    for i, line in enumerate(body):
        if (line.startswith("#") or line.startswith(">")) and i + 1 < len(body):
            following = body[i + 1]
            if following.strip() and not following.startswith(("#", ">", "|")):
                report("blank line", f"line {i + 2}: nothing after {line[:45]!r}")

    # 8 and 9. flat bold
    for unit in split_units(text):
        for check, detail in flat_bold_problems(unit):
            report(check, detail)

    # 10. per-item ledger balance
    items = [x for x in re.split(r"(?m)^(?=\d+\. )", ledger) if re.match(r"^\d+\. ", x)]
    for item in items:
        number = re.match(r"^(\d+)\. ", item).group(1)
        joined = " ".join(l.strip() for l in item.split("\n"))
        for check, detail in flat_bold_problems(joined):
            report(f"ledger item {number}: {check}", detail)

    # 11. known typos
    for pattern in TYPO_PATTERNS:
        if re.search(pattern, text):
            report("known typo", pattern)

    return name, len(items), problems


def main():
    parser = argparse.ArgumentParser(description="Validate a Kevyn vault note. Read-only.")
    parser.add_argument("note", help="path to the note to validate")
    parser.add_argument("--vault", help="vault root; detected by walking up when omitted")
    args = parser.parse_args()

    if not os.path.isfile(args.note):
        print(f"not a file: {args.note}")
        return 2

    vault = args.vault or find_vault(args.note)
    if not vault:
        print(f"warning: no 'vault' directory above {args.note}; link and figure checks limited")

    name, item_count, problems = validate(args.note, vault)
    print(f"{name}: {item_count} ledger items, {len(problems)} problems")
    for check, detail in problems:
        print(f"  [{check}] {detail}")
    if not problems:
        print("CLEAN")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
