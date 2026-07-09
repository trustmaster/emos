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
- [`03-projects/_index.md`](demo-vault/03-projects/_index.md) and the other
  `_index.md` dashboards — generated summary views.
- [`.agents/config.yaml`](demo-vault/.agents/config.yaml) — the `tools:`
  capability map wiring Jira/Confluence/Slack/GWS with example coordinates.

## Running it live

This folder is for **reading**. To use emOS for real, scaffold a fresh vault
elsewhere with `npx emos init` and start capturing — don't build on top of this
demo. The framework itself lives in [`../template/`](../template/).
