#!/usr/bin/env bash
# pptx -> pdf -> png 미리보기 + 컨택트시트
# 사용: render.sh deck.pptx [out_dir] [dpi]
set -euo pipefail
PPTX="$1"
OUT="${2:-$(dirname "$PPTX")/render}"
DPI="${3:-60}"
mkdir -p "$OUT"
# Pretendard 가 없으면 설치 (미리보기 렌더링 정확도용)
if ! fc-list | grep -qi pretendard; then
  mkdir -p ~/.fonts
  for w in Regular Medium SemiBold Bold; do
    curl -sSfL -o ~/.fonts/Pretendard-$w.otf \
      "https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/public/static/Pretendard-$w.otf" || true
  done
  fc-cache -f >/dev/null
fi
PDF="$OUT/$(basename "${PPTX%.*}").pdf"
HERE="$(cd "$(dirname "$0")" && pwd)"
# 한글-영문/숫자 자동 간격(Asian autospace)을 끈 채 변환 → PowerPoint와 같은 폭 (출처: careermizing-ir-deck)
if ! timeout 180 python3 "$HERE/pptx2pdf.py" "$PPTX" "$PDF" 2>/dev/null; then
  echo "[warn] UNO 변환 실패 → 기본 변환(자동 간격 포함)" >&2
  soffice --headless --convert-to pdf --outdir "$OUT" "$PPTX" >/dev/null 2>&1
fi
rm -f "$OUT"/p-*.png
pdftoppm -png -r "$DPI" "$PDF" "$OUT/p"
python3 - "$OUT" <<'EOF'
import sys, glob
from PIL import Image
out = sys.argv[1]
files = sorted(glob.glob(f"{out}/p-*.png"))
if files:
    ims = [Image.open(f) for f in files]
    w, h = ims[0].size
    cols = 3
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(f"{out}/contact.png")
    print(f"{len(ims)} pages -> {out}/contact.png")
EOF
echo "PDF: $PDF"
