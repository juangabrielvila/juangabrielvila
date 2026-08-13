---
name: color-to-grayscale
description: Convert a color PDF to grayscale (black-and-white) for monochrome digital printing — saves toner and avoids color-mismatch issues. Triggers on phrases like "convert PDF to grayscale", "make it black and white", "remove color from PDF", "monochrome PDF".
---

# Convert PDF to Grayscale

Strip color from every page of a PDF, producing a grayscale-only output suitable for monochrome printing.

## Inputs

- **Input PDF path** (required).
- **Output path** (optional) — defaults to `<input>-grayscale.pdf`.

## Tooling

Use `ghostscript` with the `pdfwrite` device and a grayscale color conversion strategy. This is the most reliable method — it converts both raster images and vector content.

### Recipe

```bash
gs -sOutputFile=output.pdf \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=Gray \
   -sProcessColorModel=DeviceGray \
   -dCompatibilityLevel=1.4 \
   -dNOPAUSE -dBATCH \
   input.pdf
```

## Workflow

1. Verify input exists.
2. Confirm `gs` is installed.
3. Run the conversion.
4. Spot-check by rendering page 1 to PNG and confirming no color channels:
   ```bash
   gs -sDEVICE=png16m -r72 -o /tmp/check.png -dFirstPage=1 -dLastPage=1 output.pdf
   ```
5. Report file size delta — grayscale PDFs are usually significantly smaller.

## Output

Grayscale PDF written to the requested path. Original is not modified.

## Caveats

- If the source PDF embeds CMYK or spot colors, the conversion is still safe but may flatten subtle tones.
- Text remains crisp; embedded JPEGs are re-compressed as grayscale JPEGs.
