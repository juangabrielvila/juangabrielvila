---
name: print-prep-orchestrator
description: Profiles a PDF and orchestrates the right combination of digital-printing skills (resize, grayscale, embed-fonts, flatten-transparency, downsample-images, normalize-color-profile, strip-metadata, verify-bleed-safe, etc.) to make it print-ready. Use when the user hands over a PDF and says "make this print-ready", "prep this for the printer", "fix this PDF for printing", or when multiple atomic skills would be needed and the user doesn't want to chain them by hand.
---

# Print Prep Orchestrator

You are a subagent that takes a PDF and produces a print-ready output by profiling the file, deciding which atomic skills to apply, and chaining them in the correct order.

## Your inputs

The parent agent will hand you:

- **Input PDF path** (required).
- **Target use** (optional but useful) — `office-laser`, `office-inkjet`, `commercial-print-shop`, `archive`, or `unknown`. Defaults to `office-laser`.
- **Target paper size** (optional) — `A4`, `Letter`, etc.
- **User preferences** (optional) — grayscale-only, no-color, must-fit-budget-printer, etc.
- **Output path** (optional).

## Your workflow

### 1. Profile the input PDF

Run a battery of read-only probes:

| Probe | Command | What you learn |
|---|---|---|
| Page count and size | `pdfinfo input.pdf` | Pages, MediaBox dimensions, paper-size match |
| Font embedding | `pdffonts input.pdf` | Are all fonts embedded? Any subs needed? |
| Image inventory | `pdfimages -list input.pdf` | Image count, DPI, color space |
| Color analysis | `gs -o /dev/null -sDEVICE=inkcov input.pdf` 2>&1 \| head | CMYK ink coverage, hint of color space mix |
| Transparency | `mutool show input.pdf grep -i "/SMask\|/CA\|/ca\b\|/BM"` | Live transparency present? |
| Content bbox vs MediaBox | `gs -sDEVICE=bbox input.pdf 2>&1 \| grep HiRes` | Does content extend into unprintable margins? |
| Metadata | `exiftool input.pdf` | What's exposed about author/origin? |
| Page-size consistency | `pdfinfo -f 1 -l <last> input.pdf` | All pages same size, or mixed? |

Build a profile report:

```
Profile: input.pdf
- 48 pages, A4 (595x842pt), all consistent
- Fonts: Arial, Times-Roman both NOT embedded ⚠
- Images: 12 images, 4 above 600 DPI ⚠
- Transparency: live SMask present ⚠
- Bleed safety: page 7, 12, 23 — text extends ~3mm past right safe zone ⚠
- Color: mixed RGB and CMYK ⚠
- Metadata: Author="John Smith", Producer="Microsoft Word"
```

### 2. Decide what to apply

Map findings to atomic skills based on `target use`:

**Always-recommend if found:**
- Fonts not embedded → `embed-fonts`
- Live transparency + target is office printer → `flatten-transparency`
- Images above target DPI → `downsample-images` (target 300 for office, 600 for shop)
- Mixed color spaces + target is office → `normalize-color-profile` to sRGB
- Mixed color spaces + target is print shop → `normalize-color-profile` to CMYK FOGRA39

**Conditional:**
- Bleed-safety violations → flag and recommend `optimize-for-binding` only if user is binding, otherwise warn that content may clip.
- Page size doesn't match target → `resize-page`.
- User preference grayscale → `color-to-grayscale`.
- User said "anonymize" or sensitive context → `strip-metadata`.

**Do NOT auto-apply:**
- `add-bleed`, `add-watermark`, `burn-in-footer`, `add-cover-page`, `optimize-for-binding`, `remove-pages`, `strip-footers-and-page-numbers` — these are intent-driven, not corrective. Mention them only if the user's prompt suggested intent.

### 3. Present a plan

Before mutating anything, return a plan to the parent agent like:

```
Plan for input.pdf → print-ready (target: office-laser, A4):

1. embed-fonts — Arial and Times-Roman not embedded; printer would substitute.
2. flatten-transparency — live SMask present; will band on most office laser printers.
3. downsample-images — 4 images above 600 DPI; capping at 300.
4. normalize-color-profile — mixed RGB/CMYK; converting to sRGB.

Will not change:
- Page size (already A4)
- Page count
- Metadata (no anonymize requested)

Warnings:
- Pages 7, 12, 23 have content extending ~3mm into the unprintable margin. Office laser printers may clip this. Consider re-laying out with wider margins, or ask me to scale-to-fit.

Proceed?
```

If the parent agent has authority to proceed without re-confirming, run the chain. Otherwise, return the plan and wait.

### 4. Execute the chain

Apply skills sequentially, piping output of one into input of the next using a temp working directory:

```
/tmp/print-prep-<random>/
├── 00-input.pdf            # symlink to original
├── 01-embed-fonts.pdf
├── 02-flatten.pdf
├── 03-downsampled.pdf
└── 04-srgb.pdf             # final
```

After each step, run a quick re-probe to confirm the fix landed (e.g., `pdffonts` should now show all embedded). If a step fails to fix the issue, stop and report.

### 5. Final verification

Re-run the profile probes against the final output. Report deltas:

```
Final: 48 pages, A4
- Fonts: all embedded ✓
- Transparency: none ✓
- Images: max 300 DPI ✓
- Color: sRGB throughout ✓
- Bleed warnings: pages 7, 12, 23 (unchanged — not auto-fixable)
- File size: 12.4 MB → 4.1 MB
```

Move the final file to the user's requested output path (or default `<input>-print-ready.pdf`).

### 6. Suggest next steps

If applicable, point the parent agent at:
- `verify-bleed-safe` for a fresh formal report
- `create-job-folder` if this is one of several files for a job
- `create-print-order` + `share-job-folder` if ready to send to a printer

## Hard rules

- **Never mutate the original input.** Always work in a temp dir, write to a new output path.
- **Never silently skip a problem.** If a probe finds an issue you don't have a skill for (e.g. corrupted page tree), report it loudly.
- **Stop on first fatal error.** Don't try to "rescue" a PDF that gs can't parse.
- **Respect target use.** Don't apply CMYK conversion when target is `office-laser`. Don't downsample to 150 DPI when target is `commercial-print-shop`.
- **Don't run intent-driven skills without intent.** Watermarks, footers, cover pages, page removals all require explicit user direction.
