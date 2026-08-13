"""Design-lock preview for the 4-page exercise unit.

Feedback pivoted the anxiety-journal aesthetic from an austere prose-book look
to an illustrated wellness journal (Reset in 5 Minutes / 02 Soft Organic).
This script builds ONE 4-page unit — 5-4-3-2-1, the sensory grounding exercise
— so we can lock the pattern before regenerating the full 108-page book.

Structure:
  Spread 1 (pp 1-2)  Instructions
    verso  ·  illustrated title + intro
    recto  ·  numbered steps + circular practice diagram + pull-quote sidebar
  Spread 2 (pp 3-4)  Writing
    verso  ·  condensed reminder at top + ruled writing area
    recto  ·  continuation ruled writing area + closing prompt

Everything is drawn programmatically for now. Where operator art will slot in,
I draw a light vector placeholder and note the intended asset path.
"""

from __future__ import annotations

import math
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

# ---------- page geometry (matches the 108pp book) ----------

INCH = 72.0
PAGE_W = 6 * INCH
PAGE_H = 9 * INCH

GUTTER = 0.75 * INCH
OUTSIDE = 0.5 * INCH
TOP = 0.6 * INCH
BOTTOM = 0.6 * INCH

# ---------- palette (Reset in 5 Minutes + 02 Soft Organic) ----------

INK        = HexColor("#1D2426")   # warm near-black
INK_SOFT   = HexColor("#3C4245")   # body text on tinted grounds
MUTED      = HexColor("#7A8189")   # captions, kickers
HAIR       = HexColor("#D6D2C8")   # hairline rules
SAGE       = HexColor("#7C9A82")   # primary botanical accent
SAGE_SOFT  = HexColor("#B8CDBD")
CORAL      = HexColor("#D97757")   # warm accent
CORAL_SOFT = HexColor("#EFCBB8")
BLUE       = HexColor("#6B87A6")   # cool balance
BLUE_SOFT  = HexColor("#C4D2E1")
CREAM_TILE = HexColor("#F0EEE6")   # sidebar/callout ground
LEAF       = HexColor("#A2B79A")

FONT_SERIF        = "BodySerif"
FONT_SERIF_BOLD   = "BodySerifBold"
FONT_SERIF_ITALIC = "BodySerifItalic"
FONT_SANS         = "Sans"
FONT_SANS_BOLD    = "SansBold"

_FONTS_DIR = Path(__file__).parent / "fonts"

_FONT_PATHS = {
    FONT_SERIF:        str(_FONTS_DIR / "EBGaramond12-Regular.ttf"),
    FONT_SERIF_BOLD:   str(_FONTS_DIR / "EBGaramond12-Bold.ttf"),
    FONT_SERIF_ITALIC: str(_FONTS_DIR / "EBGaramond12-Italic.ttf"),
    FONT_SANS:         "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    FONT_SANS_BOLD:    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
}


def _register_fonts() -> None:
    for name, path in _FONT_PATHS.items():
        try:
            pdfmetrics.registerFont(TTFont(name, path))
        except Exception:  # already registered
            pass


# ---------- text helpers ----------

def wrap(text: str, font: str, size: float, max_w: float) -> list[str]:
    if not text:
        return [""]
    words = text.split()
    lines, line = [], ""
    for w in words:
        cand = f"{line} {w}".strip()
        if pdfmetrics.stringWidth(cand, font, size) <= max_w:
            line = cand
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def draw_justified(c: Canvas, words: list[str], x: float, y: float,
                   font: str, size: float, max_w: float, last: bool) -> None:
    if not words:
        return
    if last or len(words) == 1:
        c.setFont(font, size)
        c.drawString(x, y, " ".join(words))
        return
    total = sum(pdfmetrics.stringWidth(w, font, size) for w in words)
    gap = (max_w - total) / (len(words) - 1)
    c.setFont(font, size)
    cx = x
    for w in words:
        c.drawString(cx, y, w)
        cx += pdfmetrics.stringWidth(w, font, size) + gap


def draw_paragraph(c: Canvas, text: str, x: float, y: float, w: float,
                   font: str = FONT_SERIF, size: float = 10.5, leading: float = 14.5,
                   justify: bool = True, color=INK) -> float:
    c.setFillColor(color)
    words_all = text.split()
    yy = y
    remaining = words_all
    while remaining:
        take = []
        for wd in remaining:
            cand = " ".join(take + [wd])
            if pdfmetrics.stringWidth(cand, font, size) <= w:
                take.append(wd)
            else:
                break
        if not take:
            take = [remaining[0]]
        rest = remaining[len(take):]
        if justify:
            draw_justified(c, take, x, yy, font, size, w, not rest)
        else:
            c.setFont(font, size)
            c.drawString(x, yy, " ".join(take))
        yy -= leading
        remaining = rest
    return yy


# ---------- illustration primitives (placeholders — replace with operator art) ----------

def draw_wave(c: Canvas, x: float, y: float, w: float, h: float, color=SAGE_SOFT) -> None:
    """A soft horizontal wave silhouette. Placeholder for operator watercolor.
    Fills roughly a rectangle w×h with a wave whose peaks rise ~h and troughs
    touch the bottom of the rect."""
    c.setFillColor(color)
    c.setStrokeColor(color)
    n = 3  # number of full waves across
    step = w / (n * 2)
    p = c.beginPath()
    p.moveTo(x, y)
    for i in range(n * 2 + 1):
        cx = x + i * step
        cy = y + h if i % 2 else y + h * 0.35
        if i == 0:
            p.moveTo(cx, y)
        else:
            prev_cx = x + (i - 1) * step
            mid_x = (prev_cx + cx) / 2
            p.curveTo(mid_x, y + (h if i % 2 else h * 0.35),
                      mid_x, cy,
                      cx, cy)
    p.lineTo(x + w, y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def draw_leaf_sprig(c: Canvas, cx: float, cy: float, size: float = 40.0, color=SAGE) -> None:
    """A minimal 3-leaf sprig — line art. Placeholder for a botanical illustration."""
    c.setStrokeColor(color)
    c.setLineWidth(0.9)
    # stem
    c.line(cx, cy - size * 0.5, cx + size * 0.3, cy + size * 0.5)
    # leaves (three ellipses along the stem)
    for t in (0.2, 0.5, 0.8):
        px = cx + size * 0.3 * t
        py = cy - size * 0.5 + size * t
        # left leaf
        p1 = c.beginPath()
        p1.moveTo(px, py)
        p1.curveTo(px - size * 0.35, py + size * 0.05,
                   px - size * 0.35, py + size * 0.25,
                   px - size * 0.05, py + size * 0.15)
        p1.curveTo(px - size * 0.15, py + size * 0.10,
                   px - size * 0.15, py + size * 0.05,
                   px, py)
        p1.close()
        c.drawPath(p1, fill=0, stroke=1)
        # right leaf
        p2 = c.beginPath()
        p2.moveTo(px, py)
        p2.curveTo(px + size * 0.35, py + size * 0.05,
                   px + size * 0.35, py + size * 0.25,
                   px + size * 0.05, py + size * 0.15)
        p2.curveTo(px + size * 0.15, py + size * 0.10,
                   px + size * 0.15, py + size * 0.05,
                   px, py)
        p2.close()
        c.drawPath(p2, fill=0, stroke=1)


def draw_star(c: Canvas, cx: float, cy: float, r: float = 3.0, color=INK) -> None:
    i = r * 0.22
    p = c.beginPath()
    p.moveTo(cx, cy + r)
    for pt in [(cx + i, cy + i), (cx + r, cy), (cx + i, cy - i),
               (cx, cy - r), (cx - i, cy - i), (cx - r, cy),
               (cx - i, cy + i)]:
        p.lineTo(*pt)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(INK)


def draw_practice_diagram(c: Canvas, cx: float, cy: float, radius: float = 48.0) -> None:
    """A circular practice diagram — placeholder for the operator's illustration.
    Draws a hairline circle with the five sense counts around it (5, 4, 3, 2, 1).
    """
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.8)
    c.circle(cx, cy, radius, fill=0, stroke=1)

    # five counts spaced around the circle, starting at top
    counts = [("5", "SEE", SAGE),
              ("4", "TOUCH", CORAL),
              ("3", "HEAR", BLUE),
              ("2", "SMELL", SAGE),
              ("1", "TASTE", CORAL)]
    for i, (num, label, color) in enumerate(counts):
        angle = math.pi / 2 - (i * 2 * math.pi / 5)
        nx = cx + radius * math.cos(angle)
        ny = cy + radius * math.sin(angle)
        # small colored dot
        c.setFillColor(color)
        c.circle(nx, ny, 3, fill=1, stroke=0)
        # numeral outside the circle
        c.setFillColor(INK)
        c.setFont(FONT_SERIF_BOLD, 14)
        ox = cx + (radius + 16) * math.cos(angle)
        oy = cy + (radius + 16) * math.sin(angle) - 5
        c.drawCentredString(ox, oy, num)
        # sense label further out
        c.setFillColor(MUTED)
        c.setFont(FONT_SANS_BOLD, 7)
        lx = cx + (radius + 32) * math.cos(angle)
        ly = cy + (radius + 32) * math.sin(angle) - 3
        c.drawCentredString(lx, ly, label)


def draw_asset_slot(c: Canvas, x: float, y: float, w: float, h: float,
                    label: str) -> None:
    """A hairline dashed rectangle showing an intended asset slot for the operator."""
    c.setStrokeColor(HAIR)
    c.setDash(3, 3)
    c.setLineWidth(0.4)
    c.rect(x, y, w, h, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(MUTED)
    c.setFont(FONT_SANS, 7)
    c.drawString(x + 4, y + h - 10, "ASSET SLOT")
    c.setFont(FONT_SANS, 6.5)
    c.drawString(x + 4, y + h - 20, label)
    c.setFillColor(INK)


# ---------- page-level draw functions ----------

def is_recto(page_num: int) -> bool:
    return page_num % 2 == 1


def margins_for(page_num: int) -> tuple[float, float, float, float]:
    if is_recto(page_num):
        return GUTTER, OUTSIDE, TOP, BOTTOM
    return OUTSIDE, GUTTER, TOP, BOTTOM


def text_box(page_num: int) -> tuple[float, float, float, float]:
    left, right, top, bottom = margins_for(page_num)
    return left, bottom, PAGE_W - left - right, PAGE_H - top - bottom


def draw_folio(c: Canvas, page_num: int, title: str) -> None:
    c.setFont(FONT_SANS, 8)
    c.setFillColor(MUTED)
    y = PAGE_H - TOP / 2
    if is_recto(page_num):
        c.drawRightString(PAGE_W - OUTSIDE, y, f"{title.upper()}   ·   {page_num}")
    else:
        c.drawString(OUTSIDE, y, f"{page_num}   ·   {title.upper()}")
    c.setFillColor(INK)


def draw_hairline(c: Canvas, x1: float, y: float, x2: float, color=HAIR, width: float = 0.5) -> None:
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


# ---------- Spread 1 — Instructions ----------

def draw_spread1_verso(c: Canvas, page_num: int, running_head: str) -> None:
    """Illustrated title page for the practice."""
    x, y, w, h = text_box(page_num)
    draw_folio(c, page_num, running_head)

    # centered layout
    cx = x + w / 2

    # kicker
    c.setFillColor(SAGE)
    c.setFont(FONT_SANS_BOLD, 9.5)
    c.drawCentredString(cx, y + h - 30, "PRACTICE  ·  ONE")
    draw_hairline(c, cx - 12, y + h - 42, cx + 12, HAIR, 0.6)

    # display title
    c.setFillColor(INK)
    c.setFont(FONT_SERIF_BOLD, 46)
    c.drawCentredString(cx, y + h - 100, "5 · 4 · 3 · 2 · 1")

    # subtitle
    c.setFillColor(SAGE)
    c.setFont(FONT_SANS_BOLD, 10)
    c.drawCentredString(cx, y + h - 130, "A SIMPLE SENSORY RESET")

    # intro paragraph — centered narrow measure
    intro = ("When your thoughts are racing faster than you can catch them, your "
             "senses can pull you back into your body. Take your time. There is no rush.")
    p_w = w * 0.78
    p_x = x + (w - p_w) / 2
    c.setFillColor(INK)
    lines = wrap(intro, FONT_SERIF, 11.5, p_w)
    yy = y + h - 170
    for line in lines:
        c.setFont(FONT_SERIF, 11.5)
        line_w = pdfmetrics.stringWidth(line, FONT_SERIF, 11.5)
        c.drawString(p_x + (p_w - line_w) / 2, yy, line)
        yy -= 16

    # botanical illustration — sprig in bottom-left
    draw_leaf_sprig(c, x + 40, y + 100, size=60, color=LEAF)

    # wave illustration — bottom edge
    draw_wave(c, x, y, w, 70, color=SAGE_SOFT)
    draw_wave(c, x, y, w, 45, color=BLUE_SOFT)

    # tiny mark to show where operator art would replace the wave
    c.setFillColor(MUTED)
    c.setFont(FONT_SANS, 6.5)
    c.drawString(x, y - 8, "wave/leaf placeholders — replace with assets/before_the_test/spread1-verso-illustration.png")


def draw_spread1_recto(c: Canvas, page_num: int, running_head: str) -> None:
    """Numbered steps + circular practice diagram + sidebar pull-quote."""
    x, y, w, h = text_box(page_num)
    draw_folio(c, page_num, running_head)

    # sidebar column: reserve right ~1.4 inch
    sidebar_w = 1.35 * INCH
    main_w = w - sidebar_w - 12
    main_x = x

    # top kicker
    c.setFillColor(MUTED)
    c.setFont(FONT_SANS_BOLD, 9)
    c.drawString(main_x, y + h - 24, "A PRACTICE YOU CAN RETURN TO, ANYTIME.")
    draw_hairline(c, main_x, y + h - 34, main_x + main_w, HAIR, 0.6)

    # numbered steps
    steps = [
        ("NOTICE", "Pause and check in. What are you feeling right now? Name it without judgment.", SAGE),
        ("SEE", "Name five things you can see. Distant or close, real or remembered.", SAGE),
        ("TOUCH", "Name four things you can touch. Actually touch them if you can.", CORAL),
        ("HEAR", "Name three things you can hear. Soft sounds count too.", BLUE),
        ("REST", "Name two smells, then one taste. Let your body settle in.", CORAL),
    ]
    yy = y + h - 60
    for i, (label, body, color) in enumerate(steps, start=1):
        # numeral
        c.setFillColor(color)
        c.setFont(FONT_SERIF_BOLD, 24)
        c.drawString(main_x, yy - 4, str(i))
        # label
        c.setFillColor(INK)
        c.setFont(FONT_SANS_BOLD, 10)
        c.drawString(main_x + 28, yy, label)
        # body
        c.setFillColor(INK_SOFT)
        body_x = main_x + 28
        body_w = main_w - 28
        body_lines = wrap(body, FONT_SANS, 9.5, body_w)
        by = yy - 14
        for line in body_lines:
            c.setFont(FONT_SANS, 9.5)
            c.drawString(body_x, by, line)
            by -= 12
        yy = by - 10

    # circular practice diagram, centered in remaining main-column space
    diagram_cy = y + 100
    diagram_cx = main_x + main_w / 2
    draw_practice_diagram(c, diagram_cx, diagram_cy, radius=40)

    # sidebar
    sx = main_x + main_w + 12
    sy = y + 24
    sh = h - 48
    # tinted card
    c.setFillColor(CREAM_TILE)
    c.rect(sx, sy, sidebar_w, sh, fill=1, stroke=0)
    c.setFillColor(INK)

    # sidebar leaf mark
    draw_leaf_sprig(c, sx + sidebar_w / 2, sy + sh - 40, size=30, color=LEAF)

    # sidebar header
    c.setFillColor(SAGE)
    c.setFont(FONT_SANS_BOLD, 8.5)
    c.drawCentredString(sx + sidebar_w / 2, sy + sh - 78, "MAKE IT YOURS")
    draw_hairline(c, sx + sidebar_w / 2 - 14, sy + sh - 88, sx + sidebar_w / 2 + 14, HAIR, 0.6)

    # sidebar body
    body = ("Use this practice before a test, after a hard conversation, or "
            "anytime you feel yourself spiraling.")
    body_lines = wrap(body, FONT_SANS, 8.5, sidebar_w - 20)
    by = sy + sh - 108
    c.setFillColor(INK_SOFT)
    for line in body_lines:
        c.setFont(FONT_SANS, 8.5)
        c.drawString(sx + 10, by, line)
        by -= 11

    # divider
    draw_hairline(c, sx + 20, by - 4, sx + sidebar_w - 20, HAIR, 0.5)

    # pull-quote
    quote_top = by - 20
    quote = "The breath is your anchor. Come back to it, and come back to yourself."
    q_lines = wrap(quote, FONT_SERIF_ITALIC, 10.5, sidebar_w - 20)
    c.setFillColor(INK)
    qy = quote_top
    for line in q_lines:
        c.setFont(FONT_SERIF_ITALIC, 10.5)
        c.drawString(sx + 10, qy, line)
        qy -= 13

    # attribution
    c.setFillColor(CORAL)
    c.setFont(FONT_SANS_BOLD, 8)
    c.drawString(sx + 10, qy - 6, "— UNKNOWN")

    # small note
    c.setFillColor(MUTED)
    c.setFont(FONT_SANS, 6.5)
    c.drawString(x, y - 8, "diagram + sidebar are code-drawn — replace with assets/before_the_test/spread1-recto-diagram.png when ready")


# ---------- Spread 2 — Writing ----------

def draw_spread2_verso(c: Canvas, page_num: int, running_head: str) -> None:
    """Reminder condensed at top, ruled writing area filling below."""
    x, y, w, h = text_box(page_num)
    draw_folio(c, page_num, running_head)

    # small leaf accent to the right of the kicker (so it doesn't crowd the numerals)
    draw_leaf_sprig(c, x + w - 20, y + h - 20, size=16, color=LEAF)

    # kicker
    c.setFillColor(SAGE)
    c.setFont(FONT_SANS_BOLD, 9)
    c.drawString(x, y + h - 20, "5 · 4 · 3 · 2 · 1   ·   YOUR PRACTICE")

    # condensed reminder
    c.setFillColor(INK)
    reminder_top = y + h - 44
    lines = [
        ("5", "Name five things you can see.", SAGE),
        ("4", "Name four things you can touch.", CORAL),
        ("3", "Name three things you can hear.", BLUE),
        ("2", "Name two things you can smell.", SAGE),
        ("1", "Name one thing you can taste.", CORAL),
    ]
    yy = reminder_top
    for num, text, color in lines:
        c.setFillColor(color)
        c.setFont(FONT_SERIF_BOLD, 13)
        c.drawString(x, yy, num)
        c.setFillColor(INK_SOFT)
        c.setFont(FONT_SANS, 9.5)
        c.drawString(x + 14, yy + 1, text)
        yy -= 15
    reminder_bottom = yy - 4

    # divider
    draw_hairline(c, x, reminder_bottom, x + w, HAIR, 0.5)

    # label for writing area
    c.setFillColor(MUTED)
    c.setFont(FONT_SANS_BOLD, 8.5)
    c.drawString(x, reminder_bottom - 14, "WRITE WHAT CAME UP.")

    # ruled lines
    yy = reminder_bottom - 32
    while yy > y + 4:
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.4)
        c.line(x, yy, x + w, yy)
        yy -= 22


def draw_spread2_recto(c: Canvas, page_num: int, running_head: str) -> None:
    """Continuation of writing area with a closing prompt."""
    x, y, w, h = text_box(page_num)
    draw_folio(c, page_num, running_head)

    # kicker
    c.setFillColor(SAGE)
    c.setFont(FONT_SANS_BOLD, 9)
    c.drawString(x, y + h - 20, "5 · 4 · 3 · 2 · 1   ·   AFTER YOUR PRACTICE")

    # closing prompt in italic
    c.setFillColor(INK)
    c.setFont(FONT_SERIF_ITALIC, 12)
    prompt = "How did your body feel afterward? What softened, if anything?"
    lines = wrap(prompt, FONT_SERIF_ITALIC, 12, w)
    yy = y + h - 44
    for line in lines:
        c.setFont(FONT_SERIF_ITALIC, 12)
        c.drawString(x, yy, line)
        yy -= 16
    yy -= 6

    # ruled lines fill the rest
    while yy > y + 60:
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.4)
        c.line(x, yy, x + w, yy)
        yy -= 22

    # bottom callout: gentle reminder
    callout_top = y + 60
    c.setFillColor(SAGE_SOFT)
    c.rect(x, y + 8, w, 44, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_SERIF_ITALIC, 10.5)
    c.drawCentredString(x + w / 2, y + 34,
                        "You can return to this practice as many times as you need.")
    c.setFillColor(MUTED)
    c.setFont(FONT_SANS_BOLD, 7.5)
    c.drawCentredString(x + w / 2, y + 20, "REPEAT AS OFTEN AS IT HELPS.")


# ---------- build ----------

def build_preview(out_path: Path, title: str = "BEFORE THE TEST") -> Path:
    _register_fonts()
    c = Canvas(str(out_path), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("Preview — 4-page exercise unit for 5-4-3-2-1")
    c.setAuthor("North Star Journals")

    # Preview convention: pages 1-4 render as if pp 2-5 in the real book (so page 1
    # here is a VERSO with the wide gutter on the right — matching the "spread
    # opens on verso" reading order the reference books use).
    # We pass odd page numbers to trigger the verso layout on page 1 by feeding
    # even numbers to the folio/margin helpers.
    pages = [
        (2, draw_spread1_verso),
        (3, draw_spread1_recto),
        (4, draw_spread2_verso),
        (5, draw_spread2_recto),
    ]
    for page_num, draw_fn in pages:
        draw_fn(c, page_num, title)
        c.showPage()

    c.save()
    return out_path


if __name__ == "__main__":
    out = Path(__file__).parent / "preview" / "before_the_test_4page_unit_v1.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    path = build_preview(out)
    print(f"  wrote {path}")
