---
name: research-new
description: Create a user-research note (interviews, usability test, survey, discovery) in 09-knowledge/research/ from the user-research template. Use when the user wants to plan or capture user research, customer interviews, usability testing, or discovery findings. Pass the study topic and optionally its project as args (e.g. "Onboarding interviews for payments-platform").
---

Create a user-research note in the knowledge base.

Read `paths.knowledge_research` (default `09-knowledge/research`), `paths.projects` (default
`03-projects`), and `owner.slug` from `.agents/config.yaml`.

1. Determine the study topic from args and generate a slug (lowercase, hyphen-separated, max 6
   words).
2. **Resolve project association (optional).** If args names a project (or one obviously
   applies), set `projects: [slug]` — validate each slug exists as a folder in
   `{paths.projects}/`. If none is stated but the topic could belong to an active project, ask
   which project(s) it informs; accept "none". A populated `projects:` makes the note surface
   in those projects' hub rollups under **Knowledge** on the next `project-sync`.
3. Read `_templates/user-research.md`.
4. Create `{paths.knowledge_research}/{YYYY-MM-DD}-{slug}.md` (today's date), creating the
   `{paths.knowledge_research}/` folder if it doesn't exist.
5. Write the file from the template with frontmatter filled:
   - `title:` from args
   - `slug:` the slug
   - `status: planned`
   - `owner:` `{{owner_slug}}` resolved from config
   - `projects:` the resolved slug array (else `[]`)
   - `date:` today's date
   - leave `method`, `participants` as prompts/empty
   - Keep the goal, findings, and insight sections as prompts to fill; preserve the append-only
     `## Raw notes` log.
   - **Do not record PII** — reference participants as P1, P2, … and keep names/contact details
     out of the file (the template says so; enforce it if the user pastes raw contacts).
6. Add `- [ ] Run/synthesize research: {topic} #follow-up{project-tag}` to the current week's
   active file in `01-weekly/`, appending ` #project/{slug}` for each linked project.
7. If any project was linked, offer to run `project-sync {slug}` now.

Output the created file path and any linked project(s).
