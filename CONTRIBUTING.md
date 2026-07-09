# Contributing to emOS

Thanks for your interest. emOS is a small, dependency-free framework — contributions
that keep it simple, portable, and tool-agnostic are the most welcome.

## Repo layout

```
template/                The framework scaffolded into a vault via `emos init`.
                         Skills, adapters, templates, docs, and the CLI all live here.
template/.emos/emos.mjs  The CLI (init / check / update / baseline), zero deps.
                         The npm `bin` points straight at this file — it's the
                         single source of truth, also scaffolded into each vault.
examples/                A fictional demo vault for exploration. No real data.
docs/                    (Inside template/) human-facing guides.
```

**Important:** the framework lives in `template/`. Edit skills, templates,
adapters, `AGENTS.md`, `conventions.md`, and the CLI under `template/`, not at the
repo root. The root `README.md`, `CONTRIBUTING.md`, and `LICENSE` are repo metadata.

## Local development

Test the CLI against a throwaway vault:

```bash
mkdir /tmp/emos-test && cd /tmp/emos-test
node /path/to/repo/template/.emos/emos.mjs init          # uses the bundled framework
# make a change in template/, then:
node /path/to/repo/template/.emos/emos.mjs check --source /path/to/repo/template
```

`emos init`/`check`/`update` operate on the **current working directory**. There
are no build or test frameworks — the CLI is plain Node, and skills are Markdown.

## Adding or changing a skill

Skills are Markdown instruction files under `template/.agents/skills/{name}/SKILL.md`.
See [docs/authoring-skills.md](docs/authoring-skills.md). Keep them:

- **Config-driven** — read values from `.agents/config.yaml`; never hardcode
  names, paths, or tool coordinates.
- **Tool-agnostic** (for workflow skills) — resolve capabilities via
  `config.tools`, not a specific product.
- **Convention-following** — dates, slugs, frontmatter per `conventions.md`.

## Adding a tool integration

Ship a **new** product-named skill plus an adapter in
`template/.agents/integrations/`, and document it. Never rename or overwrite an
existing provider. See [docs/integrations.md](docs/integrations.md).

## Guidelines

- **No real data.** Anything in `examples/` or docs must be fictional. Never
  commit real names, companies, credentials, cloud IDs, or internal URLs.
- **Zero runtime dependencies** in the CLI — keep it `npx`-able and portable
  across macOS / Linux / Windows.
- **Keep the ownership boundary honest.** If you add a framework file, add it to
  `template/.emos/manifest` so updates manage it; if it's user content, don't.
- **Small, focused PRs** with a clear description of the change and why.

## Reporting issues

Open an issue at https://github.com/trustmaster/emos/issues with steps to
reproduce (for bugs) or the use case (for features).

## License

By contributing, you agree that your contributions are licensed under the
[Apache-2.0](LICENSE) license.
