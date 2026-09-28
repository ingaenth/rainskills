// Renderiza uma peça HTML (lib.js) em MP4: fotografa seek(t) quadro a quadro no Chromium do Playwright,
// sintetiza o áudio no próprio navegador (OfflineAudioContext) e junta no ffmpeg.
//
//   node render.mjs peca.html                  -> out/peca.mp4   (tamanho vem de window.SIZE; padrão 1080x1920)
//   STILLS=1,5.5,12 node render.mjs peca.html  -> out/peca-<t>.png (revisão; depois: python folha.py peca 1,5.5,12)
//   FPS=60 LUFS=-14 BITRATE=16M OUT=dir node render.mjs peca.html
//
// Requisitos: node 18+, `npm i playwright && npx playwright install chromium`, ffmpeg no PATH.
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const arg = process.argv[2];
if (!arg) { console.error('uso: node render.mjs peca.html'); process.exit(1) }
const file = path.resolve(arg.endsWith('.html') ? arg : arg + '.html');
const name = path.basename(file, '.html');
const FPS = +(process.env.FPS || 30), LUFS = process.env.LUFS || '-14', BITRATE = process.env.BITRATE || '16M';
const OUT = path.resolve(process.env.OUT || 'out'); fs.mkdirSync(OUT, { recursive: true });
const run = args => new Promise((res, rej) => { const p = spawn('ffmpeg', args, { stdio: ['ignore', 'inherit', 'inherit'] }); p.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))) });

const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--font-render-hinting=none', '--autoplay-policy=no-user-gesture-required', '--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.error('ERRO NA PÁGINA:', e.message));
page.on('console', m => { if (m.type() === 'error') console.error('console:', m.text()) });
const url = pathToFileURL(file).href + '?render';
await page.goto(url);
const SIZE = await page.evaluate(() => window.SIZE || [1080, 1920]);
if (SIZE[0] !== 1080 || SIZE[1] !== 1920) { await page.setViewportSize({ width: SIZE[0], height: SIZE[1] }); await page.goto(url) }
await page.waitForFunction(() => window.__ready === true, null, { timeout: 120000 });
const DUR = await page.evaluate(() => window.DUR);

if (process.env.STILLS) {
  for (const s of process.env.STILLS.split(',')) { await page.evaluate(t => window.seek(t), +s); await page.screenshot({ path: path.join(OUT, `${name}-${s}.png`) }) }
  console.log('stills ok'); await browser.close(); process.exit(0);
}
const t0 = Date.now();
const wav = path.join(OUT, name + '.wav');
fs.writeFileSync(wav, Buffer.from(await page.evaluate(() => window.renderAudioB64()), 'base64'));
const vid = path.join(OUT, name + '.video.mp4');
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
  '-c:v', 'libx264', '-preset', 'slow', '-b:v', BITRATE, '-maxrate', '20M', '-bufsize', '32M', '-tune', 'film', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', String(FPS), vid],
  { stdio: ['pipe', 'inherit', 'inherit'] });
const done = new Promise(r => ff.on('close', r));
const N = Math.round(DUR * FPS);
for (let f = 0; f < N; f++) {
  await page.evaluate(t => window.seek(t), f / FPS);
  const buf = await page.screenshot({ type: 'jpeg', quality: 100 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (f % (FPS * 10) === 0) console.log(`${name}: ${f}/${N}`);
}
ff.stdin.end(); await done; await browser.close();
await run(['-y', '-loglevel', 'error', '-i', vid, '-i', wav, '-c:v', 'copy', '-af', `loudnorm=I=${LUFS}:TP=-1.5:LRA=11`,
  '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', '-movflags', '+faststart', path.join(OUT, name + '.mp4')]);
fs.unlinkSync(vid); fs.unlinkSync(wav);
console.log(`${name}: ${N} quadros, ${SIZE[0]}x${SIZE[1]}, ${DUR}s em ${((Date.now() - t0) / 1000).toFixed(0)}s → ${path.join(OUT, name + '.mp4')}`);
