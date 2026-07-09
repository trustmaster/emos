---
name: 1on1
description: Prepare a 1-on-1 session prep file for a team member — pulls their profile, unresolved carry-over from the last session, recent weekly mentions, and project context. Use when the user asks to prep, prepare, or get ready for a 1-on-1 with someone. Pass the person's name as args.
---

Prepare a 1-on-1 session for the person named in args.

Resolve the person name to a slug using the people map in .agents/config.yaml.

Do the following:

1. Read 02-people/profiles/{slug}.md — note role, level, skill_will, growth_areas, strengths, current_focus.
2. Find the most recent 1-on-1 file in 02-people/one-on-ones/{slug}/ (latest date). Read it and extract:
   - Action items from that session (lines with `- [ ]` or `#follow-up`)
   - Anything marked `#delegate` that hasn't been closed
   - Any stated blockers or concerns
3. Scan all weekly files in 01-weekly/ from the past 4 weeks for mentions of @{FirstName} — note any relevant context (wins, risks, feedback given/received).
4. Check project folders in 03-projects/ (excluding `archive/`) for any projects where this person appears as `owner` or in `team_members` in the hub frontmatter, or is named in items linked to a project via `projects:`.
5. Create a new 1-on-1 prep file at 02-people/one-on-ones/{slug}/YYYY-MM-DD.md using _templates/one-on-one.md as the base. Fill:
   - `person:` slug
   - `date:` today's date
   - `mood:` leave blank (to fill during session)
   - Populate **## Carry-over** with unresolved items from the previous session
   - Populate **## Context** with project and weekly-scan findings
   - Leave **## Discussion** and **## Action Items** blank for the live session

Output a brief summary of what you found and confirm the file was created.
