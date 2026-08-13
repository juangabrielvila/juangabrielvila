---
name: strip-footers-and-page-numbers
description: Remove footer text and page numbers from a PDF — useful when reprinting a doc whose pagination no longer matches, or stripping a journal/report footer before binding. Triggers on phrases like "remove footers", "strip page numbers", "delete the footer from this PDF".
---

# Strip Footers and Page Numbers

Erase footer content (page numbers, dates, document IDs, copyright lines) from every page of a PDF.

## Inputs

- **Input PDF path** (required).
- **Footer height** (optional) — default 50 pt from the bottom of the page. Adjust if the footer is taller or sits higher.
- **Mode** (optional):
  - `whiteout` (default) — paint a white rectangle over the footer area; preserves PDF structure and is fast.
  - `text-aware` — use `pdftotext` to identify footer text, then redact only matching text runs. Slower but no white box.
- **Output path** (optional) — defaults to `<input>-no-footer.pdf`.

## Tooling

- `pdftk`, `qpdf`, `ghostscript`, `mutool` (mupdf-tools), `pdftotext` (poppler-utils).
- For overlay-based whiteout: generate a 1-page overlay PDF with a white rectangle at the footer Y-range and stamp it onto every page using `pdftk ... background` or `qpdf --overlay`.

## Whiteout recipe (qpdf + ImageMagick or Python ReportLab)

1. Probe page size: `pdfinfo input.pdf | grep "Page size"`.
2. Generate a single-page overlay PDF the same size, with a white filled rectangle covering `(0, 0)` to `(pageWidth, footerHeight)`.
3. Stamp onto every page:
   ```bash
   qpdf input.pdf --overlay overlay.pdf -- output.pdf
   ```

## Verification step

After stamping, render page 1 and the last page to PNG and visually confirm the footer is gone and no body content was clipped:
```bash
gs -sDEVICE=png16m -r100 -o /tmp/check-%d.png -dFirstPage=1 -dLastPage=1 output.pdf
```

If `text-aware` mode: run `pdftotext output.pdf - | tail` and confirm the page-number/footer line no longer appears.

## Caveats

- Whiteout leaves a white band — not a problem on white-paper prints, but visible if the page background is colored.
- Footer height varies — when in doubt, ask the user or render a preview and let them confirm the band height.
