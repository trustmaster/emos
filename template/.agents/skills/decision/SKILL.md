---
name: decision
description: Create a new Architecture Decision Record (ADR) with the next sequential number, from the decision-record template. Use when the user wants to record or start a new architectural or technical decision. Pass the decision title as args.
---

Create a new Architecture Decision Record (ADR).

Decision title: the value of args.

1. List files in 04-decisions/ to find the highest existing ADR number (format: NNNN-slug.md). The new ADR number is that + 1, zero-padded to 4 digits.
2. Generate a slug from the title (lowercase, hyphen-separated, max 6 words).
3. Read _templates/decision-record.md.
4. Create 04-decisions/{NNNN}-{slug}.md with:
   - `id: ADR-{NNNN}`
   - `title:` from args
   - `date:` today
   - `status: proposed`
   - `deciders: [{{owner_slug}}]` (resolve `{{owner_slug}}` from `.agents/config.yaml` → `owner.slug`)
   - `projects:` — if args names a project or one clearly applies from context, set `[slug]` (validate the folder exists in 03-projects/); otherwise ask which project(s) this decision belongs to, accepting "none"
   - Leave Context, Decision, Consequences sections as structured prompts to fill
5. Rebuild 04-decisions/_index.md.
6. Add `- [ ] ADR-{NNNN}: {title} — fill decision context #decision` to the current week's active file.
7. If a project was linked, note it will surface in that project's hub on the next `project-sync`.

Output the new ADR file path and the assigned ID.
