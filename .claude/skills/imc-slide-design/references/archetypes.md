# 장표 유형 카탈로그

모든 유형은 `Deck` 메서드이며 사용 예는 `examples/showcase.py`에 한 번씩 들어 있다. 공통: `section`은 좌상단 태그, 제목은 주장 문장(`==강조==`, `**굵게**` 사용 가능), `source`는 작은 회색 캡션, `callout`은 하단 결론 바.

| # | 메서드 | 쓰임 | 핵심 인자 | 레퍼런스 |
|---|---|---|---|---|
| 1 | `cover(title, subtitle, team)` | 표지. 좌 텍스트 / 우 키비주얼 자리 | | 아르르 p1 |
| 2 | `exec_summary(rows, imc=(콘셉트, [(프로그램, 설명)…]))` | 문제→원인→정의→해결→IMC를 한 장에 | rows=[(라벨, 한 문장)] | 아르르 p2 |
| 3 | `index(groups)` | 목차(대분류 + 소분류 칩) | groups=[(대분류, [소분류])] | 아르르 |
| 4 | `approach(pill, statement, steps)` | 과제 재정의 + 접근 3단계 | | 아르르 p4 |
| 5 | `bars_and_notes(…, bars, bar_title, right_title, notes, focus)` | 좌 가로막대(핵심 1개 진하게) / 우 해석 불릿 | bars=[(라벨, 값)] | 에너지플러스 |
| 6 | `flow_with_dropoff(steps, dashed, drops)` | 여정 셰브론 + 이탈 구간 점선 + 빨간 분수 | drops=[(구간idx, 수치, 설명)] | 에너지플러스 p7 |
| 7 | `quotes_with_stat(stat_big, stat_label, stat_sub, quotes)` | 큰 수치 원 + 인터뷰 말풍선 | quotes=[(문장, 출처)] | 에너지플러스 p8–9 |
| 8 | `compare_table(rows, col_w, focus_col, align)` | 비교·판정·KPI 표. 남는 높이를 자동 분배 | rows[0]=헤더 | 양쪽 |
| 9 | `pain_solution(rows)` | Pain-Point → Solution 행 매칭 | rows=[(pain, solution)] | 아르르 |
| 10 | `dark_barriers(start, end, barriers)` | 다크 배경, 시작→끝 사이 장벽 3개 | | 에너지플러스 |
| 11 | `two_paths(top_label, top_steps, bottom_label, bottom_steps, note)` | As-Is / To-Be 두 줄 프로세스 | | 아르르 p17 |
| 12 | `big_idea(name, tagline, chips)` | 빅 아이디어 공개(다크, 큰 타이틀) | chips=프로그램 이름 | 양쪽 |
| 13 | `imc_matrix(groups, journey)` | 프로그램 × 채널·타깃·목적 + 여정 점 | groups=[{name, items:[{name, channel, target, goal, stages}]}] | 아르르 p19 |
| 14 | `program(kicker, name, subtitle, slogan, blocks, visual_label, effect)` | 프로그램 상세(다크). 우측 시안 자리 | blocks=[(소제목, [불릿])] | 아르르 Marrrket |
| 15 | `hub(center, nodes, goal)` | 콘셉트 중심 + 채널 노드 → 목표 | nodes=[(채널, 역할)] | 에너지플러스 |
| 16 | `journey_table(stages, rows)` | 고객 여정 표 (말·접점·행동·측정) | rows=[(행 이름, [단계별 셀])] | 아르르 |
| 17 | `roadmap(phases)` | 기간별 실행 + 통과 기준 | phases=[(기간, 이름, [할 일], 통과기준)] | 양쪽 |
| 18 | `budget(items, total_label, notes)` | 네이티브 도넛 + 항목 리스트 | items=[(항목, 비중%, 금액)] | 아르르 |
| 19 | `appendix(title, sections)` | 출처·한계·AI 활용 (작은 글씨 허용) | | |

## 기본 부품 (유형에 없는 장표를 만들 때)

`slide(mode, section, number)` → `title()` → `pill()` → `text()` / `rect()` / `shape_text()` / `line()` / `dot()` → `source()` → `callout()`.
특수: `hbar`(막대), `chevrons`(여정 셰브론), `table`, `bubble`(말풍선), `avatar`, `kpi_circle`, `num_circle`, `image`/`phone`(플레이스홀더).

- 좌표 단위 inch, 좌우 여백 0.6, 콘텐츠 하단 한계 = `SLIDE_H − 1.25`(결론 바가 있으면).
- 모든 `text()`는 린트에 등록된다. 직접 만든 텍스트에도 `name=`을 주면 경고 메시지에서 위치를 찾기 쉽다.

## 유형 선택 가이드

| 장표가 하려는 말 | 유형 |
|---|---|
| "이 수치가 격차를 보여준다" | `bars_and_notes` |
| "고객이 여기서 이탈한다" | `flow_with_dropoff` |
| "고객이 실제로 이렇게 말했다" | `quotes_with_stat` |
| "가설을 이렇게 판정했다" | `compare_table` |
| "문제 → 방향을 짝지으면" | `pain_solution` |
| "기존 방식 vs 우리 방식" | `two_paths` |
| "우리의 콘셉트는" | `big_idea` |
| "프로그램이 어떻게 연결되나" | `imc_matrix` → `hub` → `journey_table` |
| "이 프로그램은 이렇게 생겼다" | `program` (프로그램마다 1장, 같은 템플릿) |
| "언제 무엇을, 얼마로, 어떻게 증명" | `roadmap` / `budget` / `compare_table`(KPI) |

## 새 유형 추가 규칙

1. 같은 레이아웃을 두 번 이상 쓰게 되면 `imc_deck.py`에 메서드로 추가한다.
2. 하드코딩 좌표 대신 `MARGIN_X`, `SLIDE_W/H`, 토큰 색을 쓴다.
3. 크기는 `design-system.md` 타입 스케일에서만 고른다.
4. `examples/showcase.py`에 한 장 추가하고 `render.sh`로 확인한 뒤 이 표에 한 줄 추가한다.
