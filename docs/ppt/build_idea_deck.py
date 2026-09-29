"""Fill the SIH 2026 idea-submission template with Mantle content.

Reads the official template, replaces the prompt text boxes with real
content, embeds rendered plan diagrams, drops the instructions slide
(the template itself caps the deck at 6 slides including the title),
and writes docs/ppt/Mantle_SIH26120.pptx.

Usage:  python3 docs/ppt/build_idea_deck.py
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

TEMPLATE = "/Users/abhinav/Downloads/SIH2026-IDEA-Presentation-Format.pptx"
OUT = "/Users/abhinav/Projects/mantle/docs/ppt/Mantle_SIH26120.pptx"
ASSETS = "/Users/abhinav/Projects/mantle/docs/ppt/assets"

BODY = "Arial"
TITLE_FONT = "Times New Roman"

# Palette: template blue + the SIH bulb's orange and green.
BLUE = RGBColor(0x00, 0x70, 0xC0)
NAVY = RGBColor(0x17, 0x2B, 0x4D)
ORANGE = RGBColor(0xC5, 0x5A, 0x11)
GREEN = RGBColor(0x4E, 0x7B, 0x2D)
INK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x59, 0x59, 0x59)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
T_BLUE = RGBColor(0xDE, 0xEA, 0xF6)   # light tints for card fills
T_ORANGE = RGBColor(0xFB, 0xE9, 0xDC)
T_GREEN = RGBColor(0xE6, 0xEF, 0xDB)
T_GREY = RGBColor(0xF2, 0xF2, 0xF2)
CARD_LINE = RGBColor(0xBF, 0xBF, 0xBF)


# ---------------------------------------------------------------- helpers

def para(tf, text, size=11, bold=False, italic=False, color=INK,
         space_after=4, space_before=0, align=None, first=False,
         font=BODY):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    if align is not None:
        p.alignment = align
    p.space_after = Pt(space_after)
    if space_before:
        p.space_before = Pt(space_before)
    r = p.add_run()
    r.text = text
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return p


def rich(tf, runs, size=11, space_after=4, first=False, align=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    if align is not None:
        p.alignment = align
    p.space_after = Pt(space_after)
    for text, bold, color in runs:
        r = p.add_run()
        r.text = text
        r.font.name = BODY
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return p


def box(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w),
                                  Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.02)
    tf.margin_top = tf.margin_bottom = Inches(0.01)
    return tf


def card(slide, x, y, w, h, fill, accent=None):
    """Rounded-corner card; optional accent bar down the left edge."""
    sp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                Inches(x), Inches(y), Inches(w),
                                Inches(h))
    sp.adjustments[0] = 0.045
    sp.fill.solid()
    sp.fill.fore_color.rgb = fill
    sp.line.color.rgb = CARD_LINE
    sp.line.width = Pt(0.75)
    sp.shadow.inherit = False
    if accent is not None:
        bar = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y + 0.10),
            Inches(0.075), Inches(h - 0.20))
        bar.adjustments[0] = 0.5
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.fill.background()
        bar.shadow.inherit = False
    return sp


def chip(slide, x, y, w, h, text, fill, size=10.5):
    sp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                Inches(x), Inches(y), Inches(w),
                                Inches(h))
    sp.adjustments[0] = 0.5
    sp.fill.solid()
    sp.fill.fore_color.rgb = fill
    sp.line.fill.background()
    sp.shadow.inherit = False
    tf = sp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = Inches(0.0)
    para(tf, text, size=size, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, space_after=0, first=True)
    return sp


def find(slide, name):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    raise KeyError(name)


def kill(slide, name):
    sp = find(slide, name)
    sp._element.getparent().remove(sp._element)


def set_team(slide):
    for sh in slide.shapes:
        if sh.name.startswith("Oval") and sh.has_text_frame \
                and "Team Name" in sh.text_frame.text:
            tf = sh.text_frame
            tf.clear()
            tf.word_wrap = True
            para(tf, "TEAM", size=9, bold=True, color=NAVY,
                 align=PP_ALIGN.CENTER, space_after=0, first=True)
            para(tf, "MANTLE", size=11, bold=True, color=BLUE,
                 align=PP_ALIGN.CENTER, space_after=0)


def add_pic(slide, path, x, y, max_w, max_h):
    w_px, h_px = Image.open(path).size
    ar = w_px / h_px
    w, h = max_w, max_w / ar
    if h > max_h:
        h = max_h
        w = h * ar
    return slide.shapes.add_picture(
        path, Inches(x + (max_w - w) / 2), Inches(y + (max_h - h) / 2),
        Inches(w), Inches(h))


def title_accent(slide):
    """Thin two-tone rule under the slide title."""
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45),
                                 Inches(1.02), Inches(2.6),
                                 Inches(0.045))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()
    bar.shadow.inherit = False
    seg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45),
                                 Inches(1.02), Inches(0.55),
                                 Inches(0.045))
    seg.fill.solid()
    seg.fill.fore_color.rgb = ORANGE
    seg.line.fill.background()
    seg.shadow.inherit = False


prs = Presentation(TEMPLATE)
slides = list(prs.slides)

# ================================================================ slide 0
s = slides[0]
sub = find(s, "Subtitle 3")
sub.text_frame.clear()
para(sub.text_frame, "MANTLE", size=44, bold=True, color=NAVY,
     font=TITLE_FONT, space_after=2, first=True)
para(sub.text_frame,
     "Well-to-Surface Digital Twin for CSS + SRP Heavy-Oil Wells",
     size=18, italic=True, color=BLUE, font=TITLE_FONT)

tb = find(s, "TextBox 9").text_frame
tb.clear()
tb.word_wrap = True
fields = [
    ("Problem Statement ID –  ", "SIH26120"),
    ("Problem Statement Title –  ",
     "Digital Twin for Well-to-Surface Optimization of Cyclic Steam "
     "Stimulation (CSS) and Sucker Rod Pump (SRP) Operations for Heavy "
     "Oil Wells of Baghewala Field"),
    ("Theme –  ", "Smart Automation"),
    ("PS Category –  ", "Software"),
    ("Team ID –  ", "[from SIH portal]"),
    ("Team Name (Registered on portal) –  ", "[team name]"),
]
for i, (k, v) in enumerate(fields):
    p = tb.paragraphs[0] if i == 0 else tb.add_paragraph()
    p.space_after = Pt(9)
    for txt, bold in ((k, True), (v, False)):
        r = p.add_run()
        r.text = txt
        r.font.name = BODY
        r.font.size = Pt(19)
        r.font.bold = bold
        r.font.color.rgb = INK

# ================================================================ slide 1
s = slides[1]
set_team(s)
title = find(s, "Title 1").text_frame
runs = title.paragraphs[0].runs
runs[0].text = " "
runs[1].text = "IDEA TITLE — MANTLE"
title_accent(s)
kill(s, "TextBox 8")

# Hero strip
hero = card(s, 0.45, 1.18, 8.45, 1.02, NAVY)
htf = hero.text_frame
htf.word_wrap = True
htf.vertical_anchor = MSO_ANCHOR.MIDDLE
htf.margin_left = Inches(0.22)
htf.margin_right = Inches(0.15)
htf.margin_top = Inches(0.08)
rich(htf, [("MANTLE   ", True, WHITE),
           ("a flight simulator and autopilot for a heavy-oil well — "
            "steam and lift decided as one.", False,
            RGBColor(0xCF, 0xE2, 0xF3))], size=15, first=True,
     space_after=0)

SECTIONS = [
    ("WHAT IT IS", BLUE, T_BLUE, [
        "One live physics twin of the whole chain — steam → reservoir "
        "heat T(r,z) → viscosity → inflow → pump → 1.1-km rod string → "
        "oil · energy · ₹ · CO₂ — synced to telemetry by an EnKF "
        "(P10–P90 on every forecast).",
        "Joint optimizer screens ~5,000 CSS + SRP plans → full-physics "
        "verify → deterministic Safety Gate vetoes unsafe plans → "
        "recommended schedule with its drivers named.",
    ]),
    ("HOW IT ANSWERS THE PS", ORANGE, T_ORANGE, [
        "Kills the statement's core flaw — “optimized separately”: "
        "steam + lift become ONE decision; the Coupling Dividend "
        "(Vjoint − Vseq, ₹ + bbl, Shapley) prices what silos lose.",
        "Predicts heating / cooling / production; re-plans SPM · "
        "stroke · VFD as viscosity climbs; float margin + wave-equation "
        "impact + dynocard classifier catch failures early.",
    ]),
    ("WHAT'S NEW", GREEN, T_GREEN, [
        "Physics-rendered 3D twin ⇄ living Blueprint · Stroke Shaper "
        "in-stroke VFD profiling · Strategy Arena vs 8 baselines + "
        "oracle · hash-chained decision ledger · provenance on every "
        "number.",
    ]),
]
y = 2.38
for label, col, tint, bullets in SECTIONS:
    chip(s, 0.45, y, 2.35, 0.34, label, col)
    tf = box(s, 0.55, y + 0.40, 8.3, 1.15)
    for j, b in enumerate(bullets):
        para(tf, "•  " + b, size=10.5, space_after=3, first=(j == 0))
    y += 1.52

# Right: physics-chain diagram in a card
card(s, 9.15, 1.18, 3.75, 5.5, T_GREY)
add_pic(s, f"{ASSETS}/diagram-01.png", 9.30, 1.32, 3.45, 4.45)
cap = box(s, 9.30, 5.80, 3.45, 0.8)
para(cap, "The coupled chain — the steam plan sets the viscosity path; "
        "viscosity sets the safe pumping envelope.", size=9,
     italic=True, color=GREY, align=PP_ALIGN.CENTER, first=True)

# ================================================================ slide 2
s = slides[2]
set_team(s)
title_accent(s)
kill(s, "TextBox 8")

STACK = [
    ("FRONTEND", BLUE, T_BLUE,
     "Next.js + React + TypeScript · React Three Fiber / Three.js 3D "
     "twin · D3 / visx charts · GSAP"),
    ("ENGINE — PYTHON (uv)", ORANGE, T_ORANGE,
     "FastAPI · NumPy / SciPy / Numba physics · LightGBM + 1D-CNN "
     "dynocard classifier · custom EnKF · pymoo NSGA-III · OR-Tools "
     "CP-SAT · Stable-Baselines3 PPO"),
    ("PLATFORM", GREEN, T_GREEN,
     "PostgreSQL + TimescaleDB · Redis streams · MinIO · Mosquitto "
     "MQTT (OPC-UA ready) · Caddy · Docker Compose — one command, "
     "fully offline"),
]
for i, (head, col, tint, txt) in enumerate(STACK):
    x = 0.45 + i * 4.25
    c = card(s, x, 1.18, 4.0, 1.62, tint, accent=col)
    tf = c.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.08)
    tf.margin_top = Inches(0.07)
    para(tf, head, size=11, bold=True, color=col, space_after=3,
         align=PP_ALIGN.LEFT, first=True)
    para(tf, txt, size=9.5, space_after=0, align=PP_ALIGN.LEFT)

# Methodology chevron flow
steps = ["Telemetry\nMQTT", "Data-quality\naudit", "EnKF twin\nP10–P90",
         "Forecast\nfan", "NSGA-III\n~5k plans", "Physics +\nSafety Gate",
         "Schedule →\nledger score"]
chip(s, 0.45, 3.02, 4.4, 0.34, "METHOD — ONE CLOSED LOOP, EVERY CYCLE",
     NAVY)
x = 0.45
for i, st in enumerate(steps):
    cv = s.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(3.5),
                            Inches(1.83), Inches(0.78))
    cv.adjustments[0] = 0.35
    cv.fill.solid()
    cv.fill.fore_color.rgb = BLUE if i % 2 == 0 else NAVY
    cv.line.fill.background()
    cv.shadow.inherit = False
    tf = cv.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.02)
    tf.margin_top = tf.margin_bottom = Inches(0.0)
    for j, ln in enumerate(st.split("\n")):
        para(tf, ln, size=9, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, space_after=0, first=(j == 0))
    x += 1.74

# Bottom: physics rigor + arena bullets  |  architecture diagram
tf = box(s, 0.45, 4.55, 6.85, 2.2)
para(tf, "ENGINEERING RIGOUR", size=11, bold=True, color=BLUE,
     space_after=3, first=True)
para(tf, "•  All physics from published standards — IAPWS-IF97, "
        "Ramey / Willhite, Marx–Langenheim + r–z thermal grid, "
        "Walther / ASTM D341, Boberg–Lantz, Gibbs wave equation, "
        "API RP 11L, Modified Goodman — each unit-tested against its "
        "worked example.", size=10.5, space_after=4)
para(tf, "PROTOTYPE PROOF", size=11, bold=True, color=ORANGE,
     space_after=3)
para(tf, "•  Strategy Arena races 9 strategies — static, tuned, "
        "heuristic, pump-off, greedy, sequential-silo, shielded RL, "
        "Mantle joint MPC, oracle bound — on identical simulated wells "
        "with paired confidence intervals.", size=10.5, space_after=0)

card(s, 7.5, 4.5, 5.4, 2.3, T_GREY)
add_pic(s, f"{ASSETS}/diagram-08.png", 7.62, 4.56, 5.16, 1.92)
cap = box(s, 7.62, 6.5, 5.16, 0.26)
para(cap, "System context — synthetic SCADA today; OIL SCADA via the "
        "same MQTT / OPC-UA path.", size=8.5, italic=True, color=GREY,
     align=PP_ALIGN.CENTER, first=True, space_after=0)

# ================================================================ slide 3
s = slides[3]
set_team(s)
title_accent(s)
kill(s, "TextBox 8")

FEAS = [
    ("NO RESEARCH RISK", BLUE, T_BLUE,
     "Every model is a published standard or paper; open-source "
     "stack; runs fully offline on one laptop — docker compose up."),
    ("NO PUBLIC WELL DATA", ORANGE, T_ORANGE,
     "So we built Baghewala-S: a physics-synthetic field (30 wells × "
     "3 yrs, noise, faults, failures) calibrated to OIL anchors — "
     "17–19° API · 46–48 °C · ~10–13 kcP · 14–21 d steam."),
    ("REAL-DATA READY", GREEN, T_GREEN,
     "Canonical schema maps 1:1 to the PS's 7 data categories; "
     "MQTT / OPC-UA / CSV adapters need no code change; EnKF is the "
     "calibration path; anomaly pipeline validated on real "
     "Petrobras 3W data."),
]
for i, (head, col, tint, txt) in enumerate(FEAS):
    x = 0.45 + i * 4.25
    c = card(s, x, 1.18, 4.0, 1.82, tint, accent=col)
    tf = c.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.1)
    tf.margin_top = Inches(0.08)
    para(tf, head, size=11, bold=True, color=col, space_after=3,
         align=PP_ALIGN.LEFT, first=True)
    para(tf, txt, size=10, space_after=0, align=PP_ALIGN.LEFT)

chip(s, 0.45, 3.26, 3.6, 0.34, "CHALLENGES  →  HOW WE BEAT THEM", NAVY)
rows = [
    ("Venue machine can't run the 3D twin",
     "Own laptop · auto-quality ladder · pre-rendered transition video "
     "· whole demo runs offline"),
    ("Judges challenge synthetic data",
     "SIM tag on every number · source + assumption registries · "
     "Petrobras 3W real-data validation · never sold as field results"),
    ("Physics too slow for a live demo",
     "Surrogates pre-screen, full physics verifies · pre-computed "
     "official Arena run + < 30 s live mini-run"),
    ("Scope sprawl / nothing polished",
     "13 phases, each with a demoable exit · main always green · "
     "golden-scenario tests"),
    ("RL contender underperforms",
     "RL is only a benchmarked Arena contender — the MPC core never "
     "depends on it; the Arena reports either result honestly"),
]
tbl = s.shapes.add_table(len(rows) + 1, 2, Inches(0.45), Inches(3.76),
                         Inches(12.45), Inches(3.0)).table
tbl.columns[0].width = Inches(4.1)
tbl.columns[1].width = Inches(8.35)
for cell, txt in zip(tbl.rows[0].cells,
                     ("RISK / CHALLENGE", "MITIGATION")):
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_top = cell.margin_bottom = Inches(0.04)
    p = cell.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = txt
    r.font.name = BODY
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = WHITE
for i, (a, b) in enumerate(rows, start=1):
    for cell, txt, bold, fill in (
            (tbl.rows[i].cells[0], a, True, T_ORANGE),
            (tbl.rows[i].cells[1], b, False,
             WHITE if i % 2 else T_BLUE)):
        cell.text = ""
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_top = cell.margin_bottom = Inches(0.03)
        cell.margin_left = Inches(0.1)
        p = cell.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = txt
        r.font.name = BODY
        r.font.size = Pt(10.5)
        r.font.bold = bold
        r.font.color.rgb = INK

# ================================================================ slide 4
s = slides[4]
set_team(s)
title_accent(s)
kill(s, "TextBox 8")

aud = card(s, 0.45, 1.15, 12.45, 0.62, T_BLUE)
atf = aud.text_frame
atf.word_wrap = True
atf.vertical_anchor = MSO_ANCHOR.MIDDLE
atf.margin_left = Inches(0.18)
atf.margin_top = Inches(0.05)
rich(atf, [("TARGET AUDIENCE   ", True, NAVY),
           ("Oil India production engineers & field managers on "
            "Baghewala CSS + SRP wells — and, at fleet scale, India's "
            "domestic heavy-oil output (India imports most of its "
            "crude).", False, INK)], size=11.5, first=True,
     space_after=0)

COLS = [
    ("ECONOMIC", BLUE, T_BLUE, [
        "↑ oil recovered per cycle & per 180 d",
        "Coupling Dividend — measurable ₹/cycle from joint "
        "optimization",
        "↓ lifting cost ₹/bbl (steam + power + water + maintenance)",
        "fewer rod failures, unsettings, workovers, deferred oil",
        "longer equipment life (tracked Goodman fatigue)",
        "field scheduler sends scarce steam-days to highest-value "
        "wells",
    ]),
    ("ENVIRONMENTAL", GREEN, T_GREEN, [
        "↓ SOR → less fuel gas burned per barrel",
        "↓ CO₂e/bbl (IPCC + CEA emission factors)",
        "↓ fresh water/bbl — the scarcest resource in the Thar",
        "solar-thermal steam hybrid (Rajasthan DNI) option",
        "fewer workovers → less diesel, less waste",
    ]),
    ("SOCIAL", ORANGE, T_ORANGE, [
        "fewer high-risk states → fewer emergency interventions",
        "fewer unplanned site visits in 45–48 °C heat "
        "(heat-stress exposure)",
        "senior operators' judgement captured as institutional memory",
        "Challenge mode = safe training sim for young engineers",
        "every decision auditable → field–office trust",
    ]),
]
for i, (head, col, tint, items) in enumerate(COLS):
    x = 0.45 + i * 4.25
    c = card(s, x, 1.95, 4.0, 4.25, tint)
    tf = c.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.16)
    tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.1)
    para(tf, head, size=12.5, bold=True, color=col, space_after=5,
         align=PP_ALIGN.LEFT, first=True)
    for it in items:
        para(tf, "•  " + it, size=10.5, space_after=4,
             align=PP_ALIGN.LEFT)

foot = card(s, 0.45, 6.32, 12.45, 0.5, T_GREY)
ftf = foot.text_frame
ftf.word_wrap = True
ftf.vertical_anchor = MSO_ANCHOR.MIDDLE
ftf.margin_left = Inches(0.18)
ftf.margin_top = Inches(0.04)
rich(ftf, [("METHOD   ", True, NAVY),
           ("every figure is Mantle-vs-baseline on identical simulated "
            "wells (Baghewala-S, N seeds, mean ± sd), tagged SIM — "
            "never presented as field results.", False, GREY)],
     size=10, first=True, space_after=0)

# ================================================================ slide 5
s = slides[5]
set_team(s)
title_accent(s)
kill(s, "TextBox 8")

def ref_card(slide, x, w, groups):
    c = card(slide, x, 1.18, w, 4.45, T_GREY)
    tf = c.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.1)
    first = True
    for head, col, items in groups:
        para(tf, head, size=12.5, bold=True, color=col,
             space_after=4, space_before=0 if first else 10,
             align=PP_ALIGN.LEFT, first=first)
        first = False
        for it in items:
            para(tf, "•  " + it, size=11, space_after=3.5,
                 align=PP_ALIGN.LEFT)

ref_card(s, 0.45, 6.1, [
    ("FIELD & PROBLEM", BLUE, [
        "SIH 2026 Problem Statement SIH26120 (Oil India Limited)",
        "Oil India — Rajasthan Fields (Baghewala viscosity, CSS "
        "durations, VIT, completions)",
        "ACT SHARP consortium D4.1 (2022) — Baghewala geological "
        "characterization",
        "SPE papers on Baghewala CSS (e.g. APOG 2023)",
    ]),
    ("PHYSICS — FROM PRIMARY SOURCES", ORANGE, [
        "Marx & Langenheim (1959) reservoir heating · Boberg & Lantz "
        "(1966) stimulated productivity · Ramey (1962) + Willhite "
        "(1967) wellbore heat · Vogel (1968) inflow",
        "Gibbs (1963) rod-pump wave equation · Everitt & Jennings "
        "(1992) downhole cards · API RP 11L / Spec 11E / RP 11BR · "
        "ASTM D341 · IAPWS-IF97",
    ]),
])

ref_card(s, 6.8, 6.1, [
    ("ESTIMATION, ML & OPTIMIZATION", GREEN, [
        "Evensen (2009) Ensemble Kalman Filter · Deb et al. (2002) "
        "NSGA-II · Angelopoulos & Bates (2021) conformal prediction · "
        "Lundberg & Lee (2017) SHAP",
        "Hansen et al. (2018) model-predictive sucker-rod-pump control "
        "(BYU-PRISM)",
    ]),
    ("DATA & STANDARDS", NAVY, [
        "Vargas et al. (2019) — Petrobras 3W dataset (Apache-2.0): "
        "real well-event data validating the anomaly pipeline",
        "ISA-101 HMI · ISA-18.2 alarms · ISO 128 drawing · "
        "ISO/PAS 12835 thermal casing connections",
        "Prior-art review — 25 public SIH26120 repos surveyed "
        "(29 Sep 2026); MIT data reused only with attribution",
    ]),
])

src = card(s, 0.45, 5.85, 12.45, 0.55, T_BLUE)
stf = src.text_frame
stf.word_wrap = True
stf.vertical_anchor = MSO_ANCHOR.MIDDLE
stf.margin_left = Inches(0.18)
stf.margin_top = Inches(0.04)
rich(stf, [("SOURCE TRUTH   ", True, NAVY),
           ("every constant carries a tag — PUB (published) · SIM "
            "(simulated) · ASSUM (assumption registry) · EST "
            "(estimated) · MEAS (measured). Full bibliography + "
            "verification status: plan.md Appendix D.",
            False, INK)], size=10.5, first=True, space_after=0)

# ================================================================ prune
xml_slides = prs.slides._sldIdLst
xml_slides.remove(list(xml_slides)[6])

prs.save(OUT)
print("wrote", OUT)
