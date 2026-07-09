---
name: jira-sync
description: Sync the current Jira sprint into an emOS report grouped by status. Use when the user wants an up-to-date sprint snapshot pulled from Jira into 10-reports/. Optionally pass a JQL filter or sprint name as args.
---

> **Provider skill** for the `issue_tracker` capability (`jira`) — the `sync_iteration` operation. Active when `config.yaml` → `tools.issue_tracker: jira`. Adapter: [.agents/integrations/jira.md](../../integrations/jira.md).

Sync the current sprint from Jira into emOS.

Read Jira settings from `.agents/config.yaml` → `jira:` (`project_key`, `cloud_id`) and `external.jira` for link URLs. `{KEY}` below = `jira.project_key`.

Arguments (args, optional): a JQL filter override or sprint name. Default: current open sprint.

1. Determine today's date and current ISO week (e.g. 2026-W23).
2. Query Jira using the Atlassian MCP (cloudId from `jira.cloud_id`):
   - JQL: `project = {KEY} AND sprint in openSprints() ORDER BY status ASC, priority ASC`
   - Fields to fetch: summary, status, assignee, priority, issuetype, labels, story points if available.
3. Group tickets by status: `To Do`, `In Progress`, `In Review`, `Done`.
4. Build a sprint snapshot markdown and save it to `10-reports/jira-YYYY-Www.md`:

```
---
type: jira-sprint-snapshot
week: YYYY-Www
date: YYYY-MM-DD
project: {KEY}
projects: []            # emOS project slugs whose jira_epic appears in this sprint (see step 4a)
---

## Sprint Snapshot — YYYY-Www

### In Progress
- [{KEY}-XXX](url) — Summary — @Assignee

### In Review
- [{KEY}-XXX](url) — Summary — @Assignee

### To Do
- [{KEY}-XXX](url) — Summary — @Assignee

### Done this sprint
- [{KEY}-XXX](url) — Summary — @Assignee

## Stats
- Total: N | Done: N | In Progress: N | To Do: N
```

4a. **Link to emOS projects.** Read the hub docs in `03-projects/*/` and collect their `jira_epic` values. For any synced ticket whose epic (or key) matches a project's `jira_epic`, add that project's `{slug}` to the report's `projects:` frontmatter array, and append a trailing `#project/{slug}` to that ticket's line. The sprint snapshot then surfaces in the linked projects' hubs on the next `project-sync`.
5. If a report for this week already exists, overwrite it.
6. Report: file path saved, ticket counts per status, linked project slugs, any blocked or flagged tickets.
