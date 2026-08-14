---
name: team-new
description: Create a team entity — an org unit you lead through its manager — as a hub doc with mission, operating model, and a generated Related rollup. For directors and other leaders of managers; an EM can create one for their own team. Use when the user wants to add, register, or start tracking a team, squad, or group. Pass the team name as args.
roles: [director]
---

Create a new team hub doc.

Team name: the value of args.

Read `paths.teams` (default `02-people/teams`), `paths.profiles` (default
`02-people/profiles`), `people:`, and `owner.slug` from `.agents/config.yaml`.

**Resolve voice:** read `agent.voice` from `.agents/config.yaml`. If it's set and the file
exists, read it (plus `samples/` alongside it) and match its register in the file you write.
Apply it to the artifact only — never to your chat reply or progress narration. If the key is
absent, write plainly and say nothing; if it's set but the file is missing, say so once and
write plainly.

> A **team** is an org unit, not a piece of work. Work lives in
> `{paths.projects}/` and links to a team with `teams: [slug]`. If the user is
> describing an initiative rather than a standing group, use `project-new`
> instead and say so.

1. Generate a slug from the name (lowercase, hyphen-separated, max 4 words).
2. Check that `{paths.teams}/{slug}.md` doesn't already exist. If it does, stop
   and offer to open it instead.
3. Read `_templates/team-profile.md`.
4. Ask for the essentials in **one** batch — each optional, skip freely:
   - **Manager** — who runs this team. Resolve the name to a slug via `people:`.
     If they have no profile at `{paths.profiles}/{slug}.md`, offer to create one
     (with `relation: report`), but don't block on it.
   - **Mission** — one line.
   - **Headcount** — current, and open reqs.
   - **Projects** — any existing project slugs this team owns.
5. Create `{paths.teams}/{slug}.md` from the template with frontmatter filled:
   - `name:` from args, `slug:` the slug
   - `status: active` (use `forming` if the user says it's still being stood up)
   - `manager:`, `mission:`, `headcount:`, `projects:` from step 4
   - `formed:` today's date unless the user gives another
   - leave `parent_team`, `links`, `last_health_check` as `null`
   - **keep the `<!-- rollup:start -->…<!-- rollup:end -->` block intact** — it
     stays empty until content links to the team.
6. **Offer** (don't do automatically) to link existing content to the new team:
   - add `teams: [{slug}]` to the project hubs named in step 4;
   - add `teams: [{slug}]` to the profiles of people on the team.
   List exactly which files you'd touch and wait for a yes.
7. If `07-strategy/portfolio.md` exists, run `team-sync` to refresh the rollups.
   If it doesn't, mention that `/portfolio` can create one — don't create it here.
8. Rebuild `02-people/_index.md`.

Output the created path, the manager, and whatever you offered but didn't do.
