#!/usr/bin/env node
// 슬라이드 HTML(1080px 고정폭) 폴더를 PNG로 캡처한다.
// 사용: node snap.js <html-dir> [--scale 1]
// render_carousel.py 가 만든 slide-XX.html 파일들을 찾아 같은 폴더에 slide-XX.png 로 저장.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = process.argv[2];
  if (!dir) { console.error('usage: node snap.js <html-dir> [--scale N]'); process.exit(1); }
  const scaleIdx = process.argv.indexOf('--scale');
  const scale = scaleIdx > -1 ? Number(process.argv[scaleIdx + 1]) : 1;
  const files = fs.readdirSync(dir).filter(f => /^slide-\d+\.html$/.test(f)).sort();
  if (!files.length) { console.error('no slide-XX.html in ' + dir); process.exit(1); }
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ deviceScaleFactor: scale });
  const page = await ctx.newPage();
  for (const f of files) {
    const url = 'file://' + path.resolve(dir, f);
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const el = await page.$('.slide');
    const box = await el.boundingBox();
    await page.setViewportSize({ width: Math.round(box.width), height: Math.round(box.height) });
    const out = path.join(dir, f.replace(/\.html$/, '.png'));
    await el.screenshot({ path: out, type: 'png' });
    console.log('saved', out);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
