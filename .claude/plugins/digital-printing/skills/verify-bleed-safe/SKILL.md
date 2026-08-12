---
name: verify-bleed-safe
description: Check that all text and content in a PDF stays within the printer's printable area — i.e. nothing runs into the unprintable margin where it would be clipped. Reports per-page violations with bounding boxes. Read-only — does not modify the PDF. Triggers on phrases like "verify bleed safe", "check printable margins", "will this print without clipping".
---

# Verify Bleed-Safe

Inspect a PDF and report any pages where content extends into the printer's unprintable margin (typically 3–6mm from each edge for office laser/inkjet printers).

This is a **read-only** preflight check. It modifies nothing — it only reports.

## Inputs

- **Input PDF path** (required).
- **Safe margin** (optional, mm) — default 5mm. The minimum distance from page edge that content must respect.
- **Per-edge override** (optional) — `top=X bottom=Y left=Z right=W` if the printer's unprintable margins are asymmetric.

## How it works

For each page:

1. Get the page MediaBox: `pdfinfo -box input.pdf` or `mutool show input.pdf trailer`.
2. Compute the "safe box" = MediaBox shrunk by the safe-margin on every side.
3. Get the bounding box of all *content* on the page (text + images + vector). Use `gs -sDEVICE=bbox` for the ink-bbox of each page:
   ```bash
   gs -dQUIET -dBATCH -dNOPAUSE -sDEVICE=bbox input.pdf 2>&1 | grep "%%HiResBoundingBox"
   ```
4. Compare content bbox against safe box. If content extends past the safe box, report:
   - Page number
   - Which edge(s) violated
   - How far the violation extends (mm)

## Output

Plain-text report:

```
Bleed-safe check: input.pdf (safe margin: 5mm)

PAGE 1: OK
PAGE 2: VIOLATION — text extends 2.3mm past the right edge safe zone (content bbox: ..., safe box: ...)
PAGE 3: OK
PAGE 4: VIOLATION — image extends 8.1mm past the bottom edge safe zone
...

Summary: 2 of 12 pages have bleed-safe violations.
```

Suggest remedies in the report:
- For minor overruns (<10mm): rerun source layout with larger margins, or scale page contents down via `gs -dPDFFitPage`.
- For consistent overruns: the document may have been laid out for a printer with smaller unprintable margins — ask the user.

## Tooling

- `ghostscript` — bounding-box detection.
- `pdfinfo` (poppler-utils) — page dimensions.
- `mutool` (mupdf-tools) — alternative geometry probe.

## Notes

- This check is about *fit-within-printable-area*. It does not address commercial-print bleeds (where you want content to *extend past* the trim line). For that, use `add-bleed`.
- Violations don't always mean the print will fail — they mean it *might* clip. The printer's exact unprintable margin varies by model. 5mm is a safe default; tune for known printers.
