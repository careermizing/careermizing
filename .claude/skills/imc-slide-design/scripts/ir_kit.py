"""
ir_kit.py — IR 덱 컴포넌트 라이브러리(chief-staff/careermizing-ir-deck의 cm_deck.py)를 틸 팔레트로 재색한 버전.
블루 계열을 오늘의집 틸(138CB0 / 0B5A73 계열)로 1:1 매핑했다. 두위드 에셋·카피라이트는 제외.

원본 IR 덱(PowerPoint, 960x540pt, Pretendard)에서 실측한 좌표·색·폰트를 코드로 옮겼다.
좌표 단위는 모두 pt다. 캔버스는 960 x 540pt(13.333 x 7.5in, 16:9)다.

사용법
    import sys; sys.path.insert(0, "<skill>/scripts")
    from cm_deck import Deck, C
    d = Deck()
    s = d.content_slide("Performance", "결론형 헤드라인.", "근거 한 문장입니다.")
    d.pill(s, 121, 162, 120, "현 상황")
    d.card(s, 38, 215, 285, 268)
    d.illo(s, "scatter", 180, 330, 150)
    d.save("out.pptx")
    for w in d.warnings: print(w)     # 넘침/폭 초과 경고 → 반드시 확인

인라인 마크업 (모든 text 계열 함수 공통)
    **굵게**        → Bold
    {{강조}}        → 포인트 블루(#2F52F0) + Bold
    [[연한강조]]    → 라벨 블루(#5E7DFF)
    줄바꿈은 "\n"
"""
from __future__ import annotations

import glob
import math
import os
import re
import tempfile
from dataclasses import dataclass

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt

# ═════════════════════════════════════════════════════════════
# 1. 디자인 토큰 (원본 덱 실측값)
# ═════════════════════════════════════════════════════════════
W, H = 960, 540
MARGIN_X = 38                     # 좌측 기준선 (라벨·헤드라인·서브 모두 x=38)
CONTENT_W = W - MARGIN_X * 2      # 884
RIGHT = W - MARGIN_X              # 922
CONTENT_TOP = 162                 # pill 행
CARD_TOP = 215                    # pill 아래 카드 시작
CARD_BOTTOM = 483                 # 카드 하단

FONT = "Pretendard"
FONT_W = {  # PowerPoint는 weight를 패밀리명으로 구분한다
    "regular": "Pretendard",
    "medium": "Pretendard Medium",
    "semibold": "Pretendard SemiBold",
    "bold": "Pretendard",          # + Bold 플래그
}


def rgb(hexstr: str) -> RGBColor:
    return RGBColor.from_string(hexstr.lstrip("#").upper())


C = {
    # 블루 (pill 그라데이션 실측: #0A38E2 → #5072FA)
    "blue_deep": "0E7FA5",
    "blue_end": "34ACD4",
    "blue": "0F86AB",          # 본문 강조 텍스트
    "blue_label": "1E9BC4",    # 섹션 라벨, KPI 라벨, 하이라이트 타일
    "blue_soft": "A9DAEA",     # 이전 기간 막대, 보조
    "blue_pale": "D6EEF5",     # 표 헤더
    "blue_mist": "E3F4F9",     # 강조 박스 배경
    "navy": "0B5A73",          # 이번 기간 막대, 숫자 강조
    "navy_text": "0B5A73",
    "navy_cover": "0B5A73",
    "navy_dark": "0C1C22",
    "navy_card": "13252B",
    "cyan": "4FD6CF",          # 일러스트 보조 (원본 아이소메트릭의 청록)
    # 그레이 (배경 실측: 상단 #EFF0F1 → 하단 #E9ECEE, 카드 #F4F5F6)
    "black": "000000",
    "ink": "0C0C0C",
    "text": "404040",
    "text2": "585858",
    "muted": "7E7E7E",
    "line": "D3D6DB",
    "grey_card": "C3C4C4",
    "grey_mid": "E2E4E8",      # 가운데 회색 카드(BM)
    "bg_top": "F0F1F2",
    "bg_bottom": "E8EBED",
    "card_top": "F7F8F9",
    "card_bottom": "F1F2F4",
    "red_x": "D11F1F",
}

T = {  # (pt, weight)
    "label": (10, "bold"), "headline": (24, "bold"), "sub": (18, "medium"),
    "card_title": (18, "semibold"), "card_kicker": (14, "medium"),
    "body": (16, "regular"), "body_s": (14, "regular"),
    "pill": (14, "bold"), "pill_s": (12, "bold"),
    "kpi_value": (24, "bold"), "kpi_label": (14, "bold"),
    "footnote": (11, "regular"), "footer": (8, "regular"), "page_no": (10, "semibold"),
    "cover_title": (32, "medium"), "cover_sub": (20, "regular"), "closing": (27.7, "medium"),
}

COPYRIGHT = ""

# 원본 덱(2609_두위드_IR.pptx)에서 추출한 에셋 — scripts/extract_assets.py 로 생성
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(SKILL_DIR, "ir_assets")  # 브랜드 에셋 없음 → 절차적 배경·벡터 일러스트
_MANIFEST = None


def manifest() -> dict:
    global _MANIFEST
    if _MANIFEST is None:
        mp = os.path.join(ASSET_DIR, "manifest.json")
        if os.path.exists(mp):
            import json
            with open(mp, encoding="utf8") as f:
                _MANIFEST = json.load(f)
        else:
            _MANIFEST = {}
    return _MANIFEST


def asset_path(name: str):
    """'illo/puzzle_unstructured' → 절대 경로. 없으면 None."""
    m = manifest().get(name)
    if not m:
        return None
    p = os.path.join(ASSET_DIR, m["file"])
    return p if os.path.exists(p) else None


# illo(kind) → 원본 에셋 이름 (없으면 벡터 대체)
ILLO_ASSET = {
    "scatter": "illo/puzzle_unstructured", "puzzle": "illo/puzzle_unstructured",
    "server": "illo/server_data", "blocked": "illo/server_data",
    "stack": "illo/layers_stack", "layers": "illo/layers_stack",
    "database": "illo/data_cylinder", "cylinder": "illo/data_cylinder",
    "funnel": "illo/funnel_cone", "review": "illo/review_stars",
    "folder": "illo/folder_search", "coins": "illo/coins_growth", "growth": "illo/coins_growth",
    "platform": "illo/platform_ai", "infra": "illo/hiring_infra",
    "doc_pile": "illo/doc_pile", "report": "illo/doc_report_scan",
    "monitor": "illo/monitor_product",
}

# ═════════════════════════════════════════════════════════════
# 2. 텍스트 폭 측정 (Pretendard 실측 → 넘침 경고)
# ═════════════════════════════════════════════════════════════
_FONT_CACHE = {}
_FONT_FILE = {"regular": "Regular", "medium": "Medium", "semibold": "SemiBold", "bold": "Bold"}


def _font_path(weight):
    pats = [os.path.expanduser(f"~/.fonts/Pretendard-{_FONT_FILE[weight]}.otf"),
            f"/usr/share/fonts/**/Pretendard-{_FONT_FILE[weight]}.otf",
            os.path.expanduser(f"~/.local/share/fonts/**/Pretendard-{_FONT_FILE[weight]}.otf"),
            os.path.expanduser(f"~/Library/Fonts/Pretendard-{_FONT_FILE[weight]}.otf")]
    for p in pats:
        hit = glob.glob(p, recursive=True)
        if hit:
            return hit[0]
    return None


def text_width(text: str, size: float, weight: str = "regular") -> float:
    """한 줄 텍스트의 폭(pt). 마크업 기호는 제거하고 잰다. 폰트가 없으면 근사치."""
    plain = re.sub(r"\*\*|\{\{|\}\}|\[\[|\]\]", "", text)
    key = weight
    if key not in _FONT_CACHE:
        p = _font_path(weight)
        if p:
            from PIL import ImageFont
            _FONT_CACHE[key] = ImageFont.truetype(p, 1000)
        else:
            _FONT_CACHE[key] = None
    f = _FONT_CACHE[key]
    if f is not None:
        return f.getlength(plain) * size / 1000
    w = 0.0
    for ch in plain:  # 근사: 한글 0.92em, 숫자/영문 0.56em, 공백 0.26em
        w += 0.92 if ord(ch) > 0x3000 else (0.26 if ch == " " else 0.56)
    return w * size


def fit_size(text, max_w, sizes, weight="regular"):
    """sizes(큰→작은) 중 한 줄에 들어가는 가장 큰 크기. 없으면 마지막 값."""
    for s in sizes:
        if text_width(text, s, weight) <= max_w:
            return s
    return sizes[-1]


# ═════════════════════════════════════════════════════════════
# 3. 마크업 파서
# ═════════════════════════════════════════════════════════════
_TOKEN = re.compile(r"(\*\*.+?\*\*|\{\{.+?\}\}|\[\[.+?\]\])")


@dataclass
class Run:
    text: str
    bold: bool = False
    color: str | None = None


def parse(text: str) -> list[list[Run]]:
    paras = []
    for line in text.split("\n"):
        runs = []
        for part in _TOKEN.split(line):
            if not part:
                continue
            if part.startswith("**"):
                runs.append(Run(part[2:-2], bold=True))
            elif part.startswith("{{"):
                runs.append(Run(part[2:-2], bold=True, color=C["blue"]))
            elif part.startswith("[["):
                runs.append(Run(part[2:-2], color=C["blue_label"]))
            else:
                runs.append(Run(part))
        paras.append(runs or [Run("")])
    return paras


# ═════════════════════════════════════════════════════════════
# 4. XML 헬퍼
# ═════════════════════════════════════════════════════════════
def _effects(shape):
    spPr = shape._element.spPr
    eff = spPr.find(qn("a:effectLst"))
    if eff is None:
        eff = etree.SubElement(spPr, qn("a:effectLst"))
    return eff


def _shadow(shape, blur=14, dist=3, alpha=16, color="5A6372", dir_deg=90):
    eff = _effects(shape)
    for old in eff.findall(qn("a:outerShdw")):
        eff.remove(old)
    sh = etree.SubElement(eff, qn("a:outerShdw"), {
        "blurRad": str(Pt(blur)), "dist": str(Pt(dist)), "dir": str(int(dir_deg * 60000)),
        "algn": "ctr", "rotWithShape": "0"})
    clr = etree.SubElement(sh, qn("a:srgbClr"), {"val": color})
    etree.SubElement(clr, qn("a:alpha"), {"val": str(alpha * 1000)})


def _glow(shape, color="1E9BC4", rad=12, alpha=40):
    eff = _effects(shape)
    g = etree.Element(qn("a:glow"), {"rad": str(Pt(rad))})
    clr = etree.SubElement(g, qn("a:srgbClr"), {"val": color})
    etree.SubElement(clr, qn("a:alpha"), {"val": str(alpha * 1000)})
    eff.insert(0, g)  # 스키마 순서: glow → outerShdw


def _no_line(shape):
    shape.line.fill.background()


def _gradient(shape, c1, c2, angle=0, a1=None, a2=None):
    """선형 그라데이션. angle 0 = 좌→우, 90 = 위→아래."""
    f = shape.fill
    f.gradient()
    f.gradient_angle = angle
    stops = f.gradient_stops
    stops[0].color.rgb = rgb(c1)
    stops[0].position = 0.0
    stops[1].color.rgb = rgb(c2)
    stops[1].position = 1.0
    if a1 is not None or a2 is not None:
        gs = shape._element.spPr.find(qn("a:gradFill")).find(qn("a:gsLst"))
        for g, a in zip(gs.findall(qn("a:gs")), (a1, a2)):
            if a is not None:
                etree.SubElement(g.find(qn("a:srgbClr")), qn("a:alpha"), {"val": str(int(a * 1000))})


def _alpha_fill(shape, hexcolor, alpha_pct):
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(hexcolor)
    srgb = shape._element.spPr.find(qn("a:solidFill")).find(qn("a:srgbClr"))
    etree.SubElement(srgb, qn("a:alpha"), {"val": str(int(alpha_pct * 1000))})


def _radius(shape, r_pt, w, h):
    shape.adjustments[0] = min(0.5, r_pt / max(1, min(w, h)))


def _soft_shadow(shape, blur_emu=312382, alpha=11.2, scale=102.3):
    """원본 카드 그림자: 오프셋 없이 사방으로 퍼지는 검정 11% (blur 24.6pt, 102% 확대)."""
    eff = _effects(shape)
    for old in eff.findall(qn("a:outerShdw")):
        eff.remove(old)
    sh = etree.SubElement(eff, qn("a:outerShdw"), {
        "blurRad": str(blur_emu), "sx": str(int(scale * 1000)), "sy": str(int(scale * 1000)),
        "algn": "ctr", "rotWithShape": "0"})
    clr = etree.SubElement(sh, qn("a:prstClr"), {"val": "black"})
    etree.SubElement(clr, qn("a:alpha"), {"val": str(int(alpha * 1000))})


def _grad_line(line, stops, angle=45, width=None):
    """선에 그라데이션. stops = [(pos 0~100, 'RRGGBB', alpha 0~100), ...]."""
    ln = line._get_or_add_ln()
    if width is not None:
        ln.set("w", str(Pt(width)))
    for tag in ("a:noFill", "a:solidFill", "a:gradFill", "a:pattFill"):
        for old in ln.findall(qn(tag)):
            ln.remove(old)
    gf = etree.Element(qn("a:gradFill"))
    gs = etree.SubElement(gf, qn("a:gsLst"))
    for pos, col, a in stops:
        g = etree.SubElement(gs, qn("a:gs"), {"pos": str(int(pos * 1000))})
        c = etree.SubElement(g, qn("a:srgbClr"), {"val": col})
        if a < 100:
            etree.SubElement(c, qn("a:alpha"), {"val": str(int(a * 1000))})
    etree.SubElement(gf, qn("a:lin"), {"ang": str(int(angle * 60000)), "scaled": "0"})
    ln.insert(0, gf)


def _pic_alpha(pic, alpha_pct):
    blip = pic._element.find(".//" + qn("a:blip"))
    for old in blip.findall(qn("a:alphaModFix")):
        blip.remove(old)
    blip.insert(0, etree.Element(qn("a:alphaModFix"), {"amt": str(int(alpha_pct * 1000))}))


def _pill_geom(shape, w, body_h, tail_h, tail_hw):
    """꼬리 달린 캡슐을 한 도형(custGeom)으로: 그라데이션이 꼬리까지 끊김 없이 이어진다(원본 방식)."""
    E = 12700
    W, B, TH, TW = int(w * E), int(body_h * E), int(tail_h * E), int(tail_hw * E)
    r = B // 2
    Ht = B + TH
    spPr = shape._element.spPr
    for old in spPr.findall(qn("a:prstGeom")):
        spPr.remove(old)
    cg = etree.Element(qn("a:custGeom"))
    for t in ("a:avLst", "a:gdLst", "a:ahLst", "a:cxnLst"):
        etree.SubElement(cg, qn(t))
    etree.SubElement(cg, qn("a:rect"), {"l": "l", "t": "t", "r": "r", "b": "b"})
    pl = etree.SubElement(cg, qn("a:pathLst"))
    path = etree.SubElement(pl, qn("a:path"), {"w": str(W), "h": str(Ht)})

    def pt(tag, x, y):
        el = etree.SubElement(path, qn(tag))
        etree.SubElement(el, qn("a:pt"), {"x": str(int(x)), "y": str(int(y))})
    pt("a:moveTo", r, 0)
    pt("a:lnTo", W - r, 0)
    etree.SubElement(path, qn("a:arcTo"), {"wR": str(r), "hR": str(r), "stAng": "16200000", "swAng": "10800000"})
    if TH > 0:
        pt("a:lnTo", W / 2 + TW, B)
        pt("a:lnTo", W / 2, Ht)
        pt("a:lnTo", W / 2 - TW, B)
    pt("a:lnTo", r, B)
    etree.SubElement(path, qn("a:arcTo"), {"wR": str(r), "hR": str(r), "stAng": "5400000", "swAng": "10800000"})
    etree.SubElement(path, qn("a:close"))
    # spPr 스키마 순서: xfrm → custGeom → fill → ln
    xfrm = spPr.find(qn("a:xfrm"))
    xfrm.addnext(cg)


def _line_dash(line, dash="sysDash"):
    ln = line._get_or_add_ln()
    for old in ln.findall(qn("a:prstDash")):
        ln.remove(old)
    etree.SubElement(ln, qn("a:prstDash"), {"val": dash})


# ═════════════════════════════════════════════════════════════
# 5. 래스터 에셋 (배경 텍스처, 방사형 글로우, 인물 처리) — tempdir 캐시
# ═════════════════════════════════════════════════════════════
def _cache(name):
    d = os.path.join(tempfile.gettempdir(), "cm_deck_assets")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)


def _bg_texture(dark=False) -> str:
    """원본 배경: 상단 #EFF0F1 → 하단 #E9ECEE 세로 그라데이션 위에 1px 그리드(18px 간격, 5칸마다 진하게)."""
    from PIL import Image, ImageDraw
    path = _cache("bg_dark_v2.png" if dark else "bg_light_v2.png")
    if os.path.exists(path):
        return path
    Wpx, Hpx, step = 1920, 1080, 18
    if dark:
        top, bot, line, major = (12, 30, 36), (7, 20, 25), (20, 44, 52), (28, 56, 66)
    else:
        top, bot, line, major = (241, 242, 243), (232, 235, 237), (229, 231, 234), (222, 225, 229)
    grad = Image.linear_gradient("L").resize((Wpx, Hpx))
    im = Image.composite(Image.new("RGB", (Wpx, Hpx), bot), Image.new("RGB", (Wpx, Hpx), top), grad)
    dr = ImageDraw.Draw(im, "RGBA")
    for i, x in enumerate(range(0, Wpx, step)):
        c = major if i % 5 == 0 else line
        dr.line([(x, 0), (x, Hpx)], fill=c + (150,), width=1)
    for i, y in enumerate(range(0, Hpx, step)):
        c = major if i % 5 == 0 else line
        dr.line([(0, y), (Wpx, y)], fill=c + (150,), width=1)
    if not dark:  # 원본의 은은한 대각 하이라이트(빛줄기)
        hl = Image.new("L", (Wpx, Hpx), 0)
        hd = ImageDraw.Draw(hl)
        for off, wdt, a in ((-200, 260, 34), (500, 160, 22)):
            hd.polygon([(off + 600, 0), (off + 600 + wdt, 0), (off + wdt - 300, Hpx), (off - 300, Hpx)], fill=a)
        from PIL import ImageFilter
        hl = hl.filter(ImageFilter.GaussianBlur(60))
        im = Image.composite(Image.new("RGB", (Wpx, Hpx), (252, 252, 253)), im, hl)
    im.save(path, optimize=True)
    return path


def _radial_png(color="1E9BC4", alpha=0.55, name=None) -> str:
    """중심이 진하고 가장자리가 투명한 원형 글로우 PNG."""
    from PIL import Image
    name = name or f"glow_{color}_{int(alpha * 100)}.png"
    path = _cache(name)
    if os.path.exists(path):
        return path
    n = 512
    r, g, b = (int(color[i:i + 2], 16) for i in (0, 2, 4))
    im = Image.new("RGBA", (n, n))
    px = im.load()
    for y in range(n):
        for x in range(n):
            d = math.hypot(x - n / 2, y - n / 2) / (n / 2)
            a = max(0.0, 1 - d) ** 2.2 * alpha
            px[x, y] = (r, g, b, int(a * 255))
    im.save(path)
    return path


def _silhouette_png() -> str:
    """사진이 없을 때 쓰는 인물 자리표시: 부드러운 회색 실루엣 + 하단 페이드(흑백 사진 톤과 맞춤)."""
    from PIL import Image, ImageDraw, ImageFilter
    path = _cache("silhouette_v2.png")
    if os.path.exists(path):
        return path
    Wp, Hp = 780, 1000
    m = Image.new("L", (Wp, Hp), 0)
    dr = ImageDraw.Draw(m)
    dr.ellipse([Wp * 0.33, Hp * 0.10, Wp * 0.67, Hp * 0.47], fill=255)            # 머리
    dr.rectangle([Wp * 0.44, Hp * 0.40, Wp * 0.56, Hp * 0.56], fill=255)          # 목
    dr.rounded_rectangle([Wp * 0.06, Hp * 0.53, Wp * 0.94, Hp * 1.3], radius=int(Wp * 0.3), fill=255)  # 어깨
    m = m.filter(ImageFilter.GaussianBlur(2))
    shade = Image.linear_gradient("L").resize((Wp, Hp)).point(lambda v: 168 + v * 50 // 255)
    body = Image.merge("RGBA", (shade, shade, shade.point(lambda v: min(255, v + 6)), m))
    fade = Image.new("L", (1, Hp))
    for y in range(Hp):
        fade.putpixel((0, y), 255 if y < Hp * 0.7 else int(255 * (1 - (y - Hp * 0.7) / (Hp * 0.3))))
    alpha = Image.composite(m, Image.new("L", (Wp, Hp), 0), fade.resize((Wp, Hp)))
    body.putalpha(alpha)
    body.save(path)
    return path


def portrait_png(src: str, fade=0.28) -> str:
    """인물 사진 → 흑백 + 하단 페이드(배경색으로). 원본 인사이트/팀 장표 처리 방식."""
    from PIL import Image, ImageOps
    base = os.path.splitext(os.path.basename(src))[0]
    out = _cache(f"portrait_{base}.png")
    im = ImageOps.grayscale(Image.open(src).convert("RGB")).convert("RGBA")
    w, h = im.size
    mask = Image.new("L", (1, h))
    start = int(h * (1 - fade))
    for y in range(h):
        mask.putpixel((0, y), 255 if y < start else int(255 * (1 - (y - start) / (h - start))))
    im.putalpha(mask.resize((w, h)))
    im.save(out)
    return out


# ═════════════════════════════════════════════════════════════
# 6. 아이소메트릭 일러스트 팔레트
# ═════════════════════════════════════════════════════════════
ISO = {  # (top, left, right) 면 색
    "blue": ("CBE9F3", "6FC2DC", "1E9BC4"),
    "deep": ("9ED6E8", "1E9BC4", "0E7FA5"),
    "cyan": ("C7F4F1", "6EDDD6", "33BDB6"),
    "white": ("FFFFFF", "E3E8F2", "C9D1E0"),
    "navy": ("3E9FC2", "0D6E8E", "0C5670"),
    "grey": ("E9EBEF", "CDD1D8", "B3B9C3"),
}


# ═════════════════════════════════════════════════════════════
# 7. Deck
# ═════════════════════════════════════════════════════════════
class Deck:
    def __init__(self, template: str | None = None, copyright: str = COPYRIGHT):
        self.prs = Presentation(template) if template else Presentation()
        self.prs.slide_width = Pt(W)
        self.prs.slide_height = Pt(H)
        self._blank = self.prs.slide_layouts[6]
        self.copyright = copyright
        self.page_no = 0
        self.appendix_no = 0
        self.warnings: list[str] = []
        self._slide_idx = 0

    def _warn(self, msg):
        self.warnings.append(f"[slide {self._slide_idx}] {msg}")

    # ── 프리미티브 ─────────────────────────────────────────
    def text(self, slide, x, y, w, h, text, size=16, weight="regular", color="000000",
             align="left", anchor="top", line_spacing=1.2, wrap=True, check=True):
        tb = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
        tf = tb.text_frame
        # 줄바꿈을 끈 상자는 LibreOffice/Keynote가 가운데 기준으로 늘려 정렬이 틀어진다 →
        # 항상 wrap=True로 두고, 넘침은 아래 check에서 경고로 잡는다.
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Pt(0)
        tf.margin_top = tf.margin_bottom = Pt(0)
        tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE,
                              "bottom": MSO_ANCHOR.BOTTOM}[anchor]
        paras = parse(text)
        for i, runs in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
                           "right": PP_ALIGN.RIGHT}[align]
            p.line_spacing = line_spacing
            for r in runs:
                run = p.add_run()
                run.text = r.text
                f = run.font
                f.size = Pt(size)
                bold = r.bold or weight == "bold"
                f.bold = bold
                f.name = FONT if bold else FONT_W[weight]
                _set_ea_font(run, f.name)
                f.color.rgb = rgb(r.color or color)
        if check:  # 넘침 점검: 줄 폭 > 상자 폭이면 (자동 줄바꿈되어) 줄 수가 늘어남
            lines = 0
            for line in text.split("\n"):
                lw = text_width(line, size, "bold" if weight == "bold" else weight)
                lines += max(1, math.ceil(lw / max(w, 1) - 0.02))
                if not wrap and lw > w + 2:
                    self._warn(f"한 줄 넘침 {lw:.0f}>{w:.0f}pt: {line[:24]}…")
            need = lines * size * line_spacing * 1.17
            if need > h + size * 0.6 and h > 0:
                self._warn(f"텍스트 상자 높이 부족 (필요≈{need:.0f}pt, 상자 {h:.0f}pt): {text[:24]}…")
        return tb

    def rect(self, slide, x, y, w, h, fill="FFFFFF", radius=0, line=None, line_w=1.0,
             shadow=False, alpha=None, gradient=None, shape=None):
        kind = shape or (MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE)
        s = slide.shapes.add_shape(kind, Pt(x), Pt(y), Pt(w), Pt(h))
        if radius and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
            _radius(s, radius, w, h)
        if gradient:
            _gradient(s, *gradient)
        elif fill is None:
            s.fill.background()
        elif alpha is not None:
            _alpha_fill(s, fill, alpha)
        else:
            s.fill.solid()
            s.fill.fore_color.rgb = rgb(fill)
        if line:
            s.line.color.rgb = rgb(line)
            s.line.width = Pt(line_w)
        else:
            _no_line(s)
        if shadow:
            _shadow(s)
        return s

    def poly(self, slide, pts, fill, line=None, line_w=0.5, alpha=None):
        """자유 다각형 (pt 좌표 리스트)."""
        fb = slide.shapes.build_freeform(Pt(pts[0][0]), Pt(pts[0][1]), scale=1.0)
        fb.add_line_segments([(Pt(px), Pt(py)) for px, py in pts[1:]], close=True)
        s = fb.convert_to_shape()
        if alpha is not None:
            _alpha_fill(s, fill, alpha)
        else:
            s.fill.solid()
            s.fill.fore_color.rgb = rgb(fill)
        if line:
            s.line.color.rgb = rgb(line)
            s.line.width = Pt(line_w)
        else:
            _no_line(s)
        return s

    def line(self, slide, x1, y1, x2, y2, color="D3D6DB", w=0.75, dash=None, arrow=False):
        ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(x1), Pt(y1), Pt(x2), Pt(y2))
        ln.line.color.rgb = rgb(color)
        ln.line.width = Pt(w)
        if dash:
            _line_dash(ln.line, dash)
        if arrow:
            etree.SubElement(ln.line._get_or_add_ln(), qn("a:tailEnd"),
                             {"type": "triangle", "w": "med", "len": "med"})
        return ln

    def image(self, slide, path, x, y, w=None, h=None):
        return slide.shapes.add_picture(path, Pt(x), Pt(y),
                                        Pt(w) if w else None, Pt(h) if h else None)

    def blob(self, slide, cx, cy, r, color="1595C2", alpha=88, soft=16):
        """진한 블루 원 + 부드러운 가장자리 글로우 (포지셔닝 맵의 '우리' 위치). 흰 글자를 올려도 읽힌다."""
        o = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(cx - r), Pt(cy - r), Pt(2 * r), Pt(2 * r))
        _alpha_fill(o, color, alpha)
        _no_line(o)
        _glow(o, color, rad=soft, alpha=45)
        return o

    def asset(self, slide, name, x, y, w=None, h=None, alpha=None, center=False):
        """원본 에셋 배치. w나 h 하나만 주면 비율 유지. center=True면 (x, y)가 중심.
        이름 목록: assets/manifest.json (또는 references/assets.md)."""
        p = asset_path(name)
        if p is None:
            self._warn(f"에셋 없음: {name}")
            return None
        m = manifest()[name]
        ar = m["h"] / m["w"]
        if w is None and h is None:
            w = m["w"] / 2
        if h is None:
            h = w * ar
        if w is None:
            w = h / ar
        if center:
            x, y = x - w / 2, y - h / 2
        pic = self.image(slide, p, x, y, w, h)
        if alpha is not None:
            _pic_alpha(pic, alpha)
        return pic

    def glow(self, slide, cx, cy, r, color="1E9BC4", alpha=0.55):
        """원형 블루 글로우 (인물 뒤, 포지셔닝 맵의 '우리', 핵심 카드 뒤). 기본은 원본 에셋 fx/glow_blue."""
        if color == "1E9BC4" and asset_path("fx/glow_blue"):
            return self.asset(slide, "fx/glow_blue", cx - r, cy - r, 2 * r, 2 * r, alpha=min(100, alpha * 130))
        return self.image(slide, _radial_png(color, alpha), cx - r, cy - r, 2 * r, 2 * r)

    # ── 슬라이드 골격 ─────────────────────────────────────
    def _new(self, dark=False, bg=None):
        """bg: None(라이트/다크 기본) | 'closing' | 'cover' | 에셋 이름. 원본 합성 배경이 없으면 절차적 텍스처."""
        s = self.prs.slides.add_slide(self._blank)
        self._slide_idx += 1
        name = bg or ("bg/dark" if dark else "bg/light")
        if not name.startswith("bg/"):
            name = "bg/" + name
        p = asset_path(name)
        s.shapes.add_picture(p or _bg_texture(dark), 0, 0, Pt(W), Pt(H))
        return s

    def content_slide(self, label, headline, sub=None, *, appendix=False, dark=False):
        """표준 본문 장표: 섹션 라벨 + 결론형 헤드라인(한 줄) + 서브헤드(한 줄) + 푸터."""
        s = self._new(dark)
        fg = "FFFFFF" if dark else C["black"]
        subc = "C9CEDD" if dark else C["text"]
        self.text(s, MARGIN_X, 22, 400, 14, label, *T["label"], color=C["blue_label"])
        hs = fit_size(headline, CONTENT_W, (24, 23, 22), "bold")
        if text_width(headline, hs, "bold") > CONTENT_W:
            self._warn(f"헤드라인이 한 줄을 넘음 → 문장을 줄일 것: {headline[:30]}…")
        self.text(s, MARGIN_X, 56, CONTENT_W + 20, 34, headline, hs, "bold", fg, check=False)
        if sub:
            ss = fit_size(sub, CONTENT_W, (18, 17, 16, 15, 14), "medium")
            if text_width(sub, ss, "medium") > CONTENT_W:
                self._warn(f"서브헤드가 한 줄을 넘음 → 문장을 줄일 것: {sub[:30]}…")
            self.text(s, MARGIN_X, 101, CONTENT_W + 20, 26, sub, ss, "medium", subc, check=False)
        if appendix:
            self.appendix_no += 1
            n = self.appendix_no
        else:
            self.page_no += 1
            n = self.page_no
        self.footer(s, n, dark)
        return s

    def footer(self, slide, n, dark=False):
        c = "8A90A6" if dark else C["muted"]
        self.text(slide, 560, 513, 330, 12, self.copyright, *T["footer"], color=c, align="right", check=False)
        self.text(slide, 896, 511, 26, 14, str(n), *T["page_no"], color=c, align="right", check=False)

    def footnote(self, slide, lines, x=MARGIN_X + 8, y=None, w=430, bottom=506):
        lines = [l if l.startswith("*") else f"* {l}" for l in lines]
        y = y if y is not None else bottom - 13 * len(lines)
        self.text(slide, x, y, w, 13 * len(lines), "\n".join(lines), *T["footnote"],
                  color=C["muted"], line_spacing=1.0, check=False)

    # ── 표지 / 클로징 / 간지 ───────────────────────────────
    def cover(self, title, sub="", photo=None, tag=None):
        """표지: 원본 합성 배경(로열블루 + 연구실 엔지니어 사진) + 시안 네트워크 선. 제목은 **키워드**만 Bold.
        photo를 주면 그 사진으로 표지 배경을 새로 합성한다(우측 699pt 영역, 50% 투명 + 좌→우 블루 페이드)."""
        if photo:
            s = self.prs.slides.add_slide(self._blank)
            self._slide_idx += 1
            self.rect(s, 0, 0, W, H, fill="0B5A73")
            pic = s.shapes.add_picture(photo, Pt(261), 0, Pt(699), Pt(H))
            _pic_alpha(pic, 50)
            self.rect(s, 243, 0, 540, H, gradient=("0B5A73", "0B5A73", 0))
            _gradient(s.shapes[-1], "0B5A73", "0B5A73", 0, a1=100, a2=0)
        else:
            s = self._new(bg="bg/cover")
        if asset_path("fx/network_lines"):
            self.asset(s, "fx/network_lines", 261, 197, 699, 343)
        else:
            self._network(s, 470, 230, 490, 310)
        self.text(s, MARGIN_X, 40, 760, 90, title, 32, "medium", "FFFFFF", line_spacing=1.12)
        self.rect(s, MARGIN_X, 128, 0.75, 48, fill="FFFFFF", alpha=55)
        if sub:
            self.text(s, MARGIN_X, 205, 640, 60, sub, 20, "regular", "FFFFFF", line_spacing=1.35)
        if tag:
            self.text(s, MARGIN_X, 492, 400, 16, tag, 12, "semibold", "C4E6F1", check=False)
        return s

    def _network(self, slide, x0, y0, w, h, seed=7, n=26):
        """표지 우측 하단의 점·선 네트워크(시안 노드 + 반투명 연결선)."""
        import random
        rnd = random.Random(seed)
        pts = [(x0 + rnd.random() * w, y0 + rnd.random() * h) for _ in range(n)]
        for i, (ax, ay) in enumerate(pts):
            near = sorted(pts, key=lambda p: (p[0] - ax) ** 2 + (p[1] - ay) ** 2)[1:4]
            for bx, by in near:
                ln = self.line(slide, ax, ay, bx, by, color="62E3DA", w=0.6)
                ln_el = ln.line._get_or_add_ln()
                clr = ln_el.find(qn("a:solidFill")).find(qn("a:srgbClr"))
                etree.SubElement(clr, qn("a:alpha"), {"val": "45000"})
        for i, (ax, ay) in enumerate(pts):
            r = 2.2 if i % 3 else 3.6
            o = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(ax - r), Pt(ay - r), Pt(2 * r), Pt(2 * r))
            _alpha_fill(o, "6FF0E6" if i % 4 else "2CA6D3", 90)
            _no_line(o)

    def closing(self, text, photo=None):
        """클로징: 원본 합성 배경(#001B7F + 키보드·문서 사진 20%) + 가운데 2줄 다짐문."""
        if photo:
            s = self.prs.slides.add_slide(self._blank)
            self._slide_idx += 1
            self.rect(s, 0, 0, W, H, fill="07475A")
            pic = s.shapes.add_picture(photo, 0, 0, Pt(W), Pt(H))
            _pic_alpha(pic, 20)
        else:
            s = self._new(bg="bg/closing")
        self.text(s, 60, 222, W - 120, 90, text, 27.7, "medium", "FFFFFF", align="center",
                  line_spacing=1.35)
        return s

    def divider(self, title, sub=""):
        s = self.prs.slides.add_slide(self._blank)
        self._slide_idx += 1
        self.rect(s, 0, 0, W, H, gradient=("0D5C74", "083F50", 90))
        self.text(s, MARGIN_X, 230, CONTENT_W, 40, title, 32, "bold", "FFFFFF")
        if sub:
            self.text(s, MARGIN_X, 280, CONTENT_W, 30, sub, 18, "regular", "C9CEDD")
        return s

    # ── 라벨류 ────────────────────────────────────────────
    def pill(self, slide, x, y, w, text, style="blue", h=26, tail=True, size=None):
        """말풍선 라벨 — 원본 실측: 몸통 h≈25.5, 꼬리 높이 h×0.49, 꼬리 반폭 7pt, 한 도형.
        style: blue(#0030DE→#5E7EFF 45°) | dark(#404040, '결과') | soft(#5E7DFF) | ghost(연블루 바탕)."""
        th = h * 0.49 if tail and style != "ghost" else 0
        p = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(x), Pt(y), Pt(w), Pt(h + th))
        _pill_geom(p, w, h, th, 7 * h / 25.5)
        if style == "blue":
            _gradient(p, "0E7FA5", "3DB5DA", 45)
        elif style == "dark":
            p.fill.solid()
            p.fill.fore_color.rgb = rgb("404040")
        elif style == "soft":
            p.fill.solid()
            p.fill.fore_color.rgb = rgb(C["blue_label"])
        else:
            p.fill.solid()
            p.fill.fore_color.rgb = rgb(C["blue_mist"])
        _no_line(p)
        color = C["blue"] if style == "ghost" else "FFFFFF"
        sz = size or (14 if h >= 24 else 12)
        if text_width(text, sz, "bold") > w - 16:
            self._warn(f"pill 텍스트가 폭 초과: {text}")
        self.text(slide, x, y, w, h, text, sz, "bold", color, align="center", anchor="middle",
                  wrap=False, check=False)
        return p

    def tag(self, slide, x, y, w, text, style="dark", h=22, size=12):
        """작은 캡슐 태그 ('구직자', '기업', '핵심 가치', 'Solution 01')."""
        fill = {"dark": "3A3A3A", "blue": C["blue_label"], "mist": C["blue_mist"],
                "grad": None}[style]
        if style == "grad":
            self.rect(slide, x, y, w, h, radius=h / 2, gradient=(C["blue_deep"], C["blue_end"]))
        else:
            self.rect(slide, x, y, w, h, radius=h / 2, fill=fill)
        self.text(slide, x, y, w, h, text, size, "bold",
                  C["blue"] if style == "mist" else "FFFFFF", align="center", anchor="middle",
                  wrap=False, check=False)

    def number_badge(self, slide, cx, cy, text="!", r=10):
        """흐름선 위 블루 원형 배지 ('!' 경고, 1·2·3 단계 번호)."""
        o = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(cx - r), Pt(cy - r), Pt(2 * r), Pt(2 * r))
        _gradient(o, C["blue_deep"], C["blue_end"], 45)
        o.line.color.rgb = rgb("FFFFFF")
        o.line.width = Pt(1.5)
        _shadow(o, blur=6, dist=1, alpha=25, color="1088B0")
        self.text(slide, cx - r, cy - r, 2 * r, 2 * r, text, r * 1.1, "bold", "FFFFFF",
                  align="center", anchor="middle", wrap=False, check=False)

    # ── 카드 ──────────────────────────────────────────────
    def card(self, slide, x, y, w, h, style="white", radius=18, sheen=False):
        """둥근 카드 — 원본 도형 속성 그대로.
        white  : 흰색 70% + 1.5pt 유리 테두리(흰→#D9D9D9 45° 그라데이션) + 사방 그림자(blur 24.6pt, 11%)
        outline: 흰색 70% + 1pt #0032E7 테두리 + 같은 그림자  ← 핵심 카드, 장표당 1개
        solid  : 흰색 100% (표·스크린샷·차트 받침)
        grey   : #BFBFBF 83% + 1pt #D9D9D9  ← '결과/한계'
        mid    : 회색 그라데이션 (BM 가운데, 경쟁사 열)
        blue   : 블루 그라데이션 하이라이트 (KPI)
        dark   : 다크 장표 카드 (#09112E → #404040 57%)
        sheen  : 카드 중간의 옅은 빛 띠(원본 문제 장표 1열처럼 일러스트를 받치는 카드에만). 기본 꺼짐."""
        if style in ("white", "outline", "solid"):
            c = self.rect(slide, x, y, w, h, radius=radius, fill="FFFFFF", alpha=None if style == "solid" else 70)
            if style == "outline":
                c.line.color.rgb = rgb("0F86AB")
                c.line.width = Pt(1)
            else:
                _grad_line(c.line, [(0, "FFFFFF", 100), (37, "D9D9D9", 100), (69, "F2F2F2", 100), (99, "D9D9D9", 100)],
                           angle=45, width=1.5)
            _soft_shadow(c)
            if sheen:
                band = self.rect(slide, x + 1, y + h * 0.27, w - 2, h * 0.46, fill="FFFFFF")
                fill = band.fill
                fill.gradient()
                fill.gradient_angle = 90
                st = fill.gradient_stops
                st[0].color.rgb = rgb("D9D9D9")
                st[0].position = 0.0
                st[1].color.rgb = rgb("FFFFFF")
                st[1].position = 1.0
                gs = band._element.spPr.find(qn("a:gradFill")).find(qn("a:gsLst"))
                g0, g1 = gs.findall(qn("a:gs"))
                etree.SubElement(g0.find(qn("a:srgbClr")), qn("a:alpha"), {"val": "12000"})
                etree.SubElement(g1.find(qn("a:srgbClr")), qn("a:alpha"), {"val": "0"})
                mid = etree.SubElement(gs, qn("a:gs"), {"pos": "40000"})
                etree.SubElement(etree.SubElement(mid, qn("a:srgbClr"), {"val": "FFFFFF"}), qn("a:alpha"), {"val": "38072"})
            return c
        if style == "grey":
            c = self.rect(slide, x, y, w, h, radius=radius, fill="BFBFBF", alpha=83, line="D9D9D9", line_w=1)
            return c
        if style == "mid":
            c = self.rect(slide, x, y, w, h, radius=radius, gradient=("E6E8EC", "D9DCE2", 90))
            _soft_shadow(c)
            return c
        if style == "blue":
            c = self.rect(slide, x, y, w, h, radius=radius, gradient=(C["blue_label"], "64BEDA", 45))
            _soft_shadow(c, alpha=22)
            return c
        if style == "dark":
            c = self.rect(slide, x, y, w, h, radius=radius, gradient=("0C1C22", "404040", 90))
            gs = c._element.spPr.find(qn("a:gradFill")).find(qn("a:gsLst")).findall(qn("a:gs"))
            etree.SubElement(gs[1].find(qn("a:srgbClr")), qn("a:alpha"), {"val": "57000"})
            gs[1].set("pos", "98000")
            c.line.color.rgb = rgb("4E6A74")
            c.line.width = Pt(0.75)
            return c
        raise ValueError(style)

    def x_mark(self, slide, cx, cy, size=130, color="C00000"):
        """원본 문제 장표의 빨간 ✕ (곱하기 도형). 일러스트 위에 얹는다."""
        m = slide.shapes.add_shape(MSO_SHAPE.MATH_MULTIPLY, Pt(cx - size / 2), Pt(cy - size / 2), Pt(size), Pt(size * 1.02))
        m.adjustments[0] = 0.14337
        m.fill.solid()
        m.fill.fore_color.rgb = rgb(color)
        _no_line(m)
        return m

    def highlight_bar(self, slide, x, y, w, text, h=40, size=18):
        """카드 상단 블루 그라데이션 결론 바 ('연 7,300억 규모의 …')."""
        b = self.rect(slide, x, y, w, h, radius=9, gradient=(C["blue_deep"], C["blue_end"]))
        _shadow(b, blur=12, dist=3, alpha=28, color="1088B0")
        self.text(slide, x, y, w, h, text, size, "semibold", "FFFFFF", align="center",
                  anchor="middle", wrap=False, check=False)
        return b

    # ── 화살표 ────────────────────────────────────────────
    def flow(self, slide, x1, x2, y, badge=None):
        """pill과 pill 사이의 진행선. x1 = 앞 pill 오른쪽 끝, x2 = 뒤 pill 왼쪽 끝. badge='!' 이면 중간 배지."""
        g1, g2 = 5, 14  # 원본: 앞 pill 끝에서 5pt, 뒤 pill 앞 14pt
        if badge:
            bx = x2 - g2 - 34
            self._fade_arrow(slide, x1 + g1, bx - 14, y, head=False)
            if badge == "!" and asset_path("icon/alert_circle"):
                self.asset(slide, "icon/alert_circle", bx, y, 23, 23, center=True)
            else:
                self.number_badge(slide, bx, y, badge, r=11)
            return self._fade_arrow(slide, bx + 13, x2 - g2, y, fade=False)
        return self._fade_arrow(slide, x1 + g1, x2 - g2, y)

    def _fade_arrow(self, slide, x1, x2, y, head=True, fade=True, color="0E7FA5", wt=0.9):
        """투명→진한 블루로 짙어지는 선 + 삼각 화살촉 (원본 진행선).
        선 그라데이션은 렌더러마다 지원이 달라서, 얇은 사각형 그라데이션 + 삼각형으로 그린다."""
        hl = 6 if head else 0
        bar = self.rect(slide, x1, y - wt / 2, max(1, x2 - x1 - hl + 1), wt, fill=color)
        if fade:
            _gradient(bar, color, color, 0, a1=0, a2=100)
        if head:
            self.poly(slide, [(x2 - hl, y - 3.2), (x2, y), (x2 - hl, y + 3.2)], color)
        return bar

    def flow_line(self, slide, x1, x2, y, color=None):  # 하위 호환
        return self.line(slide, x1, y, x2, y, color=color or "4FB2D2", w=1, arrow=True)

    def chevron(self, slide, x, y, w=34, h=64, glow=True):
        """카드 사이 블루 화살표: 왼쪽으로 사라지는 꼬리(그라데이션) + 진한 삼각 머리. (x, y) = 좌상단, w×h = 전체 크기."""
        tail_w, head_w = w * 0.5, w * 0.5
        t = self.rect(slide, x, y + h * 0.28, tail_w + 1, h * 0.44, fill=C["blue_label"])
        _gradient(t, "8DCFE4", C["blue_label"], 0, a1=0, a2=80)
        cx, cy = x + tail_w + head_w / 2, y + h / 2
        head = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Pt(cx - h / 2), Pt(cy - head_w / 2),
                                      Pt(h), Pt(head_w))
        head.rotation = 90
        _gradient(head, "5FBBD8", C["blue_end"], 0)
        _no_line(head)
        if glow:
            _glow(head, rad=10, alpha=35)
        return head

    def down_arrow(self, slide, x, y, w=80, h=30, fill="3A3A3A"):
        a = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Pt(x), Pt(y), Pt(w), Pt(h))
        a.rotation = 180
        a.fill.solid()
        a.fill.fore_color.rgb = rgb(fill)
        _no_line(a)
        return a

    def wedge(self, slide, src, dst, alpha=(0, 35)):
        """두 박스를 잇는 반투명 블루 사다리꼴 (KPI 타일 → 차트 카드 '확대' 효과).
        src/dst = (x, y, w, h). src 오른쪽 변 → dst 왼쪽 변."""
        sx, sy, sw, sh = src
        dx, dy, dw, dh = dst
        p = self.poly(slide, [(sx + sw, sy), (dx, dy), (dx, dy + dh), (sx + sw, sy + sh)], C["blue_label"])
        _gradient(p, "8DCFE4", "C3E5F0", 0, a1=alpha[1], a2=alpha[0])
        return p

    # ── 데이터 표시 ───────────────────────────────────────
    def kpi(self, slide, x, y, w, h, label, value, highlight=False, value_color=None,
            label_size=14, value_size=20, illo=None):
        """KPI 타일: 위 블루 라벨 + (선택 일러스트) + 아래 큰 숫자. highlight는 장표당 1개."""
        self.card(slide, x, y, w, h, "blue" if highlight else "white", radius=16)
        lc = "FFFFFF" if highlight else C["blue_label"]
        vc = "FFFFFF" if highlight else (value_color or C["black"])
        nl = label.count("\n") + 1
        if illo:
            self.text(slide, x + 8, y + 22, w - 16, 22 * nl, label, label_size, "bold", lc,
                      align="center", line_spacing=1.1, check=False)
            self.illo(slide, illo, x + w / 2, y + h * 0.5, min(w, h) * 0.42)
            self.text(slide, x + 8, y + h - 28 - value_size, w - 16, value_size + 8, value, value_size,
                      "bold", vc, align="center", check=False)
        else:
            self.text(slide, x + 8, y + h * 0.18, w - 16, 20 * nl, label, label_size, "bold", lc,
                      align="center", line_spacing=1.1, check=False)
            self.text(slide, x + 8, y + h * 0.62, w - 16, value_size + 8, value, value_size, "bold", vc,
                      align="center", check=False)

    def stat_block(self, slide, x, y, w, kicker, value, note=None, value_size=26,
                   value_color="000000", kicker_style="blue"):
        """tag(블루 캡슐) + 큰 숫자 + 설명 — 시장 3분할 등."""
        tw = min(w - 10, text_width(kicker, 12, "bold") + 40)
        self.tag(slide, x + (w - tw) / 2, y, tw, kicker, kicker_style, h=24)
        self.text(slide, x, y + 36, w, value_size + 8, value, value_size, "bold", value_color,
                  align="center", check=False)
        if note:
            self.text(slide, x, y + 44 + value_size, w, 34, note, 12, "regular", C["text"], align="center")

    def bullets(self, slide, x, y, w, items, size=14, color="000000", gap=1.35,
                bullet="•", sub_color=None, weight="medium"):
        """불릿. '- '로 시작하는 항목은 하위 설명(작은 회색)."""
        tb = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(22 * len(items)))
        tf = tb.text_frame
        tf.word_wrap = True
        for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
            setattr(tf, m, Pt(0))
        first = True
        for it in items:
            sub = it.startswith("- ")
            line = it if sub else (f"{bullet}  {it}" if bullet else it)
            for runs in parse(line):
                p = tf.paragraphs[0] if first else tf.add_paragraph()
                first = False
                p.line_spacing = gap
                if sub:
                    p.level = 0
                    pPr = p._p.get_or_add_pPr()
                    pPr.set("marL", str(Pt(14)))
                for r in runs:
                    run = p.add_run()
                    run.text = r.text
                    f = run.font
                    f.size = Pt(size - 2 if sub else size)
                    f.bold = r.bold
                    f.name = FONT if r.bold else FONT_W["regular" if sub else weight]
                    _set_ea_font(run, f.name)
                    f.color.rgb = rgb(r.color or ((sub_color or C["text2"]) if sub else color))
        return tb

    def check_list(self, slide, x, y, w, items, size=14, gap=34):
        """블루 원형 ✓ + 문장 (Scale-Up '검증 시장 현황')."""
        for i, it in enumerate(items):
            cy = y + i * gap
            o = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(x), Pt(cy + 1), Pt(15), Pt(15))
            o.fill.solid()
            o.fill.fore_color.rgb = rgb("FFFFFF")
            o.line.color.rgb = rgb(C["blue"])
            o.line.width = Pt(1.5)
            self.poly(slide, [(x + 4, cy + 8.6), (x + 6.6, cy + 11.4), (x + 11.6, cy + 5.6),
                              (x + 11.6, cy + 7.4), (x + 6.6, cy + 13.2), (x + 4, cy + 10.4)], C["blue"])
            self.text(slide, x + 24, cy, w - 24, gap, it, size, "semibold", C["black"],
                      line_spacing=1.15)

    def table(self, slide, x, y, w, rows, col_w=None, row_h=24, header_fill=None,
              size=12, header_bold=True, border="000000", border_w=0.75, first_col_fill=None,
              align="center", bold_cells=(), blue_cells=(), muted_cells=(), header_color="000000"):
        """브랜드 표. rows[0] = 헤더. 헤더 연블루(#DAE9F9) 또는 흰색, 0.75pt 테두리."""
        nrows, ncols = len(rows), len(rows[0])
        gt = slide.shapes.add_table(nrows, ncols, Pt(x), Pt(y), Pt(w), Pt(row_h * nrows))
        tbl = gt.table
        tblPr = tbl._tbl.tblPr
        for attr in ("bandRow", "firstRow"):
            tblPr.set(attr, "0")
        style = tblPr.find(qn("a:tableStyleId"))
        if style is None:
            style = etree.SubElement(tblPr, qn("a:tableStyleId"))
        style.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"
        if col_w:
            for i, cw in enumerate(col_w):
                tbl.columns[i].width = Pt(cw)
        for r in range(nrows):
            tbl.rows[r].height = Pt(row_h)
            for c in range(ncols):
                cell = tbl.cell(r, c)
                cell.margin_left = cell.margin_right = Pt(5)
                cell.margin_top = cell.margin_bottom = Pt(2)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                fill = header_fill if (r == 0 and header_fill) else (
                    first_col_fill if (c == 0 and first_col_fill and r > 0) else "FFFFFF")
                cell.fill.solid()
                cell.fill.fore_color.rgb = rgb(fill)
                tf = cell.text_frame
                tf.word_wrap = True
                for i, runs in enumerate(parse(str(rows[r][c]))):
                    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER}[align]
                    for run_ in runs:
                        run = p.add_run()
                        run.text = run_.text
                        f = run.font
                        f.size = Pt(size)
                        b = run_.bold or (r == 0 and header_bold) or (r, c) in bold_cells
                        f.bold = b
                        f.name = FONT if b else FONT_W["regular"]
                        _set_ea_font(run, f.name)
                        col = run_.color or (C["blue"] if (r, c) in blue_cells else
                                             C["muted"] if (r, c) in muted_cells else
                                             header_color if r == 0 else C["black"])
                        f.color.rgb = rgb(col)
                _cell_border(cell, border, border_w)
        return gt

    # ── 차트 (도형으로 그림 — 원본과 같은 마감, 라벨 자유) ──────────────
    def bars(self, slide, x, base_y, w, max_h, items, bar_w=None, gap=None, vmax=None,
             axis=True, label_size=12):
        """도형 막대. items = [{"cat":"25년 하반기","value":3200,"color":C["blue_soft"],
        "inside":"약 3,200만\n(430명)","inside_color":"000000","top":"…"}].
        반환: 각 막대의 (x, top_y, w) 리스트 → 성장 화살표·말풍선 배치에 사용."""
        n = len(items)
        bar_w = bar_w or w / n * 0.58
        slot = w / n
        vmax = vmax or max(it["value"] for it in items)
        out = []
        if axis:
            self.line(slide, x, base_y, x + w, base_y, color="C9CDD3", w=0.75)
        for i, it in enumerate(items):
            bh = max(2, max_h * it["value"] / vmax)
            bx = x + slot * i + (slot - bar_w) / 2
            by = base_y - bh
            b = self.rect(slide, bx, by, bar_w, bh, fill=it.get("color", C["navy"]))
            if it.get("gradient"):
                _gradient(b, *it["gradient"], 90)
            if it.get("inside"):
                ic = it.get("inside_color", "FFFFFF")
                self.text(slide, bx - 6, by + min(bh * 0.5, 120) - 18, bar_w + 12, 40, it["inside"], 13,
                          "medium", ic, align="center", line_spacing=1.2, check=False)
            if it.get("top"):
                self.text(slide, bx - 30, by - 42, bar_w + 60, 40, it["top"], 14, "bold", C["black"],
                          align="center", anchor="bottom", line_spacing=1.15, check=False)
            if it.get("cat"):
                self.text(slide, x + slot * i, base_y + 6, slot, 16, it["cat"], label_size, "semibold",
                          C["black"], align="center", check=False)
            out.append((bx, by, bar_w))
        return out

    def growth_arrow(self, slide, x1, y1, x2, y2, width=26, text=None, text_xy=None):
        """대각 성장 화살표 (흰색→블루 그라데이션). (x1,y1) 꼬리 → (x2,y2) 머리."""
        ang = math.atan2(y2 - y1, x2 - x1)
        L = math.hypot(x2 - x1, y2 - y1)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        a = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Pt(cx - L / 2), Pt(cy - width / 2), Pt(L), Pt(width))
        a.rotation = math.degrees(ang)
        a.adjustments[0] = 0.5
        a.adjustments[1] = 0.62
        _gradient(a, "FFFFFF", C["blue_deep"], 0, a1=0, a2=100)
        _no_line(a)
        if text:
            tx, ty = text_xy or (cx - 70, cy - 10)
            self.text(slide, tx, ty, 140, 44, text, 16, "bold", C["navy_text"], align="center",
                      line_spacing=1.2, check=False)
        return a

    def callout(self, slide, x, y, text, w=58, h=30, size=9, point="left"):
        """연블루 말풍선 ('영업이익\n0.4억'). (x, y) = 꼬리 끝."""
        bx = x + 7 if point == "left" else x - 7 - w
        self.rect(slide, bx, y - h / 2, w, h, radius=6, fill="BCE3EF")
        tri = [(x, y), (bx, y - 5), (bx, y + 5)] if point == "left" else [(x, y), (bx + w, y - 5), (bx + w, y + 5)]
        self.poly(slide, tri, "BCE3EF")
        self.text(slide, bx, y - h / 2, w, h, text, size, "bold", C["navy_text"], align="center",
                  anchor="middle", line_spacing=1.05, check=False)

    def legend(self, slide, x, y, items, w=190):
        """범례 카드 (로드맵 좌상단). items = [(color, label)]."""
        h = 14 + 20 * len(items)
        self.card(slide, x, y, w, h, "solid", radius=8)
        for i, (col, lab) in enumerate(items):
            self.rect(slide, x + 12, y + 10 + i * 20, 13, 13, fill=col)
            self.text(slide, x + 32, y + 9 + i * 20, w - 40, 14, lab, 10.5, "medium", C["text"],
                      wrap=False, check=False)

    def bar_chart(self, slide, x, y, w, h, categories, series: dict, colors=None,
                  stacked=False, labels=True, number_format='#,##0', gap=80, font_size=12,
                  axis=True, highlight_last=True):
        """네이티브 차트 (데이터 편집이 필요한 Appendix용). 본문 히어로 차트는 bars() 권장."""
        cd = CategoryChartData()
        cd.categories = categories
        for name, vals in series.items():
            cd.add_series(name, vals)
        ctype = XL_CHART_TYPE.COLUMN_STACKED if stacked else XL_CHART_TYPE.COLUMN_CLUSTERED
        gf = slide.shapes.add_chart(ctype, Pt(x), Pt(y), Pt(w), Pt(h), cd)
        ch = gf.chart
        ch.has_title = False
        ch.has_legend = len(series) > 1
        ch.font.size = Pt(font_size)
        ch.font.name = FONT
        plot = ch.plots[0]
        plot.gap_width = gap
        if stacked:
            plot.overlap = 100
        colors = colors or [C["blue_soft"], C["navy"], C["blue_deep"], C["blue_label"]]
        for i, s in enumerate(plot.series):
            s.format.fill.solid()
            s.format.fill.fore_color.rgb = rgb(colors[i % len(colors)])
        if len(series) == 1 and highlight_last:
            last = plot.series[0].points[len(categories) - 1]
            last.format.fill.solid()
            last.format.fill.fore_color.rgb = rgb(C["navy"])
        if labels:
            plot.has_data_labels = True
            dl = plot.data_labels
            dl.number_format = number_format
            dl.number_format_is_linked = False
            dl.font.size = Pt(font_size)
            dl.font.bold = True
            dl.position = XL_LABEL_POSITION.INSIDE_END if stacked else XL_LABEL_POSITION.OUTSIDE_END
        ch.value_axis.visible = False
        ch.value_axis.has_major_gridlines = False
        ca = ch.category_axis
        ca.tick_labels.font.size = Pt(font_size)
        ca.tick_labels.font.bold = True
        ca.format.line.color.rgb = rgb(C["line"])
        ca.visible = axis
        return gf

    def donut(self, slide, x, y, w, h, labels, values, colors=None, hole=68):
        cd = CategoryChartData()
        cd.categories = labels
        cd.add_series("s", values)
        gf = slide.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Pt(x), Pt(y), Pt(w), Pt(h), cd)
        ch = gf.chart
        ch.has_legend = False
        ch.has_title = False
        colors = colors or [C["blue_deep"], C["blue_soft"], "C9C9C9", C["blue_label"]]
        for i, pt in enumerate(ch.plots[0].series[0].points):
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = rgb(colors[i % len(colors)])
            pt.format.line.color.rgb = rgb("FFFFFF")
        hs = ch.plots[0]._element.find(qn("c:holeSize"))
        if hs is None:
            hs = etree.SubElement(ch.plots[0]._element, qn("c:holeSize"))
        hs.set("val", str(hole))
        return gf

    def roadmap_chart(self, slide, years, x=MARGIN_X, base_y=318, w=CONTENT_W, max_h=150,
                      legend=("B2C 매출 (서비스 매출)", "B2B 매출 (채용 솔루션 판매 비용)")):
        """연도별 스택 막대 + 단계 키워드 + 총액 + (B2C / B2B) + 영업이익 말풍선 + 범례.
        years = [{"year":"26년","b2c":3.0,"b2b":2.0,"total":"5억","stage":"BEP 달성 예정","op":"0.4억"}]"""
        n = len(years)
        slot = w / n
        bar_w = slot * 0.30
        vmax = max(y["b2c"] + y["b2b"] for y in years)
        self.legend(slide, x, 158, [(C["blue_soft"], legend[0]), (C["blue_deep"], legend[1])], w=200)
        self.line(slide, x, base_y, x + w, base_y, color="9AA0AA", w=0.75)
        for i, yv in enumerate(years):
            cx = x + slot * i + slot / 2
            tot = yv["b2c"] + yv["b2b"]
            h_tot = max(3, max_h * tot / vmax)
            h_c = h_tot * yv["b2c"] / tot
            bx = cx - bar_w / 2
            self.rect(slide, bx, base_y - h_c, bar_w, h_c, fill=C["blue_soft"])
            b2 = self.rect(slide, bx, base_y - h_tot, bar_w, h_tot - h_c, fill=C["blue_deep"])
            _gradient(b2, C["blue_deep"], "2499C2", 90)
            top = base_y - h_tot
            self.text(slide, cx - 70, top - 24, 140, 18,
                      f"([[{_fmt(yv['b2c'])}]] / {{{{{_fmt(yv['b2b'])}}}}})", 13, "bold", C["text"],
                      align="center", check=False)
            self.text(slide, cx - 70, top - 46, 140, 20, yv["total"], 16, "bold", C["black"],
                      align="center", check=False)
            if yv.get("stage"):
                self.text(slide, cx - 90, top - 88, 180, 34, yv["stage"], 11.5, "bold", "0F7FA3",
                          align="center", anchor="bottom", line_spacing=1.15, check=False)
            if yv.get("op"):
                self.callout(slide, cx + 40, top - 38, f"영업이익\n{yv['op']}", w=50, h=28, size=8.5)
            self.text(slide, x + slot * i, base_y + 5, slot, 16, yv["year"], 12, "bold", C["black"],
                      align="center", check=False)

    def roadmap(self, slide, stages, x=MARGIN_X, y=342, w=CONTENT_W, h=168, highlight=None,
                kpi_label="매출 핵심 KPI", ms_label="핵심 Milestone"):
        """로드맵 하단 단계 카드. stages = [{'title','kpi':[...],'milestone':[...]}]. highlight = 현재 단계 index."""
        n = len(stages)
        gap = 12
        cw = (w - gap * (n - 1)) / n
        for i, st in enumerate(stages):
            cx = x + i * (cw + gap)
            self.card(slide, cx, y, cw, h, "outline" if i == highlight else "solid", radius=14)
            self.text(slide, cx, y + 14, cw, 18, st["title"], 13.5, "bold", "0F7FA3", align="center",
                      wrap=False)
            self.line(slide, cx + 16, y + 40, cx + cw - 16, y + 40, color="C9CDD3", w=0.75, dash="sysDot")
            body = ""
            if st.get("kpi"):
                body += f"**{kpi_label}**\n" + "\n".join(f"- {k}" for k in st["kpi"])
            if st.get("milestone"):
                body += f"\n\n**{ms_label}**\n" + "\n".join(f"- {m}" for m in st["milestone"])
            self.text(slide, cx + 14, y + 50, cw - 24, h - 56, body, 10.5, "regular", C["black"],
                      line_spacing=1.18)

    # ── 사람 ──────────────────────────────────────────────
    def portrait(self, slide, cx, bottom, h, photo=None, glow=True):
        """흑백 인물(하단 페이드) + 뒤 블루 원형 글로우(원본: fx/glow_blue 70%).
        photo = 파일 경로 또는 에셋 이름('people/insight_worker', 'team/01_ceo'). 없으면 실루엣."""
        if glow:
            r = h * 0.6
            self.glow(slide, cx, bottom - h * 0.6, r, "1E9BC4", 0.54)
        if photo and asset_path(photo):
            return self._asset_bottom(slide, photo, cx, bottom, h)
        if photo:
            from PIL import Image
            p = portrait_png(photo)
            iw, ih = Image.open(p).size
            w = h * iw / ih
            return self.image(slide, p, cx - w / 2, bottom - h, w, h)
        w = h * 0.78
        return self.image(slide, _silhouette_png(), cx - w / 2, bottom - h, w, h)

    def _asset_bottom(self, slide, name, cx, bottom, h):
        m = manifest()[name]
        w = h * m["w"] / m["h"]
        return self.asset(slide, name, cx - w / 2, bottom - h, w, h)

    def team_backdrop(self, slide):
        """팀 장표 배경: 도시 스카이라인 8% + 하단 흰 페이드(원본)."""
        if asset_path("bg/raw_team_skyline"):
            self.asset(slide, "bg/raw_team_skyline", 0, 262, 960, 278, alpha=8)

    def person_column(self, slide, x, y, w, name, role, bullets, photo=None, photo_h=230):
        """팀 장표 1열: 블루 세로선 + 이름(16B) + 직함(블루) + 불릿 + 하단 흑백 사진."""
        self.rect(slide, x, y, 1.5, 300, gradient=(C["blue_label"], C["blue_label"], 90))
        _gradient(slide.shapes[-1], C["blue_label"], C["blue_label"], 90, a1=90, a2=0)
        self.text(slide, x + 10, y, w - 10, 20, name, 16, "bold", C["text"], check=False)
        self.text(slide, x + 10, y + 22, w - 10, 18, role, 12, "bold", C["blue"], check=False)
        self.bullets(slide, x + 10, y + 56, w - 14, bullets, size=10.5, color=C["text"], gap=1.25)
        self.portrait(slide, x + w / 2, H, photo_h, photo, glow=False)

    # ── 아이소메트릭 일러스트 (편집 가능한 벡터 도형) ──────────────────
    def iso_box(self, slide, ox, oy, s, w=1.0, d=1.0, h=1.0, palette="blue", line="FFFFFF"):
        """아이소메트릭 박스. (ox, oy) = 윗면 뒤쪽 꼭짓점이 아닌 '바닥 중심' 기준점. s = 단위 크기(pt)."""
        top_c, left_c, right_c = ISO[palette] if isinstance(palette, str) else palette
        c30, s30 = math.cos(math.radians(30)), 0.5

        def P(x, y, z):
            return (ox + (x - y) * c30 * s, oy + (x + y) * s30 * s - z * s)
        x0, y0 = -w / 2, -d / 2
        x1, y1 = w / 2, d / 2
        top = [P(x0, y0, h), P(x1, y0, h), P(x1, y1, h), P(x0, y1, h)]
        left = [P(x0, y1, 0), P(x1, y1, 0), P(x1, y1, h), P(x0, y1, h)]
        right = [P(x1, y0, 0), P(x1, y1, 0), P(x1, y1, h), P(x1, y0, h)]
        self.poly(slide, left, left_c, line=line, line_w=0.4)
        self.poly(slide, right, right_c, line=line, line_w=0.4)
        return self.poly(slide, top, top_c, line=line, line_w=0.4)

    def iso_plate(self, slide, cx, cy, size, palette="white", h=0.08):
        """얇은 바닥판."""
        return self.iso_box(slide, cx, cy, size, 1, 1, h, palette)

    def illo(self, slide, kind, cx, cy, size, vector=False):
        """일러스트. 원본 에셋(ILLO_ASSET)이 있으면 그것을, 없거나 vector=True면 벡터 아이소메트릭을 그린다.
        (cx, cy) = 중심, size = 폭(pt). kind = scatter·blocked·stack·database·platform·report·growth·network·
        funnel·review·folder·coins·infra·doc_pile·monitor (마지막 6개는 원본 에셋 전용)."""
        name = ILLO_ASSET.get(kind)
        if not vector and name and asset_path(name):
            pic = self.asset(slide, name, cx, cy, w=size, center=True)
            if kind == "blocked":
                self.x_mark(slide, cx, cy, size * 0.88)
            return pic
        return self._illo_vector(slide, kind, cx, cy, size)

    def _illo_vector(self, slide, kind, cx, cy, size):
        """미리 조합한 일러스트. kind:
        scatter  — 흩어진 블록(구조화 안 된 경험)      stack   — 층층이 쌓인 데이터(구조화)
        database — 원통형 DB(데이터 자산)               blocked — stack + 큰 ✕ (데이터 부재)
        platform — 플랫폼 위 데이터 큐브(BM 가운데)      report  — 기울어진 리포트 카드(검증 리포트)
        growth   — 계단식 상승 블록(매출/성장)          network — 연결된 큐브 네트워크(인재풀/매칭)
        (cx, cy) = 일러스트 중심, size = 대략 폭(pt)."""
        u = size / 6.0
        if kind == "scatter":
            self.iso_plate(slide, cx, cy + u * 0.8, u * 4.2, "white", h=0.05)
            spots = [(-1.7, -0.6, "blue", 0.55), (0.9, -1.1, "cyan", 0.5), (1.6, 0.6, "blue", 0.6),
                     (-0.4, 0.5, "deep", 0.7), (-1.9, 0.9, "cyan", 0.45), (0.5, 1.5, "white", 0.5),
                     (-0.6, -1.5, "white", 0.42)]
            for (dx, dy, pal, sc) in spots:
                px = cx + (dx - dy) * 0.866 * u
                py = cy + u * 0.8 + (dx + dy) * 0.5 * u
                self.iso_box(slide, px, py, u * sc * 1.4, 1, 1, 1, pal)
            return
        if kind in ("stack", "blocked"):
            pals = ["cyan", "blue", "deep", "navy"]
            for i, pal in enumerate(pals):
                self.iso_box(slide, cx, cy + u * 1.5 - i * u * 0.72, u * 2.4, 1, 1, 0.22, pal)
            if kind == "blocked":
                L = size * 0.62
                for ang in (45, -45):
                    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(cx - L / 2),
                                                 Pt(cy - L * 0.07), Pt(L), Pt(L * 0.14))
                    bar.adjustments[0] = 0.2
                    bar.rotation = ang
                    bar.fill.solid()
                    bar.fill.fore_color.rgb = rgb(C["red_x"])
                    _no_line(bar)
                    _shadow(bar, blur=6, dist=2, alpha=25, color="7A0000")
            return
        if kind == "database":
            for i in range(3):
                yy = cy + u * 1.1 - i * u * 1.05
                body = slide.shapes.add_shape(MSO_SHAPE.CAN, Pt(cx - u * 1.6), Pt(yy - u * 0.9),
                                              Pt(u * 3.2), Pt(u * 1.5))
                body.adjustments[0] = 0.32
                _gradient(body, "6EDDD6" if i == 1 else "6FC2DC", "0E7FA5" if i != 1 else "2FB1AA", 0)
                body.line.color.rgb = rgb("FFFFFF")
                body.line.width = Pt(0.6)
            self.glow(slide, cx, cy, u * 2.6, "4FD6CF", 0.35)
            return
        if kind == "platform":
            self.glow(slide, cx, cy + u * 0.6, u * 3.4, "1E9BC4", 0.35)
            for r_, col, a in ((2.6, "CBE9F3", 90), (2.0, "9ED6E8", 90), (1.35, "1E9BC4", 100)):
                e = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(cx - r_ * u), Pt(cy + u * 1.2 - r_ * u * 0.5),
                                           Pt(2 * r_ * u), Pt(r_ * u))
                _alpha_fill(e, col, a)
                e.line.color.rgb = rgb("FFFFFF")
                e.line.width = Pt(0.8)
            self.iso_box(slide, cx, cy + u * 1.2, u * 1.25, 1, 1, 1.4, "deep")
            for dx, dy, pal in ((-2.3, -0.4, "cyan"), (2.2, -0.9, "blue"), (1.9, 1.0, "cyan"), (-1.8, 1.4, "white")):
                self.iso_box(slide, cx + dx * u, cy + dy * u, u * 0.55, 1, 1, 1, pal)
            return
        if kind == "report":
            for k, (dx, dy, rot) in enumerate(((-0.6, 0.3, -8), (0.4, -0.2, 6))):
                cw, ch = u * 3.0, u * 3.8
                r = self.rect(slide, cx + dx * u - cw / 2, cy + dy * u - ch / 2, cw, ch, fill="FFFFFF", radius=6)
                r.rotation = rot
                _shadow(r, blur=10, dist=3, alpha=20)
                if k == 1:
                    for j in range(4):
                        ln = self.rect(slide, cx + dx * u - cw / 2 + u * 0.4, cy + dy * u - ch / 2 + u * (0.6 + j * 0.65),
                                       cw * (0.7 if j else 0.45), u * 0.22,
                                       fill=C["blue_label"] if j == 0 else "D5DBE8", radius=1)
                        ln.rotation = rot
            self.number_badge(slide, cx + u * 1.5, cy + u * 1.4, "✓", r=u * 0.7)
            return
        if kind == "growth":
            for i, (pal, hh) in enumerate((("blue", 0.6), ("blue", 1.1), ("deep", 1.7), ("navy", 2.4))):
                self.iso_box(slide, cx + (i - 1.5) * u * 1.1, cy + u * 1.4 - (i - 1.5) * u * 0.25,
                             u * 0.9, 1, 1, hh, pal)
            return
        if kind == "network":
            nodes = [(-2, -0.6), (0, -1.3), (2, -0.5), (-1.2, 1), (1.1, 1.1), (0, 0)]
            for i, (ax, ay) in enumerate(nodes):
                for bx, by in nodes[i + 1:]:
                    if abs(ax - bx) + abs(ay - by) < 3:
                        self.line(slide, cx + ax * u, cy + ay * u, cx + bx * u, cy + by * u, color="9ED6E8", w=0.8)
            for i, (ax, ay) in enumerate(nodes):
                self.iso_box(slide, cx + ax * u, cy + ay * u + u * 0.3, u * (0.75 if i == 5 else 0.5), 1, 1, 1,
                             "deep" if i == 5 else ("cyan" if i % 2 else "blue"))
            return
        raise ValueError(kind)

    def illo_slot(self, slide, x, y, w, h, label="일러스트"):
        """원본 에셋을 넣을 자리 표시(점선). 최종본에 남기지 말 것."""
        r = self.rect(slide, x, y, w, h, fill=None, radius=10, line="AEB8D0", line_w=0.75)
        _line_dash(r.line, "dash")
        self.text(slide, x, y, w, h, f"[{label}]", 9, "regular", C["muted"], align="center",
                  anchor="middle", check=False)
        self._warn(f"자리표시 '{label}'가 남아 있음 → 원본 에셋으로 교체")

    def save(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self.prs.save(path)
        return path


# ═════════════════════════════════════════════════════════════
# 8. 내부 유틸
# ═════════════════════════════════════════════════════════════
def _fmt(v):
    return f"{v:g}" if isinstance(v, (int, float)) else str(v)


def _set_ea_font(run, name):
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", name)


def _cell_border(cell, color="000000", w=0.75):
    tcPr = cell._tc.get_or_add_tcPr()
    for edge in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = tcPr.find(qn(edge))
        if ln is None:
            ln = etree.SubElement(tcPr, qn(edge))
        ln.set("w", str(Pt(w)))
        for ch in list(ln):
            ln.remove(ch)
        sf = etree.SubElement(ln, qn("a:solidFill"))
        etree.SubElement(sf, qn("a:srgbClr"), {"val": color})
