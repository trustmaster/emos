---
name: experiment-new
description: Create an experiment / A-B test brief in a project's docs/experiments/ from the experiment template. Use when the user wants to design, plan, or start an experiment, A/B test, or growth test. Pass the experiment name and/or its project as args (e.g. "One-tap reorder test for payments-platform").
---

Create an experiment brief as a project-local doc.

Read `paths.projects` (default `03-projects`) and `owner.slug` from `.agents/config.yaml`.

**Resolve voice:** read `agent.voice` from `.agents/config.yaml`. If it's set and the file
exists, read it (plus `samples/` alongside it) and match its register in the file you write.
Apply it to the artifact only — never to your chat reply or progress narration. If the key is
absent, write plainly and say nothing; if it's set but the file is missing, say so once and
write plainly.

1. **Resolve the parent project.** If args names a project (or one obviously applies from
   context), use it — validate the slug exists as a folder in `{paths.projects}/`. If none is
   stated, ask which project this experiment belongs to; accept "none" only if the user
   insists (then place it under the closest project or ask them to create one).
2. Determine the experiment name from args and generate a slug (lowercase, hyphen-separated,
   max 6 words).
3. Read `_templates/experiment.md`.
4. Create `{paths.projects}/{project-slug}/docs/experiments/{experiment-slug}.md`, creating the
   `docs/experiments/` folder if it doesn't exist.
5. Write the file from the template with frontmatter filled:
   - `title:` from args
   - `slug:` the experiment slug
   - `status: proposed`
   - `owner:` `{{owner_slug}}` resolved from config
   - `projects:` the parent project slug (human pointer to the parent, not a rollup key)
   - leave `metric`, `started`, `ended` as prompts/empty
   - Keep the Hypothesis, Metrics, Variants, and sizing sections as prompts to fill. Preserve
     the append-only `## Results` log.
6. Add `- [ ] Set up experiment: {name} #follow-up #project/{project-slug}` to the current
   week's active file in `01-weekly/`.

Output the created file path and the parent project.
