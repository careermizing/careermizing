#!/usr/bin/env python3
"""
std 스펙 JSON → use_figma 에 넣을 스크립트 문자열을 만든다.

  python3 make_figma_code.py spec.json cfg.json > code.js

cfg.json 예:
{
  "pageId": "119:3255",                 # 대상 페이지
  "sectionName": "[WASH] 20261109 / 면접팁 / ...",
  "prefix": "전공직무 wash",            # 프레임 이름 접두
  "x": 18854, "y": 55499,               # 섹션 위치(원본 오른쪽 등 빈 곳)
  "brandAssetId": "978:1471",           # 라이트 장 좌상단 브랜드 에셋(그룹) 원본
  "darkLogoId": "978:1458",             # 다크 장 로고 인스턴스 원본
  "coverCloneId": "978:1299",           # 표지로 복제할 원본 프레임(사진·딤·로고 유지, 텍스트만 교체)
  "clones": {"1": ["978:1463", "978:1465"]}   # 장 번호(0부터)별로 그대로 복제할 노드(짤·손글씨 그룹 등)
}
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = json.load(open(sys.argv[1], encoding="utf-8"))
cfg = json.load(open(sys.argv[2], encoding="utf-8"))
src = open(os.path.join(HERE, "figma_std_builder.js"), encoding="utf-8").read()
src = "\n".join(l for l in src.split("\n") if not l.lstrip().startswith("//"))  # 주석 제거(용량 절약)
code = src.replace("__SPEC__", json.dumps(spec, ensure_ascii=False)).replace("__CFG__", json.dumps(cfg, ensure_ascii=False))
if len(code) > 50000:
    sys.exit(f"code too long: {len(code)} chars (limit 50000) — 스펙의 caption 등 불필요한 필드를 빼세요")
sys.stdout.write(code)
