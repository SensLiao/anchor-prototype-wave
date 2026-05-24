# Anchor Wave v2.1 — Surface Taxonomy

> Enum of valid `claimed_surface_type` values. Each surface in the wave
> picks one. Mismatch between claim and DOM → Gate 0 BLOCK.

## Types

| Type | DOM signature | Required affordances | Examples in this gallery |
|---|---|---|---|
| `overlay` | scrim covering viewport (`position: fixed; inset: 0`) + content panel with z-index ≥ 1000 | scrim, centered/anchored panel, close affordance, ESC handler | x-onboarding, x-command-palette, pm-* (when modal) |
| `drawer` | panel anchored to viewport edge (`position: fixed; top: 0; right/left: 0; bottom: 0; width: ...`) | side panel, slide-in transform, close affordance, underlying app still visible | x-notifications, x-agent-chat (right-floating), pm-node-detail (when drawer) |
| `full-page` | app shell (header + main + optional aside); occupies viewport without scrim | header, main content area, possibly sidebar | p0-myworkfocus, p1-caselibrary, p2-caseworkspace, p3-admin-console, p4-client-portal, p6-portfolio-cockpit |
| `wizard` | linear step flow with rail + focused panel | step rail (left or top), step counter, focused form panel, next/back/skip affordances | case-create-stepper |
| `list` | row-based primary content with sort/filter/bulk affordances | filterable rows, sort headers, row actions, bulk action toolbar (if MVP) | p1-caselibrary (also full-page), p8-review-queue, pm-marketplace |
| `canvas` | spatial pan/zoom container with nodes + edges | viewport with pan/zoom, draggable nodes, edge rendering, minimap (optional) | p9-root-canvas, case-map, p-node-inspector-6tab (when canvas) |
| `form` | label + input pairs with validation + save/cancel | labeled inputs, validation state, dirty state, save/cancel/reset | ps-general, ps-agents, ps-connectors-detail, ps-settings, case-settings |
| `dashboard` | metric tiles + charts + activity feed | KPI tiles, charts, activity stream | my-agents-health, p6-portfolio-cockpit |
| `inspector` | tabbed detail panel for a single object | 4-6 tabs, single primary object, related artifacts panel | p-node-inspector-6tab |
| `audit-view` | evidence-dense layout with citations + trace | timeline / trace, evidence cards, approval affordances | p-prime-evidence-audit |
| `chat` | conversation thread + composer | message bubbles, composer, attachment row, agent selector | x-agent-chat |
| `command-tool` | command-first interface (palette, registry overlay) | command input, result list with command labels, keyboard footer | x-command-palette, x-mcp-registry |

## Composite surfaces

A surface may compose multiple types. Pick the **outermost** as
`claimed_surface_type`:

- `x-notifications` = `drawer` containing a `list` → claim `drawer`
- `x-agent-chat` = `drawer` containing a `chat` → claim `drawer`
- `p2-caseworkspace` = `full-page` containing tabs (one of which may
  contain `canvas`) → claim `full-page`

The inner type is recorded in `contract.inner_types` for completeness
but does not affect Gate 0.

## Disambiguation rules

When filename suggests one type but DOM clearly is another:

- DOM is authoritative for `actual_surface_type_evidence.from_dom`
- Disagreement between `claimed_surface_type` and DOM → Gate 0 BLOCK
- "Claim" comes from the wave plan / prior intent, not from a free read
  of the existing HTML (which may already be wrong)

## When to add a new type

If a wave produces a surface that doesn't fit any type:

1. STOP — do not invent a one-off type in `contract.json`
2. Propose new type in `closeout.md` `taxonomy_proposals` section
3. Human approves; this file is updated; affected surfaces re-classified

This prevents type sprawl. Currently 12 types is the cap; more than
that suggests an IA problem upstream, not a taxonomy problem.
