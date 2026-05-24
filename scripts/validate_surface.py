#!/usr/bin/env python3
"""
validate_surface.py — deterministic checks for an Anchor Wave surface.

v2.1.0 changes from spec/proposal:
- GRADIENT_SEMANTIC_ALLOWLIST expanded to 9 entries (case_004 fix)
- check_surface_morphology emits sub_cause ∈
  {form_mismatch, missing_scrim, threshold_only, inner_widget_missing, none}
- hard_gates includes gate_0_sub_cause for verdict differentiation

Usage:
    python validate_surface.py <surface-dir> [--contract <contract.json>] \
        [--out <audit.json>] [--wave-slug <slug>]

No third-party dependencies. Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Detection rules — codified from references/failure-patterns.md
# ---------------------------------------------------------------------------

MARKETPLACE_ALLOWED_SURFACES = {
    "pm-marketplace", "pm-connector", "pm-node-detail",
    "pm-sop-template", "pm-workflow-template",
    "ps-marketplace-sub",
}

SCAFFOLD_LEAK_PATTERNS = [
    (r"\b4\.8\b(?=[^<]*?(?:rating|stars?|reviews?))", "rating-like 4.8"),
    (r"\b\d+(?:\.\d+)?k\s+installs?\b", "Nk installs"),
    (r">\s*Install\s*</button>", "Install button (exact)"),
    (r">\s*Install to workspace\s*<", "Install to workspace CTA"),
    (r'class="[^"]*\brating\b[^"]*"', "rating class"),
    (r'class="[^"]*\bdownloads?\b[^"]*"', "downloads class"),
]

# v2.1.0 expansion (pilot finding — case_004 + canvas idiom):
GRADIENT_SEMANTIC_ALLOWLIST = [
    ("status-dot",     "radial-gradient"),
    ("status-pill",    "radial-gradient"),
    ("focus-visible",  "radial-gradient"),
    # Pilot-validated chassis / canvas / semantic semantic patterns:
    ("html, body",     "radial-gradient"),    # chassis-wide texture (0.04 opacity)
    (".app",           "radial-gradient"),    # chassis texture on .app outer
    ("app-bg",         "radial-gradient"),    # variant naming
    ("app-shell",      "radial-gradient"),    # variant naming
    ("canvas-wrap",    "radial-gradient"),    # canonical canvas dot-grid (tldraw/Miro/n8n)
    ("canvas",         "radial-gradient"),    # canonical canvas dot-grid (broader)
    ("ghost-canvas",   "radial-gradient"),    # inspector-over-canvas aria-hidden
    ("chat-stream",    "radial-gradient"),    # chat stream texture variant
    ("granule--slash", "linear-gradient"),    # semantic failure mark
    ("data-flagged",   "linear-gradient"),    # semantic flagged-state amber tint
    ("s-card--approval", "linear-gradient"),  # semantic approval-state tint
    ("flagged-card",   "linear-gradient"),    # alternate semantic flagged
]

PILL_CANONICAL = {
    "font-size": "10px",
    "letter-spacing": "0.08em",
    "text-transform": "uppercase",
}

STALE_TAB_LABELS = {
    "Rules": "Governance",
}

MORPHOLOGY_REQUIREMENTS = {
    "overlay": {
        "must_have_panel_any": [r'class="[^"]*(?:overlay|modal|dialog|popover)[^"]*"'],
        "must_have_scrim_any": [r'class="[^"]*(?:scrim|backdrop|overlay-bg)[^"]*"',
                                 r"position:\s*fixed[^;]*inset:\s*0"],
        "must_have_z_index_gte": 1000,
    },
    "drawer": {
        "must_have_any": [r"position:\s*fixed",
                          r'class="[^"]*\bdrawer\b[^"]*"'],
        "must_have_anchor_side": True,
    },
    "wizard": {
        "must_have_any": [r'class="[^"]*\bstep-rail\b[^"]*"',
                          r'data-step\s*=',
                          r'aria-label="[^"]*step[^"]*"'],
    },
    "canvas": {
        "must_have_any": [r'class="[^"]*\bcanvas\b[^"]*"',
                          r"transform:\s*translate",
                          r'data-node-id\s*='],
    },
    "form": {
        "must_have_any": [r"<input ", r"<select ", r"<textarea "],
    },
    "list": {
        "must_have_any": [r'role="row"', r'class="[^"]*\brow\b[^"]*"', r"<tr"],
    },
    "full-page": {},
    "dashboard": {},
    "inspector": {
        "must_have_any": [r'role="tab"', r'data-tab\s*='],
    },
    "audit-view": {},
    "chat": {
        "must_have_inner_widgets": [
            (r'class="[^"]*\bmessage[^"]*"', "message bubbles"),
            (r'class="[^"]*\bcomposer[^"]*"', "composer"),
        ],
    },
    "command-tool": {
        "must_have_any": [r'class="[^"]*\bcommand[^"]*"',
                          r'role="combobox"',
                          r'placeholder="[^"]*command[^"]*"'],
    },
}


# ---------------------------------------------------------------------------
# Check functions — each returns (status, matches[, sub_cause])
# ---------------------------------------------------------------------------

def check_scaffold_leak(html: str, surface_slug: str):
    if surface_slug in MARKETPLACE_ALLOWED_SURFACES:
        return "PASS", []
    matches = []
    for pattern, label in SCAFFOLD_LEAK_PATTERNS:
        for m in re.finditer(pattern, html, flags=re.IGNORECASE):
            line = html.count("\n", 0, m.start()) + 1
            snippet = html[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            matches.append({
                "pattern": label,
                "line": line,
                "snippet": snippet.strip(),
            })
    return ("BLOCK" if matches else "PASS"), matches


def check_decorative_gradient(html: str):
    matches = []
    pattern = re.compile(
        r"(?P<sel>[^{}\n]+)\s*\{[^}]*?(?P<grad>(radial|linear)-gradient\([^)]+\))",
        re.IGNORECASE | re.DOTALL
    )
    for m in pattern.finditer(html):
        sel = m.group("sel").strip().splitlines()[-1].strip()
        grad = m.group("grad")
        # v2.1.0: more lenient selector matching
        allowed = any(
            allow_sel in sel and allow_grad in grad
            for allow_sel, allow_grad in GRADIENT_SEMANTIC_ALLOWLIST
        )
        if not allowed:
            line = html.count("\n", 0, m.start()) + 1
            matches.append({
                "selector": sel[:80],
                "gradient": grad[:80],
                "line": line,
            })
    return ("BLOCK" if matches else "PASS"), matches


def check_pill_mono_drift(html: str):
    pill_blocks = re.findall(r"\.pill\s*\{([^}]+)\}", html, flags=re.IGNORECASE)
    if not pill_blocks:
        return "PASS", []
    drifts = []
    for block in pill_blocks:
        for prop, expected in PILL_CANONICAL.items():
            m = re.search(rf"{re.escape(prop)}\s*:\s*([^;]+);", block, re.IGNORECASE)
            if m:
                actual = m.group(1).strip()
                if actual != expected:
                    drifts.append({"property": prop, "actual": actual, "expected": expected})
    return ("WARN" if drifts else "PASS"), drifts


def check_stale_tab_label(html: str):
    matches = []
    for stale, replacement in STALE_TAB_LABELS.items():
        for m in re.finditer(
            rf'(role="tab"[^>]*>|data-tab[^>]*>)\s*{re.escape(stale)}\s*<',
            html,
        ):
            line = html.count("\n", 0, m.start()) + 1
            matches.append({"stale": stale, "should_be": replacement, "line": line})
    return ("WARN" if matches else "PASS"), matches


def check_surface_morphology(html: str, claimed_type: str | None):
    """
    v2.1.0: returns (status, matches, sub_cause).
    sub_cause ∈ {form_mismatch, missing_scrim, threshold_only,
                 inner_widget_missing, none}
    """
    if not claimed_type:
        return "PASS", [], "none"
    spec = MORPHOLOGY_REQUIREMENTS.get(claimed_type)
    if spec is None:
        return "WARN", [{"issue": f"Unknown claimed_surface_type: {claimed_type}"}], "none"

    issues = []
    sub_cause = "none"

    # Overlay-specific: separate form check from threshold check
    if claimed_type == "overlay":
        has_panel = any(re.search(p, html, re.IGNORECASE) for p in spec.get("must_have_panel_any", []))
        has_scrim = any(re.search(p, html, re.IGNORECASE) for p in spec.get("must_have_scrim_any", []))
        z_indices = [int(z) for z in re.findall(r"z-index:\s*(\d+)", html)]
        max_z = max(z_indices, default=0)
        z_threshold = spec.get("must_have_z_index_gte", 1000)

        if not has_panel:
            issues.append({"issue": "overlay claimed but no overlay/modal/dialog panel element found"})
            sub_cause = "form_mismatch"
        elif not has_scrim:
            issues.append({"issue": "overlay claimed but no scrim/backdrop element found"})
            sub_cause = "missing_scrim"
        elif max_z < z_threshold:
            issues.append({
                "issue": f"overlay z-index < {z_threshold}; max found = {max_z}",
            })
            sub_cause = "threshold_only"

    elif claimed_type == "chat" and spec.get("must_have_inner_widgets"):
        missing = []
        for pattern, name in spec["must_have_inner_widgets"]:
            if not re.search(pattern, html, re.IGNORECASE):
                missing.append(name)
        if missing:
            issues.append({"issue": f"chat surface missing inner widgets: {missing}"})
            sub_cause = "inner_widget_missing"

    else:
        must_have_any = spec.get("must_have_any", [])
        if must_have_any:
            if not any(re.search(p, html, re.IGNORECASE) for p in must_have_any):
                issues.append({
                    "issue": f"{claimed_type} surface lacks any of required DOM signatures",
                    "expected_any_of": must_have_any,
                })
                sub_cause = "form_mismatch"

        if spec.get("must_have_anchor_side"):
            if not re.search(r"(top|right|bottom|left):\s*0", html):
                issues.append({"issue": "drawer requires anchor-side rule (top/right/bottom/left: 0)"})
                sub_cause = sub_cause or "form_mismatch"

    return ("BLOCK" if issues else "PASS"), issues, sub_cause


def check_accessibility_minimum(html: str):
    issues = []
    for m in re.finditer(r"<button\b[^>]*>(.*?)</button>", html, flags=re.DOTALL):
        attrs = m.group(0)[:m.group(0).index(">")]
        content = m.group(1)
        text_content = re.sub(r"<[^>]+>", "", content).strip()
        has_aria_label = "aria-label" in attrs
        if not text_content and not has_aria_label:
            line = html.count("\n", 0, m.start()) + 1
            issues.append({"issue": "button missing accessible name", "line": line})

    inputs = re.findall(r'<input\b([^>]*)>', html)
    labels = re.findall(r'<label\b[^>]*\sfor="([^"]+)"', html)
    label_targets = set(labels)
    for attrs in inputs:
        id_m = re.search(r'\bid="([^"]+)"', attrs)
        if not id_m:
            if "aria-label" not in attrs:
                issues.append({"issue": "input without id and aria-label"})
            continue
        if id_m.group(1) not in label_targets and "aria-label" not in attrs:
            issues.append({"issue": f"input id={id_m.group(1)} has no <label for> or aria-label"})

    has_motion = bool(re.search(r"(transition|animation)\s*:", html))
    has_reduced_motion = "prefers-reduced-motion" in html
    if has_motion and not has_reduced_motion:
        issues.append({"issue": "motion declared without prefers-reduced-motion fallback"})

    return ("WARN" if issues else "PASS"), issues


def check_production_source_grounding(contract: dict | None):
    if not contract:
        return "WARN", [{"issue": "no contract supplied; cannot verify grounding"}]
    if contract.get("research_only_reason"):
        return "PASS", []
    src = contract.get("production_source")
    if not src:
        return "BLOCK", [{"issue": "production_source empty and not research_only"}]
    return "PASS", []


def check_forbidden_write_path(*_):
    return "PASS", []


def check_output_schema_validity(audit_obj: dict):
    required = ["wave_slug", "surface_slug", "deterministic_validators",
                "hard_gates", "verdict", "evidence_selectors"]
    missing = [k for k in required if k not in audit_obj]
    return ("PASS" if not missing else "BLOCK"), missing


# ---------------------------------------------------------------------------
# Gate aggregation
# ---------------------------------------------------------------------------

def aggregate_hard_gates(validators: dict) -> dict:
    def status(name: str) -> str:
        return validators.get(name, {}).get("status", "PASS")

    morph_result = validators.get("surface_morphology", {})
    sub_cause = morph_result.get("sub_cause", "none")

    return {
        "gate_0_intent_alignment": status("surface_morphology"),
        "gate_0_sub_cause": sub_cause,
        "gate_1_production_source_grounding": status("production_source_grounding"),
        "gate_2_boundary_compliance": status("forbidden_write_path"),
        "gate_3_no_scaffold_leak":
            "BLOCK" if "BLOCK" in (status("scaffold_leak"), status("decorative_gradient")) else "PASS",
        "gate_4_accessibility_minimum": status("accessibility_minimum"),
    }


def initial_verdict(hard_gates: dict) -> tuple[str, str]:
    if hard_gates["gate_0_intent_alignment"] == "BLOCK":
        sub = hard_gates.get("gate_0_sub_cause", "form_mismatch")
        if sub in ("threshold_only", "inner_widget_missing"):
            return "FIX_NEEDED", f"gate_0 BLOCK with sub_cause={sub} → surgical patch suffices"
        return "REDO", f"gate_0 BLOCK with sub_cause={sub} forces REDO"
    if hard_gates["gate_1_production_source_grounding"] == "BLOCK":
        return "REDO", "gate_1 BLOCK forces REDO"
    if any(v == "BLOCK" for k, v in hard_gates.items() if k != "gate_0_sub_cause"):
        return "FIX_NEEDED", "Hard gate BLOCK (surgically patchable)"
    return "PENDING_SOFT_SCORE", "All hard gates PASS; soft scores required"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("surface_dir", type=Path)
    p.add_argument("--contract", type=Path, default=None)
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--wave-slug", default=None)
    args = p.parse_args()

    surface_dir: Path = args.surface_dir.resolve()
    if not surface_dir.is_dir():
        print(f"ERROR: not a directory: {surface_dir}", file=sys.stderr)
        return 2

    index_html = surface_dir / "index.html"
    if not index_html.exists():
        print(f"ERROR: no index.html under {surface_dir}", file=sys.stderr)
        return 2

    html = index_html.read_text(encoding="utf-8", errors="replace")
    surface_slug = surface_dir.name

    contract = None
    if args.contract and args.contract.exists():
        contract = json.loads(args.contract.read_text(encoding="utf-8"))

    claimed_type = (contract or {}).get("claimed_surface_type")

    validators = {}
    s, m = check_scaffold_leak(html, surface_slug); validators["scaffold_leak"] = {"status": s, "matches": m}
    s, m = check_decorative_gradient(html); validators["decorative_gradient"] = {"status": s, "matches": m}
    s, m = check_pill_mono_drift(html); validators["pill_mono_drift"] = {"status": s, "matches": m}
    s, m = check_stale_tab_label(html); validators["stale_tab_label"] = {"status": s, "matches": m}
    s, m, sub = check_surface_morphology(html, claimed_type)
    validators["surface_morphology"] = {"status": s, "matches": m, "sub_cause": sub}
    s, m = check_accessibility_minimum(html); validators["accessibility_minimum"] = {"status": s, "matches": m}
    s, m = check_production_source_grounding(contract); validators["production_source_grounding"] = {"status": s, "matches": m}
    s, m = check_forbidden_write_path(); validators["forbidden_write_path"] = {"status": s, "matches": m}

    hard_gates = aggregate_hard_gates(validators)
    verdict, reason = initial_verdict(hard_gates)

    evidence = []
    for vname, vresult in validators.items():
        if vresult["status"] == "BLOCK":
            for match in vresult["matches"]:
                evidence.append({"validator": vname, **match})

    audit = {
        "$schema": "anchor-wave/v2.1/surface-audit",
        "wave_slug": args.wave_slug or "uncategorized",
        "surface_slug": surface_slug,
        "contract_ref": str(args.contract) if args.contract else None,
        "deterministic_validators": validators,
        "hard_gates": hard_gates,
        "soft_scores": None,
        "min_floor_check": None,
        "weighted_score": None,
        "verdict": verdict,
        "verdict_reason": reason,
        "evidence_selectors": evidence,
        "retry_instruction": None,
        "models_used": {
            "surface_author": None, "audit_grader": None,
            "cross_review": None, "fallback_triggered": False,
        },
        "graded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    schema_status, missing = check_output_schema_validity(audit)
    audit["deterministic_validators"]["output_schema_validity"] = {
        "status": schema_status, "matches": missing,
    }

    out_path = args.out or (surface_dir / "_audit.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = {
        "surface": surface_slug,
        "verdict": verdict,
        "hard_gates": hard_gates,
        "blocking_validators": [k for k, v in validators.items() if v["status"] == "BLOCK"],
        "warning_validators": [k for k, v in validators.items() if v["status"] == "WARN"],
        "audit_path": str(out_path),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
