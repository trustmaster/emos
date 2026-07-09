---
name: meeting-new
description: Create a dated meeting note from the meeting-notes template, linked to a project. Use when the user wants to capture or start notes for a meeting, sync, or call. Pass the meeting title as args (optionally with a project, e.g. "Planning sync for gcp-cost-optimization").
---

Create a meeting note for the meeting described in args.

Read `paths.meetings` (default `08-meetings`) and `paths.projects` (default `03-projects`) from `.agents/config.yaml`.

1. Determine today's date (or the meeting date if stated in args).
2. Generate a slug from the meeting title (lowercase, hyphen-separated, max 6 words).
3. Read `_templates/meeting-notes.md`.
4. **Resolve project association.** If args names a project (or one obviously applies from context), set `projects: [slug]` — validate each slug exists as a folder in `{paths.projects}/`. If none is stated and the topic could belong to an active project, ask which project(s) it relates to; accept "none".
5. Create `{paths.meetings}/YYYY-MM-DD-{slug}.md` from the template with:
   - `title:` from args
   - `date:` the meeting date
   - `attendees:` any names parsed from args (else empty)
   - `projects:` the resolved slug array (else empty)
6. If any project was linked, note that it will surface in that project's hub on the next `project-sync` — offer to run `project-sync {slug}` now.

Output the created file path and the linked project(s).
