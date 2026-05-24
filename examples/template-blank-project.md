# Blank Project Placeholder Template

Copy this file into the target project, replace every placeholder, then use the
filled version as the input contract for an anchor prototype wave.

```yaml
project:
  name: "{project-name}"
  production_track_name: "{production-track-name}"
  research_track_name: "{research-track-name}"
  chassis_name: "{chassis-name}"
  research_vault_path: "{research-vault-path}"
  prototype_output_dir: "{prototype-output-dir}"
  rules_doc: "{rules-doc}"
  production_source_glob: "{production-source-glob}"
  global_token_file: "{global-token-file}"
  reference_repo_root: "{reference-repo-root}"
  raw_immutable_root: "{raw-immutable-root}"
  vault_sync_protocol: "{vault-sync-protocol}"

chassis:
  typography: "{font-family / weights / mono metadata rule}"
  radius: "{card radius / chip radius}"
  border: "{hairline border rule}"
  shadow: "{allowed micro shadow rule}"
  accent: "{single accent or governed palette}"
  surfaces: "{page / card / sunken / muted}"
  banned: "{visual effects or patterns forbidden in this project}"

modes:
  - key: "{mode-1}"
    name: "{mode display name}"
    applies_to: ["{surface-type}"]
  - key: "{mode-2}"
    name: "{mode display name}"
    applies_to: ["{surface-type}"]

wave:
  slug: "{wave-slug}"
  deliverables:
    - slug: "{surface-slug}"
      display: "{Surface Display Name}"
      mode: "{mode-1}"
      innovation_target: "{5-7 or 8-10}"
      output_html: "{prototype-output-dir}/{surface-slug}/index.html"
      output_writeup: "{research-vault-path}/design-research/{wave-slug}/{surface-slug}-writeup.md"
      status: "planned"

gates:
  human_final_gate: "Gate 12"
  approval_fields: "human-only"
  production_merge: "blocked until explicit approval"
```

Minimum fill checklist:

- [ ] Replace every `{PLACEHOLDER}`.
- [ ] Identify the anchor document and mode mapping table.
- [ ] Identify at least one source-readable or screenshot reference per surface family.
- [ ] Confirm output paths are separate from production source.
- [ ] Confirm master gallery ownership before dispatching any agents.
- [ ] Confirm cross-AI review timing after hi-fi output, before human final gate.

