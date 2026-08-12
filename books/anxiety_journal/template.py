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


def draw_prompt_page(c: Canvas, page_num: int, prompt: str, running_head: str) -> None:
    """Journal prompt at top, light rules for handwriting below."""
    x, y, w, h = text_box(page_num)
    draw_running_head(c, page_num, running_head)

    # prompt block
    c.setFillColor(INK)
    c.setFont(FONT_SERIF_ITALIC, 12.5)
    prompt_lines = _wrap(prompt, FONT_SERIF_ITALIC, 12.5, w)
    top_y = y + h - 6
    line_h = 16
    for i, line in enumerate(prompt_lines):
        c.drawString(x, top_y - i * line_h, line)
    prompt_bottom = top_y - len(prompt_lines) * line_h - 8

    # thin divider
    c.setStrokeColor(RULE)
    c.setLineWidth(0.4)
    c.line(x, prompt_bottom, x + w, prompt_bottom)

    # ruled lines for handwriting
    rule_gap = 22
    first_rule = prompt_bottom - rule_gap
    yy = first_rule
    while yy > y + 4:
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.line(x, yy, x + w, yy)
        yy -= rule_gap

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
    """Full-page section opener, centered, no page number."""
    cx = PAGE_W / 2
    c.setFillColor(MUTED)
    c.setFont(FONT_SANS_BOLD, 9)
    c.drawCentredString(cx, PAGE_H * 0.62, kicker.upper())

    # accent rule
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.8)
    c.line(cx - 20, PAGE_H * 0.60, cx + 20, PAGE_H * 0.60)

    c.setFillColor(INK)
    c.setFont(FONT_SERIF_BOLD, 26)
    # heading may be one or two lines
    heading_lines = _wrap(heading, FONT_SERIF_BOLD, 26, PAGE_W - 2 * INCH)
    y = PAGE_H * 0.54
    for i, line in enumerate(heading_lines):
        c.drawCentredString(cx, y - i * 30, line)

    if subhead:
        c.setFont(FONT_SERIF_ITALIC, 12)
        c.setFillColor(MUTED)
        sub_lines = _wrap(subhead, FONT_SERIF_ITALIC, 12, PAGE_W - 2.2 * INCH)
        sy = y - len(heading_lines) * 30 - 18
        for i, line in enumerate(sub_lines):
            c.drawCentredString(cx, sy - i * 16, line)


def draw_exercise_page(
    c: Canvas,
    page_num: int,
    title: str,
    intro: str,
    running_head: str,
    with_lines: bool = True,
) -> None:
    """Named exercise page: bold title, italic intro, optional practice lines."""
    x, y, w, h = text_box(page_num)
    draw_running_head(c, page_num, running_head)

    c.setFillColor(INK)
    c.setFont(FONT_SANS_BOLD, 13)
    c.drawString(x, y + h - 4, title.upper())

    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.8)
    c.line(x, y + h - 12, x + 28, y + h - 12)

    c.setFont(FONT_SERIF, 11)
    intro_lines = _wrap(intro, FONT_SERIF, 11, w)
    line_h = 15
    intro_top = y + h - 30
    for i, line in enumerate(intro_lines):
        c.drawString(x, intro_top - i * line_h, line)
    intro_bottom = intro_top - len(intro_lines) * line_h - 10

    if with_lines:
        rule_gap = 22
        yy = intro_bottom - 4
        while yy > y + 4:
            c.setStrokeColor(RULE)
            c.setLineWidth(0.4)
            c.line(x, yy, x + w, yy)
            yy -= rule_gap

    draw_page_number(c, page_num)


def draw_tracker_page(
    c: Canvas,
    page_num: int,
    title: str,
    running_head: str,
    days: list[str],
    columns: list[str],
) -> None:
    """Weekly grid: rows = days, columns = things to note."""
    x, y, w, h = text_box(page_num)
    draw_running_head(c, page_num, running_head)

    c.setFillColor(INK)
    c.setFont(FONT_SANS_BOLD, 12)
    c.drawString(x, y + h - 4, title.upper())

    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.8)
    c.line(x, y + h - 12, x + 28, y + h - 12)

    grid_top = y + h - 34
    row_h = 32
    n_rows = len(days)
    grid_h = row_h * (n_rows + 1)  # +1 for header
    grid_bottom = grid_top - grid_h

    # column layout: first column is fixed narrow, rest split remaining width
    day_col_w = 0.9 * INCH
    remaining = w - day_col_w
    n_cols = len(columns)
    col_w = remaining / n_cols

    # header row
    c.setFont(FONT_SANS_BOLD, 9)
    c.setFillColor(MUTED)
    c.drawString(x + 4, grid_top - 12, "DAY")
    for i, col_label in enumerate(columns):
        cx = x + day_col_w + i * col_w + 4
        c.drawString(cx, grid_top - 12, col_label.upper())

    # grid lines
    c.setStrokeColor(RULE)
    c.setLineWidth(0.4)
    for r in range(n_rows + 2):
        yy = grid_top - r * row_h
        c.line(x, yy, x + w, yy)
    # verticals
    xs = [x, x + day_col_w]
    for i in range(1, n_cols + 1):
        xs.append(x + day_col_w + i * col_w)
    for xx in xs:
        c.line(xx, grid_top, xx, grid_bottom)

    # day labels
    c.setFont(FONT_SERIF, 10)
    c.setFillColor(INK)
    for i, day in enumerate(days):
        yy = grid_top - (i + 1) * row_h - 20
        c.drawString(x + 6, yy, day)

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
    c.setFont(FONT_SERIF_BOLD, 22)
    c.setFillColor(INK)
    lines = _wrap(title, FONT_SERIF_BOLD, 22, PAGE_W - 1.5 * INCH)
    y = PAGE_H * 0.58
    for i, line in enumerate(lines):
        c.drawCentredString(cx, y - i * 26, line)


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
    c.setFont(FONT_SERIF_ITALIC, 13)
    c.setFillColor(INK)
    lines = _wrap(dedication, FONT_SERIF_ITALIC, 13, PAGE_W - 2 * INCH)
    y = PAGE_H * 0.55
    for i, line in enumerate(lines):
        c.drawCentredString(cx, y - i * 18, line)


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

    for title, intro in _grounding_exercises():
        draw_exercise_page(c, page, title, intro, running_head, with_lines=False)
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
    for prompt in prompts:
        draw_prompt_page(c, page, prompt, running_head)
        page = show(page)
    # page is now 55

    # ---- Section 3: Trackers (16 pp, pages 55-70) ----
    draw_section_title(c, page, "Section Three", "Trackers", f"Notice the patterns in your {cfg.tracker_focus or 'week'}.")
    page = show(page)                            # 56
    draw_blank_page(c, page); page = show(page)  # 57

    trackers = _tracker_specs(cfg)
    trackers = (trackers * ((14 // max(len(trackers), 1)) + 1))[:14]
    for spec in trackers:
        draw_tracker_page(c, page, spec["title"], running_head, DAYS, spec["columns"])
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
        "This is your journal. Use it in whatever order helps. Skip pages. Come back to "
        "pages. Nothing here is a test.",
        "",
        "There are five sections. Grounding tools you can use in the moment. Prompts to "
        "help you get thoughts out of your head and onto paper. Trackers to spot patterns. "
        "A toolkit of small practices. And eight weeks of short reflections.",
        "",
        "Try one prompt when your mind is loud. Try one tracker for a week. If a page "
        "feels wrong for you today, turn to another one. Progress is not linear, and "
        "neither is this book.",
        "",
        "There are no wrong answers here. Write in pencil, pen, whatever. Scribble. "
        "Draw. Leave pages blank. This journal will not grade you.",
        "",
        "If your anxiety is getting in the way of your daily life, please also talk to a "
        "trusted adult or a mental-health professional. Resources are on the last page.",
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


def _grounding_exercises() -> list[tuple[str, str]]:
    return [
        ("5-4-3-2-1",
         "Look around. Name five things you can see. Four things you can touch. Three "
         "things you can hear. Two things you can smell. One thing you can taste. Go slow. "
         "Your senses pull you back into your body."),
        ("Box breathing",
         "Breathe in for four counts. Hold for four. Breathe out for four. Hold for four. "
         "Repeat four times. Draw a square in the air with your finger as you breathe, "
         "one side per count."),
        ("Body scan",
         "Start at the top of your head. Slowly move your attention down: forehead, jaw, "
         "shoulders, chest, belly, arms, hands, legs, feet. Notice what's tight. Let it "
         "soften if it wants to. If it doesn't, that's fine."),
        ("Cold water reset",
         "Splash cold water on your face, or hold an ice cube for a few seconds, or run "
         "your wrists under cold water for thirty seconds. The temperature shift interrupts "
         "the anxiety loop and signals your nervous system to slow down."),
        ("Name it to tame it",
         "Say out loud, or write down, exactly what you're feeling. “I feel anxious "
         "because...” Being specific about the emotion — not just ‘bad’ "
         "— shrinks it a little. Try to name three feelings if you can."),
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
        {"title": "Anxiety level this week", "columns": ["Level 1-10", "What triggered it", "What helped"]},
        {"title": "Sleep tracker", "columns": ["Hours", "How I slept", "How I felt"]},
        {"title": "Mood check-in", "columns": ["Morning", "Afternoon", "Night"]},
        {"title": f"{focus.title()} log", "columns": ["Where / when", "Body feeling", "What I did next"]},
        {"title": "Energy this week", "columns": ["Level 1-10", "What drained me", "What refilled me"]},
        {"title": "One small win", "columns": ["Win of the day", "Who saw it", "How it felt"]},
        {"title": "Kindness to self", "columns": ["What I did", "How it felt", "Do again?"]},
    ]
