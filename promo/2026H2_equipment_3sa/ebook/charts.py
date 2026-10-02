"""본문에 들어가는 SVG 차트·도식.

마크다운 안의 `<!--chart:이름-->` 줄을 build.py가 여기서 만든 <figure>로 바꾼다.
회사 색은 모든 차트에서 같다(램리서치 파랑, AMAT 주황, TEL 청록).
"""
import html
import re

INK, SUB, MUTED, GRID, SURF = "#1B2333", "#5B6475", "#8A93A3", "#E3E7EE", "#FFFFFF"
GRAY = "#B8C0CE"
CO = {"lam": "#2a78d6", "amat": "#eb6834", "tel": "#1baf7a"}
CO_NAME = {"lam": "램리서치", "amat": "AMAT", "tel": "TEL"}
W = 640


def esc(s):
    return html.escape(str(s))


def text(x, y, s, size=11, fill=INK, anchor="start", weight=400, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" {extra}>{esc(s)}</text>')


def svg(h, body, label):
    return (f'<svg viewBox="0 0 {W} {h}" width="100%" role="img" aria-label="{esc(label)}" '
            f'xmlns="http://www.w3.org/2000/svg" style="font-family:Pretendard,sans-serif">{body}</svg>')


def figure(title, body_svg, note=""):
    cap = f'<figcaption>{esc(note)}</figcaption>' if note else ""
    return f'<figure class="chart"><div class="ct">{esc(title)}</div>{body_svg}{cap}</figure>'


def legend(items, x, y):
    out, cx = [], x
    for key, name in items:
        out.append(f'<rect x="{cx}" y="{y - 8}" width="10" height="10" rx="2" fill="{CO[key]}"/>')
        out.append(text(cx + 15, y + 1, name, 10.5, SUB))
        cx += 15 + len(name) * 9 + 22
    return "".join(out)


def spread(items, gap=13):
    """라벨 y좌표가 겹치지 않게 위아래로 밀어낸다. items: [(y, payload)]"""
    items = sorted(items, key=lambda t: t[0])
    for i in range(1, len(items)):
        if items[i][0] - items[i - 1][0] < gap:
            items[i] = (items[i - 1][0] + gap, items[i][1])
    return items


# ---------------------------------------------------------------- 가로 막대
def hbar(title, rows, unit="%", vmax=None, note=""):
    """rows: [(라벨, 값, 회사키 or None)]"""
    vmax = vmax or max(v for _, v, _ in rows) * 1.15
    left, right, top, bh, gap = 92, 60, 10, 18, 10
    h = top + len(rows) * (bh + gap) + 6
    pw = W - left - right
    b = []
    for i, (lab, v, key) in enumerate(rows):
        y = top + i * (bh + gap)
        w = max(2, pw * v / vmax)
        col = CO.get(key, GRAY)
        b.append(text(left - 10, y + bh / 2 + 4, lab, 11, INK if key else SUB, "end", 600 if key else 400))
        b.append(f'<path d="M{left},{y} h{w - 4} q4,0 4,4 v{bh - 8} q0,4 -4,4 h-{w - 4} z" fill="{col}"/>')
        b.append(text(left + w + 6, y + bh / 2 + 4, f"+{v:g}{unit}" if v > 0 else f"{v:g}{unit}", 11, INK, weight=600))
    b.append(f'<line x1="{left}" y1="{top - 4}" x2="{left}" y2="{h - 6}" stroke="{SUB}" stroke-width="1"/>')
    return figure(title, svg(h, "".join(b), title), note)


# ---------------------------------------------------------------- 꺾은선
def line(title, xlabels, series, ymin, ymax, ystep, unit="%", note="", fmt="{:g}"):
    """series: [(회사키, [값 or None ...])] — xlabels와 같은 길이"""
    left, right, top, bottom = 40, 118, 12, 26
    h = 230
    pw, ph = W - left - right, h - top - bottom
    X = lambda i: left + pw * i / (len(xlabels) - 1)
    Y = lambda v: top + ph * (1 - (v - ymin) / (ymax - ymin))
    b = []
    v = ymin
    while v <= ymax + 1e-9:
        y = Y(v)
        b.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + pw}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        b.append(text(left - 6, y + 3.5, fmt.format(v) + unit, 9.5, MUTED, "end"))
        v += ystep
    for i, lab in enumerate(xlabels):
        b.append(text(X(i), h - 8, lab, 9.5, SUB, "middle"))
    ends = []
    for key, vals in series:
        pts = [(X(i), Y(v)) for i, v in enumerate(vals) if v is not None]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        b.append(f'<path d="{d}" fill="none" stroke="{CO[key]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
        for x, y in pts:
            b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{CO[key]}" stroke="{SURF}" stroke-width="2"/>')
        last = [v for v in vals if v is not None][-1]
        ends.append((pts[-1][1], (key, pts[-1][0], last)))
    for y, (key, x, last) in spread(ends, 14):
        b.append(text(left + pw + 10, y + 4, f"{CO_NAME[key]} {fmt.format(last)}{unit}", 10.5, INK, weight=600))
    b.append(f'<line x1="{left}" y1="{top + ph}" x2="{left + pw}" y2="{top + ph}" stroke="{SUB}" stroke-width="1"/>')
    return figure(title, svg(h, "".join(b), title), note)


# ---------------------------------------------------------------- 누적 막대(고객 집중도)
def stacked(title, rows, vmax=60, note=""):
    """rows: [(회사키, [세그먼트 값...], 끝 라벨)]"""
    left, right, top, bh, gap = 92, 112, 10, 22, 12
    h = top + len(rows) * (bh + gap) + 22
    pw = W - left - right
    sx = lambda v: pw * v / vmax
    b = []
    for t in range(0, vmax + 1, 10):
        x = left + sx(t)
        b.append(f'<line x1="{x:.1f}" y1="{top - 4}" x2="{x:.1f}" y2="{h - 20}" stroke="{GRID}" stroke-width="1"/>')
        b.append(text(x, h - 6, f"{t}%", 9.5, MUTED, "middle"))
    for i, (key, segs, endlab) in enumerate(rows):
        y = top + i * (bh + gap)
        b.append(text(left - 10, y + bh / 2 + 4, CO_NAME[key], 11, INK, "end", 600))
        x = left
        txt = INK if key == "tel" else "#FFFFFF"
        for j, v in enumerate(segs):
            w = sx(v) - 2
            last = j == len(segs) - 1
            if last:
                b.append(f'<path d="M{x:.1f},{y} h{w - 4:.1f} q4,0 4,4 v{bh - 8} q0,4 -4,4 h-{w - 4:.1f} z" fill="{CO[key]}"/>')
            else:
                b.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{bh}" fill="{CO[key]}"/>')
            b.append(text(x + w / 2, y + bh / 2 + 4, f"{v:g}", 10, txt, "middle", 600))
            x += w + 2
        b.append(text(x + 6, y + bh / 2 + 4, endlab, 10.5, INK, weight=600))
    return figure(title, svg(h, "".join(b), title), note)


# ---------------------------------------------------------------- 기울기(이전→최근) 두 패널
def slopes(title, panels, note=""):
    """panels: [(패널 제목, ymin, ymax, [(회사키, (값, 라벨), (값, 라벨))])]"""
    h, top, bottom = 210, 34, 20
    pw_all = W / len(panels)
    b = []
    for p, (ptitle, ymin, ymax, rows) in enumerate(panels):
        ox = p * pw_all
        x1, x2 = ox + 92, ox + pw_all - 92
        Y = lambda v: top + (h - top - bottom) * (1 - (v - ymin) / (ymax - ymin))
        b.append(text(ox + pw_all / 2, 14, ptitle, 11, INK, "middle", 700))
        b.append(f'<line x1="{x1}" y1="{top - 6}" x2="{x1}" y2="{h - bottom + 4}" stroke="{GRID}"/>')
        b.append(f'<line x1="{x2}" y1="{top - 6}" x2="{x2}" y2="{h - bottom + 4}" stroke="{GRID}"/>')
        b.append(text(x1, h - 4, "이전", 9.5, MUTED, "middle"))
        b.append(text(x2, h - 4, "최근", 9.5, MUTED, "middle"))
        L, R = [], []
        for key, (v1, l1), (v2, l2) in rows:
            b.append(f'<line x1="{x1}" y1="{Y(v1):.1f}" x2="{x2}" y2="{Y(v2):.1f}" stroke="{CO[key]}" stroke-width="2"/>')
            for x, v in ((x1, v1), (x2, v2)):
                b.append(f'<circle cx="{x}" cy="{Y(v):.1f}" r="4" fill="{CO[key]}" stroke="{SURF}" stroke-width="2"/>')
            L.append((Y(v1), (key, l1)))
            R.append((Y(v2), (key, l2)))
        for y, (key, l1) in spread(L, 13):
            b.append(text(x1 - 9, y + 4, f"{CO_NAME[key]} {l1}", 10, INK, "end"))
        for y, (key, l2) in spread(R, 13):
            b.append(text(x2 + 9, y + 4, f"{l2} {CO_NAME[key]}", 10, INK))
    return figure(title, svg(h, "".join(b), title), note)


# ---------------------------------------------------------------- 공정별 포지션 매트릭스
def matrix(title, md_table, note=""):
    rows = []
    for ln in md_table.strip().splitlines()[2:]:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        name, vals = cells[0], cells[1:4]
        enc = []
        for c in vals:
            if c.startswith("—") or c in ("-", ""):
                enc.append(0)
            elif "**" in c:
                enc.append(2)
            else:
                enc.append(1)
        rows.append((name, enc))
    left, top, rh = 170, 30, 20
    colw = (W - left - 10) / 3
    h = top + len(rows) * rh + 34
    b = []
    for j, key in enumerate(("lam", "amat", "tel")):
        b.append(text(left + colw * (j + .5), 16, CO_NAME[key], 11.5, INK, "middle", 700))
    for i, (name, enc) in enumerate(rows):
        y = top + i * rh
        if i % 2 == 0:
            b.append(f'<rect x="0" y="{y}" width="{W}" height="{rh}" fill="#F5F7FB"/>')
        b.append(text(left - 12, y + rh / 2 + 4, name, 10.5, INK, "end"))
        for j, key in enumerate(("lam", "amat", "tel")):
            cx, cy = left + colw * (j + .5), y + rh / 2
            if enc[j] == 2:
                b.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="6.5" fill="{CO[key]}"/>')
            elif enc[j] == 1:
                b.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="5.5" fill="{SURF}" stroke="{CO[key]}" stroke-width="2"/>')
            else:
                b.append(f'<line x1="{cx - 4:.1f}" y1="{cy}" x2="{cx + 4:.1f}" y2="{cy}" stroke="{GRAY}" stroke-width="1.5"/>')
    ly = h - 12
    b.append(f'<circle cx="{left}" cy="{ly - 4}" r="6" fill="{INK}"/>')
    b.append(text(left + 12, ly, "대표 영역", 10, SUB))
    b.append(f'<circle cx="{left + 90}" cy="{ly - 4}" r="5" fill="{SURF}" stroke="{INK}" stroke-width="2"/>')
    b.append(text(left + 102, ly, "제품 있음", 10, SUB))
    b.append(f'<line x1="{left + 176}" y1="{ly - 4}" x2="{left + 184}" y2="{ly - 4}" stroke="{GRAY}" stroke-width="1.5"/>')
    b.append(text(left + 192, ly, "주력 제품 없음", 10, SUB))
    return figure(title, svg(h, "".join(b), title), note)


# ---------------------------------------------------------------- 마감 타임라인(간트)
def gantt(title, note=""):
    days = ["9/29", "9/30", "10/1", "10/2", "10/3", "10/4", "10/5", "10/6", "10/7",
            "10/8", "10/9", "10/10", "10/11", "10/12"]
    wd = ["화", "수", "목", "금", "토", "일", "월", "화", "수", "목", "금", "토", "일", "월"]
    left, right, top, rh = 74, 96, 40, 34
    n = len(days)
    cw = (W - left - right) / n
    X = lambda d: left + cw * d
    h = top + 3 * rh + 14
    b = []
    for d in range(n):
        x = X(d)
        if wd[d] in ("토", "일") or days[d] in ("10/3", "10/9"):
            b.append(f'<rect x="{x:.1f}" y="{top - 6}" width="{cw:.1f}" height="{3 * rh + 4}" fill="#F5F7FB"/>')
        b.append(text(x + cw / 2, 14, days[d], 9.5, INK, "middle", 600))
        b.append(text(x + cw / 2, 27, wd[d], 9, MUTED, "middle"))
    # 기준일
    xr = X(2) + cw / 2
    b.append(f'<line x1="{xr:.1f}" y1="{top - 8}" x2="{xr:.1f}" y2="{top + 3 * rh}" stroke="{SUB}" stroke-width="1" stroke-dasharray="3 3"/>')
    plans = [("lam", 1, 8, 5), ("amat", 0, 13, 10)]
    for r, (key, s, e, d3) in enumerate(plans):
        y = top + r * rh
        b.append(text(left - 10, y + 15, CO_NAME[key], 11, INK, "end", 600))
        b.append(f'<rect x="{X(s) + 1:.1f}" y="{y + 4}" width="{X(e + 1) - X(s) - 2:.1f}" height="16" rx="4" fill="{CO[key]}" fill-opacity="0.22"/>')
        b.append(f'<rect x="{X(d3) + 1:.1f}" y="{y + 4}" width="{X(e + 1) - X(d3) - 2:.1f}" height="16" rx="4" fill="{CO[key]}"/>')
        b.append(text(X(d3) + 6, y + 15.5, "D-3 → D-day", 9.5, INK if key == "tel" else "#FFFFFF", weight=600))
        dl = "10/7(수) 23:00" if key == "lam" else "10/12(월) 17:00"
        b.append(text(X(e + 1) + 6, y + 15.5, dl, 10, INK, weight=700))
    y = top + 2 * rh
    b.append(text(left - 10, y + 15, "TEL", 11, INK, "end", 600))
    b.append(f'<rect x="{X(9) + 1:.1f}" y="{y + 4}" width="{X(14) - X(9) + 80:.1f}" height="16" rx="4" fill="none" stroke="{CO["tel"]}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    b.append(text(X(9) + 8, y + 15.5, "공고 오픈 대기 (예년 10월 중순~11월 초)", 9.5, INK))
    b.append(text(xr, top + 3 * rh + 11, "기준일 10/1", 9, SUB, "middle"))
    return figure(title, svg(h, "".join(b), title), note)


# ---------------------------------------------------------------- 단계 흐름도
def flow(title, steps, accent, note=""):
    n = len(steps)
    gap = 8
    bw = (W - gap * (n - 1)) / n
    h = 78
    b = []
    for i, (head, sub) in enumerate(steps):
        x = i * (bw + gap)
        b.append(f'<rect x="{x:.1f}" y="2" width="{bw:.1f}" height="{h - 4}" rx="6" fill="#F5F7FB" stroke="{GRID}"/>')
        b.append(f'<rect x="{x:.1f}" y="2" width="{bw:.1f}" height="4" rx="2" fill="{accent}"/>')
        b.append(text(x + bw / 2, 24, f"{i + 1}", 12, accent, "middle", 800))
        b.append(text(x + bw / 2, 42, head, 10.5, INK, "middle", 700))
        b.append(text(x + bw / 2, 59, sub, 9, SUB, "middle"))
        if i < n - 1:
            ax = x + bw + gap / 2
            b.append(f'<path d="M{ax - 2:.1f},{h / 2 - 4} l4,4 l-4,4" fill="none" stroke="{SUB}" stroke-width="1.5"/>')
    return figure(title, svg(h, "".join(b), title), note)


# ================================================================ 차트 정의
def _idx(vals):
    return [None if v is None else round(v / vals[0] * 100, 1) for v in vals]


def build_charts(md_sources):
    """md_sources: {"02": 마크다운 원문} — 표에서 읽어야 하는 차트용"""
    c = {}
    c["growth_h1"] = hbar(
        "2025년 상반기 매출 성장률 (상위 5개 장비사)",
        [("ASML", 35, None), ("AMAT", 7, "amat"), ("램리서치", 29, "lam"), ("TEL", 12, "tel"), ("KLA", 26, None)],
        vmax=40, note="순서는 2025년 매출 순위. 자료: Counterpoint Research, Castellano")
    fy = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "FY2026"]
    c["margin"] = line(
        "영업이익률 추이 (GAAP)", fy,
        [("lam", [30.6, 31.2, 29.7, 28.6, 32.0, 35.3]),
         ("amat", [29.9, 30.2, 28.9, 28.9, 29.2, None]),
         ("tel", [None, 29.9, 28.0, 24.9, 28.7, 25.6])],
        22, 36, 2, fmt="{:g}",
        note="각 사 회계연도 기준(램리서치 6월, AMAT 10월, TEL 3월 결산). AMAT FY2026은 진행 중이라 제외")
    lam = [17.23, 17.43, 14.91, 18.44, 23.23]
    amat = [25.79, 26.52, 27.18, 28.37, None]
    tel = [2003.8, 2209.0, 1830.5, 2431.5, 2443.5]
    c["rev_index"] = line(
        "매출 지수 (FY2022 = 100)", fy[1:],
        [("lam", _idx(lam)), ("amat", _idx(amat[:4]) + [None]), ("tel", _idx(tel))],
        80, 140, 10, unit="", fmt="{:g}",
        note="통화가 달라(달러·엔) FY2022 매출을 100으로 맞춰 비교. 각 사 회계연도 기준")
    c["customers"] = stacked(
        "10% 이상 고객의 매출 비중 (단위 %)",
        [("lam", [16, 15, 12, 12], "4곳 · 약 55%"),
         ("amat", [19, 15], "2곳 · 약 34%"),
         ("tel", [15.1, 12.9], "2곳 · 약 28% 이상")],
        note="막대 한 칸이 고객 한 곳. 램리서치 FY2026, AMAT FY2025, TEL FY2026 기준")
    c["regions"] = slopes(
        "중국·한국 매출 비중의 이동",
        [("중국: FY2024 정점 → 최근", 25, 46,
          [("lam", (42, "42%"), (34, "34%")), ("amat", (37, "37%"), (30.1, "30.1%")),
           ("tel", (44, "약 44%"), (34.1, "34.1%"))]),
         ("한국: 이전 → 최근", 14, 30,
          [("lam", (27, "27% (FY21)"), (19, "19%")), ("amat", (22, "22% (FY21)"), (19.8, "19.8%")),
           ("tel", (17, "약 17% (FY25)"), (22.3, "22.3%"))])],
        note="최근: 램리서치 FY2026, AMAT FY2025, TEL FY2026")
    m = re.search(r"## 공정별 3사 장비\s*\n\n(\|.*?)\n\n", md_sources.get("02", ""), re.S)
    if m:
        c["position_map"] = matrix("공정별 3사 포지션", m.group(1), note="위 표의 굵은 글씨(대표 영역)와 제품 유무를 점으로 나타냄")
    c["deadline"] = gantt("3사 서류 일정 한눈에 보기 (2026 하반기)",
                          note="진한 구간이 D-3 → D-day 집중 점검 기간. 회색 배경은 주말·공휴일")
    c["ts_flow"] = flow("트러블슈팅 케이스를 푸는 7단계", [
        ("상황 정리", "주장 vs 데이터"), ("증상 정의", "정상과 다른 점"), ("가설", "원인 후보 2~3개"),
        ("분리 진단", "구간을 나눠 지움"), ("조치 옵션", "비용 적은 것부터"),
        ("고객 소통", "예상 시간·진행 보고"), ("에스컬레이션", "안 되면 지원 요청")], "#E0573B")
    return c


CHART_CSS = """
figure.chart { margin: 8pt 0 12pt; padding: 10pt 12pt 8pt; border: 1px solid #E3E7EE; border-radius: 6pt;
               break-inside: avoid; page-break-inside: avoid; }
figure.chart .ct { font-size: 9.5pt; font-weight: 700; color: #1B2333; margin-bottom: 6pt; }
figure.chart svg { display: block; }
figure.chart figcaption { font-size: 7.4pt; color: #8A93A3; margin-top: 5pt; }
"""
