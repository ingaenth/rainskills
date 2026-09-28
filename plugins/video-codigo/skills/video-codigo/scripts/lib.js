'use strict';
// video-codigo — motor genérico de vídeo em JavaScript.
// Timeline determinística: cada quadro é seek(t) puro; o render.mjs fotografa quadro a quadro.
// Tamanho padrão 1080x1920 (reel). Para 16:9 defina window.SIZE = [1920, 1080] ANTES de carregar este arquivo.
// A marca entra por variáveis CSS (--bg, --fg, --accent… em lib.css); nada aqui é de cliente.
const [W, H] = window.SIZE || [1080, 1920];
if (W > H) document.body.classList.add("wide");
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const P = (t, a, b) => clamp((t - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;
const E = {
  out: t => 1 - (1 - t) ** 3, out5: t => 1 - (1 - t) ** 5, in: t => t * t * t,
  inOut: t => t < .5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2,
  back: t => 1 - (1 - clamp(t)) ** 4,     // desacelera e assenta, sem quicar (padrão seguro para qualquer marca)
  overshoot: t => { const c1 = 1.7, c3 = c1 + 1; return t <= 0 ? 0 : 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2 },   // só se a marca permitir "pop"
};
const bump = (t, a, d) => Math.sin(Math.PI * P(t, a, a + d));
const $ = (tag, cls, parent, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (parent) parent.appendChild(e); return e };
const div = (cls, parent, html) => $('div', cls, parent, html);
function place(e, x, y, w, h) { if (!e.style.position) e.style.position = 'absolute'; e.style.left = x + 'px'; e.style.top = y + 'px'; if (w != null) e.style.width = w + 'px'; if (h != null) e.style.height = h + 'px'; return e }
function T(e, x = 0, y = 0, s = 1, r = 0, extra = '') { e.style.transform = `translate(${x}px,${y}px) scale(${s}) rotate(${r}deg) ${extra}` }
function O(e, o) { o = clamp(o); e.style.opacity = o; e.style.visibility = o <= 0.001 ? 'hidden' : 'visible' }
function txt(e, s) { if (e._t !== s) { e.innerHTML = s; e._t = s } }
function rise(e, t, a, d = .5, dist = 40) { const k = E.out(P(t, a, a + d)); O(e, k); T(e, 0, (1 - k) * dist) }
function inout(e, t, a, b, d = .35, dist = 50) { const k = E.out(P(t, a, a + d)), ko = E.in(P(t, b - .25, b)); O(e, k * (1 - ko)); T(e, 0, (1 - k) * dist - ko * dist * .6) }
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296 } }
const grp = n => String(Math.round(Math.abs(n))).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
// moeda BRL; troque por Intl se precisar de outra
const brl = v => (v < 0 ? '−' : '') + 'R$ ' + grp(Math.floor(Math.abs(v))) + ',' + String(Math.round(Math.abs(v) * 100) % 100).padStart(2, '0');
const NS = 'http://www.w3.org/2000/svg';
const CHECK = (s = 56, c = '#fff', w = 3.2) => `<svg width="${s}" height="${s}" viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const CUR_SVG = '<svg width="56" height="56" viewBox="0 0 24 24"><path d="M4 2l16 9.6-7.1 1.5 3.9 7.4-3 1.6-3.9-7.5L4 19.6z" fill="#fafafa" stroke="#09090b" stroke-width="1.5" stroke-linejoin="round"/></svg>';

const cssVar = (n, d) => (getComputedStyle(document.documentElement).getPropertyValue(n).trim() || d);
const stage = document.getElementById('stage');
const updaters = [], pending = [];
function scene(a, b, bg) { const L = div('layer', stage); if (bg) L.style.background = bg; updaters.push(t => { L.style.display = t >= a && t < b ? 'block' : 'none' }); return L }
function on(fn) { updaters.push(fn) }

// ---- janela sobre um print (ou vídeo) real, com câmera virtual: .set(cx, cy, escala) — travada dentro da imagem ----
function shot(parent, src, x, y, w, h, iw = 1920, ih = 1080, cls = 'shot') {
  const f = div(cls, parent); place(f, x, y, w, h);
  const isV = /\.webm$|\.mp4$/.test(src);
  const m = $(isV ? 'video' : 'img', '', f); m.src = src; m.style.width = iw + 'px'; m.style.height = ih + 'px';
  if (isV) { m.muted = true; m.preload = 'auto'; m.playsInline = true }
  return { f, m, w, h, set(cx, cy, s) { cx = clamp(cx, w / 2 / s, iw - w / 2 / s); cy = clamp(cy, h / 2 / s, ih - h / 2 / s); m.style.transform = `translate(${w / 2 - cx * s}px,${h / 2 - cy * s}px) scale(${s})` } };
}
// quadro de vídeo determinístico (no render espera o 'seeked'; no preview só sincroniza)
function seekVideo(v, time) {
  time = Math.max(0, Math.min(time, (v.duration || 99) - .05));
  if (window.__live) { if (Math.abs(v.currentTime - time) > .25) v.currentTime = time; if (v.paused) v.play().catch(() => { }); return }
  if (Math.abs(v.currentTime - time) < .004) return;
  pending.push(new Promise(r => { const done = () => { v.removeEventListener('seeked', done); r() }; v.addEventListener('seeked', done); v.currentTime = time }));
}

// ---- legenda cinética: "*palavra*" destaque (cor --accent2), "_palavra_" amarelo, "~palavra~" vermelho, "|" quebra de linha ----
function words(parent, text, x, y, w, size = 70) {
  const e = div('words', parent); place(e, x, y, w); e.style.fontSize = size + 'px';
  const ws = text.split(' ').map(s => { let c = ''; if (/^\*.*\*[.,!?:]*$/.test(s)) { c = 'hl'; s = s.replace(/\*/g, '') } else if (/^_.*_[.,!?:]*$/.test(s)) { c = 'yl'; s = s.replace(/_/g, '') } else if (/^~.*~[.,!?:]*$/.test(s)) { c = 'rd'; s = s.replace(/~/g, '') } return $('span', c, e, s === '|' ? '' : s) });
  ws.forEach((s, i) => { if (s.innerHTML === '') { s.style.display = 'block'; s.style.height = '0' } });
  return { e, ws, anim(t, a, b, rate = .07) { ws.forEach((s, i) => { const k = E.back(P(t, a + i * rate, a + i * rate + .28)); s.style.opacity = P(t, a + i * rate, a + i * rate + .06); s.style.transform = `translateY(${(1 - k) * 30}px) scale(${.7 + .3 * k})` }); const ko = E.in(P(t, b - .22, b)); e.style.opacity = 1 - ko; e.style.transform = `translateY(${-ko * 30}px)` } };
}

// ---- traço desenhado (telestrador): tele(...)(k) desenha de 0 a 1; wobble = elipse à mão; arrow = seta curva ----
function tele(parent, d, w = 9, color = cssVar('--mark', '#facc15'), glow = 'rgba(0,0,0,.35)') {
  const s = document.createElementNS(NS, 'svg'); s.setAttribute('class', 'tele'); s.setAttribute('width', W); s.setAttribute('height', H); parent.appendChild(s);
  s.innerHTML = `<path d="${d}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 10px ${glow})"/>`;
  const p = s.firstChild, L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
  return k => { p.style.strokeDashoffset = L * (1 - clamp(k)); s.style.visibility = k <= 0 ? 'hidden' : 'visible' };
}
const rt = rng(42);
function wobble(cx, cy, rx, ry, turns = 1.12) { let d = ''; const n = 64; for (let i = 0; i <= n; i++) { const a = -2.2 + i / n * Math.PI * 2 * turns; const w = 1 + (rt() - .5) * .05 + .05 * Math.sin(i * .3); d += (i ? ' L' : 'M') + (cx + Math.cos(a) * rx * w).toFixed(1) + ' ' + (cy + Math.sin(a) * ry * w).toFixed(1) } return d }
function arrow(x0, y0, x1, y1, bend = 60) { const mx = (x0 + x1) / 2 - bend, my = (y0 + y1) / 2 - bend; const a = Math.atan2(y1 - my, x1 - mx), h = 34; return `M${x0} ${y0} Q${mx} ${my} ${x1} ${y1} M${x1 - h * Math.cos(a - .5)} ${y1 - h * Math.sin(a - .5)} L${x1} ${y1} L${x1 - h * Math.cos(a + .5)} ${y1 - h * Math.sin(a + .5)}` }
function tlabel(parent, text, x, y) { const e = div('tlbl', parent, `<span>${text}</span>`); place(e, x, y); return (t, a, b = 1e9) => { const k = E.back(P(t, a, a + .3)); O(e, P(t, a, a + .05) * (1 - P(t, b - .15, b))); T(e, 0, (1 - k) * 16, 1) } }

// ---- transição: barra sólida na cor --accent atravessa a tela + véu na cor --bg ----
function sweeps(times) {
  const SL = div('layer', stage); SL.style.pointerEvents = 'none'; SL.style.zIndex = 50;
  const band = div('abs', SL); band.style.cssText += `;left:0;top:${-H * .25}px;width:${Math.round(W * .06)}px;height:${H * 1.5}px;background:${cssVar('--accent', '#6d4cff')}`;
  const veil = div('layer', SL); veil.style.background = cssVar('--bg', '#08080c');
  on(t => {
    let s = null; for (const c of times) if (t > c - .45 && t < c + .45) s = c;
    if (s === null) { O(band, 0); O(veil, 0); return }
    const k = P(t, s - .45, s + .45); band.style.transform = `translateX(${lerp(-W, W * 1.2, E.inOut(k))}px) rotate(12deg)`; O(band, 1);
    O(veil, .85 * bump(t, s - .3, .6));
  });
}
// ---- moldura de vidro com barra de navegador falsa, segurando print ou vídeo real ----
function glass(parent, src, x, y, w, h, iw = 1920, ih = 980, bar = true) {
  const f = div('glassframe', parent); place(f, x, y, w, h);
  const bh = bar ? Math.round(Math.min(w, 1400) * .04) : 0;
  if (bar) { const b = div('gbar', f); b.style.height = bh + 'px'; b.innerHTML = '<i></i><i></i><i></i>' }
  const s = shot(f, src, 0, bh, w, h - bh, iw, ih); s.frame = f; return s;
}
// ---- ícone de canal: SVGs do simple-icons em assets/icons/<nome>.svg + glifos desenhados (sms, email, call, bell) ----
const CH_BG = { whatsapp: '#25D366', instagram: 'linear-gradient(45deg,#F58529,#DD2A7B 50%,#8134AF)', facebook: '#1877F2', tiktok: '#111118', x: '#111118', threads: '#111118', gmail: '#EA4335', openai: '#111118', twilio: '#F22F46', sms: '#0ea5e9', email: '#6366f1', call: '#10b981', bell: '#f59e0b' };
function chIcon(parent, name, size = 96) {
  const e = div('chicon', parent); e.style.width = e.style.height = size + 'px'; e.style.borderRadius = size * .28 + 'px'; e.style.background = CH_BG[name] || '#111118';
  const G = { sms: '<path d="M4 5h16v11H8l-4 4z"/>', email: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', call: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a1 1 0 01-1 1A16 16 0 014 5a1 1 0 011-1z"/>', bell: '<path d="M6 16V11a6 6 0 0112 0v5l2 2H4z"/><path d="M10 20a2 2 0 004 0"/>' }[name];
  if (G) e.innerHTML = `<svg width="${size * .52}" height="${size * .52}" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round" stroke-linecap="round">${G}</svg>`;
  else { const im = $('img', '', e); im.src = `assets/icons/${name}.svg`; im.style.width = im.style.height = size * .5 + 'px'; im.style.filter = 'invert(1)' }
  return e;
}
// ---- cartão final genérico: logo (arquivo oficial) + frase + botão + nota. Marca por variáveis CSS. ----
// Troque/estenda por projeto (ex.: variantes com animação de logo) num brand.js próprio.
function endCard(L, a, { logo = null, logoW = W > H ? 520 : 620, headline = '', cta = 'Teste grátis', note = '' } = {}) {
  const wide = W > H;
  L.style.background = cssVar('--bg', '#08080c');
  const halo = div('abs', L); place(halo, W / 2 - 700, (wide ? H * .38 : H * .36) - 700, 1400, 1400);
  halo.style.background = `radial-gradient(circle, ${cssVar('--glow', 'rgba(109,76,255,.3)')} 0%, transparent 65%)`;
  let lg = null; if (logo) { lg = $('img', 'abs', L); lg.src = logo; place(lg, W / 2 - logoW / 2, wide ? 130 : 380, logoW) }
  const hl = div('abs ctr hx', L, headline); place(hl, 40, wide ? 400 : 720, W - 80); hl.style.fontSize = (wide ? 84 : 92) + 'px';
  const pw = wide ? 540 : 640, py = wide ? 720 : 1180; const pl = div('pill', L, cta + ' <span>→</span>'); place(pl, W / 2 - pw / 2, py, pw, wide ? 96 : 112);
  const nt = div('abs ctr', L, note); place(nt, 0, py + (wide ? 124 : 150), W); nt.style.cssText += ';font:500 30px var(--font-text);color:var(--fg3)';
  on(t => {
    if (t < a - .1) return;
    O(halo, E.out(P(t, a, a + 1.2)));
    if (lg) reveal(lg, t, a + .1, .9, 24);
    reveal(hl, t, a + .5, .8, 40);
    const k = E.out5(P(t, a + 1.1, a + 1.6)); O(pl, P(t, a + 1.1, a + 1.3)); T(pl, 0, (1 - k) * 24);
    rise(nt, t, a + 1.5, .5, 16);
  });
}
// entrada cinematográfica: sobe e desfoca → nítido
function reveal(e, t, a, d = .9, dist = 40) { const k = E.out5(P(t, a, a + d)); O(e, P(t, a, a + d * .4)); T(e, 0, (1 - k) * dist); e.style.filter = k < .999 ? `blur(${((1 - k) * 16).toFixed(1)}px)` : 'none' }

// ---- foto com ponto focal e câmera lenta: photo(pai, src, x, y, w, h, [fx, fy]).cam(escala, dx, dy) ----
// object-fit:cover + origem da escala no foco: o assunto continua no quadro em qualquer recorte (16:9 → 9:16).
function photo(parent, src, x, y, w, h, focal = [.5, .5]) {
  const f = div('ph', parent); place(f, x, y, w, h);
  const im = $('img', '', f); im.src = src;
  im.style.objectPosition = im.style.transformOrigin = `${focal[0] * 100}% ${focal[1] * 100}%`;
  return { f, im, cam(s = 1, dx = 0, dy = 0) { im.style.transform = `translate(${dx}px,${dy}px) scale(${s})` } };
}
// ---- sombreamento (degradê) que garante contraste do texto sobre foto ----
function shade(parent, bg) { const e = div('shade', parent); e.style.background = bg; return e }
// ---- linha com máscara: o texto sobe de trás de uma borda invisível. .go(k) com k 0→1 ----
// o padding interno evita cortar descendentes (g, y, p) e o itálico que passa da caixa.
function mline(parent, html, x, y, w, css = '', align = 'left') {
  const m = div('mask', parent); place(m, x, y, w);
  const inner = div('', m, html); inner.style.cssText += ';' + css + ';padding:.04em .12em .22em 0'; inner.style.textAlign = align;
  return { m, inner, go(k) { inner.style.transform = `translateY(${((1 - k) * 110).toFixed(2)}%)`; O(m, k > .001 ? 1 : 0) } };
}
// ---- cortina de entrada da cena L a partir de t=a: 'up' | 'down' | 'left' | 'right' | 'circle' ----
// recorta a camada com clip-path e corre um filete na cor --accent2 pela borda da cortina.
function curtain(L, a, dir = 'up', d = .6) {
  const edge = div('edge', stage); const vert = dir === 'left' || dir === 'right'; if (vert) edge.classList.add('v');
  on(t => {
    const k = E.inOut(P(t, a, a + d)), r = ((1 - k) * 100).toFixed(2);
    L.style.clipPath = k >= 1 ? 'none' : { up: `inset(${r}% 0 0 0)`, down: `inset(0 0 ${r}% 0)`, left: `inset(0 0 0 ${r}%)`, right: `inset(0 ${r}% 0 0)`, circle: `circle(${(k * 120).toFixed(2)}% at 50% 46%)` }[dir];
    const on_ = t >= a && t < a + d && dir !== 'circle'; edge.style.display = on_ ? 'block' : 'none';
    if (!on_) return;
    const pos = { up: (1 - k) * H, down: k * H, left: (1 - k) * W, right: k * W }[dir];
    if (vert) edge.style.left = (pos - 1) + 'px'; else edge.style.top = (pos - 1) + 'px';
    O(edge, bump(t, a, d) * 1.2);
  });
  return edge;
}
// ---- linha de cardápio/preço: nome grande; embaixo rótulo, pontilhado e valor. Devolve (t, a) => anima ----
// tone: { name, meta, lead, price (cores), nameSize, priceSize (px) } — tudo do briefing, nada fixo.
function priceRow(parent, it, x, y, w, tone = {}) {
  const c = k => tone[k] || cssVar(k === 'price' || k === 'lead' ? '--accent2' : k === 'meta' ? '--fg2' : '--fg', '#fff');
  const e = div('prow', parent); place(e, x, y, w);
  e.innerHTML = `<div class="mask pnm"><div style="font-size:${tone.nameSize || 72}px;color:${c('name')}">${it.name}</div></div>` +
    `<div class="prr" style="color:${c('meta')}"><span class="pmt">${it.meta || ''}</span><span class="pld" style="color:${c('lead')}"></span>` +
    `<span class="ppr" style="font-size:${tone.priceSize || 96}px;color:${c('price')}">${it.from ? `<i>${it.from === true ? 'from' : it.from}</i>` : ''}${it.price}</span></div>`;
  const nm = e.querySelector('.pnm>div'), mt = e.querySelector('.pmt'), ld = e.querySelector('.pld'), pr = e.querySelector('.ppr');
  return (t, a) => {
    nm.style.transform = `translateY(${((1 - E.out5(P(t, a, a + .8))) * 110).toFixed(2)}%)`;
    const km = E.out(P(t, a + .3, a + .9)); O(mt, km); T(mt, 0, (1 - km) * 14);
    ld.style.transform = `scaleX(${E.out(P(t, a + .35, a + 1)).toFixed(3)})`;
    const kp = E.out5(P(t, a + .45, a + 1.05)); O(pr, kp); T(pr, (1 - kp) * 30, 0);
  };
}

// ---- kit de áudio (Web Audio offline): tudo sintetizado, sem direito autoral; cada K.* agenda um som no tempo t ----
function makeKit(ctx) {
  const sr = ctx.sampleRate;
  const comp = ctx.createDynamicsCompressor(); comp.threshold.value = -16; comp.knee.value = 8; comp.ratio.value = 3.5; comp.attack.value = .004; comp.release.value = .18; comp.connect(ctx.destination);
  const bus = ctx.createGain(); bus.gain.value = .85; bus.connect(comp);
  const ir = ctx.createBuffer(2, sr * 2.8, sr); const ri = rng(3); for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < d.length; i++) d[i] = (ri() * 2 - 1) * Math.pow(1 - i / d.length, 3) }
  const rv = ctx.createConvolver(); rv.buffer = ir; const rvg = ctx.createGain(); rvg.gain.value = .3; rv.connect(rvg); rvg.connect(bus);
  const nb = ctx.createBuffer(1, sr * 2, sr); { const d = nb.getChannelData(0); const rn = rng(5); for (let i = 0; i < d.length; i++) d[i] = rn() * 2 - 1 }
  const mf = m => 440 * Math.pow(2, (m - 69) / 12);
  const out = (send = 0, pan = 0) => { const g = ctx.createGain(); let n = g; if (pan) { const p = ctx.createStereoPanner(); p.pan.value = pan; g.connect(p); n = p } n.connect(bus); if (send) { const s = ctx.createGain(); s.gain.value = send; n.connect(s); s.connect(rv) } return g };
  const osc = (type, f, t0, t1) => { const o = ctx.createOscillator(); o.type = type; o.frequency.value = f; o.start(t0); o.stop(t1); return o };
  let nOff = 0; const noise = (t0, t1) => { const s = ctx.createBufferSource(); s.buffer = nb; s.loop = true; s.start(t0, (nOff = (nOff + .37) % 1.9)); s.stop(t1); return s };
  const filt = (type, f, q = .7) => { const b = ctx.createBiquadFilter(); b.type = type; b.frequency.value = f; b.Q.value = q; return b };
  const perc = (g, t, a, v, d) => { g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + a); g.gain.exponentialRampToValueAtTime(.0001, t + a + d) };
  const K = { ctx, mf, out, osc, noise, filt, perc };
  K.kick = (t, v = .6, f0 = 150, f1 = 45, d = .4) => { const g = out(0), o = osc('sine', f0, t, t + d + .05); o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(f1, t + .12); o.connect(g); perc(g, t, .002, v, d) };
  K.snare = (t, v = .2) => { const g = out(.25), bp = filt('bandpass', 1800, .8); bp.connect(g); noise(t, t + .25).connect(bp); perc(g, t, .001, v, .18); const g2 = out(0); osc('triangle', 190, t, t + .15).connect(g2); perc(g2, t, .001, v * .6, .1) };
  K.clap = (t, v = .14) => { const g = out(.35, -.1), bp = filt('bandpass', 1500, 1.1); bp.connect(g); noise(t, t + .3).connect(bp); g.gain.setValueAtTime(0, t);[0, .011, .022].forEach(o => { g.gain.linearRampToValueAtTime(v, t + o + .001); g.gain.linearRampToValueAtTime(v * .3, t + o + .009) }); g.gain.exponentialRampToValueAtTime(.0001, t + .24) };
  K.tom = (t, f = 120, v = .35) => { const g = out(.2), o = osc('sine', f, t, t + .4); o.frequency.exponentialRampToValueAtTime(f * .55, t + .3); o.connect(g); perc(g, t, .002, v, .32) };
  K.hat = (t, v = .03, d = .045) => { const g = out(0, .25), hp = filt('highpass', 7500); hp.connect(g); noise(t, t + d + .02).connect(hp); perc(g, t, .001, v, d) };
  K.crash = (t, v = .09) => { const g = out(.4, .1), hp = filt('highpass', 5000); hp.connect(g); noise(t, t + 1.8).connect(hp); perc(g, t, .002, v, 1.6) };
  K.bass = (m, t, d, v = .14, cut = 420) => { const g = out(0), lp = filt('lowpass', cut, 1.2); lp.connect(g); osc('sawtooth', mf(m), t, t + d + .1).connect(lp); osc('sine', mf(m), t, t + d + .1).connect(g); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + .01); g.gain.setValueAtTime(v, t + d - .04); g.gain.linearRampToValueAtTime(0, t + d) };
  K.sub = (m, t, d, v = .16) => { const g = out(0); osc('sine', mf(m), t, t + d + .1).connect(g); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + .02); g.gain.setValueAtTime(v, t + d - .08); g.gain.linearRampToValueAtTime(0, t + d) };
  K.stab = (notes, t, v = .05, d = .35, cut = 3800) => { const g = out(.35), lp = filt('lowpass', 2600, 1); lp.connect(g); lp.frequency.setValueAtTime(cut, t); lp.frequency.exponentialRampToValueAtTime(800, t + d); notes.forEach(m => [-9, 9].forEach(dt => { const o = osc('sawtooth', mf(m), t, t + d + .1); o.detune.value = dt; o.connect(lp) })); perc(g, t, .006, v, d) };
  K.pad = (notes, t0, t1, v = .012, cut = 1100) => { const lp = filt('lowpass', cut, .4); const g = out(.55); lp.connect(g); g.gain.setValueAtTime(0, t0); g.gain.linearRampToValueAtTime(1, t0 + .4); g.gain.setValueAtTime(1, t1); g.gain.linearRampToValueAtTime(0, t1 + .9); notes.forEach(m => [-7, 7].forEach(dt => { const o = osc('sawtooth', mf(m), t0, t1 + 1); o.detune.value = dt; const og = ctx.createGain(); og.gain.value = v; o.connect(og); og.connect(lp) })) };
  K.pluck = (m, t, v = .05, pan = 0, type = 'triangle') => { const g = out(.3, pan), lp = filt('lowpass', 900, 2); lp.connect(g); lp.frequency.setValueAtTime(4800, t); lp.frequency.exponentialRampToValueAtTime(650, t + .22); osc(type, mf(m), t, t + .5).connect(lp); perc(g, t, .003, v, .38) };
  K.keys = (m, t, d = .8, v = .05, pan = 0) => { const g = out(.4, pan), lp = filt('lowpass', 2400, .5); lp.connect(g);[[1, 1], [2, .25], [3, .08]].forEach(([r, a]) => { const o = osc('sine', mf(m) * r, t, t + d + .2); const og = ctx.createGain(); og.gain.value = a; o.connect(og); og.connect(lp) }); perc(g, t, .01, v, d) };
  K.bell = (t, f, v = .06, d = 1.2, pan = 0) => { const g = out(.45, pan);[[1, 1], [2, .35], [3.01, .12]].forEach(([r, a]) => { const o = osc('sine', f * r, t, t + d + .1); const og = ctx.createGain(); og.gain.value = a; o.connect(og); og.connect(g) }); perc(g, t, .004, v, d) };
  K.whistle = (t, d = .35, v = .07) => { const g = out(.25), o = osc('sine', 2900, t, t + d + .05), lfo = osc('sine', 38, t, t + d + .05), lg = ctx.createGain(); lg.gain.value = 70; lfo.connect(lg); lg.connect(o.frequency); o.connect(g); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + .02); g.gain.setValueAtTime(v, t + d - .03); g.gain.linearRampToValueAtTime(0, t + d) };
  K.crowd = (t0, t1, v = .05, cut = 900) => { const g = out(.3), bp = filt('bandpass', cut, .6); bp.connect(g); noise(t0, t1 + .1).connect(bp); g.gain.setValueAtTime(0, t0); g.gain.linearRampToValueAtTime(v, t0 + .4); g.gain.setValueAtTime(v, t1 - .4); g.gain.linearRampToValueAtTime(0, t1) };
  K.groan = (t, v = .12) => { const g = out(.4), bp = filt('bandpass', 700, 1.2); bp.connect(g); noise(t, t + 1.1).connect(bp); bp.frequency.setValueAtTime(900, t); bp.frequency.exponentialRampToValueAtTime(320, t + .9); perc(g, t, .08, v, .9) };
  K.cheer = (t, v = .1) => { const g = out(.4), bp = filt('bandpass', 1400, .8); bp.connect(g); noise(t, t + 1.2).connect(bp); bp.frequency.setValueAtTime(800, t); bp.frequency.exponentialRampToValueAtTime(1800, t + .5); perc(g, t, .1, v, 1.0) };
  K.clack = (t, v = .25) => { const g = out(.2), hp = filt('highpass', 1200); hp.connect(g); noise(t, t + .08).connect(hp); perc(g, t, .001, v, .06); K.kick(t, .5, 90, 40, .3) };
  K.squeak = (t, d = .35, v = .05) => { const g = out(.1), bp = filt('bandpass', 2400, 6); bp.connect(g); noise(t, t + d + .05).connect(bp); bp.frequency.setValueAtTime(1800, t); bp.frequency.linearRampToValueAtTime(3200, t + d); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + .03); g.gain.setValueAtTime(v * .8, t + d - .05); g.gain.linearRampToValueAtTime(0, t + d) };
  K.whoosh = (t, d = .8, v = .17) => { const g = out(.25), bp = filt('bandpass', 400, 1.3); bp.connect(g); noise(t, t + d + .1).connect(bp); bp.frequency.setValueAtTime(250, t); bp.frequency.exponentialRampToValueAtTime(3200, t + d * .5); bp.frequency.exponentialRampToValueAtTime(600, t + d); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + d * .5); g.gain.exponentialRampToValueAtTime(.0001, t + d) };
  K.riser = (t0, t1, v = .12) => { const g = out(.3), bp = filt('bandpass', 300, 2); bp.connect(g); noise(t0, t1 + .05).connect(bp); bp.frequency.setValueAtTime(300, t0); bp.frequency.exponentialRampToValueAtTime(6000, t1); g.gain.setValueAtTime(.0001, t0); g.gain.exponentialRampToValueAtTime(v, t1 - .02); g.gain.linearRampToValueAtTime(0, t1 + .02) };
  K.impact = t => { K.kick(t, .9, 110, 30, 1.2); const g = out(.6), lp = filt('lowpass', 900); lp.connect(g); noise(t, t + 1).connect(lp); perc(g, t, .002, .2, .7) };
  K.tick = (t, v = .05) => { const g = out(0, .15), bp = filt('bandpass', 3600, 7); bp.connect(g); noise(t, t + .05).connect(bp); perc(g, t, .001, v, .03) };
  K.clock = (t, v = .1) => { const g = out(.05), bp = filt('bandpass', 2200, 9); bp.connect(g); noise(t, t + .05).connect(bp); perc(g, t, .001, v, .04); K.kick(t, .12, 400, 200, .05) };
  K.thump = (t, v = .5) => { K.kick(t, v, 110, 38, .5); const g = out(.3), lp = filt('lowpass', 600); lp.connect(g); noise(t, t + .3).connect(lp); perc(g, t, .002, .15, .2) };
  K.click = (t, v = .16) => { const g = out(.05), hp = filt('highpass', 1800); hp.connect(g); noise(t, t + .04).connect(hp); perc(g, t, .001, v, .018) };
  K.type = (t0, t1, v = .03) => { const r = rng(Math.round(t0 * 100)); for (let t = t0; t < t1; t += .045 + r() * .05) K.click(t, v * (.6 + .6 * r())) };
  K.blip = (t, f = 1500, v = .05, pan = 0) => { const g = out(.1, pan); osc('square', f, t, t + .06).connect(g); perc(g, t, .002, v, .04) };
  K.pop = (t, f = 700, v = .09) => { const g = out(.12), o = osc('sine', f, t, t + .15); o.frequency.setValueAtTime(f * .7, t); o.frequency.exponentialRampToValueAtTime(f * 1.6, t + .07); o.connect(g); perc(g, t, .003, v, .1) };
  K.success = (t, v = .08) => { K.bell(t, mf(81), v, 1.1, -.15); K.bell(t + .09, mf(88), v, 1.4, .15) };
  K.buzz = (t, v = .09) => { [0, .12].forEach((o, i) => { const g = out(.1), lp = filt('lowpass', 1200); lp.connect(g); osc('sawtooth', i ? 196 : 247, t + o, t + o + .2).connect(lp); perc(g, t + o, .005, v, .16) }) };
  K.endChord = t => { K.stab([48, 55, 60, 64, 67], t, .06, .8); K.crash(t, .07); K.pad([48, 55, 60, 64, 67, 71], t, t + 3, .012, 1500); K.sub(24, t, 3, .12);[72, 76, 79, 83, 86].forEach((m, i) => K.bell(t + .08 + i * .06, mf(m), .04, 2.6, (i - 2) * .2)) };
  return K;
}
async function renderAudio() {
  const sr = 44100, ctx = new OfflineAudioContext(2, Math.ceil(sr * window.DUR), sr);
  window.buildAudio(makeKit(ctx));
  return await ctx.startRendering();
}
function wavB64(buf) {
  const n = buf.length, L = buf.getChannelData(0), Rr = buf.getChannelData(1), sr = buf.sampleRate;
  const ab = new ArrayBuffer(44 + n * 4), v = new DataView(ab);
  const ws = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)) };
  ws(0, 'RIFF'); v.setUint32(4, 36 + n * 4, true); ws(8, 'WAVE'); ws(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 2, true); v.setUint32(24, sr, true); v.setUint32(28, sr * 4, true); v.setUint16(32, 4, true); v.setUint16(34, 16, true); ws(36, 'data'); v.setUint32(40, n * 4, true);
  for (let i = 0; i < n; i++) { v.setInt16(44 + i * 4, clamp(L[i], -1, 1) * 32767, true); v.setInt16(46 + i * 4, clamp(Rr[i], -1, 1) * 32767, true) }
  const u = new Uint8Array(ab); let s = ''; for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000));
  return btoa(s);
}
window.renderAudioB64 = async () => wavB64(await renderAudio());

// ---- seek / boot / preview (play com áudio, régua de tempo, zonas do Instagram) ----
async function seek(t) { pending.length = 0; for (const u of updaters) u(t); if (pending.length) await Promise.all(pending) }
window.seek = seek;
const isRender = location.search.includes('render');
if (isRender) document.body.classList.add('render');
// sobreposição das zonas cobertas pela interface do Instagram (só no preview vertical)
{ const s = div('', document.body); s.id = 'safe'; s.innerHTML = '' }
function fit() { if (isRender) return; const s = Math.min(innerWidth / W, (innerHeight - 50) / H); if (W > H) { stage.style.transform = `translate(${(innerWidth - W * s) / 2}px,0) scale(${s})`; return } stage.style.transform = `translate(${(innerWidth - W * s) / 2}px,0) scale(${s})`; const sf = document.getElementById('safe'); sf.innerHTML = `<div style="position:absolute;left:${(innerWidth - W * s) / 2}px;top:0;width:${W * s}px;height:${220 * s}px;background:rgba(255,0,0,.25)"></div><div style="position:absolute;left:${(innerWidth - W * s) / 2}px;top:${1500 * s}px;width:${W * s}px;height:${420 * s}px;background:rgba(255,0,0,.25)"></div><div style="position:absolute;left:${(innerWidth - W * s) / 2 + 940 * s}px;top:${1000 * s}px;width:${140 * s}px;height:${500 * s}px;background:rgba(255,0,0,.25)"></div>` }
async function boot() {
  if (!isRender) { const ui = div('', document.body); ui.id = 'ui'; ui.innerHTML = '<button id="play">▶ Play</button><input id="scrub" type="range" min="0" step="0.01" value="0"><span id="tc">0.00s</span><label><input type="checkbox" id="sz">zonas IG</label>' }
  addEventListener('resize', fit); fit();
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.decode().catch(() => { })));
  await Promise.all([...document.querySelectorAll('video')].map(v => v.readyState >= 1 ? 0 : new Promise(r => v.addEventListener('loadedmetadata', r, { once: true }))));
  if (window.onReady) window.onReady();
  await seek(0); window.__ready = true;
  if (isRender) return;
  const scrub = document.getElementById('scrub'), tc = document.getElementById('tc'), btn = document.getElementById('play');
  scrub.max = window.DUR; document.getElementById('sz').onchange = e => document.body.classList.toggle('safe', e.target.checked);
  let ac = null, abuf = null, src = null, t0 = 0, playing = false;
  const show = async t => { await seek(t); scrub.value = t; tc.textContent = t.toFixed(2) + 's' };
  scrub.oninput = () => { if (playing) stop(); show(+scrub.value) };
  function stop() { playing = false; window.__live = false; btn.textContent = '▶ Play'; if (src) { src.stop(); src = null } document.querySelectorAll('video').forEach(v => v.pause()) }
  btn.onclick = async () => {
    if (playing) return stop();
    btn.textContent = '…'; if (!abuf) abuf = await renderAudio(); if (!ac) ac = new AudioContext();
    let from = +scrub.value; if (from >= window.DUR - .05) from = 0;
    src = ac.createBufferSource(); src.buffer = abuf; src.connect(ac.destination); src.start(0, from); t0 = ac.currentTime - from; playing = true; window.__live = true; btn.textContent = '❚❚ Pause';
    const loop = () => { if (!playing) return; const t = ac.currentTime - t0; if (t >= window.DUR) { stop(); show(window.DUR); return } pending.length = 0; for (const u of updaters) u(t); scrub.value = t; tc.textContent = t.toFixed(2) + 's'; requestAnimationFrame(loop) }; loop();
  };
}
