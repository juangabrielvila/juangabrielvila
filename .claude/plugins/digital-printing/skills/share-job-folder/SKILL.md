---
name: share-job-folder
description: Share a print job folder with a digital printer or other recipients — via email (with the zipped folder attached) and/or Google Drive (folder share link). Pulls customer contact info and order details from the job folder for the message body. Triggers on phrases like "send this to the printer", "share the job folder", "email the print job", "share with the printer".
---

# Share Job Folder

Send a finished print job folder to a printer, print shop, or collaborator.

## Inputs

- **Job folder path** (required).
- **Recipient(s)** (required) — one or more email addresses, or a printer/contact name resolved from the contacts in config.
- **Channels** (optional) — any combination of:
  - `email` — attach zipped folder.
  - `email-with-link` — upload to Drive, share, paste link in email body (best for jobs over email size limits).
  - `gdrive` — upload to Drive, set sharing on the Drive folder, return the share URL.
- **Message** (optional) — extra text to include in the email body. Auto-generated body uses the order document.
- **Subject** (optional) — default `Print job: <job-name> [<copies> copies]`.

## Auto-generated email body

Pulled from `<job>/order.json`:

- Greeting (if recipient is in known printer contacts and has a saved name).
- Job summary: page total, copies, color/duplex/binding spec.
- Due date if set.
- Special notes verbatim.
- Customer contact block (name, email, phone) for printer reply.
- File list (filenames, pages, copies).
- Optional sentence: "Order spec attached as `order.pdf`. Files in `files/`. Full archive attached / linked below."

## Workflow

### Email (attach zip)

1. If no zip exists at `<job>.zip`, invoke `zip-job-folder` first.
2. Check zip size — if over 20 MB, recommend switching to `email-with-link` or `gdrive`.
3. Compose email using the auto-generated body.
4. Send via the user's configured email channel — Resend (`resend-personal__send-email`) or Google Workspace (`gws-personal__send_email`). Choice of provider depends on whether the user wants the message in their Sent folder (use Gmail/`gws-personal`) or whether it's a transactional send (use Resend).
5. Report `Sent to <recipient> at <time>`.

### Email-with-link

1. Upload the job folder (or its zip) to Google Drive via `gws-personal__upload_file` / `gws-personal__create_folder`.
2. Set sharing per the recipient: `gws-personal__share_file` with `role=reader` (or `commenter` if requested).
3. Compose email body with the share link in place of an attachment.
4. Send.

### Google Drive only

1. Upload to Drive.
2. Share with recipient(s).
3. Return the share URL — no email sent.

## Config

Optional contacts under `$CLAUDE_USER_DATA/digital-printing/config.json`:

```json
{
  "printer_contacts": [
    {
      "name": "Office Depot — Talpiot",
      "email": "talpiot-print@example.com",
      "preferred_channel": "email-with-link"
    }
  ]
}
```

When the user says "send to Office Depot Talpiot", resolve the email from this list and use the saved preferred channel.

## Workflow summary

1. Validate job folder has `order.json` and `order.pdf` — if not, suggest running `create-print-order` first.
2. Resolve recipient(s) and channel(s).
3. For email channels, ensure a zip exists or build one inline.
4. For Drive channels, upload and share.
5. Send / report.

## Output

Confirmation with: recipient list, channels used, share URL (if any), email message ID (if any).
