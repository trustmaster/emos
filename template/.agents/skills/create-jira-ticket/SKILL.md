---
name: create-jira-ticket
description: Create a new Jira ticket in your workspace following the project's standard format — gathers the details, shows a draft for confirmation, then creates it via MCP. Use when the user wants to file, open, or create a Jira ticket or issue. Optionally pass the ticket summary as args.
---

# Create JIRA Ticket Skill

> **Provider skill** for the `issue_tracker` capability (`jira`) — the `create_issue` operation. Active when `config.yaml` → `tools.issue_tracker: jira`. Adapter: [.agents/integrations/jira.md](../../integrations/jira.md).

This skill helps you create JIRA tickets directly in Jira using MCP integration.

Read Jira settings from `.agents/config.yaml` → `jira:`:
`project_key` (default project), `cloud_id`, and `custom_fields` (`epic_link`, `story_points`).
`{KEY}` below = `jira.project_key`.

## When to use this skill

Use this skill when you need to create a new JIRA ticket in your Jira workspace following the project's
standard format.

## Instructions

When the user invokes this skill:

1. **Gather required information** by asking the user:

   - Ticket title/summary
   - Ticket description: What is the background and why is this work needed?
   - Project key (default: `jira.project_key`)
   - Issue type (default: Task)
   - Epic link (optional — ask for epic name or key)

2. **Show a markdown draft** of the ticket to the user before creating it:

   - Display the full formatted description as it will appear in Jira
   - Include title, assignee, epic, and all sections
   - Wait for the user to confirm ("looks good", "create it") or request changes before proceeding

3. **Create the Jira ticket** using the MCP integration only after confirmation:

   - Use `mcp__atlassian__createJiraIssue` with cloudId from `jira.cloud_id`
   - Project key: default `jira.project_key`; use another if the user specifies one
   - Issue type: Typically "Task" or "Story" (ask user if unclear)
   - Assignee: default to the current session user. Resolve their account ID via `mcp__atlassian__lookupJiraAccountId`
     using the user's email (available in session context) as `searchString`, then pass the returned account ID as
     `assignee_account_id`. Only fall back to asking the user for a name/email if no session email is available or the
     lookup returns no match. Use a different assignee if the user specifies one.
   - Epic: link via `additional_fields: {"<jira.custom_fields.epic_link>": "EPIC-KEY"}` if provided and configured
   - Story points: only set via `jira.custom_fields.story_points` if that field is on the issue type's screen for your
     project. If unsure, don't set it via the API (it can save invisibly) — see "After creating the ticket" below.
   - Format the description following the template below

4. **Description template** for Jira ticket:

```markdown
## Context

[Background information explaining why this work is needed, what problem it solves, and how it fits into the broader
project goals]

## Acceptance Criteria

1. [One short line per criterion — no explanations]
2. [Second criterion]
3. [Third criterion]

## TODO

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

## Deliverables

- [ ] [Artifact name] — [brief description]
- [ ] [Artifact name] — [brief description]
```

5. **After creating the ticket**:

   - Display the ticket URL and key to the user
   - Confirm the ticket was created successfully
   - If story points could not be set via the API, remind the user to set them manually in the Jira UI.

6. **Follow project conventions**:
   - Acceptance criteria: one short line each, no explanation — just the measurable outcome
   - Deliverables: checkboxes only, no prose
   - Break down TODO items into specific, measurable tasks

## Example usage

User: "Create a JIRA ticket for the replacement analysis"

Assistant should:

1. Ask for project key (default `jira.project_key`), context, acceptance criteria, TODO items, deliverables, and epic
2. Show a markdown draft and wait for user confirmation
3. Create the ticket in Jira using MCP with the current session user as default assignee (resolved via
   `lookupJiraAccountId`)
4. Return the ticket URL and key (e.g., `{KEY}-2049`), and remind the user to set story points manually if needed

## Notes

- Keep ticket descriptions focused and concise
- Jira custom field IDs are numbered per-instance, so the values in `jira.custom_fields` are specific to your workspace.
  Use the IDs (not the human-readable names) in `additional_fields`.

## Post-creation patching pattern

When the ticket description references its own ticket key (e.g., storage paths like `.../{KEY}-XXXX/...`), the
key is unknown until creation. The pattern is:

1. Create the ticket with a placeholder (`{KEY}-XXXX`) in the description.
2. Read the assigned key from the create response.
3. Immediately call `mcp__atlassian__editJiraIssue` to replace the placeholder with the real key.

This keeps any key-derived paths searchable by ticket key alone.
