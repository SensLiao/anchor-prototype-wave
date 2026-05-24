# 12-Gate Self-Audit Checklist

> Walk Gates 1 → 11 in order before declaring a Stage 3 hi-fi deliverable
> done. Gate 12 is HUMAN ONLY — never claim it yourself.
>
> Generalized from the `uiux-quality-gate-v1` pattern.

## How to use

```
1. Finish the prototype + writeup.
2. Walk Gates 1 → 11. For each gate:
     - Read PASS criteria.
     - Gather evidence (file path : line, grep result, screenshot ref).
     - Mark PASS / WARN / BLOCK + one-line evidence string.
3. Any BLOCK → remediate before continuing.
   Any WARN → log and decide (fix now or note as follow-up).
4. Append Gate Report to writeup §6.
5. Hand off to human for Gate 12.
```

## Severity definitions

| Severity | Meaning | Action |
|---|---|---|
| BLOCK | Hard fail — must remediate before continuing | Fix now; re-run gate |
| WARN | Soft fail — log; decide with user at Gate 12 | Log in Gate Report |
| NOTE | Informational | Log only |

## The 12 gates

### Gate 1 — Style baseline compliance

**Check**: Deliverable follows the declared clean-light baseline (no glass /
no aurora / no glow / no dark-by-default).

**PASS criteria**:
- No `backdrop-blur-*`, `bg-glass-*`, `border-glass-*` classes.
- No heavy glow shadow values (e.g., `0 30px 60px rgba(0,0,0,0.4)`).
- Background is white / near-white or declared `bg-surface-*` token.
- Default mode is light; dark is opt-in.
- Accent is the single declared mono OR explicitly declared multi-accent per
  anchor doc.

**Severity**: BLOCK

### Gate 2 — Token discipline

**Check**: Color / spacing / radius / shadow / motion cite the token system,
not raw hex / px.

**PASS criteria**:
- No raw hex literals outside `:root` declarations.
- Surface / text / border references use token classes
  (`bg-surface-*` / `text-text-*` / `border-border-*`) or `var(--*)`.
- Motion durations + easings use `--duration-*` and `--ease-*` tokens.
- New raw values appear ONLY in a candidate-token block, flagged
  `/* candidate — not in runtime */`.

**Severity**: BLOCK

### Gate 3 — Reference lineage (Tier 0 / 1 / 2 cited)

**Check**: Non-trivial design decisions cite a Tier 0 (in-repo prior art),
Tier 1 (`{reference-repo-root}<vendor>/<path>`), or Tier 2 (open-web URL) source.

**PASS criteria**:
- Writeup §3 lists at least 1 Tier 0 citation (file:line inside this repo)
  for a layout/component pattern.
- Tier 1 citation if proposing a new layout / component pattern.
- Tier 2 only when Tier 0 + 1 both missed (with "announce" line).
- Each citation has one-line "what we are borrowing".

**Severity**: BLOCK

### Gate 4 — Accessibility (a11y basics)

**Check**: Keyboard focus / contrast / semantic ARIA / SR affordances are
explicit.

**PASS criteria**:
- Every interactive element has `:focus-visible` state.
- Contrast pairings declared (WCAG AA — 4.5:1 body, 3:1 large).
- Tab order described for new keyboard flow.
- ARIA roles / aria-label declared on non-semantic interactive elements.
- For data displays > 5 cols / > 50 rows: real `<table>` with `scope`
  headers OR alternative accessible pattern declared.

**Severity**: BLOCK (missing focus / contrast), WARN (missing ARIA on one element).

### Gate 5 — Reduced-motion compliance

**Check**: Every animation / transition has a `prefers-reduced-motion`
fallback.

**PASS criteria**:
- Writeup has `## Motion Spec` section listing every animation.
- For each motion entry: `reduced-motion` row with explicit fallback.
- No animation > 520ms unless justified.
- Global `@media (prefers-reduced-motion: reduce)` rule present OR cited
  from project token system.

**Severity**: BLOCK

### Gate 6 — State coverage

**Check**: Every meaningful state is defined, not just the happy default.

**PASS criteria**:
- Writeup has `## State Matrix` listing applicable states:
  default / hover / focus / active / loading / empty / error / disabled /
  selected / dragging.
- Each declared state has mock path / code sample / textual description.
- For data surfaces: `empty` + `loading` MANDATORY.
- For interactive: `hover` + `focus` + `disabled` MANDATORY.
- For multi-select / drag: `selected` + `dragging` MANDATORY.
- N/A states marked with reason.

**Severity**: BLOCK (missing mandatory), WARN (stub descriptions).

### Gate 7 — Responsive (320 / 768 / 1024 / 1440)

**Check**: Layout intent at each canonical breakpoint.

**PASS criteria**:
- Writeup `## Responsive Plan` table covers ≥ 3 of 4 breakpoints.
- Each row declares: layout column count + sidebar/drawer behavior + reflow
  rules.
- No "use default" or "TBD" rows.
- For 320: confirms no horizontal scroll OR mobile out-of-scope (with reason).

**Severity**: WARN (desktop-first OK for v1; BLOCK if surface targets mobile).

### Gate 8 — Performance budget

**Check**: Animation-property-safe, bundle-aware.

**PASS criteria**:
- Animations animate ONLY: `transform` / `opacity` / `clip-path` /
  `filter` (sparingly).
- No animation on `width` / `height` / `top` / `left` / `margin` /
  `padding` / `border` / `font-size`.
- For new components: estimated bundle cost declared (> 30kb gzipped =
  justification required).
- Image references declare format + intrinsic dimensions + loading strategy.
- No new font family added beyond what the anchor allows (Gate 10 if added).
- Heavy deps (charts / 3D) declare dynamic-import boundary.

**Severity**: BLOCK (animation violations / font addition), WARN (missing
estimate).

### Gate 9 — Anti-AI-slop (taste red team)

**Check**: Doesn't look like generic AI-template output. Earns ≥ 4 of the
10 required design qualities.

**PASS criteria** (writeup `## Design Qualities` section):
Pick ≥ 4 from this list, one-line evidence each:
1. Hierarchy through scale contrast
2. Intentional rhythm, not uniform padding
3. Depth / layering via overlap / shadows / surfaces / motion
4. Typography with character + real pairing strategy
5. Color used semantically, not decoratively
6. Hover / focus / active states that feel designed
7. Grid-breaking editorial or bento composition when appropriate
8. Texture / atmosphere when it fits the direction
9. Motion that clarifies flow, not distracts
10. Data visualization as part of design system

Banned (any presence = FAIL):
- Uniform card grid with no hierarchy
- Stock centered hero
- Unmodified library defaults
- Flat no-depth layouts
- Gray-on-white safe styling
- Default font stacks "because Tailwind"
- Dashboard-by-numbers clichés

**Severity**: WARN (taste judgment; reviewer may upgrade at Gate 12).

### Gate 10 — Boundary respect

**Check**: Obeys all 9 hard rules.

**PASS criteria** (1 per boundary):
1. No production source edits (`{production-source-glob}`)
2. No global runtime config touched (`{global-token-file}` / `tailwind.config.*`
   / `vite.config.*`)
3. No runtime deps added to main app (root `package.json` unchanged)
4. No brand assets / exact text copied
5. Reproducibility metadata present for external refs (URL + commit/date
   + browser + viewport + login state)
6. Maps to a target surface (frontmatter or §1 names a specific surface)
7. Token impact declared (existing tokens / needs-candidate-token /
   needs-ADR)
8. BE impact declared (zero / additive / breaking)
9. No bypass of merge gate (deliverable doesn't propose direct merge)

**Severity**: BLOCK on {1, 2, 3, 4, 9}; WARN on {5, 6, 7, 8} if same-revision
fixable.

### Gate 11 — UX checklist

**Check**: Apply UX skill checklist (errors / empty / loading / microcopy /
destructive / progressive disclosure).

**PASS criteria** (writeup `## UX Checklist` lists the surface's applicable
items with evidence):
- Error states have recovery actions (not just "Something went wrong")
- Empty states have primary CTA explaining next action
- Loading > 200ms uses skeleton or progress (no spinner-only)
- Microcopy is product-specific (not generic — "Save case", not "Submit")
- Destructive actions have confirmation (delete / archive / remove)
- Long forms use progressive disclosure (not 20 fields in one column)

**Severity**: WARN

### Gate 12 — User final approve (HUMAN ONLY)

**Check**: User has explicitly approved the deliverable.

**PASS criteria** (human-verifiable):
- User has reviewed deliverable + Gate 1-11 report.
- User has acknowledged WARN items.
- Approval recorded in TWO places:
  1. Writeup frontmatter: `approved_by: <user>` + `approved_date: YYYY-MM-DD`
  2. `{research-vault-path}log.md`: line "{DATE} — {research-track-name}
     approval — {slug} — gates 1-11 PASS, user approve"

**Severity**: BLOCK (no merge / promotion without it).

**Run by**: HUMAN ONLY. Subagent leaves these fields empty/null in
frontmatter — never fills them in.

## Output format (append to writeup §6)

```markdown
### Gate Report

| # | Gate | Status | Evidence |
|---|---|---|---|
| 1 | Style baseline compliance | PASS | `index.html:60` — `--accent: #171717`, no banned tokens |
| 2 | Token discipline | PASS | All hex in `:root` only; verified via grep |
| 3 | Reference lineage | PASS | Tier 0: `{production-source-glob}/pages/Foo.tsx:42` + Tier 1: `{reference-repo-root}<vendor>/...:142` |
| 4 | Accessibility | PASS | `:focus-visible` on all `.btn` / `.row`; contrast 4.6:1 verified |
| 5 | Reduced-motion | PASS | `@media (prefers-reduced-motion: reduce)` block at `:431` |
| 6 | State coverage | PASS | 8 of 11 states covered; 3 N/A with reason |
| 7 | Responsive | WARN | 1024+1440 covered; 320 marked out-of-scope (desktop-first v1) |
| 8 | Performance budget | PASS | All animations on transform/opacity; no font addition |
| 9 | Anti-AI-slop | PASS | 5 of 10 qualities earned; see §3.4 |
| 10 | Boundary respect | PASS | 0 files modified outside output paths; checked via git status |
| 11 | UX checklist | PASS | Error / empty / loading / microcopy / destructive all addressed |
| 12 | User final approve | pending human | awaiting reviewer |

### WARN items (require Gate 12 decision)
- Gate 7: mobile out-of-scope for v1 → follow-up

### N/A items
- Gate 6 `dragging` state: surface is read-only, no drag UI

### Deviations declared (Gate 10 candidate tokens / new patterns)
- None (existing token system fully covers this surface)
```
