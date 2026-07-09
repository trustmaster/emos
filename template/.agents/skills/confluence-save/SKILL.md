---
name: confluence-save
description: Push a local emOS markdown file to Confluence under the team space, creating or updating the page as needed. Use when the user wants to publish or sync a local emOS file to Confluence. Pass the file path as args.
---

> **Provider skill** for the `wiki` capability (`confluence`) — the `save_page` operation. Active when `config.yaml` → `tools.wiki: confluence`. Adapter: [.agents/integrations/confluence.md](../../integrations/confluence.md).

Push a local emOS markdown file to Confluence.

Arguments (args): path to the local file (relative to emOS root or absolute).
Example: `04-decisions/2026-06-08-image-scoring-model.md`
Example: `05-incidents/2026-06-01-api-outage.md`

1. Read the local file at the path given in args.
2. Confluence coordinates — read from `.agents/config.yaml` → `confluence:`:
   - cloudId: `confluence.cloud_id`
   - space: `confluence.space_key`
   - Team root page: ID `confluence.root_page_id` (title `confluence.root_title`)
3. Parse the frontmatter `type:` to pick the parent page. Search the space for a child of the root page matching the title below; if not found, fall back to the root page directly:
   - `type: decision` → parent title: "Architecture Decision Records"
   - `type: incident-postmortem` → parent title: "Incidents & Post-Mortems"
   - `type: project` → parent title: "Projects"
   - `type: meeting-notes` → parent title: "Meeting Notes"
   - Anything else → parent: the root page (`confluence.root_page_id`)
4. Convert the markdown body (everything after frontmatter) to publish-ready content.
   - Strip emOS-internal frontmatter fields (type, status, etc.) — they're noise in Confluence.
   - Keep the title as an H1 if not already present.
5. Check if a Confluence page with the same title already exists under that parent:
   - If yes: update the existing page (increment version).
   - If no: create a new page.
6. After saving, add a `confluence_url:` field to the local file's frontmatter with the Confluence page URL.
7. Report: Confluence page URL, whether created or updated, parent page used.

Note: Use `contentFormat: markdown` when creating/updating.
