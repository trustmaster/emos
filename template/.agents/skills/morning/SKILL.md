---
name: morning
description: Give a terse morning briefing — open TODOs, blockers/follow-ups, active incidents, upcoming P0/P1 project deadlines, and this week's scheduled 1-on-1s. Use when the user asks for a morning briefing or "what's on my plate today". Optionally pass a date as args.
---

Give a morning briefing for today. Do the following in order:

1. Find the current week's file in 01-weekly/ (today is the date in args, if provided — otherwise use today's date to determine the current ISO week number, e.g. 2026-W15).
2. Read the weekly file and extract:
   - Open TODO items (unchecked `- [ ]`)
   - Any `#blocked` or `#follow-up` items
   - Delegated items (`#delegate`) still pending
3. Check 05-incidents/ for any incidents with status `detected` or `mitigating`.
4. Check project folders in 03-projects/ (excluding `archive/`) for any projects with `priority: P0` or `priority: P1` that have a `target_date` within the next 14 days.
5. Check 02-people/one-on-ones/ for any 1-on-1s scheduled this week (look for files dated this week).

Present the briefing as:

## Morning Briefing — YYYY-MM-DD

### Open TODOs
List each unchecked item with its context.

### Blockers & Follow-ups
List each #blocked and #follow-up item.

### Active Incidents
Any incidents not yet `resolved` or `reviewed`.

### Project Deadlines (next 14 days)
P0/P1 projects approaching their target date.

### 1-on-1s This Week
Who is scheduled, with links to their profile and last session.

Keep it terse — this is a quick scan, not a narrative.
