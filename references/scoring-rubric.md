# Anchor Wave v2.1.0 — Scoring Rubric

> Implementation of §4 in SKILL.md. Verdict rule is the contract;
> weights and floors below are the default and may be overridden per
> wave plan with explicit justification.
>
> v2.1.0 pilot-validated changes:
> - §4.3: morphology sub-cause distinguishes REDO vs FIX_NEEDED
> - §4.4: maturity-aware innovation floor (mature surfaces ≥ 5, not ≥ 8.5)

## Order of operations

```
1. Run all hard gates (gates 0-4, see gates.md)
2. If any hard gate == BLOCK → emit verdict per §4.3 short-circuit
3. Else evaluate soft scores
4. Compute maturity-aware min-floor check (§4.4)
5. Compute weighted_score
6. Emit verdict
```

## §4.3 — Hard-gate short-circuit (highest priority)

v2.1.0 differentiates morphology mismatches:

```python
if hard_gates["gate_0_intent_alignment"] == "BLOCK":
    sub = hard_gates.get("gate_0_sub_cause", "form_mismatch")
    if sub in ("threshold_only", "inner_widget_missing"):
        return "FIX_NEEDED"   # surgical patch suffices
    # form_mismatch or missing_scrim → REDO
    return "REDO"

if hard_gates["gate_1_production_source_grounding"] == "BLOCK":
    return "REDO"   # never read source; fundamental

if any(g == "BLOCK" for g in hard_gates.values()):
    return "FIX_NEEDED"   # other BLOCKs are surgically patchable
```

Rationale (pilot evidence): on `x-command-palette` and `x-mcp-registry`,
Claude initially returned REDO on Gate 0 BLOCK. Codex cross-review
correctly identified these as `threshold_only` (z-index 50 < 1000), where
a 1-line CSS patch (`z-index: 1000`) fixes the gate. REDO would have
wasted effort.

## §4.4 — Maturity-aware min-floor (v2.1.0 — pilot finding)

Rationale: per-dim anchors in this file say mature surfaces target innovation
5-7 ("Pushing mature surfaces above 7 often signals over-design"). v2.0's
global `MIN_FLOOR = 8.5` contradicted this and made mature-cohort PASS
impossible. Pilot evidence (2026-05-17): p1-caselibrary innovation=8 weighted
8.875, p9-root-canvas innovation=8 weighted 8.85 — both correctly mature, both
tripped the floor.

```python
INNOVATION_FLOOR_BY_MATURITY = {
    "mature":   5.0,   # rubric: 5-7 target; 5 is acceptable floor
    "creative": 7.5,   # creative surfaces should hit ≥ 7.5
    "marquee":  8.5,   # marquee gallery centerpieces
}
NON_INNOVATION_FLOOR = 8.5    # other 5 dims still floored at 8.5

SOFT_DIMS = [
    "chassis_consistency", "mvp_coverage", "visual_quality",
    "interaction_quality", "innovation", "consistency_with_siblings",
]

innovation_target = contract.get("surface_innovation_target", "mature")
innov_floor = INNOVATION_FLOOR_BY_MATURITY[innovation_target]

floor_violators = {}
for d in SOFT_DIMS:
    floor = innov_floor if d == "innovation" else NON_INNOVATION_FLOOR
    if scores[d] < floor:
        floor_violators[d] = {"score": scores[d], "floor": floor}

if floor_violators:
    return "FIX_NEEDED"
```

Driven by `contract.surface_innovation_target` (default `mature`).

## §4.5 — Weighted score (PASS bar)

```python
WEIGHTS = {
    "chassis_consistency":       0.20,
    "mvp_coverage":              0.20,
    "visual_quality":            0.15,
    "interaction_quality":       0.15,
    "consistency_with_siblings": 0.15,
    "innovation":                0.15,
}
# sum == 1.0

weighted = sum(WEIGHTS[d] * scores[d] for d in SOFT_DIMS)

QUALITY_BAR = 9.0
return "PASS_9PLUS" if weighted >= QUALITY_BAR else "FIX_NEEDED"
```

## Per-dim rubric anchors (LLM scorer must cite anchor when assigning score)

LLM scorers must produce a 1-line justification per score, referencing
the anchor table below. No bare numbers allowed.

### chassis_consistency

| Score | Anchor |
|---|---|
| 0-3 | Wrong font, wrong palette, or dark-by-default in a light chassis |
| 4-5 | Most tokens correct; 1-2 wrong (e.g., radial-gradient leak, pill drift) |
| 6-7 | All tokens correct; some local hex values still present |
| 8 | All tokens correct; no raw hex; all citing `_context.md` |
| 9 | Above + tokens used semantically (not just visually) |
| 10 | Above + atypical surface still feels native to chassis |

### mvp_coverage

| Score | Anchor |
|---|---|
| 0-3 | < 1/3 of production sections present |
| 4-5 | ~half present; some critical missing (e.g., empty/error state) |
| 6-7 | Most present; some affordances visible but not interactive |
| 8 | All required sections visually present |
| 9 | Above + plausible empty/loading/error states |
| 10 | Above + states differentiated, not placeholder-grey |

### visual_quality

| Score | Anchor |
|---|---|
| 0-3 | Uniform spacing/padding; no hierarchy; flat |
| 4-5 | Some hierarchy; typography readable; rhythm uneven |
| 6-7 | 3-tier scale contrast; intentional rhythm; minor inconsistencies |
| 8 | All above clean; no AI-slop tells |
| 9 | Above + ≥4 of 10 anti-template qualities |
| 10 | Above + deliberate craft moment that fits chassis |

### interaction_quality

| Score | Anchor |
|---|---|
| 0-3 | No hover/focus; buttons indistinguishable from text |
| 4-5 | Hover only; no focus; no loading/empty/error |
| 6-7 | Hover/focus/active; loading or empty missing |
| 8 | Hover/focus/active + loading + empty + error all designed |
| 9 | Above + specific microcopy (not "Loading..." but "Loading 12 cases...") |
| 10 | Above + destructive confirm + progressive disclosure |

### innovation

| Score | Anchor |
|---|---|
| 0-3 | Direct copy of reference; no application context |
| 4-5 | Reference applied; no local thought |
| 6-7 | Reference + chassis adaptation visible |
| 8 | Reference + chassis + 1 deliberate delight detail |
| 9-10 | Novel composition that still respects chassis; defensible vs frontier products |

**Caveat (mature targets)**: mature surfaces target 5-7. Pushing them
above 7 often signals over-design. v2.1.0 §4.4 floor honors this.

### consistency_with_siblings

| Score | Anchor |
|---|---|
| 0-3 | Pattern differs from siblings without justification |
| 4-5 | Some shared patterns; some divergence |
| 6-7 | Mostly shared; intentional divergences exist |
| 8 | All patterns shared unless surface uniquely requires deviation |
| 9 | Above + deviations documented in writeup with reason |
| 10 | Above + this surface contributes a new pattern siblings could adopt |

## Verdict mapping (final)

| Verdict | Meaning | Next action |
|---|---|---|
| `PASS_9PLUS` | All hard gates PASS, all dims ≥ floor, weighted ≥ 9.0 | Ship to gallery + Gate 12 |
| `FIX_NEEDED` | Patches can resolve | Enter §5 fix-on-fail loop |
| `REDO` | Form-level wrong; patch won't help | §5 with `redo: true` (fresh write) |
| `ESCALATE_HUMAN` | 3 retries exhausted | Human reviews; never auto-PASS |

## Override policy

Weights or floor override requires:
1. Explicit field in wave plan: `scoring_override: {min_floor: 8.0, weights: {...}}`
2. Justification paragraph
3. Human approval before spawning subagents
