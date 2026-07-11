---
name: gws-sheets
description: "Google Sheets: read and write spreadsheet values."
---

# gws sheets

> **Prerequisite:** [gws-shared](../gws-shared/SKILL.md) — auth, global flags, security rules.

```bash
gws sheets <resource> <method> [flags]
```

## Helper

| Command | Description |
|---------|-------------|
| [`+read`](../gws-sheets-read/SKILL.md) | Read values from a range |

## Common operations

| Method | Purpose | |
|--------|---------|---|
| `spreadsheets values get` / `+read` | Read a range | read |
| `spreadsheets get` | Spreadsheet metadata (sheet names, sizes) | read |
| `spreadsheets values append` | Append rows to a range | write |
| `spreadsheets values update` | Overwrite a range | write |
| `spreadsheets create` | Create a new spreadsheet | write |

Quote ranges containing `!` with double quotes (gws-shared → Shell Tips). Write
methods change the spreadsheet — confirm before running.

## Discovering more

```bash
gws sheets --help                       # every resource and method
gws schema sheets.<resource>.<method>   # exact params, types, defaults
```
