# Anchor Wave v3.0.0 — Skills Dependencies (per-stage consumption map)

> When users clone this skill from GitHub, they need to know what OTHER
> Claude Code skills to install for the pipeline to actually produce
> high-quality output. This file is the full per-stage map.
>
> This skill itself does NOT copy other skills' source into its own
> directory. Each external skill stays standalone in the user's
> `~/.claude/skills/` or `<project>/.claude/skills/`. This file
> documents which stages of the anchor-prototype-wave pipeline reach
> into which other skill.

---

## §1 — Tier system

| Tier | Meaning | Install? |
|---|---|---|
| **Required** | Pipeline cannot complete the stage without it | Yes — install before first run |
| **Strongly recommended** | Pipeline runs, but output quality drops noticeably | Install for any serious use |
| **Recommended** | Improves one specific stage; optional for narrow waves | Install when the relevant stage applies to your wave |
| **Project-local optional** | Some projects benefit; many won't | Install only when you know you need it |

---

## §2 — Per-stage consumption

### Stage 0 — Anchor doc author

| External skill | Tier | How it's consumed |
|---|---|---|
| `grill-with-docs` | Recommended | If the user's anchor description uses ambiguous terms ("more editorial", "feel premium", "less heavy"), the anchor author invokes this skill to clarify into specific token values BEFORE committing chassis. |
| `ux-principles` (MODE A) | Strongly recommended | The anchor author asks: "for this chassis, which Laws of UX should we honor / explicitly avoid?" — produces a pre-design checklist that constrains every downstream surface. |
| `taste-skill` | Strongly recommended | Anti-AI-slop discipline at the anchor level — no decorative gradients, no glass blur, no uniform-padding flat layouts as defaults. |

### Stage 1 — Element index freeze

| External skill | Tier | How it's consumed |
|---|---|---|
| `taste-skill` | Strongly recommended | Element-level (atom + compound) craft rules: button states, focus rings, input affordances, drawer/dialog semantics. |
| `design-system` | Project-local optional | When the project already uses a token-driven design system (shadcn / radix / custom), this skill helps map anchor tokens to component primitives. |

### Stage 2 — Context author (`_context.md`)

| External skill | Tier | How it's consumed |
|---|---|---|
| `taste-skill` | Strongly recommended | The `_context.md` is the contract every subagent reads — anti-AI-slop language gets propagated through the whole wave. |

### Stage 5 — Surface subagent (mature)

| External skill | Tier | How it's consumed |
|---|---|---|
| `ux-principles` (MODE B) | Strongly recommended | Tactical numbers lookup: spacing rhythm, type scale, contrast ratios, button heights, line lengths. Mature surfaces win on numerical correctness. |
| `taste-skill` | Strongly recommended | Single-page craft + anti-AI-slop. The dominant skill for mature surface authoring. |

### Stage 5 — Surface subagent (creative)

| External skill | Tier | How it's consumed |
|---|---|---|
| `ux-principles` (MODE B) | Strongly recommended | Still need tactical numbers + Laws of UX hits. Creative ≠ ignore fundamentals. |
| `taste-skill` | Strongly recommended | Anti-AI-slop. Creative surfaces are MOST at risk of slop. |
| `prototyping-ui-directions` | Recommended | When the creative surface genuinely needs variant exploration (multiple distinct directions before pick-one), this skill's Stage 0-3 pipeline runs inside the subagent. Skip when the surface is "creative but anchored" (e.g. governance UI). |

### Stage 5 — Surface subagent (marquee)

| External skill | Tier | How it's consumed |
|---|---|---|
| `taste-skill` | Strongly recommended | Marquee = gallery centerpiece; craft level must be visible. |
| `prototyping-ui-directions` | Recommended | Marquee surfaces almost always benefit from upstream variant exploration before the marquee subagent commits. |
| `luxury-editorial-site-builder` | Project-local optional | Only when the marquee is a brand / marketing / landing-page style surface (100dvh hero, editorial composition). Not for product UI marquees. |

### Stage 7 — LLM grader (per surface)

| External skill | Tier | How it's consumed |
|---|---|---|
| `ux-principles` (MODE C) | Strongly recommended | The 6-dim soft scorer uses NN 10 heuristic + Laws of UX hit count + Built-for-Mars 5-lens audit as its rubric. Grading without MODE C = subjective vibes. |
| `ai-regression-testing` | Recommended | Catches "same model wrote it and reviewed it" blind spots. Improves grader independence vs the surface author. |

### Stage 9 — Cross-AI review

| External skill | Tier | How it's consumed |
|---|---|---|
| `codex-dispatch` | **Required** | Provides the external Codex CLI invocation pattern, env-var model routing (CODEX_REVIEW_MODEL / CODEX_LIGHT_MODEL / CODEX_FALLBACK_MODEL), sandbox flags, and fallback handling. Without this skill, Stage 9 has no way to invoke an external reviewer. |

### Stage 11 — Master gallery aggregation

| External skill | Tier | How it's consumed |
|---|---|---|
| `taste-skill` | Strongly recommended | The gallery is the user's FIRST visual impression of the wave. Craft polish matters more here than on any single surface. |
| `frontend-design` | Project-local optional | When the project uses this for downstream merge into production, the gallery aggregator pre-conforms to its component conventions. |

---

## §3 — Installation guide for downstream users

Choose ONE installation strategy. Don't mix.

### Option A — Copy from global to project

Best when you want each project to be self-contained.

```bash
mkdir -p .claude/skills
for skill in codex-dispatch ux-principles taste-skill prototyping-ui-directions \
             ai-regression-testing grill-with-docs luxury-editorial-site-builder; do
  cp -r ~/.claude/skills/$skill .claude/skills/
done
```

### Option B — Symlink from global

Best when you want a single source of truth.

```bash
mkdir -p .claude/skills
for skill in codex-dispatch ux-principles taste-skill prototyping-ui-directions \
             ai-regression-testing grill-with-docs luxury-editorial-site-builder; do
  ln -s ~/.claude/skills/$skill .claude/skills/$skill
done
```

(On Windows PowerShell: `New-Item -ItemType SymbolicLink -Path .claude/skills/<name> -Target ~/.claude/skills/<name>`)

### Option C — Skills marketplace (when available)

```bash
# Pseudocode — adapt to your Claude Code version
/plugin install codex-dispatch
/plugin install ux-principles
/plugin install taste-skill
/plugin install prototyping-ui-directions
/plugin install ai-regression-testing
/plugin install grill-with-docs
/plugin install luxury-editorial-site-builder
```

### Option D — Skip what you don't need

The pipeline will still run with only `codex-dispatch` installed
(Stage 9 needs it). Skipping the strongly-recommended skills will
produce noticeably weaker surfaces. Skipping the recommended skills is
fine if your wave doesn't touch the relevant stage (e.g. no creative
surfaces → skip `prototyping-ui-directions`).

---

## §4 — Minimum viable install

For the smallest install that still produces output the user can review:

```
codex-dispatch       # Required — Stage 9
ux-principles        # Strongly recommended — Stages 0, 5, 7
taste-skill          # Strongly recommended — Stages 0, 1, 2, 5, 11
```

3 skills, covers all critical quality pathways. The other 4 are
selectively added when a specific wave type calls for them.

---

## §5 — Where to find the skills

- **Anthropic-published**: `@anthropic-ai/skills` marketplace (when available)
- **Open-source community**: search GitHub for `claude-code-skill-{name}`
- **This project's pinning**: see the parent CLAUDE.md / project README
  for which version of each external skill has been validated against
  this version of anchor-prototype-wave

---

## §6 — Forward compatibility

When this skill (anchor-prototype-wave) is bumped to v3.x or v4.x, the
required dependency set may change. Always read the CHANGELOG.md for the
version you have installed and re-validate this dependency map against
your install.

Per-stage consumption can also expand as new sub-pipelines are added
(e.g. v3.1 might add a Stage 12 "automated screenshot capture" that
depends on a new playwright-driver skill). When stages are added, this
file is updated atomically with the CHANGELOG.md entry.
