# 커리어마이징 콘텐츠 에이전트 스킬셋

| 스킬 | 역할 |
|---|---|
| `careermizing-content/` | 인스타그램 캐러셀 기획 → 카피 → 디자인 스펙(JSON) → HTML/PNG 미리보기 → 캡션 → QA. 레퍼런스(디자인 시스템·컴포넌트·카피 톤·유형별 플레이북·캡션·QA)와 렌더러 포함 |
| `careermizing-content-review/` | 초안(카피·JSON·PNG·Figma) 검수. 운영 기준으로 P별 수정 지시 |

출처: Figma 「26 하반기 인스타그램 콘텐츠」(프로모션 / 정기 취준 정보 / 기업별 / 기능 홍보 페이지) + Notion 콘텐츠 운영 문서(캡션 가이드, SOP, 브랜딩 방향성, SPEC). 2026-11 기준.

빠른 시작:
```bash
python3 .claude/skills/careermizing-content/scripts/render_carousel.py \
  .claude/skills/careermizing-content/assets/example-spec.json /tmp/preview
node .claude/skills/careermizing-content/scripts/snap.js /tmp/preview
```
