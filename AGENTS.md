# AGENTS.md — emOS development repo

**This is the source repository for the `emos-vault` npm package. It is NOT a vault.**

If you have worked with emOS content before, unlearn that mode here. This repo *builds
the framework* that gets scaffolded into user vaults. You are editing the framework, the
CLI, skills, templates, and docs — you are **not** filing notes, prepping 1-on-1s, or
running vault skills. There is no `config.yaml`, no `people:` map, no `_index.md` to
rebuild at this level.

> ⚠️ **Two `AGENTS.md` files exist and they are different documents.**
> - **This file** (repo root) = how to develop the package. *For you, right now.*
> - [`template/AGENTS.md`](template/AGENTS.md) = the agent guide that ships **into**
>   user vaults (vault conventions, file-creation rules, roles). Edit it as framework
>   content when changing vault behavior — but do not *follow* it here.

---

## What this is

- npm package: **`emos-vault`** (bin: `emos`). Scaffolds and updates a Markdown knowledge
  vault for EMs, ICs, PMs, and directors.
- **Zero runtime dependencies.** The CLI is plain Node (`>=18`), and skills are Markdown.
  Keep it `npx`-able and portable across macOS / Linux / Windows.
- No build step, no test framework, no bundler. What you edit is what ships.

## The ownership boundary (read this before editing anything)

**The framework lives in [`template/`](template/). Edit there, not at the repo root.**

| Path | What it is | Edit when |
|------|-----------|-----------|
| `template/` | Everything scaffolded into a vault: skills, integrations, roles, templates, docs, `AGENTS.md`, `conventions.md`, the CLI | Changing framework behavior |
| `template/.emos/emos.mjs` | The CLI (`init`/`check`/`update`/`baseline`), zero deps. npm `bin` points straight at it | Changing scaffold/update logic |
| `template/.emos/manifest` | The ownership boundary itself — which vault paths the updater manages vs. leaves user-owned | Adding/removing a framework-managed file |
| `examples/demo-vault/` | A fully **fictional** demo vault for browsing. No real data | Illustrating features |
| Root `README.md`, `CONTRIBUTING.md`, `LICENSE`, `NOTICE`, `package.json` | Repo metadata | Repo-level changes only |

If you add a new framework file under `template/`, you **must** add its vault-relative path
(or a glob) to `template/.emos/manifest` — otherwise `emos update` won't manage it in
existing vaults. Conversely, never add user-content paths to the manifest. The two lines
prefixed `-` in the manifest (`config.yaml`, `settings.local.json`) are protected: real
user config that the updater never overwrites.

## Local development

There is nothing to build. Test the CLI against a throwaway vault:

```bash
# from the repo root, with $REPO as its absolute path (e.g. REPO=$(pwd)):
mkdir /tmp/emos-test && cd /tmp/emos-test
node "$REPO/template/.emos/emos.mjs" init                          # scaffold using bundled framework
# edit something under template/, then dry-run what an update would change:
node "$REPO/template/.emos/emos.mjs" check --source "$REPO/template"
```

The CLI operates on the **current working directory** as the vault; `--source` points at
the framework. When shipped, `template/` is bundled so `--source` can be omitted.

## Conventions

- **Skills** are Markdown instruction files at `template/.agents/skills/{name}/SKILL.md`.
  Keep them **config-driven** (read `.agents/config.yaml`; never hardcode names/paths/tool
  coordinates), **tool-agnostic** for workflow skills (resolve capabilities via
  `config.tools`, not a product), and convention-following. See
  [`template/docs/authoring-skills.md`](template/docs/authoring-skills.md).
- **Tool integrations** are **product-named on purpose** (`create-jira-ticket`,
  `confluence-load`, `slack-capture`, `gws-*`). To add a tool, ship a *new* skill + adapter
  in `template/.agents/integrations/` and flip a `tools:` key. **Never rename or overwrite
  an existing provider.** See [`template/docs/integrations.md`](template/docs/integrations.md).
- **No real data, ever.** Anything in `examples/` or docs must be fictional — no real names,
  companies, credentials, cloud IDs, or internal URLs.
- Small, focused changes. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full contributor guide.

## Release

CI publishes to npm on a pushed `v*` tag ([`.github/workflows/publish.yml`](.github/workflows/publish.yml)).
The workflow **fails if the tag version doesn't match `package.json`'s `version`** — bump
`package.json` and tag the matching `vX.Y.Z` together. Trusted Publishing (OIDC) uses the
Node-bundled npm; don't upgrade npm in the workflow.
