/* Capture screenshots of this site's own features, for the decks and their PDFs.
   Run against a locally served build:  python3 -m http.server 8734 -d docs
   then: node tools/shots.js http://localhost:8734
   The images land in files/shots/ and are copied verbatim into the build. */
const { chromium } = require('playwright');
const BASE = process.argv[2] || 'http://localhost:8734';
const OUT = 'files/shots';

const SHOTS = [
  { id: 'home',        url: '/',              clip: [0, 0, 1400, 900] },
  { id: 'ledger',      url: '/ledger/',       clip: [0, 0, 1400, 900] },
  { id: 'coverage',    url: '/coverage/',     clip: [0, 0, 1400, 900] },
  { id: 'join',        url: '/join/',         clip: [0, 0, 1400, 980] },
  { id: 'instruments', url: '/instruments/',  clip: [0, 0, 1400, 900] },
  { id: 'estate',      url: '/estate/',       clip: [0, 0, 1400, 1000] },
  { id: 'retrievals',  url: '/retrievals/',   clip: [0, 0, 1400, 900] },
  { id: 'packs',       url: '/packs/security-graph/06__verification/', clip: [0, 0, 1400, 950] },
  { id: 'decks',       url: '/decks/',        clip: [0, 0, 1400, 860] },
  { id: 'vaultpage',   url: '/vault/',        clip: [0, 0, 1400, 900] },
];

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 2 });
  for (const s of SHOTS) {
    await p.goto(BASE + s.url, { waitUntil: 'networkidle' });
    await p.waitForTimeout(350);
    const [x, y, width, height] = s.clip;
    await p.screenshot({ path: `${OUT}/${s.id}.png`, clip: { x, y, width, height } });
    console.log('  ' + s.id.padEnd(12), s.url);
  }
  // The vault app itself, opened standalone from the working copy.
  const va = process.env.VAULT_INDEX;
  if (va) {
    await p.goto('file://' + va, { waitUntil: 'load' });
    await p.waitForTimeout(900);
    await p.screenshot({ path: `${OUT}/vaultapp.png`, clip: { x: 0, y: 0, width: 1400, height: 900 } });
    console.log('  vaultapp     (standalone, from the vault working copy)');
  }
  await b.close();
})();
