# Jira integration adapter

**Capability:** `issue_tracker`
**Provider key:** `jira`  ← value for `config.yaml` → `tools.issue_tracker`
**Status:** `shipped`

## Prerequisites

- Atlassian MCP connected (tools prefixed `mcp__atlassian__`).
- The session user has permission to create/read issues in the project.

## Config

Reads `.agents/config.yaml` → `jira:` block:

| Key | Meaning |
|-----|---------|
| `project_key` | Default project (e.g. `PROJ`). `{KEY}` in skills. |
| `cloud_id` | Atlassian cloud UUID (from `getAccessibleAtlassianResources`). |
| `custom_fields.epic_link` | Per-instance custom field id for epic link. |
| `custom_fields.story_points` | Per-instance custom field id for story points. |

Link base URL: `external.jira` (renders `[{KEY}-123](url)`). Token: `{{jira_browse_url}}`.

## Operations

| Operation | Implemented by | Notes |
|-----------|----------------|-------|
| `create_issue` | skill: `create-jira-ticket` | Draft → confirm → `mcp__atlassian__createJiraIssue`. Assignee resolved via `lookupJiraAccountId`. |
| `sync_iteration` | skill: `jira-sync` | `sprint in openSprints()`; snapshot grouped by status → `10-reports/jira-YYYY-Www.md`. |

## Notes

- Custom field ids are numbered per-instance — the values in `jira.custom_fields`
  are specific to your workspace. Use ids (not display names) in `additional_fields`.
- Story points can save invisibly if the field isn't on the issue type's screen;
  `create-jira-ticket` warns and falls back to a manual reminder.
