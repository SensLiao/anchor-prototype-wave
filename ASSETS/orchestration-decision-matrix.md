# Orchestration Decision Matrix

> Companion to SKILL.md §3-bis. Two tables + edge-case remediation +
> external references. Use this when you're deciding **how to spawn**
> rather than **what to spawn**.
>
> **Customize**: this asset references `{PLACEHOLDER}` tokens from
> SKILL.md §0.2; fill them at the project level, not here.

---

## Table 1 — Surface × innovation × model × agent count × parallel-vs-serial

This is the master routing table. Walk down the surface list of your wave;
look up each surface's row; pick the configuration.

| Surface type | Innovation target | Model | Agent count | Parallel? | Why |
|---|---|---|---|---|---|
| **Default home** (mature) | 5-7 | sonnet | 1 subagent | yes (with sibling surfaces) | Mature paradigm; sonnet plateaus correctly at target range |
| **Settings / preferences** (mature) | 5-7 | sonnet | 1 subagent | yes | Form-heavy; mature form library = sonnet sufficient |
| **Login / auth** (mature) | 5-7 | sonnet | 1 subagent | yes | Constrained surface; no novel UX expected |
| **List / table / index** (mature) | 6-8 | sonnet | 1 subagent | yes | Density tuning; sonnet handles state matrix |
| **Detail / inspector** (mature) | 6-7 | sonnet | 1 subagent | yes | Tab strip + form sections; mature pattern |
| **Canvas / node editor** (creative) | 8-10 | **opus** | 1 subagent | yes | Spatial UX; novel interaction; sonnet plateaus too early |
| **Review queue / triage** (creative) | 8-10 | **opus** | 1 subagent | yes | Density + decision UX; novel pattern needed |
| **Evidence audit / governance** (creative) | 8-10 | **opus** | 1 subagent | yes | Compliance UX; transparency patterns are novel |
| **Marquee / flagship** (premium) | 9-10 | **opus** | 1 subagent | optionally async (own wave) | Defines gallery ceiling; do not skimp; consider giving it its own wave |
| **Element foundation** (atoms/surface/forms/nav) | 5-7 | sonnet | 1 subagent per element family | yes | Mature target; chassis lock-in is the goal not innovation |
| **Compound component** (form-field, dropdown, dialog) | 5-7 | sonnet | 1 subagent per component | yes | Built on Stage 2.1 atoms; mature target |
| **Master gallery aggregation** | n/a (aggregator) | main thread | n/a | sequential after wave | Must read all writeups; no isolated context |
| **Cross-AI review** | n/a (red team) | external CLI | 1 invocation | sequential after aggregation | Orthogonal lens; not a Claude model decision |
| **Anchor doc author** | n/a (decision) | opus, main thread | 1 | sequential at Stage 0 | High cost of being wrong; needs full context |
| **Element index freeze** | n/a (decision) | opus, main thread | 1 | sequential before Stage 2.1 | Must lock chassis at element scale before fan-out |
| **Wave plan author** | n/a (planning) | main thread | 1 | sequential before any spawn | Plan-then-execute discipline; STOP for human |

### Quick math

If your wave has X mature + Y creative + Z marquee:

```
total_agents     = X + Y + Z + 1 (master gallery) + 1 (cross-AI) + 1 (context author)
                 = X + Y + Z + 3 orchestrator-side roles
parallel_in_wave = X + Y + Z          (the surface subagents)
opus_count       = Y + Z              (creative + marquee; mature uses sonnet)
sonnet_count     = X                  (the mature surfaces)
```

If `parallel_in_wave > 10` → split into 2 waves of ≤10 each.

---

## Table 2 — Edge cases × symptom × remediation

When orchestration breaks, here's the playbook. Each row is one symptom
the orchestrator (you, the main thread) might observe; each remediation
is the fix.

| Edge case | Symptom | Severity | Remediation |
|---|---|---|---|
| **One agent fails (timeout)** | Subagent X returns no output or partial; siblings completed | medium | Read partial output → diagnose prompt → re-spawn JUST X with corrected prompt. Don't re-run wave. |
| **One agent fails (boundary violation)** | Subagent X wrote outside its allowed paths (Gate 10 BLOCK) | high | Revert the violating writes (git restore the bad paths) → re-spawn X with stricter boundary prompt → re-verify Gate 10. |
| **One agent ships under-quality** | Subagent X returns but Gate 11 self-audit has 2+ BLOCKs | medium | Don't re-spawn yet — first check whether the prompt was under-specified (mode unclear? anchor ambiguous?). If prompt was clear: re-spawn with stricter constraints. If prompt was ambiguous: fix the prompt first. |
| **Anchor under-specified** | Multiple surfaces drift on the same chassis dimension (e.g., 3 surfaces use 3 different accents because anchor said "TBD") | HIGH | Stop the wave. Author an anchor amendment (date-prefixed) that commits to the missing value. Re-spawn affected surfaces with updated `_context.md`. (Failure Mode F-6) |
| **N > max concurrent** | Spawned 15 subagents; quota / context errors mid-wave | high | Kill in-flight work that didn't complete cleanly. Split remaining into 2 waves. Re-spawn the failures as part of Wave 2. (Failure Mode F-9 / §3-bis.3) |
| **Two agents target same file** | Race condition: subagent X and Y both write to `index.md` | high | Hard rule: subagents NEVER write to shared files. Orchestrator batches shared-file updates at wave end (e.g., index/log appends). If race happened: discard later write, re-run orchestrator's batch step. (§3-bis.4 Pattern C) |
| **Partial output** (writeup present, HTML missing) | Subagent X returned writeup but no HTML | medium | Read writeup for clues (did agent get stuck mid-spec?). Re-spawn X with explicit reminder: "Write HTML first, writeup after". |
| **Partial output** (HTML present, writeup missing) | Subagent X returned HTML but no writeup | medium | Most common in long subagent contexts (HTML consumed budget; writeup truncated). Re-spawn X with smaller HTML target (cap at LINE_CEILING) OR ask subagent to write writeup first. |
| **Stage 2.0 floated** | Stage 2.1 element subagent cites a token that doesn't exist in element-contract-index | HIGH | Stop the wave. Freeze Stage 2.0 properly (status=ratified). Re-spawn affected 2.1 subagents. (Failure Mode F-1) |
| **Cross-AI review echoes Claude self-grade** | Cross-AI review says "Claude graded 9.0; I agree; top 3 improvements: minor" | medium | Re-issue cross-AI prompt with explicit "do NOT restate self-grade; cite DOM patterns + CSS selectors + frontier products" framing. (Failure Mode F-8) |
| **Premium tier diluted** | Marquee mode used on 5 of 10 surfaces | medium | Audit: re-classify those surfaces back to standard modes. Premium is constrained to 0-1 per wave. (Failure Mode F-7) |
| **Master gallery looks incoherent** | Gallery aggregates 10 surfaces but the chassis is invisible (each card looks different) | HIGH | Chassis is broken at ensemble scale. Audit each writeup §3 "Visual Chassis Application" — find which surfaces drifted. Re-spawn drifted surfaces. Consider strengthening `_context.md` first. |
| **Cross-AI review uncovers a chassis-level fault** | Cross-AI review's "top 3 priority across wave" includes a recurring issue (e.g., 5 of 10 surfaces have same a11y violation) | medium | This is a chassis fix, not a surface fix. Author a chassis amendment (date-prefixed). Don't re-spawn all 10 surfaces; defer the chassis fix to next wave's `_context.md` update. |
| **vN naming chain resurrects** | Subagent writes `*-v3.md` instead of `<DATE>-<topic>.md` | low | Rename file (date-prefix slug). Add `superseded_by` field if it deprecates something. (Failure Mode F-2) |
| **Subagent fills `approved_by`** | Writeup frontmatter has non-null `approved_by` without user signoff | high | Revert that field to null. Add reminder in prompt: "approved_by/approved_date stay null; HUMAN ONLY fills them at Gate 12." (Failure Mode F-4) |
| **Plan-then-execute skipped** | Orchestrator spawned subagents without writing a wave plan first | HIGH | Stop the wave. Snapshot what's been done. Write the plan retroactively as a forensic doc. Decide whether to continue (with ratified plan) or restart. (Failure Mode F-10) |
| **Plan ratified, then mid-wave scope creep** | Halfway through, user adds 2 surfaces to the wave | high | End the current wave at the next natural sync point. Write a new plan for Wave 2 covering the additions. Don't bend an in-flight plan. |
| **Subagent quota exhausted** | Spawn returns error before subagent starts | medium | Pause the wave. Wait for quota window. Resume with remaining subagents. Consider falling back: if Claude subagent quota is exhausted, use `codex-dispatch` for execution agents (orchestrator stays as main thread). |
| **Sync at Gate 11 not happening** | Subagent declares "done" but Gate Report missing from writeup §6 | medium | Reject the "done" claim. Re-prompt subagent: "Add Gate Report to writeup §6 before claiming done." Don't aggregate without Gate Reports. |
| **Background task silently failed** | Cross-AI review fired in background; orchestrator forgot to check; days later, found no output | low | Always foreground cross-AI review when possible. If you must background, pair with explicit "check this URL/file at end of session" reminder. |
| **Mid-wave model decision change** | Realize one mature surface needs opus after 5 minutes of sonnet output | low | Let sonnet finish. Read its output. If still mature target (5-7), keep it. If user requirement actually was creative target, re-spawn that one with opus. |

---

## §3 — Decision flowchart

```
                         User says "spawn the wave"
                                    │
                                    ▼
                  ┌─────────────────────────────────┐
                  │  Wave plan exists + ratified?   │
                  └────────────┬────────────────────┘
                          NO   │   YES
                ┌──────────────┴──────────────┐
                ▼                             ▼
       Author wave plan                Read plan §4 agent team
       (§3-tris template)                       │
                │                               ▼
                │                  ┌────────────────────────┐
                │                  │ subagent count ≤ 10 ?  │
                │                  └─────────┬──────────────┘
                │                       NO   │   YES
                │            ┌──────────────┴──────────────┐
                │            ▼                             ▼
                │     Split into 2 waves            Author / verify
                │     Update plan §4                _context.md
                │            │                             │
                │            └─────────────┬───────────────┘
                │                          ▼
                │                ┌──────────────────────┐
                │                │ grep _context.md     │
                │                │ for {PLACEHOLDER}    │
                │                └──────────┬───────────┘
                │                     0     │   >0
                │                ┌──────────┴──────────┐
                │                ▼                     ▼
                │           Spawn wave         Fill remaining
                │           (parallel)         placeholders first
                │                │                     │
                │                └──────────┬──────────┘
                │                           ▼
                ▼                ┌──────────────────────┐
       STOP for human            │ Await all subagents  │
       approval                  └──────────┬───────────┘
                                            ▼
                                 ┌──────────────────────┐
                                 │ Any failures?        │
                                 └──────────┬───────────┘
                                       NO   │   YES
                                ┌───────────┴──────────────┐
                                ▼                          ▼
                       Verify Gate Reports        Apply Table 2 remediation
                       (§6 each writeup)          (re-spawn / fix prompt / etc.)
                                │                          │
                                └─────────────┬────────────┘
                                              ▼
                                  ┌────────────────────────┐
                                  │ Aggregate master       │
                                  │ gallery (main thread)  │
                                  └──────────┬─────────────┘
                                             ▼
                                  ┌────────────────────────┐
                                  │ Fire cross-AI review   │
                                  │ (orthogonal CLI)       │
                                  └──────────┬─────────────┘
                                             ▼
                                  ┌────────────────────────┐
                                  │ Hand off to human      │
                                  │ for Gate 12 sign-off   │
                                  └────────────────────────┘
```

---

## §4 — External references

When inventing orchestration patterns beyond what this skill documents, the
following Tier 2 (open-web) resources informed this matrix. Cite them when
extending; do not paste their text into project notes verbatim.

| Source | URL | What to borrow |
|---|---|---|
| Anthropic — "How we built our multi-agent research system" | <https://www.anthropic.com/engineering/built-multi-agent-research-system> | Orchestrator-worker pattern; lead agent decomposes → spawns subagents; subagents return artifacts → lead aggregates. The "lead orchestrator + parallel workers" architecture is the canonical pattern this skill applies. |
| Anthropic — "Agentic / agent best practices" | <https://www.anthropic.com/research/building-effective-agents> | When to use parallelization vs sequencing; "evaluator-optimizer" loop for self-audit; "router" pattern for surface-type → model routing. |
| LangGraph — Supervisor (multi-agent) pattern | <https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/> | Supervisor calls workers; workers return; supervisor decides next step. Read for state-machine framing. |
| LangGraph — Hierarchical agent teams | <https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/> | Nested teams (avoid by default in this skill — see §3-bis.1); only useful when one worker is itself a wave. |
| smol-developer | <https://github.com/smol-ai/developer> | "Make me a junior developer for life" — fan-out file generation pattern. Original "spawn N parallel writes against one prompt-shaped spec" reference. |
| AutoGen (Microsoft) | <https://microsoft.github.io/autogen/> | Multi-agent conversation framework. Read for the **agent role** taxonomy (UserProxyAgent / AssistantAgent / GroupChatManager). |
| CrewAI | <https://docs.crewai.com/> | Role-based agent teams; tool delegation. Use as comparison when deciding whether a "team" concept fits your wave. |

**Tier announcement (per project HARD RULE #1)**: any of the above used
inside a project's wave plan must be announced as a Tier 2 fallback. The
skill itself integrates them as architectural references; the project that
uses this skill should still prefer Tier 0 (in-repo prior art) and Tier 1
(local checked-out reference) sources first.

---

## §5 — Tips for using this matrix

1. **Walk both tables BEFORE spawning**, not after a failure. The matrix is
   prescriptive, not forensic.
2. **Pin Table 1 in the wave plan §4** — verbatim row per agent — so reviewers
   can verify model choice without guessing.
3. **Pin Table 2 in `_context.md` §3** — every subagent should know which
   edge cases their orchestrator will catch.
4. **The flowchart in §3 is the orchestrator's contract** — if you skip a
   step, you're improvising. Improvising on wave fan-out is how 8-of-10
   subagents come back contradictory.
5. **External references in §4 are Tier 2** — used to ground this matrix,
   not to be cited inside subagent prompts. Subagent prompts should cite
   Tier 0 (in-repo) and Tier 1 (local reference) sources only.
