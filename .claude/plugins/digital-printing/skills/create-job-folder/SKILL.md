---
name: create-job-folder
description: Bundle one or more print-ready PDFs into a single "print job" folder with a manifest, ready to hand to a digital printer or share with collaborators. Triggers on phrases like "create a print job", "bundle these PDFs", "make a job folder for the printer".
---

# Create Print Job Folder

Group multiple finished PDFs into a single, named folder with a manifest describing the job.

## Inputs

- **Job name** (required) — short label, e.g. `2026-04-27-family-photo-book`. If not given, auto-generate from date + first PDF name.
- **PDF paths** (required) — one or more files to include.
- **Printer** (optional) — printer name or print shop, recorded in the manifest.
- **Notes** (optional) — free-text notes for the printer (paper stock, duplex preference, copies, finishing).
- **Parent folder** (optional) — defaults to the user's printing folder from `upload-to-printing-folder`'s config (`$CLAUDE_USER_DATA/digital-printing/config.json`); falls back to `~/Documents/Printing/` if no config.

## Layout

```
<parent>/<job-name>/
├── manifest.json
├── README.md
└── files/
    ├── 01-cover.pdf
    ├── 02-body.pdf
    └── 03-appendix.pdf
```

Files are copied (not moved) and prefixed with a 2-digit ordinal so they sort in print order.

## manifest.json schema

```json
{
  "job_name": "2026-04-27-family-photo-book",
  "created": "2026-04-27T14:32:00+03:00",
  "printer": "Office Depot — Talpiot",
  "notes": "Duplex, 120gsm matte, 2 copies, spiral bound long edge",
  "files": [
    {
      "order": 1,
      "filename": "01-cover.pdf",
      "source_path": "/home/user/work/cover-final.pdf",
      "pages": 1,
      "page_size": "A4",
      "verified": {
        "bleed_safe": true,
        "fonts_embedded": true,
        "checked_at": "2026-04-27T14:30:00+03:00"
      }
    }
  ]
}
```

## README.md

Auto-generated human-readable summary — printer name, notes, file list with page counts. This is what you'd hand to the print shop.

## Workflow

1. Resolve parent folder (config → fallback).
2. Create `<parent>/<job-name>/files/`.
3. For each input PDF:
   - Copy into `files/` with ordinal prefix.
   - Probe `pdfinfo` for page count and size.
   - If the file came from a recent verify-bleed-safe / embed-fonts run in this session, record those check results in the manifest.
4. Write `manifest.json` and `README.md`.
5. Report folder path and contents.

## Caveats

- Source files are copied, not moved — original locations untouched.
- This skill does not run preflight checks itself. If the user wants verification before bundling, run `verify-bleed-safe` etc. on the source files first (or invoke the `print-prep-orchestrator` agent).

## Output

Path to the new job folder. Suggest `share-job-folder` as the natural next step.
