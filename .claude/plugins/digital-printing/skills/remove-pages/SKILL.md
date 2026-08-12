---
name: remove-pages
description: Remove specified pages from a PDF — single pages, ranges, or "every blank page". Triggers on phrases like "remove pages 5-7 from this PDF", "delete the last page", "drop the cover page", "strip blank pages".
---

# Remove Pages from PDF

Produce a new PDF with the specified pages removed.

## Inputs

- **Input PDF path** (required).
- **Pages to remove** (required) — flexible:
  - Single: `5`
  - Range: `5-7`
  - List: `1,3,5,7`
  - Mixed: `1,3-5,12,20-end`
  - Special: `blank` (auto-detect blank pages), `last`, `first`
- **Output path** (optional) — defaults to `<input>-trimmed.pdf`.

## Tooling

`qpdf` is the cleanest option — it supports inverse selection natively. `pdftk` and `mutool` are alternatives.

### qpdf — keep all pages except 5

```bash
qpdf --empty --pages input.pdf 1-4,6-z -- output.pdf
```

The trick: qpdf can't directly *remove* pages, but it can *select* the pages you want to keep. Compute the inverse of the user's removal list against the page count.

### Page count

```bash
pdfinfo input.pdf | awk '/^Pages:/ {print $2}'
```

### Blank-page detection

For `blank` mode, render each page to a low-res PNG and check whether the image is essentially uniform white:

```bash
gs -sDEVICE=png16m -r50 -o /tmp/p%d.png input.pdf
# then for each PNG, use ImageMagick: identify -format "%[mean]" /tmp/p1.png
# values close to 65535 (16-bit max) ≈ blank
```

## Workflow

1. Get total page count.
2. Parse the user's removal spec into a sorted page list.
3. Compute the keep-list as its inverse.
4. Run qpdf with the keep-list.
5. Verify: `pdfinfo output.pdf | grep Pages` and confirm new count = old - removed.

## Output

Trimmed PDF at the requested path. Original is preserved.
