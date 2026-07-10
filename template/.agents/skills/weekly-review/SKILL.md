---
name: weekly-review
description: Run the end-of-week review — tally task completion, scan 1-on-1s/projects/incidents for the week, and mark the current weekly file completed with a retrospective. Use when the user wants to close out the current week. No args needed.
---

Run the weekly review for the current week.

1. Find the current active weekly file in 01-weekly/ (status: active).
2. Read it fully. Count:
   - Total tasks
   - Completed tasks (`- [x]`)
   - Open tasks (`- [ ]`)
   - Tasks with `#delegate`, `#blocked`, `#follow-up`
3. Scan all 1-on-1 files created this week (02-people/one-on-ones/*/YYYY-MM-DD.md matching this week's dates). Collect any unresolved action items. *(Skips gracefully for roles that hold few or no 1-on-1s.)*
4. Check project folders in 03-projects/ (excluding `archive/`) — note any that slipped their target date or changed status this week.
5. Check 05-incidents/ — note any incidents opened or status-changed this week.
6. Update the current weekly file:
   - Change `status: active` → `status: completed`
   - Add a `## Weekly Retrospective` section (prepend before any existing sections) with:
     - Completion rate (X/Y tasks done)
     - Key wins (items tagged `#win`)
     - Open items being carried forward
     - Notable observations (max 3 bullet points)
7. Report what you found. Ask if the user wants you to create next week's file now (don't create it unless confirmed).
