---
name: upload-to-printing-folder
description: Upload a print-ready PDF to the user's designated printing folder (local path or Google Drive), filing it into a subfolder by printer name or date per the user's saved preference. On first use, asks the user where their printing folder lives and how to organize subfolders, then persists that config. Triggers on phrases like "upload this to my printing folder", "send to print drive", "file this for printing".
---

# Upload to Printing Folder

Move or copy a finished PDF into the user's printing folder, organized into a subfolder by printer or date.

## Config

The skill stores its config at `$CLAUDE_USER_DATA/digital-printing/config.json` (resolving `CLAUDE_USER_DATA` with the standard fallback `${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins`).

Config schema:

```json
{
  "printing_folder": {
    "type": "local",
    "path": "/home/user/Documents/Printing"
  },
  "subfolder_strategy": "by-date",
  "default_printer": "office-laser"
}
```

`type` is `local` or `gdrive`. For `gdrive`, `path` is the Drive folder ID or path inside Drive.

`subfolder_strategy` is one of:
- `by-date` — `YYYY-MM-DD/`
- `by-printer` — `<printer-name>/`
- `by-printer-then-date` — `<printer-name>/YYYY-MM-DD/`
- `flat` — no subfolder

## First-run flow

If the config file doesn't exist:

1. Resolve `$CLAUDE_USER_DATA` and create `<root>/digital-printing/` if missing.
2. Ask the user:
   - "Where is your printing folder? (local path or Google Drive folder?)"
   - "How should I file print jobs? (by-date / by-printer / by-printer-then-date / flat)"
   - If `by-printer*`: "What printers do you have? Give me names I can use as folder names."
3. Write `config.json`.
4. Proceed with the upload.

Subsequent runs read the config and skip prompting unless the user explicitly says "change my printing folder" or "reconfigure".

## Inputs

- **PDF path** (required).
- **Printer** (optional) — overrides default for one upload, used when subfolder strategy involves printer name.
- **Date** (optional) — overrides today's date; useful for backdating.

## Workflow

1. Read or initialize config.
2. Compute the destination subfolder per strategy.
3. For `local` type:
   - `mkdir -p <printing_folder>/<subfolder>/`
   - `cp <input> <printing_folder>/<subfolder>/<basename>.pdf`
4. For `gdrive` type:
   - Use the available Google Drive MCP tools (e.g. `gws-personal__upload_file` or equivalent) to create the subfolder if missing and upload the file.
5. Verify the file exists at the destination and report the full path or Drive URL.

## Output

Confirmation message with the destination path. Do not delete the source file unless the user explicitly asks.

## Notes

- This skill never writes to `~/.claude/plugins/digital-printing/` — that's the plugin install dir, clobbered on update. Config lives in `$CLAUDE_USER_DATA`.
- The user-owned printing folder is *not* under `$CLAUDE_USER_DATA`; only the *pointer* to it is.
