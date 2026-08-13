# Assets — Before the Test

Drop operator-designed art here. The generator embeds anything in this folder
at 300 DPI into the interior PDF at the matching slot.

## Expected files (referenced by `spread_preview.py` and the eventual full build)

- `spread1-verso-illustration.png` — botanical + wave illustration at the foot
  of the illustrated title page (Spread 1 verso). Approx 6″ × 3″, RGB, 300 DPI,
  transparent background if you want the wave to bleed off the trim.
- `spread1-recto-diagram.png` — circular practice diagram for the steps page
  (Spread 1 recto). Approx 2″ × 2″, RGB, 300 DPI, transparent background.
- `spread2-verso-leaf.png` — small botanical accent for the reminder page
  (Spread 2 verso, top-right). Approx 0.6″ × 0.6″, RGB, 300 DPI, transparent.
- `spread2-recto-closing.png` — optional botanical accent for the closing
  callout at the foot of the after-practice page. Optional.

## Format notes

- **PNG** with transparent background is preferred. JPEG works if the art has
  no soft edges.
- **RGB** color mode. KDP converts to their print CMYK profile at upload; the
  PDF stays RGB in-repo.
- **300 DPI at final size** — undersized art will be upscaled and look soft.
- **Trim / bleed** — if the art is meant to touch the page edge, size it a bit
  larger than the visible area and the layout code will crop it at trim.

## Naming discipline

Keep filenames stable — the layout code references them by exact filename. If
you rename, update the corresponding path in `spread_preview.py` (and the
full-book template once the design is signed off).
