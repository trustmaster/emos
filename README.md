# 🗂️ emOS — Everyone's Markdown Organizer System

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

A Markdown-based operating system for engineering managers, technical leads, directors, and individual contributors. It's just plain `.md` files, so it works with whatever you already use — any Markdown editor (Obsidian, VS Code, Cursor, Zed, …) for humans, and any agentic coding harness (Claude Code, Codex, OpenCode, Cursor, Kimi Code, …) for the AI side. Your team, projects, decisions, incidents, 1-on-1s, and weekly planning live as files you own, with an agent that knows the conventions and does the filing.

![emOS in action](https://raw.githubusercontent.com/trustmaster/emos/main/docs/assets/weekly-note-demo.gif)

emOS combines powerful approaches:

- Structured knowledge base that you can grow day by day
- Turns any AI agent into your personal assistant
- Extensible via skills and tools
- Connects everything into an integrated operating system

No database, no SaaS, no lock-in. Just files in a git repo you control.

```bash
# Scaffold a fresh vault in an empty directory
npx emos-vault init
```

Then open it with your AI agent and ask it to configure the project.

---

## Why

Engineering management generates a lot of connected context — a project pulls in
people, meetings, decisions, incidents, and strategy. Most tools scatter that
across apps. emOS keeps it in one traversable Markdown vault where:

- **You own the data.** Plain files, in your git repo. Readable in any editor.
- **An agent does the work.** Skills for 1-on-1 prep, weekly planning, incident
  post-mortems, performance-review evidence, project context, and more.
- **Projects are first-class.** Any file links to a project via a `projects:`
  key; each project hub shows an auto-generated rollup of everything related.
- **Tools are pluggable.** Jira/Confluence/Slack/Google Workspace ship as
  defaults, but the workflows are tool-agnostic — swap in Linear, Notion, etc.

## Quick start

1. **Scaffold** an empty directory:
   ```bash
   mkdir my-vault && cd my-vault
   npx emos-vault init
   ```
   This lays down the framework, an empty content skeleton, the `.claude`
   symlink for agent discovery, and starter `config.yaml` / `CONFIG.md`.
2. **Configure** — open the vault with your coding agent (Claude Code, OpenCode,
   Codex, or any harness that reads `AGENTS.md`) and ask it to configure the
   project (this runs the `configure` skill). It prompts for your
   name, team, people, and which tools you use — all optional — and writes the
   config for you. (Prefer manual? Edit `.agents/config.yaml`.)
3. **Use it** — capture into `00-inbox/`, start a project with `/project-new`,
   prep a 1-on-1 with `/1on1 <name>`, plan your week with `/weekly-new`.

Want to see it populated first? Browse [`examples/`](examples/) — a fictional
"Payments Platform" team with projects, incidents, decisions, and dashboards.

## How it's organized

```
00-inbox/     Quick capture — unsorted
01-weekly/    Weekly planning + review
02-people/    Profiles, 1-on-1s, reviews
03-projects/  One folder per project; each has a hub doc with a Related rollup
04-decisions/ ADRs
05-incidents/ Post-mortems
06-hiring/    Positions, interviews, rubrics
07-strategy/  OKRs, roadmaps
08-meetings/  Meeting notes
09-knowledge/ Reference material
10-reports/   Recurring reports
_templates/   File templates
docs/         Guides (this repo)
.agents/      Config, conventions, skills, integration adapters, role packs
.emos/        Updater machinery (you don't edit this)
```

Each section has a generated `_index.md` dashboard the agent rebuilds with
`/rebuild`.

## Works for your role

emOS isn't just for engineering managers. One config field —
`.agents/config.yaml` → `owner.role` — selects a **role pack** that tunes
vocabulary, performance-review dimensions, the weekly status-report format, and
your default 1-on-1 framing. The folders are the same for everyone; only the
language and emphasis change.

| Role | What shifts |
|------|-------------|
| `em` (default) | Direct reports, team-health async, downward coaching 1-on-1s |
| `ic` | Self-review brag-doc, weekly *snippets*, upward 1-on-1s with your manager |
| `pm` | PRDs & launches, product-status update for stakeholders, roadmap/OKR focus |
| `director` | Portfolio of teams, program rollups, 1-on-1s with managers & skip-levels |

Set it via `/configure` (or edit the field), and switch anytime. A person's
`relation:` (`report`/`manager`/`peer`/`stakeholder`) refines framing per person.
Add your own role in a few lines — see **[docs/roles.md](docs/roles.md)**.

## Typical workflows

You drive emOS by just **talking to your agent in plain language**. Each skill
carries a description of when to use it, so the agent picks the right one from
what you ask — no command syntax to memorize. The examples below are phrased the
way you'd actually type them.

> Every skill can be triggered three ways, and you can mix them freely:
> - **Natural language** — "prep my 1-on-1 with Priya" (works in any harness)
> - **Slash command** — `/1on1 Priya` (where your harness supports them)
> - **Just ask** — describe the outcome and let the agent choose the skill
>
> The names in the [Skills & capabilities](#skills--capabilities) tables are the
> slash aliases; the plain-English trigger is always available.

**Start the day**

> *"What's on my plate today?"*

A terse briefing — open TODOs, blockers, active incidents, upcoming deadlines,
and today's 1-on-1s.

**Run the week**

> *"Start this week's plan."* — opens the week's file, carrying open TODOs forward
> *"Capture this: vendor renewal is due end of Q3."* — timestamped note into today's inbox
> *"Triage my inbox."* — the agent classifies each item and proposes where it goes, then waits for your OK
> *"Let's close out the week."* — tallies completion, scans the week, writes the retro

**Prep and run a 1-on-1**

> *"Prep my 1-on-1 with Priya."*

Builds a prep file from her profile, last session's carry-over, recent weekly
mentions, and project context. Take notes live; next week the agent pulls the
unresolved threads forward automatically.

**Spin up and work a project**

> *"Start a new project for GCP cost optimization."* — folder + hub doc + a follow-up TODO this week
> *"Pull everything about the GCP cost project into one place."* — full context loaded into the session
> *"Start meeting notes for the GCP planning sync."*
> *"Record a decision: we're adopting spot instances for batch workers."* — writes the next ADR
> *"Draft a design doc for the spot-instance migration."* — an RFC in the project's `docs/`, ready to circulate
> *"Refresh the project's Related section."* — regenerates the hub rollup after you've tagged content

**Handle an incident**

> *"We've got checkout 500s spiking in eu-west-1 — start a post-mortem."*

Creates the incident file with an inferred severity and a follow-up TODO in the
current week.

**Report up and out**

> *"Draft my weekly manager update."* — synthesizes the week's 1-on-1s, projects, and incidents
> *"Pull the current sprint into a report."* — Jira sprint snapshot grouped by status
> *"Help me prepare Priya's performance review."* — gathers real evidence, invents no ratings
> *"Log a win: cut checkout p99 latency 40% this sprint."* — appends to your brag doc so review season writes itself

**Pull in outside context** (when the matching tool is enabled)

> *"Save this Slack thread: <url>"* — classified note into the inbox
> *"Import this Confluence page: <url>"* — imported, classified, and routed
> *"Publish this file to Confluence."*

## Skills & capabilities

Ask for any of these in plain language — the agent matches your request to the
right skill. The `/<name>` column is the slash alias where your harness supports
it. Provider skills (marked ⚙︎) only activate when the matching tool is enabled
in your config.

**Daily & weekly cadence**

| Skill | What it does |
|-------|--------------|
| `/morning` | Terse briefing — TODOs, blockers, active incidents, upcoming deadlines, today's 1-on-1s |
| `/weekly-new` | Start the week's plan, carrying open TODOs and follow-ups forward |
| `/weekly-review` | Close out the week — completion tally + retrospective |
| `/capture` | Quick, no-analysis note into today's inbox |
| `/inbox` | Triage inbox items — classify and route, with confirmation before moving |
| `/import-url <url>` | Import any URL — Confluence, Google Doc, GitHub, or web page — classify and file it, then pull your action items into this week's plan (uses the matching tool when enabled, plain fetch otherwise) |

**People**

| Skill | What it does |
|-------|--------------|
| `/1on1 <name>` | Build a 1-on-1 prep file from profile, carry-over, recent mentions, and projects |
| `/perf-review <name>` | Draft a review narrative from real evidence — no invented ratings |

**Projects, decisions & incidents**

| Skill | What it does |
|-------|--------------|
| `/project-new <title>` | Create a project folder + hub doc + follow-up TODO |
| `/project <slug>` | Load a project's full context into one session |
| `/project-sync [slug]` | Regenerate the hub's auto Related rollup |
| `/meeting-new <title>` | Dated meeting note linked to a project |
| `/decision <title>` | New ADR with the next sequential number |
| `/design-doc-new <title>` | Technical design doc / RFC in a project's `docs/` — the engineering *how*: design, alternatives, security/perf, rollout |
| `/incident <desc>` | Post-mortem file with inferred severity and a follow-up TODO |

**Product**

| Skill | What it does |
|-------|--------------|
| `/prd-new <title>` | PRD in a project's `docs/` — problem, goals, requirements, metrics, rollout |
| `/experiment-new <name>` | A-B test brief — hypothesis, primary + guardrail metrics, variants, sizing, results log |
| `/roadmap-new <horizon>` | Now / Next / Later roadmap in `07-strategy/roadmaps/`; links projects to roll up |
| `/research-new <topic>` | User-research / interview-synthesis note in `09-knowledge/research/` (PII-free) |

**Reporting**

| Skill | What it does |
|-------|--------------|
| `/manager-report` | Weekly async status, synthesized from weeklies, 1-on-1s, projects, incidents |
| `/brag-log [win]` | Append to your evergreen impact log (brag doc), or harvest recent wins — feeds self-reviews and snippets |
| `/jira-sync` ⚙︎ | Pull the current sprint into a status-grouped report |
| `/github-sync` ⚙︎ | Snapshot a GitHub Projects board into a status-grouped report |

**Integrations** (capability-gated ⚙︎)

| Skill | Capability | What it does |
|-------|-----------|--------------|
| `/create-jira-ticket` | `issue_tracker` | Create a Jira ticket via MCP |
| `/jira-sync` | `issue_tracker` | Snapshot the active sprint into a report |
| `/create-github-issue` | `issue_tracker` | Create a GitHub issue (+ optional Project board) via `gh` |
| `/github-sync` | `issue_tracker` | Snapshot a GitHub Projects board into a status-grouped report |
| `/pr-review` | `code_host` | First-line PR review pass — summary, flags, architectural/dependency changes, escalations (chat only, never posts) |
| `/github-browse` | `code_host` | Read-only remote repo exploration via `gh` — for incident investigation & assignments |
| `/confluence-load`, `/confluence-save` | `wiki` | Import from / publish to Confluence |
| `/slack-capture` | `chat` | Save a Slack thread as a classified note |
| Google Workspace (`gws-*`) | `docs` | Gmail, Calendar, Drive, Docs, Sheets, Slides |

**Vault maintenance**

| Skill | What it does |
|-------|--------------|
| `/configure` | Interactive setup/update of owner, team, people, and tools (don't hand-edit YAML) |
| `/doctor` | Read-only health check — broken frontmatter, rotted project links, unmapped mentions, stale dashboards |
| `/rebuild` | Regenerate all `_index.md` dashboards |
| `/emos-update` | Check for and apply framework updates |

## Projects as hubs

emOS is filed by *type* (meetings, decisions, people…) but work happens by
*project*. Any file can carry `projects: [slug]` in its frontmatter (or a
`#project/{slug}` tag in prose). Each project's hub doc has a generated rollup:

```markdown
<!-- rollup:start — generated by project-sync, do not hand-edit -->
## Related
### Meetings · Decisions · Incidents · People · Strategy · Reports · Open TODOs
<!-- rollup:end -->
```

Run `/project-sync` to regenerate it, or `/project <slug>` to load a project's
full context into one session. See [`examples/`](examples/) for a populated hub.

## Tools & integrations

Tools are chosen by **capability**, not hardcoded:

```yaml
tools:
  issue_tracker: jira        # jira | github | none
  code_host:     github       # github | none  (PR review + code browsing)
  wiki:          confluence   # confluence | none
  chat:          slack        # slack | none
  docs:          gws          # gws | none
```

Each provider has an adapter in `.agents/integrations/` binding it to the skills
that implement it. One provider can fill several capabilities — `github` backs
both `issue_tracker` (issue creation) and `code_host` (PR review + code
browsing), so you can pair `issue_tracker: jira` with `code_host: github`. Adding
a tool (Linear, Notion, Mattermost, MS Office…) is a new skill + adapter + config
flip — you never edit the core workflows. See **[docs/integrations.md](docs/integrations.md)**.

## Staying up to date

emOS separates **framework files** (structure, templates, skills — safe to
update) from **your content** (never touched). The boundary is declared in
`.emos/manifest`. Keep your vault in your own git repo and pull improvements:

```bash
npx emos-vault update    # pull the latest published release into this vault

# or track a specific source (git ref, fork, or local clone):
./emos update --source <git-url-or-path>
```

Run either from inside your vault. Locally-edited framework files are preserved
as `<file>.emos-new` for you to merge, never clobbered.

> **Windows note:** agent discovery uses a `.claude → .agents` symlink. On
> Windows, enable Developer Mode or `git config core.symlinks true`. If symlinks
> aren't available, `emos init` copies `.agents` to `.claude` instead — re-run
> after updates to keep them in sync.

## Extending

- **Add a tool:** [docs/integrations.md](docs/integrations.md)
- **Change or add a role:** [docs/roles.md](docs/roles.md)
- **Write a skill:** [docs/authoring-skills.md](docs/authoring-skills.md)
- **Conventions:** `.agents/conventions.md`
- **Agent entry point:** `AGENTS.md`

## Requirements

- Node.js ≥ 18 (for the `emos` CLI). No other runtime dependencies.
- **Any Markdown editor** — Obsidian, VS Code, Cursor, Zed, or whatever you like —
  and/or **any agentic harness** to drive it: Claude Code, Codex, OpenCode,
  Cursor, Kimi Code, etc. Agents discover the vault via `AGENTS.md` and the
  Agent Skills (`SKILL.md`) format (with a `.claude → .agents` symlink for Claude
  Code; Codex reads `.agents/skills/` natively). No tool is required, nothing is
  locked in.

## Contributing

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[Apache-2.0](LICENSE) © 2026 Vladimir Sibirov
