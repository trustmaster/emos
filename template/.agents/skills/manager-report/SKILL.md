---
name: manager-report
description: Draft and save your weekly status / async report by synthesizing the current weekly file, this week's 1-on-1s (if any), active projects, and incidents — formatted for your role (manager async, IC snippets, PM product status, or director portfolio update). Use when the user needs to write their weekly status update. No args needed.
---

Draft and save the weekly status report for the current week, formatted for your role.

**Resolve role first:** read `owner.role` from .agents/config.yaml (default `em`) and open
the role pack at `.agents/roles/{role}.md`. Take `{{role_report_slug}}`, `{{role_report_title}}`,
`{{status_report_audience}}`, and the manager-report skill note from the pack.

1. Determine today's ISO week (e.g. 2026-W23). Find `01-weekly/YYYY-Www.md` — it may be `status: active` or `status: completed`. Read it fully.
2. Read `_templates/manager-async.md`.
3. Scan this week's 1-on-1 files in `02-people/one-on-ones/*/` — any file whose date falls within the current ISO week. Collect mood signals, shout-outs, and action items. *(Skip or de-emphasize for roles without reports — see the pack note; ICs/PMs lead with their own accomplishments instead.)*
4. Scan project folders in `03-projects/` (excluding `archive/`) — note milestone status changes, blockers, or cross-team dependencies mentioned this week. Use the `projects:` join key and `#project/{slug}` tags to attribute this week's work (weekly TODOs, meetings, decisions, incidents) to specific projects, so **Delivery & Execution can be grouped by project** rather than as a flat list.
5. Check `05-incidents/` for any incidents opened or status-changed this week.
6. Draft `10-reports/YYYY-Www-{{role_report_slug}}.md` (e.g. `-manager-async` for em, `-snippets` for ic) using the template, with the H1 title `{{role_report_title}}`. Populate each section from the sources above, in the voice of the pack's audience (`{{status_report_audience}}`):
   - **TL;DR**: 2-3 sentences synthesizing the week and the one thing needing the reader's attention.
   - **Sentiment / Highlights**: for roles with reports, team mood signals from 1-on-1s; for ICs/PMs, your own `#win` items and shipped highlights.
   - **Delivery & Execution**: completed tasks / milestones for "What Went Well"; `#blocked` and `#risk` items for Risks; `#delegate` or deferred tasks for Deprioritized; project status for Milestone Outlook.
   - **Insights & Patterns**: observations or learnings noted in weekly Notes section.
   - **Looking Ahead**: the weekly file's "Next week" section for Focus; any open escalations or asks for the reader.
7. For any section you cannot fill from available sources, leave the placeholder text intact and append `⚠️ needs input` on the same line.
8. Save the file. Set `week:` and `date:` in frontmatter to the current ISO week and today's date.
9. Report:
   - File path created.
   - Which sections were auto-filled vs. need manual input (⚠️ lines).
   - Anything notable found during the scan (open blockers, at-risk milestones, unresolved escalations).
