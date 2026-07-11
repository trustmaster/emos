---
name: prd-new
description: Create a Product Requirements Document (PRD) in a project's docs/ from the prd template. Use when the user wants to write, draft, or start a PRD, product spec, or requirements doc for a feature or initiative. Pass the PRD title and/or its project as args (e.g. "Guest checkout for payments-platform").
---

Create a PRD as a project-local doc.

Read `paths.projects` (default `03-projects`) and `owner.slug` from `.agents/config.yaml`.

1. **Resolve the parent project.** A PRD belongs to a project. If args names a project (or one
   obviously applies from context), use it — validate the slug exists as a folder in
   `{paths.projects}/`. If none is stated, ask which project this PRD is for; if the project
   doesn't exist yet, offer to run `project-new` first.
2. Determine the PRD title from args (the feature/product being specified) and generate a slug
   from it (lowercase, hyphen-separated, max 6 words).
3. Read `_templates/prd.md`.
4. Choose the filename: `{paths.projects}/{project-slug}/docs/prd.md` if the project has no PRD
   yet; otherwise `{paths.projects}/{project-slug}/docs/prd-{feature-slug}.md`. Create the
   `docs/` folder if it doesn't exist.
5. Write the file from the template with frontmatter filled:
   - `title:` from args
   - `slug:` the feature slug
   - `status: draft`
   - `owner:` `{{owner_slug}}` resolved from config
   - `projects:` the parent project slug (this is a human pointer to the parent, not a rollup
     key — the PRD already lives inside the project folder)
   - leave `jira_epic`, `target_date`, `tags` as prompts/empty
   - Keep the section structure as prompts to fill.
6. Add `- [ ] Draft PRD: {title} #follow-up #project/{project-slug}` to the current week's
   active file in `01-weekly/`.

Output the created file path and the parent project. Note that the PRD lives in the project's
`docs/` and is browsable from the project folder.
