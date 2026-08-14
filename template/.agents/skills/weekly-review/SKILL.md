---
name: weekly-review
description: Run the end-of-week review — tally task completion, scan 1-on-1s/projects/incidents for the week, and mark the current weekly file completed with a retrospective. Use when the user wants to close out the current week. No args needed.
---

Run the weekly review for the current week.

**Resolve voice:** read `agent.voice` from `.agents/config.yaml`. If it's set and the file
exists, read it (plus `samples/` alongside it) and match its register in the file you write.
Apply it to the artifact only — never to your chat reply or progress narration. If the key is
absent, write plainly and say nothing; if it's set but the file is missing, say so once and
write plainly.

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
