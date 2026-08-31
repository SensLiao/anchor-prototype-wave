# Example — 2026-08-31 — Signal anchor

A real, small exercise of this skill's two runnable pieces: the **master gallery** filled with a
genuine anchor, and `scripts/validate_surface.py` run for real against three surfaces.

## Where the surfaces came from

This skill is the downstream half of a pair. The upstream skill,
[`prototyping-ui-directions`](https://github.com/SensLiao/prototyping-ui-directions), produced three
UI directions for *Tracewell* (a canvas for reading finished agent runs) and its comparison report
recommends **Direction C — Signal** for latency and stall analysis.

Signal is therefore the locked visual anchor here: dark instrument chassis, `Inter` / `JetBrains
Mono`, 6px card radius, hairline borders, and a single accent `oklch(0.78 0.16 190)` spent only on
the traced critical path.

## What was actually run

```bash
python scripts/validate_surface.py <surface-dir> --wave-slug agent-run-canvas --out <audit.json>
```

Three surfaces, three audits, all committed under [`audits/`](audits/):

| Surface | Verdict | Hard gates |
| --- | --- | --- |
| `variant-3` (Signal — the anchor) | `PENDING_SOFT_SCORE` | 4 PASS · 1 WARN |
| `variant-2` (Field Notes) | `PENDING_SOFT_SCORE` | 4 PASS · 1 WARN |
| `variant-1` (Blueprint) | **`FIX_NEEDED`** | 3 PASS · 1 WARN · **1 BLOCK** |

## The interesting result

`variant-1` was blocked by the `decorative_gradient` validator, on this match:

```json
{"selector": "body", "gradient": "linear-gradient(to right, var(--color-grid-minor)", "line": 17}
```

That gradient is not decoration. It is a **1px drafting grid** — two `linear-gradient` stops drawing
hairlines 22px apart, which is the whole visual premise of the Blueprint direction.

This is recorded rather than patched away, because the finding is about the *validator*, not the
surface: `check_decorative_gradient` cannot currently distinguish a hairline grid from a gradient
blob. The obvious refinement is to exempt gradients whose colour stops are ≤2px apart, which is
exactly the shape a grid takes and never the shape a decorative wash takes. Filed here rather than
fixed, because changing a gate rule on the strength of one sample is how gates stop meaning anything.

The `WARN` on every surface is honest too: `gate_1_production_source_grounding` reports
`"no contract supplied; cannot verify grounding"` — no contract file was passed, so the gate
correctly declines to certify.

## What was *not* run

`score_audit_json.py` applies the §4 verdict rule **after** an LLM grader fills in the six soft
dimensions. No grader was run, so every soft score is null, every grade cell in the gallery reads
`—`, and `AVG SELF-GRADE` shows `—/10` rather than an invented number. The verdicts above are the
deterministic half of the pipeline only, which is exactly what `PENDING_SOFT_SCORE` means.

## Files

| Path | What it is |
| --- | --- |
| [`master-gallery.html`](master-gallery.html) | `ASSETS/master-gallery-template.html` with all 74 placeholders filled from the Signal anchor. Open it in a browser. |
| [`audits/*.audit.json`](audits/) | The three raw `SurfaceAudit` documents, exactly as the validator wrote them. |
