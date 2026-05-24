# Changelog

## v3.0.0 — 2026-05-17 (conversational reset)

User-facing surface collapsed: 4 modes + 7 CLI flags removed; pipeline is
now one shot, conversational, no approval gates for routine generation.
All v2.1 internal verification mechanics preserved and run silently.

### Changed (user-facing surface only)

- **§0 Invocation Modes REMOVED.** v2.1's 4-mode menu (`AUDIT_ONLY` /
  `FIX_SELECTED` / `FULL_WAVE` / `SKILL_UPGRADE_PROPOSAL`) is gone.
  The pipeline runs end-to-end on a single trigger. The skill infers
  internal pipeline branches from the state of `<output-dir>/`
  (empty → generate; surfaces present → audit-then-fix; explicit
  "modify the skill itself" → meta path with explicit confirmation).
- **All CLI flags REMOVED.** No more `--mode=`, `--from=`,
  `--max-retries=`, `--quality-bar=`, `--surfaces=`, `--max-parallel=`,
  or `--edit-skill=true`. Defaults baked in; user describes intent in
  natural language ("跑慢点 quality 调严" → skill internalizes).
- **Plan-then-execute approval gate REMOVED for routine waves.** v2.1
  required a wave plan + human ratification before FULL_WAVE could
  spawn. v3.0 only stops in 3 cases (§3): inputs incomplete,
  ESCALATE_HUMAN after 3 retries, or user-requested self-edit.
- **Two-key skill-self-edit rule REPLACED.** v2.1 required
  `--mode=FULL_WAVE --edit-skill=true`. v3.0 triggers the same
  protection via §3 case 3 — plain language "modify this skill itself"
  + explicit user confirmation.

### Preserved (all v2.1 internal mechanics, now silent / automatic)

- Surface Contract preflight (was §2; now Stage 4)
- Deterministic Python validators (was §3; now Stage 6)
- Hard gates 0-4 with morphology sub_cause (was §4.1 + §4.3; now §7)
- Maturity-aware innovation floor (was §4.4; now §7)
- LLM grader filling soft scores (was §4.2; now Stage 7)
- Composite + verdict scorer (was §4.5; now Stage 8)
- Cross-AI review trigger matrix (was §6; now Stage 9 + §6)
- Fix-on-fail loop ≤3 retries with quoted evidence (was §5; now Stage 10)
- ESCALATE_HUMAN on retry exhaustion (was A5; now §3 + Stage 10)
- Closeout + regression-dataset update (was §8; now Stage 12)
- Machine-readable JSON output schema (was §7; preserved unchanged)
- Anti-patterns A1-A8 (preserved; A9 + A10 added for v3.0 surface)
- ASSETS/ + scripts/ + examples/ (all preserved unchanged)
- references/{gates,scoring-rubric,failure-patterns,model-policy,
  output-schema,surface-taxonomy}.md (all preserved unchanged)

### New

- **§1 Outputs explicit**: the skill produces `<output-dir>/index.html`
  master gallery + N `<slug>/index.html` surface pages + `audits/`
  artifacts. Documented as a tree.
- **§3 Stop-to-ask rules**: only 3 situations cause the pipeline to
  pause (incomplete inputs / ESCALATE_HUMAN / skill-self-edit). All
  other gates removed.
- **§5 Skills this skill depends on**: per-stage map of which other
  Claude Code skills the pipeline consumes. Required: `codex-dispatch`.
  Strongly recommended: `ux-principles`, `taste-skill`. Recommended:
  `prototyping-ui-directions`, `ai-regression-testing`,
  `luxury-editorial-site-builder`, `grill-with-docs`. Install guide
  with 4 options included.
- **references/master-gallery-structure.md** (NEW): locks the Stage 11
  master gallery output to mirror `ui-lab/v2-anchor-prototypes/index.html`
  exactly — token namespace, hero header, control panel, group/row
  markup, JS filter contract. References v2 source by line range.
- **references/skills-dependencies.md** (NEW): full per-stage external
  skill consumption map for downstream GitHub users.
- **A9 anti-pattern**: re-introducing CLI flags or asking the user to
  pick a mode. The pipeline is conversational.
- **A10 anti-pattern**: stopping for plan ratification on routine wave
  generation. Only stop per §3.

### Removed

- `references/mode-resolution.md` — no modes to resolve.

### Migration from v2.1

Existing v2.1 wave artifacts under `<output-dir>/audits/` remain valid;
v3.0 reads the same SurfaceContract / SurfaceAudit / CrossReview /
WaveManifest JSON shapes. The pilot artifacts at
`ui-lab/v2-anchor-prototypes/audits/2026-05-17-pilot/` and
`ui-lab/v2-anchor-prototypes/audits/2026-05-17-anchor-wave-skill-v2.1-spec/`
remain readable.

Old user prompts that used CLI flags will be re-interpreted: the skill
ignores `--mode=`, `--from=`, etc. and infers intent from the natural
language portion of the request. If a downstream wrapper depended on
flag parsing, update it to pass plain text.

---

## v2.1.0 — 2026-05-17 (pilot-ratified)

Promoted from `audits/2026-05-17-anchor-wave-skill-v2.1-spec/` after a
12-surface AUDIT_ONLY field test on `ui-lab/v2-anchor-prototypes/`.

### New

- **§0 Invocation Modes**: 4 modes (`AUDIT_ONLY` default / `FIX_SELECTED` /
  `FULL_WAVE` / `SKILL_UPGRADE_PROPOSAL`). Each has its own tool set and
  write allowlist; live skill edits require two-key (mode + `--edit-skill=true`).
- **§1 Two-tier write allowlist** with explicit HARD_DENY: never write to
  `workspace/src/**`, `backend/src/**`, `globals.css`, `tailwind.config.*`,
  `_reference/**`, `vault/raw/**`, infra, or migrations regardless of flags.
- **§2 Required preflight**: every surface must emit a SurfaceContract JSON
  (path, claimed_surface_type, production_source, MVP affordances,
  primary_object, write_scope, `surface_innovation_target`) before scoring.
- **§3 Deterministic Python validators** (`scripts/validate_surface.py` +
  `scripts/score_audit_json.py`, stdlib only): scaffold_leak,
  decorative_gradient, pill_mono_drift, stale_tab_label, surface_morphology
  (with sub_cause), accessibility_minimum, production_source_grounding,
  output_schema_validity. Replaces "LLM eyeballs the surface" with
  reproducible, evidence-cited JSON output.
- **§4.1 Hard gates** (5): `gate_0_intent_alignment`,
  `gate_1_production_source_grounding`, `gate_2_boundary_compliance`,
  `gate_3_no_scaffold_leak`, `gate_4_accessibility_minimum`. Hard gates
  short-circuit any soft score (BLOCK is never averaged away).
- **§4.4 Maturity-aware min-floor** (pilot finding): `INNOVATION_FLOOR_BY_MATURITY`
  = {`mature`: 5.0, `creative`: 7.5, `marquee`: 8.5}. Resolves v2.0
  contradiction where rubric said "mature 5-7 target" but global `MIN_FLOOR=8.5`
  made mature PASS impossible.
- **§4.3 Morphology sub-cause** (pilot finding from Codex cross-review):
  `gate_0_sub_cause` ∈ {`form_mismatch`, `missing_scrim`, `threshold_only`,
  `inner_widget_missing`}. `threshold_only` and `inner_widget_missing` →
  FIX_NEEDED (surgical patch); `form_mismatch` / `missing_scrim` → REDO.
  Closes the v2.0 over-strictness where z-index 50 < 1000 incorrectly forced
  a full rewrite.
- **§5 Fix-on-fail loop**: max 3 retries per surface; each retry quotes
  exact failing gate evidence; ESCALATE_HUMAN if retries exhaust (never
  auto-PASS).
- **§6 Triggered cross-AI review** (replaces v2.0 always-on): REDO/FIX_NEEDED
  required; PASS_9PLUS sample 15%; known-risk surfaces always.
- **§7 Machine-readable output contract**: SurfaceContract / SurfaceAudit /
  CrossReview / WaveManifest JSON schemas in `references/output-schema.md`;
  JSON is source of truth, .md is derived.
- **§8 Closeout / regression update**: every wave must update
  `failure-patterns.md` with new patterns; without §8, every wave is amnesiac.
- **`references/` directory** (7 files): gates.md, scoring-rubric.md,
  failure-patterns.md (6 regression cases), model-policy.md (env-var driven,
  no hardcoded model), output-schema.md, surface-taxonomy.md (12 morphology
  types), mode-resolution.md (trigger-phrase → mode mapping).
- **`scripts/` directory** (2 files): validate_surface.py, score_audit_json.py.
- **A8 anti-pattern**: treating all morphology mismatches as REDO; use
  `gate_0_sub_cause`.

### Changed

- v2.0 §5 prompt template → augmented by v2.1 §2 preflight contract
- v2.0 §6 cross-AI → revised by v2.1 §6 trigger matrix
- v2.0 §8 quality gates → revised by v2.1 §4 (hard/soft split + maturity
  floor + sub-cause)
- v2.0 §11 failure modes → augmented by v2.1 §9 anti-patterns

### Preserved (unchanged from v2.0)

- §0-§4 (placeholders, triggers, pipeline, anchor declaration)
- §3-tris wave plan (still mandatory before any spawn)
- §7 vault sync, §9 master gallery, §10 upstream/downstream
- All `ASSETS/` templates (still valid; not deprecated)
- All `examples/` (still valid)

### Pilot evidence (2026-05-17, 12 surfaces of ui-lab/v2-anchor-prototypes)

- 12/12 deterministic validator reproducibility (idempotent)
- 12/12 JSON schema validity
- 6/7 known-issue cohort verdicts match expectations (1 already fixed by
  2026-05-16 cleanup)
- 5/5 known-good cohort PASS-equivalent after 3 patches in this release
- 0/12 marketplace scaffold leaks (cleanup confirmed clean)
- 11/12 gate_3 BLOCK reclassified as global chassis debt (not per-surface)
- 2/4 Codex cross-reviews disputed Claude's REDO → FIX_NEEDED for z-index
  threshold cases (input → §4.3 fix)
- 0 boundary breaches across 4 parallel sonnet subagents

Pilot artifacts: `ui-lab/v2-anchor-prototypes/audits/2026-05-17-pilot/` +
`ui-lab/v2-anchor-prototypes/audits/2026-05-17-anchor-wave-skill-v2.1-spec/`.

---

## v2.0.0

- Rewrote orchestration guidance around reusable first-principles primitives:
  deliverable, surface, agent, team, wave, stage, and gate.
- Added an agent-dispatch DSL and decision criteria for splitting work across
  one agent, N parallel agents, nested teams, or an external cross-AI reviewer.
- Added the Agent Teams vs Subagent decision matrix covering model routing,
  budget limits, sync contracts, foreground/background dispatch, partial
  failure, and file-write conflict handling.
- Added `ASSETS/planning-doc-template.md` with YAML/markdown skeleton and a
  filled Project X example.
- Added `ASSETS/orchestration-decision-matrix.md` with routing tables,
  edge-case remediation, and model-role routing.
- De-projectified the skill by replacing project-specific labels with
  placeholders and adding a top-level customization walkthrough.
- Added `examples/template-blank-project.md` so a new project can copy the
  placeholder shape and fill it before running a wave.
- Added a cross-AI review expectation for non-primary-model critique before
  human final approval.

## v1.x

- Project-specific prototype-wave playbook focused on one concrete wave.
- Relied on narrative examples and local naming instead of reusable
  placeholder-driven contracts.
