---
name: burn-in-footer
description: Burn a permanent footer label into every page of a PDF — CLIENT CONFIDENTIAL, PRIVATE, FAMILY DISTRIBUTION, DRAFT, EMBARGOED UNTIL ..., or custom text. User can choose font and size. Renders a PNG preview to verify layout before committing. Triggers on phrases like "add a CONFIDENTIAL footer", "burn in a footer", "stamp 'embargoed until' across the bottom".
---

# Burn-In Footer

Permanently overlay a footer label on every page of a PDF.

## Inputs

- **Input PDF path** (required).
- **Footer text** (required) — pick from presets or pass arbitrary text:
  - `CLIENT CONFIDENTIAL`
  - `PRIVATE`
  - `FAMILY DISTRIBUTION`
  - `DRAFT`
  - `EMBARGOED UNTIL: <date>` (substitute the date)
  - Custom string
- **Font** (optional) — default Helvetica Bold. Accepts any font available to ReportLab/Typst.
- **Size** (optional, pt) — default 10.
- **Color** (optional) — default black; accept hex or named colors.
- **Position** (optional) — `bottom-center` (default), `bottom-left`, `bottom-right`, `top-center`, `top-left`, `top-right`.
- **Vertical offset** (optional) — default 20pt from the page edge.
- **Output path** (optional) — defaults to `<input>-<slug>.pdf`.

## Tooling

Same overlay-and-stamp pattern as `add-watermark`: generate a 1-page overlay PDF that matches the input page size with the footer text drawn at the requested position, then stamp every page using `qpdf --overlay`.

### Overlay generation (Python + ReportLab)

```python
from reportlab.pdfgen import canvas
c = canvas.Canvas("overlay.pdf", pagesize=(w, h))
c.setFont(font_name, size)
c.setFillColorRGB(*rgb)
if position == "bottom-center":
    c.drawCentredString(w/2, vertical_offset, footer_text)
elif position == "bottom-left":
    c.drawString(36, vertical_offset, footer_text)
# ... etc
c.save()
```

### Stamp

```bash
qpdf input.pdf --overlay overlay.pdf -- output.pdf
```

## Verification (mandatory)

Before committing, render a preview PNG and inspect placement:

```bash
gs -sDEVICE=png16m -r150 -o /tmp/footer-check-page1.png -dFirstPage=1 -dLastPage=1 output.pdf
```

Check:
- Footer text fully visible (not clipped at bottom edge).
- Doesn't overlap body text or existing page numbers.
- Font/size renders as intended.

If the user is present, offer to show the PNG before finalising. If verification fails (clipping, collision), adjust `vertical_offset` or `size` and re-render.

## Workflow

1. Probe page size with `pdfinfo`.
2. Resolve preset → text (e.g. `EMBARGOED UNTIL` requires a date — ask if not given).
3. Generate overlay.
4. Stamp.
5. Render preview PNG, verify, then report.

## Output

Footer-stamped PDF. Original preserved.
