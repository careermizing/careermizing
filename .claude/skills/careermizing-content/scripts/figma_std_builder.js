// std 스펙(JSON) → Figma 섹션 빌더 (v2). use_figma 의 code 로 넘긴다.
// make_figma_code.py 가 __SPEC__ / __CFG__ 를 채워 완성된 스크립트를 만든다.
//
// CFG = {
//   pageId, sectionName, prefix, x, y,          섹션 위치(겹치면 오른쪽으로 자동 이동)
//   brandAssetId,   라이트 장 좌상단 브랜드 에셋(그룹) 원본
//   darkLogoId,     다크 장 로고 인스턴스 원본
//   coverCloneId,   std_cover 가 복제할 원본 표지 프레임(사진·딤·로고 유지, 텍스트만 교체)
//   serviceCloneId  std_service 가 통째로 복제할 서비스 장 원본(선택)
// }
// 슬라이드 type: std_cover | std_typo_cover | std_stack | std_cta | std_service
// 블록 kind: pairs cards flow bar gray table xlist compare panel worksheet chat calendar clone text
// 인라인 마크업: {{포인트색}} **굵게** ==형광펜(결론은 노란 밑칠, 본문은 굵게)== [[보통 굵기]] ~~취소선~~ __밑줄(포인트색)__
const SPEC = __SPEC__;
const CFG = __CFG__;

const FAM = "Noto Sans KR";
await Promise.all(["Regular", "Medium", "Bold", "Black"].map(s => figma.loadFontAsync({ family: FAM, style: s })));
const page = await figma.getNodeByIdAsync(CFG.pageId);
await figma.setCurrentPageAsync(page);

const hex = h => { h = h.replace("#", ""); return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 }; };
const solid = (h, o) => [{ type: "SOLID", color: hex(h), opacity: o === undefined ? 1 : o }];
const A = SPEC.accent || "#2F5CE0";
const INK = "#141A26", INK2 = "#091229", GRAY = "#5B6475", GRAY2 = "#61708C", LINE = "#E3E8F0", NAVY = "#081327";

// ---------- 텍스트 ----------
const TOK = /\{\{([\s\S]+?)\}\}|\*\*([\s\S]+?)\*\*|==([\s\S]+?)==|\[\[([\s\S]+?)\]\]|~~([\s\S]+?)~~|__([\s\S]+?)__/g;
function parse(src) {
  const runs = []; let last = 0, m; src = String(src || ""); TOK.lastIndex = 0;
  while ((m = TOK.exec(src))) {
    if (m.index > last) runs.push({ t: src.slice(last, m.index) });
    if (m[1] !== undefined) runs.push({ t: m[1], accent: true });
    else if (m[2] !== undefined) runs.push({ t: m[2], bold: true });
    else if (m[3] !== undefined) runs.push({ t: m[3], hl: true });
    else if (m[4] !== undefined) runs.push({ t: m[4], regular: true });
    else if (m[5] !== undefined) runs.push({ t: m[5], strike: true });
    else if (m[6] !== undefined) runs.push({ t: m[6], under: true });
    last = TOK.lastIndex;
  }
  if (last < src.length) runs.push({ t: src.slice(last) });
  return runs;
}
function txt(src, o) {
  const runs = parse(src);
  const t = figma.createText();
  t.fontName = { family: FAM, style: o.w || "Medium" };
  t.characters = runs.map(r => r.t).join("") || " ";
  t.fontSize = o.size;
  t.lineHeight = o.lh ? { unit: "PIXELS", value: o.lh } : { unit: "PERCENT", value: 140 };
  t.letterSpacing = { unit: "PIXELS", value: o.ls === undefined ? 0.32 : o.ls };
  t.fills = solid(o.color || INK, o.opacity);
  t.textAlignHorizontal = o.align || "LEFT";
  let i = 0;
  for (const r of runs) {
    const j = i + r.t.length;
    if (j > i) {
      if (r.accent || r.under) { t.setRangeFills(i, j, solid(o.accentColor || A)); t.setRangeFontName(i, j, { family: FAM, style: "Bold" }); }
      if (r.under) t.setRangeTextDecoration(i, j, "UNDERLINE");
      if (r.bold || r.hl) t.setRangeFontName(i, j, { family: FAM, style: o.strongW || "Bold" });
      if (r.regular) t.setRangeFontName(i, j, { family: FAM, style: "Regular" });
      if (r.strike) t.setRangeTextDecoration(i, j, "STRIKETHROUGH");
    }
    i = j;
  }
  if (o.width) { t.resize(o.width, t.height); t.textAutoResize = "HEIGHT"; } else t.textAutoResize = "WIDTH_AND_HEIGHT";
  return t;
}
function put(p, n, x, y) { p.appendChild(n); n.x = x; n.y = y; return n; }
function fillW(n) { n.layoutSizingHorizontal = "FILL"; if (n.type === "TEXT") n.textAutoResize = "HEIGHT"; return n; }
function al(dir, o) {
  const f = figma.createAutoLayout(dir, { itemSpacing: o.gap || 0 });
  f.fills = o.fill ? solid(o.fill, o.fillOpacity) : [];
  if (o.pad) { const [t, r, b, l] = o.pad; f.paddingTop = t; f.paddingRight = r; f.paddingBottom = b; f.paddingLeft = l; }
  if (o.radius) f.cornerRadius = o.radius;
  if (o.stroke) { f.strokes = solid(o.stroke); f.strokeWeight = o.sw || 1; f.strokeAlign = "INSIDE"; }
  if (o.name) f.name = o.name;
  if (o.center) f.counterAxisAlignItems = "CENTER";
  return f;
}
function add(p, c, fill) { p.appendChild(c); if (fill) fillW(c); return c; }
function topLine(f, color, w) { f.strokes = solid(color); f.strokeAlign = "INSIDE"; f.strokeTopWeight = w; f.strokeRightWeight = 0; f.strokeLeftWeight = 0; f.strokeBottomWeight = 0; }
function fixW(n, w) { if (n.type === "TEXT") n.textAutoResize = "HEIGHT"; n.resize(w, n.height); return n; }

// 결론 줄: == 구간은 노란 하단 형광펜 프레임
function hlLines(src, o) {
  o = o || {};
  const box = al("VERTICAL", { gap: 0, name: "결론" }); box.counterAxisAlignItems = "CENTER";
  for (const line of String(src).split("\n")) {
    const row = al("HORIZONTAL", { gap: 0 }); row.counterAxisAlignItems = "CENTER";
    for (const r of parse(line)) {
      const t = txt(r.t, { size: o.size || 36, lh: o.lh || 55.8, w: r.regular ? "Regular" : "Bold", color: r.accent ? A : (o.color || INK), align: "CENTER" });
      if (r.hl) {
        const h = al("HORIZONTAL", { pad: [0, 3, 0, 3], name: "형광펜" }); const Y = { r: 1, g: 0.94, b: 0.63 };
        h.fills = [{ type: "GRADIENT_LINEAR", gradientTransform: [[0, 1, 0], [-1, 0, 1]], gradientStops: [
          { position: 0, color: { ...Y, a: 0 } }, { position: 0.27, color: { ...Y, a: 0 } }, { position: 0.2701, color: { ...Y, a: 1 } }, { position: 1, color: { ...Y, a: 1 } }] }];
        h.appendChild(t); row.appendChild(h);
      } else row.appendChild(t);
    }
    box.appendChild(row);
  }
  return box;
}

// ---------- 블록 ----------
const svgTri = '<svg width="28" height="18" viewBox="0 0 28 18" xmlns="http://www.w3.org/2000/svg"><path d="M0 0H28L14 18Z" fill="#C9D6F2"/></svg>';
async function block(b) {
  const k = b.kind;
  if (k === "clone") {   // 파일 안 짤·사진 재사용
    const c = (await figma.getNodeByIdAsync(b.id)).clone();
    if (b.w && b.h && "resize" in c) c.resize(b.w, b.h);
    if ("cornerRadius" in c) c.cornerRadius = b.radius === undefined ? 28 : b.radius;
    c.name = b.name || "짤";
    return c;
  }
  if (k === "pairs") {
    const wrap = al("VERTICAL", { gap: 30, name: "질문 쌍" });
    for (const p of b.items) {
      const pair = add(wrap, al("VERTICAL", { gap: 6, name: "pair" }), true); pair.counterAxisAlignItems = "CENTER";
      if (p.tag) add(pair, txt(p.tag, { size: 24, w: "Bold", color: GRAY }), true);
      const g = add(pair, al("VERTICAL", { gap: 6, pad: [16, 28, 18, 28], fill: "#F7F8FA", stroke: "#E3E6EC", sw: 1.7, radius: 24, name: "일반" }), true);
      add(g, txt(p.gray_label || "일반 GPT", { size: 21, w: "Bold", color: "#99A1B0" }), true);
      add(g, txt(p.gray, { size: 27, w: "Medium", color: GRAY, lh: 39 }), true);
      add(pair, txt("▼", { size: 20, color: "#C9D6F2", align: "CENTER" }));
      const c = add(pair, al("VERTICAL", { gap: 6, pad: [16, 28, 18, 28], fill: "#F3F7FE", stroke: A, sw: 2, radius: 24, name: "강조" }), true);
      add(c, txt(p.blue_label || "커리어마이징", { size: 21, w: "Bold", color: A }), true);
      add(c, txt(p.blue, { size: 30, w: "Bold", color: INK2, lh: 43.5 }), true);
    }
    return wrap;
  }
  if (k === "cards") {
    const wrap = al("VERTICAL", { gap: b.connect === false ? 20 : 6, name: "번호 카드" }); wrap.counterAxisAlignItems = "CENTER";
    b.items.forEach((c, j) => {
      if (j && b.connect !== false) { const tri = figma.createNodeFromSvg(svgTri); tri.name = "삼각형"; wrap.appendChild(tri); }
      const card = add(wrap, al("HORIZONTAL", { gap: 30, pad: [28, 43, 28, 43], fill: "#FFFFFF", stroke: c.on ? A : LINE, sw: 3, radius: 32, center: true, name: "card" }), true);
      card.minHeight = b.min_height || 176;
      const num = c.num === undefined ? String(j + 1).padStart(2, "0") : c.num;
      if (num) fixW(add(card, txt(num, { size: 48, w: "Bold", color: A })), 64);
      const col = add(card, al("VERTICAL", { gap: 10 }), true);
      add(col, txt(c.title, { size: 36, w: "Bold", lh: 48.6 }), true);
      if (c.desc) add(col, txt(c.desc, { size: 28, w: "Medium", color: GRAY, lh: 40.6 }), true);
    });
    return wrap;
  }
  if (k === "flow") {
    const wrap = al("VERTICAL", { gap: 10, name: "순서" }); wrap.counterAxisAlignItems = "CENTER";
    b.items.forEach((x, j) => {
      if (j) add(wrap, txt("↓", { size: 28, color: A, align: "CENTER" }));
      const bx = add(wrap, al("VERTICAL", { gap: 10, pad: [28, 30, 30, 30], stroke: x.on ? A : "#CCDBFF", sw: x.on ? 2 : 1, radius: 20, name: "box" }), true);
      bx.counterAxisAlignItems = "CENTER";
      add(bx, txt(x.title, { size: 32, w: "Black", color: INK2, align: "CENTER" }), true);
      if (x.example) add(bx, txt(x.example, { size: 26, w: "Medium", color: GRAY2, align: "CENTER" }), true);
    });
    return wrap;
  }
  if (k === "bar") {
    const wrap = al("VERTICAL", { gap: 28, pad: [0, 0, 0, 40], name: "답변" });
    wrap.strokes = solid(A); wrap.strokeAlign = "INSIDE"; wrap.strokeTopWeight = 0; wrap.strokeRightWeight = 0; wrap.strokeBottomWeight = 0; wrap.strokeLeftWeight = 10;
    for (const p of b.paragraphs) add(wrap, txt(p, { size: b.size || 36, w: "Medium", lh: (b.size || 36) * 1.7 }), true);
    return wrap;
  }
  if (k === "gray") {
    const g = al("VERTICAL", { gap: 4, pad: [24, 32, 28, 32], fill: "#F2F4F8", radius: 28, name: "보조 카드" });
    add(g, txt(b.label, { size: 25, w: "Bold", lh: 38.8, color: b.labelColor || INK }), true);
    add(g, txt(b.text, b.strong ? { size: 32, w: "Bold", lh: 50 } : { size: 30, w: "Regular", color: GRAY, lh: 46.5 }), true);
    return g;
  }
  if (k === "table") {
    const tb = al("VERTICAL", { gap: 0, stroke: LINE, sw: 3, radius: 36, pad: [0, 0, 10, 0], name: "표" }); tb.clipsContent = true;
    const hd = add(tb, al("HORIZONTAL", { gap: 40, pad: [24, 43, 14, 43] }), true);
    hd.strokes = solid(INK); hd.strokeAlign = "INSIDE"; hd.strokeTopWeight = 0; hd.strokeRightWeight = 0; hd.strokeLeftWeight = 0; hd.strokeBottomWeight = 3;
    fixW(add(hd, txt(b.columns[0], { size: 26, w: "Bold", color: GRAY })), b.left_width || 250);
    add(hd, txt(b.columns[1], { size: 26, w: "Bold", color: GRAY }), true);
    b.rows.forEach((r, j) => {
      const vp = b.compact ? 16 : 26;
      const row = add(tb, al("HORIZONTAL", { gap: 40, pad: [vp, 43, vp, 43], center: true }), true);
      row.minHeight = b.row_height || 170; if (j) topLine(row, LINE, 3);
      fixW(add(row, txt(r.left, { size: b.left_size || 34, w: "Bold", lh: 47.6 })), b.left_width || 250);
      add(row, txt(r.right, { size: b.right_size || 37, w: "Bold", lh: (b.right_size || 37) * 1.5, color: r.on ? A : INK }), true);
    });
    return tb;
  }
  if (k === "xlist") {
    const wrap = al("VERTICAL", { gap: 0, name: b.ok ? "할 일" : "하지 말 것" });
    if (b.title) add(wrap, txt(b.title, { size: 30, w: "Black", color: INK2, lh: 48 }), true);
    b.rows.forEach((r, j) => {
      const ok = r.ok || b.ok;
      const row = add(wrap, al("HORIZONTAL", { gap: 22, pad: [18, 0, 18, 0], center: true }), true);
      if (j || b.title) topLine(row, "#C7D8FF", 2);
      fixW(add(row, txt(ok ? "✓" : "×", { size: 36, w: "Black", color: ok ? A : "#E02F32" })), 46);
      add(row, txt(r.text, { size: 30, w: "Medium", color: INK2, lh: 44 }), true);
    });
    return wrap;
  }
  if (k === "compare") {
    const wrap = al("HORIZONTAL", { gap: 24, name: "BEFORE AFTER" });
    for (const [p, kind] of [[b.before, "before"], [b.after, "after"]]) {
      const isA = kind === "after";
      const pn = add(wrap, al("VERTICAL", { gap: 22, pad: [34, 32, 34, 32], fill: isA ? "#F3F7FE" : "#F7F8FA", stroke: isA ? "#C7D8FF" : "#E3E6EC", sw: 1.7, radius: 24, name: kind }));
      pn.layoutGrow = 1;
      add(pn, txt(p.label, { size: 26, w: "Bold", color: isA ? A : (b.before_color || "#C00003") }), true);
      add(pn, txt(p.quote, isA ? { size: 31, w: "Bold", color: "#000000", lh: 46.5 } : { size: 31, w: "Medium", color: GRAY, lh: 46.5 }), true);
      if ((p.rows || []).length) {
        const rows = add(pn, al("VERTICAL", { gap: 8, pad: [22, 0, 0, 0] }), true); topLine(rows, isA ? "#C7D8FF" : "#D6DAE2", 2);
        for (const r of p.rows) {
          const rw = add(rows, al("HORIZONTAL", { gap: 0 }), true);
          fixW(add(rw, txt(r.label, { size: 27, w: "Bold", color: isA ? A : "#99A1B0" })), b.label_width || 100);
          add(rw, txt(r.strike ? "~~" + r.value + "~~" : r.value, { size: 27, w: "Medium", color: isA ? INK : "#99A1B0" }), true);
        }
      }
    }
    return wrap;
  }
  if (k === "panel") {
    const pn = al("VERTICAL", { gap: 22, pad: [32, 32, 36, 32], fill: "#F3F7FE", stroke: "#C7D8FF", sw: 1.7, radius: 24, name: "패널" });
    if (b.title) add(pn, txt(b.title, { size: 26, w: "Black", color: A }), true);
    for (const r of b.rows) {
      const row = add(pn, al("HORIZONTAL", { gap: 26, center: true }), true);
      const pill = add(row, al("HORIZONTAL", { fill: "#FFFFFF", stroke: A, sw: 1, radius: 20, center: true })); pill.primaryAxisAlignItems = "CENTER";
      add(pill, txt(r.tag, { size: 18, w: "Bold", color: A })); pill.resize(b.tag_width || 79, 38); pill.layoutSizingHorizontal = "FIXED"; pill.layoutSizingVertical = "FIXED";
      add(row, txt(r.text, { size: 27, w: "Bold", color: INK2, lh: 37.8 }), true);
    }
    return pn;
  }
  if (k === "worksheet") {
    const wrap = al("VERTICAL", { gap: 20, name: "메모" });
    for (const it of b.items) {
      const c = add(wrap, al("VERTICAL", { gap: 4, pad: [26, 43, 28, 43], stroke: LINE, sw: 3, radius: 32 }), true);
      add(c, txt(it.label, { size: 28, w: "Bold", color: A, lh: 43.4 }), true);
      add(c, txt(it.sentence, { size: 34, w: "Bold", color: "#0E1530", lh: 52 }), true);
      if (it.example) add(c, txt(it.example, { size: 27, w: "Medium", color: GRAY, lh: 41.9 }), true);
    }
    return wrap;
  }
  if (k === "chat") {   // 면접관 ↔ 지원자
    const wrap = al("VERTICAL", { gap: 16, name: "대화" }); wrap.counterAxisAlignItems = "CENTER";
    b.turns.forEach((tn, j) => {
      const isI = tn.who === "interviewer";
      const bub = add(wrap, al("VERTICAL", { gap: 6, pad: [20, 34, 22, 34], fill: isI ? "#FFFFFF" : "#F3F7FE", stroke: isI ? A : "#C7D8FF", sw: isI ? 3 : 1.7, radius: 28, name: isI ? "면접관" : "지원자" }), true);
      add(bub, txt(isI ? "면접관" : "지원자", { size: 22, w: "Bold", color: isI ? A : "#8A93A3" }), true);
      add(bub, txt(tn.text, { size: 31, w: isI ? "Bold" : "Medium", color: INK, lh: 46 }), true);
    });
    return wrap;
  }
  if (k === "calendar") {   // 3주 달력. marks: {"1":{"label":"면접","style":"dark"}, "2":{"label":"복기"}}
    const weeks = b.weeks || 3, cw = b.cell_w || 128, ch = b.cell_h || (b.compact ? 92 : 112);
    const wrap = al("VERTICAL", { gap: 10, name: "달력" });
    for (let w = 0; w < weeks; w++) {
      if (b.week_labels) add(wrap, txt(b.week_labels[w], { size: 22, w: "Bold", color: b.dark ? "#9FB2DB" : GRAY }), true);
      const row = add(wrap, al("HORIZONTAL", { gap: 6 }), false);
      for (let d = 1; d <= 7; d++) {
        const n = w * 7 + d; const mk = (b.marks || {})[String(n)];
        const dark = mk && mk.style === "dark", on = !!mk;
        const cell = add(row, al("VERTICAL", { gap: 2, pad: [12, 10, 10, 10], radius: 16,
          fill: dark ? INK : on ? A : (b.dark ? "#16213D" : "#F4F6FA"), name: "day " + n }));
        cell.resize(cw, ch); cell.layoutSizingHorizontal = "FIXED"; cell.layoutSizingVertical = "FIXED"; cell.counterAxisAlignItems = "CENTER";
        add(cell, txt(String(n), { size: b.compact ? 24 : 28, w: "Bold", color: on ? "#FFFFFF" : (b.dark ? "#5E6C8F" : "#9AA4B3"), align: "CENTER" }));
        if (mk && mk.label) add(cell, txt(mk.label, { size: b.compact ? 16 : 19, w: "Bold", color: "#FFFFFF", align: "CENTER", lh: 24 }));
      }
    }
    return wrap;
  }
  if (k === "text") return txt(b.text, { size: b.size || 32, w: b.w || "Medium", lh: (b.size || 32) * 1.6, color: b.color || INK, align: b.align || "LEFT" });
  return txt("[unknown block " + k + "]", { size: 30 });
}

// BEFORE/AFTER 두 패널은 본문(936px)에 붙인 뒤 같은 높이(최소 480)로 맞춘다.
function equalizeCompare(body) {
  for (const wrap of body.children.filter(c => c.name === "BEFORE AFTER")) {
    for (const p of wrap.children) { p.layoutSizingVertical = "HUG"; for (const c of p.children) if ("layoutGrow" in c) c.layoutGrow = 0; }
    const h = Math.max(SPEC.compare_min || 420, ...wrap.children.map(p => p.height));
    for (const p of wrap.children) { p.layoutSizingVertical = "FIXED"; p.resize(p.width, h); if (p.children[1]) p.children[1].layoutGrow = 1; }
  }
}
async function body(frame, blocks, y, gap) {
  const bd = al("VERTICAL", { gap: gap || 30, name: "본문" }); bd.counterAxisAlignItems = "CENTER";
  frame.appendChild(bd); bd.x = 72; bd.y = y;
  bd.resize(936, 10); bd.layoutSizingHorizontal = "FIXED"; bd.primaryAxisSizingMode = "AUTO"; bd.clipsContent = false;
  for (const b of blocks) { const n = await block(b); bd.appendChild(n); if (b.kind !== "clone" && b.kind !== "calendar") fillW(n); }
  equalizeCompare(bd);
  return bd;
}

// ---------- 섹션 ----------
const n = SPEC.slides.length; let X = CFG.x; const W = 100 + n * 1180, H = 1550;
for (let g = 0; g < 20; g++) { const hit = page.children.find(c => c.x < X + W && c.x + c.width > X && c.y < CFG.y + H && c.y + c.height > CFG.y); if (!hit) break; X = hit.x + hit.width + 200; }
const sec = figma.createSection(); sec.name = CFG.sectionName; sec.x = X; sec.y = CFG.y; sec.resizeWithoutConstraints(W, H);
const brand = CFG.brandAssetId ? await figma.getNodeByIdAsync(CFG.brandAssetId) : null;
const report = [];

for (let i = 0; i < n; i++) {
  const s = SPEC.slides[i]; let frame;
  const pg = `${String(i + 1).padStart(2, "0")} / ${String(n).padStart(2, "0")}`;
  if (s.type === "std_cover") {
    let src = await figma.getNodeByIdAsync(s.clone || CFG.coverCloneId);
    if (src.type !== "FRAME") src = src.parent;   // 사진 레이어 id 를 넘겨도 그 표지 프레임을 복제
    frame = src.clone(); sec.appendChild(frame);
    for (const c of [...frame.children]) if (c.type === "TEXT" && !/출처/.test(c.characters)) c.remove();
    if (!frame.children.some(c => c.type === "INSTANCE") && CFG.darkLogoId) { const lg = (await figma.getNodeByIdAsync(CFG.darkLogoId)).clone(); put(frame, lg, 65, 90); }
    const subT = s.sub ? txt(s.sub, { size: 44, w: "Bold", lh: 61.6, color: "#FFFFFF", opacity: 0.95, width: 940 }) : null;
    const hT = txt(s.headline, { size: 100, w: "Black", lh: 115, ls: -3, color: "#FFFFFF", width: 940 });
    const base = subT ? 1142 : 1200;
    if (subT) put(frame, subT, 72, base);
    const hY = (subT ? base - 36 : base) - hT.height; put(frame, hT, 72, hY);
    if (s.top) { const tp = txt(s.top, { size: 38, w: "Bold", color: "#FFFFFF", opacity: 0.95, width: 940 }); put(frame, tp, 72, hY - 18 - tp.height); tp.name = "표지 윗줄"; }
    if (s.source && !frame.children.some(c => c.type === "TEXT" && /출처/.test(c.characters))) put(frame, txt(s.source, { size: 16, w: "Regular", color: "#B7B7B7" }), 900, 1300);
    hT.name = "표지 헤드라인";
  } else if (s.type === "std_typo_cover") {
    frame = figma.createFrame(); sec.appendChild(frame); frame.resize(1080, 1350);
    frame.fills = [{ type: "GRADIENT_LINEAR", gradientTransform: [[0.6, 0.8, -0.2], [-0.8, 0.6, 0.6]], gradientStops: [{ position: 0, color: { ...hex("#16285A"), a: 1 } }, { position: 1, color: { ...hex("#050A18"), a: 1 } }] }];
    if (CFG.darkLogoId) { const lg = (await figma.getNodeByIdAsync(CFG.darkLogoId)).clone(); put(frame, lg, 65, 90); }
    let y = s.top_y || 230;
    if (s.eyebrow) { const e = put(frame, txt(s.eyebrow, { size: 36, w: "Bold", color: "#9FB2DB", width: 936 }), 72, y); y += e.height + 18; }
    const h = put(frame, txt(s.headline, { size: s.size || 88, w: "Black", lh: (s.size || 88) * 1.18, ls: -2.5, color: "#FFFFFF", width: 940, accentColor: "#73ABFF" }), 72, y); y += h.height + 44;
    h.name = "표지 헤드라인";
    if (s.card) {
      const card = al("VERTICAL", { gap: 18, pad: [40, 44, 42, 44], fill: "#FFFFFF", radius: 32, name: "표지 카드" });
      frame.appendChild(card); card.x = 72; card.y = y; card.resize(936, 10); card.layoutSizingHorizontal = "FIXED"; card.primaryAxisSizingMode = "AUTO";
      if (s.card.label) add(card, txt(s.card.label, { size: 24, w: "Bold", color: "#8A93A3" }), true);
      for (const b of s.card.blocks || []) { const nb = await block(b); card.appendChild(nb); if (b.kind !== "calendar") fillW(nb); }
      if (s.card.text) add(card, txt(s.card.text, { size: 33, w: "Medium", lh: 58 }), true);
      y += card.height + 30;
    }
    if (s.hint) { put(frame, txt(s.hint, { size: 28, w: "Bold", color: "#9FB2DB" }), 72, y + 10).name = "표지 힌트"; y += 60; }
    if (s.sub) put(frame, txt(s.sub, { size: 32, w: "Medium", color: "#C2D1E8", width: 936 }), 72, Math.max(y, 1180));
  } else if (s.type === "std_service" && CFG.serviceCloneId) {
    frame = (await figma.getNodeByIdAsync(CFG.serviceCloneId)).clone(); sec.appendChild(frame);
  } else if (s.type === "std_cta") {
    frame = figma.createFrame(); sec.appendChild(frame); frame.resize(1080, 1350); frame.fills = solid("#071022");
    if (CFG.darkLogoId) { const lg = (await figma.getNodeByIdAsync(CFG.darkLogoId)).clone(); put(frame, lg, 76, 65); }
    put(frame, txt(pg, { size: 22, w: "Medium", color: "#D1E0FC" }), 920, 73);
    let y = s.top || 220;
    const h = put(frame, txt(s.headline, { size: 62, w: "Black", lh: 76.3, color: "#FFFFFF", width: 930 }), 76, y); y += h.height + 28;
    if (s.sub) { const sb = put(frame, txt(s.sub, { size: 29, w: "Medium", color: "#D1E0FC", width: 928 }), 76, y); y += sb.height + 34; }
    const panel = al("VERTICAL", { gap: 0, pad: [10, 34, 10, 34], fill: "#F3F7FE", fillOpacity: 0.95, radius: 23, name: "체크리스트" });
    frame.appendChild(panel); panel.x = 76; panel.y = y; panel.resize(928, 10); panel.layoutSizingHorizontal = "FIXED"; panel.primaryAxisSizingMode = "AUTO";
    s.rows.forEach((r, j) => {
      const row = add(panel, al("HORIZONTAL", { gap: 24, pad: [18, 0, 18, 0] }), true); if (j) topLine(row, "#C7D8FF", 2);
      fixW(add(row, txt(r.num || String(j + 1).padStart(2, "0"), { size: 32, w: "Black", color: A })), 60);
      const col = add(row, al("VERTICAL", { gap: 4 }), true);
      add(col, txt(r.title, { size: 31, w: "Black", color: INK2, lh: 40 }), true);
      if (r.prompt) add(col, txt(r.prompt, { size: 25, w: "Medium", color: GRAY2 }), true);
    });
    if (panel.y + panel.height > 1070) report.push(`P${i + 1} 체크리스트가 길어요 (${Math.round(panel.y + panel.height)})`);
    if (s.product) { put(frame, txt(s.product, { size: 31, w: "Bold", color: "#FFFFFF" }), 76, 1092); if (s.product_sub) put(frame, txt(s.product_sub, { size: 25, w: "Medium", color: "#D1E0FC" }), 76, 1150); }
    if (s.button) {
      const btn = al("HORIZONTAL", { pad: [0, 32, 0, 32], fill: A, fillOpacity: 0.95, radius: 17, center: true, name: "CTA 버튼" });
      frame.appendChild(btn); btn.x = 76; btn.y = 1221; add(btn, txt(s.button, { size: 30, w: "Bold", color: "#FFFFFF" }));
      btn.resize(928, 84); btn.layoutSizingHorizontal = "FIXED"; btn.layoutSizingVertical = "FIXED";
    }
  } else {   // std_stack
    frame = figma.createFrame(); sec.appendChild(frame); frame.resize(1080, 1350); frame.fills = solid("#FFFFFF");
    if (brand) { const bc = brand.clone(); put(frame, bc, 75, 65); }
    let y = 151;
    const h = put(frame, txt(s.headline, { size: 60, w: "Bold", lh: 82.8, align: "CENTER", width: 936 }), 72, y); h.name = "헤드라인"; y += h.height;
    if (s.sub) { const sb = put(frame, txt(s.sub, { size: 30, w: "Regular", lh: 45, color: GRAY, align: "CENTER", width: 936 }), 72, y + 20); sb.name = "서브"; y += 20 + sb.height; }
    const bd = await body(frame, s.blocks || [], y + (s.body_top || 48), s.gap);
    const limit = s.conclusion ? 1110 : (s.disclaimer ? 1262 : 1290);
    // 본문이 짧으면 결론 위 빈칸을 나눠 세로 균형을 잡는다(최대 90px 내림).
    if (s.balance !== false) { const slack = (limit - 15) - bd.y - bd.height; if (slack > 0) bd.y = Math.round(bd.y + Math.min(slack / 2, 90)); }
    if (bd.y + bd.height > limit) report.push(`P${i + 1} 본문 하단 ${Math.round(bd.y + bd.height)} > ${limit}`);
    if (s.conclusion) { const c = hlLines(s.conclusion); frame.appendChild(c); c.x = Math.round((1080 - c.width) / 2); c.y = 1131; }
    if (s.disclaimer) put(frame, txt(s.disclaimer, { size: 19, w: "Medium", color: GRAY2, width: 936 }), 72, 1282).name = "면책";
  }
  frame.name = `${CFG.prefix} · P${String(i + 1).padStart(2, "0")} ${s.role || ""}`.trim();
  frame.x = 100 + i * 1180; frame.y = 100; frame.clipsContent = true;
}
return { sectionId: sec.id, x: sec.x, y: sec.y, frames: sec.children.map(c => ({ id: c.id, name: c.name })), warnings: report };
