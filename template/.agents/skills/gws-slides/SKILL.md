---
name: gws-slides
description: "Google Slides: read and create presentations."
---

# gws slides

> **Prerequisite:** [gws-shared](../gws-shared/SKILL.md) — auth, global flags, security rules.

```bash
gws slides <resource> <method> [flags]
```

## Common operations

| Method | Purpose | |
|--------|---------|---|
| `presentations get` | Read a presentation and its slides | read |
| `presentations create` | Create a blank presentation | write |
| `presentations batchUpdate` | Add or edit slides and content | write |

Write methods change the presentation — confirm before running.

## Discovering more

```bash
gws slides --help                       # every resource and method
gws schema slides.<resource>.<method>   # exact params, types, defaults
```
