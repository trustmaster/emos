---
name: incident
description: Start a new incident post-mortem file with inferred severity and a weekly TODO follow-up. Use when the user reports an incident or outage, or wants to start a post-mortem. Pass the incident description as args.
---

Start a new incident post-mortem.

Incident description: the value of args.

1. Determine today's date for the filename.
2. Generate a slug from the description (lowercase, hyphen-separated, max 5 words).
3. Find the next available incident — check 05-incidents/ to understand existing incidents for context.
4. Read _templates/incident-postmortem.md.
5. Create 05-incidents/YYYY-MM-DD-{slug}.md with:
   - `title:` from the description
   - `date:` today
   - `status: detected`
   - `severity:` — infer from description: P0 if "down/outage/critical", P1 if "degraded/elevated", P2 otherwise. Note the assumption.
   - `owner: {{owner_slug}}` (resolve `{{owner_slug}}` from `.agents/config.yaml` → `owner.slug`; can be changed)
   - `impact:` — leave placeholders for users_affected, business_impact, scope to fill
   - `projects:` — if the incident clearly relates to an active project (e.g. a rollout, a service the project owns), set `[slug]` (validate against 03-projects/); otherwise ask, accepting "none"
   - `timeline:` — add one entry: `YYYY-MM-DD HH:MM — Incident detected: {description}`
   - Leave all analysis sections (root cause, contributing factors, action items) as prompts to fill
6. Add a `- [ ] Incident: {title} #follow-up` TODO to the current week's active file in 01-weekly/. If a project was linked, append ` #project/{slug}` to that TODO line.
7. Rebuild 05-incidents/_index.md.

Output the file path created and the initial frontmatter filled.
