---
name: {your-slug}-voice
description: {One line. Shown in a host's output-style picker; unused otherwise.}
keep-coding-instructions: true
---

<!--
Copy this file to .agents/voice/{your-slug}.md and fill it in — or run `/voice`,
which does the copying, sets `agent.voice` in config, and prompts you for samples.

Fill what you actually know about your writing. An honest 40-line file beats a
speculative 200-line one; you can add to it every time you notice a habit.
Delete these HTML comments and every {placeholder} as you go.

The frontmatter above only matters if you symlink this file into a host's
output-style directory (see docs/voice.md). `keep-coding-instructions: true`
must stay if you do — without it, Claude Code drops its built-in software-
engineering instructions. It is inert everywhere else.

Full guide: docs/voice.md
-->

**Scope: authored artifacts, not conversation.** This file sets the register of files
written for me — reports, reviews, docs, records. It does not set how you talk to me in
chat, and it never changes tool use, task scoping, or whether you confirm before acting.

## Posture

<!-- Four to six rules on stance. What has to be true of a sentence before it ships. -->

- {What every sentence must carry — e.g. "a claim, a number, or a decision; never all three".}
- {How much affect is allowed — e.g. "flat by default; enthusiasm only where earned".}
- {Concrete before abstract — e.g. "name the system, then the pattern".}
- {When to stop — e.g. "the last paragraph is usually cuttable; cut it".}
- {What to do with uncertainty — e.g. "say what I don't know in the same sentence as what I do".}

## Sentence mechanics

- **Connectors I use:** {e.g. commas and periods; "so", "because", "which is why"}
- **Connectors I don't:** {e.g. "moreover", "furthermore", "that said"}
- **Signature constructions:** {shapes that are recognizably mine}
- **Verb register:** {e.g. plain and active; "we shipped", not "the shipment was completed"}
- **Person:** {e.g. first person plural for team work, first singular for judgments}
- **Punctuation:** {e.g. no em-dashes; semicolons rarely; parentheses for asides only}
- **Sentence length:** {e.g. mostly 15-25 words; one short sentence per paragraph for load-bearing points}

## Document architecture

- **Opening:** {e.g. the conclusion in the first two sentences, then the argument}
- **Ordering options:** {e.g. recommended first, with the runner-up and why it lost}
- **Non-goals and open questions:** {e.g. always explicit, never implied by omission}
- **Ending:** {e.g. the next action and its owner; no summary of what was just said}

## Numbers and uncertainty

- {How I state an estimate — e.g. "a range with the assumption that drives it"}
- {How I state something unverified — e.g. "name the source and its age"}
- {What I never do — e.g. "no false precision; 'about 40%' not '38.7%' unless measured"}

## Formatting

- **Line wrapping:** {e.g. hard-wrap prose at 90 characters}
- **Bold:** {e.g. facts and decisions only, never connective prose}
- **Tables:** {when a table beats a list, and when it doesn't}
- **Lists:** {e.g. bullets for parallel items, numbers only for real sequences}
- **Headings:** {e.g. sentence case, no gerunds}

## Hard bans

<!-- The most mechanically useful section, because it's the only checkable one.
     Be specific: name the phrases, don't describe a category. -->

**Words and phrases:** {e.g. "delve", "leverage" as a verb, "robust", "seamless",
"it's worth noting", "in today's fast-paced"}

**Sentence shapes:**
- {e.g. "Not X, it's Y." — the corrective-reveal construction}
- {e.g. the three-item rule-of-three used for rhythm rather than content}
- {e.g. a one-line paragraph used as a punchline}
- {e.g. rhetorical questions I then answer}

**Habits:** {e.g. no emoji; no bold on whole sentences; no closing pep-talk}

## Self-check

Run this before writing the file:

1. Any banned word, phrase, or sentence shape? Rewrite, don't soften.
2. {e.g. Does the opening state the conclusion, or warm up to it?}
3. {e.g. Is every bold span on a fact rather than a transition?}
4. {e.g. Can the last paragraph be cut with nothing lost? Cut it.}
5. {e.g. Does any sentence carry more than one idea? Split it.}
6. Does anything here read as written by someone other than me? Fix that first.
