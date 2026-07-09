---
name: rebuild
description: Regenerate all _index.md dashboard files (weekly, people, projects, decisions, incidents, hiring, strategy) from current content. Use when the user asks to rebuild, refresh, or regenerate the dashboards/indexes. No args needed.
---

Rebuild all dashboard index files from current content.

For each of the following dashboards, scan the relevant content files and generate a fresh `_index.md`:

---

### 01-weekly/_index.md
Scan all `01-weekly/YYYY-Www.md` files. Build a table with: Week, Status, completion rate (count `[x]` vs `[ ]`), and any `#blocked` items. Highlight the current `active` week.

### 02-people/_index.md
Scan all `02-people/profiles/*.md`. Build a roster table: Name, Role, Level, Skill/Will rating, Status. Note anyone with status other than `active`. Also list 1-on-1 cadence (count files per person in one-on-ones/).

### 03-projects/_index.md
Scan `03-projects/*/` (each subfolder except `archive/`), read the hub `{slug}.md` file inside. Group by `status` (Active · Proposed · Paused · Completed · Cancelled). For each project list: name (linked to the hub doc), `priority`, `quarter`, and a Jira epic link if `jira_epic` is set. Then scan `03-projects/archive/*/` into a Completed/Archive table. Do **not** touch the `<!-- rollup -->` blocks inside hub docs — those are owned by `project-sync`.

### 04-decisions/_index.md
Scan `04-decisions/*.md`. Build a table: ADR ID, Title, Status, Date, Deciders. Group by status.

### 05-incidents/_index.md
Scan `05-incidents/*.md`. Build a table: Date, Title, Severity, Status, Owner. Sort by date descending. Flag any not yet `reviewed`.

### 06-hiring/_index.md
Scan `06-hiring/positions/*.md` and `interviews/*.md`. Build: open positions table and candidates-in-flight table with stage and recommendation.

### 07-strategy/_index.md
Scan `07-strategy/okrs/*.md` and `roadmaps/*.md`. Summarize active OKRs with status and key results count. List roadmap files.

---

After regenerating each file, confirm the path and a one-line summary of what changed. If a directory has no content files, write a minimal placeholder.
