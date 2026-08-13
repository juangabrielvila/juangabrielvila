---
name: zip-job-folder
description: Zip a print job folder (PDFs + manifest + order document) into a single archive ready for transmission to a digital printer. Triggers on phrases like "zip the job folder", "package the print job", "make a zip for the printer".
---

# Zip Job Folder

Bundle a job folder and its order document into a single zip archive.

## Inputs

- **Job folder path** (required).
- **Output path** (optional) — defaults to `<job-folder>.zip` next to the folder.
- **Include order PDF only** (optional) — if `true`, skip `order.json` and `manifest.json` from the archive (some printers prefer just files + the human-readable order). Default `false`.

## Workflow

1. Verify the folder exists and contains at least `files/` and `manifest.json`.
2. Sanity-check: confirm no individual file is over a sensible threshold (e.g. 200 MB) — flag to user if so, since some email systems will reject the archive.
3. Run zip:
   ```bash
   cd "$(dirname "$JOB")" && zip -r "${JOB_BASENAME}.zip" "$JOB_BASENAME"
   ```
4. Report zip path and size.

## Caveats

- Zip preserves original PDFs uncompressed-equivalent; PDFs don't compress well, so the zip size will be close to the sum of file sizes.
- For very large jobs (>50 MB), suggest `share-job-folder` with the Google Drive option instead — many email systems cap attachments at 25 MB.

## Output

Zip path. Suggest `share-job-folder` as the natural next step.
