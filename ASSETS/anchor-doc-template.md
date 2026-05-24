---
slug: {DATE}-{anchor-name}-anchor
title: {ANCHOR_NAME} — {RESEARCH_TRACK_NAME} UI/UX Anchor
type: synthesis
status: active
confidence: high
created: {DATE}
updated: {DATE}
track: {RESEARCH_TRACK_LETTER}
related:
  - "[[{ROADMAP_SLUG}]]"
  - "[[{CHASSIS_WRITEUP_SLUG}]]"
  - "[[{MODE_1_SLUG}]]"
  - "[[{MODE_2_SLUG}]]"
  - "[[{MODE_N_SLUG}]]"
  - "[[{BOUNDARIES_SLUG}]]"
  - "[[{QUALITY_GATE_SLUG}]]"
sources:
  - "user directive {DATE} — '{ORIGINAL_USER_QUOTE}'"
  - "{CHASSIS_HTML_PATH} (artifact, READ ONLY)"
tags: [design-research, anchor, {RESEARCH_TRACK_TAG}, {ANCHOR_NAME_LOWER}]
domain: ui-references
---

# {ANCHOR_NAME} — {RESEARCH_TRACK_NAME} UI/UX Anchor

> **Customize**: replace every `{PLACEHOLDER}` below with project-specific
> values. The placeholders themselves correspond to SKILL.md §0.2 (project
> setup) and §4 (chassis values). Save the filled result as
> `{research-vault-path}design-research/{DATE}-{anchor-name}-anchor.md`.

## Disclaimer — Anchor, Not Production Merge

This document declares **product versioning intent**. It is NOT a production
merge. The live contract remains:

- `{rules-doc}` §UI/UX Direction (or equivalent project-level direction)
- `{global-token-file}` (the canonical token system)

This anchor sets the **target state** for promotion. Actual merge happens
via Gate 12 per surface (see {ROADMAP_SLUG} §Merge gate). **0 production
code changed by this anchor.**

## §1 — Product UI/UX Version Stack

| Version | What | Status | Authoritative source |
|---|---|---|---|
| **v1** | {V1_DESCRIPTION} — current production baseline | **LIVE in production** | `{rules-doc}` §UI/UX Direction + `{global-token-file}` |
| **v2** | **{ANCHOR_NAME}** — {V2_DESCRIPTION} | **ANCHORED {DATE}** | This document + chassis writeup + N mode writeups |
| **v3** | {V3_DESCRIPTION} — future premium tier | **Future / planned** | Not yet started; placeholder in roadmap |

**v1 → v2 trajectory**: from "{V1_TRAIT}" → "{V2_TRAIT}".

**v2 → v3 trajectory**: from "{V2_TRAIT}" → "{V3_TRAIT}".

## §2 — {ANCHOR_NAME} Chassis Definition

| Property | Value |
|---|---|
| **Artifact path** | `{CHASSIS_HTML_PATH}` (single HTML + tokens.candidate.css, do not edit) |
| **Writeup** | [[{CHASSIS_WRITEUP_SLUG}]] |
| **Lineage** | {LINEAGE_DESCRIPTION} (e.g., V1 visuals + V4 layout) |
| **Pitch** | "{ONE_LINE_PITCH}" |
| **Accent** | {ACCENT_STRATEGY} `{ACCENT_VALUE}`; **0 secondary accent** unless declared in OQ |
| **Surface palette** | {SURFACE_PALETTE_SUMMARY} — hairline borders `1px solid {BORDER_VALUE}` + {FONT_FAMILY} typography + radius {RADIUS_CARD} |
| **Token audit** | {TOKEN_COUNT} candidate tokens; **{NEEDS_ADR_COUNT} needs-ADR**; {SHIP_STATUS} |
| **Drops from prior iterations** | {DROPPED_PATTERNS} (saved-view chip / elevation shadow / secondary accent / etc.) |

## §3 — Mode Variants Application Layer

The chassis is the visual ground. **{STANDARD_MODE_COUNT} standard mode + {PREMIUM_MODE_COUNT} premium mode** are how the chassis applies to {N_SCENARIOS} different scenarios:

| Mode | Tier | Slug | Use case | Vibe |
|---|---|---|---|---|
| {MODE_1_NAME} | standard | [[{MODE_1_SLUG}]] | {MODE_1_USE_CASE} | {MODE_1_VIBE} |
| {MODE_2_NAME} | standard | [[{MODE_2_SLUG}]] | {MODE_2_USE_CASE} | {MODE_2_VIBE} |
| {MODE_3_NAME} | standard | [[{MODE_3_SLUG}]] | {MODE_3_USE_CASE} | {MODE_3_VIBE} |
| ... | ... | ... | ... | ... |
| **{PREMIUM_MODE_NAME}** | **PREMIUM** ⭐ | **[[{PREMIUM_MODE_SLUG}]]** | **{PREMIUM_USE_CASE}** | **{PREMIUM_VIBE}** |

### Surface → mode mapping

| Surface | Recommended mode |
|---|---|
| {SURFACE_P0} | {MODE_FOR_P0} |
| {SURFACE_P1} | {MODE_FOR_P1} |
| ... | ... |
| {SURFACE_MARQUEE} | **{PREMIUM_MODE_NAME}** ⭐ |

> Stage 3 surface spec **MUST** cite this mapping + the chosen mode's
> writeup as visual reference (per §6 invariant 5). **Premium tier is
> constrained** — only audit / governance / client-visible / high-value
> showcase, not "default + ornament".

## §4 — Anchor → Production Merge Path

```
1. Stage 2.1 Foundation Elements wave
   └─ each element spec lives under the chassis; cites ≥1 mode for context

2. Stage 2.2 Product Components wave
   └─ compound elements cite Stage 1 Lane D interaction specs

3. Stage 3 P0-PN surface spec → lo-fi → hi-fi → 11-gate
   └─ each surface picks mode per §3 + cites element/component library

4. Stage 4 per-surface 4-pkg (visual composition + production impl +
   verification + rollback)

5. Gate 12 user approve per surface → triggers single-surface
   {production-track-name} merge
   └─ actual edit: `{rules-doc}` UI/UX Direction (if needed) +
     `{global-token-file}` (if new token) + ship Stage 4 production impl PR

6. Cumulative P0-PN Gate 12 all PASS → anchor fully live
```

**Estimated wall-clock**: {WEEKS} weeks at {TEAM_SIZE} agent throughput.

## §5 — v3 Path Preview — v2 as v3 Precision Baseline

> Detail in [[{V3_AMENDMENT_SLUG}]]. Summary:

- v3 = next-tier tech stack ({V3_TECH_STACK_LIST}) applied as selective
  premium up-leveling on top of v2 mature surfaces
- v3 is NOT v2 replacement — v3 is delta on top of v2 baseline
- Trigger: v2 fully merged + product reaches mature business state
- Default assumption: v3 anchor doesn't start before {V3_EARLIEST_DATE}

### v3 upgrade ladder

```
Tier 0  v1 production           ← live now
Tier 1  v2 anchor + N modes     ← this anchor's target
Tier 2  v3-α single-surface pilot
Tier 3  v3-β selective rollout
Tier 4  v3 GA premium consolidation
```

### 7 hooks v2 must reserve for v3

| Hook | What v2 must do | What v3 unlocks |
|---|---|---|
| Token naming | `--<category>-<role>` not surface-locked | Global swap (dark / premium variant) |
| Element anatomy slot | Named slots not hard HTML | Premium ornament without breaking anatomy |
| Motion budget | Reduced-motion + data-state bound | Same budget, upgraded ease / choreography |
| Asset pipeline | v2 doesn't introduce brand assets | v3 `public/v3/` isolated directory |
| Persona × lens mapping | v2 surfaces already persona-aware | v3 per-persona premium differentiation |
| Metric collection | Gate 12 surfaces emit usage metrics | v3 A/B testable vs v2 |
| Component slot prop | `<Card premium={false}>` shape | `premium={true}` swap without breaking contract |

## §6 — Invariants (5 hard rules)

1. **v1/v2/v3 is version evolution, not LOCKED replacement** — v1 → v2
   still allows new tokens in `{global-token-file}` (via ADR); v2 → v3
   same.
2. **Anchor status ≠ production merge** — Gate 12 is the only merge
   channel. This doc itself touches no runtime.
3. **Chassis HTML artifact is a study source, not a contract** — the live
   contract remains `{global-token-file}` + `{rules-doc}` §UI/UX
   Direction.
4. **Stage 2.1+ wave, element specs MUST cite chassis** ({FONT} / radius
   {RADIUS} / hairline / mono accent).
5. **Stage 3 surface spec MUST cite §3 mapping + chosen mode writeup** —
   no spec is allowed to ignore the mode mapping.

## §7 — Open Questions

- **OQ-1**: {OQ_1_TEXT} → **Suggestion**: {OQ_1_SUGGESTION}
- **OQ-2**: {OQ_2_TEXT} → **Suggestion**: {OQ_2_SUGGESTION}
- **OQ-3**: {OQ_3_TEXT} → **Suggestion**: {OQ_3_SUGGESTION}
- **OQ-4**: {OQ_4_TEXT} → **Suggestion**: {OQ_4_SUGGESTION}

## §8 — Cross-link

- Overall strategy: [[{STRATEGY_SLUG}]]
- Master roadmap: [[{ROADMAP_SLUG}]]
- Chassis writeup: [[{CHASSIS_WRITEUP_SLUG}]]
- N mode writeups: [[{MODE_1_SLUG}]] / [[{MODE_2_SLUG}]] / ... / [[{MODE_N_SLUG}]]
- Premium tier (if any): [[{PREMIUM_MODE_SLUG}]]
- Boundary rules: [[{BOUNDARIES_SLUG}]]
- Quality gate: [[{QUALITY_GATE_SLUG}]]
- v3 strategic amendment: [[{V3_AMENDMENT_SLUG}]]
