---
name: rebuild
description: Regenerate all _index.md dashboard files (weekly, people, projects, decisions, incidents, hiring, strategy) from current content. Use when the user asks to rebuild, refresh, or regenerate the dashboards/indexes. No args needed.
---

Rebuild all dashboard index files from current content.

Read `owner.role` from .agents/config.yaml (default `em`) and open the role pack at
`.agents/roles/{role}.md` for its "Sections in focus / dormant" note. Build **every**
dashboard whose folder has content (they degrade to a minimal placeholder when empty);
order and lead with the role's in-focus sections. A role never removes a dashboard — it
only changes emphasis.

For each of the following dashboards, scan the relevant content files and generate a fresh `_index.md`:

---

### 01-weekly/_index.md
Scan all `01-weekly/YYYY-Www.md` files. Build a table with: Week, Status, completion rate (count `[x]` vs `[ ]`), and any `#blocked` items. Highlight the current `active` week.

### 02-people/_index.md
Scan all `02-people/profiles/*.md`. Build a roster table: Name, Role, Relation, Level, Status. Show the **Skill/Will** rating only for people with `relation: report` (blank otherwise). Note anyone with status other than `active`. Also list 1-on-1 cadence (count files per person in one-on-ones/).

**Teams section — only when `{paths.teams}` (default `02-people/teams`) holds team
files.** Omit the whole section otherwise, so vaults that haven't adopted teams get
byte-identical output to before. When present, add a table above the roster: Team
(linked to its hub), Manager, Status, Headcount (current + open), Active projects,
Last health check. Flag a blank manager or a health check older than two quarters. Do
**not** touch the `<!-- rollup -->` blocks inside team hubs — those belong to `team-sync`.

### 03-projects/_index.md
Scan `03-projects/*/` (each subfolder except `archive/`), read the hub `{slug}.md` file inside. Group by `status` (Active · Proposed · Paused · Completed · Cancelled). For each project list: name (linked to the hub doc), `priority`, `quarter`, and a Jira epic link if `jira_epic` is set. Then scan `03-projects/archive/*/` into a Completed/Archive table. Do **not** touch the `<!-- rollup -->` blocks inside hub docs — those are owned by `project-sync`.

### 04-decisions/_index.md
Scan `04-decisions/*.md`. Build a table: ADR ID, Title, Status, Date, Deciders. Group by status.

### 05-incidents/_index.md
Scan `05-incidents/*.md`. Build a table: Date, Title, Severity, Status, Owner. Sort by date descending. Flag any not yet `reviewed`.

### 06-hiring/_index.md
Scan `06-hiring/positions/*.md` and `interviews/*.md`. Build: open positions table and candidates-in-flight table with stage and recommendation. **If a `06-hiring/headcount-*.md` plan exists**, add a one-line summary of the most recent one (period, filled / open / planned / net) above the tables; omit this line entirely when there is none.

### 07-strategy/_index.md
Scan `07-strategy/okrs/*.md` and `roadmaps/*.md`. Summarize active OKRs with status and key results count. List roadmap files. **If `07-strategy/portfolio.md` or `07-strategy/delegation-register.md` exists**, link each with its `last_reviewed` / `updated` date; omit whichever is absent.

---

After regenerating each file, confirm the path and a one-line summary of what changed. If a directory has no content files, write a minimal placeholder.
