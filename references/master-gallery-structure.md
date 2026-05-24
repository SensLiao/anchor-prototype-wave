# Anchor Wave v3.0.0 — Master Gallery Structure (Stage 11 locked spec)

> Stage 11 of the pipeline writes `<output-dir>/index.html`. This document
> locks the layout to mirror the proven `ui-lab/v2-anchor-prototypes/index.html`
> structure exactly. Tokens and content vary per anchor + page list; the
> structural shape, control-panel behavior, row markup, and JS filter
> contract are non-negotiable.

Source of truth: `ui-lab/v2-anchor-prototypes/index.html` (the v2 wave
that ratified this pattern). When in doubt about what an element should
look like, read that file.

---

## §1 — Document skeleton

```
<!DOCTYPE html>
<html lang="zh-CN">  ← or appropriate lang per page list
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{ANCHOR_NAME} Prototype Review Hub | {PROJECT_NAME}</title>
  <style>
    /* §2 — :root tokens (from anchor) */
    /* §3 — base resets + .mono + .mono-label + .sr-only utilities */
    /* §4 — hero + stat-row + info-row (review checklist + update log card) */
    /* §5 — control panel (search + filters + jump nav) */
    /* §6 — section.group + .row + .row-meta + .meta-chip + .status-chip */
    /* §7 — JS-controlled .hidden */
  </style>
</head>
<body>
  <main class="shell">
    <header class="hero"> ... </header>
    <div class="info-row"> ... </div>           ← optional: review checklist + update log
    <div class="ops-grid"> ... </div>           ← optional: review queue + artifact list
    <div class="control-panel"> ... </div>
    <section class="group" id="group-{NAME}"> ... </section>  ← N times
    <footer> ... </footer>
  </main>
  <script>
    /* §8 — rowMetadata + applyFilters */
  </script>
</body>
</html>
```

---

## §2 — `:root` tokens (drive everything)

Token names are LOCKED. Anchor supplies the values.

```css
:root {
  --page-bg: {ANCHOR.surface.page};
  --card-bg: {ANCHOR.surface.card};
  --sunken-bg: {ANCHOR.surface.sunken};
  --muted-bg: {ANCHOR.surface.muted};

  --text-primary: {ANCHOR.text.primary};
  --text-secondary: {ANCHOR.text.secondary};
  --text-tertiary: {ANCHOR.text.tertiary};
  --text-mono-label: {ANCHOR.text.mono_label};

  --border-hairline: {ANCHOR.border.hairline};
  --border-strong: {ANCHOR.border.strong};

  --accent: {ANCHOR.accent.value};
  --status-amber: {ANCHOR.status.amber.fg};
  --status-amber-bg: {ANCHOR.status.amber.bg};
  --status-blue: {ANCHOR.status.blue.fg};
  --status-blue-bg: {ANCHOR.status.blue.bg};
  --status-green: {ANCHOR.status.green.fg};
  --status-green-bg: {ANCHOR.status.green.bg};
  --status-red: {ANCHOR.status.red.fg};
  --status-red-bg: {ANCHOR.status.red.bg};
  --shadow-micro: {ANCHOR.shadow.micro};

  --radius-card: {ANCHOR.radius.card};
  --radius-chip: {ANCHOR.radius.chip};
  --radius-pill: 999px;

  --space-1: 4px;   --space-2: 8px;   --space-3: 12px;
  --space-4: 16px;  --space-5: 20px;  --space-6: 24px;
  --space-8: 32px;  --space-10: 40px; --space-12: 48px;

  --font-sans: '{ANCHOR.typography.sans}', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: '{ANCHOR.typography.mono}', ui-monospace, SFMono-Regular, monospace;
}
```

If the anchor changes the spacing scale, edit the `--space-*` values
above; do NOT introduce a new variable namespace.

---

## §3 — Base resets + utility classes (LOCKED)

```css
* { box-sizing: border-box; }
body {
  margin: 0; padding: 0;
  background: var(--page-bg);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: 14px; line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  /* Optional dot grid — keep if anchor allows it; remove for pure flat anchors */
  background-image: radial-gradient(circle, {ANCHOR.dot_grid_value} 1px, transparent 1px);
  background-size: 16px 16px;
}
a { color: inherit; text-decoration: none; }
button, input, select { font: inherit; }

a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible {
  outline: 2px solid {ANCHOR.accent_focus_or_default_blue};
  outline-offset: 2px;
  border-radius: 4px;
}

.sr-only {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0,0,0,0); white-space: nowrap; border: 0;
}
.mono { font-family: var(--font-mono); }
.mono-label {
  font-family: var(--font-mono);
  font-size: 10px; font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-mono-label);
}

.shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-12) var(--space-8);
}
```

---

## §4 — Hero header (LOCKED markup, anchor styling)

```html
<header class="hero">
  <div class="hero-tag mono-label">{ANCHOR_NAME} · {WAVE_SLUG}</div>
  <h1>{WAVE_TITLE}</h1>
  <p>{ONE_PARAGRAPH_DESCRIPTION_OF_WAVE_PURPOSE_AND_AUDIENCE}</p>
  <div class="stat-row">
    <div class="stat">
      <div class="stat-num">{N_SURFACES}</div>
      <div class="stat-label">prototypes</div>
    </div>
    <div class="stat">
      <div class="stat-num">{N_GROUPS}</div>
      <div class="stat-label">groups</div>
    </div>
    <div class="stat">
      <div class="stat-num">{WAVE_DATE}</div>
      <div class="stat-label">updated</div>
    </div>
  </div>
</header>
```

CSS (LOCKED structure, anchor-token-driven values):

```css
header.hero {
  margin-bottom: var(--space-10);
  padding-bottom: var(--space-8);
  border-bottom: 1px solid var(--border-hairline);
}
.hero-tag { margin-bottom: var(--space-3); }
.hero h1 {
  font-size: 32px; font-weight: 600;
  letter-spacing: -0.02em;
  margin: 0 0 var(--space-3) 0;
}
.hero p {
  font-size: 15px;
  color: var(--text-secondary);
  max-width: 720px;
  margin: 0;
}
.hero .stat-row {
  display: flex; gap: var(--space-8);
  margin-top: var(--space-6);
}
.stat-num {
  font-size: 28px; font-weight: 600;
  letter-spacing: -0.01em;
  line-height: 1;
  margin-bottom: var(--space-1);
}
.stat-label {
  font-family: var(--font-mono);
  font-size: 10px; letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-tertiary);
}
```

---

## §5 — Control panel (LOCKED markup + JS contract)

```html
<div class="control-panel" aria-label="Prototype directory controls">
  <label class="sr-only" for="prototypeSearch">搜索原型</label>
  <input class="control-input" id="prototypeSearch" type="search"
         placeholder="搜索页面、route、status、risk..." autocomplete="off">

  <label class="sr-only" for="statusFilter">按状态过滤</label>
  <select class="control-select" id="statusFilter">
    <option value="all">全部状态</option>
    <option value="updated">已更新</option>
    <option value="review">可审阅</option>
    <option value="retain">保留参考</option>
    <option value="rebuild">需重建</option>
    <option value="parked">暂缓</option>
  </select>

  <label class="sr-only" for="riskFilter">按风险过滤</label>
  <select class="control-select" id="riskFilter">
    <option value="all">全部风险</option>
    <option value="low">低风险</option>
    <option value="medium">中风险</option>
    <option value="high">高风险</option>
  </select>

  <nav class="jump-list" aria-label="Group jump">
    <a class="jump-link" href="#group-{group-1-slug}">{Group 1 Display}</a>
    <a class="jump-link" href="#group-{group-2-slug}">{Group 2 Display}</a>
    <!-- ... one per group ... -->
    <span class="result-count" id="resultCount" aria-live="polite">{N} shown</span>
  </nav>
</div>
```

The 3 input IDs (`prototypeSearch`, `statusFilter`, `riskFilter`) and the
output ID (`resultCount`) are LOCKED — Stage 11's JS depends on them.

---

## §6 — Group + row (LOCKED markup, repeated N times)

```html
<section class="group" id="group-{group-slug}">
  <div class="group-head">
    <h2>{Group display name (zh)}</h2>
    <span class="count">{N} prototypes</span>
    <span class="group-desc">{One-line group description}</span>
  </div>
  <div class="row-list">

    <a class="row" href="{slug}/index.html" target="_blank" rel="noopener">
      <span class="row-id">{ID}</span>
      <span class="row-name">
        <span class="row-titleline">
          {Display title (zh)}
          {ROW_NOW_DOT_IF_UPDATED}    ← <span class="row-now-dot" aria-label="..."></span>
        </span>
        <span class="sub">{Sub-line en + brief description}</span>
        {STATUS_CHIP_IF_PRESENT}        ← <span class="status-chip {status}">{label}</span>
      </span>
      <span class="row-route">{route}</span>
      <span class="row-arrow">→</span>
    </a>

    <!-- ... N rows per group ... -->

  </div>
</section>
```

Class names `row` / `row-id` / `row-name` / `row-titleline` / `sub` /
`row-now-dot` / `status-chip` / `row-route` / `row-arrow` are LOCKED.
Stage 11's JS reads `<a class="row">` elements and looks up
`rowMetadata[href]` keyed by the `href` attribute.

---

## §7 — JS-controlled `.hidden`

```css
.row.hidden,
section.group.hidden { display: none; }
```

---

## §8 — Embedded `<script>` (LOCKED contract)

The Stage 11 aggregator emits this exact script. The `rowMetadata` object
is auto-populated from the page list given to the skill.

```javascript
const rowMetadata = {
  "{slug-1}/index.html": { status: "{status}", risk: "{risk}", updated: "{YYYY-MM-DD}", note: "{one-line}" },
  "{slug-2}/index.html": { status: "{status}", risk: "{risk}", updated: "{YYYY-MM-DD}", note: "{one-line}" },
  // ... one per surface ...
};

const statusLabels = {
  updated: "已更新",
  review:  "可审阅",
  retain:  "保留参考",
  rebuild: "需重建",
  parked:  "暂缓"
};
const riskLabels = {
  low:    "low risk",
  medium: "medium risk",
  high:   "high risk"
};

const rows = Array.from(document.querySelectorAll(".row"));
const searchInput = document.getElementById("prototypeSearch");
const statusFilter = document.getElementById("statusFilter");
const riskFilter = document.getElementById("riskFilter");
const resultCount = document.getElementById("resultCount");

rows.forEach((row) => {
  const href = row.getAttribute("href");
  const meta = rowMetadata[href] || { status: "retain", risk: "medium", updated: "{wave-date}", note: "research reference" };
  row.dataset.status = meta.status;
  row.dataset.risk = meta.risk;
  row.dataset.updated = meta.updated;
  row.dataset.note = meta.note;
  row.querySelector(".row-arrow")?.setAttribute("aria-hidden", "true");

  const name = row.querySelector(".row-name");
  if (name && !name.querySelector(".row-meta")) {
    const metaLine = document.createElement("span");
    metaLine.className = "row-meta";
    metaLine.innerHTML = [
      `<span class="meta-chip ${meta.status}">${statusLabels[meta.status]}</span>`,
      `<span class="meta-chip ${meta.risk}">${riskLabels[meta.risk]}</span>`,
      `<span class="meta-chip">${meta.updated}</span>`,
      `<span class="meta-chip">${meta.note}</span>`
    ].join("");
    name.appendChild(metaLine);
  }
});

function applyFilters() {
  const query = searchInput.value.trim().toLowerCase();
  const status = statusFilter.value;
  const risk = riskFilter.value;
  let visibleRows = 0;

  rows.forEach((row) => {
    const text = [
      row.textContent,
      row.getAttribute("href"),
      row.dataset.status,
      row.dataset.risk,
      row.dataset.note
    ].join(" ").toLowerCase();
    const matchesQuery = !query || text.includes(query);
    const matchesStatus = status === "all" || row.dataset.status === status;
    const matchesRisk = risk === "all" || row.dataset.risk === risk;
    const visible = matchesQuery && matchesStatus && matchesRisk;
    row.classList.toggle("hidden", !visible);
    if (visible) visibleRows += 1;
  });

  document.querySelectorAll("section.group").forEach((group) => {
    const hasVisibleRow = Boolean(group.querySelector(".row:not(.hidden)"));
    group.classList.toggle("hidden", !hasVisibleRow);
  });

  resultCount.textContent = `${visibleRows} shown`;
}

searchInput.addEventListener("input", applyFilters);
statusFilter.addEventListener("change", applyFilters);
riskFilter.addEventListener("change", applyFilters);
applyFilters();
```

Behavior contract (LOCKED):
- typing in search filters rows by visible text + href + status + risk + note
- changing status filter restricts to matching `data-status`
- changing risk filter restricts to matching `data-risk`
- groups with 0 visible rows are auto-hidden
- `resultCount` is live-updated
- meta chips appended client-side (status / risk / updated / note)

---

## §9 — Optional sections (anchor + page list decides)

The following sections from v2 are optional, included only when the
page list indicates they're relevant:

| Optional section | When to include | Example from v2 |
|---|---|---|
| `.info-row` (review checklist + update log) | When wave has multi-revision history | v2 lines 146-176 |
| `.ops-grid` (review queue + artifact list) | When wave needs a triage queue | v2 lines 183-256 |
| `.update-log-card` (collapsible log entries) | When wave has dated changelog entries | v2 lines 258-365 |
| `.row-now-dot` (pulsing update indicator) | When a row was updated this cycle | v2 lines 367-394 |
| `<details>` log entries with `.log-link-chip` | When changelog rows link to audits | v2 lines 740-756 |

Always include:
- `header.hero`
- `.control-panel`
- `section.group` × N
- `<footer>`
- `<script>` with `rowMetadata` + filter logic

---

## §10 — Forbidden modifications

- ❌ Renaming any LOCKED class (`row`, `row-id`, `row-name`, etc.)
- ❌ Renaming `prototypeSearch` / `statusFilter` / `riskFilter` / `resultCount` IDs
- ❌ Inlining different filter logic (status + risk are the canonical axes)
- ❌ Adding additional global filters without an ADR — extend
  `rowMetadata` shape if more metadata is needed, but the 3 user-facing
  controls stay
- ❌ Removing `aria-label` / `aria-live` / `.sr-only` accessibility hooks
- ❌ Removing the keyboard focus styles
- ❌ Changing the `<a class="row" href="{slug}/index.html" target="_blank">`
  link contract — Stage 11's JS depends on the `href` lookup key

---

## §11 — Reference: v2 source

Read `ui-lab/v2-anchor-prototypes/index.html` lines:
- 1-105:    `:root` tokens + base resets
- 107-145:  `header.hero` + stat-row
- 146-365:  optional info-row, ops-grid, update-log-card, etc.
- 367-394:  row-now-dot pulse animation
- 395-783:  control-panel + section.group + row markup
- 1120-1124: footer
- 1126-1246: `<script>` rowMetadata + filter logic

When a Stage 11 aggregator hits an ambiguity, read the v2 source and
mirror the choice. v2 is the locked reference.
