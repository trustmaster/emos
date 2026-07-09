---
name: emos-update
description: Check for and apply emOS framework updates using the built-in updater, so you don't have to run the CLI by hand. Use when the user says "update emOS", "check for framework updates", or "pull the latest emOS". Optionally pass the update source (a git URL or local path) as args.
---

Run the emOS framework updater on the user's behalf via the root launcher
(`./emos`, which forwards to `.emos/emos.mjs`).

## Step 1 — Determine the source

The updater needs a `--source`: the upstream emOS framework as a git URL or a
local path.

- If args provides it, use that.
- Otherwise ask the user for it. (Once emOS is published to npm, `./emos update`
  will resolve the bundled template automatically and no source is needed.)

## Step 2 — Dry run (check)

Run:

```bash
./emos check --source <source>
```

Report what *would* change — which framework files update, and flag any that
would be written as `<file>.emos-new` sidecars because they have local edits.
Only framework paths (see `.emos/manifest`) are ever touched; `config.yaml`,
`CONFIG.md`, and all content directories are never affected.

## Step 3 — Confirm, then apply

Show the summary and ask the user to confirm. Only after a clear yes:

```bash
./emos update --source <source>
```

## Step 4 — Report

- List updated files and any `.emos-new` sidecars that need a manual merge.
- Remind the user to review the changes (`git diff`) and commit when satisfied.
- If they had intentionally hand-edited a framework file and want to keep it as
  the new baseline, they can run `./emos baseline` so future updates don't
  re-flag it.

Note: on Windows the launcher is `emos.cmd` (`emos.cmd check --source …`). If the
`./emos` launcher isn't present, fall back to `node .emos/emos.mjs <cmd>`.
