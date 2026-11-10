// std 스펙(JSON) → Figma 섹션 빌더. use_figma 의 code 로 넘긴다.
// make_figma_code.py 가 __SPEC__ / __CFG__ 를 채워 완성된 스크립트를 만든다.
// CFG: { pageId, sectionName, x, y, brandAssetId, darkLogoId, coverCloneId, clones: {slideIndex: [nodeId,...]} }
const SPEC = __SPEC__;
const CFG = __CFG__;

const FAM = "Noto Sans KR";
await Promise.all(["Regular", "Medium", "Bold", "Black"].map(s => figma.loadFontAsync({ family: FAM, style: s })));
const page = await figma.getNodeByIdAsync(CFG.pageId);
await figma.setCurrentPageAsync(page);

const hex = h => { h = h.replace("#", ""); return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 }; };
const solid = (h, o) => [{ type: "SOLID", color: hex(h), opacity: o === undefined ? 1 : o }];
const A = SPEC.accent || "#2F5CE0";
const INK = "#141A26", INK2 = "#091229", GRAY = "#5B6475", GRAY2 = "#61708C", LINE = "#E3E8F0";
const created = [];

// ---------- 텍스트 ----------
const TOK = /\{\{([\s\S]+?)\}\}|\*\*([\s\S]+?)\*\*|==([\s\S]+?)==|\[\[([\s\S]+?)\]\]|~~([\s\S]+?)~~/g;
function parse(src) {
  const runs = []; let last = 0; let m;
  src = String(src || "");
  TOK.lastIndex = 0;
  while ((m = TOK.exec(src))) {
    if (m.index > last) runs.push({ t: src.slice(last, m.index) });
    if (m[1] !== undefined) runs.push({ t: m[1], accent: true });
    else if (m[2] !== undefined) runs.push({ t: m[2], bold: true });
    else if (m[3] !== undefined) runs.push({ t: m[3], hl: true });
    else if (m[4] !== undefined) runs.push({ t: m[4], regular: true });
    else if (m[5] !== undefined) runs.push({ t: m[5], strike: true });
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
      if (r.accent) { t.setRangeFills(i, j, solid(A)); if (o.accentBold !== false) t.setRangeFontName(i, j, { family: FAM, style: o.strongW || "Bold" }); }
      if (r.bold || r.hl) t.setRangeFontName(i, j, { family: FAM, style: o.strongW || "Bold" });
      if (r.regular) t.setRangeFontName(i, j, { family: FAM, style: "Regular" });
      if (r.strike) t.setRangeTextDecoration(i, j, "STRIKETHROUGH");
    }
    i = j;
  }
  if (o.width) { t.resize(o.width, t.height); t.textAutoResize = "HEIGHT"; }
  else t.textAutoResize = "WIDTH_AND_HEIGHT";
  return t;
}
function put(parent, node, x, y) { parent.appendChild(node); node.x = x; node.y = y; return node; }
function fillW(node) { node.layoutSizingHorizontal = "FILL"; if (node.type === "TEXT") node.textAutoResize = "HEIGHT"; return node; }
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
function add(parent, child, fill) { parent.appendChild(child); if (fill) fillW(child); return child; }

// 형광펜 줄 (결론): 줄마다 런을 나란히, == 구간은 노란 하단 형광펜 프레임
function hlLines(src, o) {
  const box = al("VERTICAL", { gap: 0, name: "결론" }); box.counterAxisAlignItems = "CENTER";
  for (const line of String(src).split("\n")) {
    const row = al("HORIZONTAL", { gap: 0 }); row.counterAxisAlignItems = "CENTER";
    for (const r of parse(line)) {
      const t = txt(r.t, { size: o.size, lh: o.lh, w: r.regular ? "Regular" : (o.w || "Bold"), color: r.accent ? A : (o.color || INK), align: "CENTER" });
      if (r.hl) {
        const h = al("HORIZONTAL", { pad: [0, 3, 0, 3] });
        h.fills = [{ type: "GRADIENT_LINEAR", gradientTransform: [[0, 1, 0], [-1, 0, 1]], gradientStops: [
          { position: 0, color: { r: 1, g: 0.94, b: 0.63, a: 0 } }, { position: 0.27, color: { r: 1, g: 0.94, b: 0.63, a: 0 } },
          { position: 0.27, color: { r: 1, g: 0.94, b: 0.63, a: 1 } }, { position: 1, color: { r: 1, g: 0.94, b: 0.63, a: 1 } }] }];
        h.appendChild(t); row.appendChild(h);
      } else row.appendChild(t);
    }
    box.appendChild(row);
  }
  return box;
}

// ---------- 블록 ----------
const svgTri = '<svg width="28" height="18" viewBox="0 0 28 18" xmlns="http://www.w3.org/2000/svg"><path d="M0 0H28L14 18Z" fill="#C9D6F2"/></svg>';
function block(b) {
  const k = b.kind;
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
      const card = add(wrap, al("HORIZONTAL", { gap: 30, pad: [30, 43, 30, 43], fill: "#FFFFFF", stroke: c.on ? A : LINE, sw: 3, radius: 32, center: true, name: "card" }), true);
      card.minHeight = b.min_height || 176;
      const num = c.num === undefined ? String(j + 1).padStart(2, "0") : c.num;
      if (num) { const n = add(card, txt(num, { size: 48, w: "Bold", color: A })); n.resize(Math.max(60, n.width), n.height); }
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
      const bx = add(wrap, al("VERTICAL", { gap: 10, pad: [30, 30, 32, 30], stroke: x.on ? A : "#CCDBFF", sw: x.on ? 2 : 1, radius: 20, name: "box" }), true);
      bx.counterAxisAlignItems = "CENTER";
      add(bx, txt(x.title, { size: 32, w: "Black", color: INK2, align: "CENTER" }), true);
      if (x.example) add(bx, txt(x.example, { size: 25, w: "Medium", color: GRAY2, align: "CENTER" }), true);
    });
    return wrap;
  }
  if (k === "bar") {
    const wrap = al("VERTICAL", { gap: 30, pad: [0, 0, 0, 40], name: "답변" });
    wrap.strokes = solid(A); wrap.strokeAlign = "INSIDE";
    wrap.strokeTopWeight = 0; wrap.strokeRightWeight = 0; wrap.strokeBottomWeight = 0; wrap.strokeLeftWeight = 10;
    for (const p of b.paragraphs) add(wrap, txt(p, { size: 36, w: "Medium", lh: 61.2 }), true);
    return wrap;
  }
  if (k === "gray") {
    const g = al("VERTICAL", { gap: 4, pad: [24, 32, 28, 32], fill: "#F2F4F8", radius: 28, name: "보조 카드" });
    add(g, txt(b.label, { size: 25, w: "Bold", lh: 38.8 }), true);
    add(g, txt(b.text, b.strong ? { size: 32, w: "Bold", lh: 52 } : { size: 30, w: "Regular", color: GRAY, lh: 46.5 }), true);
    return g;
  }
  if (k === "table") {
    const tb = al("VERTICAL", { gap: 0, stroke: LINE, sw: 3, radius: 36, pad: [0, 0, 10, 0], name: "표" }); tb.clipsContent = true;
    const hd = add(tb, al("HORIZONTAL", { gap: 40, pad: [24, 43, 14, 43] }), true);
    hd.strokes = solid(INK); hd.strokeAlign = "INSIDE"; hd.strokeTopWeight = 0; hd.strokeRightWeight = 0; hd.strokeLeftWeight = 0; hd.strokeBottomWeight = 3;
    const h1 = add(hd, txt(b.columns[0], { size: 26, w: "Bold", color: GRAY })); h1.resize(250, h1.height); h1.textAutoResize = "HEIGHT";
    add(hd, txt(b.columns[1], { size: 26, w: "Bold", color: GRAY }), true);
    b.rows.forEach((r, j) => {
      const vp = b.compact ? 16 : 26; const row = add(tb, al("HORIZONTAL", { gap: 40, pad: [vp, 43, vp, 43], center: true }), true);
      row.minHeight = b.row_height || 170;
      if (j) { row.strokes = solid(LINE); row.strokeAlign = "INSIDE"; row.strokeTopWeight = 3; row.strokeRightWeight = 0; row.strokeLeftWeight = 0; row.strokeBottomWeight = 0; }
      const c1 = add(row, txt(r.left, { size: 34, w: "Bold", lh: 47.6 })); c1.resize(250, c1.height); c1.textAutoResize = "HEIGHT";
      add(row, txt(r.right, { size: 37, w: "Bold", lh: 55.5, color: r.on ? A : INK }), true);
    });
    return tb;
  }
  if (k === "xlist") {
    const wrap = al("VERTICAL", { gap: 0, name: "하지 말 것" });
    b.rows.forEach((r, j) => {
      const row = add(wrap, al("HORIZONTAL", { gap: 22, pad: [14, 0, 14, 0], center: true }), true);
      if (j) { row.strokes = solid("#C7D8FF"); row.strokeAlign = "INSIDE"; row.strokeTopWeight = 2; row.strokeRightWeight = 0; row.strokeLeftWeight = 0; row.strokeBottomWeight = 0; }
      const x = add(row, txt(r.ok ? "✓" : "×", { size: 38, w: "Black", color: r.ok ? A : "#E02F32" })); x.resize(46, x.height);
      add(row, txt(r.text, { size: 29, w: "Medium", color: INK2 }), true);
    });
    return wrap;
  }
  if (k === "compare") {
    const wrap = al("HORIZONTAL", { gap: 24, name: "BEFORE AFTER" }); wrap.counterAxisAlignItems = "MAX"; wrap.counterAxisAlignItems = "MIN";
    for (const [p, kind] of [[b.before, "before"], [b.after, "after"]]) {
      const isA = kind === "after";
      const pn = add(wrap, al("VERTICAL", { gap: 22, pad: [34, 32, 34, 32], fill: isA ? "#F3F7FE" : "#F7F8FA", stroke: isA ? "#C7D8FF" : "#E3E6EC", sw: 1.7, radius: 24, name: kind }));
      pn.layoutGrow = 1;
      add(pn, txt(p.label, { size: 26, w: "Bold", color: isA ? A : "#C00003" }), true);
      const q = add(pn, txt(p.quote, isA ? { size: 31, w: "Bold", color: "#000000", lh: 46.5 } : { size: 31, w: "Medium", color: GRAY, lh: 46.5 }), true);
      const rows = add(pn, al("VERTICAL", { gap: 8, pad: [22, 0, 0, 0] }), true);
      rows.strokes = solid(isA ? "#C7D8FF" : "#D6DAE2"); rows.strokeAlign = "INSIDE"; rows.strokeTopWeight = 2; rows.strokeRightWeight = 0; rows.strokeLeftWeight = 0; rows.strokeBottomWeight = 0;
      for (const r of p.rows || []) {
        const rw = add(rows, al("HORIZONTAL", { gap: 0 }), true);
        const l = add(rw, txt(r.label, { size: 27, w: "Bold", color: isA ? A : "#99A1B0" })); l.resize(108, l.height);
        const v = add(rw, txt(r.strike ? "~~" + r.value + "~~" : r.value, { size: 27, w: "Medium", color: isA ? INK : "#99A1B0" }), true);
      }
    }
    // 패널 높이 맞추기는 본문(936px)에 붙인 뒤 equalizeCompare()에서 한다.
    // 여기서 맞추면 텍스트 폭이 0인 상태로 재서 패널이 수천 px로 늘어난다.
    return wrap;
  }
  if (k === "panel") {
    const pn = al("VERTICAL", { gap: 22, pad: [32, 32, 36, 32], fill: "#F3F7FE", stroke: "#C7D8FF", sw: 1.7, radius: 24, name: "패널" });
    if (b.title) add(pn, txt(b.title, { size: 26, w: "Black", color: A }), true);
    for (const r of b.rows) {
      const row = add(pn, al("HORIZONTAL", { gap: 26, center: true }), true);
      const pill = add(row, al("HORIZONTAL", { fill: "#FFFFFF", stroke: A, sw: 1, radius: 20, center: true }));
      pill.primaryAxisAlignItems = "CENTER"; pill.resize(79, 38); pill.layoutSizingHorizontal = "FIXED"; pill.layoutSizingVertical = "FIXED";
      add(pill, txt(r.tag, { size: 18, w: "Bold", color: A }));
      add(row, txt(r.text, { size: 27, w: "Bold", color: INK2, lh: 37.8 }), true);
    }
    return pn;
  }
  if (k === "worksheet") {
    const wrap = al("VERTICAL", { gap: 20, name: "빈칸" });
    for (const it of b.items) {
      const c = add(wrap, al("VERTICAL", { gap: 4, pad: [27, 43, 30, 43], stroke: LINE, sw: 3, radius: 32 }), true);
      add(c, txt(it.label, { size: 28, w: "Bold", color: A, lh: 43.4 }), true);
      add(c, txt(it.sentence.replace(/_{3,}/g, "______"), { size: 35, w: "Bold", color: "#0E1530", lh: 54 }), true);
      if (it.example) add(c, txt(it.example, { size: 27, w: "Medium", color: GRAY, lh: 41.9 }), true);
    }
    return wrap;
  }
  if (k === "text") return txt(b.text, { size: 32, w: "Medium", lh: 51 });
  if (k === "image") {
    const ph = figma.createFrame(); ph.name = "이미지 자리 (사진·짤로 교체)"; ph.resize(b.width || 600, b.height || 431);
    ph.cornerRadius = 28; ph.fills = solid("#F2F4F8"); ph.strokes = solid("#C8CFDB"); ph.strokeWeight = 3; ph.dashPattern = [12, 8];
    const t = txt(b.note || "이미지 자리", { size: 24, w: "Medium", color: "#8A93A3", align: "CENTER", width: (b.width || 600) - 60 });
    put(ph, t, 30, ((b.height || 431) - t.height) / 2);
    return ph;
  }
  return txt("[unknown block " + k + "]", { size: 30 });
}

// BEFORE/AFTER 두 패널을 내용 높이 기준(최소 480)으로 같은 높이로 맞춘다. 본문에 붙인 뒤 호출.
function equalizeCompare(body) {
  for (const wrap of body.children.filter(c => c.name === "BEFORE AFTER")) {
    for (const p of wrap.children) { p.layoutSizingVertical = "HUG"; for (const c of p.children) if ("layoutGrow" in c) c.layoutGrow = 0; }
    const h = Math.max(480, ...wrap.children.map(p => p.height));
    for (const p of wrap.children) { p.layoutSizingVertical = "FIXED"; p.resize(p.width, h); if (p.children[1]) p.children[1].layoutGrow = 1; }
  }
}

// ---------- 슬라이드 ----------
async function brandLight(frame) {
  const src = await figma.getNodeByIdAsync(CFG.brandAssetId);
  const c = src.clone(); frame.appendChild(c); c.x = 75; c.y = 65; created.push(c.id);
}
function head(frame, s) {
  let y = 151;
  if (s.headline) {
    const h = txt(s.headline, { size: 60, w: "Bold", lh: 82.8, align: "CENTER", width: 936 });
    put(frame, h, 72, y); h.name = "헤드라인"; y += h.height;
  }
  if (s.sub) {
    const sb = txt(s.sub, { size: 30, w: "Regular", lh: 45, color: GRAY, align: "CENTER", width: 936 });
    put(frame, sb, 72, y + 20); sb.name = "서브"; y += 20 + sb.height;
  }
  return y;
}
function tail(frame, s) {
  if (s.conclusion) {
    const c = hlLines(s.conclusion, { size: 36, lh: 55.8 });
    frame.appendChild(c); c.x = (1080 - c.width) / 2; c.y = 1131;
  }
  if (s.disclaimer) {
    const d = txt(s.disclaimer, { size: 19, w: "Medium", color: GRAY2, width: 936 });
    put(frame, d, 72, 1278); d.name = "면책";
  }
}

const n = SPEC.slides.length;
// 빈 자리 확보: 겹치는 노드가 있으면 오른쪽으로 민다
let X = CFG.x; const W = 100 + n * 1180, H = 1550;
for (let guard = 0; guard < 20; guard++) {
  const hit = page.children.find(c => c.x < X + W && c.x + c.width > X && c.y < CFG.y + H && c.y + c.height > CFG.y);
  if (!hit) break; X = hit.x + hit.width + 200;
}
const sec = figma.createSection();
sec.name = CFG.sectionName;
sec.x = X; sec.y = CFG.y;
sec.resizeWithoutConstraints(100 + n * 1180, 1550);
created.push(sec.id);
const report = [];

for (let i = 0; i < n; i++) {
  const s = SPEC.slides[i];
  const name = `${CFG.prefix} · P${String(i + 1).padStart(2, "0")} ${s.role || ""}`.trim();
  let frame;
  if (s.type === "std_cover") {
    const src = await figma.getNodeByIdAsync(CFG.coverCloneId);
    frame = src.clone(); sec.appendChild(frame);
    for (const c of [...frame.children]) if (c.type === "TEXT" && !/출처/.test(c.characters)) c.remove();
    const subT = s.sub ? txt(s.sub, { size: 44, w: "Bold", lh: 61.6, color: "#FFFFFF", opacity: 0.95, width: 940 }) : null;
    const hT = txt(s.headline, { size: 100, w: "Black", lh: 115, ls: -3, color: "#FFFFFF", width: 940 });
    const subY = 1142;
    if (subT) put(frame, subT, 72, subY);
    const hY = (subT ? subY - 36 : 1200) - hT.height;
    put(frame, hT, 72, hY);
    if (s.top) { const tp = txt(s.top, { size: 38, w: "Bold", color: "#FFFFFF", opacity: 0.95, width: 940 }); put(frame, tp, 72, hY - 18 - tp.height); tp.name = "표지 윗줄"; }
    hT.name = "표지 헤드라인"; if (subT) subT.name = "표지 서브";
  } else if (s.type === "std_service" && CFG.serviceCloneId) {
    frame = (await figma.getNodeByIdAsync(CFG.serviceCloneId)).clone(); sec.appendChild(frame);
  } else if (s.type === "std_cta") {
    frame = figma.createFrame(); sec.appendChild(frame); frame.resize(1080, 1350); frame.fills = solid("#071022");
    const logo = (await figma.getNodeByIdAsync(CFG.darkLogoId)).clone(); frame.appendChild(logo); logo.x = 76; logo.y = 65;
    put(frame, txt(`${String(i + 1).padStart(2, "0")} / ${String(n).padStart(2, "0")}`, { size: 22, w: "Medium", color: "#D1E0FC" }), 920, 73);
    let y = s.top || 220;
    const h = put(frame, txt(s.headline, { size: 62, w: "Black", lh: 76.3, color: "#FFFFFF", width: 930 }), 76, y); y += h.height + 28;
    if (s.sub) { const sb = put(frame, txt(s.sub, { size: 29, w: "Medium", color: "#D1E0FC", width: 928 }), 76, y); y += sb.height + 34; }
    const panel = al("VERTICAL", { gap: 0, pad: [12, 34, 12, 34], fill: "#F3F7FE", fillOpacity: 0.92, radius: 23, name: "체크리스트" });
    frame.appendChild(panel); panel.x = 76; panel.y = y; panel.resize(928, panel.height); panel.layoutSizingHorizontal = "FIXED";
    s.rows.forEach((r, j) => {
      const row = add(panel, al("HORIZONTAL", { gap: 26, pad: [20, 0, 20, 0] }), true);
      if (j) { row.strokes = solid("#C7D8FF"); row.strokeAlign = "INSIDE"; row.strokeTopWeight = 2; row.strokeRightWeight = 0; row.strokeLeftWeight = 0; row.strokeBottomWeight = 0; }
      const num = add(row, txt(r.num || String(j + 1).padStart(2, "0"), { size: 34, w: "Black", color: A })); num.resize(64, num.height);
      const col = add(row, al("VERTICAL", { gap: 6 }), true);
      add(col, txt(r.title, { size: 32, w: "Black", color: INK2, lh: 41.6 }), true);
      if (r.prompt) add(col, txt(r.prompt, { size: 25, w: "Medium", color: GRAY2 }), true);
    });
    if (s.product) {
      put(frame, txt(s.product, { size: 31, w: "Bold", color: "#FFFFFF" }), 76, 1092);
      if (s.product_sub) put(frame, txt(s.product_sub, { size: 25, w: "Medium", color: "#D1E0FC" }), 76, 1150);
    }
    if (s.button) {
      const btn = al("HORIZONTAL", { pad: [0, 32, 0, 32], fill: A, fillOpacity: 0.95, radius: 17, center: true, name: "CTA 버튼" });
      frame.appendChild(btn); btn.x = 76; btn.y = 1221; btn.resize(928, 84); btn.layoutSizingHorizontal = "FIXED"; btn.layoutSizingVertical = "FIXED";
      add(btn, txt(s.button, { size: 30, w: "Bold", color: "#FFFFFF" }));
    }
  } else {
    frame = figma.createFrame(); sec.appendChild(frame); frame.resize(1080, 1350); frame.fills = solid("#FFFFFF");
    await brandLight(frame);
    const y = head(frame, s);
    const clones = (CFG.clones || {})[i];
    if (clones) {
      for (const id of clones) { const c = (await figma.getNodeByIdAsync(id)).clone(); frame.appendChild(c); created.push(c.id); }
    } else {
      const body = al("VERTICAL", { gap: 30, name: "본문" });
      frame.appendChild(body); body.x = 72; body.y = y + (s.body_top || 48); body.resize(936, body.height); body.layoutSizingHorizontal = "FIXED"; body.primaryAxisSizingMode = "AUTO"; body.clipsContent = false;
      for (const b of s.blocks || []) add(body, block(b), true);
      equalizeCompare(body);
      const bottom = body.y + body.height;
      if (s.conclusion && bottom > 1110) report.push(`P${i + 1} 본문이 결론과 ${Math.round(bottom - 1110)}px 겹침`);
    }
    tail(frame, s);
  }
  frame.name = name; frame.x = 100 + i * 1180; frame.y = 100; frame.clipsContent = true;
  created.push(frame.id);
}
return { sectionId: sec.id, frames: sec.children.map(c => ({ id: c.id, name: c.name })), warnings: report, createdCount: created.length };
