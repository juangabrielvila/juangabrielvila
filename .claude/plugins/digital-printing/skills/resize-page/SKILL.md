---
name: resize-page
description: Rescale a PDF's page size — e.g. US Letter to A4, A4 to Letter, A5 to A4, or any custom dimensions. Use when the user wants to convert a PDF between paper sizes for digital printing. Triggers on phrases like "resize this PDF to A4", "convert to letter size", "change page size".
---

# Resize PDF Page Size

Rescale every page of a PDF to a different paper size while preserving content proportionally.

## Inputs

- **Input PDF path** (required).
- **Target size** (required) — `A4`, `Letter`, `A5`, `Legal`, `A3`, or custom `WIDTHxHEIGHT` in mm or pt.
- **Output path** (optional) — defaults to `<input>-<size>.pdf` next to the input.
- **Fit mode** (optional) — `scale` (default, fit content to new size, preserves aspect ratio) or `pad` (keep original content size, add margins to reach new size).

## Tooling

Prefer `ghostscript` (`gs`) — it's pre-installed on most Linux systems and handles content scaling robustly. Fall back to `pdfjam` (from `texlive-extra-utils`) for simpler page-size remapping.

### Common page sizes (pt)

- A4: 595 x 842
- Letter: 612 x 792
- Legal: 612 x 1008
- A5: 420 x 595
- A3: 842 x 1191

### Ghostscript scale-to-fit recipe

```bash
gs -o output.pdf \
   -sDEVICE=pdfwrite \
   -dPDFFitPage \
   -dFIXEDMEDIA \
   -dDEVICEWIDTHPOINTS=595 \
   -dDEVICEHEIGHTPOINTS=842 \
   input.pdf
```

Adjust `DEVICEWIDTHPOINTS` / `DEVICEHEIGHTPOINTS` for the target size.

### pdfjam alternative

```bash
pdfjam --paper a4paper --outfile output.pdf input.pdf
```

## Workflow

1. Verify the input PDF exists and is readable.
2. Confirm `gs` is installed (`command -v gs`). If not, install via `sudo apt install ghostscript`.
3. Run the conversion.
4. Verify output: `pdfinfo output.pdf | grep "Page size"` to confirm the new dimensions.
5. Report back the input/output paths and the size change.

## Output

Write the resized PDF and report the path. Do not delete the original.
