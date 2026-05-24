# Anchor Wave v2.1.0 — Gates Reference

Total: 5 hard gates (BLOCK can never be averaged away) + 7 soft scores
(0-10, evaluated only when all hard gates PASS) + Gate 12 human approval
(unchanged from v2.0).

## Hard Gates (BLOCK / PASS only — no partial credit)

### Gate 0 — Intent Alignment

**What**: surface's actual DOM morphology matches its claimed surface
type (read from contract JSON `claimed_surface_type` vs DOM inspection).

**PASS criteria** (per `surface-taxonomy.md`):
- overlay: scrim element with `position: fixed` covering viewport, content
  panel z-index ≥ 1000, dimmed background visible
- drawer: panel anchored to a viewport edge with `position: fixed`, slides
  in (transform), has close affordance
- full-page: app shell (header + main + optional aside); do NOT pretend
  to be overlays
- wizard: step rail (left or top) + focused form panel + optional right-side
  review summary
- list / canvas / form / dashboard / inspector / audit-view / chat /
  command-tool: see `surface-taxonomy.md` per-type DOM signature

**v2.1.0 sub-cause classification** (drives REDO vs FIX_NEEDED in
`scoring-rubric.md` §4.3):

| `gate_0_sub_cause` | Meaning | Verdict mapping |
|---|---|---|
| `form_mismatch` | Wrong outer shell entirely (e.g., full-page rendered for an overlay claim) | REDO |
| `missing_scrim` | Overlay has panel but no scrim element | REDO |
| `threshold_only` | Has correct structure but a single attribute is below threshold (e.g., z-index 50 vs required 1000) | FIX_NEEDED |
| `inner_widget_missing` | Outer shell correct, inner required widget missing (e.g., chat surface lacks composer) | FIX_NEEDED |

Pilot evidence (2026-05-17): Codex correctly disputed Claude's REDO verdict
on `x-command-palette` and `x-mcp-registry` — both were `threshold_only`
(z-index 50 < 1000) which is a 1-line CSS patch, not a form-level rewrite.

**Evidence required in audit.json**:
```json
{
  "gate_0_intent_alignment": "BLOCK",
  "gate_0_sub_cause": "threshold_only",
  "evidence_selectors": [
    {"selector": ".overlay-backdrop", "issue": "z-index 50 < required 1000",
     "line_range": "L211"}
  ]
}
```

---

### Gate 1 — Production Source Grounding

**What**: surface was authored after reading its corresponding
`workspace/src/pages/**` or `workspace/src/features/**` source (or
explicitly marked `research-only` with reason).

**PASS criteria**:
- contract.json `production_source` non-empty AND points to a file that
  exists, OR
- contract.json `research_only_reason` non-empty AND user acknowledged

**Remediation**: REDO with mandatory pre-read step.

---

### Gate 2 — Boundary Compliance

**What**: subagent wrote ONLY to its declared write paths.

**FAIL examples**: writes to `workspace/src/styles/globals.css`, to
`.claude/CLAUDE.md` without `--edit-skill=true`, to `vault/raw/**`, or
to a surface dir not in `--surfaces=` list.

**Remediation**: REVERT writes via `git checkout`; record in closeout;
re-spawn with corrected scope.

---

### Gate 3 — No Scaffold Leak

**What**: surface contains no marketplace-only affordances unless it IS a
marketplace surface.

**Detection rule** (codified in `scripts/validate_surface.py`):

Banned tokens outside `MARKETPLACE_ALLOWED_SURFACES`:
- rating-like numbers (`4.8` adjacent to "rating"/"stars"/"reviews")
- `<digits>k installs` patterns
- `<button>` labeled exactly "Install" or "Install to workspace"
- `rating` / `downloads` / `publisher` / `free` class metadata

**Remediation**: FIX_NEEDED, surgical patch — replace marketplace scaffold
with appropriate surface idiom.

---

### Gate 4 — Accessibility Minimum

**What**: static a11y checks pass.

**PASS criteria**:
- every `<button>` has text content or `aria-label`
- every `<input>` has `<label for>` or `aria-label`
- focus styling rule exists (`:focus` / `:focus-visible`)
- if any `transition:` / `animation:` rule exists, a
  `@media (prefers-reduced-motion: reduce)` block exists

**Remediation**: usually FIX_NEEDED, surgical patches.

---

## Soft Scores (0-10, evaluated only if all hard gates PASS)

Detailed rubrics in `scoring-rubric.md`. Quick reference:

| Dim | Anchor at score 5 | Anchor at score 9 |
|---|---|---|
| `chassis_consistency` | 1 wrong token | All tokens cite `_context.md` |
| `mvp_coverage` | Half of required sections | All sections + plausible empty/loading/error |
| `visual_quality` | Hierarchy unclear | 3-tier scale, intentional rhythm |
| `interaction_quality` | Hover only | hover/focus/active/loading/empty/error all designed |
| `innovation` | Mature reference applied literally | Mature reference + 1 delight detail that fits chassis |
| `consistency_with_siblings` | Patterns differ from 2+ siblings | Patterns match siblings; deviations justified |

Mature surfaces target innovation 5-7. v2.1.0 maturity-aware floor
(`scoring-rubric.md` §4.4) enforces this without false-FIX on innovation=6.

---

## Gate 12 — Human Approval (unchanged from v2.0)

Only the human can fill `approved_by` / `approved_date` in the writeup
frontmatter and append to closeout.md. Subagents producing these fields
empty is correct behavior.

## Severity legend

| Tag | Meaning | Effect on verdict |
|---|---|---|
| BLOCK | Critical; must not ship | Forces REDO or FIX_NEEDED per §4.3 |
| WARN | Should fix; can ship if justified | Reduces relevant soft score |
| NOTE | Optional improvement | No effect on verdict |
