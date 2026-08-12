---
name: downsample-images
description: Downsample embedded images in a PDF to a target DPI (default 300 for print, 150 for proofs). Reduces file size and prevents printers from running out of memory on documents with huge embedded photos. Triggers on phrases like "downsample images", "shrink the PDF", "reduce image DPI", "the printer keeps choking on this PDF".
---

# Downsample Images

Re-encode all raster images in a PDF at a capped DPI.

## Why it matters

Embedded images often arrive at 600+ DPI from cameras/scanners. Office printers print at 300–600 DPI native — extra pixels are wasted, balloon file size, and can exceed the printer's memory (causing partial page output or job failure).

## Inputs

- **Input PDF path** (required).
- **Target DPI** (optional) — default 300 for print, 150 for screen/proof, 600 for high-quality print shop.
- **Threshold DPI** (optional) — only downsample images above this DPI. Default 1.5 × target (e.g. target=300 → only touch images >450 DPI).
- **Output path** (optional) — defaults to `<input>-300dpi.pdf`.

## Tooling

Ghostscript with downsampling parameters tuned per image type.

### Recipe

```bash
gs -o output.pdf \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS=/printer \
   -dColorImageDownsampleType=/Bicubic \
   -dColorImageResolution=300 \
   -dGrayImageDownsampleType=/Bicubic \
   -dGrayImageResolution=300 \
   -dMonoImageDownsampleType=/Subsample \
   -dMonoImageResolution=600 \
   -dDownsampleColorImages=true \
   -dDownsampleGrayImages=true \
   -dDownsampleMonoImages=true \
   -dEmbedAllFonts=true \
   -dNOPAUSE -dBATCH \
   input.pdf
```

Adjust `*ImageResolution` values to the target DPI.

## Diagnosis

```bash
# Show embedded image dimensions and DPI
pdfimages -list input.pdf
```

Look at the `x-ppi`/`y-ppi` columns. Anything well above the target DPI is a downsample candidate.

## Verification

```bash
pdfimages -list output.pdf
ls -lh input.pdf output.pdf  # confirm size reduction
```

## Output

Downsampled PDF, typically 30–80% smaller. Original preserved.
