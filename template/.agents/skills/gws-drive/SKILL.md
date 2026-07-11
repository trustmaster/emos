---
name: gws-drive
description: "Google Drive: search, read, export, and upload files."
---

# gws drive

> **Prerequisite:** [gws-shared](../gws-shared/SKILL.md) — auth, global flags, security rules.

```bash
gws drive <resource> <method> [flags]
```

## Helper

| Command | Description |
|---------|-------------|
| [`+upload`](../gws-drive-upload/SKILL.md) | Upload a local file with auto-detected metadata |

## Common operations

| Method | Purpose | |
|--------|---------|---|
| `files list` | Search / list files (use the `q` query param) | read |
| `files get` | File metadata, or content with `alt=media` | read |
| `files download` | Download a binary file's content | read |
| `files export` | Export a Google Doc/Sheet/Slide to another MIME type | read |
| `permissions list` | See who has access to a file | read |
| `files create` / `+upload` | Create or upload a file | write |
| `files update` / `copy` | Modify or duplicate a file | write |

> Changing sharing (`permissions create` / `update` / `delete`) alters access
> control — don't run it on the user's behalf; ask them to adjust sharing.

## Shared folders & shared drives

Listing inside a shared folder or shared drive returns **empty results** unless you
pass all three of these params:

```bash
gws drive files list --params '{
  "q": "\"FOLDER_ID\" in parents and mimeType=\"application/vnd.google-apps.spreadsheet\" and trashed=false",
  "fields": "files(id,name,modifiedTime)",
  "includeItemsFromAllDrives": true,
  "supportsAllDrives": true,
  "corpora": "allDrives"
}'
```

## Discovering more

```bash
gws drive --help                       # every resource and method
gws schema drive.<resource>.<method>   # exact params, types, defaults
```
