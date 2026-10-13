# kevyn-clinicalnote-skill

A reusable AI-agent skill for converting clinical guidelines and medical papers into Kevyn's preferred compact note style.

## Skills in this repo

| Skill | Path | What it does |
| --- | --- | --- |
| **kevyn-clinicalnote-skill** | [`SKILL.md`](./SKILL.md) | Turns a clinical source into a compact clinician-facing extraction note — recommendation-first, numerically precise, source-faithful. |
| **kevyn-learning-note-pipeline** | [`kevyn-learning-note-pipeline/SKILL.md`](./kevyn-learning-note-pipeline/SKILL.md) | Runs the seven-step vault pipeline around a note: place the source, bank and verify the figures, write the note, wire it into the hub and index, pass the validation ritual, then commit and push with a `MATCH` confirmation. Ships a read-only validator in `scripts/validate_note.py`. |

The first skill writes a note. The second lands it.

## Use it for

- Clinical practice guidelines
- Consensus statements
- Randomized trials
- Cohort studies
- Systematic reviews / meta-analyses
- High-yield revision notes
- Conference / teaching preparation

## Style

The note skill produces **clinical extraction notes**, not conventional summaries:

- recommendation first
- action before explanation
- short bullets
- exact doses, thresholds, timing, targets, and exceptions
- key evidence only
- source-faithful recommendation strength
- minimal narrative prose

## Invocation

Examples:

- `Use kevyn-clinicalnote-skill on this paper.`
- `Create a Kevyn-style note from this guideline.`
- `Apply kevyn-clinicalnote-skill and keep only clinically actionable information.`
- `Run the learning-note pipeline on this reading and push it.`
- `Audit this vault note with the pipeline validator.`

See [`SKILL.md`](./SKILL.md) for the complete instructions.
