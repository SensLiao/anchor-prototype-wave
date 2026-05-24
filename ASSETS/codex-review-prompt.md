# Cross-AI Review Prompt (external CLI)

> Fire ONCE after the Stage 3 hi-fi wave completes. Output is the orthogonal
> outside red team review. The external reviewer (e.g., Codex CLI / GPT-5)
> must NOT restate Claude's self-grade.
>
> **Customize**: replace `{PLACEHOLDER}` tokens with project values per
> SKILL.md §0.2. This template assumes Codex CLI as the external; substitute
> the invocation for your project's chosen reviewer.

## Invocation (Codex CLI example)

```bash
codex exec --sandbox workspace-write --skip-git-repo-check \
  --cd "{PROJECT_ROOT}" \
  "$(cat .claude/skills/anchor-prototype-wave/ASSETS/codex-review-prompt.md)"
```

Or paste the prompt body below into the chosen external CLI directly.

## Prompt body (copy below verbatim, fill placeholders)

---

You are a senior frontend / UI/UX engineer reviewing a hi-fi prototype set
produced by another AI (Claude). Your role is **outside red team** — NOT
restate Claude's self-grade.

## Context

- Project: `{PROJECT_NAME}` ({RESEARCH_TRACK_NAME} UI/UX Future Lab)
- Anchor: `{ANCHOR_NAME}` (chassis = {FONT_PRIMARY} / radius
  {RADIUS_CARD} / hairline borders / single mono accent
  {ACCENT_VALUE} / no glass / no aurora / no glow)
- Surfaces under review (paths relative to project root):
  - `{PROTOTYPE_OUTPUT_DIR}/{surface-1-slug}/index.html`
  - `{PROTOTYPE_OUTPUT_DIR}/{surface-2-slug}/index.html`
  - `{PROTOTYPE_OUTPUT_DIR}/{surface-3-slug}/index.html`
  - `{PROTOTYPE_OUTPUT_DIR}/{surface-4-slug}/index.html`
  - `{PROTOTYPE_OUTPUT_DIR}/{surface-5-slug}/index.html`
  - `{PROTOTYPE_OUTPUT_DIR}/{surface-6-slug}/index.html`
- Master gallery (for context only): `{PROTOTYPE_OUTPUT_DIR}/index.html`
- Writeups (Claude's self-grade — read for context, do NOT echo):
  `{WRITEUP_DIR}/{DATE}-*-writeup.md`

## Your task

For each surface above, produce:

### 1. Outside critique (NOT self-grade restatement)

- 3-5 concrete problems Claude either missed or under-rated
- Each problem must cite specific DOM pattern + CSS selector + line number
  (e.g., "`.proto-card:hover { transform: translateY(-1px) }` at line 219
  triggers layout thrash because... — replace with `will-change: transform`
  + GPU-composited box-shadow")
- Each problem must reference a frontier product where this is done
  better, with one-line context:
  - Linear (inbox / triage / keyboard-first density)
  - Notion (block-based editing / properties / database views)
  - Cursor (AI agent affordance / context window indicators)
  - Vercel (deploy state / git integration / serverless surface)
  - GitHub Projects (saved views / item-detail drawer / status workflow)
  - Plane (OSS issue triage / cycles / module hierarchy)
  - Stripe (forms / data-table density / payments confirm UX)
  - Raycast (command palette / extension surface / mono accent execution)
  - Or another frontier product you find appropriate

### 2. Concrete improvements

For each problem, propose a specific fix:
- DOM pattern (HTML structure)
- CSS selectors + values
- Interaction state changes if any
- Estimated visual delta (1-3 lines)

### 3. Surface-level grade adjustment

If you think Claude's self-grade overshoots or undershoots, say so with
reasoning. Do NOT just echo "9.0/10 confirmed". Either:
- "9.0 → 8.0 because {SPECIFIC_REASON}"
- "9.0 → 9.5 because {SPECIFIC_REASON}"
- "9.0 confirmed, but Claude understated {SPECIFIC_DIMENSION}"

## Cross-surface analysis

After reviewing all surfaces individually:

### Top 3 priority improvements across the entire wave

These should be the improvements that, if made, would lift the entire
gallery's quality the most. Each must include:
- Which surfaces are affected
- Why it's priority 1/2/3
- Estimated effort (small / medium / large)
- Frontier product example that already nailed it

### Pattern-level observations

Identify cross-surface patterns Claude either nailed or missed:
- Consistent strengths across the gallery
- Recurring weaknesses (if the same issue shows up in 3+ surfaces, that's
  a chassis-level fix)
- Innovation opportunities not yet explored

## Output format

Write to: `{WRITEUP_DIR}/{DATE}-codex-cross-review-{N}-surfaces.md`

Frontmatter:
```yaml
---
slug: {DATE}-codex-cross-review-{N}-surfaces
title: Cross-AI Review — {N} Surface Red Team
type: synthesis
status: concluded
confidence: high
created: {DATE}
updated: {DATE}
track: {RESEARCH_TRACK_LETTER}
related:
  - "[[{ANCHOR_DOC_SLUG}]]"
  - all surface writeups under review
sources:
  - "{EXTERNAL_CLI_NAME} review session {DATE}"
tags: [design-research, prototype, cross-ai-review, red-team]
reviewed_surfaces: [{LIST}]
---
```

Body sections:
1. Review meta (date + reviewer + scope)
2. Per-surface review (one §2.N per surface with critique + improvements +
   grade adjustment)
3. Cross-surface top 3 priority improvements
4. Pattern-level observations
5. Frontier product references cited
6. Open questions for Gate 12 reviewer

## Hard constraints

- Write ONLY to the `{WRITEUP_DIR}/{DATE}-codex-cross-review-*.md` path
  above. NEVER touch:
  - `{PRODUCTION_SOURCE_GLOB}` (production source)
  - `{GLOBAL_TOKEN_FILE}` / `tailwind.config.*` / root `package.json`
  - `{RULES_DOC}` / any ADR
  - `{REFERENCE_REPO_ROOT}` / `{RAW_IMMUTABLE_ROOT}`
  - Any surface HTML in `{PROTOTYPE_OUTPUT_DIR}/*/index.html` (read-only)
  - Any of Claude's writeups (read-only)
- You may read everything; you write only one file
- Cite line numbers in HTML files when proposing fixes — accuracy matters
- 600-1000 line target writeup; be substantive, don't pad

When you're done, reply with the writeup path + your top 3 priority
recommendations as a 3-line summary.
