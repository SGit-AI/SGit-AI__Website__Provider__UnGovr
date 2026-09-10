/* Print each deck's slides.html to a 16:9 PDF.
   node tools/make-pdfs.js http://localhost:8734
   The PDFs are committed to the repo under files/decks/ and copied into the build,
   because CI has no browser and a deck nobody can download is not the point. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const BASE = process.argv[2] || 'http://localhost:8734';
const OUT = 'files/decks';

const DECKS = ['what-we-learned', 'what-we-built', 'how-it-composes', 'what-we-plan',
               'how-this-publishes', 'what-the-build-refuses'];

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const d of DECKS) {
    const p = await b.newPage({ viewport: { width: 1200, height: 675 } });
    await p.goto(`${BASE}/decks/${d}/slides.html`, { waitUntil: 'networkidle' });
    await p.emulateMedia({ media: 'print' });
    // Every screenshot must have decoded before the print, or it prints as an empty
    // box — which is exactly what happened to the slides below the fold.
    const missing = await p.evaluate(async () => {
      const imgs = [...document.images];
      await Promise.all(imgs.map(i => i.complete ? null : i.decode().catch(() => null)));
      return imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src);
    });
    if (missing.length) { console.error('  IMAGES DID NOT LOAD:', missing); process.exitCode = 1; }
    await p.waitForTimeout(300);
    const file = path.join(OUT, `${d}.pdf`);
    // The CSS owns the page size. Passing width/height here instead cost a
    // sub-point rounding difference against the @page rule, and every slide spilled
    // onto a second, blank page — 20 pages for a 10-slide deck. One source of
    // geometry, in the stylesheet, next to the slide it describes.
    await p.pdf({ path: file, printBackground: true, preferCSSPageSize: true,
                  margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    const kb = Math.round(fs.statSync(file).size / 1024);
    console.log(`  ${d.padEnd(18)} ${String(kb).padStart(5)} KB`);
    await p.close();
  }
  await b.close();
})();
