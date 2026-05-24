# Worked Example — 2026-05-12 → 2026-05-13 Track B v2 Anchor Prototype Wave

> The canonical 2-day execution that produced this skill. Compressed summary
> for skill reference. Full source: `vault/wiki/log.md` 2026-05-12 +
> 2026-05-13 entries.

## Context

**Project**: Agent Console (multi-persona AI agent collaboration product)
**Track**: B (UI/UX Future Lab — separate from Track A production)
**Anchor**: C5 Base v2 (chassis: Inter / radius 8px / hairline `1px solid
rgba(0,0,0,0.06)` / single mono accent `#171717` / no glass / no aurora)
**Wave goal**: produce hi-fi prototype gallery covering all 10 surfaces of
the production app, applying the C5 Base + 5 mode application layer

## Stage 0 — Foundation (sequential, main thread, ~3 hours wall-clock)

Produced 7 anchor docs in order:

1. `uiux-quality-gate-v1` — 12-gate self-audit
2. `ui-lab-boundaries` — 9 hard rules
3. `reference-package-standard-v1` — Lane A output contract
4. `skill-routing-matrix-v1` — Primary/Secondary per stage
5. `track-b-roadmap-v1` — Stage × Surface × Gate visual map
6. `2026-05-12-c5-base-v2-product-anchor` — the anchor itself
7. `2026-05-12-v3-foundation-strategic-amendment` — v3 path preview (the
   "V2 as V3 precision baseline" pattern)

INGEST 三连 observed: each doc atomic, index.md updated 6 times, log.md got
batched entries. hot.md untouched (Track B doesn't grab ⚡ slot).

## Stage 1 — Parallel Research (4 lanes, ~6 hours wall-clock)

| Lane | Subagent count | Output |
|---|---|---|
| A — Reference Intel | 11 (5 Tier A + 5 Tier B + 1 Tier C aggregate) | `references/<tier>/<vendor>/` per-vendor packages |
| B — Visual Direction Shootout | 5 (C5-01..05 variant writeups) | per-mode writeup in `visual-language/` |
| C — Surface Architecture | 1 | typology + persona × surface × intent matrix |
| D — Interaction System | 4 | living-canvas / layout-engine / semantic-zoom / motion-governor specs |

## Stage 2.0 — Element Contract Index (frozen, main thread)

Single doc: `element-contract-index-v1.md`. ~20 elements × 6-7 states × token
cites. Status: draft / research-only. **Frozen before Stage 2.1 / 3 spawn**
to prevent the floating-spec anti-pattern (per Failure Mode F-1).

## Wave 1 — Phase 1 (2026-05-12, 10 parallel subagent, ~3 hours)

User directive: "保证功能对齐，UI/UX 必须对齐 MVP 之前需要完成的功能;
按当前 anchor prototype 完成下面任务; 自主执行调用计划文档 skill + 配合
codex + agent teams + subagent; 过程不过问，最后输出 index 可视化结果".

**Wave 1 fan-out**:

| # | Type | Slug | Model | Lines | Self-grade |
|---|---|---|---|---|---|
| 1 | Element | `elements/01-atoms-buttons` | sonnet | 1576 | 9.5/9.0/9.0/6/6 |
| 2 | Element | `elements/02-surface-card-drawer` | sonnet | 1790 | 9.0/9.0/9.0/6/6 |
| 3 | Element | `elements/03-forms` | sonnet | 2144 | 9.5/8.0/9.0/6/6 |
| 4 | Element | `elements/04-nav-structural` | sonnet | 1674 | 9.0/9.0/7.0/8/6 |
| 5 | Surface mature | `p0-myworkfocus` | sonnet | 1763 | 9.0/8.5/8.0/6/6 |
| 6 | Surface mature | `p1-caselibrary` | sonnet | 2169 | 9.0/8.0/9.0/6/7 |
| 7 | Surface CREATIVE | `p2-caseworkspace` | **opus** | 3225 | 9.0/8.5/9.0/**8**/**9** |
| 8 | Surface mature | `p6-portfolio-cockpit` | sonnet | 1900 | 9.0/9.0/8.0/6/6 |
| 9 | Surface mature | `p7-module-operations` | sonnet | 2534 | 9.5/9.0/8.0/7/7 |
| 10 | Surface CREATIVE | `p8-review-queue` | **opus** | 3006 | 9.0/9.0/9.0/**10**/**9** |

**Total**: 21,781 lines HTML + 1,850 lines writeup. Avg self-grade 8.6.

**Shared context contract**: `ui-lab/v2-anchor-prototypes/_context.md`
(one file, read by all 10 subagents — saved rewriting the chassis contract
in 10 prompts).

**Master gallery**: `ui-lab/v2-anchor-prototypes/index.html` built by main
thread using the chassis itself (Inter / dot-grid backdrop / hairline /
mono accent).

## Strategic Amendment (2026-05-12 evening, main thread)

User directive: "请记录进去一点，就是当前的这个方向 V2 UI/UX，可以给到
后期 V3 我们使用更高级定制化 UI/UX 的 claude design+gpt-image2+tapnow+...
其他技术的一个技术调研和留下改进的一个基石...站在了巨人的肩膀上，去触摸
宇宙新河".

Produced: `2026-05-12-v3-foundation-strategic-amendment.md`

Key invariants added:
- V3 always depends on mature V2 baseline (not zero-imagination)
- V2 must reserve 7 hooks for V3 (token naming / element anatomy / motion
  budget / asset pipeline / persona×lens / metrics / component slot)
- v3 anchor doesn't start until v2 fully merged + product reaches mature
  business state

## Wave 2 — Phase 2 (2026-05-13, 5 parallel subagent + 1 Codex, ~2 hours)

User directive: "A: 选 prime 吧，然后开始后面的任务".

**c5-prime elevation** (main thread, sequential): elevated `c5-prime-evidence-bento`
from superseded → PREMIUM 6th mode for audit / governance / client-visible.

**Wave 2 fan-out**:

| # | Type | Slug | Model | Lines | Self-grade |
|---|---|---|---|---|---|
| 1 | ★ MARQUEE | `p-prime-evidence-audit` | **opus** | 2790 | 9.5/9.5/9.5/10/9.5 (composite 9.4) |
| 2 | Surface mature | `p3-admin-console` | sonnet | 2979 | 9.0/8.0/9.0/7/8 |
| 3 | Surface CREATIVE | `p4-client-portal` | sonnet | 2631 | 9.2/9.5/9.0/7/8.5 |
| 4 | Surface mature | `p5-login` | sonnet | 1326 | 9.6/9.5/9.0/7/5 |
| 5 | Surface mature | `p9-root-canvas` | sonnet | 2447 | 9.5/9.0/9.0/8/8.5 |
| 6 | Cross-AI review | `2026-05-13-codex-cross-review-6-surfaces` | **Codex GPT-5.4** | 847 (writeup) | — outside review |

**Total**: 12,173 lines HTML + ~1,900 lines writeup + 847 lines Codex review.

**Codex invocation**:
```bash
codex exec --sandbox workspace-write --skip-git-repo-check \
  --cd "<project>" "<prompt-from-codex-review-prompt.md>"
```

Codex review produced per-surface concrete improvements with specific DOM
patterns + CSS selectors, frontier product references (Linear / Notion /
Cursor / Vercel / GitHub Projects / Plane / Stripe / Raycast), and top 3
priority recommendations across all 6 surfaces.

## Wave totals

- **15 prototypes** (4 element + 10 surface + 1 marquee)
- **34,991 lines HTML** (self-contained, 0 runtime deps except Google Fonts
  @import for Inter + JetBrains Mono)
- **6 c5 modes** (5 standard + 1 PREMIUM)
- **11 vault writeups**
- **1 Codex cross-review** (847 lines)
- **Avg self-grade 9.0/10** (Wave 2 lifted from Wave 1's 8.6 via marquee +
  Codex feedback applied to amendments)
- **0 production code touched**

## Key learnings (applied to this skill)

1. **Foundation must precede wave** — Stage 2.0 freeze BEFORE 2.1 spawn;
   anchor BEFORE Stage 3 surface spawn. P0 surface from earlier (pre-Stage
   2.0) floated; this wave's surfaces all cite Stage 2.0 element index.
2. **Shared context contract pays for itself** — `_context.md` reused 15
   times. Saved ~3000 tokens × 15 = ~45k tokens of redundant prompt context.
3. **Master gallery uses chassis** — proves the chassis at ensemble scale.
   When the gallery itself looks coherent, the chassis is real.
4. **Opus for creative, sonnet for mature** — P2 + P8 (creative opus
   subagent) hit innovation 8-9; mature sonnet subagent stayed at 6-7
   (target range correctly). Model routing matters.
5. **Codex orthogonal, not parallel** — fire Codex AFTER Claude wave; don't
   dual-source the same surface. Different lenses = different value.
   Wave 1 tried 0 Codex; Wave 2 added Codex as orthogonal pass.
6. **Date-slug everything** — vN naming chain died after the
   `2026-05-11-visual-language-v2-retirement` lesson. All Wave 1 + 2 outputs
   use `2026-05-12-*` or `2026-05-13-*` date prefixes.
7. **PREMIUM is a constraint, not a freebie** — c5-prime only applies to
   audit / governance / client-visible / marquee. Wave 2 used it on 1
   marquee (P-Prime) + 1 client portal (P4). Default surfaces stayed on
   standard modes.

## Wall-clock summary

| Stage | Wall-clock | Sequential equivalent | Speedup |
|---|---|---|---|
| Stage 0 Foundation | 3 h | 3 h | 1× |
| Stage 1 Parallel Research | 6 h | 24 h | 4× |
| Stage 2.0 freeze | 1 h | 1 h | 1× |
| Wave 1 (10 parallel) | 3 h | 30 h | 10× |
| Wave 2 (5 parallel + Codex) | 2 h | 12 h | 6× |
| Strategic amendment | 1 h | 1 h | 1× |
| **Total** | **~16 h over 2 days** | **~70 h** | **~4.4× overall** |

## What this skill productizes from this run

| Pattern | File in skill |
|---|---|
| Anchor doc structure | `ASSETS/anchor-doc-template.md` |
| Shared `_context.md` contract | `ASSETS/shared-context-template.md` |
| Per-surface subagent prompt | `ASSETS/surface-prompt-template.md` |
| Per-element subagent prompt | `ASSETS/element-prompt-template.md` |
| Per-prototype vault writeup | `ASSETS/writeup-template.md` |
| Master gallery aggregation | `ASSETS/master-gallery-template.html` |
| Codex CLI cross-review | `ASSETS/codex-review-prompt.md` |
| 12-gate self-audit | `ASSETS/quality-gate-checklist.md` |
| INGEST 三连 (log.md + index.md) | `ASSETS/vault-sync-template.md` |
| Failure modes + guardrails | `SKILL.md §11` |
| 5-Stage pipeline + multi-agent orchestration | `SKILL.md §2-3` |
| Upstream / downstream connection | `SKILL.md §10` |

This skill is THE 2-day execution distilled into a reusable wave pattern.
Future anchors (v3 when it lands, or a separate program's anchor entirely)
can run this same pipeline by substituting their own chassis values into
the templates.
