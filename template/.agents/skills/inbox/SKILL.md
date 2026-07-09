---
name: inbox
description: Process one item from 00-inbox/ — classify its contents (action, project-seed, person-note, decision-point, knowledge, meeting-note, incident-signal, hiring-note, unclear), recommend where each piece should go, and wait for confirmation before moving or deleting anything. Use when the user wants to triage inbox items. Optionally pass a filename or search term as args to target a specific item.
---

Process the next item in the inbox.

If args is provided, treat it as a specific filename or search term to target in 00-inbox/. Otherwise, find the oldest item (by name, which sorts chronologically for dated files).

---

## Step 1 — Find the item

List everything in 00-inbox/ excluding hidden files and the _done/ subdirectory.
- If the inbox is empty, say so and stop.
- If args is given, match it. If no match, say so and stop.
- Otherwise, take the **oldest item** (first alphabetically — dated files sort naturally).

## Step 2 — Read the item

Read the full content of the file. If it is a directory, read all .md files inside it.

## Step 3 — Classify each entry

Go line by line (or block by block for longer content). Assign each a type:

| Type | What it looks like |
|------|--------------------|
| **action** | Task, TODO, follow-up that needs doing |
| **project-seed** | A project idea or initiative without a tracker yet |
| **person-note** | Something about a team member (feedback, observation, FYI) |
| **decision-point** | A choice to be made or recorded |
| **knowledge** | Reference info, how-something-works, a framework, a link to save |
| **meeting-note** | Notes from a conversation or meeting |
| **incident-signal** | A reliability concern, near-miss, or ongoing issue |
| **hiring-note** | Candidate or pipeline related |
| **unclear** | Can't classify — flag for human judgment |

## Step 4 — Output the analysis

Present the findings as:

### Inbox Item: {filename}
> {first line or title of the content}

#### Classified Items
For each classified entry, one line:
`[TYPE] {brief description} → {resolution}`

Where `{resolution}` is one of:
- `add to weekly TODO` — for action items → suggest the exact `- [ ]` line to add
- `create tracked issue` — for an action that belongs in the issue tracker → resolve the provider from `.agents/config.yaml` → `tools.issue_tracker`, then follow its adapter in `.agents/integrations/{provider}.md` (`create_issue` operation; e.g. `jira` → `create-jira-ticket`). If `tools.issue_tracker: none`, skip this option and use the weekly TODO instead.
- `/project-new {title}` — for project seeds
- `/decision {title}` — for decision points
- `/incident {description}` — for incident signals
- `/1on1 {Person}` — for person-notes (add to their next 1-on-1 carry-over)
- `move to 09-knowledge/{subfolder}/` — for knowledge entries
- `move to 08-meetings/` — for meeting notes
- `move to 06-hiring/` — for hiring notes
- `needs your input` — for unclear items

#### Project association
For each item, detect whether it belongs to an active project in `03-projects/` (match on the project title, slug, or an obvious topic overlap). When it does, note the `{slug}`. This drives the wiring in the recommended actions below.

#### Recommended Actions
Numbered list of concrete next steps, most important first. For each action you can take directly (adding a TODO to weekly, updating a 1-on-1 carry-over), state what you will do and ask for confirmation before doing it.

When an item is linked to a project, wire it as you route it:
- files routed to a type folder (meetings, decisions, incidents, knowledge, reports) get `projects: [slug]` in their frontmatter;
- TODO lines added to the weekly file get a trailing `#project/{slug}` tag.
Then it surfaces in that project's hub on the next `project-sync`.

#### What to do with this inbox item after processing?
> Options:
> 1. Archive it — move to `00-inbox/_done/{filename}`
> 2. Delete it — remove the file
> 3. Keep it — leave in inbox (only if partially unresolved)
>
> State your recommendation and wait for the user's decision before moving/deleting anything.

---

Do not execute any file moves, deletions, or content changes until the user confirms. The analysis and recommendations are the output of this command. Act only on what is explicitly approved.
