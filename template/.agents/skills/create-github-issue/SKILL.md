---
name: create-github-issue
description: Create a new GitHub issue (optionally added to a GitHub Project board) following the project's standard format — gathers the details, shows a draft for confirmation, then creates it via the `gh` CLI. Use when the user wants to file, open, or create a GitHub issue. Optionally pass the repo and/or issue title as args.
---

# Create GitHub Issue Skill

> **Provider skill** for the `issue_tracker` capability (`github`) — the `create_issue` operation. Active when `config.yaml` → `tools.issue_tracker: github`. Adapter: [.agents/integrations/github.md](../../integrations/github.md).

Create a GitHub issue directly via the `gh` CLI, following the project's standard format.

Read GitHub settings from `.agents/config.yaml` → `github:`:
`project` (optional default GitHub Project — number or URL) and `external.github` for link URLs.
**The repository is provided per-invocation, not from config** — you work across many repos and
orgs, so a single configured repo would be wrong more often than right.

## Prerequisites

- `gh` CLI installed and authenticated. Verify with `gh auth status`; if it fails, tell the user
  to run `gh auth login` and stop.

## When to use this skill

Use this skill to create a new GitHub issue in a repository, optionally adding it to a team's
GitHub Project board.

## Instructions

When the user invokes this skill:

1. **Resolve the repository** (`owner/repo`), in this order:

   - An explicit `owner/repo` (or a GitHub repo URL) in args or the request.
   - Otherwise, `gh`'s detection of the current directory's repo — confirm it with the user:
     `gh repo view --json nameWithOwner -q .nameWithOwner`.
   - If neither resolves, **ask** which repo. Never guess.

2. **Gather required information** by asking the user (skip anything already given):

   - Issue title/summary
   - Context/description: background and why this work is needed
   - Labels (optional — must already exist in the target repo)
   - Assignee (optional — default `@me`, i.e. the current `gh` user; use another if specified)
   - Project board (optional — default to `github.project` if set; accept a title/number/URL,
     or "none")

3. **Show a markdown draft** of the issue to the user before creating it:

   - Display the full formatted body as it will appear on GitHub, plus the target repo, labels,
     assignee, and project.
   - Wait for the user to confirm ("looks good", "create it") or request changes before proceeding.

4. **Body template** for the issue:

```markdown
## Context

[Background explaining why this work is needed, what problem it solves, and how it fits into the
broader goals]

## Acceptance Criteria

1. [One short line per criterion — no explanations]
2. [Second criterion]
3. [Third criterion]

## Tasks

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]
```

5. **Create the issue** with `gh`, only after confirmation. Pass the body on stdin (`-F -`) to
   avoid shell-escaping problems with multi-line Markdown:

   ```bash
   gh issue create --repo <owner/repo> --title "<title>" -F - \
     [--label "<label>"] [--assignee "<login|@me>"] <<'BODY'
   ## Context
   …
   BODY
   ```

   - Capture the printed issue **URL** from the command output.

6. **Add to a Project board**, if one applies (from args, or the `github.project` default):

   - If it's a **title** that the repo/org exposes, the simplest path is to include
     `--project "<title>"` on the `gh issue create` call in step 5.
   - If it's a **number/URL** (typical for org-level Projects v2), add after creation:
     ```bash
     gh project item-add <number> --owner <owner> --url <issue-url>
     ```
     `<owner>` is the project owner (the org or user), which may differ from the repo owner —
     ask if ambiguous. Use `--owner @me` for a personal project.
   - If the project add fails (e.g. permissions, wrong owner), report the error and leave the
     issue created — don't roll back.

7. **After creating the issue**:

   - Display the issue **URL and number** to the user (e.g. `#128`).
   - Confirm whether the Project add succeeded, or that it was skipped.

8. **Follow project conventions**:
   - Acceptance criteria: one short line each, no explanation — just the measurable outcome
   - Tasks: checkboxes only, no prose
   - Break tasks into specific, measurable items

## Example usage

User: "Create a GitHub issue in acme/checkout for the idempotency retry bug"

Assistant should:

1. Resolve repo `acme/checkout` (from args).
2. Ask for context, acceptance criteria, tasks, labels, assignee, and project (default
   `github.project`).
3. Show a markdown draft and wait for confirmation.
4. Create with `gh issue create --repo acme/checkout …`, defaulting the assignee to `@me`.
5. Add to the default Project board if `github.project` is set.
6. Return the issue URL and number.

## Notes

- Labels and milestones must already exist in the **target** repo — `gh` errors on unknown
  names. If unsure, list them first (`gh label list --repo <owner/repo>`) or omit.
- A Project board's owner is often the **org**, not the repo — `gh project item-add` needs the
  project `--owner`, not the repo owner.
- This skill never stores credentials; `gh` manages its own auth.
