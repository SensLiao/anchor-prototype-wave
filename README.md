<div align="right"><a href="README.zh-CN.md">简体中文</a></div>

<p align="center"><img src="docs/hero.png" alt="anchor-prototype-wave — one locked anchor, a whole wave of gated high-fidelity pages" width="100%"></p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-skill-db2777?style=flat" alt="Claude Code skill">
  <img src="https://img.shields.io/badge/scripts-Python%203.10%2B%20·%20stdlib%20only-db2777?style=flat" alt="Scripts: Python 3.10+, standard library only">
  <img src="https://img.shields.io/badge/license-MIT-2f9e44?style=flat" alt="License: MIT">
</p>

`anchor-prototype-wave` is a Claude Code skill that turns one locked visual anchor plus a list of pages into a full high-fidelity HTML prototype wave in a single run. It fans out parallel per-surface subagents, then gates every page through three layers — deterministic validators, an LLM grader, and cross-model (Codex) review — repairing failures in place before aggregating a master gallery. It is built for designers and engineers who need many pages that stay faithful to one reference, without hand-checking each page for drift or leftover boilerplate.

<p align="center">
  <a href="#-quick-start">Quick start</a> ·
  <a href="#-the-14-stage-pipeline">Pipeline</a> ·
  <a href="#-quality-gates">Quality gates</a> ·
  <a href="#-model-configuration">Model config</a> ·
  <a href="https://github.com/SensLiao/prototyping-ui-directions">Upstream skill</a>
</p>

## 🧭 Overview

**Problem.** Once a design direction is locked, someone still has to produce the other fifteen screens — and keep every one of them on-chassis. LLMs are good at generating a page and bad at staying consistent across twenty: accent colors drift, placeholder text leaks into "finished" pages, and a human reviewer ends up re-auditing every surface by eye. The review burden grows linearly with the page count, which defeats the point of generating them.

**Solution.** This skill turns page mass-production into a gated pipeline. The anchor (typography, palette, radii, spacing, banned styles) is frozen into a written contract that every subagent must read; pages are generated in parallel and then judged three ways — a deterministic Python validator no model can argue with, an LLM grader scoring six weighted dimensions against written rubric anchors, and a second-opinion review from a *different* model family. Anything that fails is retried with the failing evidence quoted verbatim, at most three times, and what still fails is escalated to a human rather than silently shipped.

**Scope.** This is a Claude Code *skill* — a Markdown-defined orchestration procedure plus two standalone Python scripts — not a library or app. It never auto-triggers (`disable-model-invocation: true`); you invoke it explicitly. Generated waves land in your project's `ui-lab/` directory and are not stored in this repository.

**Key terms** (for a cold reader): a **surface** is one screen/page of the prototype; the **anchor** is the locked visual reference every surface must match; a **scaffold leak** is placeholder or boilerplate that slips into a finished page.

## ✨ Highlights

- **A 14-stage pipeline (Stage 0–13)** that carries a wave from locked anchor to aggregated gallery in one conversational run — no flags, no modes to pick.
- **Parallel surface subagents**, batched ≤10 and auto-splitting beyond that, so large page lists fan out without manual chunking.
- **A deterministic floor no model can talk past** — 9 scripted checks aggregating into 5 hard gates, run by a stdlib-only Python validator.
- **Rubric-anchored soft scoring** — 6 weighted dimensions with per-page maturity floors (`mature` / `creative` / `marquee`), resolving to four verdicts: `PASS_9PLUS`, `FIX_NEEDED`, `REDO`, `ESCALATE_HUMAN`.
- **Fix-on-fail, never fake-pass** — failing surfaces are repaired in place (≤3 retries, each retry prompt quoting the failing gate's evidence verbatim); exhausted retries escalate to a human, never auto-pass.
- **Cross-model review** — Codex re-reviews every failure plus a 15% sample of passes; in the recorded pilot it overturned the first grader's `REDO` verdict in 2 of 4 disputes, which is exactly why a second model family is in the loop.
- **A shared grading vocabulary** — 12 surface-morphology types and 10 enumerated anti-patterns keep "this page is wrong" specific and reproducible.
- **Model-agnostic by construction** — every model choice comes from six environment variables; no model name is hardcoded in the skill or the scripts.

## 📊 Field evidence

The pipeline was distilled from a real two-day production run, written up in [`examples/2026-05-12-track-b-v2-wave.md`](examples/2026-05-12-track-b-v2-wave.md): **15 prototype pages, 34,991 lines of HTML, in roughly 16 hours against an estimated ~70 sequential hours (~4.4×)**, with an average self-grade of 9.0 and zero production code touched. The v2.1 promotion gate then ran a 12-surface field test recorded in the [CHANGELOG](CHANGELOG.md): 12/12 validator reproducibility, 0/12 scaffold leaks reaching the gallery. Wave outputs themselves live in the origin project, not in this repo — the numbers above are from those written records.

## 🏗 Architecture

<p align="center"><img src="docs/architecture.png" alt="anchor-prototype-wave architecture — locked anchor fans out to parallel surfaces, each passing three validation layers before the gallery" width="100%"></p>

<p align="center"><sub>One anchor, N parallel surfaces, three layers of gating, and a repair loop before anything reaches the gallery.</sub></p>

The run has three phases. **Contracts first**: the anchor is written down as a declaration document, the reusable element index is frozen, and each page gets a machine-readable `SurfaceContract` before any generation starts — a subagent spawned without a contract is one of the codified anti-patterns. **Parallel generation**: each surface subagent reads the shared context and writes exactly one file, its own `<slug>/index.html`, so agents cannot trample each other. **Gate, repair, aggregate**: every page passes the deterministic validator, the LLM grader, and (when triggered) cross-model review; failures loop back with evidence, and survivors are aggregated into a master gallery with per-page verdict badges.

## 🔢 The 14-stage pipeline

| Stage | What happens |
| --- | --- |
| 0 — Anchor doc author | The locked anchor is written into `audits/anchor-decl.md`. |
| 1 — Element index freeze | The reusable element inventory is frozen (`audits/element-index.md`). |
| 2 — Context author | `audits/_context.md` — the chassis contract every subagent reads. |
| 3 — Surface classification | Each page is classed `mature` / `creative` / `marquee` and typed against the 12 morphologies. |
| 4 — Surface contracts | One machine-readable `SurfaceContract` JSON per page. |
| 5 — Parallel generation | N surface subagents spawn (≤10 per batch); each writes only its own `<slug>/index.html`. |
| 6 — Deterministic validator | `scripts/validate_surface.py` runs the 9 checks per surface. |
| 7 — LLM grader | Six soft dimensions scored against written rubric anchors. |
| 8 — Scorer | `scripts/score_audit_json.py` computes the composite, applies maturity floors, resolves a verdict. |
| 9 — Cross-AI review | Codex reviews per the trigger matrix (all failures + 15% of passes). |
| 10 — Fix-on-fail loop | `FIX_NEEDED` → surgical patch; `REDO` → fresh rewrite; ≤3 retries, then `ESCALATE_HUMAN`. |
| 11 — Master gallery | Survivors are aggregated into a filterable gallery `index.html`. |
| 12 — Manifest + closeout | `manifest.json` updated; new failure patterns appended to the regression list. |
| 13 — Report | Counts, gallery link, and any human-escalations, back to you. |

## 🚦 Quality gates

<p align="center"><img src="docs/gates.png" alt="The gating funnel: nine deterministic checks feed five hard gates, then six weighted soft dimensions resolve to four verdicts, with a retry loop back to the start" width="100%"></p>
<p align="center"><sub>The funnel every surface passes: a deterministic floor, then weighted scoring with maturity-aware floors, then a verdict — and failures loop back carrying their evidence.</sub></p>

**Hard gates** — the deterministic floor. The validator's 9 checks aggregate into 5 gates; any `BLOCK` fails the surface regardless of how well it scores elsewhere (treating a high average as an override is anti-pattern A1):

| Gate | Fed by | Catches |
| --- | --- | --- |
| 0 · Intent alignment | `surface_morphology` | The page is the wrong *kind* of surface (a drawer built as a full page), with a `sub_cause` so fixes are targeted. |
| 1 · Production source grounding | `production_source_grounding` | The page ignores the real production sources its contract names. |
| 2 · Boundary compliance | orchestrator-enforced | A subagent writing outside its own `<slug>/index.html`. |
| 3 · No scaffold leak | `scaffold_leak` + `decorative_gradient` | Placeholder boilerplate, and decorative gradients outside the semantic allowlist. |
| 4 · Accessibility minimum | `accessibility_minimum` | Missing the accessibility floor. |

Three further checks (`pill_mono_drift`, `stale_tab_label`, `output_schema_validity`) run as advisories and audit-JSON integrity checks without feeding a gate.

**Soft dimensions** — graded 0–10 against written rubric anchors, then combined by weight:

| Dimension | Weight | Floor |
| --- | --- | --- |
| Chassis consistency | 0.20 | 8.5 |
| MVP coverage | 0.20 | 8.5 |
| Visual quality | 0.15 | 8.5 |
| Interaction quality | 0.15 | 8.5 |
| Consistency with siblings | 0.15 | 8.5 |
| Innovation | 0.15 | 5.0 / 7.5 / 8.5 by maturity (`mature` / `creative` / `marquee`) |

A composite of **9.0** is the quality bar; any floor violation resolves to `FIX_NEEDED` no matter the composite. The maturity-aware innovation floor is the mechanism that lets a settings page be plain while a marquee page must not be.

## 🚀 Quick start

### Requirements

- **Claude Code** (the skill host)
- **Python 3.10+** for the two validator/scorer scripts — standard library only, nothing to install
- The **`codex-dispatch`** skill plus the Codex CLI, for the cross-model review stage (the rest of the pipeline runs without it)

### Install

```bash
# Project-scoped install
git clone https://github.com/SensLiao/anchor-prototype-wave .claude/skills/anchor-prototype-wave
```

<details>
<summary>Global install (all projects)</summary>

```bash
git clone https://github.com/SensLiao/anchor-prototype-wave ~/.claude/skills/anchor-prototype-wave
```

</details>

### Invoke

Ask for a wave conversationally, giving the two things the skill needs — an anchor and a page list:

```text
Take the anchor from ui-lab/v2-anchor/ and generate the wave for:
dashboard, case-library, case-workspace, settings, login
```

### What you should see

The skill stops and asks only when inputs are incomplete — otherwise it runs the whole pipeline unattended. Outputs land under `ui-lab/<date>-<anchor-slug>-anchor-prototypes/`: one `<slug>/index.html` per page, an `audits/` directory with the anchor declaration, per-surface contracts and audit JSONs, and a master gallery `index.html` with per-page verdict badges. Anything graded `ESCALATE_HUMAN` after three repairs is listed for your decision — never silently included.

## 🧾 Inputs reference

**The anchor (chassis)** must declare: typography (sans family + weights, mono family), the radius scale, the hairline border value, one accent color (a second requires explicit declaration), banned tokens (e.g. glass/blur/aurora/dark-by-default/decorative gradients), status colors (amber/blue/green/red, bg+fg), surface and text color roles, the spacing scale, and shadow values. [`ASSETS/anchor-doc-template.md`](ASSETS/anchor-doc-template.md) is the fill-in skeleton.

**The page list** — per entry: a kebab-case `slug`, a display title, a one-line intent, a route, a group, and optional status/risk hints plus an explicit content brief. **Output directory** defaults to `ui-lab/<date>-<anchor-slug>-anchor-prototypes/`.

## 🔧 Running the validators standalone

Both scripts are dependency-free and runnable outside the skill — for spot-checking a single page or wiring into your own harness:

```bash
python scripts/validate_surface.py <surface-dir> --contract audits/contracts/<slug>.contract.json
python scripts/score_audit_json.py <surface-dir>/_audit.json --quality-bar 9.0
```

`validate_surface.py` writes the full audit JSON next to the page and prints a compact summary — `surface`, `verdict`, `hard_gates`, `blocking_validators`, `warning_validators`, `audit_path` — to stdout. Note that **a failing verdict still exits 0** (exit 2 is reserved for a missing directory/`index.html`), so a CI wrapper should parse the stdout JSON's `verdict` field rather than the exit code. `score_audit_json.py` accepts `--weights <weights.json>` to re-weight the six dimensions (must sum to 1.0).

## 🖼 A real audit, committed

[`examples/2026-08-31-signal-anchor/`](examples/2026-08-31-signal-anchor/) exercises the two runnable
pieces of this skill for real: the master gallery filled from a genuine anchor, and
`validate_surface.py` run against three surfaces produced by the upstream skill,
[`prototyping-ui-directions`](https://github.com/SensLiao/prototyping-ui-directions).

<p align="center"><img src="docs/example-gallery.png" alt="The master gallery rendered with the Signal anchor: anchor version stack, stats strip, foundation elements and surface prototype cards, all on the dark instrument chassis" width="100%"></p>

<p align="center"><sub><code>ASSETS/master-gallery-template.html</code> with all 74 placeholders filled from the locked Signal chassis — <code>Inter</code>/<code>JetBrains&nbsp;Mono</code>, 6px radius, hairline borders, one accent at <code>oklch(0.78 0.16 190)</code>. The gallery is built <em>in</em> the anchor it is presenting, which is how the chassis gets proven at ensemble scale before any single surface is promoted.</sub></p>

<p align="center"><img src="docs/example-audit.png" alt="Terminal output of validate_surface.py on three surfaces: two return PENDING_SOFT_SCORE with all hard gates passing, one returns FIX_NEEDED with a BLOCK on decorative_gradient" width="100%"></p>

<p align="center"><sub>Real output. Three surfaces audited, two all-PASS, one BLOCK — and the BLOCK is the interesting part.</sub></p>

**The validator flagged a false positive, and it stayed flagged.** `variant-1` was blocked by
`decorative_gradient` on `{"selector": "body", "gradient": "linear-gradient(to right, var(--color-grid-minor)", "line": 17}`
— which is not decoration at all, but a **1px drafting grid**, the entire visual premise of that
direction. The finding is about the rule rather than the page: `check_decorative_gradient` cannot yet
tell a hairline grid from a gradient blob. It is [recorded in the example](examples/2026-08-31-signal-anchor/)
with the obvious refinement (exempt gradients whose stops sit ≤2px apart) rather than quietly
patched, because loosening a gate on the strength of one sample is how gates stop meaning anything.

**Half the pipeline deliberately did not run.** `score_audit_json.py` applies the §4 verdict rule
*after* an LLM grader fills the six soft dimensions. No grader was run here, so every soft score is
null, every grade cell in the gallery reads `—`, and `AVG SELF-GRADE` shows `—/10` instead of an
invented number. `PENDING_SOFT_SCORE` is precisely what those two surfaces earned.

## 🎛 Model configuration

No model name is hardcoded anywhere. All routing comes from six environment variables (defaults from [`references/model-policy.md`](references/model-policy.md)):

| Variable | Default | Used for |
| --- | --- | --- |
| `CLAUDE_DECISION_MODEL` | `claude-opus-4-7` | Orchestration, anchor authoring, creative/marquee surfaces |
| `CLAUDE_EXECUTION_MODEL` | `claude-sonnet-4-6` | Mature surfaces, per-surface grading |
| `CLAUDE_TOOL_MODEL` | `claude-haiku-4-5-20251001` | Summaries, JSON schema checks |
| `CODEX_REVIEW_MODEL` | `gpt-5.5` | Full cross-reviews of `REDO` / `FIX_NEEDED` |
| `CODEX_LIGHT_MODEL` | `gpt-5.4-mini` | The 15% pass sample and post-fix re-audits |
| `CODEX_FALLBACK_MODEL` | `gpt-5.4` | When the primary is unavailable (recorded in the audit) |

## 🗺 Repository map

| Path | What it holds |
| --- | --- |
| [`SKILL.md`](SKILL.md) | The full pipeline definition — stages, stop rules, trigger matrix, anti-patterns. |
| [`scripts/`](scripts/) | `validate_surface.py` (439 lines) + `score_audit_json.py` (203 lines) — stdlib-only. |
| [`examples/`](examples/) | One real filled master gallery and three committed `SurfaceAudit` documents from an actual validator run. |
| [`references/`](references/) | The rulebook: [`gates.md`](references/gates.md), [`scoring-rubric.md`](references/scoring-rubric.md), [`surface-taxonomy.md`](references/surface-taxonomy.md) (12 morphologies), [`failure-patterns.md`](references/failure-patterns.md) (regression cases), [`model-policy.md`](references/model-policy.md), [`output-schema.md`](references/output-schema.md) (4 JSON schemas), [`master-gallery-structure.md`](references/master-gallery-structure.md), [`skills-dependencies.md`](references/skills-dependencies.md). |
| [`ASSETS/`](ASSETS/) | 11 fill-in templates: anchor declaration, shared context, surface/element prompts, Codex review prompt, gallery HTML, quality-gate checklist, writeups. |
| [`examples/`](examples/) | The recorded pilot-run writeup and a blank project template. |
| [`CHANGELOG.md`](CHANGELOG.md) | v1 → v3.0.0 history, including each version's promotion evidence. |

## 🔗 How it fits with prototyping-ui-directions

[`prototyping-ui-directions`](https://github.com/SensLiao/prototyping-ui-directions) is the upstream counterpart: it discovers the design direction from a fuzzy idea and a few references. `anchor-prototype-wave` then takes the chosen direction as its locked anchor and mass-produces the high-fidelity pages from it.

## 🖥 Compatibility

| Component | Support |
| --- | --- |
| Skill host | Claude Code (skills directory install; explicit invocation only) |
| Scripts | Python 3.10+, standard library only, cross-platform |
| Cross-model review | Codex CLI via the separately installed `codex-dispatch` skill |
| Generated pages | Self-contained HTML, no build step |

## 📊 Project status

The skill is **stable and pilot-ratified** — the current v3.0.0 collapsed the earlier flag/mode surface into a purely conversational interface while keeping all v2.1 verification mechanics (old flag-style prompts are still understood; the flags are simply ignored). The deterministic validator, gates, scoring, retry loop, and cross-review trigger matrix are the ratified core. Two honest caveats. The boundary-compliance gate is enforced by the orchestrator rather than the standalone validator. And while [`examples/2026-08-31-signal-anchor/`](examples/2026-08-31-signal-anchor/) now ships a real filled gallery plus three real audits, it is **not a full wave** — no LLM grading pass, no retry loop, no cross-review; a complete wave's outputs still live in the projects that run it.

## 📄 License

Released under the MIT License — see [`LICENSE`](LICENSE).

<p align="center"><sub>Built by <a href="https://github.com/SensLiao">Ruixuan "Sens" Liao</a> · USYD Advanced Computing (Honours)</sub></p>
