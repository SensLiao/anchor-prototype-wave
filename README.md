# anchor-prototype-wave

A [Claude Code](https://docs.claude.com/claude-code) skill that turns a locked
visual anchor + a page list into a parallel-subagent wave of hi-fi HTML
prototype surfaces, each scored by deterministic gates + an LLM grader +
optional cross-AI review.

Public/reporting name: **Track B Visual Research Run**. Path/skill name stays
`anchor-prototype-wave` for prompt and routing compatibility.

---

## What it does

You give the skill three things:

1. **A visual anchor** — typography, radius scale, hairline, accent color,
   banned tokens, status/surface/text colors, spacing scale, micro shadow.
2. **A page list** — slug, title, route, group, status hint, risk hint, and
   optional content brief for each surface.
3. **An output directory** — defaults to
   `ui-lab/<date>-<anchor-slug>-anchor-prototypes/`.

The skill then runs end-to-end:

- Spawns up to 10 parallel surface subagents (mature → Sonnet,
  creative/marquee → Opus) under strict write-scope (`<slug>/index.html` only)
- Runs deterministic validators (scaffold leak, decorative gradient, pill
  mono drift, morphology, forbidden write path, accessibility minimum,
  schema validity)
- Runs an LLM grader filling 6 soft-score dimensions
- Computes maturity-aware composite + verdict
  (`PASS_9PLUS | FIX_NEEDED | REDO | ESCALATE_HUMAN`)
- Triggers cross-AI review (Codex via `codex-dispatch`) on REDO / FIX_NEEDED
  / known-risk surfaces, plus 15% sampling on PASS_9PLUS
- Loops fix-on-fail up to 3 retries per failing surface, then escalates
- Aggregates a master gallery `index.html` mirroring the v2 layout
- Writes manifest, closeout, and updates `references/failure-patterns.md`
  with any new regression cases

Full spec: see [SKILL.md](SKILL.md).
Version history: see [CHANGELOG.md](CHANGELOG.md).

---

## Install

This skill orchestrates other Claude Code skills (it does **not** bundle their
source). Required + recommended dependencies are documented in
[references/skills-dependencies.md](references/skills-dependencies.md).

### Option A — copy into a project's local `.claude/skills/`

```bash
git clone https://github.com/SensLiao/anchor-prototype-wave.git \
  .claude/skills/anchor-prototype-wave
```

### Option B — install globally for all your Claude Code sessions

```bash
# Linux / macOS
git clone https://github.com/SensLiao/anchor-prototype-wave.git \
  ~/.claude/skills/anchor-prototype-wave
```

```powershell
# Windows PowerShell
git clone https://github.com/SensLiao/anchor-prototype-wave.git `
  $HOME\.claude\skills\anchor-prototype-wave
```

### Required companion skills

| Skill | Why |
|---|---|
| `codex-dispatch` | Stage 9 cross-AI review (Codex CLI invocation) |

### Strongly recommended companion skills

| Skill | Why |
|---|---|
| `ux-principles` | Stage 0/5/7 — anchor laws, tactical numbers, NN10 + Built-for-Mars audit |
| `taste-skill` | Anti-AI-slop tokens + single-page craft rules across the pipeline |

### Optional companion skills

`prototyping-ui-directions`, `ai-regression-testing`,
`luxury-editorial-site-builder`, `grill-with-docs` —
see [references/skills-dependencies.md](references/skills-dependencies.md) for
when each one improves which stage.

---

## Usage

In a Claude Code session with this skill installed:

```
> Run anchor-prototype-wave. Anchor: <paste anchor doc>.
> Pages: <list of 5-15 surfaces with slug/title/route/intent/group/status/risk>.
> Output dir: ui-lab/2026-05-24-my-anchor-prototypes/
```

The skill will:
1. Validate inputs (ask if anything is missing)
2. Run the full pipeline silently (no per-stage checkpoints)
3. Report back: surface count, PASS / FIX / REDO / ESCALATE breakdown,
   master gallery URL, and any `ESCALATE_HUMAN` surfaces for you to triage

The only times it stops to ask:

- Inputs are incomplete / ambiguous
- A surface fails 3 fix retries (`ESCALATE_HUMAN`)
- You ask it to modify itself (writes to `.claude/skills/anchor-prototype-wave/**`)

---

## Layout

```
SKILL.md                          ← full spec (read this)
CHANGELOG.md                      ← version history (v3.0.0 collapsed v2.1's 4 modes)
README.md                         ← this file
LICENSE                           ← MIT
references/
  master-gallery-structure.md     ← Stage 11 locked layout
  skills-dependencies.md          ← per-stage external skill consumption
  surface-taxonomy.md             ← 12 morphology types
  gates.md                        ← 5 hard gates + 6 soft scores
  scoring-rubric.md               ← weights, floors, verdicts, maturity-aware
  failure-patterns.md             ← regression cases (expandable by closeout)
  model-policy.md                 ← env-var driven, no hardcoded models
  output-schema.md                ← JSON schemas + examples
scripts/
  validate_surface.py             ← deterministic checks, stdlib only
  score_audit_json.py             ← composite + maturity floor + verdict
ASSETS/
  anchor-doc-template.md
  codex-review-prompt.md
  element-prompt-template.md
  master-gallery-template.html
  orchestration-decision-matrix.md
  planning-doc-template.md
  quality-gate-checklist.md
  shared-context-template.md
  surface-prompt-template.md
  vault-sync-template.md
  writeup-template.md
examples/
  2026-05-12-track-b-v2-wave.md   ← pilot example
  template-blank-project.md       ← blank shape for a new project
```

---

## License

[MIT](LICENSE) © 2026 Ruixuan Liao

---

## Contributing

Issues and PRs welcome. For non-trivial changes, open an issue first so we
can align on scope.

When proposing a change to the pipeline (stages, gates, verdict rules,
parallelism), include:
- the failure pattern or use case driving the change,
- which `references/*.md` and/or `scripts/*.py` would be touched,
- a backwards-compatibility note for users on v3.x.
