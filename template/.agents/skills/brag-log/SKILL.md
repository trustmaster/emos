---
name: brag-log
description: Append accomplishments to your evergreen impact log (brag doc), creating it if absent, so self-reviews and weekly snippets write themselves. With no args, harvest recent wins from your weeklies, completed projects, decisions, and incidents and propose entries to add. Use when the user wants to log a win, update their brag doc / impact log, or record an accomplishment. Pass the accomplishment as args, or none to harvest.
---

Maintain the owner's evergreen **impact log** (brag doc) at `{paths.reports}/brag-log.md`.

**Resolve role first:** read `owner.role` from `.agents/config.yaml` (default `em`) and open the
role pack at `.agents/roles/{role}.md`. Use its `{{review_dimensions}}` to categorize each entry.
Also read `paths.reports` (default `10-reports`), `owner.name`, and `owner.slug` from config.

1. **Ensure the log exists.** If `{paths.reports}/brag-log.md` is absent, read
   `_templates/impact-log.md` and create it, resolving `{{owner_name}}` / `{{owner_slug}}` and
   setting `updated:` to today.
2. **Gather entries.**
   - **args present** — treat args as one accomplishment. Draft a single entry from it; ask for
     the impact/metrics only if none is stated and none is obvious from context.
   - **no args** — harvest candidates the owner hasn't logged yet:
     - `01-weekly/` — this and last week's `#win` items and completed deliverables.
     - `03-projects/` — projects where `owner == owner.slug` with a recent milestone or a
       `completed`/`paused` status change.
     - `04-decisions/` — ADRs the owner authored (`deciders` includes `{{owner_slug}}`).
     - `05-incidents/` — incidents the owner owned or helped resolve.
     Propose the drafted entries and confirm before writing. Skip anything already in the log
     (match on headline/date).
3. **Draft each entry** with: a `### YYYY-MM-DD — headline`, the best-fit **Dimension** from the
   role's `{{review_dimensions}}`, **What**, **Impact** (numbers when available), **Evidence**
   (links to PRs / docs / dashboards / tickets), and optional **Recognition**.
4. **Prepend** entries to the top of the `## Log` section (newest first). This is an append-only
   log — never rewrite or delete existing entries. Set frontmatter `updated:` to today.

Output the entries added and the log path. Note the log feeds `perf-review` (self-review) and
`manager-report` (weekly snippets) — the richest single source for both.
