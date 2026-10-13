---
name: kevyn-learning-note-pipeline
description: Run the Kevyn learning-note pipeline end to end — place a source against its syllabus, bank and verify its figures, write the note, wire it into the hub and index, pass the validation ritual, then commit and push with a MATCH confirmation. Use when adding a course reading, video, dialogue, PDF, or figure set to the kevbrainllmwiki vault, when a note must land wired and validated, or when auditing a vault note for broken links, figure drift, or nested bold.
---

# Kevyn Learning-Note Pipeline

`kevyn-learning-note` writes the note. This skill lands it.

The pipeline is seven steps, run once per source. Each step ends on a completion criterion — a
condition you can check without judgement. Run them in order; the order is what keeps a note from
arriving wired-but-unvalidated or validated-but-unpushed.

## 1. Load the trail

Read the vault's handoff doc first, then load `kevyn-learning-note`.

The handoff carries **state** — repo paths, the current course and module, which item is next, the
environment quirks, and the open disagreements. The note skill carries **style and structure**. This
skill carries **procedure**.

Anchors to read before touching anything:

| Anchor | What it holds |
| --- | --- |
| `docs/dsh-session-handoff.md` in the vault repo | state, paths, commands, open rulings |
| the course hub in `vault/20-knowledge/<domain>/` | the verified item list and figure table |
| the domain `index.md` | where the note must appear |

**Done when** you can state the course, the module, and the current item number without guessing —
or you have written down that the syllabus for that module is not captured.

## 2. Place the source

The sender puts the source's own title on the first line. Match it against the captured syllabus
before writing a word.

- **Exact match** → record the position as verified, with the item number, type, and duration.
- **No match** → the position is **UNVERIFIED**. Record the inference you can defend, file the note at
  programme level, and put the question to the sender. Do not guess a module.
- **Ambiguous title** → name the competing candidates in the ledger and ask.

**Done when** the note's header states a verified position, or states UNVERIFIED plus the evidence and
the open question.

### Stop-and-ask triggers

Ask the sender, and keep working on everything that does not depend on the answer:

- a source title matching no captured syllabus item;
- two sources in one module whose titles collide with each other's headings;
- a source contradicting an earlier source on a fact the vault relies on;
- anything that would relabel, rename, or restructure existing vault content.

## 3. Bank the figures

Store first, write later. Figures arrive attached, inline, or late.

1. Copy each file to the course asset folder under
   `vault/90-assets/microsoft-ai-product-manager/course-N/`.
2. Name it `course-N-module-M-<content-slug>.png` — describe the content, and embed the module number
   once the module is known. Use a module-neutral name while the position is UNVERIFIED, and rename on
   the ruling.
3. **SHA-256 verify** the stored copy against the supplied file and record the digest, byte size, and
   pixel dimensions.
4. Convert WebP to PNG with Pillow before storing, preserving dimensions, and record that the stored
   file is a re-encode so its digest is not any original's digest.
5. **Transcribe** the figure into the note: every label, every number, and the absence of a caption,
   legend, or attribution.
6. Compare the figure against its prose. Mismatched counts, substituted labels, and a figure that
   serves a different claim are all ledger entries.

Positive rules that decide the awkward cases:

- A figure referenced but not received stays **referenced-but-not-received**. Say so, store nothing,
  and update the note when the file arrives.
- A figure described in prose with no image reference is **named-and-withheld**.
- Outside knowledge used to check a named product goes in the body under `External context:`, never in
  the figure's provenance.

**Done when** every supplied figure is stored, hashed, embedded at its marked position, and
transcribed — and every unsupplied figure is named as such in the provenance table.

## 4. Write the note

Follow `kevyn-learning-note` for voice and structure, and the vault's house sections for the rest.

Frontmatter keys in this order: `id`, `title`, `type`, `created`, `updated`, `status`, `tags`,
`sources`. Then one `# Title`. Then the position line. Then `## Core Idea`, the framework sections,
`## Mental Models`, `## Anti-patterns`, `## Worked Example`, `## Key Takeaways`,
`## Open Questions / Source Defects`, `## Related Notes`, `## Sources`.

House rules that the note skill does not carry:

- **Flat bold.** One bold span per sentence; never a span inside a span. Write the whole sentence bold
  or bold nothing in it.
- **Wikilinks resolve by file path**, not by `id`.
- **Per-note figure numbering** starts at 1 in every note; the hub's figure table numbers globally.
- Quote exactly. Keep every number, threshold, tool name, and hedge.
- Rank findings with the vault's markers, and keep the ranking honest.

**Done when** the note has valid frontmatter, one H1, every required section, a numbered defect
ledger, and no unresolved placeholder.

## 5. Wire it

A note nobody can reach is a note nobody has.

| Target | The edit |
| --- | --- |
| Course hub, `## Course Sources` | one row: title, type, position, wikilink |
| Course hub, the module's findings block | one or more `→` paragraphs carrying the note's findings |
| Course hub, `Figures — Module N Provenance` | one row per stored figure, with size and digest |
| Course hub, module structure row | update the noted-item count |
| `index.md` | one bullet under the course hub, naming the position and the note's contribution |

**Done when** the note is reachable from `index.md` and from its hub, and every figure it embeds
appears in the hub's figure table.

## 6. Run the ritual

```bash
python scripts/validate_note.py path/to/note.md
```

The script is read-only and reports every problem it finds. `reference/validation.md` explains what
each check is for, which is what you need when a check fires.

**Done when** the script reports zero problems and exits 0.

## 7. Land it

```bash
git add -A
git commit -F <message-file>
git push origin main
git rev-parse HEAD
git ls-remote origin main
git status --short
```

Write the commit message to a file and pass it with `-F`; inline messages with quoted phrases break
argument parsing. Report the commit hash and subject, `MATCH: True` or `False`, the file list, and
anything still outstanding.

A push that reports success is not proof. Compare `rev-parse HEAD` against `ls-remote origin main`
every time. A push that writes progress to stderr exits non-zero while succeeding, so read the
comparison, not the exit code.

**Done when** local `HEAD` equals the remote's `main`, the tree is clean, and the report names the
commit and the outstanding items.

## The defect ledger

Every finding lands in `## Open Questions / Source Defects` as a numbered item. It is the vault's
most valuable section, because it is the only place contradictions between sources are caught.

An entry earns its number when it is one of these:

| Class | Example |
| --- | --- |
| **Internal contradiction** | the reading promises anticipation in one section and denies it in another |
| **Figure against prose** | the text lists seven stages and the diagram draws six |
| **Cross-source conflict** | two sources give different definitions of the same term |
| **Named but not shown** | a grid, canvas, or template named and never drawn |
| **Gap in the source** | a metric required and never defined |
| **Vocabulary collision** | a term that already means something else in the vault |
| **Production defect** | a missing sentence break, an inconsistent heading case, no conclusion |

Number sequentially. Never renumber a published item: cross-references from other notes point at
these numbers, and the checker fails on a dangling reference.

Record, then ask. A contradiction is not yours to resolve.

## Working with the sender

- Report what changed, where, what was verified, and what was not.
- When a rule and a request collide, follow the rule and say why.
- Flag a recurring defect in your own output once per run, not continuously.
- A source the sender judged too thin to send is not a gap to fill.
