<div align="right"><a href="README.zh-CN.md">简体中文</a></div>

<p align="center"><img src="docs/hero.png" alt="anchor-prototype-wave banner" width="100%"></p>

<p align="center"><b>Lock one visual anchor, fan out parallel high-fidelity pages, gate every one.</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skill-f472b6?style=flat-square" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/version-3.0.0-f472b6?style=flat-square" alt="Version 3.0.0">
  <img src="https://img.shields.io/badge/status-stable-f472b6?style=flat-square" alt="Status: stable">
  <img src="https://img.shields.io/badge/pipeline-14_stages-f472b6?style=flat-square" alt="14-stage pipeline">
  <img src="https://img.shields.io/badge/Python-3-3776ab?style=flat-square" alt="Python 3">
  <img src="https://img.shields.io/badge/License-MIT-2dd4bf?style=flat-square" alt="License: MIT">
</p>

## Overview

`anchor-prototype-wave` is a Claude Code skill that turns one locked visual anchor plus a list of pages into a full high-fidelity HTML prototype wave in a single run. It fans out parallel per-surface subagents, then gates each surface with deterministic validators, an LLM grader, and cross-model (Codex) review — retrying failures before aggregating a master gallery. It is built for designers and engineers who need many pages that stay faithful to one reference, without hand-checking each page for drift or leftover boilerplate.

**Key terms** (for a cold reader):

- **Surface** — one screen/page of the prototype.
- **Anchor** — the locked visual reference every surface must match.
- **Scaffold leak** — placeholder or boilerplate that slips into a finished page.

## ✨ Highlights

- **A 14-stage pipeline (Stage 0–13)** that carries a wave from locked anchor to aggregated gallery in one run.
- **Parallel surface subagents**, batched ≤10 and auto-splitting beyond that, so large page lists fan out without manual chunking.
- **A deterministic validator** with 9 checks that aggregate into 5 hard gates — the objective, non-LLM floor every surface must clear.
- **6 weighted soft dimensions** with maturity-aware score floors, resolving to four verdicts: `PASS_9PLUS`, `FIX_NEEDED`, `REDO`, `ESCALATE_HUMAN`.
- **A fix-on-fail loop** capped at 3 retries per surface, so failures are repaired in place rather than silently shipped.
- **Cross-model review** over all failures plus a 15% sample of passes, fully model-agnostic — the models are chosen by environment variables.
- **12 surface-morphology types and 10 enumerated anti-patterns** that anchor the grading vocabulary and catch scaffold leaks.

## 🏗 How it works

The wave runs as one deterministic flow:

1. **Lock the anchor** and expand the page list into individual surfaces.
2. **Fan out** parallel per-surface subagents (batched ≤10, auto-splitting beyond that).
3. **Validate** each surface against 9 deterministic checks aggregating into 5 hard gates.
4. **Grade** the 6 weighted soft dimensions with maturity-aware floors, producing one of four verdicts.
5. **Fix on fail**, retrying a surface up to 3 times.
6. **Cross-model review** every failure plus a 15% sample of passes.
7. **Aggregate** the surviving surfaces into a master gallery.

## 🔗 How it fits with prototyping-ui-directions

[`prototyping-ui-directions`](https://github.com/SensLiao/prototyping-ui-directions) is the upstream counterpart: it discovers the design direction from a fuzzy idea and a few references. `anchor-prototype-wave` then takes the chosen direction as its locked anchor and mass-produces the high-fidelity pages from it.

## 🧰 Tech stack

- **Skill spec** — a single Markdown skill definition.
- **Scripts** — two Python 3 standard-library scripts (about 640 lines, no third-party dependencies).
- **Companion skill** — `codex-dispatch` (for cross-model review).

## 🚀 Getting started

Install the skill either into a single project or globally for every project:

```bash
# Project-scoped install
git clone https://github.com/SensLiao/anchor-prototype-wave .claude/skills/anchor-prototype-wave

# …or global install
git clone https://github.com/SensLiao/anchor-prototype-wave ~/.claude/skills/anchor-prototype-wave
```

Then invoke it conversationally, giving it an anchor and a page list. The two Python scripts are also directly runnable — for example, to validate a single surface:

```bash
python validate_surface.py <surface-dir>
```

## 📌 Project status

**v3.0.0, stable.**

## 📄 License

Released under the MIT License — see [`LICENSE`](LICENSE).

<p align="center"><sub>Built by <a href="https://github.com/SensLiao">Ruixuan "Sens" Liao</a> · USYD Advanced Computing (Honours)</sub></p>
