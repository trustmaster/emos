---
name: perf-review
description: Gather evidence and draft a narrative for a performance review from 1-on-1s, weekly mentions, projects, and incidents — without inventing ratings. Use when the user wants to prepare or update a performance review for a team member. Pass the person's name as args.
---

Prepare a performance review for the person named in args.

Resolve the person name to a slug using .agents/config.yaml.

This is an evidence-gathering and narrative-drafting workflow. Do NOT make up ratings — surface evidence and let the manager (`.agents/config.yaml` → `owner.name`) draw conclusions.

1. Read 02-people/profiles/{slug}.md — note role, level, growth_areas, strengths, current cycle expectations.
2. Determine the current review cycle from context (check 02-people/reviews/ for existing cycle directories). Use the most recent incomplete cycle.
3. Read all 1-on-1 files for this person in 02-people/one-on-ones/{slug}/ from the review period. Extract:
   - Feedback given (look for `#feedback`)
   - Wins mentioned (`#win`)
   - Concerns or risks (`#risk`, `#blocked`)
   - Growth progress on stated `growth_areas`
4. Scan weekly files in 01-weekly/ for all mentions of @{FirstName}. Note patterns (frequency of mentions, type: praise, concern, delegation, escalation).
5. Check 03-projects/ for projects this person owned or contributed to: match `{slug}` in each hub's `owner`/`team_members`, plus any project whose linked items (files carrying `projects:`) name this person. Note outcomes.
6. Check 05-incidents/ for any incidents this person was involved in (owner or contributor) — note their response.
7. Check if a review file already exists at 02-people/reviews/{cycle}/{slug}.md. If not, create it from _templates/performance-review.md with:
   - `person:` slug
   - `cycle:` current cycle name
   - `status: draft`
8. Populate or append to the review file:
   - **## Evidence Log** — bulleted list of raw evidence per source (1-on-1s, weeklies, projects, incidents), each with date and source file reference
   - **## Competency Notes** — brief notes per standard EM competency dimension: Delivery, Technical, People, Communication, Growth
   - **## Draft Narrative** — 3–5 sentences summarizing the period, highlighting standout moments

Output a summary of evidence found and confirm the file path.
