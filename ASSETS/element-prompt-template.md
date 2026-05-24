# Element Subagent Prompt — `{ELEMENT_SLUG}` ({ELEMENT_CATEGORY})

> **Role**: You are a Stage 2.1 foundation element subagent for the
> `{WAVE_NAME}` wave. Your job is to produce ONE element showcase HTML +
> ONE research writeup for `{ELEMENT_SLUG}`.
>
> **Foundation element ≠ surface mock**. You produce a showcase of one
> element family with full state matrix — not a page composition.
>
> **Customize**: replace `{PLACEHOLDER}` tokens with project values per
> SKILL.md §0.2 before sending to subagent.

## 0. Mandatory pre-read

1. `{PROTOTYPE_OUTPUT_DIR}/_context.md` — shared chassis contract for
   this wave
2. `{ANCHOR_DOC_PATH}` — anchor declaration
3. `{ELEMENT_CONTRACT_INDEX_PATH}` — the freeze for Stage 2.0 (your
   element's slot in the index)
4. `{CHASSIS_HTML_PATH}` — chassis HTML reference (READ ONLY)
5. (If `{ELEMENT_CATEGORY}` = compound) Stage 1 Lane D interaction specs
   for the relevant interaction

## 1. Element scope

You showcase: **{ELEMENT_NAMES_LIST}**

Examples by category:
- **Atoms**: button / icon-button / pill-badge / status-dot
- **Surface**: page / raised / sunken / muted + card + drawer + modal
- **Forms**: input / textarea / select / checkbox / radio / switch
- **Nav**: top-nav / sidebar / breadcrumb / tabs / segmented-control
- **Feedback**: toast / banner / progress / spinner / skeleton

**Variants × states**: each element must show the full state matrix:

| State | Required for |
|---|---|
| default | all |
| hover | interactive |
| focus / focus-visible | interactive |
| active | interactive |
| disabled | interactive |
| loading | data-fetch surfaces |
| empty | data surfaces |
| error | inputs / data fetch |
| selected | multi-select |
| dragging | drag UI |
| dirty / valid / invalid | inputs |

Mark N/A states explicitly with a one-line reason.

## 2. Innovation factor

Element subagents target **5-7** (mature). Don't invent new UX paradigms
in foundation elements — your job is to lock the chassis at element scale,
not to invent. Innovation comes at surface scale (Stage 3 novel surfaces).

## 3. Visual chassis hard constraints

Identical to `_context.md` §1. Re-grep before shipping:
- Typography: {FONT_PRIMARY} ({WEIGHTS}); {FONT_MONO} for metadata
- Radius: {RADIUS_CARD} / {RADIUS_CHIP}
- Borders: `1px solid {BORDER_HAIRLINE_VALUE}` hairline; NO elevation shadow
- Accent: {ACCENT_VALUE} mono only
- Banned: same list as surface

## 4. Self-grade matrix (writeup §6)

| Dim | 0-10 | Notes |
|---|---|---|
| Visual chassis 一致性 | __ | |
| State coverage completeness (matrix filled) | __ | List states covered |
| Element anatomy clarity (slots / parts named) | __ | |
| Laws of UX hit count | __ | List 4-6 laws |
| Innovation factor (mature target 5-7) | __ | Foundation-level, not novel |

## 5. Output paths

| Path | What |
|---|---|
| `{PROTOTYPE_OUTPUT_DIR}/elements/{ELEMENT_SLUG}.html` | Self-contained HTML showcase |
| `{WRITEUP_DIR}/{DATE}-elements-{ELEMENT_SLUG}-writeup.md` | Research writeup |

Target HTML size: {HTML_LENGTH_RANGE}. The state matrix density matters
more than the line count.

## 6. Hard boundary constraints

Same as surface prompt §7 — never touch production source, never touch
other elements' output paths, never touch `{REFERENCE_REPO_ROOT}` or
`{RAW_IMMUTABLE_ROOT}`.

## 7. Showcase layout requirements

The HTML must be organized for **mechanical extraction** in Stage 4:

- Each variant in its own `<section>` with clear `id="{element-variant}"`
- State matrix rendered as a grid (rows = states, columns = variants)
- Token values defined in `:root` only — no scattered hex
- `data-state="..."` attributes on interactive examples (so Stage 4 can
  walk states for verification)
- Anatomy diagram per element family showing named slots (header / body /
  footer / leading / trailing)

## 8. Done condition

Reply with:
1. Output paths (HTML + writeup)
2. Element + variant counts (e.g., "4 variants × 6 states × 1 element family")
3. Self-grade aggregate
4. State matrix coverage % (filled / required cells)
5. Gate Report summary
6. Boundary check: "0 files touched outside output paths"
