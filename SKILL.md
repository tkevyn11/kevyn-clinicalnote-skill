---
name: kevyn-clinicalnote-skill
description: Convert clinical guidelines, consensus documents, trials, systematic reviews, and medical papers into compact clinician-facing notes in Kevyn's preferred style: recommendation-first, action-focused, numerically precise, source-faithful, and easy to scan. Use when asked to make clinical notes, guideline notes, paper notes, revision notes, or concise evidence summaries for rapid recall.
---

# Kevyn ClinicalNote Skill

Turn a medical source into a **clinical extraction note**, not a conventional prose summary.

The goal is to remove narrative noise while preserving everything that changes clinical understanding or management.

## Core Style

- **Recommendation first.**
- **Action before explanation.**
- Use short bullets, not long paragraphs.
- Preserve exact:
  - doses
  - thresholds
  - timing
  - targets
  - contraindications
  - exceptions
  - recommendation strength
  - key outcome statistics
- Use `→` for decisions, consequences, and practical implications.
- Organize by the source's own major clinical headings whenever possible.
- Keep important uncertainty visible: `controversial`, `insufficient evidence`, `conditional`, `low certainty`, etc.
- Prefer clinician-facing language over academic prose.
- If a sentence can be safely shortened without losing clinical meaning, shorten it.

## What To Remove

Usually omit or heavily compress:

- long background sections
- historical discussion
- repeated rationale
- generic epidemiology that does not change management
- detailed methodology unless it affects interpretation
- exhaustive author discussion
- low-yield mechanistic explanation

Do **not** remove information merely because it is inconvenient. Keep it if it changes interpretation, safety, applicability, or management.

## Source Fidelity Rules

- Treat the uploaded/source paper as the authority for the note.
- Preserve its terminology, scope, framing, and level of certainty.
- Do not silently replace an older recommendation with newer knowledge.
- Do not upgrade `suggest` to `recommend`, or low-quality evidence to high certainty.
- Do not merge traumatic and spontaneous ICH evidence unless the source itself does so.
- If outside knowledge is added, label it clearly as an update or external context.
- If the source does not support a point, say so.

## Extraction Priority

Extract in this order:

1. **Clinical recommendation / action**
2. **Who it applies to**
3. **Dose / threshold / target / timing**
4. **Important exception or contraindication**
5. **Monitoring / reassessment**
6. **Evidence strength or controversy**
7. **Only the most decision-relevant supporting data**
8. **Clinical implication**

## Preferred Structure — Guideline / Consensus

```md
# [Paper / Guideline]

## [Clinical topic]

- Recommendation:
  - **[Action]**
  - [Dose / threshold / timing]
  - [Target]
- Consider:
  - [Important modifier]
- Avoid:
  - [What should not be done]
- Monitoring:
  - [Reassessment]
- Evidence / caveat:
  - [Only if clinically important]
```

### Example style

```md
## Warfarin / VKA

- Stop VKA.
- ICH + clinically relevant anticoagulation → **urgent reversal**.
- **4F-PCC + vitamin K**
- Vitamin K:
  - **10 mg IV**
- Target:
  - **INR <1.4**
- Repeat INR:
  - 15–60 min after PCC
  - then 6–8 hourly
- FFP:
  - use if PCC unavailable
- Avoid:
  - routine rFVIIa
```

## Preferred Structure — RCT / Cohort / Meta-analysis

Do not reproduce the whole paper. Capture design only to the level needed to interpret the result.

```md
# [Paper]

## Study

- Design: [RCT / cohort / meta-analysis]
- Population: [clinically relevant inclusion]
- Comparator: [if important]

## Main findings

- [Outcome]:
  - **[Result]**
- [Outcome]:
  - **[Result]**

## Clinical implication

- [What this result changes]
- BUT:
  - [major limitation / harm / uncertainty]
```

### Example style

```md
## Main findings

- Hemostatic efficacy:
  - **67.0% vs 53.1%**
- Thrombotic events:
  - **10.3% vs 5.6%**
- Mortality:
  - no significant difference

## Clinical implication

- Better hemostatic control
- BUT ↑ thrombotic events
- No proven mortality benefit
```

## Compression Rules

Use these transformations:

- `is associated with an increased risk of` → `→ ↑ risk of`
- `there was no statistically significant difference` → `→ no significant difference`
- `should be considered in patients who...` → `Consider if:`
- `is not recommended` → `**Not recommended**`
- long drug sentences → `Drug → action → dose → caveat`

Do not compress so aggressively that the note becomes ambiguous.

## Numbers

Numbers are high priority.

Always preserve clinically relevant:

- dose and unit
- route
- frequency
- timing window
- INR / platelet / fibrinogen / assay thresholds
- target values
- effect sizes and confidence intervals when important
- event rates when they materially affect interpretation

Never invent missing units, timing, or thresholds.

## Recommendation Strength

Maintain the source's wording:

- `recommend` → firm recommendation
- `suggest` → weaker recommendation
- `may consider` → optional / uncertain
- `insufficient evidence` → keep explicit
- expert consensus → label as consensus, not trial evidence

## Notes For Clinical Use

The finished note should:

- be readable in **30–90 seconds per section**
- allow rapid retrieval during study, teaching, or preparation
- make the management-changing facts visually obvious
- remain understandable without reopening the full paper
- still be traceable back to the source

## Final Quality Check

Before finishing, ask:

1. Did I preserve the source's meaning and certainty?
2. Did I keep every clinically important number?
3. Did I capture important exceptions?
4. Did I remove unnecessary prose?
5. Can a clinician scan this quickly?
6. Did I avoid adding unsupported knowledge?
7. Does the note read like **Kevyn's compact clinical extraction notes**, not an AI-generated literature summary?

If not, revise again.
