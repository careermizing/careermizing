---
name: imc-slide-design
description: 마케팅 IMC 제안서 장표(pptx)를 레퍼런스 덱(아르르 푸드·에너지플러스) 수준의 디자인으로 초안 제작할 때 쓰는 스킬. 스토리라인을 장표 유형(archetype)에 매핑하고, python-pptx 빌더(imc_deck.py)로 16:9 편집 가능한 pptx를 만든다. "장표 초안", "ppt 만들어", "IMC 발표자료", "제안서 슬라이드" 요청에 사용.
---

# IMC 장표 디자인 스킬

두 레퍼런스 덱(아르르 푸드 49p, 에너지플러스 93p)에서 뽑은 디자인 문법을 **장표 유형 함수**로 옮겨 둔 빌더다.
결과물은 전부 **편집 가능한 pptx**(텍스트·도형·네이티브 차트)이고, 시안 이미지/목업 자리는 **빈 플레이스홀더**로 남긴다(나중에 목업·이미지로 교체).

## 구성

| 파일 | 역할 |
|---|---|
| `scripts/imc_deck.py` | 빌더 라이브러리 (`Deck` 클래스, 20개 장표 유형, 린트, 저장) |
| `scripts/ir_kit.py` | **2차부터 기본 빌더.** IR 덱 스킬(chief-staff `careermizing-ir-deck`의 `cm_deck.py`)을 틸 팔레트로 재색한 pt 단위 컴포넌트 (유리 카드, 말풍선 pill, 진행선, KPI 타일, 도형 막대, 벡터 아이소메트릭 일러스트). 두위드 에셋·카피라이트는 제외 |
| `scripts/render.sh` | pptx → pdf → png + `contact.png` 컨택트시트 (Pretendard 자동 설치). `pptx2pdf.py`로 한글-영문 자동 간격을 끄고 변환 |
| `examples/showcase.py` (+ `showcase.pptx`, `showcase_contact.png` 미리보기) | 모든 유형을 한 번씩 쓰는 20장 샘플 (오늘의집 스토리라인 내용). 사용법 참고용 |
| `references/design-system.md` | 색·타입·간격·문장 규칙 (왜 이렇게 생겼는지, do/don't) |
| `references/archetypes.md` | 유형 카탈로그: 언제 쓰는지, 시그니처, 레퍼런스 출처 |
| `references/storyline-to-slides.md` | 오늘의집 스토리라인 V3(20P) → 유형 매핑표와 제작 순서 |

## 두 가지 빌더

- `ir_kit.py` (권장): 960×540pt 그리드. 좌측 정렬 **한 줄 헤드라인(24B) + 한 줄 서브헤드(18M)**, 3열 카드 x=38/337/636(폭 285), 2열 x=38/492(폭 430), pill 행 y=162 → 카드 y=215~483, 각주 좌하단. 사용 예: `ohou-team-project/deck/build_deck_v2.py`. 상세 규칙은 chief-staff `careermizing-ir-deck/references/design-system.md`, `copy-tone.md`를 따른다(강조 카드·하이라이트는 장표당 1개, 병렬 항목 사이에는 진행선을 긋지 않는다).
- `imc_deck.py` (1차): inch 단위 장표 유형 함수. 빠른 초안용.

## 작업 순서

1. **스토리라인 확정 확인** — 장표마다 "한 문장 주장"이 있어야 한다. 없으면 먼저 `references/storyline-to-slides.md` 매핑표로 장표별 주장·근거·유형을 표로 정리한다.
2. **유형 선택** — `references/archetypes.md`에서 장표의 목적에 맞는 유형을 고른다. 유형에 안 맞으면 `Deck`의 기본 부품(`title`, `pill`, `text`, `rect`, `table`, `hbar`, `callout`, `source` …)을 조합한다. 새 레이아웃을 즉흥으로 짜지 말고, 두 번 이상 쓰이면 유형으로 승격한다.
3. **빌드** — 작업용 스크립트를 `build_deck.py`로 만들어 `sys.path`에 `scripts/`를 넣고 `Deck`을 쓴다. `examples/showcase.py` 구조를 그대로 따른다.
   ```python
   import sys; sys.path.insert(0, ".claude/skills/imc-slide-design/scripts")
   from imc_deck import Deck
   d = Deck(brand="OHOUSE", team="디지털마케팅 5조")
   d.cover("제목", "부제", "팀 | 날짜")
   d.bars_and_notes("문제 발견", "…합니다", [...], "…", "…", [...], focus=(2,), source="출처: …")
   print("\n".join(d.lint()) or "lint ok")
   d.save("out/deck.pptx")
   ```
4. **린트** — `d.lint()`가 텍스트 박스 넘침을 Pretendard 폭 기준으로 추정해 알려준다. 경고가 0이 될 때까지 문장을 줄이거나 크기를 조정한다.
5. **렌더 확인** — `bash scripts/render.sh out/deck.pptx out/render 60` 후 `contact.png`와 개별 `p-XX.png`를 눈으로 확인한다. 린트만 믿지 않는다.
6. **내용 검수** — 수치·출처가 팀 자료(설문 n=51, 인터뷰 n=5, 문헌)와 일치하는지 확인. 샘플 수치를 그대로 두지 않는다.

## 지켜야 할 규칙 (요약)

- 장표 제목 = **주장 한 문장, ~합니다 체**, 2줄 이내. 핵심 구절만 `==하이라이트==`.
- 색은 **주색 한 계열 + 회색 + 경고 빨강(문제 수치에만)**. 새 색을 추가하지 않는다.
- 차트·막대는 **핵심 하나만 진하게**, 나머지는 회색. 필요하면 점선 박스로 묶는다.
- 모든 수치에는 **출처·N** 캡션(작은 회색). 출처 없는 수치는 넣지 않는다.
- 장표 하단에 **결론 한 줄(callout)** 을 두는 장표는 근거 장표(문제·원인)에 한정한다. 전략·실행 장표에는 남발하지 않는다.
- 본문 최소 크기 12pt(부록·캡션 제외). 한 장표에 메시지는 하나.
- 이미지·목업·로고 자리는 `image()`/`phone()` 플레이스홀더로 두고, 플레이스홀더에는 **무엇이 들어갈지** 라벨을 적는다.
- 기획 시안·가상 수치임이 분명한 요소(가상 RFP 예산, 목업 UI)에는 "기획 시안" 표기를 넣는다.
- 글꼴은 **Pretendard**. 발표 PC에 없으면 폰트가 바뀌어 줄바꿈이 틀어지므로, 제출 시 PDF도 함께 만든다.

## 알려진 한계

- LibreOffice 기본 변환은 한글-숫자/영문 사이에 간격을 넣는다(Asian autospace). `render.sh`는 `pptx2pdf.py`(UNO)로 이 옵션을 끄고 변환하므로 PowerPoint와 폭이 같다. UNO 변환이 실패하면 기본 변환으로 대체되며 경고를 띄운다.
- 차트는 도넛만 네이티브 차트다. 막대는 도형으로 그리므로 값을 바꾸면 `hbar` 인자를 다시 넣어야 한다.
- 표는 셀마다 사각형으로 만든다(렌더 안정성). 파워포인트 표 객체가 필요하면 별도 변환이 필요하다.
- 레퍼런스 덱의 이미지·일러스트·로고는 복제하지 않는다(구조·문법만 차용).
