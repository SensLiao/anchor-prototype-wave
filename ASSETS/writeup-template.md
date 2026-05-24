---
slug: {DATE}-{surface-or-element-slug}-writeup
title: {Surface Or Element Name} · {ANCHOR_NAME} Prototype Writeup
type: synthesis
status: concluded
confidence: medium
created: {DATE}
updated: {DATE}
track: {TRACK_LETTER}
related:
  - "[[{ANCHOR_DOC_SLUG}]]"
  - "[[{MODE_WRITEUP_SLUG}]]"
  - "[[{ROADMAP_SLUG}]]"
  - "[[{QUALITY_GATE_SLUG}]]"
sources:
  - "{OUTPUT_DIR}/{your-slug}/index.html (artifact)"
  - "{PRODUCTION_PAGE_PATH} (MVP function source)"
tags: [design-research, {WAVE_TAG}, prototype, hi-fi, {surface-or-element-tag}]
artifact_path: "{OUTPUT_DIR}/{your-slug}/"
self_grade:
  chassis: __
  mvp: __
  mode: __
  laws_ux: __
  innovation: __
  aggregate: __
approved_by: null   # filled by HUMAN at Gate 12 only
approved_date: null # filled by HUMAN at Gate 12 only
---

# {Surface Or Element Name} · {ANCHOR_NAME} Prototype Writeup

## §1 — Question

{ONE_SENTENCE_UX_PROBLEM_THIS_MOCK_SOLVES}

## §2 — MVP Function Coverage

Production source: `{PRODUCTION_PAGE_PATH}`

| Production section | Status in mock | Notes |
|---|---|---|
| {SECTION_1} | ✅ / 🟡 / ⬜ | |
| {SECTION_2} | ✅ / 🟡 / ⬜ | |
| {SECTION_3} | ✅ / 🟡 / ⬜ | |

**Coverage**: {COVERED_COUNT}/{TOTAL_COUNT} sections fully rendered.

## §3 — Visual Chassis Application

How this mock applies the {ANCHOR_NAME} chassis + assigned mode:

- **Typography**: {FONT_PRIMARY} for body, {FONT_MONO} for metadata labels
- **Radius / borders**: hairline borders only, radius {RADIUS_CARD}
- **Accent usage**: single mono `{ACCENT_VALUE}`; how it's deployed:
  {ACCENT_DEPLOYMENT}
- **Mode-specific patterns**:
  - {MODE_PATTERN_1}
  - {MODE_PATTERN_2}
  - {MODE_PATTERN_3}

## §4 — Laws of UX Applied

List 4-6 laws with one-line evidence per law:

1. **{LAW_1}** — {EVIDENCE_1}
2. **{LAW_2}** — {EVIDENCE_2}
3. **{LAW_3}** — {EVIDENCE_3}
4. **{LAW_4}** — {EVIDENCE_4}
5. (optional) **{LAW_5}** — {EVIDENCE_5}
6. (optional) **{LAW_6}** — {EVIDENCE_6}

## §5 — Innovation Notes

**Novel UX patterns applied** (if classified novel):
1. {NOVEL_PATTERN_1} — why this matters: {RATIONALE_1}
2. {NOVEL_PATTERN_2} — why this matters: {RATIONALE_2}
3. {NOVEL_PATTERN_3} — why this matters: {RATIONALE_3}

**Mature paradigms reused** (if classified mature):
1. {MATURE_PARADIGM_1} — source: {SOURCE_1}
2. {MATURE_PARADIGM_2} — source: {SOURCE_2}

## §6 — Self-grade Matrix + Gate Report

### Self-grade

| Dim | 0-10 | Notes |
|---|---|---|
| Visual chassis 一致性 | __ | |
| MVP function coverage | __ | |
| {MODE_ID} mode application quality | __ | |
| Laws of UX hit count | __ | {LAW_COUNT} laws applied |
| Innovation factor | __ | classification: {MATURE_OR_NOVEL} |

**Aggregate**: {AVG}/10

### Gate Report

| # | Gate | Status | Evidence |
|---|---|---|---|
| 1 | Style baseline compliance | PASS / WARN / BLOCK | {EVIDENCE} |
| 2 | Token discipline | PASS / WARN / BLOCK | {EVIDENCE} |
| 3 | Reference lineage | PASS / WARN / BLOCK | {EVIDENCE} |
| 4 | Accessibility | PASS / WARN / BLOCK | {EVIDENCE} |
| 5 | Reduced-motion | PASS / WARN / BLOCK | {EVIDENCE} |
| 6 | State coverage | PASS / WARN / BLOCK | {EVIDENCE} |
| 7 | Responsive | PASS / WARN / BLOCK | {EVIDENCE} |
| 8 | Performance budget | PASS / WARN / BLOCK | {EVIDENCE} |
| 9 | Anti-AI-slop | PASS / WARN / BLOCK | {EVIDENCE} |
| 10 | Boundary respect | PASS / WARN / BLOCK | {EVIDENCE} |
| 11 | UX checklist | PASS / WARN / pending | {EVIDENCE} |
| 12 | User final approve | pending human | awaiting reviewer |

## §7 — Open Questions

1. {OQ_1} — defer to Gate 12 reviewer
2. {OQ_2} — defer to Gate 12 reviewer
3. (optional) {OQ_3} — defer to Stage 4 visual composition pkg

## §8 — Cross-link

- Anchor: [[{ANCHOR_DOC_SLUG}]]
- Mode: [[{MODE_WRITEUP_SLUG}]]
- Roadmap: [[{ROADMAP_SLUG}]]
- Quality gate: [[{QUALITY_GATE_SLUG}]]
- Sibling surfaces in this wave: [[{SIBLING_1}]], [[{SIBLING_2}]], ...
- Source production page: `{PRODUCTION_PAGE_PATH}`
- Artifact: `{ARTIFACT_PATH}`

### Boundary self-check

- [ ] 0 files modified in `{production-source-glob}` (production frontend + backend)
- [ ] 0 changes to `{global-token-file}` / `tailwind.config.*` / root `package.json`
- [ ] 0 modifications to `{reference-repo-root}` or `{raw-immutable-root}`
- [ ] 0 changes to `{rules-doc}` or any ADR
- [ ] All output is in `{OUTPUT_DIR}/{your-slug}/` + this writeup file
