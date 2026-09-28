// Fotografa uma página estática (capa de reel, thumbnail, card) em PNG.
//   node foto.mjs capa.html?n=1 out/capa-1.png 1080x1920
//   node foto.mjs thumb.html out/thumb.png 1280x720
// A página deve fazer `window.__ready = true` depois de document.fonts.ready e das imagens decodificadas.
import { chromium } from 'playwright';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const [src, out, size = '1080x1920'] = process.argv.slice(2);
if (!src || !out) { console.error('uso: node foto.mjs pagina.html[?q] saida.png LxA'); process.exit(1) }
const [w, h] = size.split('x').map(Number);
const [file, q = ''] = src.split('?');
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: w, height: h } });
await p.goto(pathToFileURL(path.resolve(file)).href + (q ? '?' + q : ''));
await p.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
await p.waitForTimeout(200);
await p.screenshot({ path: out });
await b.close();
console.log(out);
