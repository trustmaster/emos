---
name: talent-map
description: Build or refresh your org's talent map — performance and growth-runway placement, promotion candidates, key-person risk, succession cover, and retention watch — from evidence already in the vault. For directors and other leaders of managers. Use when the user wants a talent review, succession planning, a bus-factor check, or to see who's ready for more. No args needed; pass a team slug to scope it.
roles: [director]
---

Create or refresh the org's talent map — an evergreen working document, not a
per-cycle artifact.

Read `paths.profiles` (default `02-people/profiles`), `paths.teams` (default
`02-people/teams`), `paths.one_on_ones` (default `02-people/one-on-ones`),
`paths.reviews` (default `02-people/reviews`), and `owner.role` from
`.agents/config.yaml`.

**Resolve voice:** read `agent.voice` from `.agents/config.yaml`. If it's set and the file
exists, read it (plus `samples/` alongside it) and match its register in the file you write.
Apply it to the artifact only — never to your chat reply or progress narration. If the key is
absent, write plainly and say nothing; if it's set but the file is missing, say so once and
write plainly.
Voice governs the narrative sections only. It never softens, embellishes, or reshapes an
evidence cell.

> **Evidence only.** Every placement, risk, and signal must trace to something written
> in the vault, and you cite where. If the record doesn't support a cell, leave it empty
> and list the person under coverage gaps. Never infer someone's intentions, ambitions,
> or personal circumstances — only what they or their manager actually stated.

## Step 1 — Population

Everyone in your org: profiles with `relation: report`, plus everyone whose `manager:`
is one of them. Scope to one team if args names a team slug. Skip anyone with
`status: departed`; flag `departing` and `on-leave` separately.

## Step 2 — Gather per person

- Profile: level, time in level, `skill_will`, `growth_areas`, `strengths`,
  `current_focus`, `status`.
- Latest review in `{paths.reviews}/*/{slug}.md` and any promo case
  (`{slug}-promo.md`).
- 1-on-1s: growth-area movement, stated ambitions, stated frustrations, `#feedback`.
- Projects owned and incidents led — scope and outcomes, not activity counts.

## Step 3 — Derive each section, conservatively

- **Placement** — performance from delivery evidence against their *current* level;
  growth runway only where there is evidence of operating above it. Default to
  `at level` rather than guessing. Cite the basis in the last column.
- **Promotion candidates** — only people with evidence at the target level already.
  Offer `/promo-case <name>` for each rather than writing the case here.
- **Key-person risk** — derive from concentration, not seniority: who is the sole owner
  of a project, the only responder on an incident type, the only name on a service.
  Cross-check team hubs' ownership tables. This is usually the most valuable section and
  the one most often wrong by omission — search widely.
- **Succession** — for every manager role and any critical IC role, name emergency cover
  and a one-year candidate. "No cover" is a legitimate and important entry.
- **Retention watch** — only concrete, recorded signals: stated intent, disengagement
  noted in a 1-on-1, a promo missed twice, a manager change. Never speculation. If you
  have nothing, leave it empty.
- **Under-supported** — people whose growth stalled for reasons within your control.
  Look for: unchanged growth areas across two cycles, no stretch project, an unfilled
  manager gap, thin 1-on-1 cadence.

## Step 4 — Write

Path: `02-people/talent-map.md`.

- **If it doesn't exist**, create it from `_templates/talent-map.md` with
  `sensitive: true`, `teams:`, and today's `updated:`.
- **If it exists**, this is a refresh: update the tables in place, set `updated:`, and
  **prepend** a dated entry to the Review log naming what moved and why. Never silently
  drop a row — if someone leaves a section, say so in the log entry. Preserve any
  human-written cell you can't independently support; mark it `(unverified)` rather than
  deleting it.

## Step 5 — Report

- Path, people covered, and what changed since the last refresh.
- **Coverage gaps** — people whose record is too thin to place, and their manager.
- The two or three findings worth acting on this month — usually a key-person risk with
  no mitigation, or a succession row with no cover.
- Suggested follow-ups: `/promo-case` for ready candidates, `/1on1` where a retention
  signal needs a conversation.

**Handling:** `sensitive: true` — never published externally, never shared with the
people it describes, and not to be pasted into chat tools. See conventions → Sensitive
Content.
