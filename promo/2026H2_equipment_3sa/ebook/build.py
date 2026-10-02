"""마크다운 원고 → 전자책 PDF.

사용: python3 ebook/build.py            (3권 모두)
      python3 ebook/build.py 01        (한 권만)

필요: python markdown, pypdf, poppler(pdftotext), node playwright(Chromium),
      ebook/fonts/Pretendard-*.woff2 (npm pack pretendard)
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
EB = ROOT / "ebook"
FONTS = EB / "fonts"
OUT = EB / "pdf"

BOOKS = {
    "01": dict(
        src="01_현직자의_3사_심층분석집.md",
        out="01_현직자의_3사_심층분석집.pdf",
        vol="01",
        short="현직자의 3사 심층 분석집",
        accent="#2F5BEA",
        break_h2=r"^3-[23]\.",
    ),
    "02": dict(
        src="02_Equipment_Tech_Map.md",
        out="02_Equipment_Tech_Map.pdf",
        vol="02",
        short="Equipment Tech Map",
        accent="#6741D9",
        break_h2=None,
    ),
    "03": dict(
        src="03_합격데이터기반_3사지원전략.md",
        out="03_합격데이터기반_3사지원전략.pdf",
        vol="03",
        short="합격 데이터 기반 3사 지원 전략",
        accent="#0E9F8A",
        break_h2=r"^6-3",
    ),
    "04": dict(
        src="04_실제_장비사_면접복기본.md",
        out="04_실제_장비사_면접복기본.pdf",
        vol="04",
        short="실제 장비사 면접 복기본",
        accent="#E0573B",
        break_h2=None,
        toc_dense=True,
    ),}

COVERS = {
    "01": dict(image="lam", pos="40% 50%", h="49%", hl="#9DB6FF",
               title=["현직자의", "3사 심층 분석집"], subtitle="사업 방향 · 기술 전략 · 직무 구조",
               hook=["같은 장비사라도 돈을 버는 곳이 다릅니다.", "세 회사가 어디에 투자하고 어떤 사람을 뽑는지",
                     "숫자와 기술 전환으로 먼저 읽어야 합니다."],
               tags=["램리서치", "AMAT", "TEL", "재무 · 기술 · 직무"],
               contents=[("PART 0", "핵심 요약 — 3사를 한 장으로"),
                         ("PART 1", "산업 구조와 재무 — 숫자로 보는 3사"),
                         ("PART 2", "기술 변곡점 — 어떤 전환이 오고, 누가 어디에 서 있는가"),
                         ("PART 3", "회사별 심층 — 사업 방향 · 기술 전략 · 직무 구조"),
                         ("PART 4", "종합 — 3사 비교와 지원자가 가져갈 것"),
                         ("부록", "용어집 · 주요 출처")]),
    "02": dict(image="amat", pos="50% 50%", hl="#C3B2FF",
               title=["Equipment", "Tech Map"], subtitle="핵심 장비의 원리 · 적용 공정 · 기술 포인트",
               hook=["장비 이름을 외우는 것으로는 부족합니다.", "어느 공정에서 무엇을 해결하는 장비인지",
                     "설명할 수 있어야 자소서와 기술면접이 연결됩니다."],
               tags=["식각 · 증착", "트랙 · 세정", "HBM · GAA", "기술면접"],
               contents=[("PART 0", "한눈에 보는 3사 장비 지도"),
                         ("PART 1–3", "램리서치 · AMAT · TEL 장비별 원리와 적용 공정"),
                         ("PART 4", "공정 트렌드 × 3사 장비 — HBM · GAA · 3D NAND · EUV · 패키징"),
                         ("PART 5", "기술면접 연결 — 예상 질문 15개와 점검표")]),
    "03": dict(image="tel", pos="70% 45%", hl="#7FDCCB",
               title=["합격 데이터 기반", "3사 지원 전략"], subtitle="하나의 경험으로 램리서치 · AMAT · TEL 모두 지원하기",
               hook=["경험을 세 개 만들 필요는 없습니다.", "같은 경험에서 회사마다 꺼내는 장면이 달라질 뿐입니다.",
                     "마감 3일 전 최종 점검까지 이어서 준비하세요."],
               tags=["장면 카드", "회사별 변환", "사례 6개", "D-3 점검"],
               contents=[("PART 1–2", "원리와 도구 — 경험을 장면 카드로 쪼개기"),
                         ("PART 3", "회사별 변환 규칙"),
                         ("PART 4", "사례 6개 × 3사 작성법"),
                         ("PART 5", "돌려쓰기 실수 10가지"),
                         ("PART 6", "제출 D-3 최종 점검"),
                         ("부록", "3사 문항 원문 · 한 장 요약 · 장면 카드 양식")]),
    "04": dict(image="asml", pos="50% 40%", hl="#FFB49E",
               title=["실제 장비사", "면접 복기본"], subtitle="면접의 흐름 · 질문 유형 · 합격 복기 기반 회사별 면접",
               hook=["장비사 면접은 회사가 달라도 흐름이 비슷합니다.", "면접관은 정답보다 원인을 좁혀 가는 순서와",
                     "경험의 실체를 끝까지 확인합니다."],
               tags=["면접 복기 4선", "질문 유형", "PT · 상황 퀴즈", "회사별 면접"],
               contents=[("PART 1–2", "장비사 면접의 진행 방식과 면접 복기 4선"),
                         ("PART 3–4", "질문 유형별 정리 · 상황 퀴즈와 PT 대비"),
                         ("PART 5–7", "램리서치 FSE · AMAT CE 면접, TEL FE 예상 질문"),
                         ("PART 8", "면접 전 최종 점검"),
                         ("부록", "질문 은행")]),
}
for _k, _c in COVERS.items():
    BOOKS[_k]["cover"] = _c

FONT_FACES = "\n".join(
    f"@font-face{{font-family:'Pretendard';font-weight:{w};"
    f"src:url('{(FONTS / f'Pretendard-{n}.woff2').as_uri()}') format('woff2');}}"
    for n, w in [("Light", 300), ("Regular", 400), ("Medium", 500),
                 ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800)]
)

BASE_CSS = """
@page { size: A4; margin: 20mm 18mm 20mm 18mm; }
:root { --ink:#1B2333; --sub:#5B6475; --line:#E3E7EE; --soft:#F5F7FB; --navy:#0F1E3D; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Pretendard','Noto Color Emoji',sans-serif; color: var(--ink);
       font-size: 9.6pt; line-height: 1.72; margin: 0; word-break: keep-all;
       overflow-wrap: break-word; letter-spacing: -0.1pt; }
p { margin: 0 0 7pt; }
strong { font-weight: 700; color: #0B1220; }
em { font-style: normal; color: var(--sub); }
a { color: inherit; text-decoration: none; }
ul, ol { margin: 0 0 8pt; padding-left: 16pt; }
li { margin: 1.5pt 0; }
li > p { margin: 0; }
hr { border: 0; border-top: 1px solid var(--line); margin: 14pt 0; }
code { font-family: 'Pretendard'; background: var(--soft); padding: 0 3pt; border-radius: 3pt; }

/* 파트 오프너 */
h1 { break-before: page; margin: 0 0 18pt; padding: 26pt 0 14pt; font-size: 20pt;
     line-height: 1.32; font-weight: 800; color: var(--navy);
     border-bottom: 2.5pt solid var(--accent); }
h1 .lbl { display: block; font-size: 10pt; font-weight: 700; letter-spacing: 2pt;
          color: var(--accent); margin-bottom: 6pt; }
h1 .sub { display: block; font-size: 11.5pt; font-weight: 500; color: var(--sub); margin-top: 6pt; }
h2 { font-size: 13.5pt; font-weight: 800; line-height: 1.4; color: var(--navy);
     margin: 22pt 0 9pt; padding: 2pt 0 2pt 9pt; border-left: 4pt solid var(--accent);
     break-after: avoid; }
h2.brk { break-before: page; margin-top: 0; }
h3 { font-size: 11pt; font-weight: 700; color: var(--navy); margin: 15pt 0 6pt; break-after: avoid; }
h4 { font-size: 10pt; font-weight: 700; color: var(--accent); margin: 12pt 0 5pt; break-after: avoid; }
h1 + hr, h2 + hr, .ch > hr:last-child { display: none; }
/* 굵은 글씨 한 줄짜리 소제목은 다음 내용과 붙여 둔다 */
p:has(> strong:only-child) { break-after: avoid; }
h3 + table, h4 + table { break-before: avoid; }

/* 표 */
table { width: 100%; border-collapse: collapse; margin: 6pt 0 12pt; font-size: 8.5pt;
        line-height: 1.55; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th { background: var(--navy); color: #fff; font-weight: 600; text-align: left;
     padding: 5pt 6pt; border: 1px solid var(--navy); }
td { padding: 4.5pt 6pt; border: 1px solid var(--line); vertical-align: top; }
tbody tr:nth-child(even) td { background: #FAFBFD; }
td strong { color: var(--navy); }
table.qa { break-inside: avoid; margin: 4pt 0 9pt; }
table.qa th:first-child { width: 11mm; background: var(--accent); text-align: center; }
table.qa th:last-child { font-weight: 700; }
table.qa td:first-child { width: 11mm; text-align: center; font-weight: 700; color: var(--accent); background: #fff; }
table.qa tbody tr td { background: #fff; }

/* 인용·예시문 박스 */
blockquote { margin: 8pt 0 12pt; padding: 9pt 12pt; background: var(--soft);
             border-left: 3pt solid var(--accent); border-radius: 0 5pt 5pt 0; }
blockquote p:last-child, blockquote ul:last-child { margin-bottom: 0; }
blockquote blockquote { background: #fff; }

/* 목차 */
.toc { break-after: page; }
.toc h1 { break-before: auto; }
.toc .row { display: flex; align-items: baseline; gap: 6pt; }
.toc .row .t { flex: 0 1 auto; }
.toc .row .dots { flex: 1 1 auto; border-bottom: 1px dotted #B8C0CE; transform: translateY(-3pt); }
.toc .row .p { flex: 0 0 22pt; text-align: right; font-variant-numeric: tabular-nums; }
.toc h1 { padding-top: 6pt; margin-bottom: 12pt; }
.toc .l1 { font-size: 10.3pt; font-weight: 700; color: var(--navy); margin: 7pt 0 1pt; }
.toc .l2 { font-size: 8.8pt; line-height: 1.6; color: var(--sub); margin: 0 0 0 12pt; }
.toc.dense .l1 { margin: 5pt 0 0; } .toc.dense .l2 { line-height: 1.42; }
.mk { position: absolute; font-size: 2pt; color: #fff; }

/* 장 끝이 몇 줄만 다음 쪽으로 넘어갈 때 쓰는 압축 단계 */
.ch.t1 { font-size: 9.3pt; line-height: 1.64; }
.ch.t1 p { margin-bottom: 6pt; }
.ch.t1 h2 { margin: 17pt 0 7pt; }
.ch.t1 h3 { margin: 12pt 0 5pt; }
.ch.t1 table { font-size: 8.2pt; margin: 5pt 0 10pt; }
.ch.t1 td { padding: 3.6pt 5.5pt; } .ch.t1 th { padding: 4.2pt 5.5pt; }
.ch.t1 blockquote { padding: 7pt 11pt; margin: 6pt 0 10pt; }
.ch.t1 h1 { padding-top: 16pt; margin-bottom: 14pt; }
.ch.t2 { font-size: 9pt; line-height: 1.56; }
.ch.t2 p { margin-bottom: 5pt; }
.ch.t2 h2 { margin: 14pt 0 6pt; }
.ch.t2 h3 { margin: 10pt 0 4pt; }
.ch.t2 table { font-size: 7.9pt; line-height: 1.48; margin: 4pt 0 8pt; }
.ch.t2 td { padding: 3pt 5pt; } .ch.t2 th { padding: 3.6pt 5pt; }
.ch.t2 blockquote { padding: 6pt 10pt; margin: 5pt 0 8pt; }
.ch.t2 h1 { padding-top: 10pt; margin-bottom: 12pt; }
.ch.t2 hr { margin: 9pt 0; }
"""

COVER_CSS = """
@page { size: A4; margin: 0; }
html,body { margin:0; height:100%; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family:'Pretendard',sans-serif; word-break: keep-all; }
.cover { position: relative; width: 210mm; height: 297mm; overflow: hidden; color: #fff;
         background: linear-gradient(180deg, #1C2029 0%, #232934 46%, #232934 100%); }
.photo { position:absolute; left:0; right:0; bottom:0; height:56%; background-size:cover;
         filter: saturate(.9) brightness(.82);
         -webkit-mask-image: linear-gradient(180deg, transparent 0%, rgba(0,0,0,.35) 22%, rgba(0,0,0,.85) 48%, #000 70%, rgba(0,0,0,.6) 92%, rgba(0,0,0,.4) 100%);
         mask-image: linear-gradient(180deg, transparent 0%, rgba(0,0,0,.35) 22%, rgba(0,0,0,.85) 48%, #000 70%, rgba(0,0,0,.6) 92%, rgba(0,0,0,.4) 100%); }
.in { position:absolute; left:18mm; right:18mm; top:0; bottom:0; }
.brand { position:absolute; top:22mm; left:0; font-size:9.6pt; font-weight:700; letter-spacing:3.4pt; }
.rule { position:absolute; left:0; right:0; height:0; border-top:.6pt solid rgba(255,255,255,.28); }
.series { position:absolute; top:35mm; font-size:9pt; font-weight:400; letter-spacing:1.6pt; color:#D5DAE3; }
.eyebrow { position:absolute; top:43mm; font-size:9pt; font-weight:600; letter-spacing:2pt; color: var(--hl); }
.title { position:absolute; top:51mm; font-size:31pt; font-weight:800; line-height:1.24; letter-spacing:-.6pt; }
.subtitle { position:absolute; top:84mm; font-size:12pt; font-weight:400; color:#E6EAF0; }
.bar { position:absolute; top:95mm; width:31mm; height:.9mm; background: var(--hl); }
.hook { position:absolute; top:101mm; font-size:10pt; line-height:1.85; color:#E1E5EC; }
.tags { position:absolute; top:125mm; display:flex; gap:2mm; flex-wrap:wrap; }
.tags span { font-size:8.2pt; padding:1.6mm 3.4mm; border:.6pt solid rgba(255,255,255,.6); border-radius:10mm;
             background: rgba(20,24,31,.35); }
.ctitle { position:absolute; top:144mm; font-size:8.4pt; letter-spacing:4.4pt; color:#AEB6C4; }
.contents { position:absolute; top:152mm; left:0; right:0; }
.contents .r { display:flex; font-size:8.8pt; line-height:1.4; margin-bottom:3.3mm; }
.contents .k { flex: 0 0 27mm; font-weight:700; color: var(--hl); }
.contents .v { color:#E8EBF0; }
.foot { position:absolute; bottom:18mm; left:0; right:0; padding-top:4mm; border-top:.6pt solid rgba(255,255,255,.28);
        font-size:8.8pt; color:#E1E5EC; display:flex; justify-content:space-between; }
"""

FOOTER = (
    '<div style="width:100%;font-size:7pt;color:#8A93A3;padding:0 18mm;'
    'display:flex;justify-content:space-between;font-family:DejaVu Sans,sans-serif;">'
    '<span style="letter-spacing:1.5px">CAREERMIZING &middot; 2026H2 EQUIPMENT 3</span>'
    '<span class="pageNumber"></span></div>'
)

RENDER_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  let browser;
  try { browser = await chromium.launch(); }
  catch (e) { browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); }
  const page = await browser.newPage();
  for (const j of jobs) {
    await page.goto('file://' + j.html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: j.pdf, format: 'A4', printBackground: true, preferCSSPageSize: true,
      displayHeaderFooter: j.footer !== null, headerTemplate: '<span></span>',
      footerTemplate: j.footer || '<span></span>' });
  }
  await browser.close();
})();
"""


def render(jobs):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(RENDER_JS)
        js = f.name
    env = dict(os.environ, NODE_PATH="/opt/node-tools/node_modules")
    subprocess.run(["node", js, json.dumps(jobs)], check=True, env=env)
    os.unlink(js)


def split_front(md_text):
    """첫 '---' 앞을 표지 정보로, 뒤를 본문으로."""
    head, _, body = md_text.partition("\n---\n")
    title, subs, meta = "", [], ""
    for line in head.splitlines():
        s = line.strip()
        if s.startswith("# "):
            title = s[2:]
        elif s.startswith("#"):
            subs.append(s.lstrip("#").strip())
        elif s.startswith("*") and s.endswith("*"):
            meta = s.strip("*")
    return title, subs, meta, body


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


LIST_RE = re.compile(r"^(\s*)([-*+]|\d+\.)\s")


def fix_lists(md_text):
    """문단 바로 뒤에 붙은 목록 앞에 빈 줄을 넣는다(인용 블록 포함)."""
    out, prev = [], ""
    for line in md_text.splitlines():
        q = re.match(r"^((?:>\s?)*)(.*)$", line)
        pre, rest = q.group(1), q.group(2)
        pq = re.match(r"^((?:>\s?)*)(.*)$", prev)
        ppre, prest = pq.group(1), pq.group(2)
        if (LIST_RE.match(rest) and prest.strip() and not LIST_RE.match(prest)
                and not prest.startswith(("|", "#")) and pre.strip() == ppre.strip()
                and not prest.startswith(" ")):
            out.append(pre.rstrip())
        out.append(line)
        prev = line
    return "\n".join(out)


def build_body_html(body_md, cfg, page_map=None, markers=True, tight=None):
    h = markdown.markdown(fix_lists(body_md), extensions=["tables", "sane_lists"])
    toc, n = [], [0]
    brk = re.compile(cfg["break_h2"]) if cfg["break_h2"] else None

    def h1(m):
        n[0] += 1
        hid = f"h{n[0]}"
        text = strip_tags(m.group(1))
        mm = re.match(r"^((?:PART \d+|부록 [A-Z]))\.\s*(.*)$", text)
        if mm:
            lbl, rest = mm.groups()
            title, _, sub = rest.partition(": ")
            inner = (f'<span class="lbl">{html.escape(lbl)}</span>{html.escape(title)}'
                     + (f'<span class="sub">{html.escape(sub)}</span>' if sub else ""))
        else:
            inner = m.group(1)
        toc.append((1, hid, text))
        mk = f'<span class="mk">@@{hid}@@</span>' if markers else ""
        return f'<h1 id="{hid}">{mk}{inner}</h1>'

    def h2(m):
        n[0] += 1
        hid = f"h{n[0]}"
        text = strip_tags(m.group(1))
        cls = ' class="brk"' if brk and brk.search(text) else ""
        toc.append((2, hid, text))
        mk = f'<span class="mk">@@{hid}@@</span>' if markers else ""
        return f'<h2 id="{hid}"{cls}>{mk}{m.group(1)}</h2>'

    h = re.sub(r"<h([12])>(.*?)</h\1>",
               lambda m: (h1 if m.group(1) == "1" else h2)(re.match(r"(.*)", m.group(2), re.S)),
               h, flags=re.S)

    # 질문 표(첫 머리칸이 Q1, Q2 …)는 평가·전략·주의 카드로 그린다
    h = re.sub(r"<table>(\s*<thead>\s*<tr>\s*<th>Q\d+</th>)", r'<table class="qa">\1', h)

    # H1 단위로 <section>을 나눠, 끝 쪽이 몇 줄만 넘어가는 장은 간격을 줄인다
    tight = tight or {}
    parts = re.split(r'(?=<h1 id=")', h)
    h = f'<section class="ch t{tight.get(-1, 0)}">{parts[0]}</section>' + "".join(
        f'<section class="ch t{tight.get(i, 0)}">{c}</section>' for i, c in enumerate(parts[1:]))

    rows = []
    for lvl, hid, text in toc:
        if lvl > cfg.get("toc_depth", 2):
            continue
        p = (page_map or {}).get(hid, "")
        rows.append(f'<div class="row l{lvl}"><a class="t" href="#{hid}">{html.escape(text)}</a>'
                    f'<span class="dots"></span><span class="p">{p}</span></div>')
    toc_html = (f'<section class="toc{" dense" if cfg.get("toc_dense") else ""}"><h1>차례</h1>' + "\n".join(rows) + "</section>")
    return toc_html + h


def page_html(css, body, accent):
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            f"<style>{FONT_FACES}{css}:root{{--accent:{accent};}}</style></head>"
            f"<body>{body}</body></html>")


def cover_html(cfg, title, subs, meta):
    c = cfg["cover"]
    img = EB / "cover" / f"{c['image']}.jpg"
    photo = (f'<div class="photo" style="background-image:url({img.as_uri()});background-position:{c["pos"]};height:{c.get("h", "56%")}"></div>'
             if img.exists() else "")
    esc = html.escape
    rows = "".join(f'<div class="r"><span class="k">{esc(k)}</span><span class="v">{esc(v)}</span></div>'
                   for k, v in c["contents"])
    tags = "".join(f"<span>{esc(t)}</span>" for t in c["tags"])
    body = f"""
<div class="cover">{photo}<div class="in">
  <div class="brand">CAREERMIZING</div>
  <div class="rule" style="top:30mm"></div>
  <div class="series">외국계 장비사 합격 패키지 &nbsp;{cfg['vol'].lstrip('0')} / 4</div>
  <div class="eyebrow">2026 하반기 램리서치 · AMAT · TEL 신입 공채 대비</div>
  <div class="title">{'<br>'.join(esc(t) for t in c['title'])}</div>
  <div class="subtitle">{esc(c['subtitle'])}</div>
  <div class="bar"></div>
  <div class="hook">{'<br>'.join(esc(t) for t in c['hook'])}</div>
  <div class="tags">{tags}</div>
  <div class="rule" style="top:139mm"></div>
  <div class="ctitle">CONTENTS</div>
  <div class="contents">{rows}</div>
  <div class="foot"><span>작성 기준일 2026년 10월 1일</span><span>MAX 플랜 구매자 전용 자료</span></div>
</div></div>"""
    return page_html(COVER_CSS, body, cfg["accent"]).replace(
        ":root{", f":root{{--hl:{c['hl']};", 1)


def heading_pages(pdf):
    out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True,
                         text=True, check=True).stdout
    pm = {}
    for i, pg in enumerate(out.split("\f"), start=1):
        for hid in re.findall(r"@\s*@\s*(h\d+)\s*@\s*@", pg):
            pm.setdefault(hid, i)
    return pm


def page_fills(pdf):
    """쪽마다 본문 글자가 내려온 정도(0~1). 바닥글은 제외."""
    x = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True,
                       text=True, check=True).stdout
    fills = []
    for pg in x.split("<page ")[1:]:
        hgt = float(re.search(r'height="([\d.]+)"', pg).group(1))
        ys = [float(v) for v in re.findall(r'yMax="([\d.]+)"', pg)]
        ys = [y for y in ys if y < hgt - 45]
        fills.append((max(ys) if ys else 0) / (hgt - 57))
    return fills


SPILL = 0.35   # 장의 마지막 쪽이 이보다 덜 차면 그 장을 한 단계 압축


def build(key):
    cfg = BOOKS[key]
    md_text = (ROOT / cfg["src"]).read_text(encoding="utf-8")
    title, subs, meta, body_md = split_front(md_text)
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        cov_h, cov_p = td / "cover.html", td / "cover.pdf"
        b1_h, b1_p = td / "b1.html", td / "b1.pdf"
        b2_h, b2_p = td / "b2.html", td / "b2.pdf"
        cov_h.write_text(cover_html(cfg, title, subs, meta), encoding="utf-8")
        render([dict(html=str(cov_h), pdf=str(cov_p), footer=None)])
        tight = {}
        for _ in range(4):
            b1_h.write_text(page_html(BASE_CSS, build_body_html(body_md, cfg, tight=tight),
                                      cfg["accent"]), encoding="utf-8")
            render([dict(html=str(b1_h), pdf=str(b1_p), footer=FOOTER)])
            pm = heading_pages(b1_p)
            fills = page_fills(b1_p)
            h1_ids = re.findall(r'<h1 id="(h\d+)"', build_body_html(body_md, cfg))
            starts = [pm[i] for i in h1_ids if i in pm]
            changed = False
            # 머리말(첫 PART 앞)이 몇 줄만 넘어간 경우
            if starts and starts[0] >= 2 and fills[starts[0] - 2] < SPILL and tight.get(-1, 0) < 2:
                tight[-1] = tight.get(-1, 0) + 1
                changed = True
            for k, st in enumerate(starts):
                last = (starts[k + 1] - 1) if k + 1 < len(starts) else len(fills)
                if last > st and fills[last - 1] < SPILL and tight.get(k, 0) < 2:
                    tight[k] = tight.get(k, 0) + 1
                    changed = True
            if not changed:
                break
        # 표지 다음부터 본문 쪽수: 바닥글 번호는 본문 PDF 기준(1부터)
        b2_h.write_text(page_html(BASE_CSS, build_body_html(body_md, cfg, pm, markers=False,
                                                            tight=tight),
                                  cfg["accent"]), encoding="utf-8")
        render([dict(html=str(b2_h), pdf=str(b2_p), footer=FOOTER)])

        w = PdfWriter()
        for src in (cov_p, b2_p):
            for p in PdfReader(str(src)).pages:
                w.add_page(p)
        w.add_metadata({"/Title": title, "/Author": "커리어마이징(Careermizing)",
                        "/Subject": " · ".join(subs)})
        dst = OUT / cfg["out"]
        with open(dst, "wb") as f:
            w.write(f)
    n1, n2 = len(PdfReader(str(dst)).pages), len(pm)
    print(f"{key}: {dst.name} — {n1}쪽, 목차 항목 {n2}개, 압축한 장 {tight}")


if __name__ == "__main__":
    for k in (sys.argv[1:] or BOOKS):
        build(k)
