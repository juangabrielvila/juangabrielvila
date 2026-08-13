---
name: add-bleed
description: Add bleed margins to a PDF for commercial print shops that trim — extends the page size by the bleed amount on each side and shifts content to the new center. Most office digital printing does NOT need this; use only when sending to a print shop. Triggers on phrases like "add bleed", "add 3mm bleed", "prep for trim".
---

# Add Bleed

Expand a PDF's page size to add bleed on every side. Commercial print shops trim to the trim line; the bleed area absorbs registration error.

## When to use

- Sending to a commercial / offset / print-shop digital press that trims final size.
- Document has edge-to-edge images or color that should extend past the trim.

## When NOT to use

- Office laser/inkjet printing — these don't trim, and printing onto a larger page just wastes paper or fails.
- Standard documents with white margins — bleed adds nothing.

## Inputs

- **Input PDF path** (required).
- **Bleed amount** (optional, mm) — default 3mm (industry standard). Some shops want 5mm.
- **Output path** (optional) — defaults to `<input>-bleed.pdf`.

## Tooling

`pdfjam` or `ghostscript`. Strategy: increase MediaBox by `2 × bleed` on each axis, then shift content by `bleed` so it remains centered.

### Recipe (ghostscript)

```bash
# input is A4: 595 x 842 pt; 3mm = 8.5 pt
gs -o output.pdf \
   -sDEVICE=pdfwrite \
   -dDEVICEWIDTHPOINTS=612 \
   -dDEVICEHEIGHTPOINTS=859 \
   -dFIXEDMEDIA \
   -c "<</PageOffset [8.5 8.5]>> setpagedevice" \
   -f input.pdf
```

## Caveats

- This skill does *not* extend background images/colors into the bleed area — it just adds whitespace. If the source layout has edge-to-edge images, those need to be redesigned with bleed at the source (Indesign, Affinity, etc.). Adding bleed *after the fact* on an already-laid-out PDF leaves a visible white band around content.
- For source-correct bleed, redo layout with bleed enabled in the design tool. This skill is a last-resort prep.

## Output

Bleed-extended PDF.
