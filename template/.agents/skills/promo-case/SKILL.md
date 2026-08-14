---
name: promo-case
description: Draft a promotion case for someone — evidence that they already operate at the target level, mapped to level expectations, with scope deltas, signature work, gaps and counter-arguments, and a sponsor plan. Gathers evidence and never asserts a decision. For managers and leaders of managers preparing a promotion packet. Use when the user wants to build, prepare, or strengthen a promo case. Pass the person's name as args.
roles: [director]
---

Draft a promotion case for the person named in args.

Read `paths.profiles` (default `02-people/profiles`), `paths.reviews` (default
`02-people/reviews`), `paths.one_on_ones` (default `02-people/one-on-ones`), and
`owner.role` from `.agents/config.yaml`. Open the role pack at
`.agents/roles/{owner.role}.md` for `{{review_dimensions}}`.

**Resolve voice:** read `agent.voice` from `.agents/config.yaml`. If it's set and the file
exists, read it (plus `samples/` alongside it) and match its register in the file you write.
Apply it to the artifact only — never to your chat reply or progress narration. If the key is
absent, write plainly and say nothing; if it's set but the file is missing, say so once and
write plainly.
Voice governs the narrative sections only. It never softens, embellishes, or reshapes an
evidence cell.

> A promotion case argues that someone is **already operating** at the target level.
> It is not a reward argument and not a readiness argument. Every claim needs an
> artifact behind it — you gather and structure evidence; you never assert that the
> promotion should happen, and you never manufacture a level expectation the org
> doesn't have.

## Step 1 — Resolve and frame

1. Resolve the name to a slug via `people:`. Read their profile for `level`, `manager`,
   `teams`, `growth_areas`, `strengths`.
2. Determine **current level** and **target level**. Ask if the profile doesn't make the
   target obvious — don't guess a ladder.
3. Ask for the org's expectations for the target level (a link, a paste, or a file in
   `09-knowledge/`). If none is available, say so plainly and build the case around the
   scope dimensions instead — and flag in the output that the expectations mapping is
   unverified against a real ladder.
4. Determine the cycle from `{paths.reviews}/` as `perf-review` does.

## Step 2 — Gather evidence

- **Existing review material** — `{paths.reviews}/{cycle}/{slug}.md` and prior cycles.
  Prior-cycle language about "next level" is the strongest signal available.
- **Projects** — where they are `owner` or in `team_members`: scope, ambiguity absorbed,
  outcomes with numbers. Note the delta between the earliest and most recent.
- **Incidents** — ones they led; how far the decision-making reached.
- **Decisions** — ADRs in `04-decisions/` where they're a decider or author.
- **1-on-1s** — `#win`, `#feedback`, growth-area movement, and any moment their manager
  described work as above level.
- **Weeklies** — mentions across the period; look for others depending on them.
- **Design docs / PRDs** in project `docs/` they authored.

## Step 3 — Structure the argument

- **Expectations → evidence table.** One row per target-level expectation. Leave a row's
  evidence blank when there isn't any — a blank row is information, and quietly padding
  it is how cases get rejected in the room.
- **Scope deltas.** Before/now for surface owned, blast radius, people pulled along,
  ambiguity absorbed. Anchor "before" to roughly a year ago or the last promotion.
- **Signature work.** Two or three situations, each written as situation → what they
  personally did → what changed. Only work that wouldn't have landed at the current level.
- **Influence beyond their own work.**
- **Gaps & counter-arguments.** Write the strongest honest case *against*, then the
  response and the plan. Derive gaps from unmoved growth areas, thin expectation rows,
  short time in level, and any recorded concern.
- **Supporting voices.** Anyone in the record who observed the work — peers,
  stakeholders, senior engineers. Note that their input still needs to be requested;
  don't present recorded remarks as solicited endorsements.

## Step 4 — Write

Create `{paths.reviews}/{cycle}/{slug}-promo.md` from `_templates/promo-case.md` with
`person:`, `cycle:`, `current_level:`, `target_level:`, `manager:`, `sponsor:` (the
vault owner unless told otherwise), `status: draft`, `sensitive: true`, today's `date:`.

If the file already exists, treat this as a refresh: update the evidence tables, keep
every human-written paragraph, and prepend a dated entry to the Log.

## Step 5 — Report

- Path written, and the case's honest shape: which expectations are well evidenced,
  which are thin, and which have nothing.
- The **weakest link** — the one gap most likely to sink it, and what would close it.
- What only a human can supply: the ladder text if it was missing, peer input, the
  decision forum and timing.
- Whether the record supports the case as *already operating* at the level, or as
  *approaching* it — stated as an evidence observation, not a recommendation.

**Handling:** `sensitive: true` — not published externally, and not shared with the
subject as-is. See conventions → Sensitive Content.
