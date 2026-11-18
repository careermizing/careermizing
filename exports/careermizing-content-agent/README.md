# 커리어마이징 콘텐츠 에이전트 · 내보내기 (2026-11-18)

| 파일 | 용도 |
|---|---|
| `SYSTEM_PROMPT.md` | 다른 AI의 "지침 / 시스템 프롬프트" 칸에 그대로 붙여넣는 요약본 (ChatGPT GPT 지침 8,000자 안) |
| `CAREERMIZING_CONTENT_AGENT.md` | 전체 규칙 통합본(제작 스킬 + 레퍼런스 12개 + 검수 스킬 + 토큰·예시 스펙). "지식 / Knowledge / 파일"로 업로드 |
| `careermizing-content.skill.zip` | Claude용 원본 스킬 폴더(제작). 렌더러 · Figma 빌더 스크립트 포함 |
| `careermizing-content-review.skill.zip` | Claude용 원본 스킬 폴더(검수) |

## AI별 넣는 법
- **Claude (claude.ai)**: 설정 → 기능 → Skills에서 두 `.skill.zip`을 각각 업로드. 또는 Project 지식에 `CAREERMIZING_CONTENT_AGENT.md`.
- **Claude Code**: zip을 풀어 `.claude/skills/` 아래에 두 폴더를 넣기(이 레포에는 이미 있음).
- **ChatGPT (GPTs / 프로젝트)**: 지침 = `SYSTEM_PROMPT.md` 내용, 지식 = `CAREERMIZING_CONTENT_AGENT.md` 업로드.
- **Gemini (Gem)**: 지침 = `SYSTEM_PROMPT.md`, 파일 = `CAREERMIZING_CONTENT_AGENT.md`.
- **그 외(API 등)**: 시스템 프롬프트에 `SYSTEM_PROMPT.md`, 첫 메시지나 RAG 문서로 통합본.

## 한계
- HTML/PNG 렌더러(`scripts/render_carousel.py`, `snap.js`)와 Figma 빌더(`figma_std_builder.js`)는 코드 실행 + Figma 연결이 있는 환경(Claude Code 등)에서만 동작. 다른 AI에서는 카피 · 스펙 · 디자인 메모까지만 나온다.
- 2026-11 하반기 Figma 원본 노드 ID(예: 짤 906:490)는 이 파일(DaDENGdebavdf360piBGwH)에서만 의미가 있다.
- 규칙을 바꾸면 레포의 `.claude/skills/`를 고치고 이 폴더를 다시 생성한다.
