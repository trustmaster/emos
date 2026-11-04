# Example vault — "Payments Platform" team

A small, fully fictional emOS vault you can browse to see the system populated:
project hubs with auto-rollups, linked meetings/decisions/incidents, people
profiles, weekly notes, dashboards, and a filled-in `config.yaml`.

Everything here is invented (Acme Inc., a payments team). No real people, data,
or credentials.

## What to look at first

- [`03-projects/checkout-reliability/checkout-reliability.md`](demo-vault/03-projects/checkout-reliability/checkout-reliability.md)
  — a project **hub**: human-written sections up top, then a generated
  `Related` rollup linking every meeting, decision, incident, and person tied to
  the project via the `projects:` join key.
- [`03-projects/checkout-reliability/roadmap.toml`](demo-vault/03-projects/checkout-reliability/roadmap.toml)
  — the data behind the **swimlane roadmap** embedded in that hub, rendered to
  [SVG](demo-vault/10-reports/assets/roadmap-2026-W29.svg) and
  [HTML](demo-vault/10-reports/assets/roadmap-2026-W29.html) by `_tools/roadmap_render.py`.
  See [`docs/roadmap-view.md`](../template/docs/roadmap-view.md).
- [`03-projects/_index.md`](demo-vault/03-projects/_index.md) and the other
  `_index.md` dashboards — generated summary views.
- [`.agents/config.yaml`](demo-vault/.agents/config.yaml) — the `tools:`
  capability map wiring Jira/Confluence/Slack/GWS with example coordinates.
- [`.agents/voice/alex.md`](demo-vault/.agents/voice/alex.md) and its
  [`samples/`](demo-vault/.agents/voice/samples/) — a **writing voice**: the register emOS
  uses for files it authors, built from documents Alex wrote personally. This is user
  content, not framework content: emOS ships the template and the `/voice` skill, never a
  voice. A shipped voice would be a generic voice, which is the thing it exists to fix.
- [`import-demo/`](import-demo/) — a public Markdown RFC used to demo `/import-url`:
  import it by URL and watch it get classified, filed, and its owner-assigned
  action items pulled into the current week's plan.

## Running it live

This folder is for **reading**. To use emOS for real, scaffold a fresh vault
elsewhere with `npx emos-vault init` and start capturing — don't build on top of this
demo. The framework itself lives in [`../template/`](../template/).
