---
name: normalize-color-profile
description: Standardize a PDF's color profile — convert to sRGB (default, best for office digital printers) or CMYK FOGRA39 (for commercial print shops). Eliminates color-shift surprises caused by mixed/unspecified color spaces. Triggers on phrases like "normalize colors", "convert to sRGB", "set CMYK profile", "fix weird colors on print".
---

# Normalize Color Profile

Convert all color content in a PDF to a single, consistent ICC profile.

## Why it matters

PDFs accumulate color from many sources — RGB photos from a phone, CMYK ads from InDesign, untagged office-doc colors. Printers interpret unspecified color unpredictably. Normalizing to one profile eliminates that variance.

## Inputs

- **Input PDF path** (required).
- **Target profile** (optional) — default `sRGB` for office digital printing. Other choices:
  - `sRGB` — IEC 61966-2.1, the safe default for office laser/inkjet, screens, and most consumer/digital workflows.
  - `CMYK-FOGRA39` — ISO Coated v2, European commercial print standard.
  - `CMYK-GRACoL` — North American commercial print standard.
  - `Gray` — convert all to grayscale (use `color-to-grayscale` skill instead for that case).
- **Output path** (optional) — defaults to `<input>-<profile>.pdf`.

## Tooling

Ghostscript with `pdfwrite` and `ColorConversionStrategy`.

### sRGB recipe (default)

```bash
gs -o output.pdf \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=sRGB \
   -sProcessColorModel=DeviceRGB \
   -dCompatibilityLevel=1.4 \
   -dEmbedAllFonts=true \
   -dNOPAUSE -dBATCH \
   input.pdf
```

### CMYK FOGRA39 recipe

```bash
gs -o output.pdf \
   -sDEVICE=pdfwrite \
   -sColorConversionStrategy=CMYK \
   -sProcessColorModel=DeviceCMYK \
   -sDefaultCMYKProfile=ISOcoated_v2_eci.icc \
   -dCompatibilityLevel=1.4 \
   -dEmbedAllFonts=true \
   -dNOPAUSE -dBATCH \
   input.pdf
```

The ICC profile file (`ISOcoated_v2_eci.icc`) must be available — install `icc-profiles` on Debian/Ubuntu, or download from ECI.

## Verification

```bash
gs -o /dev/null -sDEVICE=inkcov input.pdf  # before
gs -o /dev/null -sDEVICE=inkcov output.pdf # after
```

`inkcov` reports CMYK ink coverage per page; useful sanity check after CMYK conversion.

## Workflow

1. Probe input color spaces — if everything is already sRGB, skip and report "no-op".
2. Confirm target profile with user if unclear.
3. Run conversion.
4. Verify and report profile of output.

## Output

Color-normalized PDF.
