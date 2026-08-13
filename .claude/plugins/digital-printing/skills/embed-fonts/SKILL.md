---
name: embed-fonts
description: Force-embed all fonts in a PDF — fixes the most common cause of "looks fine on screen, wrong on the printer" issues. If the printer doesn't have the font, it substitutes a fallback and layout breaks. Triggers on phrases like "embed fonts", "fix font issues", "fonts looking wrong on print".
---

# Embed All Fonts

Re-process a PDF so every font used is fully embedded.

## Why it matters

Non-embedded fonts trigger printer-side substitution. Common substitutions (Arial → Helvetica → Liberation Sans) cause subtle width changes that ripple into reflowed lines, broken tables, and shifted page breaks.

## Inputs

- **Input PDF path** (required).
- **Output path** (optional) — defaults to `<input>-embedded.pdf`.

## Diagnosis (pre-check)

```bash
pdffonts input.pdf
```

Look at the `emb` and `sub` columns:
- `yes yes` — fully embedded subset (fine).
- `yes no` — fully embedded full font (fine).
- `no no` — NOT embedded (problem).

## Tooling

Ghostscript with `-dEmbedAllFonts=true -dSubsetFonts=true` re-runs the PDF through pdfwrite and embeds whatever it can find on the system.

### Recipe

```bash
gs -o output.pdf \
   -sDEVICE=pdfwrite \
   -dPDFSETTINGS=/prepress \
   -dEmbedAllFonts=true \
   -dSubsetFonts=true \
   -dCompatibilityLevel=1.4 \
   -dNOPAUSE -dBATCH \
   input.pdf
```

`/prepress` preset includes high-quality embedding settings.

## Verification

```bash
pdffonts output.pdf
```

Every row should show `emb=yes`. If any are still `no`, the font isn't installed on the system — install via `fc-list` / `apt install`, then re-run.

## Caveats

- If the source PDF references a font that isn't installed locally and isn't embedded, gs cannot embed it and will substitute. The output will still print "consistently" but with the substitution baked in — verify visually.
- Some commercial fonts have embedding restrictions in their license; gs respects flags. If embedding is denied, gs warns.

## Output

Font-embedded PDF.
