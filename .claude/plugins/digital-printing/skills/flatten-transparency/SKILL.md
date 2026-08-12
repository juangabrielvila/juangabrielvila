---
name: flatten-transparency
description: Flatten transparency in a PDF — eliminates banding, color shifts, and weird overprint artifacts on older or cheaper digital printers. Triggers on phrases like "flatten transparency", "fix banding on print", "flatten layers in PDF".
---

# Flatten Transparency

Convert transparent overlays, alpha blends, and soft masks into solid raster/vector output. Many digital printers (especially older RIPs or budget office units) mishandle live transparency, causing banding or color shifts.

## Inputs

- **Input PDF path** (required).
- **Quality** (optional) — `print` (default, 300 DPI raster regions), `screen` (150 DPI, smaller files), `prepress` (highest fidelity).
- **Output path** (optional) — defaults to `<input>-flat.pdf`.

## Tooling

Ghostscript with `pdfwrite` and `-dCompatibilityLevel=1.3` flattens automatically because PDF 1.3 has no live transparency model.

### Recipe

```bash
gs -o output.pdf \
   -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.3 \
   -dPDFSETTINGS=/printer \
   -dEmbedAllFonts=true \
   -dSubsetFonts=true \
   -dNOPAUSE -dBATCH \
   input.pdf
```

`Compatibility=1.3` forces flattening. `/printer` tunes raster quality for print.

## Diagnosis (when to use)

Symptoms that suggest transparency is the culprit:
- Soft drop-shadows print as banded gradients.
- Logos with alpha look milky or washed out.
- Colors near transparent overlays shift.

Probe for transparency:

```bash
mutool show input.pdf grep -i "/SMask\|/CA\|/ca\b\|/BM"
```

Hits → live transparency present.

## Caveats

- Flattening rasterizes affected regions — file size may grow.
- Text inside flattened regions may become a raster image and lose searchability/selectability. Keep the original.

## Output

Flattened PDF. Original preserved — flattening is destructive in the sense that liveness is lost.
