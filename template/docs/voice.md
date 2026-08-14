# Writing voice: sounding like yourself

emOS controls two of the three axes of what it writes for you. `conventions.md` owns
**structure** — where a file goes, what frontmatter it carries, which status values are
legal. Role packs own **vocabulary and emphasis** — what things are called and which
sections your role leans on. Nothing owned **register**: the word choice, sentence shape,
and formatting habits that make a document read as yours.

So every artifact came out in the agent's default voice. That default is recognizable, and
register is the axis a reader notices first. Your weekly report goes to a director, your
review gets pasted into Workday, your reliability roll-up goes to stakeholders. A document
that reads as machine-written costs you credibility whether or not the content is right.

`agent.voice` is the third axis.

## The model

```
config.yaml → agent.voice          optional path to a voice file
        │
        ▼
.agents/voice/{owner.slug}.md      register: posture, sentence mechanics,
        │       + samples/         document architecture, formatting, bans
        │
        ▼
prose-authoring skill              reads the file, matches its register in the
                                   artifact it writes
```

Same shape as the role → pack → skill chain, and the tool → provider → adapter chain, with
one deliberate difference: **the pack is never shipped.** emOS gives you the slot, the
template, the skill, and this guide. The content is yours, because a voice that ships is a
generic voice, which is the thing being fixed.

A role pack generalizes. "What an engineering manager calls things" is the same for every
EM, so `em.md` ships. A voice does not generalize. "How you write" is the one part of this
system nobody else can author for you.

## What it does and does not touch

**It styles files the agent writes.** Reports, reviews, design docs, meeting notes,
incident post-mortems, escalations.

**It does not style conversation.** The agent still answers you, reports failures, and
asks for confirmation in its normal register. A voice file is not a personality.

**It does not change behavior.** Not tool use, not task scoping, not whether the agent
confirms before doing something irreversible.

If you want your chat replies styled too, see [Using it as a host output style](#using-it-as-a-host-output-style)
below. That is a separate, explicit opt-in.

### Precedence

```
conventions.md + AGENTS.md   →   role pack   →   voice file
   structure & safety            vocabulary       register
```

Voice wins on wording. The template wins on everything structural: required fields,
headings, frontmatter, file location, status vocabulary. A voice file cannot move a file,
rename a slug, change a status value, or drop a required field — and it never overrides the
sensitive-content or untrusted-content rules in `AGENTS.md`. If yours seems to demand any
of that, the agent follows the template and tells you.

In files marked `sensitive: true` — talent maps, calibration packs, promo cases — voice
applies to narrative sections only. It never softens, embellishes, or reshapes an evidence
cell. The record stays the record.

## Setting one up

```
/voice
```

Scaffolds `.agents/voice/{your-slug}.md` from the template, creates `samples/`, sets
`agent.voice` in your config, and asks you for writing samples.

Then feed it your own writing, one document at a time:

```
/voice ~/Documents/that-rfc-i-wrote.md
/voice https://internal.wiki/my-post-mortem
```

Each one gets stripped to prose, filed under `samples/`, and indexed with a note on what
it demonstrates.

### Building a voice from your own documents

The written rules matter less than you'd expect. What actually moves register is few-shot
exposure to your writing. Aim for **three or four samples** spanning different registers:

| Pick | Why |
|------|-----|
| A document you wrote for people senior to you | Shows how you compress and what you lead with |
| A document you wrote for your team | Shows your default explanatory mode |
| Something you wrote under time pressure | Strips the polish and exposes your actual habits |
| A document you're proud of | Your ceiling, not your average |

Two rules for every sample:

- **Strip it to prose.** Drop template scaffolding, tables of contents, images, API
  reference tables. A sample teaches voice; it is not an archive.
- **Never include machine-drafted text.** Not even text you reviewed and approved. It will
  teach the agent to reproduce the register you're trying to escape. If a document is
  mixed, cut the drafted parts or label them as an anti-pattern.

Then write the rules, using what you notice in the samples. The template prompts for:

**Posture** — what a sentence must carry, how much affect, concrete before abstract, when
to stop. **Sentence mechanics** — connectors you use, constructions that are yours, verb
register, person, punctuation. **Document architecture** — how you open, how you order
options, how you handle unknowns, how you end. **Numbers and uncertainty** — how you state
an estimate you don't fully trust. **Formatting** — wrapping, bold, tables, list types.
**Hard bans** — words, phrases, and sentence shapes you never use. **Self-check** — a
numbered list the agent runs before writing.

The ban list does the most mechanical work, because it is the only part that is
unambiguously checkable. Be specific: not "avoid clichés" but the actual phrases.

### Sizing

Keep the voice file under roughly 200 lines and each sample under roughly 300. Every
prose-authoring skill reads them, so the context cost should stay proportionate to the
artifact being written. If it starts to bite, keep the voice file and make samples opt-in.

## Ownership: yours, and unmanaged

`.agents/voice/` is **not in `.emos/manifest`**. That means:

- `emos update` never writes there. Your file cannot be overwritten by a release.
- `emos check` never reports it as drift.
- `emos baseline` never records a hash for it.
- Nothing under it ever ships upstream.

The manifest also carries two defensive lines (`- .agents/voice/**`,
`- .agents/output-styles/**`). They are belt-and-braces: the directory is already outside
every include glob, and the updater only writes paths that exist upstream. The lines exist
so that a future release which *does* ship a file at one of those paths can never collide
with yours.

### Private ≠ untracked

**Private** here means *not framework-managed*. It does not mean gitignored.

Your vault is probably its own private repo, and your voice file belongs in it like any
other content — versioned, diffable, restorable. The shipped `.gitignore` leaves it
tracked.

`samples/` is the exception, and only as an opt-in. Your samples are excerpts of documents
you actually wrote, so they may quote people content, unpublished numbers, or internal
system names. If your vault repo is shared, uncomment this line:

```
# .agents/voice/samples/
```

If you're excerpting a review or a promo case, anonymize it. The real record already lives
under `02-people/`; the sample only needs to teach sentence shape.

## Using it as a host output style

Some harnesses can load a Markdown file into the system prompt to set register for a whole
session. Claude Code calls these **output styles** and finds them in `.claude/output-styles/`,
which resolves through the existing `.claude → .agents` symlink.

To opt in, symlink the file:

```bash
mkdir -p .agents/output-styles
ln -s ../voice/alex.md .agents/output-styles/alex-voice.md
```

Then select it: run `/config` and pick it under **Output style**, or set `outputStyle` in
`.claude/settings.local.json`. It applies after `/clear` or on your next session.

Symlink the **file**, never the directory — that keeps `samples/` out of the style picker.
One artifact, two entry points, nothing duplicated.

Four things worth knowing before you do this:

1. **It styles your conversation too**, not just authored files. That is the point of
   opting in, and it is outside what `agent.voice` promises on its own.
2. **`keep-coding-instructions: true` must stay in the frontmatter.** A custom output style
   drops the host's built-in software-engineering instructions unless that field is set,
   and it defaults to `false`. The shipped template always emits `true`. Deleting it is not
   a stylistic choice.
3. **Output styles don't reach subagents**, which run their own system prompt. The
   `agent.voice` path does, which is why it's the primary mechanism and this is an extra.
4. **`/output-style` no longer exists** — deprecated in Claude Code v2.1.73, removed in
   v2.1.91. Use `/config` or the settings field.

The symlink is invisible to the updater (`walk()` skips symlinks), so none of this creates
drift.

## Turning it off

Remove `agent.voice` from `.agents/config.yaml`. Every skill reverts to plain output on the
next run and no file needs deleting. If you set up the host hookup, delete the symlink and
clear `outputStyle` from your settings.

## Related

- [roles.md](roles.md) — the pack-behind-a-config-key pattern this follows. A role pack
  changes *what things are called*; a voice file changes *how sentences are built*.
- [authoring-skills.md](authoring-skills.md) — the resolution line to include if you write
  your own prose-authoring skill.
