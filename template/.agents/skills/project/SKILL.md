---
name: project
description: Load the full context of a project into the session — hub doc, all linked meetings/decisions/incidents/reports, people, open TODOs, and project-local docs — as one briefing. Use when the user wants to get up to speed on a project, work on it, or "pull everything about X into one place". Pass the project name or slug as args.
---

Assemble a single-session briefing for the project named in args. This is a **read + brief** workflow — the hub doc is the durable artifact; this does not create a new file.

Read `paths.projects` from `.agents/config.yaml` (default `03-projects`).

## Step 1 — Resolve the project

Match args to a folder in `{paths.projects}/` (exact slug, or fuzzy match on title/folder name). If it resolves to more than one, list the candidates and stop.

## Step 2 — Refresh, then read the hub

1. Run the `project-sync` logic for this slug first, so the rollup reflects current reality.
2. Read the hub doc `{paths.projects}/{slug}/{slug}.md`. Note: objective, status, priority, quarter, owner, team_members, external links (Jira/Confluence/dashboard), and the freshly-regenerated Related rollup.

## Step 3 — Pull the linked context

From the rollup's linked files, read enough to brief (don't dump full files):
- **Meetings** — the 2–3 most recent; note decisions taken and open action items.
- **Decisions** — any with `status: proposed` (needs resolution) + the latest accepted ones.
- **Incidents** — any not yet `reviewed`.
- **Strategy** — the OKR/roadmap entries this project rolls up to.
- **Reports** — the most recent report mentioning it.

## Step 4 — Recent activity & TODOs

- Scan `01-weekly/` for the past ~6 weeks for `#project/{slug}` tags and mentions of the project title. Collect open `- [ ]`, `#blocked`, `#risk`, `#follow-up` items.
- List the project-local working docs in `{paths.projects}/{slug}/docs/` (name + one-line gist each).

## Step 5 — Brief

Output a structured briefing:

- **Snapshot** — status · priority · quarter · owner · target date, one-line objective.
- **Where it stands** — synthesized from recent meetings, decisions, reports.
- **Open & blocked** — TODOs, blockers, risks, unresolved decisions, un-reviewed incidents.
- **People** — owner + contributors.
- **Docs & links** — project-local docs and external links available to open.
- **Suggested next actions** — 2–4 concrete items, most important first.

Confirm the hub rollup was refreshed and name the hub file path.
