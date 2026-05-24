# Research-Sync Protocol Template ({vault-sync-protocol})

> Every artifact produced by this skill must observe the project's local
> **{vault-sync-protocol}** — three updates per write, never one, never
> two. The protocol name is project-specific (some projects call it
> "note-ingest", "kb-publish", "research-sync", or another local publish protocol); the shape
> is the same.

## The three updates

1. **Write atomic note** — one file per concept / decision. YAML frontmatter
   with 6 required fields (slug / title / type / status / confidence /
   created). Body uses `[[slug]]` forward-links.
2. **Update `{research-vault-path}index.md`** — add slug to appropriate
   type section.
3. **Append `{research-vault-path}log.md`** — timestamped log entry naming
   source + produced notes.

## What does NOT update

- A "current step" / "hot" file (e.g., `{research-vault-path}hot.md`) —
  reserved for {production-track-name} current step (a short
  ≈500-word slot). {research-track-name} waves do NOT touch it.
- `{raw-immutable-root}` — immutable. Never edit raw.
- ADR files — only an ADR ratification commit may edit `decisions/`.

## Naming convention

Use **date-prefixed topic slugs**:

- ✅ `<YYYY-MM-DD>-<topic-name>-anchor.md`
- ✅ `<YYYY-MM-DD>-cross-review-<N>-surfaces.md`
- ❌ `visual-language-v2.md` (vN naming chain — retired pattern)
- ❌ `anchor-final.md` (no date / no topic / ambiguous)
- ❌ `<chassis-name>-v2.md` (vN in filename — even though "v2" here
  means product version, the precedent is bad)

The version is inside the doc (`§Version Stack` table), not in the filename.

## log.md append format

Append a new section at the **top** of `{research-vault-path}log.md`
(newest first):

```markdown
## {DATE} — {ONE_LINE_HEADLINE_OF_THE_INGEST}

> {USER_DIRECTIVE_OR_TRIGGER_SUMMARY}

**Core deliverable**: {ONE_LINE}.

**Produced notes**:
- `[[{slug-1}]]` — {one-line description}
- `[[{slug-2}]]` — {one-line description}
- `[[{slug-3}]]` — {one-line description}

**Sources read**:
- `{path-1}` ({raw or artifact})
- `{path-2}`

**Boundary self-check**:
- ✅ All output in {prototype-output-dir} or research vault
- ✅ 0 modifications to {LIST_OF_FORBIDDEN_PATHS}
- ✅ 0 changes to the production-track "current step" / hot file
- ✅ 0 runtime deps added

**Cross-link**:
- {SLUG_OR_FILE_PATH} — relevant existing note

---
```

## index.md update format

Find the appropriate type section in `{research-vault-path}index.md`
(e.g., `## synthesis`, `## decisions`, `## references`) and add a new
entry alphabetically OR chronologically depending on existing pattern.
Use this row format:

```markdown
- [[{slug}]] — {title} ({status} · {confidence}) — {one-line description}
```

If a new type section is needed, register the type in
`{research-vault-path}_registry/types.md` first (or your project's
equivalent registry).

## Subagent compliance

Every subagent in this skill's wave receives this template as part of its
prompt. The wave orchestrator (main thread) is responsible for:

1. Verifying each subagent's writeup has correct frontmatter
2. Aggregating subagent outputs into ONE log.md entry (not N entries —
   batch the wave)
3. Updating index.md in ONE commit per wave

Sub-agents do NOT edit `log.md` or `index.md` themselves. They write only
their writeup + their HTML. The orchestrator does the vault sync.

## Approval recording (Gate 12 only, HUMAN ONLY)

When the user approves a surface at Gate 12:

1. Edit the surface writeup frontmatter:
   ```yaml
   approved_by: {user-name}
   approved_date: {DATE}
   ```
2. Append to `{research-vault-path}log.md` (new section at top):
   ```markdown
   ## {DATE} — Gate 12 approval — {surface-slug}

   User approved {surface-slug} at Gate 12. Gates 1-11 PASS per
   `[[{surface-slug}-writeup]]`. WARN items: {list-or-none}. Next:
   Stage 4 production impl pkg → {production-track-name} merge.

   ---
   ```
3. The agent never writes either of these unilaterally — only after
   explicit user approval message.

## Failure modes

- **Skipping log.md update** — wave looks done but research vault is
  incomplete; audit fails. Fix: orchestrator must batch the log.md update
  at wave end.
- **Subagent writes log.md directly** — multiple parallel writes corrupt
  the file. Fix: subagents have read-only access to log.md.
- **vN naming chain resurrects** — someone renames an existing note to
  `*-v3.md`. Fix: rename forbidden; use `superseded_by` field in
  frontmatter instead.
- **Current-step / hot file updated by a research-track wave** — boundary
  violation. Fix: pre-commit grep check; if a {research-track-name} wave
  touches the "current step" / "hot" file, reject.
