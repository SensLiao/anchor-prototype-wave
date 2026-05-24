# Anchor Wave v2.1.0 — Output Schema

> Every audit + contract + closeout emits machine-readable JSON.
> Markdown summaries are derived; JSON is source of truth.
>
> v2.1.0 additions:
> - SurfaceContract: `surface_innovation_target` ∈ {mature, creative, marquee}
> - SurfaceAudit: `gate_0_sub_cause` ∈ {form_mismatch, missing_scrim, threshold_only, inner_widget_missing, none}

## File layout per wave

```
audits/<wave-slug>/
  manifest.json
  contracts/<surface-slug>.contract.json
  audits/<surface-slug>.audit.json
  audits/<surface-slug>.audit.md
  cross-review/<surface-slug>.codex.json    # if triggered
  cross-review/<surface-slug>.codex.md      # if triggered
  closeout.md
  closeout.json
```

---

## Schema: SurfaceContract

Emitted by §2 preflight, before any scoring.

```json
{
  "$schema": "anchor-wave/v2.1/surface-contract",
  "wave_slug": "2026-05-17-pilot",
  "surface_slug": "x-onboarding",
  "claimed_surface_type": "overlay",
  "actual_surface_type_evidence": {
    "from_filename": "x-onboarding",
    "from_route": "/onboarding (first-login overlay)",
    "from_dom": "overlay"
  },
  "surface_innovation_target": "mature",
  "production_source": "workspace/src/features/onboarding/OnboardingOverlay.tsx",
  "production_source_grounding_quotes": [
    {
      "file": "workspace/src/features/onboarding/OnboardingOverlay.tsx",
      "line_range": "L15-L42",
      "quote": "<Dialog open={!hasOnboarded} scrim ..."
    }
  ],
  "research_only_reason": null,
  "required_mvp_affordances": [
    "scrim covering app",
    "centered onboarding panel",
    "progress dots",
    "skip / continue / back affordances",
    "role -> provider -> first-case flow"
  ],
  "primary_object": "user_first_login_journey",
  "primary_object_fields": ["role", "provider", "first_case"],
  "forbidden_scaffold_patterns": ["marketplace_card", "rating_chip", "install_button"],
  "write_scope": ["ui-lab/v2-anchor-prototypes/x-onboarding/index.html"],
  "mode": "AUDIT_ONLY",
  "created_by": "subagent:audit-grader-batch1",
  "created_at": "2026-05-17T14:32:00Z"
}
```

Field requirements:

| Field | Required | Validation |
|---|---|---|
| `claimed_surface_type` | yes | enum from surface-taxonomy.md |
| `surface_innovation_target` (v2.1.0) | yes | enum {`mature`, `creative`, `marquee`}; default `mature` |
| `production_source` | yes (or `research_only_reason`) | file must exist OR reason non-empty |
| `required_mvp_affordances` | yes | min 3 items |
| `primary_object` | yes | single noun phrase |
| `write_scope` | yes | must subset DEFAULT_WRITE_ALLOWLIST + SURFACE_WRITE_ALLOWLIST |
| `mode` | yes | enum from §0 |

---

## Schema: SurfaceAudit

Emitted by §3 validators + §4 scoring.

```json
{
  "$schema": "anchor-wave/v2.1/surface-audit",
  "wave_slug": "2026-05-17-pilot",
  "surface_slug": "x-onboarding",
  "contract_ref": "audits/2026-05-17-pilot/contracts/x-onboarding.contract.json",
  "deterministic_validators": {
    "scaffold_leak": {"status": "PASS", "matches": []},
    "decorative_gradient": {
      "status": "BLOCK",
      "matches": [{"selector": ".app", "line": 63, "value": "radial-gradient(...)"}]
    },
    "pill_mono_drift": {"status": "PASS", "matches": []},
    "surface_morphology": {
      "status": "BLOCK",
      "sub_cause": "form_mismatch",
      "matches": [{"issue": "Full app shell rendered; overlay required"}]
    },
    "forbidden_write_path": {"status": "PASS"},
    "production_source_grounding": {"status": "PASS"},
    "accessibility_minimum": {"status": "WARN", "matches": [{"selector": "button.icon", "issue": "no accessible name"}]},
    "output_schema_validity": {"status": "PASS"}
  },
  "hard_gates": {
    "gate_0_intent_alignment": "BLOCK",
    "gate_0_sub_cause": "form_mismatch",
    "gate_1_production_source_grounding": "PASS",
    "gate_2_boundary_compliance": "PASS",
    "gate_3_no_scaffold_leak": "BLOCK",
    "gate_4_accessibility_minimum": "WARN"
  },
  "soft_scores": null,
  "min_floor_check": null,
  "weighted_score": null,
  "verdict": "REDO",
  "verdict_reason": "gate_0_intent_alignment BLOCK with sub_cause=form_mismatch forces REDO",
  "evidence_selectors": [
    {
      "gate": "gate_0_intent_alignment",
      "selector": "body > div.app",
      "issue": "Full app shell; overlay required",
      "line_range": "L158-L161",
      "expected": "scrim + centered panel"
    }
  ],
  "retry_instruction": {
    "kind": "REDO",
    "fresh_write": true,
    "must_address_gates": ["gate_0_intent_alignment", "gate_3_no_scaffold_leak"],
    "must_quote_evidence": true
  },
  "models_used": {
    "surface_author": null,
    "audit_grader": "claude-sonnet-4-6",
    "cross_review": null,
    "fallback_triggered": false
  },
  "graded_at": "2026-05-17T14:35:00Z"
}
```

**v2.1.0 changes**:
- `hard_gates.gate_0_sub_cause` (new): always present when gate_0 == BLOCK
- `deterministic_validators.surface_morphology.sub_cause` (new): drives the gate_0_sub_cause
- `verdict_reason` (changed): now cites sub_cause when relevant

Note: when `verdict` ∈ {REDO, FIX_NEEDED}, `soft_scores` MAY be null
(short-circuited at hard gate). When verdict = PASS_9PLUS or
FIX_NEEDED-from-soft-floor, `soft_scores` is required.

---

## Schema: CrossReview

Emitted by Codex (or other external) cross-AI per §6.

```json
{
  "$schema": "anchor-wave/v2.1/cross-review",
  "wave_slug": "2026-05-17-pilot",
  "surface_slug": "x-onboarding",
  "reviewer": "codex",
  "reviewer_model": "gpt-5.5",
  "audit_ref": "audits/2026-05-17-pilot/audits/x-onboarding.audit.json",
  "disputed_gates": [
    {
      "gate": "gate_0_intent_alignment",
      "claude_verdict": "BLOCK",
      "codex_agrees": true,
      "codex_evidence": "Body has app shell at L158; no scrim element. Confirmed overlay morphology violation."
    }
  ],
  "additional_findings": [
    {
      "dimension": "consistency_with_siblings",
      "severity": "WARN",
      "issue": "Onboarding step rail differs from case-create-stepper step rail",
      "suggested_fix": "Unify on the case-create-stepper rail pattern",
      "evidence_selector": ".step-rail at L321"
    }
  ],
  "verdict_codex_recommends": "REDO",
  "verdict_codex_disagrees_with_claude": false,
  "top_3_priorities": [
    "Rebuild as overlay (scrim + centered panel)",
    "Replace Install CTAs with Continue/Connect/Create first case",
    "Align step rail with case-create-stepper sibling"
  ],
  "frontier_references": [
    "Linear onboarding: full-screen overlay with right-side rail",
    "Notion onboarding: centered card with progress dots"
  ],
  "reviewed_at": "2026-05-17T14:45:00Z"
}
```

---

## Schema: WaveManifest

Emitted at wave start (draft) and updated at closeout (final).

```json
{
  "$schema": "anchor-wave/v2.1/wave-manifest",
  "wave_slug": "<wave-slug>",
  "mode": "AUDIT_ONLY",
  "max_parallel": 8,
  "quality_bar": 9.0,
  "max_retries": 3,
  "surfaces": ["..."],
  "surface_groups": {"batch_1": ["..."]},
  "verdicts": {"<slug>": "PASS_9PLUS|FIX_NEEDED|REDO|ESCALATE_HUMAN"},
  "stats": {
    "total": 0, "pass_9plus": 0, "fix_needed": 0, "redo": 0, "escalate_human": 0
  },
  "cross_review_count": 0,
  "validators_run": 0,
  "regression_dataset_additions": [],
  "models_used_summary": {},
  "started_at": "...",
  "completed_at": null,
  "human_approver": null
}
```

---

## Validation invariants

Any consumer of these files MUST treat the JSON as authoritative. If
the .md summary disagrees, the JSON wins. Markdown is for humans;
JSON is for the pipeline.
