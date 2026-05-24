# Anchor Wave v2.1.0 — Failure Patterns (Regression Cases)

> Each pattern is a known failure mode. New waves add to this file
> rather than relying on memory. Validators in
> `scripts/validate_surface.py` codify these as detection rules so
> they cannot silently return.
>
> Format: ID / pattern / first-seen / detection rule / expected behavior.

---

## case_001 — Marketplace scaffold leak

**First seen**: 2026-05-14 (Codex audit of 7 incomplete surfaces).

**Pattern**: marketplace card affordances (rating numbers like `4.8`,
download counts like `1.2k installs`, `Install` buttons, publisher
chips) appear in surfaces that have nothing to do with browsing /
installing capabilities.

**Pilot follow-up (2026-05-17)**: 2026-05-16 stale-de-risk cleanup removed
ALL marketplace scaffold from the 7 prior-flagged surfaces. Pilot
re-validated: 0 hits on `scaffold_leak` across all 12 audited surfaces.
Validator is correctly tuned; keep as defense-in-depth.

**Detection rule** (`check_scaffold_leak`):

```python
BANNED_TOKENS = [
    r"\b4\.8\b(?=[^<]*?(?:rating|stars?|reviews?))",
    r"\b\d+(?:\.\d+)?k\s+installs?\b",
    r">\s*Install\s*</button>",
    r">\s*Install to workspace\s*<",
    r'class="[^"]*\brating\b[^"]*"',
    r'class="[^"]*\bdownloads?\b[^"]*"',
]

ALLOWED_SURFACES = {
    "pm-marketplace", "pm-connector", "pm-node-detail",
    "pm-sop-template", "pm-workflow-template",
    "ps-marketplace-sub",
}
```

---

## case_002 — Overlay rendered as full-page

**First seen**: 2026-05-14 (Codex audit).

**Pattern**: surface claims to be an overlay (`onboarding`,
`command-palette`) but is rendered as a full app shell with header /
nav / sidebar.

**Pilot follow-up (2026-05-17)**: x-onboarding still hits this
(`form_mismatch` sub-cause → REDO). x-command-palette and x-mcp-registry
hit a DIFFERENT sub-cause: `threshold_only` (correct overlay structure,
but z-index 50 < required 1000). v2.1.0 added `gate_0_sub_cause`
classification so REDO vs FIX_NEEDED is correctly distinguished.

**Detection rule** (`check_surface_morphology`):

```python
if contract["claimed_surface_type"] == "overlay":
    has_scrim = bool(soup.select_one(
        '[class*="scrim"], [class*="overlay-bg"], [class*="backdrop"]'
    ))
    has_panel_structure = bool(soup.select_one(
        '[class*="overlay"], [class*="modal"], [class*="dialog"]'
    ))
    z_indices = [int(z) for z in re.findall(r"z-index:\s*(\d+)", style)]
    max_z = max(z_indices, default=0)

    if not has_panel_structure:
        sub_cause = "form_mismatch"        # → REDO
    elif not has_scrim:
        sub_cause = "missing_scrim"        # → REDO
    elif max_z < 1000:
        sub_cause = "threshold_only"       # → FIX_NEEDED (v2.1.0)
    else:
        return PASS
```

---

## case_003 — Object model mismatch (mcp-registry)

**First seen**: 2026-05-14 (Codex audit).

**Pilot follow-up (2026-05-17)**: 2026-05-16 cleanup CORRECTED this:
the prototype now shows server rows with name/transport/health/tool-count/
scopes. case_003 considered resolved on x-mcp-registry; keep rule for
future MCP registry variants.

**Detection rule**: harder to fully automate; relies on contract
`primary_object` field declared in §2 preflight. Validator checks DOM
for first-level list items matching the declared object schema.

---

## case_004 — Decorative gradient violates "no decorative gradient"

**First seen**: 2026-05-14 (Codex audit — all 7 surfaces).

**Pattern**: `radial-gradient(circle at 1px 1px, ...)` used as ambient
decoration (dot-grid texture) on body/app/canvas backgrounds.

**Pilot finding (2026-05-17)**: 11 of 12 audited surfaces fired this
gate. The patterns are actually **semantic chassis idioms**, not
arbitrary decoration:
- `.app` / `html, body` dot-grid at 0.04 opacity = chassis-wide texture
- `.canvas-wrap` dot-grid = canonical canvas idiom (tldraw / Miro / n8n)
- `.ghost-canvas` dot-grid = inspector-over-canvas aria-hidden context
- `.granule--slash` linear-gradient = semantic failure mark
- `[data-flagged]` linear-gradient = semantic flagged-state amber tint

**v2.1.0 fix**: expand `GRADIENT_SEMANTIC_ALLOWLIST` from 3 entries to 9.

**Detection rule (v2.1.0)** (`check_decorative_gradient`):

```python
GRADIENT_SEMANTIC_ALLOWLIST = [
    ("status-dot",     "radial-gradient"),
    ("status-pill",    "radial-gradient"),
    ("focus-visible",  "radial-gradient"),
    # v2.1.0 additions (pilot finding):
    ("html, body",     "radial-gradient"),    # chassis texture
    (".app",           "radial-gradient"),    # chassis texture on .app outer
    ("canvas-wrap",    "radial-gradient"),    # canonical canvas dot-grid
    ("ghost-canvas",   "radial-gradient"),    # inspector-over-canvas
    ("granule--slash", "linear-gradient"),    # semantic failure mark
    ("data-flagged",   "linear-gradient"),    # semantic flagged-state tint
]

for rule in css_rules:
    if 'radial-gradient' in rule.value or 'linear-gradient' in rule.value:
        if not any(allow_sel in rule.selector and allow_grad in rule.value
                   for allow_sel, allow_grad in GRADIENT_SEMANTIC_ALLOWLIST):
            yield FAIL(gate_3_no_scaffold_leak,
                       f"Decorative gradient at {rule.selector}: {rule.value}")
```

**Expected behavior**: solid backgrounds for non-semantic surfaces;
allowlisted gradients for semantic chassis patterns.

---

## case_005 — Pill mono drift

**First seen**: 2026-05-14 (Codex audit).

**Pattern**: `.pill` class uses JetBrains Mono with `letter-spacing:
0.04em` and lowercase, instead of the canonical 10px uppercase
0.08em metadata pill.

**Pilot finding (2026-05-17)**: p-node-inspector-6tab still drifts
(10.5px vs canonical 10px). One surface, one fix.

**Severity**: WARN (not BLOCK) — visually minor but compounds across
the gallery.

---

## case_006 — Stale tab label (Rules vs Governance)

**First seen**: 2026-05-13 (HARD RULE #6 IA reset).

**Pilot finding (2026-05-17)**: 2026-05-16 cleanup applied; 0 hits on
this rule across 12 surfaces. Visible label is `Governance`. Legacy
`data-tab="rules"` retained for JS wiring.

---

## case_007 — Morphology threshold-only mismatch (v2.1.0 new)

**First seen**: 2026-05-17 (Codex Wave 2 cross-review of pilot).

**Pattern**: surface has correct outer morphology (overlay scrim + panel
present, drawer side-anchored panel present) but a single threshold
attribute fails (e.g., overlay backdrop has z-index 50 instead of
required ≥ 1000).

**Pilot evidence**: x-command-palette + x-mcp-registry — Claude initially
returned REDO; Codex disputed → FIX_NEEDED is correct because a 1-line
CSS patch (`z-index: 1000`) resolves it.

**Detection rule**: handled by `check_surface_morphology` emitting
`gate_0_sub_cause = "threshold_only"`; `scoring-rubric.md` §4.3 maps
that to FIX_NEEDED instead of REDO.

**Severity**: BLOCK (gate_0), but verdict = FIX_NEEDED (not REDO).

---

## Adding new patterns

Every wave's `closeout.md` MUST check: did this wave reveal a new
recurring failure pattern? If yes, append:

1. New `case_NNN` entry in this file
2. Corresponding rule in `scripts/validate_surface.py`
3. Mention in closeout.md `regression_dataset_updates` section

This is what makes the skill compound. Without it, the same bug
returns next wave.
