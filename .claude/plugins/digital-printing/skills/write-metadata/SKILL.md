---
name: write-metadata
description: Set or replace PDF metadata — title, author, subject, keywords. Useful for cataloguing scanned documents or standardizing batch outputs. Triggers on phrases like "set the title of this PDF", "write metadata", "tag this PDF with author/keywords".
---

# Write PDF Metadata

Set the standard PDF metadata fields.

## Inputs

- **Input PDF path** (required).
- **Title** (optional).
- **Author** (optional).
- **Subject** (optional).
- **Keywords** (optional) — comma-separated.
- **Output path** (optional) — defaults to overwriting `<input>` (after backup) or `<input>-tagged.pdf`. Confirm with user.

## Tooling

`exiftool` writes both the Info dictionary and XMP cleanly.

### Recipe

```bash
exiftool \
  -Title="Quarterly Report" \
  -Author="Daniel Rosehill" \
  -Subject="Internal review" \
  -Keywords="quarterly,2026,review" \
  -overwrite_original_in_place=false \
  -o output.pdf input.pdf
```

## Verification

```bash
exiftool output.pdf | grep -E "Title|Author|Subject|Keywords"
```

## Workflow

1. Confirm fields with user — if any are missing, ask before assuming defaults.
2. Run exiftool.
3. Verify and report.

## Output

PDF with new metadata. Original preserved (unless user explicitly asked to overwrite).
