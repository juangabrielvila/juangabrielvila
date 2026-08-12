---
name: add-watermark
description: Overlay a diagonal text watermark (DRAFT, PRIVATE, CONFIDENTIAL, etc.) at 45° across every page in light red (or user-specified color), at low opacity so body text remains readable. Triggers on phrases like "add a DRAFT watermark", "stamp PRIVATE on every page", "watermark this PDF".
---

# Add Diagonal Watermark

Stamp a large rotated text watermark across every page of a PDF.

## Inputs

- **Input PDF path** (required).
- **Watermark text** (required) — `DRAFT`, `PRIVATE`, `CONFIDENTIAL`, or arbitrary string.
- **Color** (optional) — default `light red` (RGB 0.85, 0.2, 0.2 at 25% opacity). Accept named colors or hex.
- **Opacity** (optional) — default 0.20 (20%).
- **Angle** (optional) — default 45°.
- **Font** (optional) — default Helvetica Bold.
- **Size** (optional) — default auto-fit (≈ page diagonal length / text length × 0.6).
- **Output path** (optional) — defaults to `<input>-<watermark-slug>.pdf`.

## Tooling

Generate a single-page overlay PDF the same size as the input, then stamp it onto every page using `qpdf --overlay`.

### Overlay generation (Python + ReportLab)

```python
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

c = canvas.Canvas("overlay.pdf", pagesize=(width_pt, height_pt))
c.saveState()
c.translate(width_pt/2, height_pt/2)
c.rotate(45)
c.setFillColor(Color(0.85, 0.2, 0.2, alpha=0.20))
c.setFont("Helvetica-Bold", font_size)
c.drawCentredString(0, 0, "DRAFT")
c.restoreState()
c.save()
```

### Stamp onto input

```bash
qpdf input.pdf --overlay overlay.pdf -- output.pdf
```

## Workflow

1. Probe page size with `pdfinfo`.
2. Compute font size to fit (text width ≈ 60% of page diagonal).
3. Generate the overlay.
4. **Verification** — render page 1 of the output to PNG and inspect:
   ```bash
   gs -sDEVICE=png16m -r100 -o /tmp/wm-check.png -dFirstPage=1 -dLastPage=1 output.pdf
   ```
   Confirm watermark is visible, centered, at the right angle, body text still readable.
5. Stamp onto all pages.
6. Report and offer to show the user the preview PNG.

## Output

Watermarked PDF.

## Caveats

- Some viewers (older Acrobat) struggle with PDF transparency; if printing is critical and the printer is old, consider `flatten-transparency` after watermarking.
