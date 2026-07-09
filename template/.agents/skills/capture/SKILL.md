---
name: capture
description: Quick-capture a short piece of text into today's inbox file with a timestamp — no analysis or reformatting. Use when the user says "capture this", wants a quick note jotted down, or wants something saved to 00-inbox fast. Pass the text to capture as args.
---

Quick-capture the text provided in args to the inbox.

1. Determine today's date.
2. Check if 00-inbox/YYYY-MM-DD.md already exists. If yes, append to it. If no, create it.
3. Append the following entry to the file (at the end):

```
- YYYY-MM-DD HH:MM — {captured text}
```

Use the current time if available, otherwise omit the time.

If args (or the current session) clearly references a project, append a `#project/{slug}` tag to the captured line so it surfaces in that project later. Do not prompt for it — only tag when it's obvious; otherwise capture the text as-is.

4. Confirm the text was captured and the file path.

Keep it quick — no analysis, no reformatting, no extra files. Just capture.
