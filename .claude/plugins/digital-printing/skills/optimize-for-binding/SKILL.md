---
name: optimize-for-binding
description: Adjust a PDF's layout for binding — add a gutter (inner margin), mirror margins for duplex printing so the binding edge is consistent, and optionally shift content outward. Triggers on phrases like "prep for binding", "add gutter", "mirror margins for duplex", "binding-friendly layout".
---

# Optimize PDF for Binding

Shift content to leave room for a binding gutter without cropping. Supports single-sided (uniform shift) or double-sided (mirror left/right shift) layout.

## Inputs

- **Input PDF path** (required).
- **Gutter** (required) — extra inner margin in mm (typical: 10–15mm for spiral/comb, 15–20mm for perfect bound).
- **Duplex** (optional, default `true`) — if `true`, mirror the shift: odd pages shift right, even pages shift left. If `false`, all pages shift right (single-sided).
- **Output path** (optional) — defaults to `<input>-bound.pdf`.

## Tooling

`pdfjam` (from `texlive-extra-utils`) handles gutter/binding offsets cleanly. Ghostscript can also do it via `pdfwrite` with a translation matrix, but `pdfjam` is more readable.

### pdfjam recipe — duplex mirror

```bash
pdfjam --offset "10mm 0mm" --twoside --outfile output.pdf input.pdf
```

`--twoside` automatically mirrors odd/even page offsets. `--offset "X Y"` shifts content (positive X = right).

### Single-sided uniform shift

```bash
pdfjam --offset "10mm 0mm" --outfile output.pdf input.pdf
```

## Caveats

- Shifting content can push the outer edge into the printer's unprintable margin. Always run `verify-bleed-safe` after this skill to confirm content still fits within the printable area.
- For docs already laid out with a gutter (e.g. typeset books), don't double-up — ask the user first.
- For perfect-bound thick books, gutter should *increase* with page count (creep allowance). Out of scope for v1; flag to user if doc is >100 pages.

## Workflow

1. Confirm `pdfjam` is installed (`command -v pdfjam`); if not, `sudo apt install texlive-extra-utils`.
2. Run the offset.
3. Suggest running `verify-bleed-safe` next.

## Output

Bound-ready PDF. Original preserved.
