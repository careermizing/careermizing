"""IMC 제안서용 장표 빌더 (python-pptx).

두 개의 모범 레퍼런스(아르르 푸드 / 에너지플러스)에서 뽑은 디자인 문법을
슬라이드 '유형(archetype)' 단위 함수로 옮긴 라이브러리.

원칙
- 한 덱에 색상 계열은 하나(PRIMARY 계열) + 중립 회색 + 경고 빨강만 쓴다.
- 장표 제목은 '주장 한 문장'(~합니다)이다. 핵심 구절만 ==하이라이트==.
- 본문 강조는 **굵게+주색**. 출처는 항상 작은 회색 캡션.
- 이미지/목업이 들어갈 자리는 image()/phone() 플레이스홀더로 비워 둔다.

좌표 단위는 inch, 슬라이드는 13.333 x 7.5 (16:9).
"""
from __future__ import annotations

import copy
import json
import os
import re
from dataclasses import dataclass, field

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# ----------------------------------------------------------------------------
# 디자인 토큰
# ----------------------------------------------------------------------------
TOKENS = {
    "font": "Pretendard",
    "primary": "138CB0",     # 주색 (핵심 막대, 필, 강조 글자)
    "deep": "0B5A73",        # 짙은 주색 (필 헤더 배경, 다크 라벨)
    "mid": "7FA9B8",         # 보조 칩/보조 막대
    "tint": "D9EEF4",        # 연한 면 (카드, 컬럼 배경)
    "tint2": "EAF6FA",       # 더 연한 면
    "hilite": "C9ECF5",      # 제목 하이라이트 배경
    "ink": "111111",         # 제목 글자
    "text": "2A2A2A",        # 본문 글자
    "mute": "8A8F94",        # 출처/보조 글자
    "gray": "E7E7E7",        # 비강조 막대/라벨 배경
    "gray2": "F0F0F0",       # 아주 연한 회색 면
    "bg": "F6F6F4",          # 기본 배경
    "white": "FFFFFF",
    "dark": "262A2D",        # 다크 슬라이드 배경
    "alert": "C62828",       # 이탈/문제 수치 (빨강, 최소한으로만)
}

SLIDE_W, SLIDE_H = 13.333, 7.5
MARGIN_X = 0.6


def load_tokens(path: str | None = None) -> dict:
    t = dict(TOKENS)
    if path and os.path.exists(path):
        t.update(json.load(open(path, encoding="utf-8")))
    return t


def rgb(h: str) -> RGBColor:
    return RGBColor.from_string(h.upper())


# ----------------------------------------------------------------------------
# 텍스트 폭 추정 (넘침 검수용)
# ----------------------------------------------------------------------------
_FONT_CACHE: dict = {}


def _pil_font(bold: bool, size: float):
    from PIL import ImageFont

    key = (bold, round(size * 4))
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    name = "Pretendard-Bold.otf" if bold else "Pretendard-Regular.otf"
    for base in (os.path.expanduser("~/.fonts"), "/usr/share/fonts", "/usr/local/share/fonts"):
        p = os.path.join(base, name)
        if os.path.exists(p):
            f = ImageFont.truetype(p, int(size * 4))
            _FONT_CACHE[key] = f
            return f
    _FONT_CACHE[key] = None
    return None


def text_width_pt(s: str, size: float, bold: bool = False, tracking: float = 0.0) -> float:
    f = _pil_font(bold, size)
    if f is None:  # 폰트 없으면 한글 1em, 영문 0.55em로 근사
        return sum(size if ord(c) > 0x2E80 else size * 0.55 for c in s)
    return f.getlength(s) / 4.0 + tracking * len(s)


def estimate_lines(text: str, size: float, box_w_in: float, bold=False, tracking=0.0) -> int:
    avail = box_w_in * 72
    lines = 0
    for para in text.split("\n"):
        plain = re.sub(r"(\*\*|==)", "", para)
        if not plain:
            lines += 1
            continue
        cur = 0.0
        n = 1
        for tok in re.findall(r"\S+\s*|\s+", plain):
            w = text_width_pt(tok, size, bold, tracking)
            if cur + w <= avail:
                cur += w
                continue
            if w > avail:  # 한 단어가 너무 길면 글자 단위
                for ch in tok:
                    cw = text_width_pt(ch, size, bold, tracking)
                    if cur + cw > avail:
                        n += 1
                        cur = 0
                    cur += cw
            else:
                n += 1
                cur = w
        lines += n
    return lines


# ----------------------------------------------------------------------------
# 낮은 수준 유틸
# ----------------------------------------------------------------------------
def _strip_style(shape):
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)


def _shadow(shape, blur=8, dist=2, alpha=18):
    spPr = shape._element.spPr
    for e in spPr.findall(qn("a:effectLst")):
        spPr.remove(e)
    eff = etree.SubElement(spPr, qn("a:effectLst"))
    sh = etree.SubElement(
        eff, qn("a:outerShdw"), blurRad=str(int(blur * 12700)), dist=str(int(dist * 12700)),
        dir="5400000", algn="t", rotWithShape="0",
    )
    c = etree.SubElement(sh, qn("a:srgbClr"), val="000000")
    etree.SubElement(c, qn("a:alpha"), val=str(alpha * 1000))


def _set_ea(run_font_el, face):
    rPr = run_font_el
    for tag in ("a:latin", "a:ea", "a:cs"):
        for e in rPr.findall(qn(tag)):
            rPr.remove(e)
    for tag in ("latin", "ea", "cs"):
        etree.SubElement(rPr, qn(f"a:{tag}"), typeface=face)


@dataclass
class Box:
    slide_idx: int
    name: str
    text: str
    size: float
    w: float
    h: float
    bold: bool
    tracking: float
    line_spacing: float


class Deck:
    def __init__(self, tokens: dict | None = None, brand: str = "", team: str = ""):
        self.t = tokens or load_tokens()
        self.prs = Presentation()
        self.prs.slide_width = Inches(SLIDE_W)
        self.prs.slide_height = Inches(SLIDE_H)
        self.blank = self.prs.slide_layouts[6]
        self.brand = brand
        self.team = team
        self._boxes: list[Box] = []
        self.page = 0

    # ---- 슬라이드 -----------------------------------------------------------
    def slide(self, mode: str = "light", section: str = "", number: bool = True, notes: str = ""):
        s = self.prs.slides.add_slide(self.blank)
        self.page += 1
        s._mode = mode
        bg = {"light": self.t["bg"], "dark": self.t["dark"], "deep": self.t["deep"], "white": self.t["white"]}[mode]
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(bg)
        if section:
            self.tag(s, section, dark=mode in ("dark", "deep"))
        if number:
            self.text(s, SLIDE_W - 1.1, SLIDE_H - 0.5, 0.6, 0.3, str(self.page), size=10,
                      color=self.t["mute"], align="r", name="pageno")
        if self.brand:
            self.text(s, SLIDE_W - 2.6, 0.28, 2.0, 0.3, self.brand, size=10, bold=True,
                      color=self.t["mute"] if mode == "light" else self.t["mid"], align="r", name="brand")
        if notes:
            s.notes_slide.notes_text_frame.text = notes
        return s

    # ---- 텍스트 -------------------------------------------------------------
    def text(self, s, x, y, w, h, text, size=14, bold=False, color=None, align="l", anchor="t",
             line_spacing=1.2, tracking=-0.2, name="", italic=False, wrap=True, em_color=None,
             hl_color=None, margin=0.0):
        """마크업: **강조**(굵게+주색), ==하이라이트==(배경색), \n 줄바꿈."""
        color = color or self.t["text"]
        dark = getattr(s, "_mode", "light") in ("dark", "deep")
        em_color = em_color or (self.t["hilite"] if dark else self.t["primary"])
        hl_color = hl_color or self.t["hilite"]
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = wrap
        tf.margin_left = tf.margin_right = Inches(margin)
        tf.margin_top = tf.margin_bottom = Inches(0)
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        paras = str(text).split("\n")
        for i, para in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
            p.line_spacing = line_spacing
            self._runs(p, para, size, bold, color, em_color, hl_color, tracking, italic)
        self._boxes.append(Box(self.page, name or str(text)[:20], str(text), size, w, h, bold, tracking, line_spacing))
        return tb

    def _runs(self, p, para, size, bold, color, em_color, hl_color, tracking, italic=False):
        # 토큰 분리: **..** / ==..==
        parts = re.split(r"(\*\*.+?\*\*|==.+?==)", para)
        for part in parts:
            if not part:
                continue
            kind = None
            if part.startswith("**") and part.endswith("**"):
                kind, part = "em", part[2:-2]
            elif part.startswith("==") and part.endswith("=="):
                kind, part = "hl", part[2:-2]
            r = p.add_run()
            r.text = part
            f = r.font
            f.size = Pt(size)
            f.bold = True if kind in ("em", "hl") else bold
            f.italic = italic
            f.color.rgb = rgb(em_color if kind == "em" else color)
            rPr = r._r.get_or_add_rPr()
            rPr.set("spc", str(int(tracking * 100)))
            rPr.set("lang", "ko-KR")
            rPr.set("altLang", "en-US")
            if kind == "hl":
                hl = etree.SubElement(rPr, qn("a:highlight"))
                etree.SubElement(hl, qn("a:srgbClr"), val=hl_color)
            # 폰트 (latin/ea/cs) — highlight 뒤에 와야 스키마 순서가 맞다
            _set_ea(rPr, self.t["font"])

    # ---- 도형 ---------------------------------------------------------------
    def rect(self, s, x, y, w, h, fill=None, line=None, line_w=0.75, dash=False, radius=0.0,
             shadow=False, shape=None, name=""):
        shp_type = shape or (MSO_SHAPE.ROUNDED_RECTANGLE if radius > 0 else MSO_SHAPE.RECTANGLE)
        shp = s.shapes.add_shape(shp_type, Inches(x), Inches(y), Inches(w), Inches(h))
        _strip_style(shp)
        if radius > 0 and shp_type == MSO_SHAPE.ROUNDED_RECTANGLE:
            shp.adjustments[0] = min(0.5, radius / min(w, h))
        if fill:
            shp.fill.solid()
            shp.fill.fore_color.rgb = rgb(fill)
        else:
            shp.fill.background()
        if line:
            shp.line.color.rgb = rgb(line)
            shp.line.width = Pt(line_w)
            if dash:
                shp.line.dash_style = MSO_LINE.DASH
        else:
            shp.line.fill.background()
        if shadow:
            _shadow(shp)
        if name:
            shp.name = name
        return shp

    def shape_text(self, shp, text, size=14, bold=False, color=None, align="c", anchor="m", line_spacing=1.15,
                   tracking=-0.2, margin=0.08, em_color=None, w=None, h=None):
        color = color or self.t["text"]
        tf = shp.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(margin)
        tf.margin_top = tf.margin_bottom = Inches(0.03)
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        dark_fill = False
        em_color = em_color or self.t["primary"]
        for i, para in enumerate(str(text).split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
            p.line_spacing = line_spacing
            self._runs(p, para, size, bold, color, em_color, self.t["hilite"], tracking)
        ww = w if w is not None else Emu(shp.width).inches
        hh = h if h is not None else Emu(shp.height).inches
        self._boxes.append(Box(self.page, str(text)[:20], str(text), size, ww - 2 * margin, hh - 0.06, bold, tracking, line_spacing))

    def line(self, s, x1, y1, x2, y2, color=None, w=1.0, dash=False, arrow=False):
        ln = s.shapes.add_connector(1, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        ln.line.color.rgb = rgb(color or self.t["primary"])
        ln.line.width = Pt(w)
        if dash:
            ln.line.dash_style = MSO_LINE.DASH
        if arrow:
            lnEl = ln.line._get_or_add_ln()
            etree.SubElement(lnEl, qn("a:tailEnd"), type="triangle", w="med", len="med")
        return ln

    def dot(self, s, cx, cy, d=0.12, fill=None):
        return self.rect(s, cx - d / 2, cy - d / 2, d, d, fill=fill or self.t["primary"], shape=MSO_SHAPE.OVAL)

    # ---- 공통 컴포넌트 ------------------------------------------------------
    def tag(self, s, text, dark=False):
        """좌상단 섹션 태그 ('시장분석 |')"""
        self.text(s, 0.55, 0.3, 4.0, 0.3, f"{text} |", size=12, bold=True,
                  color=self.t["mid"] if dark else self.t["primary"], name="tag")

    def title(self, s, text, y=0.78, size=26, sub=None, align="c", w=None, color=None):
        """주장 한 문장. 핵심 구절만 ==하이라이트==. 2줄 이내 권장."""
        dark = getattr(s, "_mode", "light") in ("dark", "deep")
        color = color or (self.t["white"] if dark else self.t["ink"])
        w = w or (SLIDE_W - 2 * MARGIN_X)
        lines = estimate_lines(text, size, w, bold=True, tracking=-0.5)
        h = lines * size * 1.3 / 72 + 0.05
        self.text(s, MARGIN_X, y, w, h, text, size=size, bold=True, color=color, align=align,
                  line_spacing=1.25, tracking=-0.5, name="title",
                  hl_color=self.t["hilite"] if not dark else self.t["primary"],
                  em_color=self.t["white"] if dark else self.t["ink"])
        if sub:
            self.text(s, MARGIN_X, y + h + 0.08, w, 0.3, sub, size=12, color=self.t["mute"], align=align, name="subtitle")
        return y + h

    def pill(self, s, x, y, w, text, h=0.44, fill=None, color=None, size=15, bold=True):
        shp = self.rect(s, x, y, w, h, fill=fill or self.t["deep"], radius=h / 2)
        self.shape_text(shp, text, size=size, bold=bold, color=color or self.t["white"], tracking=-0.2, margin=0.12)
        return shp

    def label(self, s, x, y, w, h, text, fill=None, color=None, size=13, bold=True):
        shp = self.rect(s, x, y, w, h, fill=fill or self.t["mid"])
        self.shape_text(shp, text, size=size, bold=bold, color=color or self.t["white"])
        return shp

    def source(self, s, text, x=None, y=None, w=None, align="r", size=10):
        x = MARGIN_X if x is None else x
        w = (SLIDE_W - 2 * MARGIN_X) if w is None else w
        y = (SLIDE_H - 0.55) if y is None else y
        self.text(s, x, y, w, 0.4, text, size=size, color=self.t["mute"], align=align, name="source", line_spacing=1.1)

    def callout(self, s, text, y=None, h=0.66, x=None, w=None, dark=False, size=19):
        """하단 결론 바. 라이트: 연회색 바 / 다크: 검정 바 (참조: 에너지플러스 p13)"""
        x = 0.0 if x is None and dark else (MARGIN_X if x is None else x)
        w = SLIDE_W if w is None and dark else ((SLIDE_W - 2 * MARGIN_X) if w is None else w)
        y = (SLIDE_H - 1.45) if y is None else y
        if dark:
            self.rect(s, x, y, w, SLIDE_H - y, fill=self.t["dark"])
            self.text(s, x + 0.6, y + 0.2, w - 1.2, SLIDE_H - y - 0.4, text, size=size + 3, bold=True,
                      color=self.t["white"], align="c", anchor="m", line_spacing=1.3, tracking=-0.4,
                      hl_color=self.t["primary"], em_color=self.t["white"], name="callout")
        else:
            box = self.rect(s, x, y, w, h, fill=self.t["gray"])
            self.shape_text(box, text, size=size, bold=True, color=self.t["ink"], tracking=-0.4)
        return y

    def image(self, s, x, y, w, h, label="IMAGE", fill=None):
        """이미지 자리표시. 나중에 목업/사진으로 교체."""
        shp = self.rect(s, x, y, w, h, fill=fill or self.t["gray2"], line=self.t["mid"], dash=True, line_w=1.0)
        self.shape_text(shp, f"[ IMAGE ]\n{label}", size=11, color=self.t["mute"], bold=False, line_spacing=1.3)
        return shp

    def phone(self, s, x, y, w=1.9, label="앱 화면 목업"):
        h = w * 2.05
        shp = self.rect(s, x, y, w, h, fill=self.t["white"], line=self.t["ink"], line_w=2.25, radius=0.28, shadow=True)
        self.rect(s, x + w * 0.34, y + 0.1, w * 0.32, 0.07, fill=self.t["ink"], radius=0.035)
        inner = self.rect(s, x + 0.12, y + 0.3, w - 0.24, h - 0.5, fill=self.t["gray2"], line=self.t["gray"], radius=0.12)
        self.shape_text(inner, f"[ MOCKUP ]\n{label}", size=10, color=self.t["mute"], line_spacing=1.3)
        return shp

    def avatar(self, s, cx, cy, d=0.78, fill=None):
        base = self.rect(s, cx - d / 2, cy - d / 2, d, d, fill=fill or self.t["tint"], shape=MSO_SHAPE.OVAL)
        self.rect(s, cx - d * 0.17, cy - d * 0.30, d * 0.34, d * 0.34, fill=self.t["mid"], shape=MSO_SHAPE.OVAL)
        self.rect(s, cx - d * 0.30, cy + d * 0.08, d * 0.60, d * 0.34, fill=self.t["mid"],
                  shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
        return base

    def bubble(self, s, x, y, w, h, quote, who="", side="l", size=14.5):
        """인터뷰 말풍선: 아바타 + 둥근 흰 박스 + 출처. **굵게**로 핵심어."""
        av = 0.78
        if side == "l":
            self.avatar(s, x + av / 2, y + h / 2 - 0.1, av)
            bx = x + av + 0.12
        else:
            self.avatar(s, x + w - av / 2, y + h / 2 - 0.1, av)
            bx = x
        bw = w - av - 0.12
        box = self.rect(s, bx, y, bw, h - 0.28, fill=self.t["white"], line=self.t["gray"], radius=0.22, shadow=True)
        self.shape_text(box, quote, size=size, color=self.t["text"], align="l", margin=0.18, tracking=-0.2,
                        line_spacing=1.25, em_color=self.t["ink"])
        if who:
            self.text(s, bx + 0.1, y + h - 0.25, bw, 0.22, who, size=10, color=self.t["mute"], name="who")

    def kpi_circle(self, s, cx, cy, d, big, label="", sub="", fill=None, big_size=40):
        c = self.rect(s, cx - d / 2, cy - d / 2, d, d, fill=fill or self.t["primary"], shape=MSO_SHAPE.OVAL)
        self.text(s, cx - d / 2 + 0.1, cy - d * 0.36, d - 0.2, 0.4, label, size=14, color=self.t["white"], align="c",
                  line_spacing=1.1, name="kpi_label")
        self.text(s, cx - d / 2, cy - d * 0.12, d, 0.8, big, size=big_size, bold=True, color=self.t["white"],
                  align="c", tracking=-1, name="kpi_big")
        if sub:
            self.text(s, cx - d / 2 + 0.1, cy + d * 0.26, d - 0.2, 0.3, sub, size=12, color=self.t["white"], align="c", name="kpi_sub")

    def hbar(self, s, x, y, w, rows, row_h=0.56, gap=0.16, label_w=2.3, focus=(), vmax=None,
             fmt="{v:g}%", box_focus=True, size=15):
        """가로 막대. focus 행만 주색(진), 나머지 회색. 포커스 구간은 점선 박스."""
        vmax = vmax or max(v for _, v in rows)
        bar_w = w - label_w - 0.9
        for i, (lab, v) in enumerate(rows):
            yy = y + i * (row_h + gap)
            isf = i in focus
            self.text(s, x, yy, label_w - 0.15, row_h, lab, size=size, color=self.t["primary"] if isf else self.t["text"],
                      bold=isf, align="r", anchor="m", name="hbar_label")
            bw = max(0.05, bar_w * v / vmax)
            self.rect(s, x + label_w, yy + 0.04, bw, row_h - 0.08, fill=self.t["primary"] if isf else self.t["gray"])
            self.text(s, x + label_w + bw + 0.1, yy, 0.9, row_h, fmt.format(v=v), size=size, bold=isf,
                      color=self.t["ink"], anchor="m", name="hbar_val")
        if focus and box_focus:
            f0, f1 = min(focus), max(focus)
            self.rect(s, x - 0.08, y + f0 * (row_h + gap) - 0.07, w + 0.1,
                      (f1 - f0 + 1) * (row_h + gap) - gap + 0.14, line=self.t["primary"], dash=True, line_w=1.25)
        return y + len(rows) * (row_h + gap)

    def chevrons(self, s, x, y, w, h, steps, dashed=(), ramp=True, size=13, gap=0.04, accent_last=False):
        """프로세스 셰브론. ramp=True면 연한→진한 색 그라데이션 단계. dashed 단계는 점선 외곽(문제 구간)."""
        n = len(steps)
        cw = (w + gap * (n - 1) * 0) / n
        ramp_cols = self._ramp(n)
        for i, st in enumerate(steps):
            cx = x + i * (cw - 0.08 + gap)
            is_d = i in dashed
            shp = self.rect(s, cx, y, cw, h, fill=None if is_d else ramp_cols[i],
                            line=self.t["primary"] if is_d else None, dash=is_d, line_w=1.5,
                            shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON)
            if shp.adjustments:
                shp.adjustments[0] = 0.28
            light = i < n * 0.5 and not is_d
            self.shape_text(shp, st, size=size, bold=True,
                            color=self.t["ink"] if (light or is_d) else self.t["white"], margin=0.3)
        return y + h

    def _ramp(self, n):
        a = rgb(self.t["tint"])
        b = rgb(self.t["primary"])
        out = []
        for i in range(n):
            f = i / max(1, n - 1)
            out.append("%02X%02X%02X" % tuple(int(a[k] + (b[k] - a[k]) * f) for k in range(3)))
        return out

    def num_circle(self, s, cx, cy, n, d=0.5, fill=None, color=None, size=14, line=None):
        c = self.rect(s, cx - d / 2, cy - d / 2, d, d, fill=fill or self.t["white"], line=line or self.t["tint"],
                      line_w=1.5, shape=MSO_SHAPE.OVAL, shadow=True)
        self.shape_text(c, str(n), size=size, color=color or self.t["text"], margin=0)

    def table(self, s, x, y, col_w, rows, row_h=0.62, header=True, size=13.5, focus_col=None, align=None,
              head_fill=None, zebra=True, first_col_bold=False, fill_to=None):
        """셀 단위 사각형으로 만드는 표(렌더 안정적). rows[0]은 헤더. 셀에 **강조** 사용 가능."""
        align = align or ["c"] * len(col_w)
        cy = y
        heights = []
        for ri, row in enumerate(rows):
            lines = 1
            for ci, cell in enumerate(row):
                lines = max(lines, estimate_lines(str(cell), size, col_w[ci] - 0.2, bold=(ri == 0 and header)))
            heights.append(max(row_h, lines * size * 1.25 / 72 + 0.18))
        if fill_to is not None:  # 남는 세로 공간을 행 높이에 분배(행당 최대 +0.45in)
            extra = fill_to - y - sum(heights)
            if extra > 0:
                add = min(0.45, extra / len(heights))
                heights = [h + add for h in heights]
        for ri, row in enumerate(rows):
            cx = x
            is_h = header and ri == 0
            for ci, cell in enumerate(row):
                fill = (head_fill or self.t["deep"]) if is_h else (
                    self.t["tint2"] if (focus_col is not None and ci == focus_col) else (
                        self.t["white"] if (not zebra or ri % 2 == 1) else self.t["gray2"]))
                r = self.rect(s, cx, cy, col_w[ci], heights[ri], fill=fill, line=self.t["gray"], line_w=0.5)
                self.shape_text(r, str(cell), size=size, bold=is_h or (first_col_bold and ci == 0),
                                color=self.t["white"] if is_h else self.t["text"],
                                align=align[ci], margin=0.1, em_color=self.t["primary"])
                cx += col_w[ci]
            cy += heights[ri]
        return cy

    # ========================================================================
    # 슬라이드 유형 (archetypes)
    # ========================================================================
    def cover(self, title, subtitle="", team="", mode="gradient"):
        s = self.slide("deep", number=False)
        # 좌측 텍스트 / 우측 이미지 자리
        self.rect(s, 0, 0, SLIDE_W, SLIDE_H, fill=self.t["deep"])
        self.rect(s, SLIDE_W * 0.58, 0, SLIDE_W * 0.42, SLIDE_H, fill=self.t["primary"])
        self.image(s, SLIDE_W * 0.62, 0.6, SLIDE_W * 0.34, SLIDE_H - 1.2, "표지 키비주얼 (모바일 목업 / 대표 이미지)",
                   fill=self.t["tint"])
        if self.brand:
            self.text(s, 0.8, 2.0, 5, 0.4, self.brand, size=14, bold=True, color=self.t["hilite"])
        h = estimate_lines(title, 32, 6.9, bold=True, tracking=-0.6) * 32 * 1.3 / 72
        self.text(s, 0.8, 2.5, 6.9, h + 0.1, title, size=32, bold=True, color=self.t["white"], line_spacing=1.3,
                  tracking=-0.6, name="cover_title")
        if subtitle:
            self.text(s, 0.8, 2.5 + h + 0.25, 6.9, 0.6, subtitle, size=15, color=self.t["hilite"], line_spacing=1.3, name="cover_sub")
        if team or self.team:
            self.text(s, 0.8, SLIDE_H - 1.2, 6.9, 0.4, team or self.team, size=13, color=self.t["white"], name="cover_team")
        return s

    def index(self, groups: list[tuple[str, list[str]]], title="INDEX"):
        s = self.slide("light")
        self.text(s, 0, 1.45, SLIDE_W, 0.5, f"|  {title}  |", size=24, bold=True, color=self.t["primary"], align="c")
        n = len(groups)
        cw = min(2.55, (SLIDE_W - 2 * MARGIN_X - (n - 1) * 0.25) / n)
        gap = (SLIDE_W - 2 * MARGIN_X - n * cw) / max(1, n - 1) if n > 1 else 0
        for i, (head, items) in enumerate(groups):
            x = MARGIN_X + i * (cw + gap)
            self.text(s, x, 2.25, cw, 0.35, f"{i+1:02d}", size=18, color=self.t["primary"], align="c")
            hb = self.rect(s, x, 2.65, cw, 0.6, fill=self.t["primary"])
            self.shape_text(hb, head, size=17, bold=True, color=self.t["white"])
            for j, it in enumerate(items):
                ib = self.rect(s, x, 3.45 + j * 0.7, cw, 0.52, fill=self.t["gray"])
                self.shape_text(ib, it, size=13.5, color=self.t["text"])
        return s

    def exec_summary(self, rows: list[tuple[str, str]], imc: tuple[str, list[tuple[str, str]]] | None = None,
                     tag="Executive Summary"):
        """좌 라벨 열 + 우 한 문장. 마지막 줄에 IMC(콘셉트 + 프로그램 타일). (참조: 아르르 p2)"""
        s = self.slide("light", section=tag)
        y = 0.95
        lab_w, gap = 1.75, 0.12
        body_w = SLIDE_W - 2 * MARGIN_X - lab_w - gap
        n = len(rows)
        avail = SLIDE_H - 0.9 - y - (1.45 if imc else 0.1)
        rh = min(0.78, (avail - (n - 1) * 0.12) / n)
        for i, (lab, body) in enumerate(rows):
            yy = y + i * (rh + 0.12)
            self.label(s, MARGIN_X, yy, lab_w, rh, lab, fill=self.t["mid"], size=15)
            b = self.rect(s, MARGIN_X + lab_w + gap, yy, body_w, rh, fill=self.t["white"], shadow=True)
            self.shape_text(b, body, size=16, color=self.t["ink"], tracking=-0.3)
        if imc:
            concept, progs = imc
            yy = y + n * (rh + 0.12)
            ih = 1.3
            self.label(s, MARGIN_X, yy, lab_w, ih, "IMC", fill=self.t["deep"], size=15)
            cb = self.rect(s, MARGIN_X + lab_w + gap, yy, 2.9, ih, fill=self.t["white"], shadow=True)
            self.shape_text(cb, concept, size=21, bold=True, color=self.t["ink"], tracking=-0.5)
            px = MARGIN_X + lab_w + gap + 3.0
            pw = (SLIDE_W - MARGIN_X - px - 0.12) / 2
            for k, (nm, ds) in enumerate(progs[:4]):
                r_, c_ = divmod(k, 2)
                bx = px + c_ * (pw + 0.12)
                by = yy + r_ * (ih / 2 + 0.0)
                tb = self.rect(s, bx, by, pw, ih / 2 - 0.1, fill=self.t["white"], shadow=True)
                self.shape_text(tb, f"{nm}\n{ds}", size=13, color=self.t["text"], tracking=-0.2, line_spacing=1.1,
                                em_color=self.t["ink"])
        return s

    def approach(self, pill, statement, steps: list[str], tag="Approach"):
        """질문 한 줄 → 점선 트리 → 3개 번호 원 + 설명. (참조: 아르르 p3, 에너지플러스 p3)"""
        s = self.slide("light", section=tag)
        self.pill(s, SLIDE_W / 2 - 1.6, 1.3, 3.2, pill, h=0.46, fill=self.t["primary"], size=15)
        self.text(s, 1.2, 2.0, SLIDE_W - 2.4, 1.2, f"“  {statement}  ”", size=26, bold=True, color=self.t["ink"], align="c",
                  line_spacing=1.3, tracking=-0.5, name="approach_stmt")
        self.dot(s, SLIDE_W / 2, 3.5, 0.12)
        n = len(steps)
        xs = [SLIDE_W * (i + 0.5) / n for i in range(n)]
        ty = 4.15
        self.line(s, SLIDE_W / 2, 3.5, SLIDE_W / 2, ty, dash=True, w=1)
        self.line(s, xs[0], ty, xs[-1], ty, dash=True, w=1)
        for i, x in enumerate(xs):
            self.line(s, x, ty, x, ty + 0.55, dash=True, w=1)
            self.num_circle(s, x, ty + 0.85, i + 1, d=0.62, size=15)
            self.text(s, x - 2.1, ty + 1.45, 4.2, 1.1, steps[i], size=17, color=self.t["text"], align="c", line_spacing=1.35,
                      name="approach_step")
        return s

    def two_panel(self, section, title, left_pill, right_pill, left_w=6.0, sub=None, dark=False):
        """좌/우 필 헤더가 달린 2단 기본 골격. 반환: (slide, (lx,ly,lw), (rx,ry,rw)) 본문 시작 좌표."""
        s = self.slide("dark" if dark else "light", section=section)
        ty = self.title(s, title)
        y = ty + 0.35
        total = SLIDE_W - 2 * MARGIN_X
        gap = 0.4
        lw = left_w
        rw = total - lw - gap
        self.pill(s, MARGIN_X, y, lw, left_pill)
        self.pill(s, MARGIN_X + lw + gap, y, rw, right_pill)
        return s, (MARGIN_X, y + 0.65, lw), (MARGIN_X + lw + gap, y + 0.65, rw)

    def pain_solution(self, section, title, rows: list[tuple[str, str]], left_head="Pain-Point", right_head="Solution"):
        """흰 둥근 박스(문제) → 주색 화살표 블록(해결). (참조: 에너지플러스 p16)"""
        s = self.slide("light", section=section)
        ty = self.title(s, title)
        y0 = ty + 0.45
        self.text(s, 1.2, y0, 4.2, 0.4, left_head, size=16, bold=True, color=self.t["ink"], align="c")
        self.text(s, 6.4, y0, 5.8, 0.4, right_head, size=16, bold=True, color=self.t["primary"], align="c")
        n = len(rows)
        rh = min(1.15, (SLIDE_H - 0.8 - (y0 + 0.55) - (n - 1) * 0.3) / n)
        for i, (pain, sol) in enumerate(rows):
            yy = y0 + 0.55 + i * (rh + 0.3)
            l = self.rect(s, 1.2, yy, 5.4, rh, fill=self.t["white"], radius=0.25, shadow=True)
            self.shape_text(l, pain, size=17, bold=True, color=self.t["ink"])
            arr = self.rect(s, 5.95, yy, 6.2, rh, fill=self.t["primary"], radius=0.25)
            tri = self.rect(s, 5.8, yy + rh / 2 - 0.3, 0.45, 0.6, fill=self.t["white"], shape=MSO_SHAPE.ISOSCELES_TRIANGLE)
            tri.rotation = 90
            self.shape_text(arr, sol, size=17, bold=True, color=self.t["white"], margin=0.5)
        return s

    def quotes_with_stat(self, section, title, stat_big, stat_label, stat_sub, quotes: list[tuple[str, str]],
                         source="", callout=None, left_pill="핵심 수치", right_pill="고객의 목소리"):
        """왼쪽 큰 수치(원) + 오른쪽 인터뷰 말풍선 2~3개. (참조: 에너지플러스 p8/p9)"""
        s, (lx, ly, lw), (rx, ry, rw) = self.two_panel(section, title, left_pill, right_pill, left_w=4.4)
        self.kpi_circle(s, lx + lw / 2, ly + 1.55, 2.8, stat_big, label=stat_label, sub=stat_sub)
        if source:
            self.source(s, source, x=lx, y=ly + 3.15, w=lw, align="c")
        n = len(quotes)
        floor = (SLIDE_H - 1.25) if callout else (SLIDE_H - 0.7)
        bh = min(1.45, (floor - ry) / n - 0.1)
        for i, (q, who) in enumerate(quotes):
            self.bubble(s, rx, ry + i * (bh + 0.1), rw, bh, q, who, side="l" if i % 2 == 0 else "r")
        if callout:
            self.callout(s, callout, y=SLIDE_H - 1.1)
        return s

    def bars_and_notes(self, section, title, bars, bar_title, right_title, notes: list[str], focus=(0,),
                       source="", callout=None, fmt="{v:g}%"):
        """왼쪽 가로 막대(핵심만 진하게 + 점선 박스) / 오른쪽 해석 불릿."""
        s, (lx, ly, lw), (rx, ry, rw) = self.two_panel(section, title, bar_title, right_title, left_w=6.4)
        bottom = self.hbar(s, lx, ly + 0.1, lw, bars, focus=focus, fmt=fmt)
        if source:
            self.source(s, source, x=lx, y=bottom + 0.05, w=lw, align="l")
        yy = ry + 0.1
        for n in notes:
            h = estimate_lines(n, 16, rw - 0.4, tracking=-0.2) * 16 * 1.4 / 72 + 0.28
            self.dot(s, rx + 0.1, yy + 0.14, 0.1)
            self.text(s, rx + 0.3, yy, rw - 0.3, h, n, size=16, color=self.t["text"], line_spacing=1.4, name="note")
            yy += h + 0.12
        if callout:
            self.callout(s, callout, y=SLIDE_H - 1.1)
        return s

    def flow_with_dropoff(self, section, title, steps, dashed=(), drops=(), pill="구간별 이탈", source="", callout=None):
        """프로세스 셰브론 + 이탈 구간(점선) + 구간별 이탈 수치(빨강). (참조: 에너지플러스 p7)"""
        s = self.slide("light", section=section)
        ty = self.title(s, title)
        self.pill(s, SLIDE_W / 2 - 2.5, ty + 0.35, 5.0, pill, fill=self.t["primary"])
        if source:
            self.source(s, source, y=ty + 0.9, align="c")
        self.chevrons(s, MARGIN_X, 3.1, SLIDE_W - 2 * MARGIN_X, 1.1, steps, dashed=dashed)
        n = len(steps)
        cw = (SLIDE_W - 2 * MARGIN_X) / n
        for (idx, val, lab) in drops:
            cx = MARGIN_X + idx * (cw - 0.08 + 0.04) + cw / 2
            self.text(s, cx - 1.2, 4.35, 2.4, 0.7, val, size=32, bold=True, color=self.t["alert"], align="c", tracking=-0.8)
            self.text(s, cx - 1.5, 5.1, 3.0, 0.5, lab, size=12.5, color=self.t["text"], align="c", line_spacing=1.25)
        if callout:
            self.callout(s, callout, y=SLIDE_H - 1.1)
        return s

    def compare_table(self, section, title, rows, col_w, focus_col=None, source="", callout=None, pill=None, size=13.5,
                      align=None, row_h=0.62):
        s = self.slide("light", section=section)
        ty = self.title(s, title)
        y = ty + 0.35
        if pill:
            self.pill(s, MARGIN_X, y, SLIDE_W - 2 * MARGIN_X, pill)
            y += 0.65
        if source:
            self.source(s, source, y=y, align="r")
            y += 0.28
        self.table(s, MARGIN_X, y, col_w, rows, focus_col=focus_col, size=size, align=align, row_h=row_h,
                   fill_to=(SLIDE_H - 1.3) if callout else (SLIDE_H - 0.8))
        if callout:
            self.callout(s, callout, y=SLIDE_H - 1.1)
        return s

    def two_paths(self, section, title, top_label, top_steps, bottom_label, bottom_steps, note="", source=""):
        """기존(단품 중심) vs 제안(공간 변화 중심) 두 줄 프로세스. (참조: 에너지플러스 As-Is/To-Be, 아르르 p17)"""
        s = self.slide("light", section=section)
        ty = self.title(s, title)
        y = ty + 0.5
        total = SLIDE_W - 2 * MARGIN_X
        self.text(s, MARGIN_X, y, 6, 0.4, top_label, size=16, bold=True, color=self.t["ink"])
        n1 = len(top_steps)
        for i, st in enumerate(top_steps):
            w = (total - (n1 - 1) * 0.3) / n1
            bx = MARGIN_X + i * (w + 0.3)
            b = self.rect(s, bx, y + 0.55, w, 0.95, fill=self.t["gray"], radius=0.2)
            self.shape_text(b, st, size=16, bold=True, color=self.t["text"])
            if i < n1 - 1:
                self.text(s, bx + w, y + 0.8, 0.3, 0.5, "›", size=22, bold=True, color=self.t["mute"], align="c")
        y2 = y + 2.0
        self.text(s, MARGIN_X, y2, 8, 0.4, bottom_label, size=16, bold=True, color=self.t["primary"])
        n2 = len(bottom_steps)
        for i, st in enumerate(bottom_steps):
            w = (total - (n2 - 1) * 0.3) / n2
            bx = MARGIN_X + i * (w + 0.3)
            last = i == n2 - 1
            b = self.rect(s, bx, y2 + 0.55, w, 1.15, fill=self.t["primary"] if last else self.t["tint"], radius=0.2)
            self.shape_text(b, st, size=16, bold=True, color=self.t["white"] if last else self.t["ink"])
            if i < n2 - 1:
                self.text(s, bx + w, y2 + 0.9, 0.3, 0.5, "›", size=22, bold=True, color=self.t["primary"], align="c")
        if note:
            self.callout(s, note, y=SLIDE_H - 1.1)
        if source:
            self.source(s, source, y=SLIDE_H - 1.55)
        return s

    def dark_barriers(self, section, title, start, end, barriers: list[tuple[str, str]], pill="이탈 위험 요인"):
        """다크 배경 + 라인 위의 3개 장벽. (참조: 에너지플러스 p11/p18)"""
        s = self.slide("dark", section=section)
        ty = self.title(s, title)
        self.pill(s, SLIDE_W / 2 - 2.2, ty + 0.4, 4.4, pill, fill=self.t["primary"])
        ly = 4.3
        self.rect(s, 0, ly - 0.03, SLIDE_W, 0.06, fill=self.t["mid"])
        self.dot(s, 1.7, ly, 0.28, fill=self.t["hilite"])
        self.dot(s, SLIDE_W - 1.7, ly, 0.28, fill=self.t["primary"])
        self.text(s, 0.9, ly - 0.6, 1.6, 0.3, start, size=13, color=self.t["white"], align="c")
        self.text(s, SLIDE_W - 2.5, ly - 0.6, 1.6, 0.3, end, size=13, color=self.t["white"], align="c")
        n = len(barriers)
        xs = [3.6 + i * (SLIDE_W - 7.2) / max(1, n - 1) for i in range(n)]
        for i, (lab, sub) in enumerate(barriers):
            w = 0.8
            b = self.rect(s, xs[i] - w / 2, ly - 1.05, w, 2.1, fill=self.t["mid"], line=self.t["hilite"], line_w=1.0,
                          radius=0.08)
            self.text(s, xs[i] - w / 2, ly - 0.3, w, 0.6, "»", size=30, bold=True, color=self.t["hilite"], align="c")
            self.line(s, xs[i], ly + 1.05, xs[i], ly + 1.45, color=self.t["mid"], dash=True)
            self.text(s, xs[i] - 1.7, ly + 1.55, 3.4, 0.5, f"{i+1}. {lab}", size=17, bold=True, color=self.t["white"], align="c")
            if sub:
                self.text(s, xs[i] - 1.7, ly + 2.05, 3.4, 0.6, sub, size=12, color=self.t["hilite"], align="c", line_spacing=1.3)
        return s

    def big_idea(self, name, tagline, chips: list[str], note=""):
        """빅 아이디어 공개. 배경 이미지 자리 + 거대 타이틀 + 프로그램 칩 4개. (참조: 아르르 'Arrr-in-One')"""
        s = self.slide("dark", number=False)
        self.image(s, 0, 0, SLIDE_W, SLIDE_H, "배경 키비주얼 (공간 사진 / 일러스트) — 위에 어두운 오버레이", fill="3A4247")
        ov = self.rect(s, 0, 0, SLIDE_W, SLIDE_H, fill="000000")
        # 투명도는 XML로 설정
        sf = ov._element.spPr.find(qn("a:solidFill"))
        clr = sf.find(qn("a:srgbClr"))
        etree.SubElement(clr, qn("a:alpha"), val="45000")
        self.text(s, 0.6, 2.2, SLIDE_W - 1.2, 1.7, name, size=66, bold=True, color=self.t["white"], align="c",
                  tracking=-2, name="bigidea", line_spacing=1.1)
        self.text(s, 0.6, 4.05, SLIDE_W - 1.2, 0.5, tagline, size=18, color=self.t["white"], align="c")
        n = len(chips)
        cw = 2.5
        gap = 0.25
        x0 = (SLIDE_W - (n * cw + (n - 1) * gap)) / 2
        for i, c in enumerate(chips):
            b = self.rect(s, x0 + i * (cw + gap), 5.0, cw, 0.55, fill=self.t["white"], radius=0.27)
            self.shape_text(b, c, size=14, bold=True, color=self.t["ink"])
        if note:
            self.text(s, 0.6, 6.4, SLIDE_W - 1.2, 0.4, note, size=11, color=self.t["hilite"], align="c")
        return s

    def imc_matrix(self, groups: list[dict], journey=("인지", "고려", "구매"), tag="IMC 개요", title=None):
        """프로그램 × (채널/타깃특성/목적) + 고객여정 점. groups=[{name, items:[{name, channel, target, goal, stages:[0,1]}]}]
        (참조: 아르르 p19)"""
        s = self.slide("light", section=tag)
        y0 = (self.title(s, title) + 0.35) if title else 1.0
        gw, iw = 1.25, 1.75
        cw = [1.95, 2.0, 1.8]
        jw = 0.78 if len(journey) <= 3 else 0.62
        x0 = MARGIN_X
        xc = x0 + gw + iw + 0.1
        # 헤더
        h1 = self.pill(s, xc, y0, sum(cw) + 0.1, "IMC 전략 개요", h=0.46, fill=self.t["deep"])
        xj = xc + sum(cw) + 0.35
        self.pill(s, xj, y0, jw * len(journey) + 0.1, "고객여정지도", h=0.46, fill=self.t["deep"])
        for i, hd in enumerate(["채널", "타깃 특성", "목적"]):
            self.label(s, xc + sum(cw[:i]) + 0.05 * i, y0 + 0.55, cw[i], 0.36, hd, fill=self.t["mid"], size=12)
        for j, jn in enumerate(journey):
            self.label(s, xj + j * jw + 0.05 * j, y0 + 0.55, jw, 0.36, jn, fill=self.t["primary"], size=12)
        total_items = sum(len(g["items"]) for g in groups)
        rh = min(1.2, (SLIDE_H - 0.8 - (y0 + 1.05)) / total_items - 0.07)
        yy = y0 + 1.05
        for g in groups:
            gh = len(g["items"]) * (rh + 0.07) - 0.07
            self.label(s, x0, yy, gw, gh, g["name"], fill=self.t["deep"], size=14)
            for it in g["items"]:
                self.label(s, x0 + gw + 0.05, yy, iw, rh, it["name"], fill=self.t["white"], color=self.t["ink"], size=13)
                for i, k in enumerate(["channel", "target", "goal"]):
                    b = self.rect(s, xc + sum(cw[:i]) + 0.05 * i, yy, cw[i], rh, fill=self.t["white"], line=self.t["gray"], line_w=0.5)
                    self.shape_text(b, it[k], size=12.5, color=self.t["text"], line_spacing=1.1)
                if it.get("stages"):
                    st = it["stages"]
                    self.line(s, xj + min(st) * (jw + 0.05) + jw / 2, yy + rh / 2, xj + max(st) * (jw + 0.05) + jw / 2,
                              yy + rh / 2, color=self.t["primary"], w=1.5)
                    for k in st:
                        self.dot(s, xj + k * (jw + 0.05) + jw / 2, yy + rh / 2, 0.16)
                yy += rh + 0.07
        return s

    def program(self, kicker, name, subtitle, slogan, blocks: list[tuple[str, list[str]]], visual_label="시안 이미지 / 목업",
                effect=None, dark=True):
        """IMC 프로그램 상세. 좌: 프로그램명+슬로건+블록(세로선 소제목), 우: 시안 자리. (참조: 아르르 Marrrket 시리즈)"""
        s = self.slide("dark" if dark else "light")
        c_main = self.t["white"] if dark else self.t["ink"]
        c_sub = self.t["hilite"] if dark else self.t["primary"]
        self.text(s, 0.6, 0.45, 6, 0.3, kicker, size=11, color=c_sub, name="kicker")
        self.text(s, 0.6, 0.75, 7.5, 0.9, name, size=44, bold=True, color=c_main, tracking=-1.5, name="prog_name")
        if subtitle:
            self.text(s, 0.6, 1.62, 7.5, 0.45, subtitle, size=17, color=c_main, name="prog_sub")
        sl = self.rect(s, 0.6, 2.2, min(7.2, text_width_pt(slogan, 15, False) / 72 + 1.1), 0.46,
                       fill=self.t["mute"] if dark else self.t["gray"], radius=0.23)
        self.shape_text(sl, f"“ {slogan} ”", size=15, color=c_main)
        y = 2.95
        for head, lines in blocks:
            self.rect(s, 0.6, y + 0.04, 0.05, 0.3, fill=c_sub)
            self.text(s, 0.8, y, 6, 0.38, head, size=18, bold=True, color=c_main, name="blk_head")
            y += 0.45
            body = "\n".join(f"•  {l}" for l in lines)
            h = estimate_lines(body, 14, 6.3, tracking=-0.2) * 14 * 1.4 / 72 + 0.1
            self.text(s, 0.85, y, 6.3, h, body, size=14, color=c_main if dark else self.t["text"], line_spacing=1.4,
                      name="blk_body")
            y += h + 0.2
        self.image(s, 8.0, 0.75, 4.75, SLIDE_H - 1.7 if not effect else SLIDE_H - 3.1, visual_label,
                   fill="353B40" if dark else self.t["gray2"])
        if effect:
            eb = self.rect(s, 8.0, SLIDE_H - 2.2, 4.75, 1.4, fill="353B40" if dark else self.t["tint2"], radius=0.15)
            self.shape_text(eb, f"[기대효과]\n{effect}", size=13, color=c_main, align="l", margin=0.2, line_spacing=1.3,
                            anchor="m")
        return s

    def hub(self, section, title, center, nodes: list[tuple[str, str]], goal):
        """콘셉트 중심 + 채널 노드 원형 배치 → 하단 '구매' 목표. (IMC 통합)"""
        import math

        s = self.slide("light", section=section)
        ty = self.title(s, title)
        cx, cy = SLIDE_W / 2, 4.15
        R, ry_ = 3.5, 1.5
        n = len(nodes)
        for i, (nm, ds) in enumerate(nodes):
            ang = -math.pi / 2 + 2 * math.pi * i / n
            nx, ny = cx + R * math.cos(ang), cy + ry_ * math.sin(ang)
            self.line(s, cx, cy, nx, ny, color=self.t["mid"], dash=True, w=1)
        self.kpi_circle(s, cx, cy, 2.1, center, big_size=15)
        for i, (nm, ds) in enumerate(nodes):
            ang = -math.pi / 2 + 2 * math.pi * i / n
            nx, ny = cx + R * math.cos(ang), cy + ry_ * math.sin(ang)
            b = self.rect(s, nx - 1.25, ny - 0.5, 2.5, 1.0, fill=self.t["white"], line=self.t["primary"], radius=0.18, shadow=True)
            self.shape_text(b, f"**{nm}**\n{ds}", size=12.5, color=self.t["text"], line_spacing=1.15)
        g = self.rect(s, SLIDE_W / 2 - 3.8, SLIDE_H - 0.95, 7.6, 0.55, fill=self.t["deep"], radius=0.27)
        self.shape_text(g, goal, size=14, bold=True, color=self.t["white"])
        return s

    def journey_table(self, section, title, stages: list[str], rows: list[tuple[str, list[str]]], source=""):
        """단계 셰브론 + 행(고객의 말 / 접점 / 핵심 행동 / 측정). (참조: 에너지플러스 고객여정 p20)"""
        s = self.slide("light", section=section)
        ty = self.title(s, title)
        lab_w = 1.5
        x0 = MARGIN_X
        y0 = ty + 0.35
        n = len(stages)
        cw = (SLIDE_W - 2 * MARGIN_X - lab_w - 0.1) / n
        self.label(s, x0, y0, lab_w, 0.7, "단계", fill=self.t["gray"], color=self.t["ink"], size=13)
        ramp = self._ramp(n)
        for i, st in enumerate(stages):
            shp = self.rect(s, x0 + lab_w + 0.1 + i * cw, y0, cw + 0.05, 0.7, fill=ramp[i],
                            shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON)
            shp.adjustments[0] = 0.25
            self.shape_text(shp, st, size=15, bold=True, color=self.t["ink"] if i < n / 2 else self.t["white"], margin=0.25)
        yy = y0 + 0.85
        avail = SLIDE_H - 0.9 - yy
        rh = avail / len(rows) - 0.08
        for lab, cells in rows:
            self.label(s, x0, yy, lab_w, rh, lab, fill=self.t["gray"], color=self.t["ink"], size=14)
            for i, c in enumerate(cells):
                b = self.rect(s, x0 + lab_w + 0.1 + i * cw, yy, cw - 0.05, rh, fill=self.t["white"], line=self.t["gray"], line_w=0.5)
                self.shape_text(b, c, size=13, color=self.t["text"], line_spacing=1.2)
            yy += rh + 0.08
        if source:
            self.source(s, source)
        return s

    def roadmap(self, section, title, phases: list[tuple[str, str, list[str], str]]):
        """기간 헤더 + 실행 + 통과 기준. phases=[(기간, 이름, [실행...], 통과기준)]"""
        s = self.slide("light", section=section)
        ty = self.title(s, title)
        n = len(phases)
        gap = 0.2
        w = (SLIDE_W - 2 * MARGIN_X - gap * (n - 1)) / n
        y = ty + 0.4
        ramp = self._ramp(n)
        for i, (per, nm, acts, gate) in enumerate(phases):
            x = MARGIN_X + i * (w + gap)
            h = self.rect(s, x, y, w, 0.9, fill=ramp[i], shape=MSO_SHAPE.PENTAGON)
            h.adjustments[0] = 0.18
            self.text(s, x + 0.15, y + 0.1, w - 0.5, 0.3, per, size=12, color=self.t["ink"] if i < n / 2 else self.t["white"], bold=True)
            self.text(s, x + 0.15, y + 0.4, w - 0.5, 0.4, nm, size=16, bold=True, color=self.t["ink"] if i < n / 2 else self.t["white"])
            body = "\n".join(f"•  {a}" for a in acts)
            bh = 2.5
            b = self.rect(s, x, y + 1.05, w, bh, fill=self.t["white"], line=self.t["gray"], radius=0.1)
            self.shape_text(b, body, size=13.5, color=self.t["text"], align="l", anchor="t", margin=0.15, line_spacing=1.35)
            g = self.rect(s, x, y + 1.05 + bh + 0.15, w, 0.95, fill=self.t["tint2"], line=self.t["primary"], dash=True, radius=0.1)
            self.shape_text(g, f"**통과 기준**\n{gate}", size=12.5, color=self.t["text"], align="l", margin=0.15, line_spacing=1.25)
        return s

    def budget(self, section, title, items: list[tuple[str, float, str]], total_label="10억", notes: list[str] | None = None):
        """도넛 + 항목 리스트. items=[(이름, 비중%, 금액)]"""
        s = self.slide("light", section=section)
        ty = self.title(s, title)
        cd = CategoryChartData()
        cd.categories = [i[0] for i in items]
        cd.add_series("비중", [i[1] for i in items])
        gf = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(0.9), Inches(ty + 0.3), Inches(4.8), Inches(4.6), cd)
        ch = gf.chart
        ch.has_legend = False
        ch.has_title = False
        plot = ch.plots[0]
        plot.has_data_labels = False
        ramp = self._ramp(len(items))[::-1]
        for idx, pt_ in enumerate(plot.series[0].points):
            pt_.format.fill.solid()
            pt_.format.fill.fore_color.rgb = rgb(ramp[idx])
            pt_.format.line.color.rgb = rgb(self.t["bg"])
        # 도넛 구멍 크기
        dn = ch._chartSpace.xpath(".//c:holeSize")
        if dn:
            dn[0].set("val", "62")
        self.text(s, 2.3, ty + 2.3, 2.0, 0.8, total_label, size=34, bold=True, color=self.t["ink"], align="c")
        self.text(s, 2.3, ty + 3.05, 2.0, 0.3, "가상 총예산", size=11, color=self.t["mute"], align="c")
        x, y = 6.3, ty + 0.5
        for i, (nm, pct, amt) in enumerate(items):
            col = ramp[i]
            self.rect(s, x, y + i * 0.55 + 0.1, 0.22, 0.22, fill=col)
            self.text(s, x + 0.4, y + i * 0.55, 3.4, 0.42, nm, size=14, bold=(i < 3), color=self.t["ink"], anchor="m")
            self.text(s, x + 3.8, y + i * 0.55, 0.9, 0.42, f"{pct:g}%", size=14, bold=True, color=self.t["primary"], anchor="m", align="r")
            self.text(s, x + 4.8, y + i * 0.55, 1.2, 0.42, amt, size=13, color=self.t["mute"], anchor="m", align="r")
        if notes:
            yy = y + len(items) * 0.55 + 0.25
            for n_ in notes:
                self.dot(s, x + 0.1, yy + 0.12, 0.09)
                self.text(s, x + 0.3, yy, 5.7, 0.5, n_, size=12, color=self.t["text"], line_spacing=1.3)
                yy += 0.5
        return s

    def appendix(self, title, sections: list[tuple[str, list[str]]], note=""):
        """출처/한계/AI활용 등 부록(밀도 높음, 작은 글씨)."""
        s = self.slide("light", section="Appendix")
        self.text(s, MARGIN_X, 0.8, 8, 0.6, f"|  {title}", size=24, bold=True, color=self.t["ink"])
        y = 1.55
        for head, lines in sections:
            self.text(s, MARGIN_X, y, 8, 0.3, head, size=13, bold=True, color=self.t["primary"])
            y += 0.34
            body = "\n".join(lines)
            h = estimate_lines(body, 11, SLIDE_W - 2 * MARGIN_X, tracking=-0.1) * 11 * 1.35 / 72 + 0.05
            self.text(s, MARGIN_X, y, SLIDE_W - 2 * MARGIN_X, h, body, size=11, color=self.t["text"], line_spacing=1.35, name="app_body")
            y += h + 0.18
        return s

    def divider(self, part, title, question="", parts: list[str] | None = None, current=0, pages=""):
        """파트 구분 장표. 짙은 배경 + 큰 파트명 + 이 파트가 답할 질문 + 하단 진행 표시."""
        s = self.slide("deep", number=False)
        if pages:
            self.text(s, SLIDE_W - 5.6, 1.0, 5.0, 1.6, pages, size=88, bold=True, color="1A6F89", align="r",
                      tracking=-3, name="div_pages")
        self.text(s, 0.9, 2.15, 6, 0.4, f"PART {part}", size=16, bold=True, color=self.t["hilite"], name="div_part")
        self.text(s, 0.9, 2.6, 11.0, 0.9, title, size=40, bold=True, color=self.t["white"], tracking=-1.2, name="div_title")
        self.rect(s, 0.9, 3.65, 0.8, 0.06, fill=self.t["hilite"])
        if question:
            self.text(s, 0.9, 3.95, 11.0, 0.9, question, size=18, color=self.t["tint"], line_spacing=1.35, name="div_q")
        if parts:
            n = len(parts)
            gap = 0.12
            w = (SLIDE_W - 1.8 - gap * (n - 1)) / n
            for i, p_ in enumerate(parts):
                cur = i == current
                b = self.rect(s, 0.9 + i * (w + gap), SLIDE_H - 1.05, w, 0.42, fill=self.t["primary"] if cur else None,
                              line=None if cur else self.t["mid"], line_w=0.75, radius=0.21)
                self.shape_text(b, f"{chr(65 + i)}  {p_}", size=12, bold=cur, color=self.t["white"] if cur else self.t["mid"])
        return s

    def phone_flow(self, section, title, steps: list[tuple[str, str, str]], phone_w=1.75, source="", callout=None,
                   focus_last=True):
        """모바일 화면 n개를 단계별로 나열. steps=[(단계명, 화면 라벨, 아래 설명)]. 화면은 목업 자리."""
        s = self.slide("light", section=section)
        ty = self.title(s, title)
        n = len(steps)
        colw = (SLIDE_W - 2 * MARGIN_X) / n
        ph = phone_w * 2.05
        yl = ty + 0.4
        yp = yl + 0.5
        for i, (head, scr, cap) in enumerate(steps):
            cx = MARGIN_X + colw * (i + 0.5)
            hot = focus_last and i == n - 1
            hb = self.rect(s, cx - 1.2, yl, 2.4, 0.38, fill=self.t["primary"] if hot else self.t["tint"], radius=0.19)
            self.shape_text(hb, head, size=13, bold=True, color=self.t["white"] if hot else self.t["deep"])
            self.phone(s, cx - phone_w / 2, yp, phone_w, scr)
            self.text(s, cx - colw / 2 + 0.15, yp + ph + 0.12, colw - 0.3, 0.6, cap, size=12.5, color=self.t["text"],
                      align="c", line_spacing=1.25, name="pf_cap")
            if i < n - 1:
                self.text(s, cx + colw / 2 - 0.25, yp + ph / 2 - 0.35, 0.5, 0.6, "›", size=34, bold=True,
                          color=self.t["primary"], align="c", name="pf_arrow")
        if source:
            self.source(s, source, y=(SLIDE_H - 1.5) if callout else None, align="r")
        if callout:
            self.callout(s, callout, y=SLIDE_H - 1.1)
        return s

    def closing(self, title, tagline, rows: list[tuple[str, str]], end="감사합니다"):
        """마무리. 콘셉트 + 문제/전략/IMC 세 문장 요약."""
        s = self.slide("deep", number=False)
        self.text(s, 0.6, 0.9, SLIDE_W - 1.2, 0.9, title, size=44, bold=True, color=self.t["white"], align="c",
                  tracking=-1.5, name="close_title")
        self.text(s, 0.6, 1.85, SLIDE_W - 1.2, 0.4, tagline, size=16, color=self.t["hilite"], align="c", name="close_tag")
        y = 2.75
        for lab, body in rows:
            self.label(s, 1.4, y, 1.6, 0.8, lab, fill=self.t["primary"], size=15)
            b = self.rect(s, 3.1, y, SLIDE_W - 4.5, 0.8, fill="10677F")
            self.shape_text(b, body, size=15, color=self.t["white"], align="l", margin=0.3, em_color=self.t["hilite"])
            y += 0.95
        self.text(s, 0.6, SLIDE_H - 1.2, SLIDE_W - 1.2, 0.6, end, size=24, bold=True, color=self.t["white"], align="c",
                  name="close_end")
        return s

    def note(self, s, text):
        """발표자 노트(스크립트)."""
        s.notes_slide.notes_text_frame.text = text
        return s

    # ---- 저장 / 검수 --------------------------------------------------------
    def lint(self) -> list[str]:
        """텍스트 상자 넘침(추정) 검사. 반환: 경고 문자열 목록."""
        warns = []
        for b in self._boxes:
            if b.w <= 0.1 or b.h <= 0.1:
                continue
            lines = estimate_lines(b.text, b.size, b.w, bold=b.bold, tracking=b.tracking)
            need = lines * b.size * b.line_spacing * 1.17 / 72
            if need > b.h * 1.08 + 0.04:
                warns.append(f"p{b.slide_idx}: '{b.text[:24]}…' {lines}줄 필요 {need:.2f}in > 박스 {b.h:.2f}in")
        return warns

    def save(self, path: str):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self.prs.save(path)
        return path
