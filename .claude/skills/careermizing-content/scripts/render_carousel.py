#!/usr/bin/env python3
"""
커리어마이징 캐러셀 미리보기 렌더러.

JSON 스펙(슬라이드 배열) → 1080×1350(또는 1440) HTML 슬라이드 + index.html(한 줄 미리보기).
PNG가 필요하면 같은 폴더의 snap.js(Playwright)를 돌린다.

사용:
  python3 render_carousel.py spec.json out_dir
  node snap.js out_dir            # slide-01.png … 생성

스펙 형식은 ../assets/example-spec.json 과 SKILL.md 참고.
인라인 마크업: {{포인트색}}  **굵게**  ==형광펜==  ~~취소선~~  [[보통 굵기]]  줄바꿈은 \n
"""
import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import std_format  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TOKENS = json.load(open(os.path.join(HERE, "..", "assets", "tokens.json"), encoding="utf-8"))

FONT_LINKS = {
    # Pretendard / SUIT 는 jsdelivr, 나머지는 Google Fonts. 네트워크가 막히면 Noto Sans KR → 시스템 폰트로 폴백.
    "pretendard": [
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">',
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/sun-typeface/SUIT@2/fonts/variable/woff2/SUIT-Variable.css">',
    ],
    "google": [
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&family=Nanum+Pen+Script&family=Raleway:wght@100;600&family=Inter:wght@500;600;700&display=swap" rel="stylesheet">',
    ],
}


# ---------- inline markup ----------
def md(text, accent_class="pt"):
    if text is None:
        return ""
    if isinstance(text, list):
        text = "\n".join(text)
    t = html.escape(str(text), quote=False)
    t = re.sub(r"\{\{(.+?)\}\}", rf'<span class="{accent_class}">\1</span>', t, flags=re.S)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t, flags=re.S)
    t = re.sub(r"==(.+?)==", r'<mark>\1</mark>', t, flags=re.S)
    t = re.sub(r"~~(.+?)~~", r"<s>\1</s>", t, flags=re.S)
    t = re.sub(r"\[\[(.+?)\]\]", r'<span class="r">\1</span>', t, flags=re.S)
    return t.replace("\n", "<br>")


def esc(s):
    return html.escape(str(s or ""), quote=True)


# ---------- CSS ----------
def build_css(spec):
    c = TOKENS["colors"]
    accent = spec.get("accent", c["brand"]["point"])
    canvas = str(spec.get("canvas", "1350"))
    h = 1440 if canvas == "1440" else 1350
    font = spec.get("font", "pretendard")
    if font == "noto":
        family = "'Noto Sans KR', 'Pretendard Variable', Pretendard, sans-serif"
        display = family
    else:
        family = "'Pretendard Variable', Pretendard, 'Noto Sans KR', sans-serif"
        display = "'SUIT Variable', SUIT, 'Pretendard Variable', Pretendard, 'Noto Sans KR', sans-serif"
    return f"""
:root {{
  --accent: {accent};
  --accent-soft: #EEF3FF; --accent-tint: #F0F7FF; --accent-chip: #E5F0FF; --accent-line: #C9D5F4;
  --navy: {c['dark']['bg_alt']}; --navy2: {c['dark']['bg']}; --navy-card: #0B1326; --navy-card-border: #213357;
  --text: {c['light']['text']}; --text2: {c['light']['text_secondary']}; --text3: {c['light']['text_tertiary']};
  --line: {c['light']['line']}; --line2: {c['light']['line_alt']}; --card-border: {c['light']['card_border_dark']};
  --hl: {c['light']['highlighter']}; --before: {c['status']['before_text']}; --before-bg: {c['status']['before_bg']};
  --yellow: {c['brand']['yellow_alt']}; --mint: {c['brand']['mint']};
  --dark-text2: {c['dark']['text_secondary']}; --dark-page: {c['dark']['page_alt']}; --dark-eyebrow: {c['dark']['eyebrow']};
  --dark-hook: {c['dark']['hook']}; --dark-small: {c['dark']['small']}; --caption: {c['light']['caption']};
  --W: 1080px; --H: {h}px;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #e9ecf1; }}
body {{ font-family: {family}; color: var(--text); -webkit-font-smoothing: antialiased; }}
.strip {{ display: flex; gap: 40px; padding: 40px; overflow-x: auto; align-items: flex-start; }}
.strip .slide {{ flex: 0 0 auto; box-shadow: 0 20px 60px rgba(0,0,0,.18); }}
.slide {{ position: relative; width: var(--W); height: var(--H); overflow: hidden; background: #fff; display: flex; flex-direction: column; padding: 164px 76px 58px; }}
.slide.dark {{ background: var(--navy); color: #fff; }}
.slide.dark2 {{ background: var(--navy2); color: #fff; }}
.slide.gray {{ background: #F2F4F8; }}
.slide.soft {{ background: #F7F9FD; }}
.slide.cream {{ background: #FAF7F1; color: #0A152E; }}
.slide.gradient {{ background: linear-gradient(180deg, #0B1530 0%, #050A1A 100%); color: #fff; }}
.slide.datalist {{ background: linear-gradient(180deg, #050D22 0%, #061028 100%); color: #F8FAFF; padding: 70px 64px 62px; }}
.slide.radial {{ background: radial-gradient(1296px 1296px at 540px -144px, #16308F 0%, #11246A 26%, #0C1745 52%, #070D28 100%); color: #fff; padding: 96px 72px 70px; }}
.slide.photo {{ background: #05091C; color: #fff; }}
.slide.photo .bg {{ position: absolute; inset: 0; background-size: cover; background-position: center; }}
.slide.photo .bg.placeholder {{ background: linear-gradient(135deg, #3b4a66 0%, #1b2538 100%); }}
.slide.photo .overlay {{ position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(0,0,0,.08) 23%, rgba(0,0,0,.28) 36.7%, rgba(0,0,0,.94) 91.8%); }}
.slide.photo .overlay.flat {{ background: rgba(8,13,23,.48); }}
.slide > * {{ position: relative; }}
.pt {{ color: var(--accent); }}
.dark .pt, .dark2 .pt, .gradient .pt {{ color: #73ABFF; }}
mark {{ background: linear-gradient(transparent 55%, var(--hl) 55%); color: inherit; padding: 0 2px; }}
s {{ color: var(--text3); }}
b {{ font-weight: 800; }}

/* 브랜드 마크 · 페이지 번호 */
.brand {{ position: absolute; left: 78px; top: 66px; display: flex; align-items: center; gap: 12px; font-weight: 500; font-size: 26px; color: var(--accent); letter-spacing: -0.3px; }}
.brand .dot {{ width: 25px; height: 25px; border-radius: 50%; background: var(--accent); }}
.dark .brand, .dark2 .brand, .gradient .brand, .photo .brand, .radial .brand {{ color: #fff; }}
.brand.logo {{ font-family: Raleway, sans-serif; font-weight: 600; font-size: 31px; gap: 10px; }}
.brand.logo .dot {{ width: 42px; height: 42px; background: radial-gradient(circle at 35% 35%, #7FA6FF, #1E3A8A); }}
.photo .brand.logo, .dark .brand.logo {{ background: linear-gradient(90deg, #BBD0FF, #FFF); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.light .brand.logo {{ background: linear-gradient(90deg, #323F91, #356FB6); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.page {{ position: absolute; right: 76px; top: 70px; font-size: 22px; font-weight: 500; color: var(--text2); letter-spacing: -0.3px; }}
.dark .page, .dark2 .page, .gradient .page, .photo .page, .radial .page {{ color: var(--dark-page); }}
.page.bottom {{ top: auto; bottom: 36px; }}

/* 텍스트 역할 */
.eyebrow {{ font-weight: 700; font-size: 34px; line-height: 1.4; color: var(--dark-eyebrow); margin-bottom: 28px; }}
.chip {{ display: inline-flex; align-items: center; height: 56px; padding: 0 26px; border-radius: 999px; font-weight: 700; font-size: 26px; background: var(--accent-chip); color: var(--accent); margin-bottom: 36px; align-self: flex-start; }}
.chip.solid {{ background: var(--accent); color: #fff; }}
.chip.ghost {{ background: rgba(255,255,255,.14); color: #fff; }}
.chip.white {{ background: #fff; color: #050A1A; }}
.chip.sm {{ height: 44px; font-size: 20px; padding: 0 18px; margin-bottom: 0; }}
h1.headline {{ font-weight: 900; font-size: 60px; line-height: 1.25; letter-spacing: -0.9px; word-break: keep-all; }}
.dark h1.headline, .dark2 h1.headline, .gradient h1.headline {{ font-size: 72px; line-height: 1.3; letter-spacing: -1.4px; }}
.center {{ text-align: center; }}
p.sub {{ font-weight: 500; font-size: 27px; line-height: 1.55; color: var(--text2); margin-top: 22px; word-break: keep-all; }}
.dark p.sub, .dark2 p.sub, .gradient p.sub {{ color: var(--dark-text2); font-size: 34px; }}
.body {{ margin-top: 40px; display: flex; flex-direction: column; gap: 28px; }}
.body p {{ font-weight: 500; font-size: 33px; line-height: 1.6; word-break: keep-all; }}
.dark .body p, .dark2 .body p, .gradient .body p {{ color: var(--dark-text2); }}
.conclusion {{ margin-top: auto; padding-top: 32px; text-align: center; font-weight: 700; font-size: 32px; line-height: 1.45; word-break: keep-all; }}
.disclaimer {{ margin-top: 20px; font-weight: 500; font-size: 23px; line-height: 1.4; color: var(--text2); }}
.dark .disclaimer, .gradient .disclaimer {{ color: var(--dark-text2); }}
.source {{ position: absolute; right: 40px; bottom: 36px; font-size: 17px; color: var(--caption); letter-spacing: -0.4px; }}
.footer {{ margin-top: auto; padding-top: 18px; border-top: 2px solid #E4E7EC; display: flex; justify-content: space-between; font-size: 19px; color: #8A909C; font-weight: 500; }}
.footer .next {{ font-weight: 700; color: #5C6270; }}

/* 카드류 */
.stack {{ margin-top: 40px; display: flex; flex-direction: column; gap: 18px; }}
.card {{ background: #fff; border: 1px solid var(--card-border); border-radius: 20px; padding: 26px 34px; }}
.gray .card, .soft .card {{ border-color: var(--line2); }}
.dark .card, .dark2 .card {{ background: var(--navy-card); border: 2px solid var(--navy-card-border); border-radius: 24px; }}
.gradient .card {{ background: #131D3C; border: 2px solid #334A85; border-radius: 24px; }}
.card.tint {{ background: var(--accent-tint); border: 2px solid var(--accent); }}
.card.highlight {{ background: var(--accent-soft); border: 1.5px solid var(--accent); }}
.dark .card.highlight {{ background: #142445; border: 2px solid #3370DB; }}
.card.navy {{ background: #1E2A44; border: 0; color: #fff; }}
.card.solid {{ background: var(--accent); border: 0; color: #fff; }}
.row {{ display: flex; gap: 28px; align-items: flex-start; }}
.num {{ flex: 0 0 auto; font-weight: 900; font-size: 36px; line-height: 1.2; color: var(--accent); min-width: 56px; }}
.dark .num, .dark2 .num, .gradient .num {{ color: var(--yellow); }}
.card:has(.num.square) {{ padding: 18px 28px; }}
.card:has(.num.square) .row {{ align-items: center; }}
.num.square {{ width: 72px; height: 72px; border-radius: 18px; background: var(--accent); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 28px; min-width: 0; }}
.card .label {{ font-weight: 700; font-size: 24px; color: var(--accent); margin-bottom: 10px; }}
.dark .card .label, .dark2 .card .label {{ color: #75ADFF; }}
.card .title {{ font-weight: 700; font-size: 33px; line-height: 1.4; word-break: keep-all; }}
.card .desc {{ font-weight: 500; font-size: 24px; line-height: 1.4; color: var(--text2); margin-top: 6px; word-break: keep-all; }}
.dark .card .desc, .dark2 .card .desc, .gradient .card .desc {{ color: var(--dark-text2); }}
.quote {{ margin-top: 36px; }}
.quote .qlabel {{ font-weight: 700; font-size: 25px; color: var(--text2); margin-bottom: 14px; }}
.quote .qtext {{ font-weight: 700; font-size: 35px; line-height: 1.65; color: var(--text2); word-break: keep-all; }}

/* 비교 */
.cols {{ margin-top: 44px; display: flex; gap: 24px; align-items: stretch; }}
.cols .col {{ flex: 1; border-radius: 28px; padding: 36px 30px; background: #fff; border: 2px solid var(--line); display: flex; flex-direction: column; gap: 22px; }}
.cols .col.right {{ background: var(--accent-tint); border-color: var(--accent); }}
.cols .col.before {{ background: var(--before-bg); border-color: #FFEAEA; flex: 0 0 40%; }}
.cols .col .ctitle {{ font-weight: 700; font-size: 32px; line-height: 1.45; word-break: keep-all; }}
.cols .col ul {{ list-style: none; display: flex; flex-direction: column; gap: 10px; }}
.cols .col li {{ font-weight: 500; font-size: 28px; line-height: 1.5; color: var(--text2); }}
.cols .col li::before {{ content: "• "; }}
.result {{ margin-top: auto; background: #fff; border: 2px solid #87B0FF; border-radius: 22px; padding: 26px 22px; font-weight: 900; font-size: 32px; line-height: 1.45; color: var(--accent); }}
.gradient .cols .col, .dark .cols .col, .dark2 .cols .col {{ background: #131D3C; border-color: #334A85; color: #fff; }}
.gradient .cols .col.right, .dark .cols .col.right, .dark2 .cols .col.right {{ background: #142445; border-color: #3370DB; }}
.gradient .cols .col li, .dark .cols .col li {{ color: #B8C4E0; }}
.gradient .result, .dark .result {{ background: #0B1326; border-color: #4A8FFF; color: #73ABFF; }}
.gradient .quote .qlabel, .dark .quote .qlabel {{ color: #B8C4E0; }}
.gradient .quote .qtext, .dark .quote .qtext {{ color: #fff; }}
.gradient .card .label {{ color: #FBC61E; }}
.gradient .card.highlight {{ background: #142445; border: 2px solid #3370DB; }}
.gradient .conclusion, .dark .conclusion {{ color: #fff; }}
.gradient .conclusion.yellow, .dark .conclusion.yellow {{ color: #FBC61E; }}
.radial .checklist-dark .ck {{ font-size: 36px; }}
.radial .button.big {{ background: #2E75F2; }}
.gradient mark, .dark mark, .dark2 mark, .radial mark {{ background: none; color: #FBC61E; }}
.c1440 {{ padding-bottom: 110px; }}
.c1440 .page.bottom {{ bottom: 44px; }}
.c1440 .source {{ bottom: 44px; right: 76px; }}
.c1440 .cover-photo {{ padding-bottom: 120px; }}
.chip.before-chip {{ background: #DB3838; color: #fff; }}
.chip.after-chip {{ background: var(--accent); color: #fff; }}
.chip.neutral {{ background: #1F242E; color: #fff; }}

/* BEFORE / AFTER (세로) */
.before-box {{ margin-top: 40px; background: var(--before-bg); border: 2px solid #FFEAEA; border-radius: 24px; padding: 28px 34px; display: flex; gap: 24px; align-items: center; }}
.before-box .blabel {{ font-weight: 700; font-size: 26px; color: var(--before); flex: 0 0 auto; }}
.before-box .btext {{ font-weight: 700; font-size: 30px; line-height: 1.5; text-decoration: line-through; color: var(--text3); }}
.after-card {{ margin-top: 22px; background: #fff; border: 1px solid var(--card-border); border-radius: 24px; padding: 30px 34px; }}
.after-card .alabel {{ font-weight: 700; font-size: 26px; color: var(--accent); margin-bottom: 18px; }}
.after-card .seg {{ display: flex; gap: 22px; align-items: flex-start; padding: 18px 0; }}
.after-card .seg + .seg {{ border-top: 2px solid #E3E8F0; }}
.tag {{ flex: 0 0 150px; height: 56px; border: 2px solid var(--accent); border-radius: 30px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 23px; color: var(--accent); background: #fff; }}
.after-card .seg p, .answer-card .seg p {{ font-weight: 500; font-size: 29px; line-height: 1.7; word-break: keep-all; flex: 1; }}

/* 답변 카드 */
.answer-card {{ margin-top: 40px; background: #fff; border: 1px solid var(--card-border); border-radius: 28px; padding: 40px 44px; display: flex; flex-direction: column; }}
.gray .answer-card {{ border: 0; border-radius: 36px; }}
.answer-card .alabel {{ align-self: flex-start; background: var(--accent); color: #fff; border-radius: 10px; padding: 8px 18px; font-weight: 700; font-size: 24px; margin-bottom: 26px; }}
.answer-card .seg {{ display: flex; gap: 24px; align-items: flex-start; padding: 16px 0; }}
.answer-card .seg + .seg {{ border-top: 2px solid #E3E8F0; }}
.answer-card .seg p {{ font-size: 31px; }}
.answer-card.bar {{ border: 0; padding: 0 0 0 48px; border-left: 10px solid var(--accent); border-radius: 0; }}

/* 대화 */
.chat {{ margin-top: 40px; display: flex; flex-direction: column; gap: 14px; align-items: center; }}
.chat .turn {{ width: 100%; background: #fff; border-radius: 28px; padding: 28px 40px; display: flex; gap: 30px; align-items: flex-start; }}
.chat .turn.interviewer {{ border: 4px solid var(--accent); }}
.chat .turn .who {{ flex: 0 0 90px; font-weight: 700; font-size: 24px; color: var(--text3); padding-top: 6px; }}
.chat .turn.interviewer .who {{ color: var(--accent); }}
.chat .turn p {{ font-weight: 700; font-size: 31px; line-height: 1.5; word-break: keep-all; }}
.chat .arrow {{ font-size: 22px; color: #B6C3DD; }}

/* 표 */
table.tbl {{ margin-top: 40px; width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #7EA0FF; border-radius: 14px; overflow: hidden; }}
table.tbl th {{ background: var(--accent-soft); color: var(--accent); font-weight: 800; font-size: 22px; text-align: left; padding: 18px 26px; }}
table.tbl td {{ padding: 24px 26px; font-size: 26px; line-height: 1.4; border-top: 1px solid #E4E7EC; vertical-align: top; word-break: keep-all; }}
table.tbl td:first-child {{ background: #FAFBFE; font-weight: 700; width: 34%; }}
table.tbl td + td {{ border-left: 1px solid #E4E7EC; font-weight: 500; color: var(--text2); }}
table.tbl td small {{ display: block; font-size: 20px; color: #8A909C; margin-top: 6px; }}

/* 다크 데이터 리스트 */
.datalist .logo-sm {{ font-family: Raleway, sans-serif; font-weight: 600; font-size: 22px; background: linear-gradient(90deg, #BBD0FF, #FFF); -webkit-background-clip: text; background-clip: text; color: transparent; margin-bottom: 60px; }}
.datalist h1.headline {{ font-size: 64px; line-height: 1.3; letter-spacing: -1.4px; font-weight: 800; }}
.datalist p.sub {{ font-size: 29px; color: #97A5C0; }}
.dl {{ margin-top: 48px; border-top: 1px solid #1F2430; }}
.dl .r {{ display: flex; gap: 22px; align-items: center; padding: 22px 0; border-bottom: 1px solid #424857; position: relative; }}
.dl .r.hi::after {{ content: ""; position: absolute; left: -36px; right: -36px; top: -4px; bottom: -4px; border: 9px solid #ECFFAD; border-radius: 34px; pointer-events: none; }}
.dl .d {{ flex: 0 0 152px; font-weight: 700; font-size: 25px; color: #7EA3FF; letter-spacing: -0.5px; }}
.dl .n {{ flex: 0 0 auto; font-weight: 900; font-size: 24px; color: #F8FAFF; min-width: 200px; }}
.dl .m {{ flex: 1; font-weight: 400; font-size: 22px; color: #97A5C0; line-height: 1.3; }}
.dl .s {{ flex: 0 0 auto; font-weight: 700; font-size: 25px; color: #F8FAFF; }}
.footnote {{ margin-top: auto; font-size: 20px; color: #8F9DB8; line-height: 1.4; }}

/* 체크리스트 / 워크시트 */
.checks {{ margin-top: 36px; border-top: 1px solid #E1E7F2; }}
.checks .c {{ display: flex; gap: 24px; align-items: center; padding: 30px 4px; border-bottom: 1px solid #E1E7F2; }}
.checks .box {{ width: 38px; height: 38px; border: 2px solid #C3CEDE; border-radius: 9px; flex: 0 0 auto; }}
.checks .cl {{ font-weight: 700; font-size: 31px; flex: 0 0 262px; }}
.checks .cd {{ font-size: 22px; color: #8A909C; line-height: 1.4; }}
.ws {{ margin-top: 40px; display: flex; flex-direction: column; gap: 20px; }}
.ws .item {{ background: #fff; border: 3px solid #E3E8F0; border-radius: 32px; padding: 30px 42px; }}
.dark .ws, .dark2 .ws {{ background: #F2F6FF; border-radius: 22px; padding: 28px; gap: 0; color: var(--text); }}
.dark .ws .item, .dark2 .ws .item {{ background: transparent; border: 0; border-radius: 0; padding: 18px 0; }}
.dark .ws .item + .item, .dark2 .ws .item + .item {{ border-top: 2px solid #CBD7F7; }}
.ws .wl {{ font-weight: 700; font-size: 28px; color: var(--accent); margin-bottom: 10px; }}
.ws .wsent {{ font-weight: 700; font-size: 33px; line-height: 1.5; word-break: keep-all; }}
.dark .ws .wsent, .dark2 .ws .wsent {{ font-weight: 500; font-size: 31px; color: var(--text); }}
.ws .wex {{ font-weight: 500; font-size: 26px; color: var(--text2); margin-top: 8px; }}
.blank {{ display: inline-block; min-width: 124px; border-bottom: 4px solid #9DB4E8; }}
.accent-bar {{ width: 111px; height: 9px; background: var(--accent); margin-bottom: 40px; }}
.path {{ margin-top: auto; font-weight: 500; font-size: 23px; color: #D5E1FB; line-height: 1.4; }}
.button {{ margin-top: 20px; background: var(--accent); color: #fff; border-radius: 15px; padding: 0 30px; height: 82px; display: flex; align-items: center; font-weight: 700; font-size: 34px; }}
.button.big {{ height: 130px; border-radius: 30px; justify-content: center; font-size: 42px; font-weight: 900; }}
.checklist-dark {{ margin-top: 48px; display: flex; flex-direction: column; gap: 34px; }}
.checklist-dark .ck {{ display: flex; gap: 22px; align-items: center; font-weight: 700; font-size: 38px; }}
.checklist-dark .ck::before {{ content: "✓"; color: #6EB0FF; font-weight: 900; font-size: 34px; }}

/* 표지 */
.cover-typo {{ padding: 245px 64px 90px; }}
.cover-typo .q {{ font-weight: 900; font-size: 78px; line-height: 1.3; letter-spacing: -1.2px; word-break: keep-all; }}
.cover-typo .bar {{ width: 135px; height: 8px; border-radius: 4px; background: var(--accent); margin: 44px 0 40px; }}
.cover-typo .hook {{ font-weight: 700; font-size: 40px; line-height: 1.45; color: var(--dark-hook); word-break: keep-all; }}
.cover-typo .small {{ margin-top: auto; font-weight: 500; font-size: 28px; line-height: 1.5; color: var(--dark-small); word-break: keep-all; }}
.cover-photo {{ padding: 90px 72px 60px; justify-content: flex-end; }}
.cover-photo .subtop {{ font-weight: 600; font-size: 50px; line-height: 1.3; letter-spacing: -1px; margin-bottom: 24px; word-break: keep-all; }}
.cover-photo .h {{ font-weight: 900; font-size: 100px; line-height: 1.12; letter-spacing: -2.5px; word-break: keep-all; }}
.cover-photo .subbottom {{ font-weight: 600; font-size: 44px; line-height: 1.35; margin-top: 36px; color: rgba(255,255,255,.95); word-break: keep-all; }}
.cover-photo .badge {{ align-self: flex-start; margin-top: 32px; background: #2E73FA; color: #fff; border-radius: 39px; padding: 16px 40px; font-weight: 700; font-size: 34px; }}
.cover-photo .period {{ font-weight: 600; font-size: 46px; color: rgba(255,255,255,.75); margin-bottom: 20px; }}

/* 라디얼 CTA */
.shot {{ margin-top: 26px; width: 100%; height: 560px; border-radius: 20px; border: 1px solid rgba(255,255,255,.1); box-shadow: 0 40px 120px rgba(0,0,0,.6); background: #DCE2EE; display: flex; align-items: center; justify-content: center; color: #8A93A3; font-size: 26px; font-weight: 500; text-align: center; line-height: 1.5; background-size: cover; background-position: top; }}
.radial .h {{ margin-top: 48px; font-weight: 800; font-size: 56px; line-height: 1.2; letter-spacing: -1.1px; color: rgba(255,255,255,.92); word-break: keep-all; }}
.radial .h .grad {{ background: linear-gradient(174.8deg, #FFF 30%, rgba(210,219,255,.95) 65%, rgba(160,180,255,.9) 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.radial .cta-row {{ margin-top: 44px; display: flex; gap: 20px; }}
.radial .cta-row .bar {{ width: 3px; height: 64px; border-radius: 2px; background: linear-gradient(to bottom, #4EF0A8, rgba(78,240,168,0)); flex: 0 0 auto; margin-top: 6px; }}
.radial .cta-row p {{ font-weight: 700; font-size: 44px; line-height: 1.3; color: rgba(255,255,255,.88); word-break: keep-all; }}
.photo .promo-h {{ font-family: Inter, sans-serif; font-weight: 700; font-size: 56px; line-height: 1.16; }}
.photo .promo-sub {{ margin-top: 24px; font-size: 24px; line-height: 1.3; color: #CCD5E2; }}

/* 기능/혜택 */
.feature-card {{ margin-top: 40px; background: #fff; border: 2px solid #E7ECF4; border-radius: 28px; padding: 44px 48px; box-shadow: 0 24px 30px rgba(13,35,110,.12); display: flex; flex-direction: column; gap: 18px; }}
.feature-card .inner {{ background: #F0F3F8; border-radius: 20px; padding: 34px; font-size: 27px; line-height: 1.55; color: #3C4352; }}
.price-row {{ background: #F0F3F8; border-radius: 20px; height: 101px; display: flex; align-items: center; justify-content: space-between; padding: 0 38px; font-weight: 600; font-size: 34px; }}
.price-row .old {{ text-decoration: line-through; color: #A6AFC0; margin-right: 18px; }}
.price-row .new {{ font-weight: 900; color: var(--accent); }}
.caption-sm {{ margin-top: 14px; text-align: right; font-size: 22px; color: #A6AFC0; }}
.placeholder-box {{ margin-top: 30px; background: #DCE2EE; border: 3px dashed #C9D2E0; border-radius: 28px; height: 540px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; color: #8A93A3; font-size: 26px; font-weight: 500; }}
.placeholder-box small {{ font-size: 21px; color: #A5ADBB; }}
.note {{ background: #FFF7DB; color: #262626; padding: 60px; font-size: 26px; line-height: 1.55; font-weight: 500; white-space: pre-wrap; }}
.emphasis {{ margin-top: 36px; font-weight: 500; font-size: 34px; line-height: 1.5; color: var(--yellow); word-break: keep-all; }}
.caption-dark {{ margin-top: auto; font-size: 24px; color: var(--dark-text2); }}
.img {{ margin-top: 36px; width: 100%; border-radius: 28px; background: #DCE2EE center/cover no-repeat; height: 430px; }}
"""


# ---------- slide builders ----------
def brand(spec, s, theme_cls):
    kind = s.get("brand", spec.get("brand_mark", "dot"))
    if kind == "none":
        return ""
    if kind == "logo":
        return '<div class="brand logo"><span class="dot"></span>CareerMizing</div>'
    return '<div class="brand"><span class="dot"></span>CareerMizing</div>'


CANVAS = {"v": "1350"}


def page_no(i, n, s, bottom=False):
    if s.get("page") is False:
        return ""
    if CANVAS["v"] == "1440":
        bottom = True
    cls = "page bottom" if bottom else "page"
    return f'<div class="{cls}">{i:02d} / {n:02d}</div>'


def headline(s, cls=""):
    h = s.get("headline")
    if not h:
        return ""
    return f'<h1 class="headline {cls}">{md(h)}</h1>'


def sub(s):
    return f'<p class="sub">{md(s["sub"])}</p>' if s.get("sub") else ""


def chip(s, default_cls=""):
    if not s.get("chip"):
        return ""
    return f'<div class="chip {s.get("chip_style", default_cls)}">{md(s["chip"])}</div>'


def conclusion(s):
    cls = "conclusion " + s.get("conclusion_style", "")
    return f'<div class="{cls.strip()}">{md(s["conclusion"])}</div>' if s.get("conclusion") else ""


def disclaimer(s):
    return f'<div class="disclaimer">{md(s["disclaimer"])}</div>' if s.get("disclaimer") else ""


def source(s):
    return f'<div class="source">{esc(s["source"])}</div>' if s.get("source") else ""


def footer(s):
    if not (s.get("footer_left") or s.get("footer_next")):
        return ""
    return (f'<div class="footer"><span>{md(s.get("footer_left", ""))}</span>'
            f'<span class="next">{md(s.get("footer_next", ""))}</span></div>')


def theme_class(s, default="light"):
    t = s.get("theme", default)
    return {"light": "light", "dark": "dark", "dark2": "dark2", "gray": "gray", "soft": "soft",
            "cream": "cream", "gradient": "gradient"}.get(t, "light")


def cards_html(cards, numbered=True, square=False):
    out = []
    for i, c in enumerate(cards, 1):
        num = c.get("num", f"{i:02d}" if numbered else "")
        numcls = "num square" if square else "num"
        numh = f'<div class="{numcls}">{md(num)}</div>' if num else ""
        label = f'<div class="label">{md(c["label"])}</div>' if c.get("label") else ""
        title = f'<div class="title">{md(c.get("title", ""))}</div>' if c.get("title") else ""
        desc = f'<div class="desc">{md(c["desc"])}</div>' if c.get("desc") else ""
        extra = " " + c["style"] if c.get("style") else ""
        out.append(f'<div class="card{extra}"><div class="row">{numh}<div style="flex:1">{label}{title}{desc}</div></div></div>')
    return "".join(out)


def build_slide(spec, s, i, n):
    t = s["type"]
    if t.startswith("std_"):
        return std_format.build(spec, s, i, n, md, esc)
    th = theme_class(s, {"cover_typo": "dark", "cta_worksheet": "dark", "datalist": "datalist",
                         "promo_cards": "gradient", "promo_cta": "dark2", "steps": "light",
                         "service_placeholder": "dark2"}.get(t, "light"))
    inner = ""
    extra_cls = ""

    if t == "cover_typo":
        th = "dark"
        extra_cls = "cover-typo"
        inner = (page_no(i, n, s) + brand(spec, s, th)
                 + (f'<div class="eyebrow">{md(s.get("eyebrow"))}</div>' if s.get("eyebrow") else "")
                 + f'<div class="q">{md(s.get("headline"))}</div>'
                 + '<div class="bar"></div>'
                 + (f'<div class="hook">{md(s.get("hook"))}</div>' if s.get("hook") else "")
                 + (f'<div class="small">{md(s.get("small"))}</div>' if s.get("small") else ""))

    elif t in ("cover_photo", "cover_promo"):
        th = "photo"
        extra_cls = "cover-photo"
        img = s.get("image")
        bg = (f'<div class="bg" style="background-image:url({esc(img)})"></div>' if img
              else '<div class="bg placeholder"></div>')
        ov = '<div class="overlay flat"></div>' if s.get("overlay") == "flat" else '<div class="overlay"></div>'
        parts = [bg, ov]
        if s.get("brand", "logo") != "none":
            parts.append('<div class="brand logo" style="top:90px;left:65px"><span class="dot"></span>CareerMizing</div>')
        parts.append(page_no(i, n, s))
        if s.get("period"):
            parts.append(f'<div class="period">{md(s["period"])}</div>')
        if s.get("sub_top"):
            parts.append(f'<div class="subtop">{md(s["sub_top"])}</div>')
        parts.append(f'<div class="h">{md(s.get("headline"))}</div>')
        if s.get("sub_bottom"):
            parts.append(f'<div class="subbottom">{md(s["sub_bottom"])}</div>')
        if s.get("badge"):
            parts.append(f'<div class="badge">{md(s["badge"])}</div>')
        parts.append(source(s))
        inner = "".join(parts)

    elif t == "text":
        body = ""
        if s.get("body"):
            paras = s["body"] if isinstance(s["body"], list) else [s["body"]]
            body = '<div class="body">' + "".join(f"<p>{md(p)}</p>" for p in paras) + "</div>"
        quote = ""
        if s.get("quote"):
            q = s["quote"]
            quote = (f'<div class="quote"><div class="qlabel">{md(q.get("label", ""))}</div>'
                     f'<div class="qtext">{md(q.get("text", ""))}</div></div>')
        img = f'<div class="img" style="background-image:url({esc(s["image"])})"></div>' if s.get("image") else ""
        hl = f'<div class="stack"><div class="card highlight"><div class="title">{md(s["highlight"])}</div></div></div>' if s.get("highlight") else ""
        inner = (page_no(i, n, s) + brand(spec, s, th) + chip(s) + headline(s, "center" if s.get("align") == "center" else "")
                 + sub(s) + quote + body + img + hl + conclusion(s) + disclaimer(s) + footer(s))

    elif t in ("cards", "steps"):
        cards = s.get("cards") or [{"title": x} for x in s.get("steps", [])]
        square = t == "steps"
        hl = f'<div class="card highlight" style="margin-top:22px"><div class="title">{md(s["highlight"])}</div></div>' if s.get("highlight") else ""
        bar = f'<div class="card highlight center" style="margin-top:22px"><div class="title pt" style="font-weight:900">{md(s["bar"])}</div></div>' if s.get("bar") else ""
        inner = (page_no(i, n, s) + brand(spec, s, th) + chip(s) + headline(s) + sub(s)
                 + f'<div class="stack">{cards_html(cards, s.get("numbered", True), square)}{hl}{bar}</div>'
                 + conclusion(s) + disclaimer(s) + footer(s))

    elif t == "compare":
        def col(c, cls):
            chip_cls = c.get("chip_style", "neutral" if cls == "left" else "after-chip")
            ch = f'<div class="chip sm {chip_cls}">{md(c["chip"])}</div>' if c.get("chip") else ""
            title = f'<div class="ctitle">{md(c["title"])}</div>' if c.get("title") else ""
            bullets = ("<ul>" + "".join(f"<li>{md(b)}</li>" for b in c.get("bullets", [])) + "</ul>") if c.get("bullets") else ""
            result = f'<div class="result">{md(c["result"])}</div>' if c.get("result") else ""
            return f'<div class="col {cls}">{ch}{title}{bullets}{result}</div>'
        left_cls = "left before" if s.get("left", {}).get("chip_style") == "before-chip" else "left"
        inner = (page_no(i, n, s) + brand(spec, s, th) + chip(s) + headline(s) + sub(s)
                 + f'<div class="cols">{col(s["left"], left_cls)}{col(s["right"], "right")}</div>'
                 + conclusion(s) + disclaimer(s))

    elif t == "before_after":
        segs = "".join(
            f'<div class="seg">' + (f'<div class="tag">{md(a["tag"])}</div>' if a.get("tag") else "") + f'<p>{md(a["text"])}</p></div>'
            for a in s.get("after", []))
        inner = (page_no(i, n, s) + brand(spec, s, th) + headline(s) + sub(s)
                 + f'<div class="before-box"><div class="blabel">BEFORE</div><div class="btext">{md(s.get("before", ""))}</div></div>'
                 + f'<div class="after-card"><div class="alabel">AFTER</div>{segs}</div>'
                 + conclusion(s) + disclaimer(s))

    elif t == "answer":
        segs = "".join(
            f'<div class="seg"><p>{md(p["text"])}</p>' + (f'<div class="tag">{md(p["tag"])}</div>' if p.get("tag") else "") + "</div>"
            for p in s.get("paragraphs", []))
        label = f'<div class="alabel">{md(s["label"])}</div>' if s.get("label") else ""
        cls = "answer-card bar" if s.get("style") == "bar" else "answer-card"
        inner = (page_no(i, n, s) + brand(spec, s, th) + headline(s, "center" if s.get("align") == "center" else "") + sub(s)
                 + f'<div class="{cls}">{label}{segs}</div>' + conclusion(s) + disclaimer(s))

    elif t == "chat":
        turns = []
        for k, tn in enumerate(s.get("turns", [])):
            who_cls = "interviewer" if tn.get("who") == "interviewer" else "applicant"
            who = "면접관" if who_cls == "interviewer" else "지원자"
            if k:
                turns.append('<div class="arrow">▼</div>')
            turns.append(f'<div class="turn {who_cls}"><div class="who">{who}</div><p>{md(tn["text"])}</p></div>')
        inner = (page_no(i, n, s) + brand(spec, s, th) + headline(s, "center") + sub(s)
                 + '<div class="chat">' + "".join(turns) + "</div>" + conclusion(s) + disclaimer(s))

    elif t == "table":
        cols = s.get("columns", [])
        thead = "<tr>" + "".join(f"<th>{md(c)}</th>" for c in cols) + "</tr>" if cols else ""
        rows = ""
        for r in s.get("rows", []):
            cells = []
            for cell in r:
                if isinstance(cell, dict):
                    cells.append(f'<td>{md(cell.get("text", ""))}<small>{md(cell.get("note", ""))}</small></td>')
                else:
                    cells.append(f"<td>{md(cell)}</td>")
            rows += "<tr>" + "".join(cells) + "</tr>"
        inner = (page_no(i, n, s) + brand(spec, s, th) + headline(s) + sub(s)
                 + f'<table class="tbl">{thead}{rows}</table>' + conclusion(s) + disclaimer(s) + footer(s))

    elif t == "datalist":
        th = "datalist"
        rows = ""
        for r in s.get("rows", []):
            hi = " hi" if r.get("highlight") else ""
            rows += (f'<div class="r{hi}"><div class="d">{md(r.get("date", ""))}</div><div class="n">{md(r.get("name", ""))}</div>'
                     f'<div class="m">{md(r.get("memo", ""))}</div><div class="s">{md(r.get("status", ""))}</div></div>')
        inner = (page_no(i, n, s) + '<div class="logo-sm">CareerMizing</div>' + headline(s) + sub(s)
                 + f'<div class="dl">{rows}</div>'
                 + (f'<div class="footnote">{md(s["footnote"])}</div>' if s.get("footnote") else ""))

    elif t == "checklist":
        items = "".join(f'<div class="c"><div class="box"></div><div class="cl">{md(it.get("label", ""))}</div><div class="cd">{md(it.get("desc", ""))}</div></div>'
                        for it in s.get("items", []))
        box = ""
        if s.get("box"):
            b = s["box"]
            box = (f'<div class="stack"><div class="card navy"><div class="title">{md(b.get("title", ""))}</div>'
                   f'<div class="desc" style="color:rgba(255,255,255,.62)">{md(b.get("text", ""))}</div></div></div>')
        inner = (page_no(i, n, s) + brand(spec, s, th) + headline(s) + sub(s) + f'<div class="checks">{items}</div>' + box
                 + conclusion(s) + disclaimer(s) + footer(s))

    elif t in ("worksheet", "cta_worksheet"):
        if t == "cta_worksheet":
            th = "dark"
        items = ""
        for it in s.get("items", []):
            sent = md(it.get("sentence", "")).replace("______", '<span class="blank"></span>').replace("__", '<span class="blank" style="min-width:90px"></span>')
            ex = f'<div class="wex">{md(it["example"])}</div>' if it.get("example") else ""
            items += f'<div class="item"><div class="wl">{md(it.get("label", ""))}</div><div class="wsent">{sent}</div>{ex}</div>'
        pre = '<div class="accent-bar"></div>' if t == "cta_worksheet" else ""
        tail = ""
        if t == "cta_worksheet":
            tail = ((f'<div class="path">{md(s["path"])}</div>' if s.get("path") else '<div class="path"></div>')
                    + (f'<div class="button">{md(s["button"])}</div>' if s.get("button") else ""))
        else:
            tail = conclusion(s) + disclaimer(s)
        inner = page_no(i, n, s) + brand(spec, s, th) + pre + headline(s) + sub(s) + f'<div class="ws">{items}</div>' + tail

    elif t == "promo_cards":
        th = "gradient"
        body = f'<div class="body"><p>{md(s["body"])}</p></div>' if s.get("body") else ""
        emp = f'<div class="emphasis">{md(s["emphasis"])}</div>' if s.get("emphasis") else ""
        cap = f'<div class="caption-dark">{md(s["caption"])}</div>' if s.get("caption") else ""
        inner = (page_no(i, n, s) + (f'<div class="chip white">{md(s["tag"])}</div>' if s.get("tag") else "")
                 + headline(s) + body + f'<div class="stack">{cards_html(s.get("cards", []), True)}</div>' + emp + cap)

    elif t == "promo_cta":
        th = "radial" if s.get("theme") == "radial" else "dark2"
        checks = "".join(f'<div class="ck">{md(c)}</div>' for c in s.get("checks", []))
        inner = (page_no(i, n, s) + (f'<div class="chip solid">{md(s["chip"])}</div>' if s.get("chip") else "")
                 + headline(s) + f'<div class="checklist-dark">{checks}</div>'
                 + f'<div class="button big" style="margin-top:auto">{md(s.get("button", ""))}</div>'
                 + (f'<div class="conclusion" style="margin-top:36px;font-weight:500;color:#C7D4E8;font-size:30px">{md(s["sub"])}</div>' if s.get("sub") else ""))

    elif t == "cta_radial":
        th = "radial"
        lines = s.get("headline_lines", [])
        h = "<br>".join(md(x) for x in lines[:-1]) + (f'<br><span class="grad">{md(lines[-1])}</span>' if lines else "")
        shot = (f'<div class="shot" style="background-image:url({esc(s["image"])})"></div>' if s.get("image")
                else f'<div class="shot">서비스 화면 캡처 자리<br><small>{esc(s.get("placeholder", "예: 대기업 특화 취준 AI 기업분석 화면"))}</small></div>')
        inner = (f'<div class="chip ghost">{md(s.get("pill", "Careermizing"))}</div>' + shot
                 + f'<div class="h">{h}</div>'
                 + f'<div class="cta-row"><div class="bar"></div><p>{md(s.get("cta", ""))}</p></div>')

    elif t == "promo_brand":
        th = "photo"
        img = s.get("image")
        bg = (f'<div class="bg" style="background-image:url({esc(img)})"></div>' if img else '<div class="bg placeholder"></div>')
        inner = (bg + '<div class="overlay" style="background:linear-gradient(to bottom,#000 9.9%,rgba(0,0,0,.28) 52.5%,rgba(0,0,0,.94) 91.8%)"></div>'
                 + f'<div class="chip white sm" style="margin-top:-60px;margin-bottom:40px">{md(s.get("chip", "커리어마이징"))}</div>'
                 + f'<div class="promo-h">{md(s.get("headline"))}</div>'
                 + (f'<div class="promo-sub">{md(s["sub"])}</div>' if s.get("sub") else "")
                 + '<div class="brand logo" style="top:auto;bottom:70px;left:58px;font-size:24px"><span class="dot" style="width:30px;height:30px"></span>CareerMizing</div>')

    elif t == "feature":
        card = ""
        if s.get("card"):
            c = s["card"]
            chips = "".join(f'<span class="chip sm {("solid" if k == 0 else "")}" style="margin-right:12px">{md(x)}</span>' for k, x in enumerate(c.get("chips", [])))
            card = (f'<div class="feature-card"><div>{chips}</div>'
                    + (f'<div class="title">{md(c["title"])}</div>' if c.get("title") else "")
                    + f'<div class="inner">{md(c.get("text", ""))}</div>'
                    + (f'<div><span class="chip sm" style="background:#EAF0F7;color:#3C4352">{md(c["source"])}</span></div>' if c.get("source") else "")
                    + "</div>")
        img = f'<div class="img" style="height:583px;background-image:url({esc(s["image"])})"></div>' if s.get("image") else ""
        body = f'<div class="body"><p>{md(s["body"])}</p></div>' if s.get("body") else ""
        inner = (page_no(i, n, s) + chip(s, "solid") + headline(s) + body + img + card
                 + f'<div class="caption-sm">{esc(s.get("caption", "* 화면은 이해를 돕기 위한 예시입니다"))}</div>' + conclusion(s))

    elif t == "benefit":
        rows = "".join(f'<div class="price-row"><span>{md(r["label"])}</span><span><span class="old">{md(r.get("old", ""))}</span><span class="new">{md(r.get("new", ""))}</span></span></div>'
                       for r in s.get("prices", []))
        inner = (page_no(i, n, s) + chip(s) + headline(s)
                 + (f'<p class="sub" style="color:var(--text);font-weight:600;font-size:36px">{md(s["period"])}</p>' if s.get("period") else "")
                 + f'<div class="stack">{rows}</div>'
                 + (f'<div class="body"><p style="font-size:30px;color:#616161">{md(s["terms"])}</p></div>' if s.get("terms") else "")
                 + conclusion(s))

    elif t == "service_placeholder":
        th = "dark2"
        inner = ('<div class="chip ghost">Careermizing</div>'
                 + f'<div class="placeholder-box">서비스 화면 캡처 자리<small>{esc(s.get("placeholder", "예: 경험정리 → 꼬리질문 연습 화면"))}</small></div>'
                 + f'<h1 class="headline" style="font-size:48px;margin-top:40px">{md(s.get("headline"))}</h1>'
                 + (f'<div class="cta-row" style="margin-top:30px;display:flex;gap:20px"><div style="width:6px;background:#fff;border-radius:3px"></div><p style="font-size:33px;line-height:1.6;color:rgba(255,255,255,.92);font-weight:500">{md(s["sub"])}</p></div>' if s.get("sub") else ""))

    elif t == "note":
        return f'<section class="slide note" id="s{i}">{esc(s.get("text", ""))}</section>'

    else:
        inner = f'<h1 class="headline">[unknown type: {esc(t)}]</h1>'

    c1440 = ' c1440' if CANVAS['v'] == '1440' else ''
    return f'<section class="slide {th} {extra_cls}{c1440}" id="s{i}">{inner}</section>'


def page_html(spec, body, css, title):
    font = spec.get("font", "pretendard")
    links = "\n".join((FONT_LINKS["pretendard"] if font != "noto" else []) + FONT_LINKS["google"])
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><title>{esc(title)}</title>
{links}
<style>{css}</style></head>
<body>{body}</body></html>"""


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    spec_path, out_dir = sys.argv[1], sys.argv[2]
    spec = json.load(open(spec_path, encoding="utf-8"))
    CANVAS["v"] = str(spec.get("canvas", "1350"))
    os.makedirs(out_dir, exist_ok=True)
    css = build_css(spec) + std_format.css(spec.get("accent", TOKENS["colors"]["brand"]["point"]))
    slides = spec["slides"]
    n = len([s for s in slides if s.get("type") != "note"])
    rendered = []
    for i, s in enumerate(slides, 1):
        idx = min(i, n)
        html_slide = build_slide(spec, s, idx, n)
        rendered.append(html_slide)
        with open(os.path.join(out_dir, f"slide-{i:02d}.html"), "w", encoding="utf-8") as f:
            f.write(page_html(spec, html_slide, css, f'{spec.get("title", "carousel")} {i:02d}'))
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page_html(spec, '<div class="strip">' + "".join(rendered) + "</div>", css, spec.get("title", "carousel")))
    if spec.get("caption"):
        with open(os.path.join(out_dir, "caption.txt"), "w", encoding="utf-8") as f:
            f.write(spec["caption"].strip() + "\n")
    shutil.copy(spec_path, os.path.join(out_dir, "spec.json"))
    print(f"rendered {len(slides)} slides → {out_dir}/index.html")
    print(f"PNG: node {os.path.join(HERE, 'snap.js')} {out_dir}")


if __name__ == "__main__":
    main()
