# CLAUDE.md

Context for Claude Code (or Cowork) working in this repository. Read this in full at the start of every session.

## Mission

Publish a portfolio of low-content books on Amazon KDP generating **$350+/month in royalties within 6 months**. This is a volume + niche-discipline play, not a single hit. Target: **25–35 titles live within 90 days**.

## Operator (the human)

- Skill: graphics/visual design — this is the moat vs. AI-slop competitors
- Time: 10–15 hrs/week (~40–60 hrs/month)
- Audience: none required — KDP is search-driven
- Budget: minimal; ads only after organic winners emerge (month 3+)
- **Cannot** upload to KDP via API — no public upload API exists. Operator uploads manually. Claude never attempts to automate KDP uploads.

## Claude's role

Own everything up to the KDP upload button:
- Niche validation with real Amazon BSR / review-count data
- Title, subtitle, and description drafting
- Backend keywords (7 per title) and category picks (2 per title)
- Interior generation — Python + reportlab for journals, puzzle books, planners, activity books; brief templates for coloring books that the operator polishes
- Cover briefs (first-pass, operator finishes)
- Launch tracker, review-request insert templates, pricing experiments
- Post-launch: BSR monitoring, keyword iteration, AMS ad targeting drafts

## Guardrails — non-negotiable

- **No copyrighted/trademarked material**: no copyrighted characters, brand names, sports team names, or trademarked event names (e.g. never "FIFA World Cup" — say "2027 global soccer tournament"). Amazon actively delists infringing titles.
- **KDP AI-disclosure rules**: code-generated interiors (puzzle grids, journal prompts) don't require disclosure. AI-generated illustrations do — flag any AI art content clearly.
- **No income guarantees.** Talk in probabilities and historical reference points, not promises.
- **No ToS-violating scraping.** Public best-seller/search-result pages via WebFetch/WebSearch are fine. Never automate at volumes that resemble scraping.

## Tech stack

- **Interior generation:** Python + `reportlab`
- **Output format:** print-ready PDF (interior + separate full cover PDF)
- **Tracking:** Google Sheet or repo CSV (columns below)
- No web app / no database — this is a content-generation + ops repo

## Interior specs (KDP-ready)

| | Journals | Coloring/Activity |
|---|---|---|
| Trim size | 6x9 in | 8.5x11 in |
| Bleed | none (text-only) | 0.125 in all sides for full-page art |
| Margins | 0.75 in gutter, 0.5 in outside, 0.6 in top/bottom | 0.5 in all around + 0.125 in bleed |
| Gutter | Mirrored odd/even — mandatory for perfect binding | same |
| Fonts | Embed all; no commercial-print-restricted licenses | same |
| Page count | 100–120 (royalty sweet spot at $6.99–$9.99) | same |

## Cover specs (KDP-ready)

- Full cover PDF (front + spine + back), sized to KDP's cover calculator output
- 300 DPI, CMYK
- 0.125 in bleed on outside edges
- Spine width varies by page count — use KDP's per-title calculator
- Leave barcode placeholder — KDP auto-generates

## Validated niches (starting set)

1. **Junk Journal Starter Kits** — Papercrafts | Mixed Media — fast interior (2–3 hrs, code-generated ephemera)
2. **Bold-Line Mushroom Coloring for Adults** — Coloring Books for Grown-Ups | Flowers & Plants — medium (operator vector art)
3. **Anxiety Journal for Teens** — Teen Mental & Emotional Health | Anxieties & Phobias — fast (fully code-generated; template exists, see Assets)
4. **Vision Board Book for 2027** — Motivational | Mysticism/Spirituality — medium (cut-out word grids, affirmations)

Full rationale/signal data and the 20-title draft library (5 titles × 4 niches) live in the original project brief — don't re-derive titles that already exist there; ask if you need the list re-surfaced.

## Workflow per title

1. Claude generates: interior PDF, title/subtitle/description, 7 keywords, 2 categories, cover brief
2. Operator polishes cover, sanity-checks interior, uploads to KDP manually
3. Operator publishes; Claude adds the title to the tracker with launch date
4. Claude monitors weekly: BSR, sales rank velocity, keyword ranking
5. After 60 days: Claude flags winners for AMS ad targeting drafts; flags duds for metadata iteration (new title/keywords/cover) or delisting

## Weekly cadence (10–15 hrs/week)

- 5–6 new titles generated per week
- Operator upload session: 1–2 hrs/week, batched
- **Monday:** Claude runs BSR check on all live titles, reports winners/losers
- **Friday:** Claude drafts next week's title queue for operator approval

## Tracker columns

`Title | Niche | Status | Upload Date | ASIN | BSR (weekly) | Sales | Notes`

## Success metrics

- Month 3: organic sales on 5+ titles
- Month 4: $150+ MRR
- Month 6: $350+ MRR (goal)
- Month 9: $750+ MRR (stretch)

## Assets already produced

- Demo interior PDF: *The Calm Down Book* (108 pages, 6x9, mirrored gutter) — operator has this file from a prior session; use as the template base for anxiety-journal titles #2–#5
- Draft title library — 20 titles across the 4 niches above

## Pen names (assigned)

| Niche | Pen name |
|---|---|
| Junk Journal Starter Kits | Marigold & Ink |
| Bold-Line Mushroom Coloring for Adults | Quiet Woods Press |
| Anxiety Journal for Teens | North Star Journals |
| Vision Board Book for 2027 | The Intention Press |

Checked against active Amazon author/imprint pages at time of selection (Aug 2026) — no direct collisions found. Re-check before final KDP account setup in case of newer registrations.

## Open operator decisions (resolve before/at kickoff)

- KDP account region (US / UK / both)
- Print vs. Kindle vs. both — default recommendation: paperback-first for low-content
- Price ceiling — default $6.99–$9.99 paperback, $2.99 Kindle
- Preferred cover-polish tool (Illustrator / Figma / Affinity)

## First tasks when this project starts

1. Confirm pen names for each niche
2. Generate the remaining 4 anxiety-journal interior PDFs (titles #2–#5) using the Calm Down Book template as the base
3. Draft cover briefs for one title per niche (4 briefs total)
4. Set up the tracker (Google Sheet or repo CSV) with the columns above

## What Claude should avoid

- Don't attempt KDP uploads or claim to have published anything — that's manual, operator-only
- Don't fabricate BSR/sales data — pull real numbers via search/fetch or say data isn't available
- Don't reuse copyrighted names/IP in titles, keywords, or cover briefs
- Don't promise or imply guaranteed earnings in any generated copy
