---
name: skip-level
description: Prep a skip-level 1-on-1, or with no args report your skip-level coverage across the org — who you haven't spoken with recently, recurring themes, and signals that don't match what their managers report. For directors and other leaders of managers. Use when the user wants to prep a skip-level, or asks who they're overdue to speak with. Pass a person's name as args, or none for the coverage report.
roles: [director]
---

Skip-levels are how you get unfiltered signal from people who don't report to you.
This skill has two modes.

Read `paths.profiles` (default `02-people/profiles`), `paths.one_on_ones` (default
`02-people/one-on-ones`), `paths.teams` (default `02-people/teams`), `people:`, and
`owner.role` from `.agents/config.yaml`.

---

## Mode A — with args: prep one skip-level

1. Resolve the name to a slug via `people:`.
2. Confirm the relationship: their profile should carry `relation: skip`. If it says
   `report`, this is a normal 1-on-1 — say so and hand off to `1on1`. If they have no
   profile, offer to create one with `relation: skip` and their manager set.
3. Run the `1on1` skill's workflow for this person — it already handles `relation: skip`
   framing and writes the prep file to
   `{paths.one_on_ones}/{slug}/YYYY-MM-DD.md`. Don't duplicate its file handling.
4. Then **add** the skip-specific context that `1on1` doesn't gather:
   - **Their manager's view.** The most recent 1-on-1 with their manager: what was said
     about this person or their team.
   - **Team context.** Their team hub (via the profile's `teams:` or the manager link) —
     current health rating, open incidents, delivery pressure.
   - **Last skip.** What you discussed last time and what you promised to do. An unkept
     promise from a skip-level is the fastest way to make the next one useless.
   - **Deltas worth probing.** Anywhere the team hub or manager 1-on-1 says one thing and
     this person's own weekly mentions or last skip said another. List them as questions,
     not conclusions.
5. Suggest 3–5 open questions suited to a skip: what's slower than it should be, what
   they'd change, where the team's direction is unclear, whether they're growing, what
   they'd want you to hear that their manager might soften. Never questions that ask them
   to evaluate their manager directly.

**Boundaries, and say them in the output:** a skip-level is for signal and growth, not
direction. Don't take decisions that belong to their manager, don't relay what was said
in a way that identifies the source without permission, and record nothing in the file
that you wouldn't be willing to have read back to you.

---

## Mode B — no args: coverage report

Read-only. Writes nothing.

1. Build the skip population: every profile with `relation: skip`, plus every person
   whose `manager:` is one of your reports (a manager with `relation: report`). Note
   which team each belongs to.
2. For each, find the most recent file in `{paths.one_on_ones}/{slug}/` and compute days
   since. Treat "overdue" as **>90 days** unless the user names a different cadence.
3. Report:
   - **Overdue** — table of person · team · manager · last skip · days since, worst first.
     Include anyone who has *never* had one, listed first.
   - **Coverage by team** — how many of each team's people you've spoken with in the last
     two quarters. A team at 0% is the real finding.
   - **Recurring themes** — patterns across the last ~6 months of skip notes: what comes
     up in more than one conversation, and in how many. Attribute to a team, not a person,
     unless the person raised it publicly.
   - **Unresolved commitments** — open `- [ ]` items and `#follow-up` tags in skip files
     where you are the owner. These are debts; list them with age.
   - **Contradictions** — where skip-level signal disagrees with the team's health log or
     its manager's reporting. State both sides and the source; draw no conclusion.
   - **Suggested next three** — who to book, and the reason each.
4. Offer to prep the top one (Mode A). Don't do it unprompted.

Skip files carry personal candour — treat them as `sensitive` even where the flag isn't
set: quote sparingly, never publish externally, and don't name a source for a theme
without checking first.
