---
name: careermizing-content
description: 커리어마이징(CareerMizing) 인스타그램 캐러셀 콘텐츠를 기획·카피라이팅·디자인 스펙·캡션까지 한 번에 만드는 콘텐츠 에이전트 스킬. 프로모션 / 정기 취준 정보(취준팁·면접팁·정보성) / 기업별(공채·D-3·기업분석) / 기능 홍보 네 유형의 서사 구조, 카피 톤(해요체+근거, 단정·보장·선착순 금지), 디자인 시스템(1080×1350, 포인트 블루 #2F5CE0, 네이비·라이트 테마, 컴포넌트 좌표), 캡션·해시태그, 자체 QA까지 포함한다. 사용자가 "캐러셀 만들어줘", "인스타 콘텐츠", "면접팁 7장", "공채 일정 정리 콘텐츠", "프로모션 카피", "D-3 콘텐츠", "기능 홍보 게시물", "캡션 써줘", "Figma에 올릴 카피", "커리어마이징 톤으로", "이 기획안을 슬라이드로" 등을 말하면 — 캐러셀·인스타그램이라는 단어가 없어도 커리어마이징의 취준생 대상 소셜 콘텐츠를 만들거나 고치는 요청이면 — 반드시 이 스킬을 사용한다. HTML/PNG 미리보기 렌더러를 포함한다.
---

# 커리어마이징 콘텐츠 에이전트

취준생을 위한 커리어마이징 인스타그램 캐러셀을 **기획안 → 장별 카피 → 디자인 스펙(JSON) → 미리보기 PNG → 캡션 → QA**까지 만든다. 원천은 Figma 「26 하반기 인스타그램 콘텐츠」 440여 장과 Notion 운영 SOP를 역설계한 `references/`다. 레퍼런스에 없는 규칙을 지어내지 말고, 모르면 레퍼런스를 먼저 연다.

## 왜 이 순서인가

이 채널은 "휘발성 바이럴"이 아니라 **저장할 만한 전문 정보로 신뢰를 쌓아 프로필 → 가입**으로 보내는 채널이다. 그래서 (1) 입구는 취준생의 고민처럼 쉽게, (2) 본문은 근거와 실제 발화로 깊게, (3) 제품은 마지막 장에서만, (4) 모든 수치·기출·가격은 확인된 것만 쓴다. 디자인은 네이비·화이트·블루 한 벌로 통일돼 있어 "커리어마이징 것"으로 보이게 하는 게 핵심이다.

## 작업 흐름

1. **유형 판정** — 요청을 넷 중 하나로 분류하고 해당 플레이북을 읽는다.
   - 취준팁·면접팁·정보성(일정/자격증/전형) → `references/content-types/job-info.md`
   - 프로모션(자료·플랜·기능 리뉴얼 판매) → `references/content-types/promotion.md`
   - 기업별(공채 오픈·D-3·채용 뉴스·기업 맞춤 기능) → `references/content-types/company.md`
   - 기능 홍보(출시·리뉴얼 공지) → `references/content-types/feature.md`
   어느 유형이든 `references/brand-voice.md`(톤·금지 표현·기능 명칭)는 반드시 읽는다.
2. **기획안(Brief)** — Layer / Persona / Moment / Pain·Question / One Sentence Insight / Hook 3안(A 최종·B 공감형·C 저장형) / Evidence Pack(출처+열람일, 미열람 데이터 명시) / Carousel Flow(장당 한 문장) / Proof(가상 예시 표시) / Main CTA 1개 / Success Metric. 사용자가 기획안을 이미 줬으면 빠진 필드만 채운다.
3. **장별 카피** — `references/components.md` §4의 서사 표로 장수와 역할을 정하고, 장마다 `메인(2행) / 서브 / 본문 / 하단 결론 / 면책 / Visual(아키타입)`을 쓴다. 톤은 brand-voice.md §2~§6. 예문이 필요하면 `references/copy-examples.md`.
4. **디자인 스펙** — 아키타입 이름(`cover_typo`, `text`, `cards`, `before_after`, `answer`, `cta_worksheet` …)과 테마를 지정하고 `assets/example-spec.json` 형식의 JSON을 쓴다. 토큰은 `assets/tokens.json`, 수치는 `references/design-system.md`.
5. **미리보기 렌더** — 아래 명령으로 HTML/PNG를 만들고 PNG를 직접 열어 본다. 넘침 경고(WARN)가 나오면 카피를 줄인다. 사용자에게는 PNG(또는 index.html)를 전달한다.
6. **캡션·배포** — `references/caption-guide.md`로 캡션·해시태그·Story 투표·Threads 한 문단을 쓴다. 캡션은 spec의 `caption` 필드에도 넣는다.
7. **QA** — `references/qa-checklist.md`로 자체 점검하고, 결과를 "검수 요청 템플릿" 형식으로 요약한다. 확인 못 한 수치·가격·기능 상태는 **"확인 필요"로 명시**한다(추정 금지).

Figma에 직접 올려야 하면 Figma MCP(`use_figma`, 사전 `figma-use` 스킬 필수)로 1080×1350 프레임을 만들고 섹션 이름을 `[STATUS] YYYYMMDD / 유형 / 주제 (NP)` 규칙으로 붙인다. 캐러셀 끝에 `NOTE · 캡션 & 검수 메모` 프레임을 추가한다.

## 렌더러

```bash
python3 scripts/render_carousel.py spec.json out_dir     # slide-NN.html + index.html + caption.txt
node scripts/snap.js out_dir                            # slide-NN.png (Playwright). 넘치면 WARN 출력
```

- 스펙: `title, canvas("1350"|"1440"), accent, font("pretendard"|"noto"), brand_mark("dot"|"logo"), slides[], caption`.
- 인라인 마크업: `{{포인트색}}`, `**굵게**`, `==형광펜==`, `~~취소선~~`, 줄바꿈 `\n`.
- 지원 type: `cover_typo cover_photo cover_promo text cards steps compare before_after answer chat table datalist checklist worksheet cta_worksheet promo_cards promo_cta cta_radial promo_brand feature benefit service_placeholder note`. 각 필드는 `scripts/render_carousel.py`의 `build_slide` 분기와 `assets/example-spec.json` 참조.
- 사진·캡처는 `image` 필드에 경로를 넣는다. 없으면 플레이스홀더(회색/네이비 그라디언트)로 렌더되고, 그 자리는 "이미지 교체 필요"로 보고한다.
- 폰트는 Pretendard/SUIT(jsdelivr) → Noto Sans KR(Google Fonts) 순으로 폴백한다. 오프라인이면 시스템 폰트로 렌더되므로 최종본은 Figma에서 확인하라고 안내한다.

## 절대 지킬 것 (brand-voice.md §8 요약)

- '무조건 탈락 / 모든 면접관 / 합격 보장 / 대기업 공통 기출(근거 없음) / 선착순' 금지. 기업 의도 단정 금지.
- 가상 답변은 반드시 "※ 이해를 돕기 위한 가상 답변입니다" 표시. 합격자 답변·실제 기출로 포장 금지.
- 가격·무료 횟수·기능 상태는 게시 당일 기준 확인 전엔 "확인 필요"로. 미배포 기능을 제공 중처럼 쓰지 않는다.
- 사진·캡처마다 출처 캡션 / "* 화면은 이해를 돕기 위한 예시입니다". 무단 인물 사진 금지.
- 제품은 마지막 장(과 홍보 1장)에서만. P1~P3 제품명 노출 없음(취준팁).
- 브랜드 표기 `CareerMizing` / 커리어마이징, 기능명은 공식 명칭(경험정리·마스터 이력서·기업별 이력서·기업분석·자기소개서 AI·면접).

## 산출물 형식

사용자에게 돌려줄 때는 이 순서로: ① 기획안 요약(Insight·Hook 3안·CTA) ② 장별 카피 표(P/역할/메인/서브/본문/결론/면책/아키타입) ③ 미리보기 PNG 경로 또는 첨부 ④ 캡션+해시태그 ⑤ QA 결과와 확인 필요 항목. 렌더하지 않았다면 그 이유를 적는다.

## 레퍼런스 지도

| 파일 | 언제 읽나 |
|---|---|
| `references/brand-voice.md` | 항상. 어미·훅 공식·강조 규칙·CTA·금지 표현·기능 명칭 |
| `references/design-system.md` | 디자인 스펙 쓸 때. 캔버스·테마 5종·컬러·타이포·그리드·로고·사진 규칙·치트시트 |
| `references/components.md` | 아키타입 고르고 장 구성할 때. 컴포넌트 40종·아키타입 22종·서사 표 |
| `references/content-types/*.md` | 유형별 구조·카피 템플릿·가격/근거 규칙 |
| `references/caption-guide.md` | 캡션·해시태그·UTM |
| `references/qa-checklist.md` | 제출 전 점검·검수 요청·상태/네이밍 |
| `references/copy-examples.md` | 실제 카피 전문(면접팁 7P, 정보성, 프로모션, 검수 메모) |
| `assets/tokens.json`, `assets/example-spec.json` | 렌더러 입력 |
