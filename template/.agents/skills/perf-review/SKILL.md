---
name: perf-review
description: Gather evidence and draft a review narrative — a self-review / brag-doc for yourself, or a review of someone else — from 1-on-1s, weekly mentions, projects, and incidents, without inventing ratings. Use when the user wants to prepare or update a performance review or self-review. Pass the person's name as args, or none for a self-review.
---

Prepare a performance review. The **subject** is the person named in args; with no args,
the subject is the vault owner (a self-review / brag-doc).

**Resolve role first:** read `owner.role` from .agents/config.yaml (default `em`) and open
the role pack at `.agents/roles/{role}.md`. Use its `{{review_dimensions}}` and perf-review
skill note. If no subject was given and the role's note defaults to self-review (e.g. `ic`,
`pm`), proceed as a self-review; otherwise resolve the subject name to a slug via `people:`.

This is an evidence-gathering and narrative-drafting workflow. Do NOT make up ratings —
surface evidence and let the reader draw conclusions.

**Evidence sources depend on the subject:**
- **Self-review (subject = owner):** the owner has no profile/1-on-1s. Gather from the
  owner's **own** weekly files (wins, deliverables, `#win`/`#risk`), projects where
  `owner == owner.slug`, decisions authored, and incidents owned. Skip the `@mention` and
  profile steps below.
- **Someone else (subject ≠ owner):** use all steps below.

1. Read 02-people/profiles/{slug}.md — note role, level, growth_areas, strengths, current cycle expectations. *(others only)*
2. Determine the current review cycle from context (check 02-people/reviews/ for existing cycle directories). Use the most recent incomplete cycle.
3. Read all 1-on-1 files for this person in 02-people/one-on-ones/{slug}/ from the review period. Extract feedback given (`#feedback`), wins (`#win`), concerns/risks (`#risk`, `#blocked`), and growth progress. *(others only)*
4. Scan weekly files in 01-weekly/ — for others, all mentions of @{FirstName} (note patterns: praise, concern, delegation, escalation); for a self-review, your own entries (wins, deliverables, recurring themes).
5. Check 03-projects/ for projects the subject owned or contributed to: match the slug in each hub's `owner`/`team_members` (for a self-review, `owner == owner.slug`), plus any project whose linked items name the subject. Note outcomes.
6. Check 05-incidents/ for incidents the subject was involved in (owner or contributor) — note the response.
7. Determine the output path and create from _templates/performance-review.md if absent:
   - Others: `02-people/reviews/{cycle}/{slug}.md` with `person: {slug}`.
   - Self-review: `02-people/reviews/{cycle}/{owner.slug}.md` with `person: {owner.slug}`.
   - Both set `cycle:` and `status: draft`.
8. Populate or append to the review file:
   - **## Evidence Log** — bulleted list of raw evidence per source (weeklies, projects, incidents, and 1-on-1s for others), each with date and source file reference
   - **## Competency Notes** — brief notes per the role pack's `{{review_dimensions}}`
   - **## Draft Narrative** — 3–5 sentences summarizing the period, highlighting standout moments

Output a summary of evidence found and confirm the file path.
