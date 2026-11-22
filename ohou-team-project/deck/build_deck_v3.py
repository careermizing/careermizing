"""오늘의집 IMC 발표자료 3차 — 레퍼런스 덱(아르르·프로시드) 형식 + IR 컴포넌트(ir_kit).

실행:  python3 ohou-team-project/deck/build_deck_v3.py
출력:  ohou-team-project/deck/오늘의집_IMC_발표_3차.pptx

형식(레퍼런스): 좌상단 섹션 태그 · 가운데 정렬 주장형 제목(핵심 구절 하이라이트) · 블록 위 캡슐 헤더 ·
               하단 결론 바 · 다크 프로그램 상세 · IMC 매트릭스 · 여정표 · 도넛 예산
보정(1차 문제): 고정 그리드(좌우 40pt, 3열/2열/4열), 콘텐츠 영역 y=112~500을 꽉 채움, 장표 간 같은 요소는 같은 y
좌표 단위 pt(960×540). 시안 이미지·목업 자리는 비워 둠.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "imc-slide-design", "scripts"))
import ir_kit  # noqa: E402
from ir_kit import C, Deck, W, H, _line_dash, text_width  # noqa: E402

OUT = os.path.join(HERE, "오늘의집_IMC_발표_3차.pptx")
TEAM = "[조 이름]"
d = Deck()

# ── 그리드·색 ────────────────────────────────────────────────────────
L, CW = 40, 880
RX = L + CW
CT = 112            # 콘텐츠 시작 (제목 한 줄 기준)
CB = 500            # 콘텐츠 끝 (결론 바 없을 때)
CY = 458            # 결론 바 y (있을 때 콘텐츠 끝은 446)
G3 = 16
W3 = (CW - 2 * G3) / 3
X3 = [L + i * (W3 + G3) for i in range(3)]
W2 = (CW - 20) / 2
X2 = [L, L + W2 + 20]
W4 = (CW - 3 * 14) / 4
X4 = [L + i * (W4 + 14) for i in range(4)]

PRI, DEEP, LBL, MIST, INK, TXT, MUTE = "0F86AB", "0B5A73", "1E9BC4", "E3F4F9", "111111", "3A3F42", "8A9094"
BG, DARK, ALERT = "F5F6F4", "1F272A", "C62828"
GRAD = ("0E7FA5", "34ACD4")

PROG = [("01", "장면 사연함", "발견"), ("02", "장면 밸런스게임", "선택"), ("03", "장면 키트", "구매"), ("04", "장면 집들이", "공유")]
PARTS = ["찾는 곳과 사는 곳", "다른 곳에서 사는 이유", "상품 대신 장면", "사연에서 집들이까지", "투자와 증명"]
page = [0]


# ── 레퍼런스 형식 골격 ────────────────────────────────────────────────
def base(section="", dark=False, number=True):
    s = d.prs.slides.add_slide(d._blank)
    d._slide_idx += 1
    d.rect(s, 0, 0, W, H, fill=DARK if dark else BG)
    if section:
        d.text(s, L, 22, 300, 14, f"{section}  |", 11, "bold", "8DCFE4" if dark else PRI, check=False)
    d.text(s, RX - 260, 22, 260, 14, "OHOUSE  ·  IMC PROPOSAL", 9, "semibold", "5F7A84" if dark else "A3A9AD",
           align="right", check=False)
    if number:
        page[0] += 1
        d.text(s, RX - 40, 514, 40, 12, str(page[0]), 10, "semibold", "5F7A84" if dark else MUTE, align="right",
               check=False)
    s._dark = dark
    return s


def title(s, text, y=46, size=24):
    """가운데 정렬 주장형 제목. 한 줄 원칙(넘으면 경고)."""
    dark = getattr(s, "_dark", False)
    ir_kit.HL_COLOR = "0E7FA5" if dark else "C9ECF5"
    tw = text_width(text, size, "bold")
    if tw > CW:
        d._warn(f"제목 한 줄 초과({tw:.0f}pt): {text[:30]}")
    d.text(s, L, y, CW, 34, text, size, "bold", "FFFFFF" if dark else INK, align="center", check=False)
    ir_kit.HL_COLOR = "C9ECF5"
    return y + 34


def hpill(s, x, y, w, text, style="grad", h=26, size=13):
    """블록 위 캡슐 헤더 (레퍼런스 형식)."""
    if style == "grad":
        d.rect(s, x, y, w, h, radius=h / 2, gradient=GRAD)
        c = "FFFFFF"
    elif style == "deep":
        d.rect(s, x, y, w, h, radius=h / 2, fill=DEEP)
        c = "FFFFFF"
    elif style == "dark":
        d.rect(s, x, y, w, h, radius=h / 2, fill="3F4447")
        c = "FFFFFF"
    else:  # light
        d.rect(s, x, y, w, h, radius=h / 2, fill="E2E5E7")
        c = TXT
    d.text(s, x, y, w, h, text, size, "bold", c, align="center", anchor="middle", check=False)


def callout(s, text, y=CY, h=42, size=16):
    """하단 결론 바 (레퍼런스: 연회색 바 + 핵심 구절 강조)."""
    d.rect(s, L, y, CW, h, radius=8, fill="E3E6E8")
    d.text(s, L + 20, y, CW - 40, h, text, size, "bold", INK, align="center", anchor="middle", check=False)


def src(s, text, y=508):
    d.text(s, L, y, CW - 60, 12, text, 9, "regular", MUTE, check=False)


def note(s, text):
    s.notes_slide.notes_text_frame.text = text


def slot(s, x, y, w, h, label, dark=False, prefix=True, label_y=None):
    r = d.rect(s, x, y, w, h, fill="F7FAFB" if not dark else "26353A", radius=10,
               line="9ED6E8" if not dark else "3E5A63", line_w=1)
    _line_dash(r.line, "dash")
    ly = (y + h / 2 - 20) if label_y is None else label_y
    d.text(s, x + 8, ly, w - 16, 40, (f"[ 기획 시안 ]\n{label}" if prefix else label), 10.5, "regular",
           "8A9AA0" if not dark else "7FA9B8", align="center", anchor="middle", line_spacing=1.3, check=False)
    return r


def phone(s, cx, y, w, label):
    h = w * 2.0
    d.rect(s, cx - w / 2, y, w, h, fill="FFFFFF", radius=w * 0.16, line="1C2A30", line_w=2.2, shadow=True)
    d.rect(s, cx - w * 0.15, y + 6, w * 0.3, 4, fill="1C2A30", radius=2)
    d.rect(s, cx - w / 2 + 7, y + 16, w - 14, h - 26, fill="F3F7F8", radius=w * 0.09)
    d.text(s, cx - w / 2 + 10, y + 16, w - 20, h - 26, f"[ 목업 ]\n{label}", 9, "regular", "8A9AA0",
           align="center", anchor="middle", line_spacing=1.3, check=False)


def divider(idx, head, question, pages):
    s = base(number=False)
    d.rect(s, 0, 0, W, H, gradient=("0D5C74", "083F50", 90))
    d._network(s, 560, 50, 380, 290, seed=idx + 3, n=22)
    d.text(s, RX - 330, 320, 330, 110, pages, 80, "bold", "1A7690", align="right", check=False)
    d.text(s, L, 176, 400, 20, f"PART {'ABCDE'[idx]}", 14, "bold", "8DCFE4", check=False)
    d.text(s, L, 200, 640, 50, head, 36, "bold", "FFFFFF", check=False)
    d.rect(s, L, 260, 45, 2, fill="8DCFE4")
    d.text(s, L, 276, 500, 50, question, 16, "regular", "CFE7EF", line_spacing=1.35)
    gw = (CW - 4 * 8) / 5
    for i, p in enumerate(PARTS):
        x = L + i * (gw + 8)
        cur = i == idx
        d.rect(s, x, 470, gw, 28, radius=14, fill="1E9BC4" if cur else None, line=None if cur else "3E8199", line_w=0.75)
        d.text(s, x, 470, gw, 28, f"{'ABCDE'[i]}  {p}", 11, "bold" if cur else "medium",
               "FFFFFF" if cur else "8DB9C7", align="center", anchor="middle", check=False)


def card_head(s, x, y, w, text, size=16, color=INK):
    d.text(s, x, y, w, 22, text, size, "bold", color, align="center", check=False)


def dotline(s, x, y, w):
    d.line(s, x + 18, y, x + w - 18, y, color="C9CDD3", dash="sysDot")


# ══ 표지 ══════════════════════════════════════════════════════════
s = base(number=False)
d.rect(s, 0, 0, W, H, gradient=("0E6A87", "084B5E", 135))
d.rect(s, 556, 0, 404, H, fill="0B5A73", alpha=60)
d._network(s, 560, 300, 400, 240, seed=11, n=22)
d.text(s, 56, 150, 480, 18, "OHOUSE  ·  IMC CAMPAIGN PROPOSAL", 12, "bold", "8DCFE4", check=False)
d.text(s, 56, 178, 480, 96, "오늘의집에서 **찾고**,\n오늘의집에서 **사는** 이유", 34, "medium", "FFFFFF", line_spacing=1.2)
d.rect(s, 56, 282, 45, 2, fill="8DCFE4")
d.text(s, 56, 298, 460, 50, "〈우리 집의 다음 장면〉\n탐색에서 결제까지 잇는 IMC 캠페인 제안", 17, "regular", "DDF0F6", line_spacing=1.4)
d.text(s, 56, 470, 460, 16, f"{TEAM}  ·  2026.12.01", 12, "semibold", "BCE3EF", check=False)
d.text(s, 56, 490, 460, 14, "※ 팀이 작성한 가상 RFP에 대한 제안입니다", 10, "regular", "8DCFE4", check=False)
phone(s, 690, 70, 120, "표지 키비주얼\n앱 화면 목업")
phone(s, 830, 120, 100, "장면 키트\n화면 목업")

# ══ Executive Summary (레퍼런스: 좌 라벨 열 + 우 한 문장, 마지막 IMC 행) ════
s = base("Executive Summary")
title(s, "탐색 1위 플랫폼이 ==결제까지 가져오는 방법==을 제안합니다")
rows = [("문제 발견", "오늘의집에서 발견한 상품도, 일부는 {{쿠팡·네이버에서 결제}}됩니다."),
        ("원인 검증", "가격·구매 습관·배송 혜택이 {{함께 작용}}해 구매처가 바뀝니다."),
        ("구매 기회", "오늘의집 구매자 61%는 {{실사용 사진·후기}}를 구매 이유로 꼽았습니다."),
        ("전략", "단품이 아니라 {{'내 집의 공간 변화'}}를 구매 단위로 제안합니다.")]
lw = 150
for i, (k, v) in enumerate(rows):
    y = CT + i * 62
    d.rect(s, L, y, lw, 52, radius=8, fill="7FA9B8" if i < 3 else LBL)
    d.text(s, L, y, lw, 52, k, 15, "bold", "FFFFFF", align="center", anchor="middle", check=False)
    d.card(s, L + lw + 10, y, CW - lw - 10, 52, "white", radius=10)
    d.text(s, L + lw + 30, y, CW - lw - 50, 52, v, 16, "medium", INK, anchor="middle", check=False)
y = CT + 4 * 62
d.rect(s, L, y, lw, CB - y, radius=8, gradient=("0B5A73", "0E7FA5"))
d.text(s, L, y, lw, CB - y, "IMC", 18, "bold", "FFFFFF", align="center", anchor="middle", check=False)
d.card(s, L + lw + 10, y, 250, CB - y, "outline", radius=10)
d.text(s, L + lw + 10, y + 26, 250, 14, "BIG IDEA", 10.5, "bold", LBL, align="center", check=False)
d.text(s, L + lw + 10, y + 44, 250, 60, "우리 집의\n다음 장면", 22, "bold", INK, align="center", line_spacing=1.2)
pw = (CW - lw - 10 - 250 - 10 - 10) / 2
ph_ = (CB - y - 10) / 2
for k, (no, nm, st) in enumerate(PROG):
    bx = L + lw + 10 + 250 + 10 + (k % 2) * (pw + 10)
    by = y + (k // 2) * (ph_ + 10)
    d.card(s, bx, by, pw, ph_, "white", radius=10)
    d.tag(s, bx + 16, by + ph_ / 2 - 11, 46, st, "grad" if k == 2 else "blue", h=22, size=11)
    d.text(s, bx + 74, by, pw - 84, ph_, f"**{nm}**\n[[PROGRAM {no}]]", 14.5, "medium", INK, anchor="middle",
           line_spacing=1.25, check=False)

# ══ INDEX ═════════════════════════════════════════════════════════
s = base()
d.text(s, 0, 58, W, 30, "|   INDEX   |", 22, "bold", PRI, align="center", check=False)
toc = [("찾는 곳과\n사는 곳", ["발견과 구매의 단절", "구매처를 정하는 순간"]),
       ("다른 곳에서\n사는 이유", ["원인 가설과 검증", "오늘의집에서 사는 이유"]),
       ("상품 대신\n장면", ["구매 가치 재정의", "BIG IDEA"]),
       ("사연에서\n집들이까지", ["프로그램 4종", "채널·여정·실행 계획"]),
       ("투자와\n증명", ["예산 배분", "KPI·검증 설계"])]
cw5 = (CW - 4 * 14) / 5
for i, (t, items) in enumerate(toc):
    x = L + i * (cw5 + 14)
    d.text(s, x, 118, cw5, 30, f"0{i + 1}", 24, "bold", LBL, align="center", check=False)
    d.rect(s, x, 156, cw5, 70, radius=10, gradient=GRAD if i != 3 else ("0B5A73", "0E7FA5"))
    d.text(s, x, 156, cw5, 70, t, 16, "bold", "FFFFFF", align="center", anchor="middle", line_spacing=1.2, check=False)
    for j, it in enumerate(items):
        y = 240 + j * 56
        d.card(s, x, y, cw5, 46, "white", radius=10)
        d.text(s, x, y, cw5, 46, it, 13.5, "medium", INK, align="center", anchor="middle", check=False)
    d.text(s, x, 360, cw5, 14, f"PART {'ABCDE'[i]}", 10, "bold", MUTE, align="center", check=False)
d.rect(s, L, 400, CW, 100, radius=12, fill="E3E6E8")
d.text(s, L + 30, 400, CW - 60, 100,
       "자료 표기  ·  [[확인된 사실]] 공개 자료  |  [[팀 관찰]] 자체 설문(n=51)·인터뷰(n=5)  |  [[전략적 해석]] 팀의 판단  |  [[캠페인 제안]] 가상 실행안\n"
       "모든 화면·이미지는 기획 시안이며, 수치에는 장표 하단에 출처와 표본을 적었습니다.", 13, "medium", TXT,
       align="center", anchor="middle", line_spacing=1.6, check=False)

# ══ PART A ════════════════════════════════════════════════════════
divider(0, "찾는 곳과 사는 곳이 다릅니다", "발견과 구매가 갈라지는 사례는 무엇이고, 여정의 어디에서 일어나는가?", "A")

# 01 ─────────────
s = base("문제 발견")
title(s, "오늘의집에서 찾았는데, ==결제는 왜 다른 곳에서== 했을까요?")
gw_ = 34
w3b = (CW - 2 * gw_) / 3
xs = [L + i * (w3b + gw_) for i in range(3)]
heads = [("① 발견  ·  오늘의집", "grad"), ("② 비교  ·  네이버", "grad"), ("③ 결제  ·  쿠팡", "dark")]
labels = ["오늘의집 집들이 화면\n(책상·가구 디자인)", "네이버 검색 결과 화면\n(같은 상품 가격 비교)", "쿠팡 상품·결제 화면"]
caps = ["집들이 콘텐츠에서\n{{책상·가구 디자인}}을 참고", "같은 상품을 검색해\n{{가격·조건}}을 다시 비교",
        "실제 가격 차이와\n**익숙한 배송**으로 결제"]
for i, x in enumerate(xs):
    hpill(s, x, CT, w3b, heads[i][0], heads[i][1])
    d.card(s, x, CT + 36, w3b, 410 - CT - 36 + 36, "grey" if i == 2 else ("outline" if i == 0 else "white"))
    phone(s, x + w3b / 2, CT + 52, 104, labels[i])
    d.text(s, x + 10, 384, w3b - 20, 44, caps[i], 14.5, "medium", INK, align="center", line_spacing=1.3)
    if i < 2:
        d.chevron(s, x + w3b + 5, 250, 24, 48)
callout(s, "문제는 집을 보여주지 못하는 것이 아니라, {{발견이 구매로 이어지는 순간}}입니다")
src(s, "팀 관찰 | 고객 인터뷰 P1 사례 (n=5 중 1명) — 전체 이용자 행동을 대표하지 않음")
note(s, "오늘의집의 문제는 집을 보여주지 못하는 것이 아닙니다. 발견에서 구매로 연결되는 순간을 더 강하게 만들어야 합니다.")

# 02 ─────────────
s = base("문제 발견")
title(s, "오늘의집은 ==구매·설치·시공까지== 연결하는 플랫폼으로 확장 중입니다")
d.kpi(s, L, CT, 250, 334, "2025 매출", "약 3,215억 원", highlight=True, value_size=26)
d.illo(s, "growth", L + 125, CT + 150, 120, vector=True)
d.text(s, L, CT + 296, 250, 18, "전년 대비 +11.7%", 14, "bold", "FFFFFF", align="center", check=False)
rx, rw = L + 266, CW - 266
steps = [("콘텐츠·커뮤니티", "집들이·사진·노하우로\n공간을 보여줌", "stack"), ("상품 탐색", "공간 속 상품 태그로\n상품을 찾음", "scatter"),
         ("커머스 구매", "오늘의집에서\n결제", "report"), ("배송·설치 / 시공", "일부 상품·지역의\n배송·설치, 시공", "platform")]
sw = (rw - 3 * 10) / 4
for i, (t, c, ill) in enumerate(steps):
    x = rx + i * (sw + 10)
    hpill(s, x, CT, sw, t, "grad" if i < 3 else "deep")
    d.card(s, x, CT + 36, sw, 298, "white")
    d.illo(s, ill, x + sw / 2, CT + 130, 96, vector=True)
    d.text(s, x + 8, CT + 220, sw - 16, 44, c, 13.5, "medium", INK, align="center", line_spacing=1.3)
    d.text(s, x, CT + 290, sw, 20, f"STEP {i + 1}", 11, "bold", LBL, align="center", check=False)
callout(s, "이 확장을 뒷받침할 {{'구매 경험'}}은 지금 충분한가요?")
src(s, "확인된 사실 | 오늘의집 공식 2025 실적 발표(ohstory.io) · 시공·배송 제공 범위는 상품·지역마다 다름")

# 03 ─────────────
s = base("문제 발견")
title(s, "리빙 상품을 ==찾는 채널과 결제하는 채널==은 서로 경쟁하고 있습니다")
cols = [("오늘의집", "grad", ["실제 집 콘텐츠·상품 연결", "공간 맥락, 실사용 사진·후기", "발견의 출발점"]),
        ("네이버", "dark", ["검색·가격 비교", "최저가·조건 비교", "비교 단계"]),
        ("쿠팡", "dark", ["구매 습관·멤버십·빠른 배송", "익숙함, 배송 속도", "결제 단계"]),
        ("취향 플랫폼", "dark", ["디자인·브랜드 큐레이션", "취향에 맞는 상품 발견", "발견 단계"])]
rl = ["대표 강점", "기대하는 구매 가치", "여정에서의 위치"]
lab_w = 128
ccw = (CW - lab_w - 10 - 3 * 10) / 4
cx0 = L + lab_w + 10
rh = (CY - 12 - (CT + 36)) / 3
for r_, lab in enumerate(rl):
    y = CT + 36 + r_ * rh
    d.rect(s, L, y + rh / 2 - 17, lab_w, 34, radius=17, fill="E2E5E7")
    d.text(s, L, y + rh / 2 - 17, lab_w, 34, lab, 13, "bold", TXT, align="center", anchor="middle", check=False)
for i, (nm, st, vals) in enumerate(cols):
    x = cx0 + i * (ccw + 10)
    hpill(s, x, CT, ccw, nm, st)
    d.card(s, x, CT + 36, ccw, CY - 12 - CT - 36, "outline" if i == 0 else "mid")
    for r_, v in enumerate(vals):
        y = CT + 36 + r_ * rh
        d.text(s, x + 10, y, ccw - 20, rh, v, 15, "bold" if (i == 0 and r_ == 2) else ("semibold" if i == 0 else "medium"),
               PRI if i == 0 else TXT, align="center", anchor="middle", line_spacing=1.25)
        if r_ < 2:
            dotline(s, x, y + rh, ccw)
callout(s, "고객은 {{하나의 플랫폼만 쓰지 않습니다}} — 발견과 결제가 다른 곳에서 일어납니다")
src(s, "전략적 해석 | 플랫폼별 대표 포지션 기준이며 독점적 기능 구분이 아님")

# 04 ─────────────
s = base("문제 발견")
title(s, "오늘의집에서 처음 본 고객 ==12명 중 5명==은 다른 곳에서 구매했습니다")
lw4 = 520
hpill(s, L, CT, lw4, "처음 본 플랫폼에서 그대로 구매한 응답자")
hpill(s, L + lw4 + 20, CT, CW - lw4 - 20, "무엇을 의미하나", "deep")
d.card(s, L, CT + 36, lw4, CY - 12 - CT - 36, "white")
d.bars(s, L + 40, 404, lw4 - 80, 196, [
    {"cat": "오늘의집", "value": 7 / 12, "color": PRI, "inside": "58%", "top": "7/12"},
    {"cat": "네이버", "value": 8 / 11, "color": "A9DAEA", "inside": "73%", "inside_color": "0B5A73", "top": "8/11"},
    {"cat": "쿠팡", "value": 11 / 12, "color": "A9DAEA", "inside": "92%", "inside_color": "0B5A73", "top": "11/12"}],
    vmax=1.0, label_size=14)
rx = L + lw4 + 20
rw = CW - lw4 - 20
d.kpi(s, rx, CT + 36, rw, 118, "오늘의집 최초 발견 고객 중 다른 곳에서 구매", "5 / 12명", highlight=True, value_size=28)
d.card(s, rx, CT + 166, rw, CY - 12 - CT - 166, "white")
d.bullets(s, rx + 20, CT + 184, rw - 36, ["세 플랫폼 중 {{오늘의집의 일치 비율이 가장 낮음}}",
                                          "서비스 전환율이 아닌, 자체 조사의 최초 발견처–최근 구매처 일치 비율",
                                          "각 11~12명의 작은 표본, 응답자 편향 있음"], size=13.5, color=INK, gap=1.45)
callout(s, "'오늘의집에서는 안 산다'가 아니라, {{발견과 구매가 갈라지는 경우}}가 있습니다")
src(s, "팀 관찰 | 자체 2차 설문(n=51) 중 각 플랫폼 최초 발견 응답자 기준")

# 05 ─────────────
s = base("문제 발견")
title(s, "문제 지점은 결제 버튼이 아니라, ==최종 구매처를 고르는 순간==입니다")
stages = ["공간 문제 인식", "콘텐츠·상품 탐색", "후보 비교", "구매처 결정", "결제", "설치·사용"]
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
cwv = CW / 6
ramp = ["D6EEF5", "BCE3EF", None, None, "34ACD4", "0E7FA5"]
for i, st in enumerate(stages):
    x = L + i * cwv
    sh = d.rect(s, x, CT, cwv + 6, 44, shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON,
                fill=ramp[i] if ramp[i] else "FFFFFF", line=PRI if ramp[i] is None else None, line_w=1.25)
    sh.adjustments[0] = 0.3
    if ramp[i] is None:
        _line_dash(sh.line, "dash")
    d.text(s, x + 18, CT, cwv - 24, 44, st, 13, "bold", "FFFFFF" if i >= 4 else INK, align="center",
           anchor="middle", check=False)
d.text(s, L + 2 * cwv, CT + 50, 2 * cwv, 16, "▲ 이동이 일어나는 구간", 11.5, "bold", ALERT, align="center", check=False)
cy0 = CT + 78
ch_ = CY - 12 - cy0
d.card(s, X3[0], cy0, W3, ch_, "white")
d.card(s, X3[1], cy0, W3, ch_, "outline")
d.card(s, X3[2], cy0, W3, ch_, "grey")
card_head(s, X3[0], cy0 + 18, W3, "발견한 곳")
card_head(s, X3[1], cy0 + 18, W3, "구매처를 정하는 순간")
card_head(s, X3[2], cy0 + 18, W3, "결제한 곳")
d.illo(s, "stack", X3[0] + W3 / 2, cy0 + 112, 110, vector=True)
d.text(s, X3[1], cy0 + 54, W3, 40, "구매처 이동", 28, "bold", ALERT, align="center", check=False)
d.illo(s, "scatter", X3[1] + W3 / 2, cy0 + 132, 96, vector=True)
d.text(s, X3[1] + 10, cy0 + 190, W3 - 20, 40, "결제창 이탈이 아니라,\n**구매 전에 다른 앱을 여는 행동**", 14, "semibold", INK,
       align="center", line_spacing=1.3)
d.illo(s, "report", X3[2] + W3 / 2, cy0 + 112, 100, vector=True)
d.text(s, X3[0] + 10, cy0 + 190, W3 - 20, 40, "{{오늘의집}}\n집들이·상품 탐색", 14, "semibold", INK, align="center", line_spacing=1.3)
d.text(s, X3[2] + 10, cy0 + 190, W3 - 20, 40, "**쿠팡·네이버**\n가격·배송 재비교 후 결제", 14, "semibold", "404040", align="center",
       line_spacing=1.3)
callout(s, "고객은 탐색 후 {{가격·혜택·배송을 다시 비교}}하고 구매처를 정합니다")
src(s, "팀 관찰 | 고객 인터뷰 n=5 · 서비스 내부 클릭스트림은 실측하지 않음 ('결제 페이지 이탈률'로 해석하지 않음)")

# ══ PART B ════════════════════════════════════════════════════════
divider(1, "왜 다른 곳에서 결제하는가", "구매처 이동의 원인을 검증하고, 오늘의집에서 구매하는 예외를 찾습니다.", "B")

# 06 ─────────────
s = base("원인 검증")
title(s, "구매처를 바꾸는 원인으로 ==세 가지 구매 판단==을 가정했습니다")
hyp = [("H1. 구매 습관", "\"그냥 원래 쓰던 앱에서\n사면 되지\"", "쇼핑 앱 이용 · 인터뷰", "scatter"),
       ("H2. 가격", "\"같은 물건인데\n다른 데가 더 싸네\"", "가격 인식 · 실제 비교 경험", "growth"),
       ("H3. 배송·혜택", "\"이미 멤버십도 있고\n더 빨리 오네\"", "배송 이유 · 멤버십 · 인터뷰", "network")]
for i, x in enumerate(X3):
    hpill(s, x, CT, W3, hyp[i][0])
    d.card(s, x, CT + 36, W3, 296, "white")
    d.illo(s, hyp[i][3], x + W3 / 2, CT + 118, 110, vector=True)
    d.text(s, x + 10, CT + 186, W3 - 20, 14, "고객의 판단", 11, "bold", MUTE, align="center", check=False)
    d.text(s, x + 10, CT + 206, W3 - 20, 50, hyp[i][1], 17, "bold", INK, align="center", line_spacing=1.3)
    dotline(s, x, CT + 274, W3)
    d.text(s, x + 10, CT + 286, W3 - 20, 14, "조사 방법", 11, "bold", MUTE, align="center", check=False)
    d.text(s, x + 10, CT + 304, W3 - 20, 18, hyp[i][2], 13.5, "semibold", PRI, align="center", check=False)
d.rect(s, L, CT + 344, CW, CB - CT - 344, radius=10, fill="E3E6E8")
d.text(s, L + 24, CT + 344, CW - 48, CB - CT - 344,
       "**함께 확인한 대안 가설**     이사할 때만 쓰는 앱  ·  구경 전용 앱  ·  가입/결제 UI 불편  ·  첫 구매 경험 부재  ·  내 집 사용 확신 부족",
       13.5, "medium", TXT, align="center", anchor="middle", check=False)

# 07 ─────────────
s = base("원인 검증")
title(s, "==가격·익숙함·배송 혜택==이 함께 작용해 구매처 이동을 만듭니다")
rc = [("익숙한 앱", "49%", "주 이용 쇼핑 앱이 쿠팡", "'다른 앱에서 사는 게\n익숙해서' 30%", "표본 51명, 문항별 분모 다름"),
      ("가격", "42%", "'오늘의집이 비쌀 것 같다'", "인터뷰 5명 중 3명이 비교 후\n쿠팡의 가격 우위 언급", "인식과 실제 가격 차이 모두 존재"),
      ("배송·혜택", "86%", "멤버십 1개 이상 보유", "구매처 변경자 21명 중 7명이\n배송을 이유로 선택", "원인 중복 가능, 인과 미검증")]
for i, x in enumerate(X3):
    hpill(s, x, CT, W3, rc[i][0])
    d.card(s, x, CT + 36, W3, 262, "white")
    d.text(s, x, CT + 56, W3, 50, rc[i][1], 44, "bold", PRI, align="center", check=False)
    d.text(s, x, CT + 112, W3, 20, rc[i][2], 15, "semibold", INK, align="center", check=False)
    dotline(s, x, CT + 146, W3)
    d.text(s, x + 14, CT + 160, W3 - 28, 44, rc[i][3], 13.5, "medium", TXT, align="center", line_spacing=1.35)
    d.tag(s, x + 24, CT + 254, W3 - 48, "한계 · " + rc[i][4], "dark", h=24, size=10.5)
d.rect(s, L, CT + 308, CW, 28, radius=14, fill=MIST)
d.text(s, L, CT + 308, CW, 28, "반례  ·  오늘의집 구매 경험 33/51 (65%) → '첫 구매 장벽'만의 문제로 보기 어렵습니다", 13, "semibold", PRI,
       align="center", anchor="middle", check=False)
callout(s, "구매처 이동은 한 가지 오해가 아니라, {{여러 이유의 결합}}입니다")
src(s, "팀 관찰 | 자체 2차 설문(n=51), 고객 인터뷰(n=5)")

# 08 ─────────────
s = base("원인 검증")
title(s, "할 수 없는 경쟁을 인정해야, ==새로운 구매 이유==를 찾을 수 있습니다")
hpill(s, X2[0], CT, W2, "경쟁사가 이미 강한 것", "dark")
hpill(s, X2[1], CT, W2, "오늘의집이 더 강화할 것")
ph = 214
d.card(s, X2[0], CT + 36, W2, ph, "grey")
d.card(s, X2[1], CT + 36, W2, ph, "outline")
for i, t in enumerate(["단품 최저가", "멤버십 기반 빠른 배송", "매일 쓰는 구매 습관"]):
    y = CT + 56 + i * 62
    d.rect(s, X2[0] + 28, y, W2 - 56, 48, radius=10, fill="FFFFFF", alpha=55)
    d.text(s, X2[0] + 28, y, W2 - 56, 48, t, 16.5, "semibold", "404040", align="center", anchor="middle", check=False)
for i, t in enumerate(["실제 공간에서의 사용 맥락", "내 집에 맞는 선택 지원", "구매 이후 배송·설치 (적용 상품)"]):
    y = CT + 56 + i * 62
    d.rect(s, X2[1] + 28, y, W2 - 56, 48, radius=10, fill=MIST)
    d.text(s, X2[1] + 28, y, W2 - 56, 48, t, 16.5, "semibold", PRI, align="center", anchor="middle", check=False)
d.chevron(s, L + W2 - 2, CT + 118, 24, 50)
yb = CT + ph + 50
d.text(s, L, yb, 300, 18, "채택하지 않을 프레임", 13, "bold", INK, check=False)
fw = (CW - 3 * 10) / 4
for i, f_ in enumerate(["오늘의집이 사실 더 싸다", "이사하는 사람만 쓴다", "아무도 여기서 사지 않는다", "UI가 불편해서 안 산다"]):
    x = L + i * (fw + 10)
    d.rect(s, x, yb + 24, fw, 34, radius=17, fill="FFFFFF", line="D3D6DB", line_w=0.75)
    d.text(s, x, yb + 24, fw, 34, f"✕  {f_}", 13, "medium", MUTE, align="center", anchor="middle", check=False)
callout(s, "RFP는 최저가·할인 캠페인을 배제합니다 → {{가격 외의 구매 이유}}가 필요합니다")
src(s, "팀 관찰 | 구매 UI 불편 동의 약 22%, 오늘의집 구매 경험 65% (n=51)")

# 09 ─────────────
s = base("구매 기회")
title(s, "오늘의집에서 산 고객은 ==실사용 사진·후기==를 가장 큰 이유로 꼽았습니다")
d.kpi(s, L, CT, 250, CY - 12 - CT, "오늘의집 구매 이유 1위\n실사용 사진·후기 신뢰", "61%  (20/33)", highlight=True, value_size=28)
d.illo(s, "report", L + 125, CT + 170, 110, vector=True)
rx, rw = L + 266, CW - 266
hpill(s, rx, CT, rw, "오늘의집 구매 이유 (복수응답, 구매 경험자 n=33)")
d.card(s, rx, CT + 36, rw, 180, "white")
br = [("실사용 사진·후기 신뢰", 61), ("사진 속 상품 바로 구매", 27), ("단독 상품", 21), ("배송·설치", 12)]
for i, (t, v) in enumerate(br):
    y = CT + 52 + i * 38
    d.text(s, rx + 16, y, 170, 28, t, 14, "bold" if i == 0 else "medium", PRI if i == 0 else TXT, align="right",
           anchor="middle", check=False)
    d.rect(s, rx + 200, y + 6, 330 * v / 61, 18, radius=4, fill=PRI if i == 0 else "D5DBE0")
    d.text(s, rx + 208 + 330 * v / 61, y, 60, 28, f"{v}%", 14, "bold", INK, anchor="middle", check=False)
nw = (rw - 14) / 2
for k, tx in enumerate(["51명 중 **26명**은 '비슷한 집 실제 사례'나\n'공간 속 상품 한 번에 담기'를 원함\n[[표현된 선호이며 실제 구매 효과는 아님]]",
                        "인터뷰에서도 **디자인·보증·사용 이유**가\n중요한 상품은 오늘의집을 고른\n경우가 있었음"]):
    x = rx + k * (nw + 14)
    d.card(s, x, CT + 228, nw, CY - 12 - CT - 228, "white")
    d.text(s, x + 18, CT + 228, nw - 36, CY - 12 - CT - 228, tx, 13.5, "medium", INK, anchor="middle", line_spacing=1.4)
callout(s, "가격을 부정하지 않고, {{가격 외 정보가 중요해지는 구매 상황}}을 찾습니다")
src(s, "팀 관찰 | 자체 2차 설문(n=51) 중 오늘의집 구매 경험자 n=33, 고객 인터뷰 n=5")

# ══ PART C ════════════════════════════════════════════════════════
divider(2, "상품 대신 장면을 팝니다", "왜 '공간 변화'가 구매 가치가 되고, 어떤 콘셉트로 모이는가?", "C")

# 10 ─────────────
s = base("전략 도출")
title(s, "좋은 콘텐츠가 있어도, ==같은 상품은 다른 곳에서도== 살 수 있습니다")
hpill(s, X2[0], CT, W2, "지금  ·  단품을 발견하는 경로", "dark")
hpill(s, X2[1], CT, W2, "제안  ·  공간 변화를 사는 경로")
ph = CY - 12 - CT - 36
d.card(s, X2[0], CT + 36, W2, ph, "grey")
d.card(s, X2[1], CT + 36, W2, ph, "outline")
left = ["집들이 사진에서 상품 발견", "상품명 확인", "다른 앱에서 검색", "쿠팡에서 단품 결제"]
right = ["우리 집의 공간 문제", "변화 시나리오 선택", "실제 사용·조합 확인", "오늘의집에서 결제"]
step_h, step_g = 52, (ph - 32 - 4 * 52) / 3
for i in range(4):
    y = CT + 52 + i * (step_h + step_g)
    d.rect(s, X2[0] + 40, y, W2 - 80, step_h, radius=10, fill="FFFFFF", alpha=60)
    d.text(s, X2[0] + 40, y, W2 - 80, step_h, left[i], 16, "semibold", "404040", align="center", anchor="middle", check=False)
    if i == 3:
        d.rect(s, X2[1] + 40, y, W2 - 80, step_h, radius=10, gradient=GRAD)
    else:
        d.rect(s, X2[1] + 40, y, W2 - 80, step_h, radius=10, fill=MIST)
    d.text(s, X2[1] + 40, y, W2 - 80, step_h, right[i], 16, "semibold", "FFFFFF" if i == 3 else PRI, align="center",
           anchor="middle", check=False)
    if i < 3:
        d.down_arrow(s, X2[0] + W2 / 2 - 9, y + step_h + step_g / 2 - 4, 18, 9, fill="7E7E7E")
        d.down_arrow(s, X2[1] + W2 / 2 - 9, y + step_h + step_g / 2 - 4, 18, 9, fill=PRI)
d.chevron(s, L + W2 - 2, CT + 36 + ph / 2 - 25, 24, 50)
callout(s, "필요한 것은 그 장면을 {{내 집에서 만들기 위해 무엇을 살지}} 정하는 경험입니다")
src(s, "전략 가설 | 단순 상품 나열이면 방어력이 약함 — 검수된 SKU·PB/단독·협업 구성이 확보된 회차부터 실험")
note(s, "남의 집 사진을 더 보여주는 것은 발견을 돕습니다. 하지만 필요한 것은 그 장면을 내 집에서 만들기 위해 무엇을 사야 하는지까지 결정하는 경험입니다.")

# 11 ─────────────
s = base("전략 도출")
title(s, "그래서 ==‘상품’이 아닌 ‘공간 변화’==를 구매 단위로 제안합니다")
cats = [("범용 생활용품", "가격·배송·익숙함", "일반 상품 판매", "메인 제외", "grey"),
        ("디자인 소품·패브릭", "분위기·취향·연출", "집들이·사진·단독 상품", "조합의 보조 상품", "white"),
        ("공간 활용형\n가구·수납·조명", "크기·배치·사용 목적·조합", "실제 집 사례·리뷰·\n상품·일부 설치", "우선 대상", "outline"),
        ("전면 리모델링", "품질·견적·업체·일정", "일부 시공 자산", "1차 범위 제외", "grey")]
for i, (t, f_, a, j, st) in enumerate(cats):
    x = X4[i]
    hpill(s, x, CT, W4, j, "grad" if st == "outline" else ("light" if st == "white" else "dark"))
    d.card(s, x, CT + 36, W4, CY - 12 - CT - 36, st)
    d.text(s, x + 10, CT + 52, W4 - 20, 52, t, 17, "bold", PRI if st == "outline" else INK, align="center",
           anchor="middle", line_spacing=1.2)
    dotline(s, x, CT + 118, W4)
    d.text(s, x + 12, CT + 132, W4 - 24, 14, "고객이 따지는 것 (가설)", 11, "bold", MUTE, align="center", check=False)
    d.text(s, x + 12, CT + 152, W4 - 24, 44, f_, 14.5, "semibold", INK, align="center", line_spacing=1.25)
    dotline(s, x, CT + 210, W4)
    d.text(s, x + 12, CT + 224, W4 - 24, 14, "연결 가능한 오늘의집 자산", 11, "bold", MUTE, align="center", check=False)
    d.text(s, x + 12, CT + 244, W4 - 24, 44, a, 14.5, "semibold", PRI if st == "outline" else INK, align="center",
           line_spacing=1.25)
callout(s, "타깃: 지금 집의 {{특정 공간 문제를 해결하려는 사람}} (20~30대 1~2인 가구는 크리에이티브 후보)", size=15)
src(s, "근거 | 오늘의집 슬림수납장·1인용 가구 검색 증가 보도(2026) — 검색 증가가 거래액 증가를 뜻하지는 않음 · 대상 SKU는 조건 점검 후 확정")

# 12 BIG IDEA ─────
s = base(number=False)
d.rect(s, 0, 0, W, H, gradient=("0D5C74", "07475A", 90))
slot(s, 0, 0, W, H, "배경 키비주얼 — 현실적인 작은 방의 BEFORE → 변화 후 장면 (어두운 오버레이)", dark=True, label_y=470)
d.rect(s, 0, 0, W, H, fill="062F3B", alpha=55)
d.text(s, 0, 104, W, 18, "BIG IDEA", 13, "bold", "8DCFE4", align="center", check=False)
d.text(s, 0, 130, W, 70, "우리 집의 다음 장면", 56, "bold", "FFFFFF", align="center", check=False)
d.text(s, 0, 214, W, 26, "마음에 드는 집을 보는 것에서, 내가 살고 싶은 집을 만드는 것으로", 19, "medium", "DDF0F6", align="center", check=False)
pw = 180
gp = (CW - 4 * pw) / 3
for i, (no, nm, st) in enumerate(PROG):
    x = L + i * (pw + gp)
    d.rect(s, x, 286, pw, 80, radius=14, fill="FFFFFF", alpha=94 if i != 2 else 100, line=None if i != 2 else "8DCFE4", line_w=1.5)
    d.text(s, x, 300, pw, 14, f"{st}  ·  PROGRAM {no}", 10.5, "bold", LBL, align="center", check=False)
    d.text(s, x, 322, pw, 26, nm, 18, "bold", INK, align="center", check=False)
    if i < 3:
        d._fade_arrow(s, x + pw + 6, x + pw + gp - 6, 326, color="8DCFE4")
d.text(s, 0, 392, W, 20, "\"우리 집에서 바꾸고 싶은 한 장면은?\" — 발견하고, 고르고, 오늘의집에서 사고, 다시 보여줍니다", 14, "medium",
       "BCE3EF", align="center", check=False)
note(s, "이 콘셉트는 슬로건이 아니라, 고객이 다음 장면을 발견하고 선택하고 구매하고 공유하는 네 단계로 작동합니다.")

# ══ PART D ════════════════════════════════════════════════════════
divider(3, "사연에서 집들이까지", "\"우리 집에서 바꾸고 싶은 한 장면은?\" — 네 개의 프로그램을 하나의 구매 여정으로 잇습니다.", "D")

# IMC 매트릭스 (레퍼런스: 아르르 p19) ─
s = base("IMC 개요")
title(s, "네 개의 프로그램은 ==발견·선택·구매·공유==의 한 여정으로 이어집니다")
gx, gw = L, 64
px, pw_ = L + 70, 168
cx_ = [px + pw_ + 8 + k * 152 for k in range(3)]
cw_ = 146
jx = cx_[2] + cw_ + 14
jw = (RX - jx - 3 * 4) / 4
hpill(s, cx_[0], CT, cx_[2] + cw_ - cx_[0], "IMC 전략 개요", "deep")
hpill(s, jx, CT, RX - jx, "고객 여정", "deep")
for k, hd in enumerate(["채널", "타깃 특성", "목적"]):
    d.rect(s, cx_[k], CT + 32, cw_, 24, radius=4, fill="7FA9B8")
    d.text(s, cx_[k], CT + 32, cw_, 24, hd, 12, "bold", "FFFFFF", align="center", anchor="middle", check=False)
for k, hd in enumerate(["인지", "고려", "구매", "확산"]):
    d.rect(s, jx + k * (jw + 4), CT + 32, jw, 24, radius=4, fill=LBL)
    d.text(s, jx + k * (jw + 4), CT + 32, jw, 24, hd, 11.5, "bold", "FFFFFF", align="center", anchor="middle", check=False)
mat = [("발견", "장면 사연함", "바꾸고 싶은 공간 고민 수집", "숏폼 · 인스타 · 기획전 메인", "공간 고민이 있는 고객", "고민 선택 · 사례 탐색", [0]),
       ("선택", "장면 밸런스게임", "같은 방 A/B 중 방향 선택", "크리에이터 · 유튜브 · 앱 A/B 카드", "변화 방향을 못 정한 고객", "A/B 선택 → 키트 이동", [0, 1]),
       ("구매", "장면 키트", "장면을 만드는 상품 조합", "앱 기획전 · 상품 페이지", "구매를 검토하는 고객", "SKU 상세 → 결제", [1, 2]),
       ("공유", "장면 집들이", "실제 변화 후기 → 다음 고객 근거", "숏폼 · 후기 · 커뮤니티", "구매 완료 고객", "후기 · 다음 고객의 사례", [2, 3])]
ry0 = CT + 64
rh = (CB - ry0 - 3 * 8) / 4
for r_, (g, nm, desc, chn, tgt, goal, stg) in enumerate(mat):
    y = ry0 + r_ * (rh + 8)
    hot = r_ == 2
    d.rect(s, gx, y, gw, rh, radius=8, gradient=("0B5A73", "0E7FA5") if hot else None, fill=None if hot else DEEP)
    d.text(s, gx, y, gw, rh, g, 15, "bold", "FFFFFF", align="center", anchor="middle", check=False)
    d.card(s, px, y, pw_, rh, "outline" if hot else "white", radius=10)
    d.text(s, px + 8, y + 14, pw_ - 16, 20, nm, 15.5, "bold", PRI if hot else INK, align="center", check=False)
    d.text(s, px + 8, y + 40, pw_ - 16, 30, desc, 11.5, "medium", MUTE, align="center", line_spacing=1.2)
    for k, v in enumerate([chn, tgt, goal]):
        d.rect(s, cx_[k], y, cw_, rh, radius=8, fill="FFFFFF", line="E2E5E7", line_w=0.75)
        d.text(s, cx_[k] + 8, y, cw_ - 16, rh, v, 13, "semibold" if k == 2 else "medium", PRI if k == 2 else INK,
               align="center", anchor="middle", line_spacing=1.25)
    for k in range(4):
        d.rect(s, jx + k * (jw + 4), y, jw, rh, radius=6, fill="EEF1F2")
    cy_ = y + rh / 2
    xa = jx + min(stg) * (jw + 4) + jw / 2
    xb = jx + max(stg) * (jw + 4) + jw / 2
    if xb > xa:
        d.rect(s, xa, cy_ - 1.5, xb - xa, 3, fill=PRI)
    for k in stg:
        d.rect(s, jx + k * (jw + 4) + jw / 2 - 6, cy_ - 6, 12, 12, fill=PRI, shape=MSO_SHAPE.OVAL)

# 프로그램 상세 (레퍼런스: 다크 프로그램 장표) ─
def program(idx, sub, slogan, blocks, mock, kpi, extra=None):
    no, nm, st = PROG[idx]
    s = base("IMC 실행", dark=True)
    d.text(s, L, 46, 500, 14, f"PROGRAM {no}  ·  {st}", 11, "bold", "8DCFE4", check=False)
    d.text(s, L, 64, 500, 52, nm, 40, "bold", "FFFFFF", check=False)
    d.text(s, L, 118, 500, 20, sub, 15, "medium", "CFE7EF", check=False)
    sw_ = min(500, text_width(slogan, 13, "medium") + 60)
    d.rect(s, L, 148, sw_, 28, radius=14, fill="3A4A50")
    d.text(s, L, 148, sw_, 28, f"“ {slogan} ”", 13, "medium", "FFFFFF", align="center", anchor="middle", check=False)
    bw_, by0 = 500, 190
    bh_ = (CB - by0 - 2 * 10) / 3
    for i, (head, body) in enumerate(blocks):
        y = by0 + i * (bh_ + 10)
        d.card(s, L, y, bw_, bh_, "dark", radius=12)
        d.rect(s, L + 18, y + 17, 3, 18, fill="8DCFE4")
        d.text(s, L + 30, y + 14, bw_ - 50, 22, head, 15.5, "bold", "FFFFFF", check=False)
        d.text(s, L + 30, y + 42, bw_ - 50, bh_ - 48, body, 12.5, "regular", "D5E3E8", line_spacing=1.35)
    mx, mw = L + bw_ + 20, CW - bw_ - 20
    slot(s, mx, 46, mw, 340, "", dark=True, prefix=False)
    d.tag(s, mx + 14, 58, 70, "기획 시안", "blue", h=20, size=10)
    mock(s, mx, 46, mw, 340)
    d.rect(s, mx, 398, mw, CB - 398, radius=12, fill="26353A")
    d.text(s, mx + 18, 412, mw - 36, 14, "성공 지표", 11, "bold", "8DCFE4", check=False)
    d.text(s, mx + 18, 432, mw - 36, CB - 440, kpi, 13.5, "semibold", "FFFFFF", line_spacing=1.4)
    if extra:
        note(s, extra)


def mock_cards(s, x, y, w, h):
    cw_, chh = (w - 3 * 14) / 2, (h - 60 - 14) / 2
    for i, t in enumerate(["좁은 침실", "수납 부족", "재택 공간", "작은 거실"]):
        slot(s, x + 14 + (i % 2) * (cw_ + 14), y + 46 + (i // 2) * (chh + 14), cw_, chh, f"고민 카드\n{t}", dark=True, prefix=False)


def mock_ab(s, x, y, w, h):
    cw_ = (w - 3 * 14 - 20) / 2
    slot(s, x + 14, y + 46, cw_, h - 60, "A안 · 수납 중심\n선반 · 정리 도구 · 조명", dark=True, prefix=False)
    slot(s, x + 14 + cw_ + 34, y + 46, cw_, h - 60, "B안 · 휴식 중심\n낮은 테이블 · 조명 · 의자", dark=True, prefix=False)
    d.text(s, x + 14 + cw_, y + h / 2, 34, 30, "VS", 13, "bold", "8DCFE4", align="center", anchor="middle", check=False)


def mock_kit(s, x, y, w, h):
    phone(s, x + w * 0.3, y + 50, 128, "키트 상품 목록\n규격 · 선택 이유\n가격 · 배송 조건")
    phone(s, x + w * 0.72, y + 74, 112, "오늘의집\n상품 상세 · 결제")


def mock_board(s, x, y, w, h):
    cw_, chh = (w - 3 * 14) / 2, (h - 60 - 14) / 2
    for i, t in enumerate(["BEFORE · 불편", "A/B 선택 이유", "설치 · 사용", "AFTER · 완성"]):
        slot(s, x + 14 + (i % 2) * (cw_ + 14), y + 46 + (i // 2) * (chh + 14), cw_, chh, f"{i + 1}컷\n{t}", dark=True, prefix=False)


program(0, "바꾸고 싶은 공간 고민을 캠페인의 출발점으로", "당신 집에서 바꾸고 싶은 한 장면은?",
        [("숏폼·카드뉴스·기획전에서 질문을 던짐", "\"퇴근하면 가방부터 바닥에 내려놓는 방. 당신의 다음 장면은?\"\n좁은 침실 · 수납 부족 · 재택 공간 · 작은 거실 고민 카드"),
         ("고민 카드를 고르면 비슷한 집 사례로 연결", "사진 업로드 없이 선택만으로 참여. 원하면 실제 공간 사진과 고민을\n보내고, 일부 사연은 다음 단계 콘텐츠로 제작"),
         ("고른 고민이 밸런스게임·키트로 이어짐", "같은 고민 태그로 다음 프로그램과 연결. 사진·사연 재사용은 동의 필수,\n제작 혜택을 모든 참여자에게 보장하지 않음")],
        mock_cards, "고민 선택률 · 사례 탐색 진입률\n유입 후 상품 탐색률")

program(1, "같은 방, 두 가지 다음 장면 중 하나를 고름", "내 집은 A에 가까울까, B에 가까울까?",
        [("같은 공간 고민에 현실적인 두 가지 방향 제시", "예) 원룸 창가 — A 수납 중심 / B 휴식 중심\n두 안 모두 실제로 설치 가능한 상품만 연결"),
         ("크리에이터가 장점과 포기한 것까지 설명", "문제 → 우선순위 → 장점·포기한 것 → 선택 이유 → 필요한 제품\n숏폼 15~30초 · 유튜브 2~4분 · 인스타 캐러셀"),
         ("고객은 '우리 집은 A / B'를 고르고 키트로", "앱 A/B 비교 카드에서 선택 → 해당 장면 키트로 연결\n정답 투표가 아니라 내 상황에 맞는 방향 고르기")],
        mock_ab, "A/B 선택 완료율 · 선택 후 키트 클릭\n상품 후보 저장률")

program(2, "고른 장면을 만드는 상품을 오늘의집에서 결제", "고르고, 확인하고, 오늘의집에서 결제까지",
        [("공간 문제 중심으로 3~5개 상품을 조합", "'예쁜 조명 추천'이 아니라 '작은 침실 동선 확보' 같은 쓰임새 제안\n예) 6평 침실 — 좁은 수납장 · 침대 아래 수납 · 벽면 조명"),
         ("규격·선택 이유와 함께 부적합 조건까지 고지", "판매 가능한 SKU만 연결 (재고 · 규격 · 배송 · 설치 확인)\n동일 제품과 대체 제품을 구분해 표기"),
         ("필요한 상품만 골라 오늘의집에서 결제", "PB·단독·협업 전용 구성 우선 검토, 미확보 시 독점 표기 금지\n할인 묶음이 아닌 '구매 목적의 조합' — 전체 결제를 강요하지 않음")],
        mock_kit, "키트 → 상품 상세 클릭률 · SKU 구매 전환율\n구매자 수 · 거래액")

# 키트 모바일 여정 ─
s = base("Program 03")
title(s, "고객이 보는 화면은 ==고민 선택에서 오늘의집 결제까지== 네 단계입니다")
scr = [("1  고민 선택", "고민 태그 화면", "'수납 부족', '일·휴식 분리' 등\n나의 고민을 고름"),
       ("2  장면 밸런스게임", "A/B 장면 비교 화면", "실제 사례·변화 이유·사용 조건을\n보고 장면 선택"),
       ("3  장면 키트", "키트 상품 목록 화면", "상품 3~5개의 규격·선택 이유\n가격·배송·설치 조건 확인"),
       ("4  오늘의집 결제", "상품 상세·결제 화면", "옵션·판매가·배송 확인 후\n오늘의집에서 결제")]
for i, x in enumerate(X4):
    hpill(s, x, CT, W4, scr[i][0], "grad" if i == 3 else "deep")
    d.card(s, x, CT + 36, W4, CB - CT - 36 - 20, "outline" if i == 3 else "white")
    phone(s, x + W4 / 2, CT + 52, 118, scr[i][1])
    d.text(s, x + 8, CT + 300, W4 - 16, 44, scr[i][2], 13.5, "medium", INK, align="center", line_spacing=1.35)
    if i < 3:
        d.text(s, x + W4 - 2, CT + 150, 18, 30, "›", 26, "bold", PRI, align="center", anchor="middle", check=False)
src(s, "캠페인 제안 | 기존 기획전·콘텐츠 편집으로 시작 가능한 MVP 범위 · 상품 3~5개는 가상 운영 가정 · 현재 기능(상품 태그·3D·AR)을 새 기능으로 발표하지 않음", y=494)

program(3, "달라진 우리 집이 다음 고객의 선택 근거로", "이 장면을 만든 상품은 오늘의집에서",
        [("선정된 공간의 실제 변화를 20초 숏폼으로", "0~3초 BEFORE '이 좁은 방, 바뀔 수 있을까?' → A/B 선택 이유\n→ 배치·사용 → AFTER + '이 장면을 만든 상품은 오늘의집에서'"),
         ("구매 고객이 '왜 골랐는지'를 집들이로 공유", "선택 이유 · 실제 사용 · 아쉬운 점까지 사진·영상으로 기록\n이용 동의 후 다음 고객의 선택 자료로 재편집"),
         ("기존 비포·애프터 영상은 이 프로그램으로 흡수", "주기적 비포·애프터 업로드가 메인이 아님\n일부 SKU만 기존 매장 체험과 연계 (대규모 팝업 전제 X)")],
        mock_board, "콘텐츠 → 키트 클릭률 · 구매 후 후기 생성률\n후기 기반 재방문율")

# 채널 통합 ─
s = base("IMC 통합")
title(s, "매체별 활동은 달라도, 고객에게 전달하는 ==다음 행동은 하나==입니다")
d.highlight_bar(s, L, CT, CW, "모든 접점  →  같은 공간 고민  →  장면 키트  →  오늘의집 결제", h=38, size=16)
ch = [("Paid", "메타 · 유튜브 · 디지털", "문제 공감 숏폼", "인지·유입", "고민 선택 페이지"),
      ("Owned", "앱 · 기획전", "밸런스게임 + 장면 키트", "고려·구매", "SKU 상세·결제"),
      ("Creator", "릴스 · 유튜브 · 커뮤니티", "선택 이유와 실제 변화", "고려·확산", "해당 에피소드 키트"),
      ("UGC", "장면 집들이", "구매 고객의 실제 후기", "구매 후 신뢰", "다음 고객의 사례"),
      ("Offline (선택)", "기존 매장 일부", "체험 가능한 SKU 시연", "고관여 확신", "QR → 해당 키트"),
      ("CRM (2단계)", "앱 푸시 · 알림", "관심 상품의 사용 사례", "재고려", "동의·정책 확인 후")]
gh = (CB - CT - 50 - 12) / 2
for i, (nm, med, msg, role, nxt) in enumerate(ch):
    x = X3[i % 3]
    y = CT + 50 + (i // 3) * (gh + 12)
    st = "outline" if nm == "Owned" else ("grey" if "2단계" in nm else "white")
    d.card(s, x, y, W3, gh, st)
    d.tag(s, x + 18, y + 18, 112, nm, "grad" if nm == "Owned" else ("dark" if "2단계" in nm else "blue"), h=24, size=12)
    d.text(s, x + 140, y + 18, W3 - 156, 24, med, 11.5, "medium", MUTE, anchor="middle", check=False)
    d.text(s, x + 18, y + 60, W3 - 36, 22, msg, 16.5, "bold", INK, check=False)
    dotline(s, x, y + 100, W3)
    d.text(s, x + 18, y + 114, 70, 18, "역할", 11, "bold", MUTE, check=False)
    d.text(s, x + 70, y + 112, W3 - 88, 20, role, 13.5, "semibold", INK, check=False)
    d.text(s, x + 18, y + 140, 70, 18, "다음 행동", 11, "bold", MUTE, check=False)
    d.text(s, x + 70, y + 138, W3 - 88, 20, f"→ {nxt}", 13.5, "bold", PRI, check=False)
note(s, "영상은 브랜드 홈이 아니라 그 영상의 공간 고민/키트로 보낸다. 스크랩 기반 CRM은 동의·데이터 정책 확인 후 2단계.")

# 고객 여정 ─
s = base("IMC 통합")
title(s, "발견 → 선택 → 구매 → 공유, ==캠페인을 한 고객 여정==으로 완성합니다")
st5 = ["관심", "고려", "검토", "구매", "사용·공유"]
lw_ = 112
cw5 = (CW - lw_ - 10 - 4 * 8) / 5
xs5 = [L + lw_ + 10 + i * (cw5 + 8) for i in range(5)]
rampc = ["D6EEF5", "BCE3EF", "8DCFE4", "0E7FA5", "34ACD4"]
for i, t in enumerate(st5):
    sh = d.rect(s, xs5[i], CT, cw5 + 6, 36, shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON, fill=rampc[i])
    sh.adjustments[0] = 0.28
    d.text(s, xs5[i] + 12, CT, cw5 - 14, 36, t, 14, "bold", "FFFFFF" if i >= 3 else INK, align="center", anchor="middle",
           check=False)
rows = [("고객의 말", ["\"우리 집에도\n저런 문제가 있어\"", "\"A/B 중 내가\n원하는 건?\"", "\"실제로 뭘\n사야 하지?\"", "\"이 조건이면\n여기서 사자\"", "\"우리 집은 이렇게\n바뀌었어\""]),
        ("접점", ["장면 사연함\n광고·고객 사연", "장면 밸런스게임", "장면 키트", "오늘의집\n상품 페이지", "장면 집들이"]),
        ("핵심 행동", ["고민 선택", "장면 선택", "SKU 상세·조건 확인", "결제", "사진·선택 이유 공유"]),
        ("측정", ["진입률", "선택 완료율", "상세 클릭률", "구매율·구매자 수·거래액", "UGC·재구매"])]
ry0 = CT + 48
rh = (CB - ry0 - 3 * 8) / 4
for r_, (lab, cells) in enumerate(rows):
    y = ry0 + r_ * (rh + 8)
    d.rect(s, L, y, lw_, rh, radius=10, fill="E2E5E7")
    d.text(s, L, y, lw_, rh, lab, 14, "bold", TXT, align="center", anchor="middle", check=False)
    for i, c in enumerate(cells):
        hot = i == 3
        d.card(s, xs5[i], y, cw5, rh, "outline" if (hot and r_ >= 2) else "white", radius=10)
        d.text(s, xs5[i] + 6, y, cw5 - 12, rh, c, 13 if r_ == 0 else 13.5, "medium" if r_ == 0 else "semibold",
               PRI if hot else INK, align="center", anchor="middle", line_spacing=1.25)

# 로드맵 ─
s = base("실행 계획")
title(s, "12주 동안 파일럿에서 확장까지, ==단계마다 통과 기준==으로 판단합니다")
ph4 = [("1~2주", "준비", 2), ("3~4주", "파일럿", 2), ("5~8주", "확대", 4), ("9~12주", "확장", 4)]
tw = CW / 12
x = L
for i, (wk, nm, n) in enumerate(ph4):
    w = tw * n - 4
    if i == 1:
        d.rect(s, x, CT, w, 30, radius=8, gradient=GRAD)
    else:
        d.rect(s, x, CT, w, 30, radius=8, fill="D5EAF2")
    d.text(s, x, CT, w, 30, f"{wk}  ·  {nm}", 13, "bold", "FFFFFF" if i == 1 else DEEP, align="center", anchor="middle",
           check=False)
    x += tw * n
for k in range(13):
    d.line(s, L + tw * k, CT + 34, L + tw * k, CT + 40, color="9AA0AA", w=0.75)
RM = [("준비", ["문제별 고객 사례·콘텐츠 권리 확보", "SKU·가격·배송·설치 검수", "추적 이벤트 설계"], "구매 가능한 키트 2개\n+ 권리 검수 완료"),
      ("파일럿", ["공간 고민 2개로 시작", "밸런스게임 콘텐츠·기획전·광고 연계"], "방문 → 상품 → 구매\n흐름 정상 작동"),
      ("확대", ["반응 좋은 고민 중심 크리에이터 확대", "실제 구매 후기(집들이) 추가"], "비교 그룹 대비\n구매 전환 확인"),
      ("확장", ["우수 조합 확장", "파트너 협업 검토", "동의 기반 리마케팅"], "구매자·거래액·효율\n반품 점검")]
cy0 = CT + 50
chh = CY - 12 - cy0
for i, (nm, acts, gate) in enumerate(RM):
    x = X4[i]
    d.card(s, x, cy0, W4, chh, "outline" if i == 1 else "white", radius=14)
    d.text(s, x, cy0 + 14, W4, 22, nm, 17, "bold", PRI if i == 1 else INK, align="center", check=False)
    dotline(s, x, cy0 + 44, W4)
    d.text(s, x + 16, cy0 + 54, 80, 14, "실행", 11, "bold", MUTE, check=False)
    d.bullets(s, x + 16, cy0 + 74, W4 - 28, acts, size=13, color=INK, gap=1.45, weight="medium")
    gy = cy0 + chh - 76
    if i == 1:
        d.rect(s, x + 12, gy, W4 - 24, 64, radius=10, gradient=GRAD)
    else:
        d.rect(s, x + 12, gy, W4 - 24, 64, radius=10, fill=MIST)
    d.text(s, x + 12, gy + 6, W4 - 24, 14, "통과 기준", 10.5, "bold", "FFFFFF" if i == 1 else LBL, align="center", check=False)
    d.text(s, x + 16, gy + 22, W4 - 32, 38, gate, 13, "semibold", "FFFFFF" if i == 1 else PRI, align="center",
           line_spacing=1.2)
callout(s, "같은 SKU의 가격·배송 경쟁력이 크게 떨어지면 {{캠페인 소재로 밀지 않습니다}}", size=15)

# ══ PART E ════════════════════════════════════════════════════════
divider(4, "무엇에 쓰고, 무엇으로 증명하나", "가상 RFP 예산 10억 원의 배분과, 캠페인이 만든 구매 변화를 확인하는 방법", "E")

# 예산 ─
s = base("예산·성과")
title(s, "예산은 화제성이 아니라 ==‘장면 키트’ 구매 경험==을 만드는 데 집중합니다")
bud = [("퍼포먼스·매체 운영", 30, "3.0억"), ("실제 사례·크리에이터 콘텐츠", 20, "2.0억"), ("장면 키트·브랜드 협업 운영", 20, "2.0억"),
       ("소비자 참여·UGC 운영", 10, "1.0억"), ("앱 기획전·CRM 운영", 10, "1.0억"), ("오프라인 소규모 체험", 5, "0.5억"), ("측정·실험", 5, "0.5억")]
cols_ = ["0B5A73", "0E7FA5", "34ACD4", "8DCFE4", "BCE3EF", "D5DBE0", "C3C4C4"]
hpill(s, L, CT, 330, "가상 RFP 총예산 10억 원", "deep")
d.card(s, L, CT + 36, 330, CY - 12 - CT - 36, "white")
d.donut(s, L + 30, CT + 50, 270, 262, [b[0] for b in bud], [b[1] for b in bud], colors=cols_, hole=62)
d.text(s, L, CT + 160, 330, 34, "10억 원", 26, "bold", INK, align="center", check=False)
d.text(s, L, CT + 194, 330, 16, "팀의 초기 배분 가정", 11, "medium", MUTE, align="center", check=False)
rx, rw = L + 346, CW - 346
hpill(s, rx, CT, rw, "항목별 배분")
d.card(s, rx, CT + 36, rw, CY - 12 - CT - 36, "white")
for i, (nm, p, amt) in enumerate(bud):
    y = CT + 52 + i * 38
    d.rect(s, rx + 20, y + 9, 12, 12, fill=cols_[i], radius=3)
    d.text(s, rx + 42, y, 210, 30, nm, 14, "semibold" if i < 3 else "medium", INK, anchor="middle", check=False)
    d.rect(s, rx + 258, y + 8, 170 * p / 30, 14, radius=4, fill=cols_[i])
    d.text(s, rx + 436, y, 40, 30, f"{p}%", 14, "bold", PRI if i < 3 else INK, anchor="middle", check=False)
    d.text(s, rx + rw - 66, y, 46, 30, amt, 12.5, "medium", MUTE, align="right", anchor="middle", check=False)
callout(s, "구매와 직접 연결되는 접점(매체·콘텐츠·키트)에 {{70% 집중}}, 효과가 확인된 곳에 증액합니다", size=15)
src(s, "가상 RFP 예산 · 실제 견적 아님 — SKU 협업·크리에이터 출연료·시공비·계측 비용은 견적 근거 없음")

# KPI ─
s = base("예산·성과")
title(s, "성공은 조회 수가 아니라 ==실제로 달라진 구매 행동==으로 판단합니다")
tiers = [("선행 지표", "white", ["광고 → 고민 선택 진입률", "밸런스게임 A/B 선택률", "키트 → SKU 상세 클릭률"]),
         ("핵심 · 사업 지표", "outline", ["노출·비노출 그룹의\nSKU 구매 전환율 차이", "고유 구매자 수", "커머스 거래액 (환불 반영)"]),
         ("품질 · 장기 지표", "white", ["반품률 · 고객 획득비용", "매출총이익 (가능 시)", "브랜드 연상 · 재방문 · 재구매"])]
th = 236
for i, x in enumerate(X3):
    hpill(s, x, CT, W3, tiers[i][0], "grad" if i == 1 else "deep")
    d.card(s, x, CT + 36, W3, th, tiers[i][1])
    if i == 1:
        d.highlight_bar(s, x + 16, CT + 52, W3 - 32, "핵심 KPI · 증분 효과", h=28, size=13)
        d.text(s, x + 10, CT + 92, W3 - 20, 50, tiers[i][2][0], 17, "bold", PRI, align="center", line_spacing=1.25)
        dotline(s, x, CT + 152, W3)
        for k, it in enumerate(tiers[i][2][1:]):
            d.rect(s, x + 18, CT + 164 + k * 50, W3 - 36, 40, radius=10, fill=MIST)
            d.text(s, x + 18, CT + 164 + k * 50, W3 - 36, 40, it, 14, "bold", PRI, align="center", anchor="middle", check=False)
    else:
        for k, it in enumerate(tiers[i][2]):
            yy = CT + 56 + k * 70
            d.rect(s, x + 18, yy, W3 - 36, 56, radius=10, fill="F1F4F5")
            d.text(s, x + 18, yy, W3 - 36, 56, it, 14, "semibold", INK, align="center", anchor="middle", check=False)
vy = CT + 36 + th + 12
d.text(s, L, vy, 120, 16, "검증 설계", 12.5, "bold", INK, check=False)
for i, t in enumerate(["비노출 · 일반 기획전 그룹과 무작위 비교", "기간·SKU·신규/기존·유입경로 통제", "노출 → 고민 → 키트 → 상세 → 결제 로그 연결"]):
    x = X3[i]
    d.rect(s, x, vy + 22, W3, 36, radius=10, fill=MIST)
    d.number_badge(s, x + 22, vy + 40, str(i + 1), r=11)
    d.text(s, x + 42, vy + 22, W3 - 50, 36, t, 12.5, "semibold", PRI, anchor="middle", check=False)
callout(s, "단순 전후 매출이나 참여자 구매율이 아니라 {{노출·비노출 그룹의 차이}}로 증명합니다", size=15)
note(s, "결과가 나쁘면 화제성이 아니라 상품 구성·실제 가격 경쟁력·전환 경로를 먼저 재점검한다.")

# ══ 마무리 (레퍼런스: 콘셉트 + 세 문장 요약) ══════════════════════════
s = base(number=False)
d.rect(s, 0, 0, W, H, gradient=("0D5C74", "07475A", 90))
d._network(s, 660, 400, 280, 130, seed=5, n=14)
d.text(s, 0, 74, W, 56, "우리 집의 다음 장면", 40, "bold", "FFFFFF", align="center", check=False)
d.text(s, 0, 136, W, 22, "마음에 드는 집을 보는 것에서, 내가 살고 싶은 집을 만드는 것으로", 16, "medium", "BCE3EF", align="center",
       check=False)
sm = [("문제", "오늘의집에서 발견해도, 일부 고객은 **가격·배송·구매 습관** 때문에 다른 곳에서 결제합니다."),
      ("전략", "단품 비교를 넘어, 실제 공간 경험을 **‘우리 집의 변화’라는 구매 가치**로 재구성합니다."),
      ("IMC", "**장면 사연함 → 밸런스게임 → 키트 → 집들이**로 발견부터 오늘의집 결제·공유까지 잇습니다.")]
for i, (k, v) in enumerate(sm):
    y = 190 + i * 64
    d.rect(s, 110, y, 120, 52, radius=10, fill="1E9BC4")
    d.text(s, 110, y, 120, 52, k, 16, "bold", "FFFFFF", align="center", anchor="middle", check=False)
    d.rect(s, 240, y, 610, 52, radius=10, fill="FFFFFF", alpha=12)
    d.text(s, 262, y, 576, 52, v, 14.5, "medium", "FFFFFF", anchor="middle", check=False)
d.text(s, 0, 420, W, 30, "감사합니다", 22, "bold", "FFFFFF", align="center", check=False)
d.text(s, 0, 456, W, 16, f"{TEAM}  ·  Q&A", 12, "semibold", "8DCFE4", align="center", check=False)

# ══ 부록 ══════════════════════════════════════════════════════════
s = base("Appendix")
title(s, "출처 · 조사 한계 · 표기 규칙 · 생성형 AI 활용")
secs = [("주요 출처", ["[1] 오늘의집 공식 2025 실적 발표 — ohstory.io/press/pressrelease/15242",
                    "[2] 오늘의집 공간 효율형 수납 검색 관련 보도 — ohstory.io/press/media/16002",
                    "[3] 오늘의집 1인용 가구 검색 관련 보도 — ohstory.io/press/media/15915",
                    "[4] 자체 2차 설문 (n=51)   [5] 자체 고객 인터뷰 (n=5)   [6] 팀 작성 가상 RFP"]),
        ("조사 한계", ["2차 설문 n=51은 40대 이상 49%, 자가 57%로 20~30대 임차 가구를 대표하지 않음",
                    "최초 발견처–구매처 일치 비율(7/12 등)은 서비스 전환율이 아니라 자체 조사 응답 비율",
                    "공간 조합·선택 경험이 가격·배송 혜택을 넘어설 만큼 가치 있는지는 인과 증거가 없어 실험 설계와 함께 제안"]),
        ("표기 규칙 · 생성형 AI 활용", ["확인된 사실 / 팀 관찰 / 전략적 해석 / 캠페인 제안을 출처 캡션에 구분 표기. 화면·이미지는 모두 기획 시안",
                                   "생성형 AI는 자료 구조화, 설문 집계 보조, 문안 초안, 장표 레이아웃 제작에 활용. 수치·출처는 원자료와 대조"])]
for j, (tt, ls) in enumerate(secs):
    x = X3[j]
    hpill(s, x, CT, W3, tt, "deep" if j != 1 else "grad")
    d.card(s, x, CT + 36, W3, 214, "white")
    d.bullets(s, x + 18, CT + 52, W3 - 34, ls, size=11.5, color=TXT, gap=1.45, weight="regular")
vy = CT + 264
hpill(s, L, vy, CW, "남은 검증 과제 (P0) — 실행 전 반드시 확인", "dark")
p0 = [("공간 조합의 구매 영향", "구매 의향·선택 소규모 실험\n가능하면 실제 전환 비교"),
      ("대상 SKU 가격·배송 조건", "동일 SKU 10~20개 실사\n옵션·배송비·설치비 포함"),
      ("PB·단독·협업 구성", "브랜드·공급 범위와\n실행 가능성 조사"),
      ("카테고리 매출 기여", "공개 판매 랭킹·대리 지표\n확인 불가 수치는 명시")]
for k, (h_, b_) in enumerate(p0):
    x = X4[k]
    d.card(s, x, vy + 36, W4, CB - vy - 36, "white")
    d.text(s, x + 10, vy + 52, W4 - 20, 20, h_, 14, "bold", PRI, align="center", check=False)
    d.text(s, x + 10, vy + 80, W4 - 20, 40, b_, 12, "medium", TXT, align="center", line_spacing=1.35)

d.save(OUT)
print("saved", OUT, "slides:", len(d.prs.slides))
print("warnings:", len(d.warnings))
for w in d.warnings:
    print("  -", w)
