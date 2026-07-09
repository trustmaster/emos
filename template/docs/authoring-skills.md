# Authoring skills

A **skill** is a Markdown file of instructions the agent follows when you invoke
it. Skills are how emOS turns "prep my 1-on-1" or "start an incident" into a
repeatable workflow. This guide shows how to write one.

## Anatomy

A skill is a directory under `.agents/skills/` containing a `SKILL.md`:

```
.agents/skills/my-skill/SKILL.md
```

```markdown
---
name: my-skill
description: One or two sentences describing WHAT it does and WHEN to use it.
  Include trigger phrases the user is likely to say. Pass X as args.
---

Plain-language, numbered instructions the agent follows top to bottom.
```

- **`name`** — must match the directory; becomes the `/my-skill` slash command.
- **`description`** — this is the trigger. The agent reads it to decide when the
  skill applies, so lead with the action and name the situations/phrases that
  should invoke it. State what `args` means if the skill takes an argument.

Discovery is automatic: Claude Code finds skills via the `.claude -> .agents`
symlink. No registration step — creating the directory is enough. (Optionally add
a row to the command table in `AGENTS.md` so humans can see it.)

## Writing the body

The body is instructions, not code. Keep them concrete and ordered.

- **Read config, don't hardcode.** Pull owner, paths, people, and org context
  from `.agents/config.yaml`. Resolve `{{tokens}}` (e.g. `{{owner_slug}}`,
  `{{team}}`) at write time — never write a literal token into a file.
- **Use `paths:`** from config for directory locations rather than hardcoding
  `03-projects/` etc. where practical.
- **Follow the conventions** in [`.agents/conventions.md`](../.agents/conventions.md):
  ISO dates, kebab-case slugs, `@FirstName` in prose / slug in frontmatter,
  the `type:`/`status:` frontmatter contract, and the `projects: [slug]` join key
  if the skill creates content that belongs to a project.
- **Start from a template.** If the skill creates a file type, read the matching
  `_templates/*.md` first and fill it in.
- **Respect append-only sections** (`## Current Status`, logs): prepend dated
  entries, never rewrite history.
- **Handle `args`.** Say what happens when it's present vs. absent (e.g. "if args
  is a name, target it; otherwise take the oldest inbox item").
- **End with output.** State what to report back (file path created, summary).
- **Confirm before side effects.** For anything hard to reverse (moves, deletes,
  publishing externally), present the plan and wait for a yes.

## Two kinds of skills

**Workflow skills** are tool-agnostic and orchestrate the vault (`1on1`,
`weekly-new`, `project`, `inbox`, `manager-report`). When one needs an external
capability, it resolves the provider from config rather than naming a product —
see below.

**Provider skills** implement an operation for one external tool
(`create-jira-ticket`, `confluence-load`, `slack-capture`). They are product-named
on purpose and bound to a capability through an adapter. If you're adding one,
read [integrations.md](integrations.md) — you write the skill *and* an adapter in
`.agents/integrations/`, then point `config.tools.{capability}` at it.

To call a capability from a workflow skill, follow this pattern:

```markdown
Resolve the issue tracker: read `.agents/config.yaml` → `tools.issue_tracker`.
If `none`, tell the user and stop. Otherwise open
`.agents/integrations/{provider}.md` and follow its `create_issue` operation
(which names the skill to use).
```

## Trying it

Invoke it in Claude Code by typing `/my-skill` (with args if it takes them). Watch
that it reads the right config, writes to the right path, and reports back. Adjust
the instructions until it behaves; there's no build step.

## Updates and ownership

Skills under `.agents/skills/**` are framework-managed. A skill **you** add that
isn't part of upstream emOS is yours and stays put. If you locally edit a
*shipped* skill, `node .emos/emos.mjs update` won't clobber your edit — it writes
the incoming version alongside as `<file>.emos-new` for you to merge. Run
`node .emos/emos.mjs baseline` after intentional local edits so future updates
don't flag them. (See the main README, "Staying Up to Date".)
