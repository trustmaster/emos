---
name: roadmap-new
description: Create a product roadmap (Now / Next / Later) in 07-strategy/roadmaps/ from the roadmap template. Use when the user wants to start, draft, or plan a roadmap for a horizon, quarter, or half. Pass the roadmap name/horizon as args (e.g. "Payments H2 2026").
---

Create a roadmap in the strategy area.

Read `paths.roadmaps` (default `07-strategy/roadmaps`), `paths.strategy` (default
`07-strategy`), `owner.slug`, and `context.team` from `.agents/config.yaml`.

1. Determine the roadmap title and horizon from args (e.g. "2026-H2", "2026-Q3", or a themed
   name). Generate a slug (lowercase, hyphen-separated, max 6 words) — prefer a horizon-based
   slug like `2026-h2` when args names a period.
2. Check that no file named `{slug}.md` already exists in `{paths.roadmaps}/` (offer to open it
   instead of overwriting). Create the `{paths.roadmaps}/` folder if it doesn't exist.
3. Read `_templates/roadmap.md`.
4. Write `{paths.roadmaps}/{slug}.md` from the template with frontmatter filled:
   - `title:` from args
   - `slug:` the slug
   - `status: active`
   - `owner:` `{{owner_slug}}` resolved from config
   - `team:` `{{team}}` resolved from config
   - `horizon:` the parsed horizon (else leave as a prompt)
   - `last_reviewed:` today's date
   - `projects:` if args or context clearly names initiatives that map to existing project
     slugs, set them as an array (validate each exists in `paths.projects`); otherwise leave
     `[]`. A populated `projects:` makes the roadmap surface in those projects' hub rollups
     under **Strategy** on the next `project-sync`.
   - Keep the Now / Next / Later tables as prompts to fill; preserve the append-only
     `## Revision log`.
5. Rebuild `{paths.strategy}/_index.md`.
6. Add `- [ ] Fill in roadmap: {title} #follow-up` to the current week's active file in
   `01-weekly/`.

Output the created file path. If `projects:` was set, note it will surface in those hubs on the
next `project-sync`.
