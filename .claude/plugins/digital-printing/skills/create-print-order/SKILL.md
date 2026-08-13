---
name: create-print-order
description: Generate a formal print job order — a printer-facing document (PDF + JSON) that specifies files, copies, color instructions, paper, binding, finishing, special notes, and the customer's contact info. Drops it into a job folder so it's ready to hand to a digital printer or print shop. Triggers on phrases like "create a print order", "make a printer order sheet", "write up the job for the printer".
---

# Create Print Job Order

Produce a structured order document that tells a digital printer exactly what to do with the files in a job folder. Output is both a human-readable PDF (`order.pdf`) and a machine-readable JSON (`order.json`).

## Inputs

- **Job folder path** (required) — the folder created by `create-job-folder`. The order references files inside `<job>/files/`.
- **Copies** (required) — number of copies to print (per file, or per job).
- **Color** (required) — `color`, `grayscale`, or `mixed` (per file). For `mixed`, expect a per-file map.
- **Paper** (optional) — stock and weight, e.g. `120gsm matte coated`, `80gsm uncoated`, `200gsm cardstock`. Default `standard 80gsm office`.
- **Sides** (optional) — `single` or `duplex`. Default `duplex`.
- **Binding** (optional) — `none`, `staple`, `spiral` (specify edge), `comb`, `perfect-bound`, `saddle-stitch`. Plus instructions (e.g. "spiral on long edge").
- **Finishing** (optional) — `trim`, `lamination`, `hole-punch`, `fold` (with type).
- **Special notes** (optional) — free text for the printer.
- **Due date** (optional).
- **Contact info** — pulled from `$CLAUDE_USER_DATA/digital-printing/config.json` under `contact`. On first use, prompt and persist:
  - Full name
  - Email
  - Phone
  - Optional: company, billing reference

## Config

Adds to the existing `digital-printing/config.json`:

```json
{
  "printing_folder": { "...": "..." },
  "subfolder_strategy": "...",
  "contact": {
    "name": "Daniel Rosehill",
    "email": "daniel@example.com",
    "phone": "+972 ...",
    "company": "DSR Holdings"
  }
}
```

## order.json schema

```json
{
  "order_id": "2026-04-27-family-photo-book",
  "created": "2026-04-27T15:00:00+03:00",
  "due": "2026-05-01",
  "customer": {
    "name": "Daniel Rosehill",
    "email": "daniel@example.com",
    "phone": "+972 ...",
    "company": "DSR Holdings"
  },
  "files": [
    {
      "filename": "01-cover.pdf",
      "pages": 1,
      "copies": 2,
      "color": "color",
      "sides": "single",
      "paper": "200gsm cardstock"
    },
    {
      "filename": "02-body.pdf",
      "pages": 48,
      "copies": 2,
      "color": "grayscale",
      "sides": "duplex",
      "paper": "80gsm uncoated"
    }
  ],
  "binding": {
    "type": "spiral",
    "instructions": "Long edge, black coil"
  },
  "finishing": ["trim"],
  "notes": "Please call before starting if any file fails preflight."
}
```

## order.pdf

A clean one-page Typst-rendered order sheet:

- **Header**: ORDER + order ID + date + due date
- **Customer block**: name, email, phone, company
- **Files table**: filename, pages, copies, color, sides, paper
- **Binding & finishing block**
- **Special notes block**
- **Footer**: total page count × copies summary; signature line

Use Typst with IBM Plex Sans (the user's preferred typeface) when available.

## Workflow

1. Read job folder; verify `manifest.json` exists.
2. Resolve customer info from config; if missing, prompt and persist.
3. Resolve per-file print specs — if `color` is `mixed`, ask user for per-file values (or read from manifest if recorded there).
4. Write `order.json` to the job folder.
5. Render `order.pdf` to the job folder.
6. Update `manifest.json` to reference the order.
7. Report path.

## Output

`<job-folder>/order.json` and `<job-folder>/order.pdf`. The folder is now ready to zip and send.
