"""오늘의집 IMC 발표자료 2차 — IR 덱 레이아웃 시스템(ir_kit) + 오늘의집 틸 팔레트.

실행:  python3 ohou-team-project/deck/build_deck_v2.py
출력:  ohou-team-project/deck/오늘의집_IMC_발표_2차.pptx

1차 대비 변경
- 레이아웃: 좌측 정렬 한 줄 헤드라인 + 서브헤드, 3열/2열 고정 그리드(x=38/337/636), 말풍선 pill + 진행선, 유리 카드, 좌하단 각주
- 프로그램 네이밍: 다음 장면 제보소/선택하기/컬렉션/공개 → 장면 사연함 / 장면 밸런스게임 / 장면 키트 / 장면 집들이
좌표 단위 pt (960×540). 시안 이미지·목업 자리는 비워 둠.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "imc-slide-design", "scripts"))
from ir_kit import C, Deck, W, H, MARGIN_X as L, CONTENT_W as CW, RIGHT as R, _line_dash  # noqa: E402

OUT = os.path.join(HERE, "오늘의집_IMC_발표_2차.pptx")
TEAM = "[조 이름]"
d = Deck(copyright=f"OHOUSE IMC PROPOSAL  ·  {TEAM}")

DEEP, PRI, LBL, MIST, PALE = C["navy"], C["blue"], C["blue_label"], C["blue_mist"], C["blue_pale"]
X3 = [38, 337, 636]
W3 = 285
X2 = [38, 492]
W2 = 430
PROG = [("01", "장면 사연함", "발견"), ("02", "장면 밸런스게임", "선택"), ("03", "장면 키트", "구매"), ("04", "장면 집들이", "공유")]
PARTS = ["찾는 곳과 사는 곳", "다른 곳에서 사는 이유", "상품 대신 장면", "사연에서 집들이까지", "투자와 증명"]


# ── 공통 헬퍼 ──────────────────────────────────────────────────────
def slot(s, x, y, w, h, label, dark=False, prefix=True, label_y=None):
    """시안 자리: 점선 테두리 + 라벨. 목업·이미지로 교체."""
    r = d.rect(s, x, y, w, h, fill="F7FAFB" if not dark else "16323B", radius=10,
               line="9ED6E8" if not dark else "2E5A66", line_w=1)
    _line_dash(r.line, "dash")
    ly = (y + h / 2 - 20) if label_y is None else label_y
    d.text(s, x + 10, ly, w - 20, 40, (f"[ 기획 시안 ]\n{label}" if prefix else label), 11, "regular",
           "8A9AA0" if not dark else "7FA9B8", align="center", anchor="middle", line_spacing=1.3, check=False)
    return r


def phone(s, cx, y, w, label):
    h = w * 2.0
    d.rect(s, cx - w / 2, y, w, h, fill="FFFFFF", radius=w * 0.16, line="1C2A30", line_w=2.2, shadow=True)
    d.rect(s, cx - w * 0.15, y + 6, w * 0.3, 4, fill="1C2A30", radius=2)
    inner = d.rect(s, cx - w / 2 + 7, y + 16, w - 14, h - 26, fill="F3F7F8", radius=w * 0.09)
    d.text(s, cx - w / 2 + 10, y + 16, w - 20, h - 26, f"[ 목업 ]\n{label}", 9.5, "regular", "8A9AA0",
           align="center", anchor="middle", line_spacing=1.3, check=False)
    return inner


def pill_row(s, xs, ws, y, labels, styles=None, badge_at=None, flow=True):
    """카드 위 pill 행 + pill 사이 진행선."""
    styles = styles or ["blue"] * len(labels)
    centers = []
    for i, (x, w, lab) in enumerate(zip(xs, ws, labels)):
        pw = ws_pill = min(w - 20, max(110, len(lab) * 15 + 34))
        px = x + (w - pw) / 2
        d.pill(s, px, y, pw, lab, style=styles[i])
        centers.append((px, px + ws_pill))
    for i in range(len(centers) - 1 if flow else 0):
        d.flow(s, centers[i][1], centers[i + 1][0], y + 13, badge="!" if badge_at == i + 1 else None)


def card_title(s, x, y, w, title, color=None, size=17):
    d.text(s, x, y, w, 24, title, size, "semibold", color or C["ink"], align="center", check=False)


def blue_conclusion(s, x, y, w, text, size=15.5):
    d.text(s, x + 10, y, w - 20, 46, text, size, "bold", PRI, align="center", line_spacing=1.25)


def divider(part_idx, title, question, pages):
    s = d.prs.slides.add_slide(d._blank)
    d._slide_idx += 1
    d.rect(s, 0, 0, W, H, gradient=("0D5C74", "083F50", 90))
    d._network(s, 560, 60, 380, 300, seed=part_idx + 3, n=22)
    d.text(s, R - 330, 330, 330, 110, pages, 80, "bold", "1A7690", align="right", check=False)
    d.text(s, L, 178, 400, 20, f"PART {'ABCDE'[part_idx]}", 14, "bold", "8DCFE4", check=False)
    d.text(s, L, 202, 800, 50, title, 36, "bold", "FFFFFF", check=False)
    d.rect(s, L, 262, 0.75 * 60, 2, fill="8DCFE4")
    d.text(s, L, 278, 500, 50, question, 16, "regular", "CFE7EF", line_spacing=1.35)
    gw = (CW - 4 * 8) / 5
    for i, p in enumerate(PARTS):
        x = L + i * (gw + 8)
        cur = i == part_idx
        b = d.rect(s, x, 470, gw, 28, radius=14, fill="1E9BC4" if cur else None, line=None if cur else "3E8199",
                   line_w=0.75)
        d.text(s, x, 470, gw, 28, f"{'ABCDE'[i]}  {p}", 11, "bold" if cur else "medium",
               "FFFFFF" if cur else "8DB9C7", align="center", anchor="middle", check=False)
    return s


def note(s, text):
    s.notes_slide.notes_text_frame.text = text


# ══ 표지 ══════════════════════════════════════════════════════════
s = d.prs.slides.add_slide(d._blank)
d._slide_idx += 1
d.rect(s, 0, 0, W, H, gradient=("0E6A87", "084B5E", 135))
d._network(s, 470, 200, 470, 320, seed=11, n=30)
d.text(s, L, 40, 760, 90, "오늘의집에서 **찾고**,\n오늘의집에서 **사는** 이유", 32, "medium", "FFFFFF", line_spacing=1.15)
d.rect(s, L, 132, 0.75, 48, fill="FFFFFF", alpha=55)
d.text(s, L, 205, 640, 60, "〈우리 집의 다음 장면〉\n탐색에서 결제까지 잇는 IMC 캠페인 제안", 20, "regular", "FFFFFF", line_spacing=1.35)
d.text(s, L, 470, 500, 16, f"2026 디지털마케팅 IMC 제안  ·  {TEAM}  ·  2026.12.01", 12, "semibold", "BCE3EF", check=False)
d.text(s, L, 492, 500, 14, "※ 팀이 작성한 가상 RFP에 대한 제안입니다", 10, "regular", "8DCFE4", check=False)

# ══ Summary ═══════════════════════════════════════════════════════
s = d.content_slide("Executive Summary", "탐색 1위 플랫폼이 결제까지 가져오는 방법, 〈우리 집의 다음 장면〉",
                    "단품 가격 경쟁 대신 '공간 변화'라는 구매 이유로 오늘의집 결제를 만듭니다.")
rows = [("문제", "오늘의집에서 발견한 상품도 일부는 **쿠팡·네이버에서 결제**"),
        ("원인", "가격·구매 습관·배송 혜택이 **함께 작용**해 구매처가 바뀜"),
        ("기회", "오늘의집 구매자 61%가 **실사용 사진·후기**를 구매 이유로 선택"),
        ("전략", "단품이 아니라 **'내 집의 공간 변화'**를 구매 단위로 제안")]
for i, (k, v) in enumerate(rows):
    y = 158 + i * 82
    d.card(s, L, y, 470, 72, "white", radius=14)
    d.tag(s, L + 18, y + 25, 56, k, "blue" if i < 3 else "grad", h=22)
    d.text(s, L + 90, y + 14, 365, 44, v, 15, "medium", C["ink"], anchor="middle", line_spacing=1.25)
d.chevron(s, 514, 276, 30, 60)
d.card(s, 552, 158, 370, 318, "outline")
d.text(s, 552, 178, 370, 16, "BIG IDEA", 11, "bold", LBL, align="center", check=False)
d.text(s, 552, 198, 370, 34, "우리 집의 다음 장면", 26, "bold", C["ink"], align="center", check=False)
d.text(s, 552, 236, 370, 18, "마음에 드는 집을 보는 것에서, 내가 살고 싶은 집을 만드는 것으로", 11.5, "medium", C["text"],
       align="center", check=False)
for i, (no, nm, st) in enumerate(PROG):
    y = 272 + i * 49
    d.rect(s, 576, y, 322, 40, radius=10, fill=MIST if i != 2 else "FFFFFF", line=None if i != 2 else PRI, line_w=1)
    d.tag(s, 588, y + 9, 46, st, "grad" if i == 2 else "blue", h=22, size=11)
    d.text(s, 646, y, 240, 40, f"**{nm}**   [[PROGRAM {no}]]", 14, "medium", C["ink"], anchor="middle", check=False)

# ══ Contents ══════════════════════════════════════════════════════
s = d.content_slide("Contents", "문제를 확인하고, 원인을 검증하고, 하나의 캠페인으로 풉니다",
                    "가설을 세우고 설문·인터뷰로 검증한 순서 그대로 구성했습니다.")
toc = [("찾는 곳과 사는 곳", ["발견과 구매의 단절", "구매처를 정하는 순간"], "03–07"),
       ("다른 곳에서 사는 이유", ["원인 가설과 검증", "오늘의집에서 사는 이유"], "08–11"),
       ("상품 대신 장면", ["구매 가치 재정의", "BIG IDEA"], "12–13"),
       ("사연에서 집들이까지", ["프로그램 4종", "채널·여정·실행 계획"], "14–22"),
       ("투자와 증명", ["예산 배분", "KPI·검증 설계"], "23–24")]
cw5 = (CW - 4 * 12) / 5
for i, (t, items, pg) in enumerate(toc):
    x = L + i * (cw5 + 12)
    d.card(s, x, 162, cw5, 300, "outline" if i == 3 else "white", radius=14)
    d.text(s, x, 184, cw5, 40, f"0{i + 1}", 30, "bold", PRI if i == 3 else LBL, align="center", check=False)
    d.text(s, x, 234, cw5, 14, f"PART {'ABCDE'[i]}", 10, "bold", C["muted"], align="center", check=False)
    d.text(s, x + 10, 254, cw5 - 20, 44, t, 16, "bold", C["ink"], align="center", line_spacing=1.2)
    d.line(s, x + 20, 310, x + cw5 - 20, 310, color="C9CDD3", dash="sysDot")
    d.bullets(s, x + 16, 324, cw5 - 28, items, size=12.5, color=C["text"], gap=1.6)
    d.text(s, x, 430, cw5, 16, f"p.{pg}", 11, "semibold", C["muted"], align="center", check=False)

# ══ PART A ════════════════════════════════════════════════════════
divider(0, "찾는 곳과 사는 곳이 다릅니다", "발견과 구매가 갈라지는 사례는 무엇이고, 여정의 어디에서 일어나는가?", "03–07")

# 01 ─────────────
s = d.content_slide("Problem", "오늘의집에서 발견하고, 결제는 다른 앱에서 끝나는 구매 여정",
                    "인터뷰 P1은 오늘의집에서 디자인을 참고한 뒤, 네이버에서 비교하고 쿠팡에서 결제했습니다.")
pill_row(s, X3, [W3] * 3, 162, ["발견 · 오늘의집", "비교 · 네이버", "결제 · 쿠팡"], ["blue", "blue", "dark"], badge_at=2)
caps = [("집들이 콘텐츠에서", "**책상·가구 디자인**을 참고"), ("같은 상품을 검색해", "**가격·조건**을 다시 비교"),
        ("실제 가격 차이와", "**익숙한 배송**으로 결제")]
labels = ["오늘의집 집들이 화면", "네이버 검색 결과 화면", "쿠팡 상품·결제 화면"]
for i, x in enumerate(X3):
    d.card(s, x, 215, W3, 268, "grey" if i == 2 else ("outline" if i == 0 else "white"))
    phone(s, x + W3 / 2, 230, 92, labels[i])
    d.text(s, x + 10, 425, W3 - 20, 44, f"{caps[i][0]}\n{caps[i][1]}", 14, "medium",
           C["ink"], align="center", line_spacing=1.3)
d.footnote(s, ["팀 관찰 : 고객 인터뷰 P1 사례 (n=5 중 1명) — 전체 이용자 행동을 대표하지 않음"])
note(s, "오늘의집의 문제는 집을 보여주지 못하는 것이 아닙니다. 발견에서 구매로 연결되는 순간을 더 강하게 만들어야 합니다.")

# 02 ─────────────
s = d.content_slide("Business", "콘텐츠에서 구매·설치·시공까지, 연결형 리빙 플랫폼으로 확장 중",
                    "오늘의집의 성장 방향은 공간 콘텐츠 이후의 구매 경험까지 연결하는 데 있습니다.")
d.kpi(s, L, 158, 250, 325, "2025 매출", "약 3,215억 원", highlight=True, value_size=26)
d.text(s, L, 400, 250, 20, "전년 대비 +11.7%", 15, "bold", "FFFFFF", align="center", check=False)
d.illo(s, "growth", L + 125, 300, 120, vector=True)
d.card(s, 302, 158, 620, 325, "white")
steps = [("콘텐츠·커뮤니티", "집들이·사진·노하우"), ("상품 탐색", "공간 속 상품 태그"), ("커머스 구매", "오늘의집 결제"),
         ("배송·설치 / 시공", "일부 상품·지역")]
sx = [326 + i * 148 for i in range(4)]
for i, (t, c) in enumerate(steps):
    d.pill(s, sx[i], 186, 132, t, style="blue" if i < 2 else "soft", tail=False)
    d.text(s, sx[i], 222, 132, 18, c, 12.5, "medium", C["text"], align="center", check=False)
    if i < 3:
        d._fade_arrow(s, sx[i] + 134, sx[i + 1] - 3, 199)
d.illo(s, "platform", 612, 320, 150, vector=True)
d.highlight_bar(s, 326, 418, 572, "이 확장을 뒷받침할 '구매 경험'은 지금 충분한가?", h=42, size=17)
d.footnote(s, ["확인된 사실 : 오늘의집 공식 2025 실적 발표(ohstory.io) · 시공·배송 범위는 상품·지역마다 다름"], w=600)

# 03 ─────────────
s = d.content_slide("Market", "찾는 채널과 결제하는 채널이 나뉜 리빙 커머스 경쟁 구도",
                    "오늘의집은 발견의 출발점이지만, 비교와 결제는 네이버·쿠팡에서 일어나기 쉽습니다.")
cols = [("오늘의집", "blue", ["실제 집 콘텐츠·상품 연결", "공간 맥락, 실사용 사진·후기", "**발견의 출발점**"]),
        ("네이버", "dark", ["검색·가격 비교", "최저가·조건 비교", "비교 단계"]),
        ("쿠팡", "dark", ["구매 습관·멤버십·빠른 배송", "익숙함, 배송 속도", "결제 단계"]),
        ("취향 플랫폼", "dark", ["디자인·브랜드 큐레이션", "취향에 맞는 상품 발견", "발견 단계"])]
rows_lbl = ["대표 강점", "기대하는 구매 가치", "여정에서의 위치"]
lx, cx0, ccw = L, 180, (R - 180 - 3 * 10) / 4
for r_, lab in enumerate(rows_lbl):
    y = 236 + r_ * 78
    d.rect(s, lx, y + 14, 130, 34, radius=17, fill="E2E4E8")
    d.text(s, lx, y + 14, 130, 34, lab, 13, "bold", C["text"], align="center", anchor="middle", check=False)
for i, (nm, st, vals) in enumerate(cols):
    x = cx0 + i * (ccw + 10)
    d.card(s, x, 200, ccw, 283, "outline" if i == 0 else "mid")
    d.pill(s, x + (ccw - 120) / 2, 162, 120, nm, style=st)
    for r_, v in enumerate(vals):
        y = 236 + r_ * 78
        d.text(s, x + 10, y, ccw - 20, 62, v, 14.5, "semibold" if i == 0 else "medium",
               PRI if i == 0 else C["text"], align="center", anchor="middle", line_spacing=1.25)
        if r_ < 2:
            d.line(s, x + 20, y + 70, x + ccw - 20, y + 70, color="C9CDD3", dash="sysDot")
d.footnote(s, ["전략적 해석 : 플랫폼별 대표 포지션 기준이며 독점적 기능 구분이 아님"])

# 04 ─────────────
s = d.content_slide("Evidence", "오늘의집에서 처음 본 고객 12명 중 5명은 다른 곳에서 구매",
                    "같은 기준에서 네이버는 8/11, 쿠팡은 11/12가 처음 본 곳에서 그대로 구매했습니다.")
d.card(s, L, 158, 540, 325, "white")
d.text(s, L, 178, 540, 20, "처음 본 플랫폼에서 그대로 구매한 응답자", 16, "bold", LBL, align="center", check=False)
bars = d.bars(s, L + 40, 430, 460, 190, [
    {"cat": "오늘의집", "value": 7 / 12, "color": PRI, "inside": "58%", "top": "7/12"},
    {"cat": "네이버", "value": 8 / 11, "color": C["blue_soft"], "inside": "73%", "inside_color": "0B5A73", "top": "8/11"},
    {"cat": "쿠팡", "value": 11 / 12, "color": C["blue_soft"], "inside": "92%", "inside_color": "0B5A73", "top": "11/12"}],
    vmax=1.0, label_size=14)
d.kpi(s, 594, 158, 328, 150, "오늘의집 최초 발견 고객 중\n다른 곳에서 구매", "5 / 12명", highlight=True, value_size=30)
d.card(s, 594, 320, 328, 163, "white")
d.text(s, 614, 336, 290, 18, "해석할 때 주의할 점", 14, "bold", C["ink"], check=False)
d.bullets(s, 614, 362, 292, ["서비스 전환율이 아닌, 자체 조사의\n최초 발견처–최근 구매처 일치 비율",
                             "표본이 작고(각 11~12명) 응답자 구성에\n편향이 있음"], size=12.5, color=C["text"], gap=1.3)
d.footnote(s, ["팀 관찰 : 자체 2차 설문(n=51) 중 각 플랫폼 최초 발견 응답자 기준"])

# 05 ─────────────
s = d.content_slide("Customer Journey", "이동이 일어나는 지점은 결제 버튼이 아닌 '구매처를 정하는 순간'",
                    "고객은 탐색 후 가격·혜택·배송을 다시 비교하며, 결제할 앱을 이때 고르고 있었습니다.")
stages = ["공간 문제 인식", "콘텐츠·상품 탐색", "후보 비교", "구매처 결정", "결제", "설치·사용"]
pw6 = 128
gap6 = (CW - 6 * pw6) / 5
pxs = [L + i * (pw6 + gap6) for i in range(6)]
for i, st in enumerate(stages):
    d.pill(s, pxs[i], 162, pw6, st, style="dark" if i == 3 else ("soft" if i in (0, 1, 2) else "blue"), tail=i == 3)
    if i < 5:
        d.flow(s, pxs[i] + pw6, pxs[i + 1], 175)
d.card(s, X3[0], 228, W3, 255, "white")
d.card(s, X3[1], 228, W3, 255, "outline")
d.card(s, X3[2], 228, W3, 255, "grey")
card_title(s, X3[0], 248, W3, "발견한 곳")
card_title(s, X3[1], 248, W3, "구매처를 정하는 순간")
card_title(s, X3[2], 248, W3, "결제한 곳")
d.illo(s, "stack", X3[0] + W3 / 2, 340, 120, vector=True)
d.illo(s, "scatter", X3[1] + W3 / 2, 340, 130, vector=True)
d.illo(s, "report", X3[2] + W3 / 2, 340, 110, vector=True)
blue_conclusion(s, X3[0], 420, W3, "오늘의집\n집들이·상품 탐색")
blue_conclusion(s, X3[1], 420, W3, "결제창 이탈이 아니라\n구매 전 다른 앱을 여는 행동")
d.text(s, X3[2] + 10, 420, W3 - 20, 46, "쿠팡·네이버\n가격·배송 재비교 후 결제", 15.5, "bold", "404040", align="center",
       line_spacing=1.25)
d.footnote(s, ["팀 관찰 : 고객 인터뷰 n=5 · 서비스 내부 클릭스트림은 실측하지 않음"])

# ══ PART B ════════════════════════════════════════════════════════
divider(1, "왜 다른 곳에서 결제하는가", "구매처 이동의 원인을 검증하고, 오늘의집에서 구매하는 예외를 찾습니다.", "08–11")

# 06 ─────────────
s = d.content_slide("Hypothesis", "구매처 이동을 설명하는 세 가지 가설, 습관·가격·배송 혜택",
                    "대안 가설(구경 전용 앱, UI 불편, 첫 구매 장벽 등)까지 함께 놓고 설문·인터뷰로 검증했습니다.")
hyp = [("H1. 구매 습관", "\"그냥 원래 쓰던 앱에서\n사면 되지\"", "쇼핑 앱 이용 · 인터뷰", "scatter"),
       ("H2. 가격", "\"같은 물건인데\n다른 데가 더 싸네\"", "가격 인식 · 실제 비교 경험", "growth"),
       ("H3. 배송·혜택", "\"이미 멤버십도 있고\n더 빨리 오네\"", "배송 이유 · 멤버십 · 인터뷰", "network")]
pill_row(s, X3, [W3] * 3, 162, [h[0] for h in hyp], flow=False)
for i, x in enumerate(X3):
    d.card(s, x, 215, W3, 210, "white")
    d.illo(s, hyp[i][3], x + W3 / 2, 280, 100, vector=True)
    d.text(s, x + 10, 340, W3 - 20, 48, hyp[i][1], 16.5, "semibold", C["ink"], align="center", line_spacing=1.25)
    d.tag(s, x + (W3 - 170) / 2, 395, 170, hyp[i][2], "mist", h=22, size=11)
d.rect(s, L, 437, CW, 46, radius=12, fill="E2E4E8")
d.text(s, L + 20, 437, CW - 40, 46, "**함께 확인한 대안 가설**    이사할 때만 쓰는 앱  ·  구경 전용 앱  ·  가입/결제 UI 불편  ·  첫 구매 경험 부재  ·  내 집 사용 확신 부족",
       13, "medium", C["text"], anchor="middle", check=False)

# 07 ─────────────
s = d.content_slide("Root Cause", "구매처 이동은 '익숙함·가격·배송 혜택'이 겹쳐서 만든 결과",
                    "한 가지 오해만 풀면 해결되는 문제가 아니라, 여러 이유가 동시에 작동하고 있었습니다.")
rc = [("익숙한 앱", "49%", "주 이용 쇼핑 앱이 쿠팡", ["'다른 앱에서 사는 게 익숙해서' 30%"], "표본 51명, 문항별 분모 다름"),
      ("가격", "42%", "'오늘의집이 비쌀 것 같다'", ["인터뷰 5명 중 3명이 비교 후\n쿠팡의 가격 우위 언급"], "인식과 실제 가격 차이가 모두 존재"),
      ("배송·혜택", "86%", "멤버십 1개 이상 보유", ["구매처 변경자 21명 중 7명이\n배송을 이유로 선택"], "원인 중복 가능, 인과 미검증")]
pill_row(s, X3, [W3] * 3, 162, [r_[0] for r_ in rc], flow=False)
for i, x in enumerate(X3):
    d.card(s, x, 215, W3, 228, "white")
    d.text(s, x, 232, W3, 48, rc[i][1], 40, "bold", PRI, align="center", check=False)
    d.text(s, x, 284, W3, 20, rc[i][2], 14.5, "semibold", C["ink"], align="center", check=False)
    d.line(s, x + 24, 316, x + W3 - 24, 316, color="C9CDD3", dash="sysDot")
    d.text(s, x + 16, 328, W3 - 32, 50, rc[i][3][0], 13.5, "medium", C["text"], align="center", line_spacing=1.3)
    d.tag(s, x + 30, 402, W3 - 60, "한계 · " + rc[i][4], "dark", h=24, size=10.5)
d.rect(s, L, 453, CW, 30, radius=15, gradient=(C["blue_deep"], C["blue_end"]))
d.text(s, L, 453, CW, 30, "반례 : 오늘의집 구매 경험 33/51 (65%) → '첫 구매 장벽'만의 문제로 보기 어려움", 13.5, "semibold", "FFFFFF",
       align="center", anchor="middle", check=False)
d.footnote(s, ["팀 관찰 : 자체 2차 설문(n=51), 고객 인터뷰(n=5)"], bottom=508)

# 08 ─────────────
s = d.content_slide("Constraint", "가격·배송 경쟁은 내려놓고, 오늘의집이 이길 수 있는 영역에 집중",
                    "RFP는 최저가·할인 중심 캠페인을 배제하므로, 가격 외의 구매 이유를 찾아야 합니다.")
d.pill(s, X2[0] + (W2 - 170) / 2, 162, 170, "경쟁사가 이미 강한 것", style="dark")
d.pill(s, X2[1] + (W2 - 170) / 2, 162, 170, "오늘의집이 강화할 것", style="blue")
d.card(s, X2[0], 215, W2, 190, "grey")
d.card(s, X2[1], 215, W2, 190, "outline")
for i, t in enumerate(["단품 최저가", "멤버십 기반 빠른 배송", "매일 쓰는 구매 습관"]):
    d.rect(s, X2[0] + 30, 236 + i * 54, W2 - 60, 42, radius=10, fill="FFFFFF", alpha=55)
    d.text(s, X2[0] + 30, 236 + i * 54, W2 - 60, 42, t, 16, "semibold", "404040", align="center", anchor="middle", check=False)
for i, t in enumerate(["실제 공간에서의 사용 맥락", "내 집에 맞는 선택 지원", "구매 이후 배송·설치 (적용 상품)"]):
    d.rect(s, X2[1] + 30, 236 + i * 54, W2 - 60, 42, radius=10, fill=MIST)
    d.text(s, X2[1] + 30, 236 + i * 54, W2 - 60, 42, t, 16, "semibold", PRI, align="center", anchor="middle", check=False)
d.chevron(s, 465, 280, 26, 56)
d.text(s, L, 420, 300, 18, "채택하지 않을 프레임", 13, "bold", C["ink"], check=False)
fr = ["오늘의집이 사실 더 싸다", "이사하는 사람만 쓴다", "아무도 여기서 사지 않는다", "UI가 불편해서 안 산다"]
fw = (CW - 3 * 10) / 4
for i, f_ in enumerate(fr):
    x = L + i * (fw + 10)
    d.rect(s, x, 444, fw, 32, radius=16, fill="FFFFFF", line="D3D6DB", line_w=0.75)
    d.text(s, x, 444, fw, 32, f"✕  {f_}", 12.5, "medium", C["muted"], align="center", anchor="middle", check=False)
d.footnote(s, ["팀 관찰 : 구매 UI 불편 동의 약 22%, 오늘의집 구매 경험 65% (n=51)"], bottom=510, w=600)

# 09 ─────────────
s = d.content_slide("Opportunity", "오늘의집 구매자 61%가 꼽은 이유, '실사용 사진·후기'에 대한 신뢰",
                    "가격 외 정보가 중요해지는 구매 상황에서는 오늘의집이 선택되고 있었습니다.")
d.kpi(s, L, 158, 250, 325, "오늘의집 구매 이유 1위\n실사용 사진·후기 신뢰", "61%  (20/33)", highlight=True, value_size=28)
d.illo(s, "report", L + 125, 318, 110, vector=True)
d.card(s, 302, 158, 620, 220, "white")
d.text(s, 302, 174, 620, 18, "오늘의집 구매 이유 (복수응답, 구매 경험자 n=33)", 15, "bold", LBL, align="center", check=False)
br = [("사진·후기 신뢰", 61), ("사진 속 상품 바로 구매", 27), ("단독 상품", 21), ("배송·설치", 12)]
for i, (t, v) in enumerate(br):
    y = 210 + i * 38
    d.text(s, 322, y, 160, 28, t, 13.5, "semibold" if i == 0 else "medium", PRI if i == 0 else C["text"],
           align="right", anchor="middle", check=False)
    d.rect(s, 494, y + 5, 340 * v / 61, 18, radius=4, fill=PRI if i == 0 else "D5DBE0")
    d.text(s, 500 + 340 * v / 61, y, 60, 28, f"{v}%", 13.5, "bold", C["ink"], anchor="middle", check=False)
d.card(s, 302, 390, 300, 93, "white")
d.text(s, 318, 402, 270, 72, "51명 중 **26명**은 '비슷한 집 실제 사례'나\n'공간 속 상품 한 번에 담기'를 원함\n[[표현된 선호이며 실제 구매 효과는 아님]]",
       12.5, "medium", C["ink"], line_spacing=1.3)
d.card(s, 622, 390, 300, 93, "white")
d.text(s, 638, 402, 270, 72, "인터뷰에서도 **디자인·보증·사용 이유**가\n중요한 상품은 오늘의집을 고른 경우가 있었음",
       12.5, "medium", C["ink"], line_spacing=1.3)
d.footnote(s, ["팀 관찰 : 자체 2차 설문(n=51) 중 오늘의집 구매 경험자 n=33, 고객 인터뷰 n=5"], bottom=510, w=600)

# ══ PART C ════════════════════════════════════════════════════════
divider(2, "상품 대신 장면을 팝니다", "왜 '공간 변화'가 구매 가치가 되고, 어떤 콘셉트로 모이는가?", "12–13")

# 10 ─────────────
s = d.content_slide("Strategy", "사진 속 상품은 결국 다른 앱에서도 검색할 수 있는 상품",
                    "필요한 것은 그 장면을 내 집에서 만들기 위해 '무엇을 살지'까지 정하는 경험입니다.")
d.pill(s, X2[0] + (W2 - 190) / 2, 162, 190, "지금 · 단품을 발견하는 경로", style="dark")
d.pill(s, X2[1] + (W2 - 200) / 2, 162, 200, "제안 · 공간 변화를 사는 경로", style="blue")
d.card(s, X2[0], 215, W2, 268, "grey")
d.card(s, X2[1], 215, W2, 268, "outline")
left = ["집들이 사진에서 상품 발견", "상품명 확인", "다른 앱에서 검색", "쿠팡에서 단품 결제"]
right = ["우리 집의 공간 문제", "변화 시나리오 선택", "실제 사용·조합 확인", "오늘의집에서 결제"]
for i in range(4):
    y = 232 + i * 62
    d.rect(s, X2[0] + 40, y, W2 - 80, 40, radius=10, fill="FFFFFF", alpha=60)
    d.text(s, X2[0] + 40, y, W2 - 80, 40, left[i], 15, "semibold", "404040", align="center", anchor="middle", check=False)
    last = i == 3
    if last:
        d.rect(s, X2[1] + 40, y, W2 - 80, 40, radius=10, gradient=(C["blue_deep"], C["blue_end"]))
    else:
        d.rect(s, X2[1] + 40, y, W2 - 80, 40, radius=10, fill=MIST)
    d.text(s, X2[1] + 40, y, W2 - 80, 40, right[i], 15, "semibold", "FFFFFF" if last else PRI, align="center", anchor="middle",
           check=False)
    if i < 3:
        d.down_arrow(s, X2[0] + W2 / 2 - 9, y + 45, 18, 9, fill="7E7E7E")
        d.down_arrow(s, X2[1] + W2 / 2 - 9, y + 45, 18, 9, fill=PRI)
d.chevron(s, 465, 320, 26, 56)
d.footnote(s, ["전략 가설 : 단순 상품 나열이면 방어력이 약함 — 검수된 SKU·PB/단독·협업 구성이 확보된 회차부터 실험"], w=700)
note(s, "남의 집 사진을 더 보여주는 것은 발견을 돕습니다. 하지만 필요한 것은 그 장면을 내 집에서 만들기 위해 무엇을 사야 하는지까지 결정하는 경험입니다.")

# 11 ─────────────
s = d.content_slide("Target", "1차 대상은 '공간 활용형 가구·수납·조명'을 고민하는 고객",
                    "크기·배치·조합이 중요해, 단품 가격 비교만으로는 결정하기 어려운 구매 상황입니다.")
cats = [("범용 생활용품", "가격·배송·익숙함", "일반 상품 판매", "메인 제외", "grey"),
        ("디자인 소품·패브릭", "분위기·취향·연출", "집들이·사진·단독 상품", "보조 상품", "white"),
        ("공간 활용형\n가구·수납·조명", "크기·배치·사용 목적·조합", "실제 집 사례·리뷰·상품·일부 설치", "우선 대상", "outline"),
        ("전면 리모델링", "품질·견적·업체·일정", "일부 시공 자산", "1차 범위 제외", "grey")]
cw4 = (CW - 3 * 12) / 4
for i, (t, f_, a, j, st) in enumerate(cats):
    x = L + i * (cw4 + 12)
    d.card(s, x, 158, cw4, 325, st)
    if st == "outline":
        d.highlight_bar(s, x + 12, 170, cw4 - 24, "우선 대상", h=32, size=15)
    else:
        d.tag(s, x + (cw4 - 110) / 2, 175, 110, j, "dark" if st == "grey" else "mist", h=24)
    d.text(s, x + 10, 216, cw4 - 20, 48, t, 17, "bold", PRI if st == "outline" else C["ink"], align="center",
           anchor="middle", line_spacing=1.2)
    d.line(s, x + 20, 276, x + cw4 - 20, 276, color="C9CDD3", dash="sysDot")
    d.text(s, x + 14, 290, cw4 - 28, 16, "고객이 따지는 것 (가설)", 11, "bold", C["muted"], align="center", check=False)
    d.text(s, x + 14, 310, cw4 - 28, 46, f_, 14, "semibold", C["ink"], align="center", line_spacing=1.25)
    d.text(s, x + 14, 368, cw4 - 28, 16, "연결 가능한 오늘의집 자산", 11, "bold", C["muted"], align="center", check=False)
    d.text(s, x + 14, 388, cw4 - 28, 60, a, 14, "semibold", PRI if st == "outline" else C["ink"], align="center",
           line_spacing=1.25)
d.footnote(s, ["근거 : 오늘의집 슬림수납장·1인용 가구 검색 증가 보도(2026) — 검색 증가가 거래액 증가를 뜻하지는 않음",
               "타깃 : 지금 집의 특정 공간 문제를 해결하려는 사람. 20~30대 1~2인 가구는 초기 크리에이티브 후보"], w=880, bottom=512)

# 12 BIG IDEA ─────
s = d.prs.slides.add_slide(d._blank)
d._slide_idx += 1
d.rect(s, 0, 0, W, H, gradient=("0D5C74", "07475A", 90))
slot(s, 0, 0, W, H, "배경 키비주얼 — 현실적인 작은 방의 BEFORE → 변화 후 장면 (어두운 오버레이)", dark=True, label_y=470)
d.rect(s, 0, 0, W, H, fill="062F3B", alpha=55)
d.text(s, 0, 112, W, 18, "BIG IDEA", 13, "bold", "8DCFE4", align="center", check=False)
d.text(s, 0, 140, W, 70, "우리 집의 다음 장면", 54, "bold", "FFFFFF", align="center", check=False)
d.text(s, 0, 222, W, 26, "마음에 드는 집을 보는 것에서, 내가 살고 싶은 집을 만드는 것으로", 19, "medium", "DDF0F6",
       align="center", check=False)
pw = 176
gp = (CW - 4 * pw) / 3
for i, (no, nm, st) in enumerate(PROG):
    x = L + i * (pw + gp)
    d.rect(s, x, 300, pw, 74, radius=14, fill="FFFFFF", alpha=94 if i != 2 else 100, line=None if i != 2 else "8DCFE4", line_w=1.5)
    d.text(s, x, 312, pw, 14, f"{st}  ·  PROGRAM {no}", 10.5, "bold", LBL, align="center", check=False)
    d.text(s, x, 332, pw, 26, nm, 17, "bold", C["ink"], align="center", check=False)
    if i < 3:
        d._fade_arrow(s, x + pw + 6, x + pw + gp - 6, 337, color="8DCFE4")
d.text(s, 0, 400, W, 20, "\"우리 집에서 바꾸고 싶은 한 장면은?\" — 발견하고, 고르고, 오늘의집에서 사고, 다시 보여준다", 14, "medium",
       "BCE3EF", align="center", check=False)
note(s, "이 콘셉트는 슬로건이 아니라, 고객이 다음 장면을 발견하고 선택하고 구매하고 공유하는 네 단계로 작동합니다.")

# ══ PART D ════════════════════════════════════════════════════════
divider(3, "사연에서 집들이까지", "\"우리 집에서 바꾸고 싶은 한 장면은?\" — 네 개의 프로그램을 하나의 구매 여정으로 잇습니다.", "14–22")

# 13 IMC Overview ─
s = d.content_slide("IMC Overview", "사연 → 밸런스게임 → 키트 → 집들이, 한 여정으로 잇는 4개 프로그램",
                    "모든 프로그램은 같은 '공간 고민'으로 연결되고, 마지막에는 오늘의집 결제로 모입니다.")
cw4 = (CW - 3 * 12) / 4
xs4 = [L + i * (cw4 + 12) for i in range(4)]
pill_row(s, xs4, [cw4] * 4, 162, [f"{p[2]} · {p[0]}" for p in PROG], ["soft", "soft", "blue", "soft"])
info = [("장면 사연함", "바꾸고 싶은 공간 고민을\n고르고 사연을 보냄", "숏폼 · 인스타 · 기획전", "고민 선택률"),
        ("장면 밸런스게임", "같은 방 A/B 중\n우리 집 장면을 고름", "크리에이터 · 유튜브 · 앱", "A/B 선택 완료율"),
        ("장면 키트", "그 장면을 만드는 상품을\n오늘의집에서 결제", "앱 기획전 · 상품 페이지", "SKU 구매 전환율"),
        ("장면 집들이", "달라진 집을 공유해\n다음 고객의 근거로", "숏폼 · 후기 · 커뮤니티", "후기 생성률")]
for i, x in enumerate(xs4):
    d.card(s, x, 215, cw4, 268, "outline" if i == 2 else "white")
    d.text(s, x, 234, cw4, 24, info[i][0], 18, "bold", PRI if i == 2 else C["ink"], align="center", check=False)
    d.text(s, x + 10, 268, cw4 - 20, 44, info[i][1], 13.5, "medium", C["text"], align="center", line_spacing=1.3)
    d.line(s, x + 20, 326, x + cw4 - 20, 326, color="C9CDD3", dash="sysDot")
    d.text(s, x, 340, cw4, 14, "채널", 11, "bold", C["muted"], align="center", check=False)
    d.text(s, x + 10, 358, cw4 - 20, 20, info[i][2], 13, "semibold", C["ink"], align="center", check=False)
    d.text(s, x, 392, cw4, 14, "핵심 지표", 11, "bold", C["muted"], align="center", check=False)
    if i == 2:
        d.highlight_bar(s, x + 16, 412, cw4 - 32, info[i][3], h=34, size=14)
    else:
        d.tag(s, x + 24, 418, cw4 - 48, info[i][3], "mist", h=26, size=12.5)

# 14–17 Programs ──
def program(idx, headline, sub, steps, mock, kpi, extra_note=None):
    no, nm, st = PROG[idx]
    s = d.content_slide(f"Program {no}  ·  {st}", headline, sub)
    for i, (t, desc) in enumerate(steps):
        y = 158 + i * 111
        d.card(s, L, y, 520, 100, "outline" if (idx == 2 and i == 2) else "white")
        d.number_badge(s, L + 34, y + 50, str(i + 1), r=14)
        d.text(s, L + 64, y + 18, 440, 22, t, 16.5, "semibold", C["ink"], check=False)
        d.text(s, L + 64, y + 46, 440, 44, desc, 13, "regular", C["text"], line_spacing=1.3)
    d.card(s, 574, 158, 348, 258, "solid")
    d.tag(s, 590, 170, 76, "기획 시안", "dark", h=20, size=10)
    mock(s)
    d.card(s, 574, 426, 348, 57, "white")
    d.text(s, 590, 426, 70, 57, "성공 지표", 12, "bold", LBL, anchor="middle", check=False)
    d.text(s, 660, 426, 250, 57, kpi, 12.5, "semibold", C["ink"], anchor="middle", line_spacing=1.25)
    if extra_note:
        note(s, extra_note)
    return s


def mock_cards(s):
    for i, t in enumerate(["좁은 침실", "수납 부족", "재택 공간", "작은 거실"]):
        x = 596 + (i % 2) * 158
        y = 200 + (i // 2) * 102
        slot(s, x, y, 146, 92, f"고민 카드 · {t}", prefix=False)


def mock_ab(s):
    slot(s, 590, 196, 154, 206, "A안 · 수납 중심\n선반·정리 도구·조명", prefix=False)
    slot(s, 752, 196, 154, 206, "B안 · 휴식 중심\n낮은 테이블·조명·의자", prefix=False)
    d.text(s, 734, 285, 28, 28, "vs", 13, "bold", PRI, align="center", anchor="middle", check=False)


def mock_kit(s):
    phone(s, 690, 192, 100, "키트 상품 목록\n규격·선택 이유\n가격·배송 조건")
    phone(s, 810, 192, 100, "오늘의집\n상품 상세·결제")


def mock_board(s):
    for i, t in enumerate(["BEFORE · 불편", "A/B 선택", "설치·사용", "AFTER · 완성"]):
        x = 596 + (i % 2) * 158
        y = 200 + (i // 2) * 102
        slot(s, x, y, 146, 92, f"{i + 1}컷 · {t}", prefix=False)


program(0, "장면 사연함 — '바꾸고 싶은 한 장면'을 받는 데서 캠페인 시작",
        "사진 없이도 고민을 고를 수 있게 해 참여 문턱을 낮추고, 고른 고민을 다음 단계로 넘깁니다.",
        [("숏폼·카드뉴스·기획전에서 질문을 던짐", "\"퇴근하면 가방부터 바닥에 내려놓는 방. 당신의 다음 장면은?\"\n좁은 침실·수납 부족·재택 공간·작은 거실 고민 카드"),
         ("고민 카드를 고르면 비슷한 집 사례로 연결", "사진 업로드 없이 선택만으로 참여. 원하면 실제 공간 사진과\n고민 한 줄을 보내고, 일부 사연은 다음 단계 콘텐츠로 제작"),
         ("고른 고민 태그가 밸런스게임·키트로 이어짐", "같은 고민 ID로 다음 프로그램과 연결. 사진·사연 재사용은\n동의 필수, 제작 혜택을 모든 참여자에게 보장하지 않음")],
        mock_cards, "고민 선택률 · 사례 탐색 진입률\n유입 후 상품 탐색률")

program(1, "장면 밸런스게임 — 같은 방, A와 B 중 우리 집의 다음 장면 고르기",
        "완성된 집을 보여주는 비포·애프터와 달리, 고객이 앞으로 만들 장면을 직접 고르게 합니다.",
        [("같은 공간 고민에 현실적인 두 가지 방향 제시", "예) 원룸 창가 — A 수납 중심 / B 휴식 중심\n두 안 모두 실제로 설치 가능한 상품만 연결"),
         ("크리에이터가 장점과 포기한 것까지 설명", "문제 → 우선순위 → 장점·포기한 것 → 선택 이유 → 필요한 제품\n숏폼 15~30초 · 유튜브 2~4분 · 인스타 캐러셀"),
         ("고객은 '우리 집은 A / B'를 고르고 키트로 이동", "앱 A/B 비교 카드에서 선택 → 해당 장면 키트로 연결\n정답 투표가 아니라 내 상황에 맞는 방향 고르기")],
        mock_ab, "A/B 선택 완료율 · 선택 후 키트 클릭\n상품 후보 저장률")

program(2, "장면 키트 — 고른 장면을 만드는 상품을 오늘의집에서 한 번에 결제",
        "캠페인 전체에서 구매 전환을 담당하는 장치로, 링크 모음이 아니라 '선택 이유가 붙은 조합'입니다.",
        [("공간 문제 중심으로 3~5개 상품을 조합", "'예쁜 조명 추천'이 아니라 '작은 침실 동선 확보' 같은 쓰임새 제안\n예) 6평 침실 — 좁은 수납장 · 침대 아래 수납 · 벽면 조명"),
         ("규격·선택 이유와 함께 부적합 조건까지 고지", "판매 가능한 SKU만 연결(재고·규격·배송·설치 확인)\n동일 제품과 대체 제품을 구분해 표기"),
         ("필요한 상품만 골라 오늘의집에서 결제", "PB·단독·협업 전용 구성을 우선 검토, 미확보 시 독점 표기 금지\n할인 묶음이 아니라 '구매 목적의 조합' — 전체 결제를 강요하지 않음")],
        mock_kit, "키트 → 상품 상세 클릭률 · SKU 구매 전환율\n구매자 수 · 거래액")

s = d.content_slide("Program 03  ·  구매", "고객이 보는 화면은 고민 선택에서 오늘의집 결제까지 네 단계",
                    "기존 기획전·콘텐츠 편집으로 시작할 수 있는 범위로 설계했습니다.")
cw4 = (CW - 3 * 12) / 4
xs4 = [L + i * (cw4 + 12) for i in range(4)]
pill_row(s, xs4, [cw4] * 4, 162, ["1 · 고민 선택", "2 · 밸런스게임", "3 · 장면 키트", "4 · 상품 페이지"], ["soft", "soft", "soft", "blue"])
scr = [("고민 태그 화면", "'수납 부족', '일·휴식 분리' 등\n나의 고민을 고름"),
       ("A/B 장면 비교 화면", "실제 사례·변화 이유·사용 조건을\n보고 장면 선택"),
       ("키트 상품 목록 화면", "상품 3~5개의 규격·선택 이유\n가격·배송·설치 조건 확인"),
       ("상품 상세·결제 화면", "옵션·판매가·배송 확인 후\n오늘의집에서 결제")]
for i, x in enumerate(xs4):
    d.card(s, x, 215, cw4, 268, "outline" if i == 3 else "white")
    phone(s, x + cw4 / 2, 228, 92, scr[i][0])
    d.text(s, x + 8, 425, cw4 - 16, 44, scr[i][1], 12.5, "medium", C["ink"], align="center", line_spacing=1.3)
d.footnote(s, ["캠페인 제안 : 상품 3~5개는 가상 운영 가정 · 현재 오늘의집 기능(상품 태그·3D·AR 등)을 새 기능으로 발표하지 않음"], w=880)

program(3, "장면 집들이 — 달라진 우리 집이 다음 고객의 선택 근거가 되는 순환",
        "오늘의집의 대표 포맷인 '집들이'를 구매 후기로 바꿔, 실제 변화 콘텐츠를 다시 키트로 연결합니다.",
        [("선정된 공간의 실제 변화 과정을 20초 숏폼으로", "0~3초 BEFORE '이 좁은 방, 바뀔 수 있을까?' → A/B 선택 이유\n→ 배치·사용 → AFTER + '이 장면을 만든 상품은 오늘의집에서'"),
         ("구매 고객이 '왜 골랐는지'를 집들이로 공유", "선택 이유 · 실제 사용 · 아쉬운 점까지 사진·영상으로 기록\n이용 동의 후 다음 고객의 선택 자료로 재편집"),
         ("기존 비포·애프터 영상은 이 프로그램으로 흡수", "주기적 비포·애프터 업로드가 메인이 아님\n일부 SKU만 기존 매장 체험과 연계(대규모 팝업 전제 X)")],
        mock_board, "콘텐츠 → 키트 클릭률 · 구매 후 후기 생성률\n후기 기반 재방문율")

# 18 Channel ─────
s = d.content_slide("Channel", "매체별 역할은 달라도, 고객에게 전달하는 다음 행동은 하나",
                    "어떤 채널이든 같은 공간 고민과 장면 키트로 연결하고, 브랜드 홈으로 흘려보내지 않습니다.")
d.highlight_bar(s, L, 158, CW, "모든 접점  →  같은 공간 고민  →  장면 키트  →  오늘의집 결제", h=40, size=17)
ch = [("Paid", "메타 · 유튜브 · 디지털", "문제 공감 숏폼", "인지·유입", "고민 선택 페이지"),
      ("Owned", "앱 · 기획전", "밸런스게임 + 장면 키트", "고려·구매", "SKU 상세·결제"),
      ("Creator", "릴스 · 유튜브 · 커뮤니티", "선택 이유와 실제 변화", "고려·확산", "해당 에피소드 키트"),
      ("UGC", "장면 집들이", "구매 고객의 실제 후기", "구매 후 신뢰", "다음 고객의 사례"),
      ("Offline (선택)", "기존 매장 일부", "체험 가능한 SKU 시연", "고관여 확신", "QR → 해당 키트"),
      ("CRM (2단계)", "앱 푸시 · 알림", "관심 상품의 사용 사례", "재고려", "동의·정책 확인 후")]
for i, (nm, med, msg, role, nxt) in enumerate(ch):
    x = X3[i % 3]
    y = 212 + (i // 3) * 138
    d.card(s, x, y, W3, 128, "outline" if nm == "Owned" else ("grey" if "2단계" in nm else "white"))
    d.tag(s, x + 16, y + 14, 110, nm, "grad" if nm == "Owned" else ("dark" if "2단계" in nm else "blue"), h=24, size=12)
    d.text(s, x + 136, y + 14, W3 - 150, 24, med, 11.5, "medium", C["muted"], anchor="middle", check=False)
    d.text(s, x + 16, y + 48, W3 - 32, 22, msg, 15.5, "bold", C["ink"], check=False)
    d.text(s, x + 16, y + 76, W3 - 32, 18, f"[[{role}]]", 12.5, "semibold", C["ink"], check=False)
    d.text(s, x + 16, y + 98, W3 - 32, 18, f"→ {nxt}", 12.5, "semibold", PRI, check=False)
note(s, "스크랩 기반 CRM은 상품·콘텐츠 매핑, 수신 동의, 데이터 정책 확인 뒤 2단계로 제안한다.")

# 19 Journey ─────
s = d.content_slide("Customer Journey", "관심에서 공유까지, 단계마다 고객의 말·접점·행동·지표를 설계",
                    "고객의 한마디가 다음 단계로 넘어가는 이유가 되도록 접점을 배치했습니다.")
st5 = ["관심", "고려", "검토", "구매", "사용·공유"]
lw_, cw5 = 112, (CW - 112 - 10 - 4 * 8) / 5
xs5 = [L + lw_ + 10 + i * (cw5 + 8) for i in range(5)]
for i, t in enumerate(st5):
    d.pill(s, xs5[i], 158, cw5, t, style="blue" if i == 3 else "soft", tail=False, h=30)
rows = [("고객의 말", ["\"우리 집에도\n저런 문제가 있어\"", "\"A/B 중 내가\n원하는 건?\"", "\"실제로 뭘\n사야 하지?\"", "\"이 조건이면\n여기서 사자\"", "\"우리 집은 이렇게\n바뀌었어\""]),
        ("접점", ["장면 사연함\n광고·고객 사연", "장면 밸런스게임", "장면 키트", "오늘의집\n상품 페이지", "장면 집들이"]),
        ("핵심 행동", ["고민 선택", "장면 선택", "SKU 상세·조건 확인", "**결제**", "사진·선택 이유 공유"]),
        ("측정", ["진입률", "선택 완료율", "상세 클릭률", "**구매율·구매자 수·거래액**", "UGC·재구매"])]
for r_, (lab, cells) in enumerate(rows):
    y = 200 + r_ * 72
    d.rect(s, L, y, lw_, 64, radius=12, fill="E2E4E8")
    d.text(s, L, y, lw_, 64, lab, 13.5, "bold", C["text"], align="center", anchor="middle", check=False)
    for i, c in enumerate(cells):
        hot = i == 3
        d.card(s, xs5[i], y, cw5, 64, "outline" if (hot and r_ == 2) else "white", radius=12)
        d.text(s, xs5[i] + 6, y, cw5 - 12, 64, c, 12.5 if r_ == 0 else 13, "medium" if r_ == 0 else "semibold",
               PRI if hot else C["ink"], align="center", anchor="middle", line_spacing=1.2)

# 20 Roadmap ─────
s = d.content_slide("Roadmap", "12주 동안 파일럿에서 확장까지, 단계마다 통과 기준으로 판단",
                    "전환이 확인된 조합만 키우고, 가격·배송 경쟁력이 크게 떨어지는 SKU는 소재로 밀지 않습니다.")
ph = [("1~2주", "준비", 2), ("3~4주", "파일럿", 2), ("5~8주", "확대", 4), ("9~12주", "확장", 4)]
tw = CW / 12
x = L
for i, (wk, nm, n) in enumerate(ph):
    w = tw * n - 4
    d.rect(s, x, 158, w, 34, radius=8, gradient=(C["blue_deep"], C["blue_end"]) if i == 1 else None,
           fill=None if i == 1 else ("D5EAF2" if i != 1 else None))
    d.text(s, x, 158, w, 34, f"{wk}  ·  {nm}", 13.5, "bold", "FFFFFF" if i == 1 else C["navy"], align="center",
           anchor="middle", check=False)
    x += tw * n
for k in range(13):
    d.line(s, L + tw * k, 198, L + tw * k, 204, color="9AA0AA", w=0.75)
RM = [("준비", ["문제별 고객 사례·콘텐츠 권리 확보", "SKU·가격·배송·설치 검수", "추적 이벤트 설계"], "구매 가능한 키트 2개\n+ 권리 검수 완료"),
      ("파일럿", ["공간 고민 2개로 시작", "밸런스게임 콘텐츠·기획전·광고 연계"], "방문 → 상품 → 구매\n흐름 정상 작동"),
      ("확대", ["반응 좋은 고민 중심 크리에이터 확대", "실제 구매 후기(집들이) 추가"], "비교 그룹 대비\n구매 전환 확인"),
      ("확장", ["우수 조합 확장", "파트너 협업 검토", "동의 기반 리마케팅"], "구매자·거래액·효율\n반품 점검")]
rw4 = (CW - 3 * 12) / 4
for i, (nm, acts, gate) in enumerate(RM):
    x = L + i * (rw4 + 12)
    d.card(s, x, 216, rw4, 267, "outline" if i == 1 else "white", radius=14)
    d.text(s, x, 232, rw4, 22, nm, 17, "bold", PRI if i == 1 else C["ink"], align="center", check=False)
    d.line(s, x + 16, 262, x + rw4 - 16, 262, color="C9CDD3", dash="sysDot")
    d.text(s, x + 16, 272, 80, 16, "실행", 11, "bold", C["muted"], check=False)
    d.bullets(s, x + 16, 292, rw4 - 28, acts, size=13, color=C["ink"], gap=1.45, weight="medium")
    d.rect(s, x + 12, 405, rw4 - 24, 66, radius=10, fill=MIST if i != 1 else None,
           gradient=(C["blue_deep"], C["blue_end"]) if i == 1 else None)
    d.text(s, x + 12, 411, rw4 - 24, 14, "통과 기준", 10.5, "bold", "FFFFFF" if i == 1 else LBL, align="center", check=False)
    d.text(s, x + 16, 428, rw4 - 32, 38, gate, 13, "semibold", "FFFFFF" if i == 1 else PRI, align="center",
           line_spacing=1.2)

# ══ PART E ════════════════════════════════════════════════════════
divider(4, "무엇에 쓰고, 무엇으로 증명하나", "가상 RFP 예산 10억 원의 배분과, 캠페인이 만든 구매 변화를 확인하는 방법", "23–24")

# 21 Budget ─────
s = d.content_slide("Budget", "가상 예산 10억 원 중 70%를 구매와 직접 연결되는 접점에 배분",
                    "화제성보다 '장면 키트' 구매 경험을 만드는 데 집중하고, 효과가 확인된 곳에 증액합니다.")
bud = [("퍼포먼스·매체 운영", 30, "3.0억"), ("실제 사례·크리에이터 콘텐츠", 20, "2.0억"), ("장면 키트·브랜드 협업 운영", 20, "2.0억"),
       ("소비자 참여·UGC 운영", 10, "1.0억"), ("앱 기획전·CRM 운영", 10, "1.0억"), ("오프라인 소규모 체험", 5, "0.5억"),
       ("측정·실험", 5, "0.5억")]
cols_ = ["0B5A73", "0E7FA5", "34ACD4", "8DCFE4", "BCE3EF", "D5DBE0", "C3C4C4"]
d.card(s, L, 158, 330, 325, "white")
d.donut(s, L + 25, 175, 280, 260, [b[0] for b in bud], [b[1] for b in bud], colors=cols_, hole=62)
d.text(s, L, 280, 330, 34, "10억 원", 26, "bold", C["ink"], align="center", check=False)
d.text(s, L, 314, 330, 16, "가상 RFP 총예산", 11, "medium", C["muted"], align="center", check=False)
d.text(s, L + 20, 448, 290, 18, "팀의 초기 배분 가정이며 실제 견적 아님", 11, "medium", C["muted"], align="center", check=False)
d.card(s, 382, 158, 540, 325, "white")
for i, (nm, p, amt) in enumerate(bud):
    y = 178 + i * 36
    d.rect(s, 402, y + 9, 12, 12, fill=cols_[i], radius=3)
    d.text(s, 424, y, 210, 30, nm, 13.5, "semibold" if i < 3 else "medium", C["ink"], anchor="middle", check=False)
    d.rect(s, 640, y + 8, 180 * p / 30, 14, radius=4, fill=cols_[i])
    d.text(s, 826, y, 40, 30, f"{p}%", 13.5, "bold", PRI if i < 3 else C["ink"], anchor="middle", check=False)
    d.text(s, 866, y, 46, 30, amt, 12, "medium", C["muted"], align="right", anchor="middle", check=False)
d.highlight_bar(s, 402, 436, 500, "구매 직결 접점(매체·콘텐츠·키트) 70% 집중", h=34, size=14.5)
d.footnote(s, ["SKU 협업·크리에이터 출연료·시공비·계측 비용은 현재 견적 근거 없음 — 테스트 후 재배분"], bottom=510, w=600)

# 22 KPI ─────
s = d.content_slide("KPI", "성공은 조회 수가 아닌 '노출·비노출 그룹의 구매 전환 차이'로 판단",
                    "단순 전후 매출 비교나 참여자 구매율만으로 캠페인 효과를 확정하지 않습니다.")
tiers = [("선행 지표", "white", ["광고 → 고민 선택 진입률", "밸런스게임 A/B 선택률", "키트 → SKU 상세 클릭률"]),
         ("핵심 · 사업 지표", "outline", ["노출·비노출 그룹의\nSKU 구매 전환율 차이", "고유 구매자 수", "커머스 거래액 (환불 반영)"]),
         ("품질 · 장기 지표", "white", ["반품률 · 고객 획득비용", "매출총이익 (가능 시)", "브랜드 연상 · 재방문 · 재구매"])]
pill_row(s, X3, [W3] * 3, 162, [t[0] for t in tiers], ["soft", "blue", "soft"], flow=False)
for i, x in enumerate(X3):
    d.card(s, x, 215, W3, 190, tiers[i][1])
    if i == 1:
        d.highlight_bar(s, x + 16, 228, W3 - 32, "핵심 KPI", h=28, size=13)
        d.text(s, x + 10, 264, W3 - 20, 50, tiers[i][2][0], 17, "bold", PRI, align="center", line_spacing=1.25)
        d.line(s, x + 24, 322, x + W3 - 24, 322, color="C9CDD3", dash="sysDot")
        d.bullets(s, x + 40, 334, W3 - 70, tiers[i][2][1:], size=14, color=C["ink"], gap=1.5, weight="semibold")
    else:
        for k, it in enumerate(tiers[i][2]):
            yy = 236 + k * 54
            d.rect(s, x + 18, yy, W3 - 36, 44, radius=10, fill="F3F6F7")
            d.text(s, x + 18, yy, W3 - 36, 44, it, 14, "semibold", C["ink"], align="center", anchor="middle", check=False)
steps3 = ["비노출 / 일반 기획전 그룹과 무작위 비교", "기간·SKU·신규/기존·유입경로 통제", "노출 → 고민 → 키트 → 상세 → 결제 로그 연결"]
d.text(s, L, 418, 120, 18, "검증 설계", 13, "bold", C["ink"], check=False)
for i, t in enumerate(steps3):
    x = X3[i]
    d.rect(s, x, 442, W3, 40, radius=12, fill=MIST)
    d.number_badge(s, x + 22, 462, str(i + 1), r=11)
    d.text(s, x + 42, 442, W3 - 50, 40, t, 12.5, "semibold", PRI, anchor="middle", check=False)
note(s, "결과가 나쁘면 화제성이 아니라 상품 구성·실제 가격 경쟁력·전환 경로를 먼저 재점검한다.")

# ══ Closing ═══════════════════════════════════════════════════════
s = d.prs.slides.add_slide(d._blank)
d._slide_idx += 1
d.rect(s, 0, 0, W, H, gradient=("0D5C74", "07475A", 90))
d._network(s, 600, 330, 340, 200, seed=5, n=18)
d.text(s, 60, 200, W - 120, 90, "〈우리 집의 다음 장면〉으로,\n오늘의집에서 찾고 오늘의집에서 사는 경험을 만들겠습니다.", 27.7, "medium",
       "FFFFFF", align="center", line_spacing=1.35)
d.text(s, 0, 330, W, 20, "감사합니다", 15, "semibold", "8DCFE4", align="center", check=False)

# ══ Appendix ══════════════════════════════════════════════════════
s = d.content_slide("Appendix", "출처 · 조사 한계 · 표기 규칙 · 생성형 AI 활용", None, appendix=True)
secs = [("주요 출처", ["[1] 오늘의집 공식 2025 실적 발표 — ohstory.io/press/pressrelease/15242",
                    "[2] 오늘의집 공간 효율형 수납 검색 관련 보도 — ohstory.io/press/media/16002",
                    "[3] 오늘의집 1인용 가구 검색 관련 보도 — ohstory.io/press/media/15915",
                    "[4] 자체 2차 설문 (n=51)   [5] 자체 고객 인터뷰 (n=5)   [6] 팀 작성 가상 RFP"]),
        ("조사 한계", ["2차 설문 n=51은 40대 이상 49%, 자가 57%로 20~30대 임차 가구를 대표하지 않음",
                    "최초 발견처–구매처 일치 비율(7/12 등)은 서비스 전환율이 아니라 자체 조사 응답 비율",
                    "공간 조합·선택 경험이 가격·배송 혜택을 넘어설 만큼 가치 있는지는 인과 증거가 없어 실험 설계와 함께 제안"]),
        ("표기 규칙 · AI 활용", ["확인된 사실 / 팀 관찰 / 전략적 해석 / 캠페인 제안을 각주에 구분 표기. 화면·이미지는 모두 기획 시안",
                             "생성형 AI는 자료 구조화, 설문 집계 보조, 문안 초안, 장표 레이아웃 제작에 활용. 수치·출처는 원자료와 대조"])]
y = 150
for t, ls in secs:
    d.text(s, L, y, 400, 18, t, 14, "bold", LBL, check=False)
    d.bullets(s, L, y + 24, CW, ls, size=12, color=C["text"], gap=1.35, weight="regular")
    y += 30 + 21 * len(ls) + 18

d.save(OUT)
print("saved", OUT, "slides:", len(d.prs.slides))
print("warnings:", len(d.warnings))
for w in d.warnings:
    print("  -", w)
