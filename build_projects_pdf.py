"""
F.O.C.U.S.© Projects — PDF of every public GitHub project (live page + code links, clickable)
Built from _TEMPLATES/jachbit_pdf_base_template.py v4.0 | Jachbit 2026

Reads projects.json (names, categories, descriptions, live links) and the public GitHub repo list,
same as index.html: a public repo missing from projects.json is listed under "New - not described yet".
Run: python build_projects_pdf.py   ->  FOCUS_Projects_GitHub_YYYYMMDD_HHMMSS.pdf (never overwrites)

Template notes:

INK-SAVING FORMAT — RULES (read before every PDF project):
  - White page background always — no fills, no bands, no shading
  - NO colored line bands anywhere — no orange/navy rules as decorative bands
  - Page header: white background, navy bold title, thin navy bottom rule only
  - Page footer: white background, grey text, thin grey top rule — min 0.5 inch (36pt) from bottom edge
  - Section titles (locked 2026-08-04): LIGHT_GREY band, accent (NAVY default) bold text,
    accent left bar (LINEBEFORE 3.5pt) + accent underline (LINEBELOW 0.8pt), 0.4pt MID_GREY box —
    use section_bar(); NEVER a solid navy/orange/brand-colour BACKGROUND fill
  - Table headers: LIGHT_GREY background only, navy bold text — NO colored rule bands
  - Table data rows: alternate WHITE / ROW_ALT only — no colored fills
  - Body text: BLACK on white
  - Accent colors used ONLY for data text highlights, never for fills or bands

USAGE:
  Copy this file into your project and rename it (e.g. generate_mypdf.py).
  Replace the build() story content with your own.
  Run: python generate_mypdf.py

DEPENDENCIES: pip install reportlab
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from datetime import datetime
from xml.sax.saxutils import escape
import json
import os
import urllib.request

# ── Brand Colors ─────────────────────────────────────────────────────────────
# Use these exactly — no new background fill colors
NAVY       = colors.Color(0.0,   0.168627, 0.360784)    # rgb(0, 43, 92)
ORANGE     = colors.Color(0.901961, 0.360784, 0.0)      # rgb(230, 92, 0)  — text only
DARK_GREY  = colors.Color(0.266667, 0.266667, 0.266667) # rgb(68, 68, 68)
BLACK      = colors.black
WHITE      = colors.white
LIGHT_GREY = colors.Color(0.94, 0.94, 0.94)   # table header bg only
MID_GREY   = colors.Color(0.82, 0.82, 0.82)   # rules and grid lines
ROW_ALT    = colors.Color(0.97, 0.97, 0.97)   # table row alt — very subtle
GREEN_DARK = colors.Color(0.05, 0.38, 0.15)
RED_DARK   = colors.Color(0.55, 0.10, 0.02)
BLUE_MID   = colors.Color(0.10, 0.35, 0.65)

# ── Page Geometry ─────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter
MARGIN_L = MARGIN_R = 48.0
MARGIN_T = 52.0
MARGIN_B = 72.0    # 1 inch bottom margin — keeps footer well within safe zone
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R   # ~516 pt usable width

# ── Style Factory ─────────────────────────────────────────────────────────────
def S(name, **kw):
    d = dict(fontName="Helvetica", fontSize=9, leading=13,
             textColor=BLACK, spaceAfter=0, spaceBefore=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

# Title block
CTIT_S  = S("ct",  fontName="Helvetica-Bold", fontSize=20, textColor=NAVY,      leading=26, alignment=TA_CENTER)
CSUB_S  = S("cs",  fontSize=10, textColor=NAVY,  leading=14, alignment=TA_CENTER)
CDATE_S = S("cd",  fontSize=8,  textColor=DARK_GREY, leading=12, alignment=TA_CENTER)
DISC_S  = S("ds",  fontName="Helvetica-Oblique", fontSize=7, textColor=DARK_GREY, leading=10, alignment=TA_CENTER)

# Section headers — text style for section_bar() (LIGHT_GREY band + accent left bar/underline, no fill)
SEC_S   = S("sc",  fontName="Helvetica-Bold", fontSize=10, textColor=NAVY, leading=14)

# Body text
BODY_S  = S("bd",  fontSize=8.5, textColor=BLACK,     leading=12.5)
BOLD_S  = S("bo",  fontName="Helvetica-Bold", fontSize=8.5, textColor=BLACK, leading=12.5)
NAVY_S  = S("nv",  fontName="Helvetica-Bold", fontSize=8.5, textColor=NAVY,  leading=12.5)
SMALL_S = S("sm",  fontSize=7.5, textColor=BLACK,     leading=11)
LINK_S  = S("lk",  fontSize=8,   textColor=BLUE_MID,  leading=11)
WARN_S  = S("wn",  fontSize=8.5, textColor=RED_DARK,  leading=12.5)
BUL_S   = S("bl",  fontSize=8.5, textColor=BLACK,     leading=13, leftIndent=10)

# Footer styles
FOOT_S  = S("ft",  fontSize=6.5, textColor=DARK_GREY, leading=9,  alignment=TA_CENTER)
VERSE_S = S("vs",  fontSize=6,   textColor=ORANGE,    leading=9,  alignment=TA_CENTER)
COPY_S  = S("cp",  fontSize=5.5, textColor=DARK_GREY, leading=8,  alignment=TA_CENTER)

# Table styles — header uses LIGHT_GREY fill only, never navy/colored fill
TH_S    = S("th",  fontName="Helvetica-Bold", fontSize=7.5, textColor=NAVY,  leading=10, alignment=TA_CENTER)
TD_S    = S("td",  fontSize=7.5, textColor=BLACK, leading=11, alignment=TA_CENTER)
TD_L    = S("tdl", fontSize=7.5, textColor=BLACK, leading=11, alignment=TA_LEFT)
TD_B    = S("tdb", fontName="Helvetica-Bold", fontSize=7.5, textColor=NAVY,  leading=11, alignment=TA_LEFT)

# ── Page Header / Footer ──────────────────────────────────────────────────────
NOW_STR  = datetime.now().strftime("%Y-%m-%d %H:%M")
DATE_STR = datetime.now().strftime("%Y-%m-%d")

PROJECT_TITLE = "F.O.C.U.S.© — Projects"
FOOTER_LABEL  = "Projects directory"

def on_page(canvas, doc):
    canvas.saveState()

    # ── PAGE HEADER ──────────────────────────────────────────────────────────
    # White background, navy text, single thin navy rule at bottom — NO colored bands
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(MARGIN_L, PAGE_H - 20, PROJECT_TITLE)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(DARK_GREY)
    canvas.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 20, f"Jachbit 2026  |  {DATE_STR}")
    canvas.setStrokeColor(MID_GREY)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, PAGE_H - 24, PAGE_W - MARGIN_R, PAGE_H - 24)

    # ── PAGE FOOTER ──────────────────────────────────────────────────────────
    # Content starts at 54pt (~0.75 inch) from bottom — well within safe print margin
    # Thin grey rule only — NO orange/colored bands
    canvas.setStrokeColor(MID_GREY)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN_L, 54, PAGE_W - MARGIN_R, 54)

    # Line 1: document label (center) + page number (right)
    canvas.setFillColor(DARK_GREY)
    canvas.setFont("Helvetica", 6.5)
    canvas.drawCentredString(PAGE_W / 2, 44, f"F.O.C.U.S.©  |  Jachbit 2026  |  {FOOTER_LABEL}")
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 6.5)
    canvas.drawRightString(PAGE_W - MARGIN_R, 44, f"Page {doc.page}")

    # Line 2: Bible verses — black bold, centered
    canvas.setFillColor(BLACK)
    canvas.setFont("Helvetica-Bold", 6)
    canvas.drawCentredString(PAGE_W / 2, 33,
        "John 3:16   |   1 John 3:16   |   Matt 6:33   |   Jer 33:3   |   Prov 3:5-6   |   Prov 27:17")

    # Line 3: copyright
    canvas.setFillColor(DARK_GREY)
    canvas.setFont("Helvetica", 5.5)
    canvas.drawCentredString(PAGE_W / 2, 22,
        "© 2026 Jachbit. All rights reserved. May not be copied or shared without express written consent of the publisher.  linktr.ee/jachbit")

    canvas.restoreState()

# ── Reusable Helpers ──────────────────────────────────────────────────────────
def sp(n=6):
    """Vertical spacer."""
    return Spacer(1, n)

def section_bar(text, accent=NAVY):
    """
    Section header (rule locked 2026-08-04) — 1-cell Table: LIGHT_GREY band,
    accent bold text, accent LEFT BAR (3.5pt) + accent UNDERLINE (0.8pt), 0.4pt MID_GREY box.
    NEVER a solid accent fill. NAVY is the default accent.
    """
    t = Table([[Paragraph(text, ParagraphStyle("sc_acc", parent=SEC_S, textColor=accent))]],
              colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT_GREY),
        ("LINEBEFORE",    (0,0), (0,0),   3.5, accent),
        ("LINEBELOW",     (0,0), (-1,-1), 0.8, accent),
        ("BOX",           (0,0), (-1,-1), 0.4, MID_GREY),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
    ]))
    return t

def grey_rule():
    """Thin grey divider rule — use between sections."""
    return HRFlowable(width=CONTENT_W, thickness=0.5, color=MID_GREY, spaceAfter=6, spaceBefore=4)

def std_table_style(has_header=True):
    """
    Standard table style: LIGHT_GREY header row (navy text), alternating white/ROW_ALT,
    grey grid lines. No orange bands anywhere.
    """
    base = [
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, ROW_ALT]),
        ("LINEBELOW",     (0,0), (-1,-2), 0.3, MID_GREY),
        ("BOX",           (0,0), (-1,-1), 0.5, MID_GREY),
        ("GRID",          (0,0), (-1,-1), 0.3, MID_GREY),
    ]
    if has_header:
        base += [
            ("BACKGROUND",  (0,0), (-1,0), LIGHT_GREY),
            ("LINEBELOW",   (0,0), (-1,0), 0.5, MID_GREY),  # grey only — no orange
        ]
    return TableStyle(base)

def info_table_style():
    """
    Two-column info table (label | value). No header row. White/ROW_ALT alternating.
    """
    return TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("ROWBACKGROUNDS",(0,0), (-1,-1), [WHITE, ROW_ALT]),
        ("LINEBELOW",     (0,0), (-1,-2), 0.4, MID_GREY),
        ("BOX",           (0,0), (-1,-1), 0.5, MID_GREY),
    ])

# ── Data: projects.json + the public GitHub repo list ─────────────────────────
HERE     = os.path.dirname(os.path.abspath(__file__))
SELF     = "FOCUS-Projects"
NEW_CAT  = "New - not described yet"

def load_projects():
    with open(os.path.join(HERE, "projects.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    owner = cfg["owner"]
    repos = []
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{owner}/repos?per_page=100",
                                     headers={"User-Agent": "focus-projects-pdf"})
        with urllib.request.urlopen(req, timeout=15) as r:
            repos = json.load(r)
    except Exception as e:
        print(f"GitHub list not read ({e}) - using projects.json only")
    by_name = {r["name"].lower(): r for r in repos}
    out = []
    for p in cfg["projects"]:
        gh = by_name.get(p["repo"].lower(), {})
        out.append(dict(p, code=f"https://github.com/{owner}/{p['repo']}", pushed=gh.get("pushed_at")))
    listed = {p["repo"].lower() for p in cfg["projects"]}
    for r in repos:
        if r.get("fork") or r["name"].lower() in listed or r["name"] == SELF:
            continue
        out.append(dict(repo=r["name"], title=r["name"], category=NEW_CAT,
                        description=r.get("description") or "Added to GitHub recently - not described yet.",
                        site=f"https://{owner}.github.io/{r['name']}/" if r.get("has_pages") else None,
                        code=r["html_url"], pushed=r.get("pushed_at")))
    cats = list(cfg["categories"])
    for p in out:
        if p["category"] not in cats:
            cats.append(p["category"])
    return owner, cats, out

def link(url):
    u = escape(url)
    return f'<link href="{u}" color="#1a59a6">{u}</link>'

# ── Build Function ────────────────────────────────────────────────────────────
def build():
    owner, cats, projects = load_projects()
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(HERE, f"FOCUS_Projects_GitHub_{ts}.pdf")

    doc = SimpleDocTemplate(
        out,
        pagesize=letter,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T,  bottomMargin=MARGIN_B,
        title="F.O.C.U.S.© — Projects",
        author="Jachbit 2026",
    )

    live = sum(1 for p in projects if p.get("site"))
    story = []

    # ── Title Block ───────────────────────────────────────────────────────────
    story.append(sp(6))
    story.append(Paragraph("F.O.C.U.S.©", CSUB_S))
    story.append(sp(4))
    story.append(Paragraph("Projects", CTIT_S))
    story.append(sp(6))
    story.append(Paragraph("Every public F.O.C.U.S. project on GitHub, with its live page and its code", CDATE_S))
    story.append(sp(4))
    story.append(Paragraph(f"Jachbit 2026  ·  {NOW_STR}  ·  {len(projects)} projects ({live} with a live page)  ·  "
                           f"all categories  ·  github.com/{owner}", DISC_S))
    story.append(sp(4))
    story.append(Paragraph(f"Online version (always current): {link(f'https://{owner}.github.io/{SELF}/')}", 
                           ParagraphStyle("ol", parent=CDATE_S)))
    story.append(sp(8))
    story.append(grey_rule())

    col_w = [CONTENT_W * 0.30, CONTENT_W * 0.70]
    n = 0
    for c in cats:
        items = [p for p in projects if p["category"] == c]
        if not items:
            continue
        n += 1
        rows = [[Paragraph("PROJECT", TH_S), Paragraph("WHAT IT IS  ·  LINKS", TH_S)]]
        for p in items:
            status = ("<font color='#0d6126'><b>Live page</b></font>" if p.get("site")
                      else "<font color='#8c1a05'><b>Runs locally</b></font>")
            if c == NEW_CAT:
                status = "<font color='#8c1a05'><b>New</b></font>"
            upd = f"  ·  updated {p['pushed'][:10]}" if p.get("pushed") else ""
            left = Paragraph(f"<b>{escape(p['title'])}</b><br/><font size='6.5'>repo: {escape(p['repo'])}</font><br/>"
                             f"<font size='6.5'>{status}{upd}</font>", TD_B)
            right = [escape(p["description"])]
            if p.get("site"):
                right.append(f"<b>Page:</b> {link(p['site'])}")
            right.append(f"<b>Code:</b> {link(p['code'])}")
            rows.append([left, Paragraph("<br/>".join(right), TD_L)])
        t = Table(rows, colWidths=col_w, repeatRows=1)
        st = std_table_style()
        st.add("VALIGN", (0, 0), (-1, -1), "TOP")
        t.setStyle(st)
        story.append(KeepTogether([section_bar(f"{n}.  {c.upper()}  ({len(items)})"), sp(6), t]))
        story.append(sp(10))

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF generated: {out}")

if __name__ == "__main__":
    build()
