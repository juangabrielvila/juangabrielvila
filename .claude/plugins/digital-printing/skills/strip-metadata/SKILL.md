---
name: strip-metadata
description: Remove all metadata from a PDF — author, title, producer, creation date, comments, embedded XMP, and document info dictionary. Useful before sharing or printing externally. Triggers on phrases like "strip metadata", "remove author info", "scrub PDF metadata", "anonymize this PDF".
---

# Strip PDF Metadata

Wipe all identifying metadata from a PDF.

## Inputs

- **Input PDF path** (required).
- **Output path** (optional) — defaults to `<input>-clean.pdf`.

## What gets stripped

- Document Info dictionary: `/Title`, `/Author`, `/Subject`, `/Keywords`, `/Creator`, `/Producer`, `/CreationDate`, `/ModDate`.
- XMP metadata stream.
- Annotations and comments (optional, ask user).

## Tooling

`exiftool` is the most thorough — it handles both legacy Info dict and XMP.

### Recipe

```bash
exiftool -all:all= -overwrite_original_in_place=false -o output.pdf input.pdf
```

To also remove XMP and re-linearize cleanly, follow up with `qpdf`:

```bash
qpdf --linearize output.pdf output-final.pdf && mv output-final.pdf output.pdf
```

## Verification

```bash
exiftool output.pdf
pdfinfo output.pdf
```

Both should show empty/default values for Author, Title, Producer, etc.

## Caveats

- `Producer` and `Creator` may repopulate if downstream tools touch the file. Run `strip-metadata` last in any pipeline.
- Embedded fonts and form metadata are not stripped — this skill targets identifying info only.

## Output

Metadata-stripped PDF. Original preserved.
