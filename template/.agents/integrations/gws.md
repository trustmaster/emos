# Google Workspace integration adapter

**Capability:** `docs` (document suite — docs, sheets, slides, drive; also calendar/mail)
**Provider key:** `gws`  ← value for `config.yaml` → `tools.docs`
**Status:** `shipped`

## Prerequisites

- The `gws` CLI installed and authenticated (github.com/googleworkspace/cli).
- See the `gws-*` skills for per-service usage (`gws-drive`, `gws-docs`,
  `gws-sheets`, `gws-slides`, `gws-gmail`, `gws-calendar`, and `gws-shared` for
  auth/global-flag patterns).

## Config

Link base URL: `external.gdrive`. The `gws` CLI manages its own auth (OAuth via
`gcloud`), so no credentials live in `config.yaml`.

## Operations

The document-suite contract is intentionally light — the `gws-*` skill family is
the implementation. Map operations to whichever `gws-*` skill fits:

| Operation | Implemented by | Notes |
|-----------|----------------|-------|
| `read_doc` | skills: `gws-docs`, `gws-sheets-read`, `gws-slides` | Export/read a Doc/Sheet/Slides file. |
| `write_doc` | skills: `gws-docs-write`, `gws-sheets`, `gws-slides` | Append/write content. |
| `list_files` | skill: `gws-drive` | Browse Drive / shared drives. |

## Auth refresh

If a `gws` command fails with **401 Unauthorized** or **403 Forbidden**, the
session token has expired. Refresh it, then retry:

```bash
export GCLOUD_SDK_ROOT=$(gcloud info --format="value(installation.sdk_root)")
export PYTHONPATH="$GCLOUD_SDK_ROOT/lib/third_party:$GCLOUD_SDK_ROOT/lib"
export GOOGLE_WORKSPACE_CLI_TOKEN=$(python3 -c "
import google.auth
from google.auth.transport.requests import Request

scopes = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/presentations.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly'
]

creds, project = google.auth.default(scopes=scopes)
if not creds.valid:
    creds.refresh(Request())
print(creds.token)
")
```

## Notes

- Exporting a Google Doc as Markdown: use the `text/markdown` MIME type.
- This adapter is deliberately not decomposed further — the `gws-*` bundle is
  GSuite-specific by nature. A different document suite (e.g. MS Office / Graph
  API) would ship as its own skills + adapter and set `tools.docs` accordingly.
