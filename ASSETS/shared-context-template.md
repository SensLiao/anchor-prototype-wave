# {WAVE_NAME} — Shared Context

> {RESEARCH_TRACK_NAME} Stage 3 hi-fi prototype wave. All subagents must read this
> document as the execution contract before producing any HTML or writeup.
>
> **Customize**: replace `{PLACEHOLDER}` tokens with project values per
> SKILL.md §0.2. The orchestrator (main thread) writes this file ONCE
> before spawning subagents; every subagent reads it.

## 1. {ANCHOR_NAME} Visual Contract (non-negotiable)

- **Typography**: {FONT_PRIMARY} ({WEIGHTS_PRIMARY}); {FONT_MONO}
  {WEIGHT_MONO} uppercase {MONO_SIZE} tracking {MONO_TRACKING} (for
  metadata / lane labels only)
- **Radius**: {RADIUS_CARD} (cards / inputs), {RADIUS_CHIP} (chips / pills)
- **Borders**: `1px solid {BORDER_HAIRLINE_VALUE}` hairline. **No elevation
  shadow** like `0 8px 16px`. Micro shadow allowed:
  `0 1px 2px {SHADOW_MICRO_VALUE}`.
- **Accent**: **{ACCENT_STRATEGY}** ({ACCENT_VALUE}). **0 secondary accent**
  unless declared in §1.1 below. Status: {STATUS_AMBER_RULE},
  {STATUS_RED_RULE}.
- **Surfaces**:
  - page-bg `{SURFACE_PAGE}`
  - card-bg `{SURFACE_CARD}`
  - sunken-bg `{SURFACE_SUNKEN}`
  - muted-bg `{SURFACE_MUTED}`
- **Text**: primary `{TEXT_PRIMARY}`, secondary `{TEXT_SECONDARY}`,
  tertiary `{TEXT_TERTIARY}`, mono-label `{TEXT_MONO_LABEL}`
- **Spacing scale**: {SPACING_SCALE} (e.g., 4 / 8 / 12 / 16 / 20 / 24 / 32 / 48)
- **Banned tokens**: {BANNED_LIST} (e.g., glass / blur / aurora / glow shadow /
  dark mode / rainbow status / decorative gradient)

### 1.1 Secondary accent rule (optional)

{IF_SECONDARY_ACCENT_RULE_OR_NONE}

## 2. File constraints

- Output **single self-contained HTML** + inline `<style>` + minimal vanilla
  JS only when required for interaction state demo
- **{FONT_PRIMARY} via Google Fonts `@import`** in CSS (the only allowed
  external dependency)
- All tokens defined in `:root` — 0 inline hex literals scattered through
  the file
- Target HTML length **{HTML_LENGTH_RANGE}** (not strictly enforced;
  information density > line count)
- Top banner: `[SURFACE/ELEMENT NAME] · {ANCHOR_NAME} Prototype ·
  {MODE_ID} · {ALIGNMENT_NOTE}`
- Bottom footer: route path + MVP function checklist (which production
  features have visual representation in the mock)

## 3. Hard boundaries

| Write to | NEVER touch |
|---|---|
| `{PROTOTYPE_OUTPUT_DIR}/{your-slug}/index.html` | `{PROTOTYPE_OUTPUT_DIR}/_archive/*` (read-only) |
| `{WRITEUP_DIR}/{date-slug}-writeup.md` | `{PRODUCTION_SOURCE_GLOB}` (production source) |
| | `{GLOBAL_TOKEN_FILE}`, `tailwind.config.*`, root `package.json` |
| | `{RULES_DOC}`, any ADR file |
| | `{REFERENCE_REPO_ROOT}` |
| | `{RAW_IMMUTABLE_ROOT}` |

## 4. Mandatory pre-read

- `{ANCHOR_DOC_PATH}` ({ANCHOR_NAME} declaration)
- `{CHASSIS_WRITEUP_PATH}` (visual chassis writeup)
- `{CHASSIS_HTML_PATH}` (chassis HTML reference, READ ONLY)
- `{TOKENS_CANDIDATE_PATH}` (token reference, READ ONLY)
- Your assigned mode writeup: see anchor §{MODE_MAPPING_SECTION}

## 5. MVP function alignment (surface only)

- Must read `{PRODUCTION_PAGE_PATH}` to extract real UI structure
- Must scan `{PRODUCTION_MODULE_DIR}` lightly for state shape
- Mock must render **every prod-visible section** (no half-done mocks; if
  prod has 5 sections, mock has 5 sections)
- Mature functions use mature paradigms; novel functions (agent canvas /
  trace / governance / outbound capability) should apply innovation UX
- Implicit creative references (do **not** cite URLs inside the HTML):
  - dribbble.com/tags/ui-ux-design
  - lawsofux.com (Hick's / Fitts's / Miller's / Aesthetic-Usability /
    Doherty Threshold / Recognition over Recall / etc.)
  - List which Laws of UX you applied in the writeup §4

## 6. Self-grade (every subagent fills the writeup §6 matrix)

| Dim | 0-10 self-grade | notes |
|---|---|---|
| Visual chassis 一致性 ({FONT_PRIMARY} / radius {RADIUS_CARD} / hairline / mono accent) | | |
| MVP function coverage completeness | | |
| {MODE_ID} mode application quality | | |
| Laws of UX hit count (list which) | | |
| Innovation factor (mature 5-7; novel 8-10) | | |

## 7. Writeup template (every subagent writes one)

Path: `{WRITEUP_DIR}/{date-slug}-{your-slug}-writeup.md`

Frontmatter:

```yaml
---
slug: {date-slug}-{your-slug}-writeup
title: {Surface Name} · {ANCHOR_NAME} Prototype Writeup
type: synthesis
status: concluded
confidence: medium
created: {DATE}
updated: {DATE}
track: {RESEARCH_TRACK_LETTER}
related:
  - "[[{ANCHOR_DOC_SLUG}]]"
  - "[[{MODE_WRITEUP_SLUG}]]"   ← your assigned mode
  - "[[{ROADMAP_SLUG}]]"
sources:
  - "{PROTOTYPE_OUTPUT_DIR}/{your-slug}/index.html (artifact)"
  - "{PRODUCTION_PAGE_PATH} (MVP function source)"
tags: [design-research, {WAVE_TAG}, prototype, hi-fi, {surface-tag}]
artifact_path: "{PROTOTYPE_OUTPUT_DIR}/{your-slug}/"
---
```

Body sections (in order):

1. Question (1 sentence — what UX problem this mock solves)
2. MVP Function Coverage (production feature list × mock implementation
   status)
3. Visual Chassis Application (how it applies {ANCHOR_NAME} + your assigned
   mode)
4. Laws of UX Applied (list 4-6 laws with one-line explanation each)
5. Innovation Notes (novel parts: how innovated; mature parts: how reused)
6. Self-grade Matrix (the §6 table)
7. Open Questions (1-3 unanswered design questions, defer to Gate 12)
8. Cross-link

## 8. Downstream handoff

This prototype enters the {ROADMAP_SLUG} surface × stage matrix at Stage 3
hi-fi. Stage 4 visual composition pkg will mechanically extract token diff
+ element reuse map from your mock, so:

- Use clear class names
- Token-ize all values (no scattered hex literals)
- Keep element boundaries visually distinct
- Annotate non-obvious decisions with HTML comments
