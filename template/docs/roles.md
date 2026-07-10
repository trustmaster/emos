# Roles: one vault, many roles

emOS started as an engineering-manager tool, but the engine — capture, weekly
cadence, projects-as-hubs, decisions, meetings — fits anyone who runs work through
notes. What differed by role was only *vocabulary* and *emphasis*: an IC has no
direct reports, a PM reports to stakeholders, a director runs a portfolio of
teams. So role is a swappable **pack** behind a single config field, the same way
a tool is a swappable **provider** behind a capability.

## The model

```
config.yaml → owner.role          picks a role
        │
        ▼
.agents/roles/{role}.md            pack: vocabulary tokens, review dimensions,
        │                          report format, default 1-on-1 relationship
        ▼
role-sensitive skill               1on1 · perf-review · manager-report · morning ·
(reads owner.role, opens pack)     weekly-review · configure · rebuild
```

A role-sensitive skill never hardcodes manager/report/team language. It reads
`config.owner.role`, opens that pack, resolves the pack's **vocabulary tokens**,
and follows its **skill notes**. Full pack contract:
[`.agents/roles/README.md`](../.agents/roles/README.md).

| Role key | For | Report slug | 1-on-1 default | Review dimensions |
|----------|-----|-------------|----------------|-------------------|
| `em` | Engineering manager (default) | `manager-async` | report | Delivery, Technical, People, Communication, Growth |
| `ic` | Individual contributor / senior+ | `snippets` | manager | Delivery, Technical, Craft, Collaboration, Growth |
| `pm` | Product manager | `launch-status` | stakeholder | Product Sense, Execution, Influence, Data, Strategy |
| `director` | Director / senior leader | `portfolio` | report / skip | Org Impact, Strategy, Talent, Execution, Stakeholder |

**The folder taxonomy is the same for every role.** Packs change what things are
*called* and which sections you *lean on* — never where files live. Default `em`
reproduces the classic behavior, so existing vaults that never set `owner.role`
are unaffected.

## Switching your role

Run `/configure` (it asks for your role and tailors the people prompt), or set it
directly:

```yaml
owner:
  role: ic          # em | ic | pm | director
```

That's the whole switch. The next time you run `perf-review`, `manager-report`,
`1on1`, etc., they resolve the `ic` pack — self-review by default, upward 1-on-1s,
weekly `snippets` instead of a manager async report.

## Relationships (per-person framing)

Role sets the default; a person's `relation:` refines it. Each profile carries:

```yaml
relation: report    # report | manager | peer | stakeholder | skip
```

`1on1` reads it to frame the prep: coaching for a `report`, managing-up for your
`manager`, alignment for a `peer`/`stakeholder`. Absent ⇒ the pack's
`{{oneonone_default_relation}}`. The `people:` map in `config.yaml` stays a flat
`@Mention → slug` map for every role — relationship lives on the profile.

## Adding a custom role pack — worked example

Say your org has a **Technical Program Manager** role. You add a pack; you do
**not** edit any skill.

**1. Copy the template.** Copy
[`.agents/roles/_pack-template.md`](../.agents/roles/_pack-template.md) to
`.agents/roles/tpm.md` and fill the four blocks:

```markdown
# Technical Program Manager role pack
**Role key:** `tpm`
**Status:** community

## Vocabulary
| Token | Value for this role |
|-------|---------------------|
| `{{role_report_slug}}` | `program-status` |
| `{{role_report_title}}` | `Program Status - {{team}}` |
| `{{review_dimensions}}` | `Execution, Coordination, Risk, Communication, Impact` |
| `{{oneonone_default_relation}}` | `stakeholder` |
| `{{status_report_audience}}` | `program stakeholders and sponsors` |

## People & relationships
Workstream leads and sponsors; default relation stakeholder. …

## Sections in focus / dormant
03-projects (programs), 07-strategy, 08-meetings, 10-reports. Dormant: 06-hiring.

## Skill notes
- 1on1 — cross-workstream alignment …
- perf-review — self-review by default …
- manager-report — program status roll-up …
```

**2. Select it.**

```yaml
owner:
  role: tpm
```

Done. Every role-sensitive skill now resolves the `tpm` pack. The shipped packs
stay on disk, unused, ready if you switch — nothing was overwritten.

## Where things live

| Thing | Location | Owner |
|-------|----------|-------|
| Active role | `.agents/config.yaml` → `owner.role` | you |
| Role packs | `.agents/roles/{role}.md` | framework (shipped) / you (new) |
| Pack contract & token list | `.agents/roles/README.md` | framework |
| Per-person relationship | profile frontmatter `relation:` | you |

New packs you add are **yours** — the framework updater only overwrites shipped
paths, and it preserves any local edit to a shipped pack as a `.emos-new` sidecar
(see the main README, "Staying up to date"). After an intentional local edit to a
shipped file, run `./emos baseline` so it stops being flagged as a conflict.
