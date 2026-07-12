---
name: weekly-new
description: Create the planning file for the current week, carrying forward open TODOs and follow-ups from the previous week. Use when the user wants to start a new week's plan. No args needed.
---

Create the planning file for the current week.

1. Run `date +%G-W%V` to get the current ISO week (e.g. 2026-W24). Do not infer it from the date. (This form is portable across macOS/BSD and GNU/Linux.) Check whether 01-weekly/YYYY-Www.md already exists. If it does, say so and stop — do not overwrite it.
2. Read the most recent weekly file in 01-weekly/ (highest week number before the current one). If it has `status: active`, update it to `status: completed` now (before creating the new file).
3. From that file, collect all unchecked `- [ ]` items and any `#follow-up` tags — these are the carry-forward items. **Preserve any `#project/{slug}` tags on these lines verbatim** so carried tasks stay linked to their projects (this is what keeps them in the project hubs' Open TODOs rollup).
4. Read the current 01-weekly/_index.md for any delegated items still open.
5. Read _templates/weekly.md.
6. Create 01-weekly/YYYY-Www.md using exactly the sections from the template (## TODO, ## Next week, ## This quarter, ## Notes) — no invented headings. Place carry-forward items and items from the previous week's "## Next week" section under **## TODO**. Leave other sections empty/as-is from the template. Set `status: active` in the new file's frontmatter.
7. Rebuild 01-weekly/_index.md to reflect the new active week.

Confirm the file path created and list the carry-forward items found.
