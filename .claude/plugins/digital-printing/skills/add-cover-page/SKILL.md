---
name: add-cover-page
description: Generate a matching-size cover page with a title (and optional subtitle, author, date) and prepend it to a PDF. Triggers on phrases like "add a cover page", "prepend a title page", "make a cover for this PDF".
---

# Add Cover Page

Create a single-page cover that matches the input PDF's page size and prepend it.

## Inputs

- **Input PDF path** (required).
- **Title** (required).
- **Subtitle** (optional).
- **Author** (optional).
- **Date** (optional, default today).
- **Style** (optional) — `minimal` (centered title, thin rule), `classic` (title + horizontal rule + metadata block), `bold` (large title, colored band). Default `classic`.
- **Output path** (optional) — defaults to `<input>-with-cover.pdf`.

## Tooling

Two clean approaches — pick whichever is available:

### Option A: Typst (preferred — fast, modern)

```typst
#set page(width: 595pt, height: 842pt, margin: 4cm)
#set text(font: "IBM Plex Sans")

#align(center + horizon)[
  #text(28pt, weight: "bold")[#TITLE]
  #v(1em)
  #text(16pt)[#SUBTITLE]
  #v(3em)
  #line(length: 40%)
  #v(1em)
  #text(12pt)[#AUTHOR · #DATE]
]
```

Compile: `typst compile cover.typ cover.pdf`. Page size must match the input PDF exactly — probe with `pdfinfo` first.

### Option B: ReportLab (Python)

If Typst isn't available, use `reportlab` to draw a single-page PDF at the same dimensions.

## Workflow

1. Probe input page size: `pdfinfo input.pdf | grep "Page size"` → extract width/height in pt.
2. Generate cover PDF at matching size.
3. Verify cover layout by rendering to PNG: `gs -sDEVICE=png16m -r100 -o /tmp/cover.png cover.pdf`. Check title isn't clipped, alignment is correct, font rendered properly. If the user is present, show them the preview before committing.
4. Concatenate: `qpdf --empty --pages cover.pdf 1 input.pdf 1-z -- output.pdf`.
5. Verify output: `pdfinfo output.pdf | grep Pages` should show input pages + 1.

## Output

Cover-prepended PDF. Original preserved.
