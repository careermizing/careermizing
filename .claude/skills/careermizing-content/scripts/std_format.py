"""
취준팁 표준 포맷 (std_*) — 커리어마이징 정기 콘텐츠의 모범 사례 두 편을 그대로 재현한다.

  · 「주변에서는 본인을 어떻게 평가하나요?」 (Figma 978:1640)
  · 「[DRAFT] 20261012 / 면접팁 / 공백기가 있네요?」 [REDESIGN] (Figma 871:332)

공통 문법: 1080×1350 · 흰 배경 · 좌상단 브랜드 에셋(아이콘+Raleway) · 페이지 번호 없음(마지막 다크 장만) ·
중앙 정렬 헤드라인 2행(1행 #141A26 / 2행 포인트 블루) · 회색 서브 한 줄 · 본문 컴포넌트 1개 ·
하단 중앙 결론(형광펜 #FFF0A0) · 짤/사진 적극 사용 · Noto Sans KR.

render_carousel.py 가 type 이 'std_' 로 시작하면 이 모듈의 build() 를 호출한다.
"""

def css(accent):
    return f"""
/* ===== std (취준팁 표준 포맷) ===== */
.std {{ --a: {accent}; --ink: #141A26; --ink2: #091229; --gray: #5B6475; --gray2: #61708C; --line: #E3E8F0; --hl: #FFF0A0;
  background: #fff; color: var(--ink); padding: 151px 72px 0; font-family: 'Noto Sans KR', 'Pretendard Variable', sans-serif; letter-spacing: .32px; }}
.std .pt {{ color: var(--a); }}
.std mark {{ background: linear-gradient(transparent 27%, var(--hl) 27%); color: inherit; padding: 0 3px; }}
.std b {{ font-weight: 700; }}
.std .asset {{ position: absolute; left: 75px; top: 65px; display: flex; align-items: center; gap: 7px; }}
.std .asset .ic {{ position: relative; width: 35px; height: 35px; }}
.std .asset .ic i {{ position: absolute; width: 30px; height: 30px; border-radius: 50%; mix-blend-mode: multiply; }}
.std .asset .ic i:nth-child(1) {{ left: 2px; top: 0; background: #6F8FE8; }}
.std .asset .ic i:nth-child(2) {{ left: 5px; top: 3px; background: #4C7BE0; }}
.std .asset .ic i:nth-child(3) {{ left: 0; top: 5px; background: #2E4CA8; }}
.std .asset .wm {{ font-family: Raleway, sans-serif; font-weight: 600; font-size: 26.2px; line-height: 1; letter-spacing: 0;
  background: linear-gradient(90deg, #323F91, #356FB6); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.std.dark .asset .ic i:nth-child(1), .std.photo .asset .ic i:nth-child(1) {{ background: #A9C2FF; mix-blend-mode: screen; }}
.std.dark .asset .ic i:nth-child(2), .std.photo .asset .ic i:nth-child(2) {{ background: #7FA0F5; mix-blend-mode: screen; }}
.std.dark .asset .ic i:nth-child(3), .std.photo .asset .ic i:nth-child(3) {{ background: #4D6FE0; mix-blend-mode: screen; }}
.std.dark .asset .wm, .std.photo .asset .wm {{ font-size: 31.7px; background: linear-gradient(90deg, #BBD0FF, #FFF); -webkit-background-clip: text; background-clip: text; }}
.std.dark .asset .ic, .std.photo .asset .ic {{ width: 48px; height: 48px; }}
.std.dark .asset .ic i, .std.photo .asset .ic i {{ width: 41px; height: 41px; }}
.std.photo .asset {{ left: 65px; top: 90px; }}

.std h1 {{ font-weight: 700; font-size: 60px; line-height: 82.8px; text-align: center; color: var(--ink); word-break: keep-all; }}
.std h1.left {{ text-align: left; font-weight: 900; color: var(--ink2); line-height: 1.25; margin-top: 14px; }}
.std .sub {{ margin-top: 20px; font-weight: 400; font-size: 30px; line-height: 45px; color: var(--gray); text-align: center; word-break: keep-all; }}
.std .sub.left {{ text-align: left; font-weight: 500; color: var(--gray2); margin-top: 34px; }}
.std .body {{ margin-top: 48px; }}
.std .concl {{ position: absolute; left: 72px; right: 72px; top: 1131px; text-align: center; font-weight: 700; font-size: 36px; line-height: 55.8px; color: var(--ink); word-break: keep-all; }}
.std .concl .r {{ font-weight: 400; }}
.std .concl.blue {{ top: 1200px; font-weight: 500; font-size: 26px; line-height: 1.32; color: var(--a); }}
.std .concl.interviewer {{ top: 1120px; font-weight: 900; font-size: 30px; line-height: 1.3; color: var(--a); }}
.std .concl.interviewer .who {{ color: var(--ink2); }}
.std .disc {{ position: absolute; left: 72px; right: 72px; top: 1278px; font-weight: 500; font-size: 19px; color: var(--gray2); }}

/* 이미지 자리 */
.std .img {{ margin: 0 auto; width: 600px; height: 431px; border-radius: 28px; background: #F2F4F8 center/cover no-repeat; position: relative; }}
.std .img.ph::after {{ content: attr(data-label); position: absolute; inset: 0; border: 3px dashed #C8CFDB; border-radius: 28px; display: flex; align-items: center; justify-content: center; text-align: center;
  font-size: 24px; font-weight: 500; color: #8A93A3; line-height: 1.5; white-space: pre-line; padding: 30px; }}
/* 짤 아래 인용 카드 */
.std .qcard {{ margin-top: 64px; background: #fff; border: 3px solid #B9CDF9; border-radius: 28px; padding: 16px 30px 22px; text-align: center; }}
.std .qcard .ql {{ font-weight: 700; font-size: 24px; line-height: 37px; color: #9AA2B1; }}
.std .qcard .qt {{ font-family: 'Nanum Pen Script', 'Ownglyph RDO ballpen', cursive; font-size: 50px; line-height: 60px; color: var(--a); word-break: keep-all; }}

/* 번호 카드 + 삼각형 연결 */
.std .ncards {{ margin-top: 50px; display: flex; flex-direction: column; align-items: center; }}
.std .ncard {{ width: 100%; min-height: 200px; border: 3px solid var(--line); border-radius: 32px; background: #fff; display: flex; align-items: center; gap: 30px; padding: 34px 43px; }}
.std .ncard.on {{ border-color: var(--a); }}
.std .ncard .n {{ flex: 0 0 60px; font-weight: 700; font-size: 48px; line-height: 1.2; color: var(--a); }}
.std .ncard .t {{ font-weight: 700; font-size: 36px; line-height: 48.6px; word-break: keep-all; }}
.std .ncard .d {{ margin-top: 10px; font-weight: 500; font-size: 28px; line-height: 40.6px; color: var(--gray); word-break: keep-all; }}
.std .tri {{ width: 0; height: 0; border-left: 14px solid transparent; border-right: 14px solid transparent; border-top: 18px solid #C9D6F2; margin: 6px 0; }}

/* 표 */
.std .tbl {{ margin-top: 48px; border: 3px solid var(--line); border-radius: 36px; padding: 0 0 10px; }}
.std .tbl .hd, .std .tbl .rw {{ display: flex; gap: 40px; padding: 0 43px; }}
.std .tbl .hd {{ padding-top: 24px; padding-bottom: 14px; border-bottom: 3px solid var(--ink); font-weight: 700; font-size: 26px; color: var(--gray); }}
.std .tbl .rw {{ align-items: center; min-height: 196px; padding-top: 26px; padding-bottom: 26px; }}
.std .tbl .rw + .rw {{ border-top: 3px solid var(--line); }}
.std .tbl .c1 {{ flex: 0 0 210px; font-weight: 700; font-size: 34px; line-height: 1.4; word-break: keep-all; }}
.std .tbl .c2 {{ flex: 1; font-weight: 700; font-size: 37px; line-height: 55.5px; word-break: keep-all; }}
.std .tbl .rw.on .c2 {{ color: var(--a); }}

/* 답변(좌측 세로 바) */
.std .bar {{ margin-top: 52px; border-left: 10px solid var(--a); padding-left: 40px; display: flex; flex-direction: column; gap: 30px; }}
.std .bar p {{ font-weight: 500; font-size: 36px; line-height: 61.2px; word-break: keep-all; }}
.std .gcard {{ margin-top: 54px; background: #F2F4F8; border-radius: 28px; padding: 24px 32px 28px; }}
.std .gcard .gl {{ font-weight: 700; font-size: 25px; line-height: 38.8px; }}
.std .gcard .gt {{ font-weight: 400; font-size: 30px; line-height: 46.5px; color: var(--gray); word-break: keep-all; }}
.std .gcard .gt.strong {{ font-weight: 700; color: var(--ink); font-size: 32px; line-height: 52px; }}

/* 빈칸 워크시트 */
.std .ws {{ margin-top: 43px; display: flex; flex-direction: column; gap: 20px; }}
.std .ws .it {{ border: 3px solid var(--line); border-radius: 32px; padding: 27px 43px 30px; }}
.std .ws .wl {{ font-weight: 700; font-size: 28px; line-height: 43.4px; color: var(--a); }}
.std .ws .wsn {{ font-weight: 700; font-size: 35px; line-height: 54px; color: #0E1530; word-break: keep-all; }}
.std .ws .wsn .bl {{ display: inline-block; width: 124px; height: 4px; background: #9DB4E8; vertical-align: middle; margin: 0 8px; }}
.std .ws .wex {{ font-weight: 500; font-size: 27px; line-height: 41.9px; color: var(--gray); }}

/* 순서 박스(↓ 연결) */
.std .flow {{ margin-top: 50px; display: flex; flex-direction: column; align-items: center; }}
.std .flow .bx {{ width: 100%; border: 1px solid #CCDBFF; border-radius: 20px; padding: 30px 30px 32px; text-align: center; }}
.std .flow .bx.on {{ border: 2px solid var(--a); }}
.std .flow .ft {{ font-weight: 900; font-size: 32px; line-height: 1.3; color: var(--ink2); word-break: keep-all; }}
.std .flow .fe {{ margin-top: 10px; font-weight: 500; font-size: 25px; line-height: 1.4; color: var(--gray2); word-break: keep-all; }}
.std .flow .ar {{ font-size: 28px; line-height: 1; color: var(--a); margin: 12px 0; }}

/* BEFORE/AFTER 2단 패널 */
.std .ba {{ display: flex; gap: 24px; align-items: stretch; }}
.std .ba .pn {{ flex: 440; min-height: 500px; border-radius: 24px; padding: 34px 32px 34px; background: #F7F8FA; border: 1.7px solid #E3E6EC; display: flex; flex-direction: column; }}
.std .ba .pn.after {{ flex: 472; background: #F3F7FE; border-color: #C7D8FF; }}
.std .ba .pl {{ font-weight: 700; font-size: 26px; color: #C00003; margin-bottom: 22px; }}
.std .ba .after .pl {{ color: var(--a); }}
.std .ba .pq {{ font-weight: 700; font-size: 31px; line-height: 1.5; color: #000; word-break: keep-all; flex: 1; }}
.std .ba .pr {{ margin-top: 24px; border-top: 2px solid #C7D8FF; padding-top: 22px; display: flex; flex-direction: column; gap: 8px; }}
.std .ba .before .pr {{ border-color: #D6DAE2; }}
.std .ba .pr div {{ font-weight: 500; font-size: 27px; line-height: 1.55; }}
.std .ba .pr span {{ font-weight: 700; color: var(--a); display: inline-block; min-width: 108px; }}
.std .ba .before .pq {{ font-weight: 500; color: #5B6475; }}
.std .ba .before .pr div, .std .ba .before .pr span {{ color: #99A1B0; }}
.std .ba .before .pr .x {{ text-decoration: line-through; }}

/* 질문 쌍(GPT vs 복기) */
.std .pairs {{ display: flex; flex-direction: column; gap: 30px; }}
.std .pair .ptag {{ display: block; font-weight: 700; font-size: 24px; color: var(--gray); margin: 0 0 10px 4px; }}
.std .pair .q {{ border-radius: 24px; padding: 16px 28px 18px; }}
.std .pair .q .ql {{ font-weight: 700; font-size: 21px; margin-bottom: 6px; }}
.std .pair .q.g {{ background: #F7F8FA; border: 1.7px solid #E3E6EC; }}
.std .pair .q.g .ql {{ color: #99A1B0; }}
.std .pair .q.g .qt {{ font-weight: 500; font-size: 27px; line-height: 1.45; color: var(--gray); }}
.std .pair .q.c {{ background: #F3F7FE; border: 2px solid var(--a); }}
.std .pair .q.c .ql {{ color: var(--a); }}
.std .pair .q.c .qt {{ font-weight: 700; font-size: 30px; line-height: 1.45; color: var(--ink2); word-break: keep-all; }}
.std .pair .ar {{ text-align: center; color: #C9D6F2; font-size: 20px; line-height: 1; margin: 5px 0; }}

/* 답변 패널(태그 pill) + × 리스트 */
.std .panel {{ margin-top: 54px; background: #F3F7FE; border: 1.7px solid #C7D8FF; border-radius: 24px; padding: 32px 32px 36px; }}
.std .panel .pt0 {{ font-weight: 900; font-size: 26px; color: var(--a); margin-bottom: 26px; }}
.std .panel .row {{ display: flex; gap: 26px; align-items: flex-start; }}
.std .panel .row + .row {{ margin-top: 22px; }}
.std .panel .pill {{ flex: 0 0 79px; height: 38px; border: 1px solid var(--a); border-radius: 20px; background: #fff; color: var(--a); font-weight: 700; font-size: 18px; display: flex; align-items: center; justify-content: center; }}
.std .panel .rt {{ font-weight: 700; font-size: 25px; line-height: 1.4; color: var(--ink2); word-break: keep-all; }}
.std .xl {{ margin-top: 50px; }}
.std .xl .xt {{ font-weight: 900; font-size: 34px; color: var(--ink2); margin-bottom: 12px; }}
.std .xl .xr {{ display: flex; gap: 22px; align-items: center; padding: 14px 0; }}
.std .xl .xr + .xr {{ border-top: 2px solid #C7D8FF; }}
.std .xl .xr .x {{ font-weight: 900; font-size: 38px; color: #E02F32; width: 46px; }}
.std .xl .xr.ok .x {{ color: var(--a); }}
.std .xl .xr .tx {{ font-weight: 500; font-size: 29px; color: var(--ink2); }}

/* 마지막 다크 CTA (공백기 P6) */
.std.dark {{ background: #071022; color: #fff; padding-top: 246px; }}
.std.dark .pg {{ position: absolute; right: 76px; top: 73px; font-weight: 500; font-size: 22px; color: #D1E0FC; }}
.std.dark h1 {{ text-align: left; font-weight: 900; font-size: 62px; line-height: 1.23; color: #fff; }}
.std.dark .sub {{ text-align: left; font-weight: 500; font-size: 29px; color: #D1E0FC; margin-top: 30px; }}
.std.dark .ck {{ margin-top: 34px; background: rgba(243,247,254,.92); border-radius: 23px; padding: 12px 34px; color: var(--ink2); }}
.std.dark .ck .ckr {{ display: flex; gap: 26px; padding: 20px 0; align-items: baseline; }}
.std.dark .ck .ckr + .ckr {{ border-top: 2px solid #C7D8FF; }}
.std.dark .ck .cn {{ flex: 0 0 64px; font-weight: 900; font-size: 34px; color: var(--a); }}
.std.dark .ck .ct {{ font-weight: 900; font-size: 32px; line-height: 1.3; }}
.std.dark .ck .cp {{ margin-top: 6px; font-weight: 500; font-size: 25px; color: var(--gray2); }}
.std.dark .ph {{ position: absolute; left: 76px; right: 76px; top: 1092px; }}
.std.dark .ph .h {{ font-weight: 700; font-size: 31px; color: #fff; }}
.std.dark .ph .s {{ margin-top: 8px; font-weight: 500; font-size: 25px; color: #D1E0FC; }}
.std.dark .btn {{ position: absolute; left: 76px; right: 76px; top: 1221px; height: 84px; border-radius: 17px; background: var(--a); opacity: .95; display: flex; align-items: center; padding: 0 32px; font-weight: 700; font-size: 30px; color: #fff; }}

/* 포토 표지 */
.std.photo {{ background: #071022; color: #fff; padding: 0 72px 146px; display: flex; flex-direction: column; justify-content: flex-end; }}
.std.photo .bgimg {{ position: absolute; inset: 0; background: linear-gradient(103deg, #122552, #050A18) center/cover no-repeat; }}
.std.photo .bgimg.has {{ background-size: cover; }}
.std.photo .dim {{ position: absolute; inset: 0; background: rgba(0,0,0,var(--dim, .3)); }}
.std.photo .fade {{ position: absolute; left: 0; right: 0; bottom: 0; height: 654px; background: linear-gradient(to bottom, rgba(0,0,0,0), #000 64.5%); }}
.std.photo .top {{ font-weight: 600; font-size: 45px; line-height: 1.35; margin-bottom: 14px; }}
.std.photo .ch {{ font-weight: 900; font-size: 100px; line-height: 118px; letter-spacing: -2.5px; word-break: keep-all; }}
.std.photo .cs {{ margin-top: 34px; font-weight: 700; font-size: 44px; line-height: 61.6px; color: rgba(255,255,255,.95); word-break: keep-all; }}
.std.photo .src {{ position: absolute; right: 38px; bottom: 34px; font-size: 16px; color: #B7B7B7; }}
.std.photo .phl {{ position: absolute; right: 72px; top: 100px; font-size: 20px; color: rgba(255,255,255,.45); text-align: right; }}

/* 자유 텍스트 블록 · 블록 간 간격 */
.std .txt {{ font-weight: 500; font-size: 32px; line-height: 1.6; color: var(--ink); word-break: keep-all; }}
.std .body > * + * {{ margin-top: 30px; }}
.std .body > .tri + *, .std .body > .qcard {{ margin-top: 40px; }}

/* 서비스 장 (주변평가 P08) */
.std.svc {{ background: #0E1530; color: #fff; padding: 152px 72px 0; }}
.std.svc .cap {{ position: absolute; left: 72px; top: 60px; height: 64px; padding: 0 26px; border-radius: 32px; background: rgba(255,255,255,.12); display: flex; align-items: center; font-weight: 700; font-size: 26px; }}
.std.svc .shot {{ height: 740px; border-radius: 28px; background: #DCE2EE center/cover no-repeat; position: relative; }}
.std.svc .shot.ph::after {{ content: attr(data-label); position: absolute; inset: 0; border: 3px dashed #C9D2E0; border-radius: 28px; display: flex; align-items: center; justify-content: center; text-align: center;
  font-size: 28px; font-weight: 500; color: #8A93A3; white-space: pre-line; line-height: 1.6; }}
.std.svc .sh {{ margin-top: 65px; font-weight: 700; font-size: 48px; line-height: 67px; word-break: keep-all; }}
.std.svc .ss {{ margin-top: 40px; border-left: 6px solid #fff; padding-left: 28px; font-weight: 500; font-size: 33px; line-height: 52.8px; color: rgba(255,255,255,.92); }}
"""


def _asset():
    return '<div class="asset"><div class="ic"><i></i><i></i><i></i></div><div class="wm">CareerMizing</div></div>'


# ---------------------------------------------------------------------------
# 본문 블록 — 어떤 슬라이드에서든 조합 가능. 크기·굵기·색은 CSS(기본 문법)로 고정.
# ---------------------------------------------------------------------------
def block(b, md, esc):
    k = b.get("kind")
    if k == "image":
        img = b.get("src")
        h = b.get("height", 431)
        w = b.get("width", 600)
        if img:
            return f'<div class="img" style="width:{w}px;height:{h}px;background-image:url({esc(img)})"></div>'
        return f'<div class="img ph" style="width:{w}px;height:{h}px" data-label="{esc(b.get("note", "이미지 자리 (사진·짤로 교체)"))}"></div>'
    if k == "quote":
        return f'<div class="qcard"><div class="ql">{md(b.get("label", ""))}</div><div class="qt">{md(b.get("text", ""))}</div></div>'
    if k == "cards":
        parts = []
        for j, c in enumerate(b.get("items", [])):
            if j and b.get("connect", True):
                parts.append('<div class="tri"></div>')
            on = " on" if c.get("on") else ""
            num = c.get("num", f"{j+1:02d}")
            numh = f'<div class="n">{md(num)}</div>' if num else ""
            parts.append(f'<div class="ncard{on}" style="min-height:{b.get("min_height", 200)}px">{numh}<div>'
                         f'<div class="t">{md(c.get("title", ""))}</div>'
                         + (f'<div class="d">{md(c["desc"])}</div>' if c.get("desc") else "") + "</div></div>")
        gap = "" if b.get("connect", True) else ' style="gap:20px"'
        return f'<div class="ncards"{gap}>{"".join(parts)}</div>'
    if k == "table":
        hd = b.get("columns", ["", ""])
        rows = "".join(f'<div class="rw{" on" if r.get("on") else ""}" style="min-height:{b.get("row_height", 196)}px"><div class="c1">{md(r["left"])}</div><div class="c2">{md(r["right"])}</div></div>'
                       for r in b.get("rows", []))
        return f'<div class="tbl"><div class="hd"><div class="c1" style="font-size:26px;color:inherit">{md(hd[0])}</div><div>{md(hd[1])}</div></div>{rows}</div>'
    if k == "bar":
        return '<div class="bar">' + "".join(f"<p>{md(p)}</p>" for p in b.get("paragraphs", [])) + "</div>"
    if k == "gray":
        strong = " strong" if b.get("strong") else ""
        return f'<div class="gcard"><div class="gl">{md(b.get("label", ""))}</div><div class="gt{strong}">{md(b.get("text", ""))}</div></div>'
    if k == "worksheet":
        its = []
        for it in b.get("items", []):
            sent = md(it.get("sentence", "")).replace("______", '<span class="bl"></span>')
            ex = f'<div class="wex">{md(it["example"])}</div>' if it.get("example") else ""
            its.append(f'<div class="it"><div class="wl">{md(it.get("label", ""))}</div><div class="wsn">{sent}</div>{ex}</div>')
        return f'<div class="ws">{"".join(its)}</div>'
    if k == "flow":
        parts = []
        for j, x in enumerate(b.get("items", [])):
            if j:
                parts.append('<div class="ar">↓</div>')
            parts.append(f'<div class="bx{" on" if x.get("on") else ""}"><div class="ft">{md(x["title"])}</div>'
                         + (f'<div class="fe">{md(x["example"])}</div>' if x.get("example") else "") + "</div>")
        return f'<div class="flow">{"".join(parts)}</div>'
    if k == "compare":
        def pn(p, kind):
            rows = ""
            for r in p.get("rows", []):
                x = ' class="x"' if r.get("strike") else ""
                rows += f'<div><span>{md(r["label"])}</span><span{x} style="font-weight:500;min-width:0;color:inherit">{md(r["value"])}</span></div>'
            rows = f'<div class="pr">{rows}</div>' if rows else ""
            return f'<div class="pn {kind}"><div class="pl">{md(p.get("label", ""))}</div><div class="pq">{md(p.get("quote", ""))}</div>{rows}</div>'
        return f'<div class="ba">{pn(b["before"], "before")}{pn(b["after"], "after")}</div>'
    if k == "pairs":
        out = []
        for p in b.get("items", []):
            tag = f'<div class="ptag">{md(p["tag"])}</div>' if p.get("tag") else ""
            out.append(f'<div class="pair">{tag}<div class="q g"><div class="ql">{md(p.get("gray_label", "일반 GPT"))}</div><div class="qt">{md(p["gray"])}</div></div>'
                       f'<div class="ar">▼</div><div class="q c"><div class="ql">{md(p.get("blue_label", "커리어마이징"))}</div><div class="qt">{md(p["blue"])}</div></div></div>')
        return f'<div class="pairs">{"".join(out)}</div>'
    if k == "panel":
        rows = "".join(f'<div class="row"><div class="pill">{md(r["tag"])}</div><div class="rt">{md(r["text"])}</div></div>' for r in b.get("rows", []))
        return f'<div class="panel"><div class="pt0">{md(b.get("title", ""))}</div>{rows}</div>'
    if k == "xlist":
        xrs = "".join(f'<div class="xr{" ok" if r.get("ok") else ""}"><div class="x">{"✓" if r.get("ok") else "×"}</div><div class="tx">{md(r["text"])}</div></div>' for r in b.get("rows", []))
        return f'<div class="xl"><div class="xt">{md(b.get("title", ""))}</div>{xrs}</div>'
    if k == "text":
        return f'<div class="txt">{md(b.get("text", ""))}</div>'
    if k == "spacer":
        return f'<div style="height:{b.get("h", 30)}px"></div>'
    return f'<div class="txt">[unknown block: {esc(k)}]</div>'


# 하위 호환: std_<kind> 슬라이드 = 블록 하나짜리 std_stack
LEGACY = {
    "std_meme": lambda s: ([{"kind": "image", "src": s.get("image"), "note": s.get("image_note", "이미지 자리 (사진·짤로 교체)")}]
                           + ([dict(kind="quote", **s["quote"])] if s.get("quote") else [])),
    "std_cards": lambda s: [{"kind": "cards", "items": s.get("cards", [])}],
    "std_table": lambda s: [{"kind": "table", "columns": s.get("columns", ["", ""]), "rows": s.get("rows", [])}],
    "std_answer": lambda s: [{"kind": "bar", "paragraphs": s.get("paragraphs", [])}] + ([dict(kind="gray", **s["card"])] if s.get("card") else []),
    "std_worksheet": lambda s: [{"kind": "worksheet", "items": s.get("items", [])}],
    "std_flow": lambda s: [{"kind": "flow", "items": s.get("boxes", [])}],
    "std_compare": lambda s: [{"kind": "compare", "before": s["before"], "after": s["after"]}],
    "std_pairs": lambda s: [{"kind": "pairs", "items": s.get("pairs", [])}],
    "std_panel": lambda s: ([dict(kind="panel", **s["panel"])] if s.get("panel") else []) + ([dict(kind="xlist", **s["xlist"])] if s.get("xlist") else []),
}


def build(spec, s, i, n, md, esc):
    t = s["type"]
    left = s.get("align") == "left"
    h1 = (f'<h1 class="{"left" if left else ""}">{md(s["headline"])}</h1>' if s.get("headline") else "")
    sub = (f'<div class="sub {"left" if left else ""}">{md(s["sub"])}</div>' if s.get("sub") else "")
    concl = ""
    if s.get("conclusion"):
        concl = f'<div class="concl {s.get("conclusion_style", "")}">{md(s["conclusion"])}</div>'
    disc = f'<div class="disc">{md(s["disclaimer"])}</div>' if s.get("disclaimer") else ""

    if t == "std_cover":
        img = s.get("image")
        bg = (f'<div class="bgimg has" style="background-image:url({esc(img)})"></div>' if img else '<div class="bgimg"></div>')
        ph = "" if img else f'<div class="phl">{esc(s.get("image_note", "표지 사진·짤 자리"))}</div>'
        top = f'<div class="top">{md(s["top"])}</div>' if s.get("top") else ""
        cs = f'<div class="cs">{md(s["sub"])}</div>' if s.get("sub") else ""
        src = f'<div class="src">{esc(s["source"])}</div>' if s.get("source") else ""
        return (f'<section class="slide std photo" id="s{i}" style="--dim:{s.get("dim", .3)}">{bg}<div class="dim"></div><div class="fade"></div>{ph}'
                f'{_asset()}{top}<div class="ch">{md(s["headline"])}</div>{cs}{src}</section>')

    if t == "std_cta":
        rows = "".join(f'<div class="ckr"><div class="cn">{md(r.get("num", f"{k+1:02d}"))}</div><div><div class="ct">{md(r["title"])}</div>'
                       + (f'<div class="cp">{md(r["prompt"])}</div>' if r.get("prompt") else "") + "</div></div>"
                       for k, r in enumerate(s.get("rows", [])))
        ph = (f'<div class="ph"><div class="h">{md(s.get("product", ""))}</div><div class="s">{md(s.get("product_sub", ""))}</div></div>' if s.get("product") else "")
        btn = f'<div class="btn">{md(s.get("button", ""))}</div>' if s.get("button") else ""
        pg = f'<div class="pg">{i:02d} / {n:02d}</div>' if s.get("page", True) else ""
        style = f' style="padding-top:{s["top"]}px"' if s.get("top") else ""
        return f'<section class="slide std dark" id="s{i}"{style}>{_asset()}{pg}<h1>{md(s["headline"])}</h1>{sub}<div class="ck">{rows}</div>{ph}{btn}</section>'

    if t == "std_service":
        img = s.get("image")
        shot = (f'<div class="shot" style="background-image:url({esc(img)})"></div>' if img
                else f'<div class="shot ph" data-label="{esc(s.get("image_note", "서비스 화면 캡처 자리"))}"></div>')
        ss = f'<div class="ss">{md(s["sub"])}</div>' if s.get("sub") else ""
        return (f'<section class="slide std svc" id="s{i}"><div class="cap">{md(s.get("pill", "CareerMizing"))}</div>{shot}'
                f'<div class="sh">{md(s["headline"])}</div>{ss}</section>')

    if t == "std_stack":
        blocks = s.get("blocks", [])
    elif t in LEGACY:
        blocks = LEGACY[t](s)
    else:
        blocks = [{"kind": "text", "text": f"[unknown std type: {t}]"}]
    mt = s.get("body_top", 28 if blocks and blocks[0].get("kind") == "image" else 48)
    body = f'<div class="body" style="margin-top:{mt}px">' + "".join(block(b, md, esc) for b in blocks) + "</div>"
    return f'<section class="slide std" id="s{i}">{_asset()}{h1}{sub}{body}{concl}{disc}</section>'
