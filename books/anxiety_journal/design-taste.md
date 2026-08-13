# Anxiety-Journal Design Taste

Reference books — pulled from operator-supplied Kindle-sample images:

- **Atomic Habits** — James Clear (Portfolio / Avery)
- **The Subtle Art of Not Giving a F\*ck** — Mark Manson (Harper)
- **Don't Believe Everything You Think (Expanded)** — Joseph Nguyen (Simon & Schuster)

All three publish 100% one-color interiors on cream stock, at small trims (5.25″×8″ to 5.5″×8.25″), in warm transitional serifs, with quiet chapter openers and generous margins. The North Star Journals line should sit visually next to these on a bedside table — feel like a book, not a workbook.

## Design Map

**Trim** 6×9 in (KDP journal standard — we keep this; the references are prose books, we are a journal)
**Paper** Cream (chosen at KDP upload; interior PDF stays black-only)
**Body font** EB Garamond 12 Regular, 11 pt, leading 15 pt, full-justified
**Body italic** EB Garamond 12 Italic
**Body bold** EB Garamond 12 Bold
**Heading font** Liberation Sans Bold — used only in ALL CAPS at small sizes for kickers and running heads
**Display numerals** EB Garamond 12 Bold — used oversized for chapter opener numerals
**Body ink** Pure black (#000000)
**Muted / caption ink** Neutral gray #6b6b6b
**Rule ink** Very light gray #d6d6d6
**Accent color** NONE — kill the teal. Every rule, kicker, and mark is black or gray.
**Running head** Sans small caps, page-top-outside, tiny (8.5 pt). Format: `4  ·  ANXIETY JOURNAL` (verso) / `ANXIETY JOURNAL  ·  5` (recto). Page number and title on the same top line — no separate bottom number.
**Chapter/section opener** Three elements, centered, vertically balanced: tiny sans kicker (`SECTION ONE`) → giant serif numeral (`I`) → title in serif bold. No subhead. No accent rule.
**Body paragraphs** Full-justified. First line of every paragraph after the first indented 0.15 in. First paragraph after a heading is not indented.
**Section-opening paragraph** Starts with a 3-line drop cap (raised initial, EB Garamond Bold).

## Taste DNA

### Principle 1  ·  Ink is enough  — RESTRAINT

- **Trigger** Reaching for a color to signal hierarchy (an accent rule, a colored kicker).
- **Decision** Don't. Black ink and gray. Nothing else.
- **Reason** The three reference interiors are 100% one-color. An accent color makes a self-help title read as "workbook printed at Kinko's" instead of "book bought at a bookstore." For a journal on a nightstand next to Atomic Habits, feel over function.
- **Evidence** Zero accent color in any of the reference sample images. All hierarchy is weight, size, and whitespace.
- **Trade-off** Emphasis has to come from typography alone. Section openers can't lean on a color pop.

### Principle 2  ·  The numeral IS the opener  — EMPHASIS

- **Trigger** Designing a section opener page.
- **Decision** Three elements max — kicker (`SECTION ONE`, tiny sans caps), giant serif numeral (`I` at ~140 pt), title (`Start Here` in serif bold at ~28 pt). Nothing else on the page. Centered.
- **Reason** Atomic Habits and Subtle Art both do exactly this. Adding a subtitle waters it down; the title alone must earn the page.
- **Evidence** Atomic Habits opener: dots-cluster + `1` + `The Surprising Power of Atomic Habits`. Subtle Art: `CHAPTER` + stylized `1` + horizontal rule + `Don't Try`. Both are under four elements.
- **Trade-off** No room to preview what's in the section. The title alone has to signal it.

### Principle 3  ·  Every section starts with a raised initial  — CONVENTION

- **Trigger** Opening the first paragraph of any prose page — how-to-use, exercise intro, weekly reflection.
- **Decision** Set the first letter as a 3-line drop cap in EB Garamond Bold.
- **Reason** Universal convention in trade nonfiction. Cheap warmth. Signals "you are at the start of something worth reading" without needing color or ornament.
- **Evidence** Subtle Art uses a 2-line raised initial (`Ch` on `Charles Bukowski...`). Atomic Habits uses `THE FATE OF BRITISH CYCLING` small-caps opener — same convention, different execution.
- **Trade-off** Slightly harder to word-wrap around; adds one measure of complexity to the exercise-page code.

### Principle 4  ·  Warm serif over neutral serif  — FEEL

- **Trigger** Choosing body type.
- **Decision** EB Garamond 12 (Claude Garamont revival, 2005). Not Liberation Serif / Times.
- **Reason** Liberation Serif reads as "office memo." Garamond reads as "book." For a journal a teen is supposed to want to open on a hard night, that difference matters more than font-file convenience.
- **Evidence** All three references use Garalde/transitional serifs — Kepler-family (Atomic Habits), Miller (Subtle Art), a Garamond variant (Don't Believe).
- **Trade-off** OTF instead of TTF (reportlab handles both). Slightly heavier file. Small-caps and old-style figures aren't in the free file — approximated with fake small caps if needed.

## What we deliberately do NOT lift

- **Trim size** — refs are 5.25×8 or 5.5×8.25 (prose books). We stay 6×9 (KDP journal standard, more writing room).
- **Full-page chapter numerals as art** — Subtle Art's giant blackletter `1` is beautiful but would need illustration work per number; we use the type-set serif numeral instead.
- **Dot-cluster decorative marks** — Atomic Habits chapter openers use scattered dots as a motif; skipping to keep the aesthetic austere.

## Concrete changes to `template.py`

1. Register EB Garamond 12 Regular / Bold / Italic as body fonts. Keep Liberation Sans / Sans Bold only for kickers, running heads, page numbers.
2. Replace `ACCENT = HexColor("#2f5d63")` with pure black wherever a rule is drawn. Delete all teal-colored elements.
3. Rewrite `draw_running_head` to render as small caps at the page top, format `<page>  ·  <TITLE>` on verso, mirrored on recto. Remove the separate bottom page number.
4. Rewrite `draw_section_title` to just three centered elements — kicker, giant numeral, title. Delete subhead, delete watermark experiment.
5. Add a `draw_drop_cap_paragraph(...)` helper. Use it on the first paragraph of every exercise/weekly-reflection intro.
6. Switch body prose to full-justified (custom line-fill using `pdfmetrics.stringWidth`) with 0.15″ first-line indent after paragraph 1.
7. Tracker: keep the structural fix from the last pass, but repaint every colored rule/kicker as gray or black.
