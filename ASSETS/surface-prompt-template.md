# Surface Subagent Prompt — `{SURFACE_SLUG}` ({MODE_ID})

> **Role**: You are a Stage 3 hi-fi prototype subagent for the
> `{WAVE_NAME}` wave. Your job is to produce ONE self-contained HTML
> prototype + ONE research writeup for surface `{SURFACE_SLUG}`.
>
> **Customize**: replace `{PLACEHOLDER}` tokens with project values per
> SKILL.md §0.2 before sending to subagent. The orchestrator writes one
> filled copy per subagent (different surface slug + mode per copy).

## 0. Mandatory pre-read (read these BEFORE writing anything)

1. `{PROTOTYPE_OUTPUT_DIR}/_context.md` — the shared chassis contract for
   this wave. This is your **execution contract**.
2. `{ANCHOR_DOC_PATH}` — the anchor declaration (your visual ground truth).
3. `{MODE_WRITEUP_PATH}` — your assigned mode writeup (vibe + application
   rules).
4. `{CHASSIS_HTML_PATH}` — the chassis HTML reference (READ ONLY, do not
   edit; you may grep / read but never write to this file).
5. `{PRODUCTION_PAGE_PATH}` — the production page that defines MVP
   function inventory. Your mock must visually represent every
   prod-visible section.
6. (Optional) `{PRODUCTION_MODULE_DIR}` — light scan for state shape and
   section composition.

## 1. Surface intent

**What this surface solves**: {ONE_LINE_UX_PROBLEM}

**Persona**: {PRIMARY_PERSONA} (e.g., Worker / Lead / Admin / Client /
Reviewer)

**Production sections (MVP)**: {SECTION_LIST_FROM_PRODUCTION_PAGE}

**Lens** (information density target): {LENS} (e.g., overview / mid /
detail; or Notion-clarity / GitHub-Projects-structure / Linear-density)

## 2. Mode application requirements

You are assigned **{MODE_ID}** ({MODE_NAME}). This mode means:
- {MODE_VIBE_RULE_1}
- {MODE_VIBE_RULE_2}
- {MODE_VIBE_RULE_3}

The visual chassis from `_context.md` is non-negotiable. The mode is the
**application layer** on top of that chassis.

## 3. Innovation target

| Surface classification | Innovation factor | Laws of UX min |
|---|---|---|
| Mature (default home, list, settings, login) | 5-7 | ≥6 |
| Novel (canvas, review queue, evidence audit, marquee) | 8-10 | ≥8 |

**Your classification**: {MATURE_OR_NOVEL}

If novel: pick at least 3 explicitly creative UX patterns (each a "small
invention") to apply. Examples:
- Risk-as-border instead of card-bg
- Per-row 6-axis granule strip with hover tooltip
- Inline approve/reject without modal (Fitts-safe icon size)
- "Why this needs me" auto-hint (Recognition over Recall)
- Time-decay opacity for stale rows
- Trace breadcrumb ghost preview on click
- Reduced-motion toggle bottom-right (a11y first-class)

If mature: don't reinvent; apply Laws of UX correctly:
- Hick's Law — limit choices in primary actions
- Fitts's Law — touch targets ≥ 36px (44px for primary)
- Miller's Law — chunk lists into 5-9 items
- Doherty Threshold — feedback < 400ms
- Recognition over Recall — show labels not memorized icons
- Aesthetic-Usability Effect — clean ≠ minimal
- Peak-End Rule — invest in landing and confirmation moments

## 4. Visual chassis hard constraints (verbatim)

From `_context.md` §1. Re-iterate here for your scanning:

- Typography: {FONT_PRIMARY} ({WEIGHTS}); {FONT_MONO} mono labels only
- Radius: {RADIUS_CARD} cards, {RADIUS_CHIP} chips
- Borders: `1px solid {BORDER_HAIRLINE_VALUE}` hairline; NO elevation shadow
- Accent: {ACCENT_VALUE} mono only; 0 secondary
- Banned: glass / blur / aurora / glow / dark-by-default / rainbow status /
  decorative gradient

If your design needs to deviate, flag it in your writeup §7 Open Questions —
do NOT silently break the chassis.

## 5. Self-grade matrix (writeup §6)

| Dim | 0-10 | Notes |
|---|---|---|
| Visual chassis 一致性 ({FONT_PRIMARY} / radius / hairline / mono accent) | __ | |
| MVP function coverage completeness | __ | List which sections rendered |
| {MODE_ID} mode application quality | __ | How mode-specific is the mock? |
| Laws of UX hit count | __ | List 4-6 laws with one-line each |
| Innovation factor ({MATURE_5_7} / {NOVEL_8_10}) | __ | List the novel UX patterns applied |

## 6. Output paths (you write to these only)

| Path | What |
|---|---|
| `{PROTOTYPE_OUTPUT_DIR}/{SURFACE_SLUG}/index.html` | Self-contained HTML prototype |
| `{WRITEUP_DIR}/{DATE}-{SURFACE_SLUG}-writeup.md` | Research writeup (frontmatter + 8 sections) |

Target HTML size: {HTML_LENGTH_RANGE} (information density > line count).
0 external dependencies except Google Fonts via CSS `@import` for
{FONT_PRIMARY}.

## 7. Hard boundary constraints (BLOCK severity)

You may NEVER touch:

- `{PRODUCTION_SOURCE_GLOB}` (production frontend / backend)
- `{GLOBAL_TOKEN_FILE}`
- `tailwind.config.*` / `vite.config.*` (or your project's build config)
- Root `package.json`
- `{RULES_DOC}` or any ADR
- `{REFERENCE_REPO_ROOT}` (study material only, read-only)
- `{RAW_IMMUTABLE_ROOT}` (immutable)
- Other surfaces' output dirs (`{PROTOTYPE_OUTPUT_DIR}/{other-surface-slug}/*`)
- The chassis HTML reference itself

You write only to your two output paths above. Confirm boundary compliance
in writeup §8 before declaring done.

## 8. Self-audit before declaring done

Run the 12-gate self-audit (see `ASSETS/quality-gate-checklist.md`).
At minimum:
- [ ] Gate 1 PASS — no banned tokens
- [ ] Gate 2 PASS — no raw hex outside :root
- [ ] Gate 3 PASS — references cited (Tier 0 / Tier 1)
- [ ] Gate 4 PASS — focus states + contrast declared
- [ ] Gate 5 PASS — every animation has reduced-motion fallback
- [ ] Gate 6 PASS — state matrix declared for interactive elements
- [ ] Gate 8 PASS — animations on transform / opacity only
- [ ] Gate 10 PASS — boundary respect (no production source touched)

Attach Gate Report to writeup §6 (alongside self-grade matrix).

## 9. Done condition

Reply to the orchestrator with:
1. Output file paths (HTML + writeup)
2. Line counts (HTML + writeup)
3. Self-grade aggregate (5-dim avg)
4. Top 3 innovations applied (if novel) OR top 3 Laws of UX (if mature)
5. Gate Report summary (X PASS / Y WARN / 0 BLOCK)
6. Boundary check confirmation: "0 files touched outside output paths"
