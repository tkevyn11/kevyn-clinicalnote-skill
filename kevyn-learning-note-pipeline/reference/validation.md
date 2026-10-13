# The validation ritual

Eleven checks. Each one exists because it has caught real breakage in the vault. Run them all; a
clean run on nine of eleven is how a broken note ships.

## 1. Frontmatter and structure

Keys present, in order, and no duplicates: `id`, `title`, `type`, `created`, `updated`, `status`,
`tags`, `sources`. Exactly one `# Title`, below the frontmatter and above the first `##`.

Every required section present: `Core Idea`, `Mental Models`, `Anti-patterns`, `Worked Example`,
`Key Takeaways`, `Open Questions / Source Defects`, `Related Notes`, `Sources`.

*Why:* an Obsidian dataview query and the hub's index both depend on the key order, and a missing
section is invisible until someone looks for it.

## 2. Wikilinks resolve

Every `[[target]]` resolves against a walk of the whole vault — by vault-relative path first, then by
unique filename anywhere in the tree.

*Why:* wikilinks resolve by **file path**, not by `id`. A link to a bare slug that is not a filename
renders as a dead link in Obsidian and reads as fine in the source.

## 3. Embedded figures exist

Every `![](...)` path resolves on disk, relative to the vault root.

*Why:* a figure moved or renamed by a later edit leaves the note rendering an empty box.

## 4. Defect numbering

The ledger runs `1..N`, ascending, no duplicates, and no gaps. Every `See defect N` reference points
at an existing item.

*Why:* cross-references from other notes cite these numbers, so renumbering silently breaks them. The
dangling-reference check is the one that catches a reference to an item that was cut.

## 5. No placeholder text

Search for `TODO`, `FIXME`, `None yet`, `Pending`, `not supplied yet`, and a bare `placeholder`.

*Why:* a note is sometimes committed in two passes, and the first pass leaves a marker behind.

## 6. Related Notes hygiene

No duplicate link in the section, and no link from a note to itself.

*Why:* duplicates arrive from bulk edits, and a self-link is how a rename goes wrong.

## 7. Blank-line separation

A heading or a blockquote is followed by a blank line before any paragraph, table, or list.

*Why:* a targeted `edit` can remove a newline and join a heading to the paragraph beneath it. Markdown
still renders it, so nothing looks wrong — but the heading stops being a heading in some parsers.

## 8. Flat bold — parity

Within every paragraph unit and every table row, the count of `**` markers is even.

A **unit** is the largest span a single bold span may cross: a run of consecutive lines, with blank
lines and headings ending it. Two boundary rules decide the cases that look wrong:

- **Blockquote lines join.** A quoted source's own emphasis wraps across lines, so `> … **word` on one
  line and `> … word**` on the next is one balanced span, not two faults. Join consecutive `>` lines
  into one unit; a bare `>` line ends the unit.
- **Table rows stand alone.** A row's bold must balance inside the row.

*Why:* an odd count means a bold span runs past the end of the block and silently bolds whatever
follows, including the next section's heading. A checker that skips blockquote lines reports clean on
a note whose quotes are broken, which is worse than not checking them — the region looks verified.

## 9. Flat bold — nesting

Scan each unit left to right, tracking whether a span is open. A `**` encountered while a span is
already open, where the next character is alphanumeric or a marker glyph, is a nested span.

*Why:* parity alone passes `**outer **inner** rest**`, because that is four markers. Nesting is the
defect the hand-authored notes actually produce, and it is invisible in the rendered output while
making the emphasis unpredictable.

Markup written inside an inline code span is text, not markup, so the checker masks those spans before
scanning. A note that quotes a defect in order to name it — as the handoff doc quotes the nested-bold
pattern — reports clean.

The repair is a rewrite, not a script. Delete the inner pair by hand and re-read the sentence; a
mechanical "delete the pair" pass cannot tell an inner closer from the outer one, and it has removed
outer closers and unbalanced whole lists.

## 10. Per-item ledger balance

Split the ledger on `^N. ` and re-run checks 8 and 9 inside each item.

*Why:* ledger items are contiguous with no blank lines between them, so the whole list is one
paragraph unit. One item's imbalance cascades into false reports on every item after it, and a
per-item pass localises the fault to the item that caused it.

## 11. Known typos

Grep for the slugs that bulk edits have corrupted before: a misspelled note title used as a link, a
truncated word, and a retired note name.

*Why:* a renamed note leaves its old name in every link that referenced it.

## Reading the output

The script prints one line per problem with the file, the check, and the offending text. Work the
list top to bottom and re-run — repairs in one check can create a problem in another.
