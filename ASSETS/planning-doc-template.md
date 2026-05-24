# Wave Planning Doc Template

> **Purpose**: a fillable skeleton for the wave plan that the orchestrator
> (main thread) MUST produce BEFORE spawning any subagent. Plan-then-execute
> is non-negotiable for this skill. See SKILL.md §3-tris for the discipline.
>
> **Customize**: replace every `{PLACEHOLDER}` token below with your project's
> concrete value. Verify with
> `grep -r '{[A-Z_-]\+}' <your-filled-plan.md>` before declaring the plan
> ratified.

---

## §A — Blank skeleton (paste, fill, ratify)

Save the filled version as
`{research-vault-path}plans/{DATE}-{wave-slug}-plan.md`.

```yaml
---
slug: {DATE}-{wave-slug}-plan
title: {WAVE_NAME} — Wave Plan
type: plan
status: draft   # change to "ratified" after human approval; "concluded" after wave end
confidence: medium
created: {DATE}
updated: {DATE}
track: {RESEARCH_TRACK_LETTER}
related:
  - "[[{ANCHOR_DOC_SLUG}]]"
  - "[[{ELEMENT_INDEX_SLUG}]]"
  - "[[{ROADMAP_SLUG}]]"
sources:
  - "user directive {DATE} — '{ORIGINAL_USER_QUOTE_OR_TRIGGER_SUMMARY}'"
tags: [design-research, plan, {WAVE_TAG}]
domain: orchestration
---
```

### §1 — Wave goal

One paragraph. What does this wave produce? Why now? What does it NOT
produce?

```
Example:
"Wave 2 of {chassis-name} anchor application. Produce hi-fi mocks for the
remaining {N} surfaces ({surface-slug-list}), plus 1 marquee surface
using the {mode-prime} PREMIUM tier. Anchor `{chassis-name}` is
ratified; element-contract-index v1 is frozen. This wave does NOT
produce Stage 4 merge packages — that's a separate plan after Gate 12."
```

### §2 — Inputs

Where the wave reads from. Cite paths absolutely.

| Input | Path | Read-only? |
|---|---|---|
| Anchor doc | `{ANCHOR_DOC_PATH}` | yes |
| Chassis writeup | `{CHASSIS_WRITEUP_PATH}` | yes |
| Element contract index | `{ELEMENT_INDEX_PATH}` | yes |
| Shared context | `{prototype-output-dir}_context.md` | written by main thread; read-only for subagents |
| Reference repos | `{reference-repo-root}{ref-list}` | yes |
| Production source (for MVP alignment) | `{production-source-glob}` matching `{surface-slug-list}` | yes |
| Project rules doc | `{rules-doc}` | yes (never write) |

### §3 — Deliverables

Itemized list. Each item has a path; missing paths is a plan failure.

```
- 1 _context.md      (path: {prototype-output-dir}_context.md)
- N surface HTMLs    (path: {prototype-output-dir}{surface-N-slug}/index.html)
- N surface writeups (path: {research-vault-path}design-research/{DATE}-{surface-N-slug}-writeup.md)
- 1 master gallery   (path: {prototype-output-dir}index.html)
- 1 cross-AI review  (path: {research-vault-path}design-research/{DATE}-codex-cross-review-{N}-surfaces.md)
```

### §4 — Agent team

Table format. Each row is one agent. **Don't bundle multiple agents per row.**

| # | Agent name | Role | Model | Tools | Scope | Output | Validation | Stop condition |
|---|---|---|---|---|---|---|---|---|
| 1 | shared-context-author | Write _context.md from anchor + chassis | main thread (orchestrator) | Read, Write, Edit | none beyond `_context.md` | `{prototype-output-dir}_context.md` | grep check: no `{PLACEHOLDER}` remaining | file written, byte count > N |
| 2 | surface-{slug-1} | Hi-fi prototype for surface 1 | sonnet | Read, Write, Edit, Grep, Glob | mature, mode={MODE_X} | `{prototype-output-dir}{slug-1}/index.html` + writeup | Gate 1-11 self-audit PASS | Gate Report posted to writeup §6 |
| 3 | surface-{slug-2} | Hi-fi prototype for surface 2 | sonnet | Read, Write, Edit, Grep, Glob | mature, mode={MODE_Y} | (similar) | (similar) | (similar) |
| 4 | surface-{slug-3} | Hi-fi prototype for surface 3 (creative) | **opus** | Read, Write, Edit, Grep, Glob | creative, mode={MODE_Z} | (similar) | Gate 1-11 PASS, innovation ≥8 | (similar) |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| K | master-gallery | Aggregate all writeups into gallery HTML | main thread | Read, Write, Edit | aggregator only | `{prototype-output-dir}index.html` | All N cards present + chassis applied | gallery loads in browser |
| K+1 | codex-review (external CLI) | Outside red-team review | external (Codex / GPT-5) | (external sandbox) | post-wave, read-only of all surfaces | `{research-vault-path}design-research/{DATE}-codex-cross-review.md` | non-restate of Claude self-grade | writeup posted |

### §5 — Boundary contracts

Cite the project rules doc. Each agent gets:

```
ALL subagents in this wave may NEVER write to:
  - {production-source-glob} (production frontend)
  - backend production source equivalents
  - {global-token-file}
  - tailwind.config.* / vite.config.* (or your project's build config)
  - root package.json
  - {rules-doc} (and any ADR)
  - {reference-repo-root}* (study material only)
  - {raw-immutable-root}* (immutable archive)
  - other subagents' output directories
  - the chassis HTML reference

The orchestrator (main thread) may write:
  - {prototype-output-dir}_context.md (once, before wave spawn)
  - {prototype-output-dir}index.html (master gallery, after wave aggregation)
  - {research-vault-path}index.md (batched index update at wave end)
  - {research-vault-path}log.md (batched log update at wave end)
```

### §6 — Sync points

When does the wave converge? Each sync is a checkpoint:

1. **After `_context.md` written**: main thread verifies grep returns 0
   `{PLACEHOLDER}` tokens; then spawns wave.
2. **Per subagent — Gate 11 self-audit**: subagent must post Gate Report
   to its writeup §6 before declaring done.
3. **Wave aggregation**: main thread waits for all N subagents to return;
   reads each writeup's frontmatter `self_grade` + Gate Report; assembles
   master gallery.
4. **Cross-AI review fire**: AFTER aggregation; external CLI reads all
   HTMLs + writeups; produces orthogonal critique.
5. **Gate 12 sign-off**: HUMAN ONLY. Orchestrator hands off the master
   gallery URL + Gate Report summary; STOPS.

### §7 — Risk register

Known risks BEFORE wave start. Each gets a code + mitigation.

| Code | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R-1 | Subagent count > 10 → hits concurrency ceiling | low / medium / high | low / medium / high | Split into 2 waves of ≤10 |
| R-2 | Creative subagent (opus) over-budget on HTML lines | low / medium / high | low / medium / high | Cap at {LINE_CEILING} lines |
| R-3 | Chassis ambiguity in `_context.md` causes drift across subagents | low / medium / high | low / medium / high | Grep `_context.md` for `{PLACEHOLDER}` before spawn |
| R-4 | One subagent fails → master gallery missing a card | low / medium / high | low / medium / high | Diagnose prompt, re-spawn JUST that subagent (don't re-run wave) |
| R-5 | Cross-AI review flags chassis-level issue | medium | medium | Defer fix to a strategic amendment + next wave; don't block Gate 12 on chassis if surfaces are individually approvable |
| R-6 | Subagent writes outside output path (boundary violation) | low | high | Gate 10 BLOCK; revert subagent output; re-spawn with stricter prompt |
| R-7 | Plan ratified, then mid-wave scope creep | medium | high | End wave; write new plan; start new wave |

### §8 — Approval checkpoint

```
This plan is in `status: draft`. Awaiting human approval to:
  - Ratify (change status to "ratified")
  - Spawn the N agents listed in §4

Human reviewer should confirm:
  - [ ] Wave goal in §1 matches the original intent
  - [ ] Agent team in §4 covers all deliverables in §3
  - [ ] No agent crosses any boundary in §5
  - [ ] Risk register §7 has at least 1 mitigation per HIGH-impact row
  - [ ] Subagent count ≤ 10

On approval, orchestrator changes status to "ratified" and spawns.
On rejection, orchestrator iterates on the plan.
```

---

## §B — Example: Project X 5-surface wave (filled-in)

This is a fully-filled hypothetical example. Project X is a fictional
analytics dashboard with 5 surfaces.

```yaml
---
slug: 2027-03-14-projectx-nova-wave-1-plan
title: Project X Nova Wave 1 — 5-Surface Hi-Fi Wave Plan
type: plan
status: draft
confidence: medium
created: 2027-03-14
updated: 2027-03-14
track: B
related:
  - "[[2027-03-10-projectx-nova-v1-anchor]]"
  - "[[2027-03-12-projectx-element-contract-index-v1]]"
  - "[[2027-03-08-projectx-track-b-roadmap]]"
sources:
  - "user directive 2027-03-14 — 'spawn the 5-surface wave on Nova v1'"
tags: [design-research, plan, projectx, nova-wave-1]
domain: orchestration
---
```

### §1 — Wave goal

Produce hi-fi prototype mocks for the 5 Project X surfaces (Dashboard,
Project Detail, Settings, Login, Evidence Audit). Apply the ratified Nova
v1 chassis (Inter / radius 8px / hairline `1px solid rgba(0,0,0,0.06)` /
mono accent `#0F172A`) and 4 mode application layers (overview / detail
/ preferences / auth) + 1 PREMIUM mode (evidence-bento) on the marquee
Evidence Audit surface. Wave does NOT produce Stage 4 merge packages —
separate plan after Gate 12.

### §2 — Inputs

| Input | Path | Read-only? |
|---|---|---|
| Anchor doc | `docs/research/2027-03-10-projectx-nova-v1-anchor.md` | yes |
| Chassis writeup | `docs/research/2027-03-09-projectx-nova-chassis-writeup.md` | yes |
| Element contract index | `docs/research/2027-03-12-projectx-element-contract-index-v1.md` | yes |
| Shared context | `prototypes/nova-wave-1/_context.md` | written by main thread; read-only for subagents |
| Reference repos | `_reference/{linear,plane,n8n,shadcn-ui,vercel-clone}/` | yes |
| Production source | `apps/web/src/pages/{Dashboard,Project,Settings,Login,EvidenceAudit}.tsx` | yes |
| Project rules doc | `.claude/CLAUDE.md` | yes (never write) |

### §3 — Deliverables

- 1 _context.md      → `prototypes/nova-wave-1/_context.md`
- 5 surface HTMLs    → `prototypes/nova-wave-1/{dashboard,project-detail,settings,login,evidence-audit}/index.html`
- 5 surface writeups → `docs/research/nova-wave-1/2027-03-14-{slug}-writeup.md`
- 1 master gallery   → `prototypes/nova-wave-1/index.html`
- 1 codex review     → `docs/research/nova-wave-1/2027-03-15-codex-cross-review-5-surfaces.md`

### §4 — Agent team

| # | Agent name | Role | Model | Tools | Scope | Output | Validation | Stop condition |
|---|---|---|---|---|---|---|---|---|
| 1 | shared-context-author | Write _context.md from Nova v1 anchor | main thread | Read, Write, Edit | only _context.md | `prototypes/nova-wave-1/_context.md` | grep returns 0 `{PLACEHOLDER}` | file written |
| 2 | surface-dashboard | Hi-fi for Dashboard | sonnet | Read, Write, Edit, Grep, Glob | mature, mode=overview | HTML + writeup | Gate 1-11 PASS | Gate Report posted |
| 3 | surface-project-detail | Hi-fi for Project Detail | sonnet | (same) | mature, mode=detail | HTML + writeup | (same) | (same) |
| 4 | surface-settings | Hi-fi for Settings | sonnet | (same) | mature, mode=preferences | HTML + writeup | (same) | (same) |
| 5 | surface-login | Hi-fi for Login | sonnet | (same) | mature, mode=auth | HTML + writeup | (same) | (same) |
| 6 | surface-evidence-audit | Hi-fi for Evidence Audit (MARQUEE) | **opus** | (same) | creative+marquee, mode=evidence-bento | HTML + writeup | Gate 1-11 PASS, innovation ≥9, Laws of UX ≥8 | Gate Report + 3 novel patterns documented |
| 7 | master-gallery | Aggregate 5 writeups → gallery HTML | main thread | Read, Write, Edit | aggregator only | `prototypes/nova-wave-1/index.html` | 5 cards + chassis applied + version stack tile strip | gallery loads in browser |
| 8 | codex-review | Cross-AI outside critique | external (Codex GPT-5) | external sandbox | post-wave read-only | `docs/research/nova-wave-1/2027-03-15-codex-cross-review-5-surfaces.md` | NOT restate Claude self-grade; cite ≥5 frontier products | writeup posted |

**Total**: 8 agents (1 orchestrator + 5 surface subagents + 1 aggregator
+ 1 cross-AI). Within safe 10-concurrent ceiling.

### §5 — Boundary contracts

ALL subagents in this wave may NEVER write to:
- `apps/web/src/*` / `apps/api/src/*` (production)
- `apps/web/src/styles/globals.css`
- `tailwind.config.*` / `vite.config.*`
- root `package.json`
- `.claude/CLAUDE.md` (and any ADR)
- `_reference/*`
- `archives/*`
- other subagents' output directories
- the Nova chassis HTML reference

The orchestrator (main thread) may write:
- `prototypes/nova-wave-1/_context.md` (once, before spawn)
- `prototypes/nova-wave-1/index.html` (master gallery, after aggregation)
- `docs/research/index.md` (batched at wave end)
- `docs/research/log.md` (batched at wave end)

### §6 — Sync points

1. After `_context.md` written: orchestrator runs `grep` for placeholders;
   then spawns Wave (agents 2-6 launched simultaneously).
2. Per subagent — Gate 11 self-audit: each subagent posts Gate Report to
   writeup §6 before declaring done.
3. Wave aggregation: orchestrator awaits all 5 subagents; reads writeup
   frontmatter; runs agent #7.
4. Cross-AI review fire: AFTER aggregation; agent #8 reads all 5 HTMLs +
   writeups; produces orthogonal critique.
5. Gate 12 sign-off: HUMAN ONLY. Orchestrator hands off the master
   gallery URL + Gate Report summary; STOPS.

### §7 — Risk register

| Code | Risk | P | I | Mitigation |
|---|---|---|---|---|
| R-1 | Subagent count = 5 < 10 ceiling | low | low | No split needed |
| R-2 | Evidence-audit (opus marquee) over-budget on HTML lines | medium | medium | Cap at 3500 lines HTML |
| R-3 | Chassis ambiguity in `_context.md` | low | high | grep `_context.md` for `{PLACEHOLDER}` before spawn |
| R-4 | One mature surface fails | medium | low | Re-spawn JUST that one; gallery survives 4/5 |
| R-5 | Evidence-audit marquee fails | low | HIGH | Re-spawn with stricter prompt; gallery has no centerpiece without it; consider blocking Gate 12 |
| R-6 | Cross-AI review flags chassis issue | medium | medium | Defer fix to strategic amendment + Wave 2; surfaces individually approvable |
| R-7 | Plan creep (user adds surface mid-wave) | low | high | Refuse; end wave; new plan |

### §8 — Approval checkpoint

```
This plan is in `status: draft`. Awaiting human approval to spawn agents
2-8 per §4.

Reviewer checklist:
  - [ ] Wave goal in §1 matches original intent
  - [ ] 5 surfaces in §4 cover the 5 production pages in §2
  - [ ] No agent crosses boundary in §5
  - [ ] R-5 (marquee failure) has explicit mitigation
  - [ ] Subagent count = 5, well below 10 ceiling

On approval: orchestrator changes this doc's status to "ratified",
spawns Wave.
On rejection: orchestrator iterates.
```

---

## §C — Tips for filling this template

1. **Don't skip §4 agent specialization** — sonnet vs opus matters; if you
   pick wrong, the wave hits ceiling at innovation 6-7.
2. **§5 boundary contracts MUST cite the project rules doc verbatim** —
   paraphrasing here is the source of Gate 10 BLOCK fails.
3. **§7 risk register is not optional** — at least 1 mitigation per
   HIGH-impact row; otherwise you're flying blind on partial failure.
4. **§3 deliverables paths use the same root** — all 5 surfaces share
   `{prototype-output-dir}<wave-slug>/` so the master gallery aggregator
   can glob them.
5. **One plan per wave** — if you have 2 waves (Wave 1 + Wave 2), write 2
   plans. Don't bundle.
6. **Plan revisions are git-tracked** — change `updated:` field on each
   edit; keep `status` accurate (draft → ratified → concluded).
