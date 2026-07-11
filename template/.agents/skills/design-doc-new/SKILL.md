---
name: design-doc-new
description: Create a technical design doc / RFC in a project's docs/ from the design-doc template. Use when the user wants to write, draft, or start a design doc, RFC, technical design, tech spec, or engineering proposal for how to build something — "RFC" and "design doc" mean the same artifact here. Pass the title and/or its project as args (e.g. "Idempotent retries for payments-platform").
---

Create a technical design doc (a.k.a. RFC) as a project-local doc. This is the engineering
**how** — distinct from a PRD (the product **what/why**) and heavier than an ADR (which records
a single decision). A design doc often *produces* ADRs; capture those with `/decision`.

Read `paths.projects` (default `03-projects`) and `owner.slug` from `.agents/config.yaml`.

1. **Resolve the parent project.** A design doc belongs to a project. If args names a project
   (or one obviously applies from context), use it — validate the slug exists as a folder in
   `{paths.projects}/`. If none is stated, ask which project this design is for; if the project
   doesn't exist yet, offer to run `project-new` first.
2. Determine the design title from args (the system/feature being designed) and generate a slug
   from it (lowercase, hyphen-separated, max 6 words).
3. Read `_templates/design-doc.md`.
4. Choose the filename: `{paths.projects}/{project-slug}/docs/design-doc.md` if the project has
   no design doc yet; otherwise `{paths.projects}/{project-slug}/docs/design-doc-{feature-slug}.md`.
   Create the `docs/` folder if it doesn't exist.
5. Write the file from the template with frontmatter filled:
   - `title:` from args
   - `slug:` the feature slug
   - `status: draft`
   - `owner:` `{{owner_slug}}` resolved from config
   - `projects:` the parent project slug (a human pointer to the parent, not a rollup key — the
     doc already lives inside the project folder)
   - leave `reviewers`, `jira_epic`, `target_date`, `supersedes`, `tags` as prompts/empty
   - Keep the section structure as prompts to fill.
6. If a PRD already exists in the same `docs/` (`prd.md`), reference it in the Appendix so the
   **what/why** and the **how** cross-link.
7. Add `- [ ] Draft design doc: {title} #follow-up #project/{project-slug}` to the current week's
   active file in `01-weekly/`.

Output the created file path and the parent project. Note that the design doc lives in the
project's `docs/` (browsable there), and that decisions resolved in it should be recorded as
ADRs via `/decision` linked with `projects: [{project-slug}]`.
