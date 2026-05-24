#!/usr/bin/env python3
"""
score_audit_json.py — apply §4 verdict rule to a SurfaceAudit JSON
that has had its soft scores filled in by an LLM grader.

v2.1.0 changes from spec/proposal:
- §4.3 morphology sub-cause: gate_0 BLOCK with sub_cause=threshold_only
  OR inner_widget_missing → FIX_NEEDED (not REDO)
- §4.4 maturity-aware floor: innovation floor depends on contract
  surface_innovation_target ∈ {mature, creative, marquee}

Usage:
    python score_audit_json.py <audit.json> [--out <audit.json>] \
        [--quality-bar 9.0] [--contract <contract.json>]

No dependencies. Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SOFT_DIMS = [
    "chassis_consistency",
    "mvp_coverage",
    "visual_quality",
    "interaction_quality",
    "innovation",
    "consistency_with_siblings",
]

DEFAULT_WEIGHTS = {
    "chassis_consistency":       0.20,
    "mvp_coverage":              0.20,
    "visual_quality":            0.15,
    "interaction_quality":       0.15,
    "consistency_with_siblings": 0.15,
    "innovation":                0.15,
}

# v2.1.0 — maturity-aware floors (pilot finding)
INNOVATION_FLOOR_BY_MATURITY = {
    "mature":   5.0,   # rubric: 5-7 target; 5 is acceptable floor
    "creative": 7.5,
    "marquee":  8.5,
}
NON_INNOVATION_FLOOR = 8.5


def resolve_floor(dim: str, innovation_target: str) -> float:
    if dim == "innovation":
        return INNOVATION_FLOOR_BY_MATURITY.get(innovation_target, 5.0)
    return NON_INNOVATION_FLOOR


def score(audit: dict, quality_bar: float, weights: dict, contract: dict | None) -> dict:
    hard = audit.get("hard_gates", {})
    soft = audit.get("soft_scores") or {}
    innovation_target = (contract or {}).get("surface_innovation_target", "mature")

    # v2.1.0 §4.3 — morphology sub-cause short-circuit
    if hard.get("gate_0_intent_alignment") == "BLOCK":
        sub = hard.get("gate_0_sub_cause", "form_mismatch")
        if sub in ("threshold_only", "inner_widget_missing"):
            audit["verdict"] = "FIX_NEEDED"
            audit["verdict_reason"] = f"gate_0 BLOCK sub_cause={sub} → surgical patch suffices (v2.1.0)"
            audit["retry_instruction"] = {
                "kind": "PATCH",
                "fresh_write": False,
                "must_address_gates": ["gate_0_intent_alignment"],
                "must_address_sub_cause": sub,
                "must_quote_evidence": True,
            }
            return audit
        # form_mismatch / missing_scrim → REDO
        audit["verdict"] = "REDO"
        audit["verdict_reason"] = f"gate_0 BLOCK sub_cause={sub} forces REDO (form-level)"
        audit["retry_instruction"] = {
            "kind": "REDO",
            "fresh_write": True,
            "must_address_gates": ["gate_0_intent_alignment"],
            "must_address_sub_cause": sub,
            "must_quote_evidence": True,
        }
        return audit

    if hard.get("gate_1_production_source_grounding") == "BLOCK":
        audit["verdict"] = "REDO"
        audit["verdict_reason"] = "gate_1 BLOCK forces REDO"
        audit["retry_instruction"] = {
            "kind": "REDO", "fresh_write": True,
            "must_address_gates": ["gate_1_production_source_grounding"],
            "must_quote_evidence": True,
        }
        return audit

    blocked = [k for k, v in hard.items()
               if v == "BLOCK" and k != "gate_0_sub_cause"]
    if blocked:
        audit["verdict"] = "FIX_NEEDED"
        audit["verdict_reason"] = f"Hard gates blocked (patchable): {blocked}"
        audit["retry_instruction"] = {
            "kind": "PATCH", "fresh_write": False,
            "must_address_gates": blocked,
            "must_quote_evidence": True,
        }
        return audit

    missing = [d for d in SOFT_DIMS if d not in soft]
    if missing:
        audit["verdict"] = "PENDING_SOFT_SCORE"
        audit["verdict_reason"] = f"Missing soft scores: {missing}"
        return audit

    # v2.1.0 §4.4 — maturity-aware min-floor
    floor_violators = {}
    for d in SOFT_DIMS:
        floor = resolve_floor(d, innovation_target)
        if soft[d] < floor:
            floor_violators[d] = {"score": soft[d], "floor": floor}

    audit["min_floor_check"] = {
        "innovation_target": innovation_target,
        "innovation_floor": INNOVATION_FLOOR_BY_MATURITY.get(innovation_target, 5.0),
        "non_innovation_floor": NON_INNOVATION_FLOOR,
        "violators": floor_violators,
    }

    if floor_violators:
        audit["verdict"] = "FIX_NEEDED"
        audit["verdict_reason"] = f"min-floor violated (maturity={innovation_target}): {floor_violators}"
        audit["retry_instruction"] = {
            "kind": "PATCH", "fresh_write": False,
            "must_address_dims": list(floor_violators.keys()),
            "must_quote_evidence": True,
        }
        return audit

    weighted = sum(weights[d] * soft[d] for d in SOFT_DIMS)
    audit["weighted_score"] = round(weighted, 3)

    if weighted >= quality_bar:
        audit["verdict"] = "PASS_9PLUS"
        audit["verdict_reason"] = f"weighted_score={weighted:.3f} ≥ quality_bar={quality_bar}; maturity={innovation_target}"
        audit["retry_instruction"] = None
    else:
        audit["verdict"] = "FIX_NEEDED"
        audit["verdict_reason"] = f"weighted_score={weighted:.3f} < quality_bar={quality_bar}"
        audit["retry_instruction"] = {
            "kind": "PATCH", "fresh_write": False,
            "must_address_dims": [d for d, s in soft.items() if s < quality_bar],
            "must_quote_evidence": True,
        }

    return audit


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("audit_path", type=Path)
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--quality-bar", type=float, default=9.0)
    p.add_argument("--contract", type=Path, default=None,
                   help="Path to SurfaceContract JSON for maturity-aware floor")
    p.add_argument("--weights", type=Path, default=None,
                   help="Optional JSON file overriding default weights")
    args = p.parse_args()

    audit = json.loads(args.audit_path.read_text(encoding="utf-8"))

    weights = DEFAULT_WEIGHTS
    if args.weights:
        weights = json.loads(args.weights.read_text(encoding="utf-8"))
        total = sum(weights.values())
        if abs(total - 1.0) > 0.001:
            print(f"ERROR: weights sum to {total}, must be 1.0", file=sys.stderr)
            return 2

    contract = None
    if args.contract and args.contract.exists():
        contract = json.loads(args.contract.read_text(encoding="utf-8"))

    audit = score(audit, args.quality_bar, weights, contract)

    out_path = args.out or args.audit_path
    out_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = {
        "surface": audit.get("surface_slug"),
        "verdict": audit.get("verdict"),
        "verdict_reason": audit.get("verdict_reason"),
        "weighted_score": audit.get("weighted_score"),
        "min_floor_check": audit.get("min_floor_check"),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
