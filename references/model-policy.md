# Anchor Wave v2.1 — Model Policy

> No model names are hardcoded in SKILL.md. All model selection happens
> here, env-var driven, with safe defaults.

## Claude (internal) routing

Used for: surface authoring, audit grading, master gallery aggregation.

```
CLAUDE_DECISION_MODEL   ${CLAUDE_DECISION_MODEL:-claude-opus-4-7}
CLAUDE_EXECUTION_MODEL  ${CLAUDE_EXECUTION_MODEL:-claude-sonnet-4-6}
CLAUDE_TOOL_MODEL       ${CLAUDE_TOOL_MODEL:-claude-haiku-4-5-20251001}
```

Per-role assignment:

| Role | Model var | Default |
|---|---|---|
| Wave plan author / orchestrator | CLAUDE_DECISION_MODEL | opus |
| Anchor doc author | CLAUDE_DECISION_MODEL | opus |
| Surface author — mature (form, list, settings) | CLAUDE_EXECUTION_MODEL | sonnet |
| Surface author — creative (canvas, governance, evidence) | CLAUDE_DECISION_MODEL | opus |
| Surface author — marquee (flagship) | CLAUDE_DECISION_MODEL | opus |
| Audit grader (per surface) | CLAUDE_EXECUTION_MODEL | sonnet |
| Master gallery aggregator | main thread | (inherits) |
| Doc summarization / JSON output schema check | CLAUDE_TOOL_MODEL | haiku |

## Codex (external cross-AI) routing

Used for: cross-AI red-team review per §6 trigger matrix.

```
CODEX_REVIEW_MODEL        ${CODEX_REVIEW_MODEL:-gpt-5.5}
CODEX_LIGHT_MODEL         ${CODEX_LIGHT_MODEL:-gpt-5.4-mini}
CODEX_FALLBACK_MODEL      ${CODEX_FALLBACK_MODEL:-gpt-5.4}
```

Per-trigger assignment:

| Trigger | Model var | Default | Why |
|---|---|---|---|
| REDO surface full review | CODEX_REVIEW_MODEL | gpt-5.5 | High-stakes form-level redesign verdict |
| FIX_NEEDED surface review | CODEX_REVIEW_MODEL | gpt-5.5 | Patch validity check needs strong reasoning |
| PASS sampling (15%) | CODEX_LIGHT_MODEL | gpt-5.4-mini | Cheap sanity check; sampling spreads cost |
| Re-audit after Wave 4 fix | CODEX_LIGHT_MODEL | gpt-5.4-mini | Confirm fix landed, no new regressions |
| If primary unavailable / quota exhausted | CODEX_FALLBACK_MODEL | gpt-5.4 | Degrade gracefully |

## Invocation pattern (codex-dispatch skill)

```bash
codex exec \
  --model "${CODEX_REVIEW_MODEL:-gpt-5.5}" \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --cd "$REPO_ROOT" \
  "$(cat audits/<wave>/cross-review/<surface>.prompt.md)"
```

Never inline the model name in the prompt. If a model is unsupported
by the local Codex CLI version, the dispatcher must fall back to
`CODEX_FALLBACK_MODEL` and record the fallback in the audit JSON
`models_used` field.

## Forbidden patterns

- ❌ Hardcoding `gpt-5.4` or `gpt-5.5` in SKILL.md
- ❌ Hardcoding `claude-opus-4-7` in subagent prompts (use role label)
- ❌ Mixing models within a single wave's cross-review without recording
  in the audit JSON (loss of reproducibility)

## Recording

Every audit JSON includes:

```json
{
  "models_used": {
    "surface_author": "claude-sonnet-4-6",
    "audit_grader": "claude-sonnet-4-6",
    "cross_review": "gpt-5.5",
    "fallback_triggered": false
  }
}
```

This enables retrospective analysis: "did opus surfaces really
out-innovate sonnet ones?" / "did the gpt-5.5 reviewer find issues
gpt-5.4-mini missed in sampling?"
