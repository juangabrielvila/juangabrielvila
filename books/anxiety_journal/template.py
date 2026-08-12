"""Shared interior template for the North Star Journals anxiety-journal line.

6x9 in trim, mirrored 0.75 in gutter, no bleed. 108 pages, KDP-ready.
Fonts embedded (Liberation Serif/Sans — SIL/GPL-with-font-exception, safe for
commercial embedding). All layout drawn on a raw canvas for tight control.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

INCH = 72.0
PAGE_W = 6 * INCH
PAGE_H = 9 * INCH

GUTTER = 0.75 * INCH
OUTSIDE = 0.5 * INCH
TOP = 0.6 * INCH
BOTTOM = 0.6 * INCH

INK = HexColor("#1a1a1a")
MUTED = HexColor("#6b6b6b")
RULE = HexColor("#d6d6d6")
ACCENT = HexColor("#2f5d63")

FONT_SERIF = "BodySerif"
FONT_SERIF_BOLD = "BodySerifBold"
FONT_SERIF_ITALIC = "BodySerifItalic"
FONT_SANS = "Sans"
FONT_SANS_BOLD = "SansBold"

_FONT_PATHS = {
    FONT_SERIF: "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    FONT_SERIF_BOLD: "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    FONT_SERIF_ITALIC: "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    FONT_SANS: "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    FONT_SANS_BOLD: "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
}

_fonts_registered = False


def _register_fonts() -> None:
    global _fonts_registered
    if _fonts_registered:
        return
    for name, path in _FONT_PATHS.items():
        pdfmetrics.registerFont(TTFont(name, path))
    _fonts_registered = True


@dataclass
class BookConfig:
    """Per-title content overrides. Structural template is shared."""

    slug: str                 # filename slug, e.g. "overthinker"
    title: str                # main title on cover/title page
    subtitle: str             # subtitle
    pen_name: str = "North Star Journals"
    dedication: str = "For anyone whose brain won't turn down the volume."
    how_to_use: list[str] = field(default_factory=list)   # 2 pages worth of paragraphs
    section1_intro: str = ""  # intro line for grounding tools section
    prompts: list[str] = field(default_factory=list)       # ~30 journal prompts
    exercises: list[tuple[str, str]] = field(default_factory=list)  # ~10 (title, intro) pairs
    affirmations_seed: list[str] = field(default_factory=list)      # 6-8 example affirmations
    tracker_focus: str = ""   # short phrase describing what to track (e.g. "worry episodes")


# ---------- low-level draw helpers ----------

def is_recto(page_num: int) -> bool:
    """Odd page numbers are right-hand (recto)."""
    return page_num % 2 == 1


def margins_for(page_num: int) -> tuple[float, float, float, float]:
    """Return (left, right, top, bottom) margins for the given page number."""
    if is_recto(page_num):
        return GUTTER, OUTSIDE, TOP, BOTTOM
    return OUTSIDE, GUTTER, TOP, BOTTOM


def text_box(page_num: int) -> tuple[float, float, float, float]:
    """(x, y, width, height) of the printable text area."""
    left, right, top, bottom = margins_for(page_num)
    return left, bottom, PAGE_W - left - right, PAGE_H - top - bottom


def draw_page_number(c: Canvas, page_num: int) -> None:
    """Bottom-outside page number, muted."""
    c.setFont(FONT_SANS, 8.5)
    c.setFillColor(MUTED)
    if is_recto(page_num):
        x = PAGE_W - OUTSIDE
        c.drawRightString(x, BOTTOM / 2, str(page_num))
    else:
        x = OUTSIDE
        c.drawString(x, BOTTOM / 2, str(page_num))
    c.setFillColor(INK)


def draw_running_head(c: Canvas, page_num: int, text: str) -> None:
    """Small italic running head, top-outside."""
    c.setFont(FONT_SERIF_ITALIC, 8.5)
    c.setFillColor(MUTED)
    y = PAGE_H - TOP / 2
    if is_recto(page_num):
        c.drawRightString(PAGE_W - OUTSIDE, y, text)
    else:
        c.drawString(OUTSIDE, y, text)
    c.setFillColor(INK)


def _fill_rules(c: Canvas, x: float, top_y: float, bottom_limit: float, w: float, rule_gap: float = 22.0) -> None:
    """Draw ruled lines starting at top_y, moving down until bottom_limit."""
    c.setStrokeColor(RULE)
    c.setLineWidth(0.4)
    yy = top_y
    while yy >= bottom_limit:
        c.line(x, yy, x + w, yy)
        yy -= rule_gap


def draw_prompt_page(c: Canvas, page_num: int, prompt: str, running_head: str, prompt_number: int | None = None) -> None:
    """Journal prompt near top with breathing room, ruled lines fill to bottom."""
    x, y, w, h = text_box(page_num)
    draw_running_head(c, page_num, running_head)

    # prompt-number tag
    top_y = y + h - 18
    if prompt_number is not None:
        c.setFillColor(MUTED)
        c.setFont(FONT_SANS_BOLD, 9)
        c.drawString(x, top_y, f"NO. {prompt_number:02d}")
        top_y -= 14

    # prompt block
    c.setFillColor(INK)
    c.setFont(FONT_SERIF_ITALIC, 13.5)
    prompt_lines = _wrap(prompt, FONT_SERIF_ITALIC, 13.5, w)
    line_h = 18
    for i, line in enumerate(prompt_lines):
        c.drawString(x, top_y - i * line_h, line)
    prompt_bottom = top_y - len(prompt_lines) * line_h - 12

    # thin divider
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.6)
    c.line(x, prompt_bottom, x + 32, prompt_bottom)

    # ruled lines fill remaining space
    first_rule = prompt_bottom - 24
    _fill_rules(c, x, first_rule, y + 6, w, rule_gap=22)

    draw_page_number(c, page_num)


def draw_blank_page(c: Canvas, page_num: int) -> None:
    """Intentionally blank — no page number, no head. Used between sections."""
    # Nothing drawn; caller still calls c.showPage().
    _ = (c, page_num)


def draw_section_title(
    c: Canvas,
    page_num: int,
    kicker: str,
    heading: str,
    subhead: str = "",
) -> None:
    """Full-page section opener. Oversized numeral watermark for visual weight,
    kicker + heading + subhead grouped at the optical center, decorative bottom
    rule for balance.
    """
    cx = PAGE_W / 2

    # oversized muted numeral watermark, tucked in the lower third for balance
    numeral = _kicker_to_numeral(kicker)
    if numeral:
        c.setFillColor(HexColor("#e8ecee"))
        # scale by numeral width so 'I' isn't tiny and 'VIII' isn't overflowing
        size = 160 if len(numeral) >= 3 else 200 if len(numeral) == 2 else 180
        c.setFont(FONT_SERIF_BOLD, size)
        c.drawCentredString(cx, PAGE_H * 0.20, numeral)

    # kicker
    c.setFillColor(MUTED)
    c.setFont(FONT_SANS_BOLD, 10)
    c.drawCentredString(cx, PAGE_H * 0.66, kicker.upper())

    # accent rule
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.0)
    c.line(cx - 24, PAGE_H * 0.64, cx + 24, PAGE_H * 0.64)

    # heading
    c.setFillColor(INK)
    c.setFont(FONT_SERIF_BOLD, 34)
    heading_lines = _wrap(heading, FONT_SERIF_BOLD, 34, PAGE_W - 1.6 * INCH)
    y = PAGE_H * 0.58
    for i, line in enumerate(heading_lines):
        c.drawCentredString(cx, y - i * 38, line)

    # subhead
    if subhead:
        c.setFont(FONT_SERIF_ITALIC, 13)
        c.setFillColor(MUTED)
        sub_lines = _wrap(subhead, FONT_SERIF_ITALIC, 13, PAGE_W - 2 * INCH)
        sy = y - len(heading_lines) * 38 - 20
        for i, line in enumerate(sub_lines):
            c.drawCentredString(cx, sy - i * 17, line)

    # no explicit bottom rule — numeral watermark carries the lower half


_ROMAN = {"one": "I", "two": "II", "three": "III", "four": "IV", "five": "V",
          "six": "VI", "seven": "VII", "eight": "VIII"}


def _kicker_to_numeral(kicker: str) -> str:
    """Extract 'Two' from 'Section Two' -> 'II'. Empty string if not found."""
    parts = kicker.lower().replace("·", " ").split()
    for p in parts:
        if p in _ROMAN:
            return _ROMAN[p]
    return ""


def draw_exercise_page(
    c: Canvas,
    page_num: int,
    title: str,
    intro: str,
    running_head: str,
    steps: list[str] | None = None,
    try_it_prompt: str = "Try it now.",
    with_lines: bool = True,
) -> None:
    """Named exercise page. Header + intro paragraph + optional numbered steps +
    a "try it now" divider, then ruled lines that fill to the bottom margin.

    When `steps` is passed, they render as numbered lines under the intro. When
    with_lines is True, ruled lines fill the remainder of the page for practice.
    """
    x, y, w, h = text_box(page_num)
    draw_running_head(c, page_num, running_head)

    # kicker + title
    c.setFillColor(MUTED)
    c.setFont(FONT_SANS_BOLD, 8.5)
    c.drawString(x, y + h - 8, "PRACTICE")

    c.setFillColor(INK)
    c.setFont(FONT_SERIF_BOLD, 22)
    title_lines = _wrap(title, FONT_SERIF_BOLD, 22, w)
    title_top = y + h - 32
    for i, line in enumerate(title_lines):
        c.drawString(x, title_top - i * 24, line)
    y_cursor = title_top - len(title_lines) * 24 - 6

    # accent rule under title
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.9)
    c.line(x, y_cursor, x + 36, y_cursor)
    y_cursor -= 18

    # intro paragraph
    c.setFillColor(INK)
    c.setFont(FONT_SERIF, 11.5)
    intro_lines = _wrap(intro, FONT_SERIF, 11.5, w)
    line_h = 16
    for line in intro_lines:
        c.drawString(x, y_cursor, line)
        y_cursor -= line_h
    y_cursor -= 6

    # optional numbered steps
    if steps:
        c.setFont(FONT_SERIF, 11)
        step_line_h = 15
        for i, step in enumerate(steps, start=1):
            label = f"{i}."
            c.setFont(FONT_SANS_BOLD, 10)
            c.setFillColor(ACCENT)
            c.drawString(x, y_cursor, label)
            c.setFont(FONT_SERIF, 11)
            c.setFillColor(INK)
            wrapped = _wrap(step, FONT_SERIF, 11, w - 22)
            for j, wline in enumerate(wrapped):
                c.drawString(x + 22, y_cursor - j * step_line_h, wline)
            y_cursor -= len(wrapped) * step_line_h + 6
        y_cursor -= 4

    if with_lines:
        # "Try it now." divider
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.line(x, y_cursor, x + w, y_cursor)
        c.setFont(FONT_SANS_BOLD, 8.5)
        c.setFillColor(MUTED)
        c.drawString(x, y_cursor - 12, try_it_prompt.upper())
        y_cursor -= 26

        _fill_rules(c, x, y_cursor, y + 6, w, rule_gap=22)

    draw_page_number(c, page_num)


def draw_tracker_page(
    c: Canvas,
    page_num: int,
    title: str,
    running_head: str,
    days: list[str],
    columns: list[str],
    subtitle: str = "",
) -> None:
    """Weekly grid: rows = days, columns = things to note.

    Row height auto-sizes to fill the printable page height so every cell has
    real room to write in. Column labels wrap onto up to two lines so they
    never collide.
    """
    x, y, w, h = text_box(page_num)
    draw_running_head(c, page_num, running_head)

    # kicker + title
    c.setFillColor(MUTED)
    c.setFont(FONT_SANS_BOLD, 8.5)
    c.drawString(x, y + h - 8, "TRACKER")

    c.setFillColor(INK)
    c.setFont(FONT_SERIF_BOLD, 20)
    c.drawString(x, y + h - 32, title)

    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.9)
    c.line(x, y + h - 38, x + 36, y + h - 38)

    y_cursor = y + h - 60
    if subtitle:
        c.setFont(FONT_SERIF_ITALIC, 10.5)
        c.setFillColor(MUTED)
        sub_lines = _wrap(subtitle, FONT_SERIF_ITALIC, 10.5, w)
        for line in sub_lines:
            c.drawString(x, y_cursor, line)
            y_cursor -= 13
        y_cursor -= 6

    grid_top = y_cursor
    grid_bottom = y + 4
    n_rows = len(days)
    header_h = 26  # room for two-line column labels
    row_h = (grid_top - grid_bottom - header_h) / n_rows
    n_cols = len(columns)

    # column widths — day col fixed narrow, rest share the remainder
    day_col_w = 0.7 * INCH
    remaining = w - day_col_w
    col_w = remaining / n_cols

    # header cells: wrap labels to fit up to 2 lines
    c.setFont(FONT_SANS_BOLD, 8.5)
    c.setFillColor(MUTED)
    header_bottom = grid_top - header_h
    c.drawString(x + 4, header_bottom + 8, "DAY")
    for i, col_label in enumerate(columns):
        cx = x + day_col_w + i * col_w + 4
        max_label_w = col_w - 8
        wrapped = _wrap(col_label.upper(), FONT_SANS_BOLD, 8.5, max_label_w)[:2]
        if len(wrapped) == 1:
            c.drawString(cx, header_bottom + 8, wrapped[0])
        else:
            c.drawString(cx, header_bottom + 14, wrapped[0])
            c.drawString(cx, header_bottom + 2, wrapped[1])

    # horizontal grid lines
    c.setStrokeColor(RULE)
    c.setLineWidth(0.4)
    c.line(x, grid_top, x + w, grid_top)
    c.line(x, header_bottom, x + w, header_bottom)
    for r in range(1, n_rows + 1):
        yy = header_bottom - r * row_h
        c.line(x, yy, x + w, yy)
    # verticals
    xs = [x, x + day_col_w]
    for i in range(1, n_cols + 1):
        xs.append(x + day_col_w + i * col_w)
    for xx in xs:
        c.line(xx, grid_top, xx, header_bottom - n_rows * row_h)

    # day labels — vertically centered in each row
    c.setFont(FONT_SERIF, 10.5)
    c.setFillColor(INK)
    for i, day in enumerate(days):
        cell_top = header_bottom - i * row_h
        cell_center_y = cell_top - row_h / 2 - 3
        c.drawString(x + 8, cell_center_y, day)

    draw_page_number(c, page_num)


def draw_title_page(c: Canvas, page_num: int, title: str, subtitle: str, pen_name: str) -> None:
    """Full title page — centered, no page number."""
    cx = PAGE_W / 2

    c.setFillColor(INK)
    c.setFont(FONT_SERIF_BOLD, 30)
    title_lines = _wrap(title, FONT_SERIF_BOLD, 30, PAGE_W - 1.5 * INCH)
    y = PAGE_H * 0.62
    for i, line in enumerate(title_lines):
        c.drawCentredString(cx, y - i * 34, line)

    y2 = y - len(title_lines) * 34 - 20

    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.8)
    c.line(cx - 30, y2, cx + 30, y2)

    c.setFont(FONT_SERIF_ITALIC, 13.5)
    c.setFillColor(MUTED)
    sub_lines = _wrap(subtitle, FONT_SERIF_ITALIC, 13.5, PAGE_W - 2 * INCH)
    for i, line in enumerate(sub_lines):
        c.drawCentredString(cx, y2 - 22 - i * 18, line)

    c.setFont(FONT_SANS_BOLD, 10)
    c.setFillColor(INK)
    c.drawCentredString(cx, BOTTOM + 30, pen_name.upper())


def draw_half_title(c: Canvas, page_num: int, title: str) -> None:
    cx = PAGE_W / 2
    c.setFillColor(INK)
    c.setFont(FONT_SERIF_BOLD, 24)
    lines = _wrap(title, FONT_SERIF_BOLD, 24, PAGE_W - 1.5 * INCH)
    total_h = len(lines) * 28
    y = PAGE_H / 2 + total_h / 2  # true vertical center
    for i, line in enumerate(lines):
        c.drawCentredString(cx, y - i * 28, line)
    # small accent below
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.9)
    c.line(cx - 18, y - total_h - 6, cx + 18, y - total_h - 6)


def draw_copyright_page(c: Canvas, page_num: int, cfg: BookConfig, year: int) -> None:
    """Copyright + safety disclaimer + brief resource note."""
    x, y, w, h = text_box(page_num)
    c.setFillColor(INK)
    c.setFont(FONT_SANS, 9)

    lines = [
        f"Copyright © {year} {cfg.pen_name}. All rights reserved.",
        "",
        "No part of this journal may be reproduced, distributed, or transmitted in any",
        "form or by any means, including photocopying, recording, or other electronic or",
        "mechanical methods, without the prior written permission of the publisher,",
        "except for brief quotations embodied in critical reviews and certain other",
        "noncommercial uses permitted by copyright law.",
        "",
        "This journal is intended for self-reflection and general well-being. It is not",
        "a substitute for professional mental-health care. If you are struggling, please",
        "reach out to a trusted adult, counselor, or crisis line. In the U.S., call or",
        "text 988 (Suicide & Crisis Lifeline). Outside the U.S., see findahelpline.com.",
        "",
        f"First edition, {year}.",
        f"Published by {cfg.pen_name}.",
    ]
    line_h = 12
    top = y + h - 20
    for i, line in enumerate(lines):
        c.drawString(x, top - i * line_h, line)


def draw_dedication_page(c: Canvas, page_num: int, dedication: str) -> None:
    cx = PAGE_W / 2
    c.setFont(FONT_SERIF_ITALIC, 14)
    c.setFillColor(INK)
    lines = _wrap(dedication, FONT_SERIF_ITALIC, 14, PAGE_W - 2 * INCH)
    total_h = len(lines) * 20
    y = PAGE_H / 2 + total_h / 2  # true vertical center
    for i, line in enumerate(lines):
        c.drawCentredString(cx, y - i * 20, line)


def draw_body_page(
    c: Canvas,
    page_num: int,
    heading: str,
    body: list[str],
    running_head: str,
) -> None:
    """Prose page — heading + wrapped paragraphs, no ruled lines."""
    x, y, w, h = text_box(page_num)
    draw_running_head(c, page_num, running_head)

    c.setFillColor(INK)
    if heading:
        c.setFont(FONT_SANS_BOLD, 12)
        c.drawString(x, y + h - 4, heading.upper())
        c.setStrokeColor(ACCENT)
        c.setLineWidth(0.8)
        c.line(x, y + h - 12, x + 28, y + h - 12)
        top = y + h - 34
    else:
        top = y + h - 4

    c.setFont(FONT_SERIF, 11)
    line_h = 15
    yy = top
    for para in body:
        lines = _wrap(para, FONT_SERIF, 11, w)
        for line in lines:
            if yy < y + 4:
                break
            c.drawString(x, yy, line)
            yy -= line_h
        yy -= 8  # paragraph break

    draw_page_number(c, page_num)


def draw_notes_page(c: Canvas, page_num: int, running_head: str) -> None:
    """Ruled page, no prompt."""
    x, y, w, h = text_box(page_num)
    draw_running_head(c, page_num, running_head)

    c.setFillColor(MUTED)
    c.setFont(FONT_SANS_BOLD, 9)
    c.drawString(x, y + h - 4, "NOTES")

    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.8)
    c.line(x, y + h - 12, x + 20, y + h - 12)

    rule_gap = 22
    yy = y + h - 30
    while yy > y + 4:
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.line(x, yy, x + w, yy)
        yy -= rule_gap

    draw_page_number(c, page_num)


def _wrap(text: str, font: str, size: float, max_w: float) -> list[str]:
    """Simple greedy word-wrap using registered font metrics."""
    if not text:
        return [""]
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if pdfmetrics.stringWidth(candidate, font, size) <= max_w:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


# ---------- book assembly ----------

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def build_book(cfg: BookConfig, out_dir: Path, year: int = 2026) -> Path:
    """Build the full 108-page interior PDF for one title.

    Layout (108 pp):
      1  half-title            (recto)
      2  blank                 (verso)
      3  title page            (recto)
      4  copyright             (verso)
      5  dedication            (recto)
      6  blank                 (verso)
      7-8  how to use          (spread)
      9   contents             (recto)
      10  blank                (verso)
      11  section 1 opener     (recto)
      12  blank
      13-22  10 grounding-tool pages (5 exercises x 2 pages each)
      23  section 2 opener     (recto)
      24  blank
      25-54  30 prompt pages
      55  section 3 opener     (recto)
      56  blank
      57-70 14 tracker pages
      71  section 4 opener     (recto)
      72  blank
      73-82 10 exercise pages
      83-84 2 affirmations pages
      85  section 5 opener     (recto)
      86  blank
      87-102 8 weekly-reflection spreads
      103 resources page       (recto)
      104 blank
      105-108 4 notes pages
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{cfg.slug}_interior_6x9_108pp.pdf"

    _register_fonts()
    c = Canvas(
        str(out_path),
        pagesize=(PAGE_W, PAGE_H),
        pageCompression=1,
    )
    c.setTitle(cfg.title)
    c.setAuthor(cfg.pen_name)
    c.setSubject("A guided journal for teens")

    running_head = cfg.title

    def show(page_num: int) -> int:
        c.showPage()
        return page_num + 1

    page = 1

    # ---- Front matter (10) ----
    draw_half_title(c, page, cfg.title)
    page = show(page)                            # 2
    draw_blank_page(c, page); page = show(page)  # 3
    draw_title_page(c, page, cfg.title, cfg.subtitle, cfg.pen_name)
    page = show(page)                            # 4
    draw_copyright_page(c, page, cfg, year); page = show(page)  # 5
    draw_dedication_page(c, page, cfg.dedication); page = show(page)  # 6
    draw_blank_page(c, page); page = show(page)  # 7

    # 7-8: how to use (spread)
    how = cfg.how_to_use or _default_how_to_use()
    half = max(1, len(how) // 2)
    draw_body_page(c, page, "How to use this journal", how[:half], running_head)
    page = show(page)                            # 8
    draw_body_page(c, page, "", how[half:], running_head); page = show(page)  # 9

    # 9-10: contents + blank
    draw_body_page(c, page, "Contents", _contents_list(), running_head)
    page = show(page)                            # 10
    draw_blank_page(c, page); page = show(page)  # 11

    # ---- Section 1: Grounding tools (12 pp, pages 11-22) ----
    draw_section_title(c, page, "Section One", "Start Here", "Five grounding tools you can use anywhere.")
    page = show(page)                            # 12
    draw_blank_page(c, page); page = show(page)  # 13

    for ex_title, ex_intro, ex_steps in _grounding_exercises():
        draw_exercise_page(
            c, page, ex_title, ex_intro, running_head,
            steps=ex_steps, try_it_prompt="What did you notice?", with_lines=True,
        )
        page = show(page)
        draw_notes_page(c, page, running_head)
        page = show(page)
    # 5 exercises * 2 pages = 10, page is now 23

    # ---- Section 2: Journal prompts (32 pp, pages 23-54) ----
    draw_section_title(c, page, "Section Two", "Prompts", cfg.section1_intro or "Write freely. There are no wrong answers.")
    page = show(page)                            # 24
    draw_blank_page(c, page); page = show(page)  # 25

    prompts = list(cfg.prompts) if cfg.prompts else _default_prompts()
    prompts = (prompts * ((30 // max(len(prompts), 1)) + 1))[:30]
    for i, prompt in enumerate(prompts, start=1):
        draw_prompt_page(c, page, prompt, running_head, prompt_number=i)
        page = show(page)
    # page is now 55

    # ---- Section 3: Trackers (16 pp, pages 55-70) ----
    draw_section_title(c, page, "Section Three", "Trackers", f"Notice the patterns in your {cfg.tracker_focus or 'week'}.")
    page = show(page)                            # 56
    draw_blank_page(c, page); page = show(page)  # 57

    trackers = _tracker_specs(cfg)
    trackers = (trackers * ((14 // max(len(trackers), 1)) + 1))[:14]
    for spec in trackers:
        draw_tracker_page(
            c, page, spec["title"], running_head, DAYS, spec["columns"],
            subtitle=spec.get("subtitle", ""),
        )
        page = show(page)
    # page is now 71

    # ---- Section 4: Coping toolkit (14 pp, pages 71-84) ----
    draw_section_title(c, page, "Section Four", "Your Toolkit", "Small practices you can return to on hard days.")
    page = show(page)                            # 72
    draw_blank_page(c, page); page = show(page)  # 73

    exercises = list(cfg.exercises) if cfg.exercises else _default_exercises()
    exercises = (exercises * ((10 // max(len(exercises), 1)) + 1))[:10]
    for title, intro in exercises:
        draw_exercise_page(c, page, title, intro, running_head, with_lines=True)
        page = show(page)
    # page is now 83

    # 83-84 affirmations
    aff = cfg.affirmations_seed or _default_affirmations()
    draw_body_page(
        c, page,
        "Affirmations",
        [
            "Write down phrases that feel true (or that you want to be true). Circle the "
            "ones that help most. Come back to them.",
            "",
            *[f"• {a}" for a in aff],
        ],
        running_head,
    )
    page = show(page)                            # 84
    draw_notes_page(c, page, running_head); page = show(page)  # 85

    # ---- Section 5: Weekly reflections (18 pp, pages 85-102) ----
    draw_section_title(c, page, "Section Five", "Weekly Reflections", "Eight weeks of looking back and forward.")
    page = show(page)                            # 86
    draw_blank_page(c, page); page = show(page)  # 87

    for week in range(1, 9):
        # left page (verso): "This week I noticed..."
        draw_exercise_page(
            c, page,
            f"Week {week}  ·  Looking back",
            "What did you notice about your anxiety this week? What set it off? "
            "What helped, even a little?",
            running_head,
            with_lines=True,
        )
        page = show(page)
        # right page (recto): "Next week I'll try..."
        draw_exercise_page(
            c, page,
            f"Week {week}  ·  Looking forward",
            "Pick one small thing to try next week. One breath, one message, one "
            "conversation. Small counts.",
            running_head,
            with_lines=True,
        )
        page = show(page)
    # page is now 103

    # ---- Back matter (6 pp, pages 103-108) ----
    draw_body_page(
        c, page,
        "When you need more help",
        [
            "This journal is for reflection, not treatment. If your anxiety is getting "
            "in the way of school, sleep, eating, friendships, or feeling safe, please "
            "talk to a trusted adult, a school counselor, or a therapist.",
            "",
            "If you are in crisis:",
            "• U.S. — Call or text 988 (Suicide & Crisis Lifeline).",
            "• U.S. — Text HOME to 741741 (Crisis Text Line).",
            "• U.K. — Call 116 123 (Samaritans).",
            "• Global — findahelpline.com lists lines in your country.",
            "",
            "If you or someone else is in immediate danger, call your local emergency number.",
        ],
        running_head,
    )
    page = show(page)                            # 104
    draw_blank_page(c, page); page = show(page)  # 105

    for _ in range(4):                           # 105-108
        draw_notes_page(c, page, running_head)
        page = show(page)

    # page counter is now 109 (i.e., last drawn was 108)
    assert page == 109, f"expected 108 pages, produced {page - 1}"
    c.save()
    return out_path


# ---------- default shared content (used when a book config leaves a slot empty) ----------

def _default_how_to_use() -> list[str]:
    return [
        "This is your journal. Nothing in it is a test, and there is no wrong "
        "way to use it. Some pages will hit exactly right on a hard day. Others "
        "will feel like nothing. That is normal. Move on.",
        "",
        "There are five sections inside. Grounding tools you can use in the "
        "moment, when your body is in the middle of it. Prompts to help you get "
        "the loud thoughts out of your head and onto paper, where they get a "
        "little smaller. Trackers to help you notice patterns — what triggers "
        "your anxiety, what actually helps, how sleep and mood connect. A "
        "toolkit of small practices for the hard days. And eight weeks of "
        "short reflections at the end.",
        "",
        "You do not have to go in order. If a prompt feels wrong today, turn "
        "to another one. If a tracker doesn't fit your week, skip it. Progress "
        "is not linear, and neither is this book.",
        "",
        "A few small suggestions:",
        "",
        "• If your mind is loud, start with a grounding tool from Section One. "
        "Sometimes your body has to steady before your thoughts will.",
        "",
        "• Try one prompt a day for a week, then look back. You'll see patterns "
        "you couldn't see in the moment.",
        "",
        "• Try one tracker for a full week before deciding whether it helps. "
        "Patterns take time to show up on the page.",
        "",
        "• Write in pencil, pen, marker, whatever. Scribble. Doodle in the "
        "margins. Leave a page half-empty. This journal will not grade you.",
        "",
        "• If you fill a page and want more room, use one of the notes pages "
        "at the back. They're there on purpose.",
        "",
        "One important thing: this journal is for reflection, not treatment. "
        "If your anxiety is getting in the way of school, sleep, eating, "
        "friendships, or feeling safe — please also talk to a trusted adult, "
        "a school counselor, or a mental-health professional. There are "
        "resources at the back of the book. You do not have to do this alone.",
    ]


def _contents_list() -> list[str]:
    return [
        "One  ·  Start Here — five grounding tools",
        "Two  ·  Prompts — thirty pages to write it out",
        "Three  ·  Trackers — spot the patterns",
        "Four  ·  Your Toolkit — small practices for hard days",
        "Five  ·  Weekly Reflections — eight weeks",
        "",
        "When you need more help  ·  page 103",
    ]


def _grounding_exercises() -> list[tuple[str, str, list[str]]]:
    """(title, intro paragraph, numbered steps)."""
    return [
        (
            "5-4-3-2-1",
            "A classic sensory grounding exercise. When your thoughts are racing "
            "faster than you can catch them, your senses can pull you back into "
            "your body. Take your time with each step. There is no rush.",
            [
                "Name five things you can SEE. Say them out loud or in your head.",
                "Name four things you can TOUCH. Actually touch them if you can.",
                "Name three things you can HEAR. Distant sounds count too.",
                "Name two things you can SMELL. Or two smells you like.",
                "Name one thing you can TASTE. Or one taste you'd like right now.",
            ],
        ),
        (
            "Box breathing",
            "A simple breath pattern used by athletes, first responders, and "
            "anyone who needs to steady a racing nervous system. Four counts "
            "in, four hold, four out, four hold. Draw a square in the air with "
            "your finger as you go — one side per count.",
            [
                "Breathe in slowly through your nose for four counts.",
                "Hold your breath gently for four counts.",
                "Breathe out slowly through your mouth for four counts.",
                "Hold empty for four counts. That's one full cycle.",
                "Repeat four times. Notice how your body feels different at the end.",
            ],
        ),
        (
            "Body scan",
            "Anxiety lives in the body — tight jaw, clenched shoulders, shallow "
            "breath. A slow scan helps you locate where you're holding it, so "
            "you can start to let it go. There is no wrong way to do this.",
            [
                "Start at the top of your head. Notice how it feels.",
                "Move down slowly: forehead, jaw, neck, shoulders.",
                "Continue down: chest, belly, arms, hands, hips.",
                "Keep going: legs, knees, ankles, feet.",
                "Where do you feel tight? Let it soften if it wants to. If it doesn't, that's okay too.",
            ],
        ),
        (
            "Cold water reset",
            "A temperature shift is one of the fastest ways to interrupt an "
            "anxiety spiral. Cold on the face triggers the mammalian dive reflex, "
            "which slows your heart rate on purpose. Sounds strange. Works fast.",
            [
                "Go to a sink, or grab an ice cube or a cold drink.",
                "Splash cold water on your face for 30 seconds — especially your forehead and cheeks.",
                "Or: hold an ice cube in your palm until it starts to melt.",
                "Or: run cold water over your wrists for 30 seconds.",
                "Breathe slowly while you do it. Notice the shift.",
            ],
        ),
        (
            "Name it to tame it",
            "Vague, big feelings feel unmanageable. Specific, named feelings "
            "feel smaller. Being precise about your emotion shrinks it a little "
            "and gives you something to actually work with.",
            [
                "Pause. Ask: what am I actually feeling right now?",
                "Skip 'bad.' Try more specific words: anxious, angry, disappointed, embarrassed, lonely.",
                "Say it out loud or write it down: 'I feel ______ because ______.'",
                "See if you can name a second feeling underneath the first one.",
                "Notice — did naming it change the size of it at all?",
            ],
        ),
    ]


def _default_prompts() -> list[str]:
    return [
        "What does your anxiety sound like in your head? Write it out word for word.",
        "When did you first notice anxiety today? What was happening?",
        "What is one thing your anxiety is trying to protect you from?",
        "Write a letter to your anxiety. You do not have to send it.",
        "What is a story you keep telling yourself that might not be fully true?",
        "What would you do this week if you were 10% braver?",
        "Name three things you did today that took courage, even small ones.",
        "What do you need from the people around you right now? What is hard to ask for?",
        "Describe a place — real or imagined — where your nervous system feels safe.",
        "What is one thing you are proud of this week? Be specific.",
        "What are you avoiding? What would happen if you did the smallest version of it?",
        "Write about a time you felt scared and got through it. What helped?",
        "What is a kind thing you can say to yourself right now that isn't a lie?",
        "What does your body feel like when you are anxious? Draw it or describe it.",
        "Who can you talk to when things get heavy? What makes them safe?",
        "What is your anxiety trying to tell you? Is it a message you already know?",
        "What are three things that are true right now that have nothing to do with your worry?",
        "If a friend told you exactly what you're thinking, what would you say back?",
        "What is one thing you can do tomorrow that would be a small kindness to yourself?",
        "What does ‘enough’ look like for you today? Not perfect. Just enough.",
        "Write about a small win from this week that no one else noticed.",
        "What are you tired of pretending is fine?",
        "What is one boundary you want to try setting, with whom, and how?",
        "What did your anxiety make you skip today? What would it have taken to show up?",
        "What is a compliment someone gave you that you brushed off? Write it back to yourself.",
        "What is one thing you can let go of, even just for tonight?",
        "Describe your ideal morning. What is one small piece of it you could add tomorrow?",
        "Where do you feel calmest? Bring yourself there in your mind and describe it.",
        "What is a hard thing you have already lived through? What did you learn from it?",
        "Finish this: “Today I am proud that I...”",
    ]


def _default_exercises() -> list[tuple[str, str]]:
    return [
        ("The worry list", "Write down every worry currently in your head. All of them. "
         "Then circle the ones you can do something about today, and put a line through the "
         "ones you can't. Look at the difference."),
        ("Three good things", "Write down three good things that happened today, however "
         "small. Toast that wasn't burnt counts. A text that made you smile counts."),
        ("Reframe it", "Write down an anxious thought at the top. Underneath, write: What "
         "would I tell a friend who said this? Write that response with the same care."),
        ("The 10-10-10", "Ask: Will this matter in 10 minutes? In 10 months? In 10 years? "
         "Write your honest answer to each. Notice how the size of the worry changes."),
        ("Anxiety weather report", "Give today's anxiety a weather forecast. Cloudy? "
         "Thunderstorm? A little windy? Describe what you'd need to get through weather "
         "like this."),
        ("The 5-minute rule", "Pick one thing you've been avoiding. Set a timer for five "
         "minutes and do only that. Then stop. Write about what came up."),
        ("Permission slip", "Write yourself permission for something you've been withholding. "
         "“I give myself permission to...” Rest. Say no. Not be okay. Ask for help."),
        ("Body first", "Before you try to think your way through it: drink water, eat "
         "something, move your body for five minutes, or step outside. Then check in. "
         "What changed?"),
        ("What I can control", "Draw a small circle inside a big one. Inside the small "
         "circle: what you can control today. Outside it: what you cannot. Keep your "
         "attention in the small circle."),
        ("The smallest next step", "You do not have to see the whole path. What is the "
         "next single step — the smallest possible one — you could take? Do that."),
    ]


def _default_affirmations() -> list[str]:
    return [
        "I am allowed to take up space.",
        "I can feel anxious and still do the thing.",
        "My feelings are information, not instructions.",
        "I do not have to be sure to move forward.",
        "One breath. One step. That counts.",
        "I have made it through 100% of my hardest days.",
        "I am not my worst thought.",
        "Rest is not quitting.",
    ]


def _tracker_specs(cfg: BookConfig) -> list[dict]:
    focus = cfg.tracker_focus or "worry"
    return [
        {
            "title": "Anxiety level this week",
            "subtitle": "Rate your baseline anxiety each day. Note what set it off and what helped.",
            "columns": ["Level 1-10", "What triggered it", "What helped"],
        },
        {
            "title": "Sleep tracker",
            "subtitle": "How many hours, how well, and how you felt the next day. Patterns show up fast.",
            "columns": ["Hours slept", "Quality 1-10", "How I felt"],
        },
        {
            "title": "Mood check-in",
            "subtitle": "Three quick check-ins each day. One word each is enough.",
            "columns": ["Morning", "Afternoon", "Night"],
        },
        {
            "title": f"{focus.title()} log",
            "subtitle": "Notice when it shows up. What was happening? What did you do next?",
            "columns": ["When and where", "Body feeling", "What I did next"],
        },
        {
            "title": "Energy this week",
            "subtitle": "What drained you. What refilled you. Both matter.",
            "columns": ["Level 1-10", "What drained me", "What refilled me"],
        },
        {
            "title": "One small win",
            "subtitle": "Every day, name one small thing. Toast that wasn't burnt counts.",
            "columns": ["Win of the day", "Who noticed", "How it felt"],
        },
        {
            "title": "Kindness to self",
            "subtitle": "One kind thing you did for yourself each day. Rest counts. Naps count.",
            "columns": ["What I did", "How it felt", "Do again?"],
        },
    ]
