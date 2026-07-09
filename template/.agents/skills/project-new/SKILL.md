---
name: project-new
description: Create a new project folder and hub doc from the project-tracker template, with a docs/ subfolder for working files, and add a follow-up TODO to the current week. Use when the user wants to start tracking a new project or initiative in emOS. Pass the project title as args.
---

Create a new project folder with its hub doc.

Project title: the value of args.

Read `paths.projects` (default `03-projects`) and `owner.slug` from `.agents/config.yaml`.

1. Generate a slug from the title (lowercase, hyphen-separated, max 6 words).
2. Check that no folder named `{slug}` already exists in `{paths.projects}/`.
3. Read `_templates/project-tracker.md`.
4. Create the folder `{paths.projects}/{slug}/` and an empty `{paths.projects}/{slug}/docs/` subfolder (for project-local working docs, drafts, research — add a `.gitkeep` if the tool needs a file to track the empty dir).
5. Create `{paths.projects}/{slug}/{slug}.md` from the template with frontmatter filled:
   - `title:` from args
   - `slug:` the slug
   - `status: active`
   - `priority:` ask or default `P2`
   - `owner:` `{{owner_slug}}` resolved from config
   - `started:` today's date
   - leave `quarter`, `team_members`, `jira_epic`, `confluence`, `target_date`, `tags` as prompts/empty
   - **keep the `<!-- rollup:start -->…<!-- rollup:end -->` block intact** — it stays empty until content links to the project.
6. Add `- [ ] Set up project: {title} #follow-up #project/{slug}` to the current week's active file in `01-weekly/`.
7. Rebuild `{paths.projects}/_index.md`.

Output the created folder path and hub doc path.
