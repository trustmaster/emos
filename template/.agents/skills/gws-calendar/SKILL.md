---
name: gws-calendar
description: "Google Calendar: read the agenda and manage events."
---

# gws calendar

> **Prerequisite:** [gws-shared](../gws-shared/SKILL.md) — auth, global flags, security rules.

```bash
gws calendar <resource> <method> [flags]
```

## Common operations

| Method | Purpose | |
|--------|---------|---|
| `events list` | List events in a time window (the agenda) | read |
| `events get` | Full detail for one event | read |
| `freebusy query` | Check availability across calendars | read |
| `events quickAdd` | Create an event from a text string | write |
| `events insert` | Create a fully specified event | write |
| `events update` / `patch` | Modify an event | write |

Write methods change the user's calendar — confirm before running.

## Discovering more

```bash
gws calendar --help                       # every resource and method
gws schema calendar.<resource>.<method>   # exact params, types, defaults
```
