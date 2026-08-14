---
name: staff-meeting
description: Create the next note in your recurring leadership-team (staff) meeting series, carrying forward open actions and parked topics from the previous session, with a standing agenda and per-team status pulled from the vault. For anyone running a recurring meeting with their leadership team or leads. Use when the user wants to prep, start, or write up their staff meeting or leadership sync. No args needed; pass a date to target a specific session.
roles: [director]
---

Create the next note in the recurring staff-meeting series. Unlike `meeting-new` (which
creates a standalone note), this one **carries forward** — the value is in the continuity.

Read `paths.meetings` (default `08-meetings`), `paths.teams` (default
`02-people/teams`), `paths.reports` (default `10-reports`), `people:`, and `owner.role`
from `.agents/config.yaml`.

**Resolve voice:** read `agent.voice` from `.agents/config.yaml`. If it's set and the file
exists, read it (plus `samples/` alongside it) and match its register in the file you write.
Apply it to the artifact only — never to your chat reply or progress narration. If the key is
absent, write plainly and say nothing; if it's set but the file is missing, say so once and
write plainly.

## Step 1 — Find the series

Look in `{paths.meetings}/` for the most recent file with `series: staff` in
frontmatter (filenames look like `YYYY-MM-DD-staff.md`). That's the previous session.
If there is none, this is the first one — say so and skip step 2's carry-over.

## Step 2 — Carry forward from the previous session

From the previous file, collect:

- **Open action items** — unchecked `- [ ]` lines from its Action Items and Carry-over
  sections. Keep the original owner and the date they were first raised, so age is
  visible. Anything older than three sessions gets flagged in the report — it's either
  not real or not owned.
- **Parked topics** whose return date has arrived or passed.
- **Decisions** recorded but not yet marked communicated.

## Step 3 — Assemble this session's context

- **Per team** — for each hub in `{paths.teams}/`: current health rating, its newest
  health-log line, active projects at risk, and open incidents. One line per team; this
  is the "around the room" prompt, not a substitute for it.
- **Delivery** — projects in `03-projects/` with `#risk`, `#blocked`, or a slipped
  `target_date`.
- **People** — open reqs from `06-hiring/positions/`, anyone `departing`, and the newest
  headcount plan's asks.
- **Escalations** — open items in `{paths.reports}/escalations/` and `#escalate` tags
  from the last two weeks of `01-weekly/`.
- **Decisions needing the room** — ADRs in `04-decisions/` with `status: proposed`.

If `{paths.teams}/` is empty, fall back to project- and incident-level context and
mention that `/team-new` would sharpen this.

## Step 4 — Write the file

Create `{paths.meetings}/YYYY-MM-DD-staff.md` (today, or the date in args) from
`_templates/staff-meeting.md`:

- `series: staff`, `date:`, `attendees:` (your managers — profiles with
  `relation: report`), `teams:` (all synced teams).
- **Carry-over** — the items from step 2, each with its original date.
- **This week's topics** — pre-fill rows from step 3 for anything that genuinely needs
  the room, each with an owner and a purpose (`decide` / `discuss` / `inform`). Leave the
  table open for people to add to; don't pad it.
- Leave **Notes**, **Decisions** and **Action Items** empty for the live session.

If a file already exists for that date, don't overwrite it — open it, refresh only the
**Carry-over** section, and say what you refreshed.

## Step 5 — Report

- File path, and how many actions carried forward.
- **Stale actions** — anything open across three or more sessions, with its owner. Say it
  plainly; this is the main thing the series is for.
- The suggested agenda items and why each made the list.
- Anything you found that needs a decision but has no owner.
