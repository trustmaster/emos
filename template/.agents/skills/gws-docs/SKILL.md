---
name: gws-docs
description: "Google Docs: read and create documents."
---

# gws docs

> **Prerequisite:** [gws-shared](../gws-shared/SKILL.md) — auth, global flags, security rules.

```bash
gws docs <resource> <method> [flags]
```

## Helper

| Command | Description |
|---------|-------------|
| [`+write`](../gws-docs-write/SKILL.md) | Append plain text to a document |

## Common operations

| Method | Purpose | |
|--------|---------|---|
| `documents get` | Read a document's content | read |
| `documents create` | Create a blank document | write |
| `documents batchUpdate` / `+write` | Insert or edit content | write |

Write methods change the document — confirm before running.

## Discovering more

```bash
gws docs --help                       # every resource and method
gws schema docs.<resource>.<method>   # exact params, types, defaults
```
