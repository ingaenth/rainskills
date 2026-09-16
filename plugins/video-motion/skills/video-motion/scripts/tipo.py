#!/usr/bin/env python3
"""Tipografia cinetica exata, em pos, via libass (filtro `ass` do ffmpeg).

Cada letra sai como foi escrita - o modelo de video nao e chamado. O roteiro e
um JSON com fundo(s), painel(is) de transicao e linhas de texto, cada uma com
um instante de entrada, um efeito e (opcionalmente) uma saida.

    tipo.py render roteiro.json --out tipo.mp4 [--base clipe.mp4] [--fontes ./fontes]
    tipo.py ass    roteiro.json --out tipo.ass          so o arquivo .ass, para montar.sh
    tipo.py fundo  roteiro.json --out fundo.mp4         so fundo + paineis, sem texto
    tipo.py exemplo > roteiro.json                      modelo de roteiro comentado

Roteiro:
{
 "w": 1280, "h": 720, "fps": 30, "dur": 6,
 "fonte": "Liberation Sans Narrow", "peso": "bold",
 "fundos":  [{"t": 0, "cor": "#00E000"}, {"t": 3.0, "cor": "#0A4A0A"}],
 "paineis": [{"t": 2.9, "dur": 0.25, "cor": "#0A4A0A", "de": "esq"}],
 "linhas": [
  {"texto": "ESTAMOS", "t": 0.0, "fim": 6, "efeito": "pop",   "x": 640, "y": 220, "corpo": 150, "cor": "#1C1A20"},
  {"texto": "DE CARA", "t": 0.6,           "efeito": "slide-esq", "y": 360, "cor": "#80FF80"},
  {"texto": "NOVA",    "t": 1.2,           "efeito": "queda",     "y": 500, "saida": "cima", "fim": 4.0}
 ]
}

Efeitos de entrada: pop, slide-esq, slide-dir, slide-cima, slide-baixo, queda,
maquina (letra a letra), fade, rolo (letreiro gigante atravessando), corte (sem
animacao). Saidas: fade, cima, baixo, esq, dir, encolhe. Campos herdados da linha
anterior quando omitidos: x, y, corpo, cor, fim, alinhamento (fonte e peso vem
sempre do topo do roteiro ou da propria linha).
`alinh`: 5 centro (padrao), 4 esquerda, 6 direita (numeracao ASS).
"""
import argparse, json, os, subprocess, sys

FF = os.environ.get("FFMPEG") or ("ffmpeg" if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0 else "./ffmpeg")

EXEMPLO = __doc__.split("Roteiro:")[1].split("Efeitos")[0].strip()


def cor_ass(hexcor, alpha=0):
    """#RRGGBB -> &HAABBGGRR"""
    c = hexcor.lstrip("#")
    if len(c) == 3:
        c = "".join(x * 2 for x in c)
    r, g, b = c[0:2], c[2:4], c[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper()


def ts(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def esc(txt):
    return txt.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", "\\N")


def ms(seg):
    return int(round(seg * 1000))


class Roteiro:
    def __init__(self, d):
        self.w = d.get("w", 1280); self.h = d.get("h", 720)
        self.fps = d.get("fps", 30); self.dur = d.get("dur", 6)
        self.fonte = d.get("fonte", "Liberation Sans Narrow")
        self.peso = d.get("peso", "bold")
        self.fundos = sorted(d.get("fundos", [{"t": 0, "cor": "#000000"}]), key=lambda f: f["t"])
        self.paineis = d.get("paineis", [])
        self.linhas = d.get("linhas", [])
        self.pausa = d.get("pausa_pop", 0.18)

    # ---------- ASS ----------
    def estilos(self):
        vistos, out = set(), []
        for L in self._linhas():
            k = (L["fonte"], L["corpo"], L["cor"], L["peso"], L["alinh"], L.get("italico", False))
            if k in vistos:
                continue
            vistos.add(k)
            nome = self._nome_estilo(k)
            bold = -1 if str(L["peso"]).lower() in ("bold", "black", "heavy", "negrito") else 0
            it = -1 if L.get("italico") else 0
            # SecondaryColour transparente: e o que faz o efeito "maquina" (\k) revelar letra a letra
            out.append(f"Style: {nome},{L['fonte']},{L['corpo']},{cor_ass(L['cor'])},{cor_ass(L['cor'],255)},"
                       f"&H00000000,&H80000000,{bold},{it},0,0,100,100,{L.get('espaco',0)},0,1,"
                       f"{L.get('contorno',0)},{L.get('sombra',0)},{L['alinh']},0,0,0,1")
        return out

    @staticmethod
    def _nome_estilo(k):
        return "S" + str(abs(hash(k)) % 10**8)

    def _linhas(self):
        base = {"x": self.w // 2, "y": self.h // 2, "corpo": int(self.h * 0.18), "cor": "#FFFFFF",
                "fonte": self.fonte, "peso": self.peso, "fim": self.dur, "alinh": 5, "efeito": "pop"}
        out = []
        for L in self.linhas:
            cur = dict(base); cur.update(L)
            out.append(cur)
            # fonte e peso NAO sao herdados: uma linha de apoio em regular mudava o titulo seguinte
            for k in ("x", "y", "corpo", "cor", "fim", "alinh"):
                base[k] = cur[k]
        return out

    def eventos(self):
        ev = []
        for n, L in enumerate(self._linhas()):
            st = self._nome_estilo((L["fonte"], L["corpo"], L["cor"], L["peso"], L["alinh"], L.get("italico", False)))
            t0, t1 = float(L["t"]), float(L["fim"])
            x, y = L["x"], L["y"]
            txt = esc(L["texto"])
            ent = L.get("efeito", "pop"); sai = L.get("saida")
            dur_ent = float(L.get("dur_ent", 0.28)); dur_sai = float(L.get("dur_sai", 0.25))
            layer = 10 + n
            fim_ent = t1 - dur_sai if sai else t1
            tag_sai = ""
            # --- entrada ---
            if ent == "pop":
                a, b = ms(dur_ent * 0.6), ms(dur_ent)
                tag = f"\\pos({x},{y})\\fscx0\\fscy0\\t(0,{a},\\fscx116\\fscy116)\\t({a},{b},\\fscx100\\fscy100)"
                ev.append(self._ev(layer, t0, fim_ent, st, tag, txt))
            elif ent.startswith("slide-") or ent == "queda":
                lado = "cima" if ent == "queda" else ent.split("-")[1]
                off = {"esq": (-self.w * 0.6, 0), "dir": (self.w * 0.6, 0),
                       "cima": (0, -self.h * 0.7), "baixo": (0, self.h * 0.7)}[lado]
                ov = 0.06 if ent != "queda" else 0.10   # overshoot
                x0, y0 = x + off[0], y + off[1]
                xo, yo = x - off[0] * ov, y - off[1] * ov
                a = ms(dur_ent * 0.7)
                ev.append(self._ev(layer, t0, t0 + dur_ent * 0.7, st,
                                   f"\\move({x0:.0f},{y0:.0f},{xo:.0f},{yo:.0f},0,{a})", txt))
                b = ms(dur_ent * 0.3)
                ev.append(self._ev(layer, t0 + dur_ent * 0.7, t0 + dur_ent, st,
                                   f"\\move({xo:.0f},{yo:.0f},{x},{y},0,{b})", txt))
                ev.append(self._ev(layer, t0 + dur_ent, fim_ent, st, f"\\pos({x},{y})", txt))
            elif ent == "maquina":
                por = ms(float(L.get("por_letra", 0.06))) // 10   # centesimos
                k = "".join(f"{{\\k{por}}}{esc(c)}" for c in L["texto"])
                ev.append(self._ev(layer, t0, fim_ent, st, f"\\pos({x},{y})", k))
            elif ent == "fade":
                ev.append(self._ev(layer, t0, fim_ent, st, f"\\pos({x},{y})\\fad({ms(dur_ent)},0)", txt))
            elif ent == "rolo":
                # letreiro gigante atravessando de direita para esquerda em `fim - t`
                larg = L.get("largura_texto", len(L["texto"]) * L["corpo"] * 0.62)
                x0, x1 = self.w + larg / 2, -larg / 2
                ev.append(self._ev(layer, t0, t1, st, f"\\move({x0:.0f},{y},{x1:.0f},{y},0,{ms(t1 - t0)})", txt))
                continue
            else:  # corte
                ev.append(self._ev(layer, t0, fim_ent, st, f"\\pos({x},{y})", txt))
            # --- saida ---
            if sai:
                d = ms(dur_sai)
                if sai == "fade":
                    tag = f"\\pos({x},{y})\\fad(0,{d})"
                elif sai == "encolhe":
                    tag = f"\\pos({x},{y})\\t(0,{d},\\fscx0\\fscy0)"
                else:
                    off = {"esq": (-self.w * 0.6, 0), "dir": (self.w * 0.6, 0),
                           "cima": (0, -self.h * 0.7), "baixo": (0, self.h * 0.7)}[sai]
                    tag = f"\\move({x},{y},{x + off[0]:.0f},{y + off[1]:.0f},0,{d})"
                ev.append(self._ev(layer, fim_ent, t1, st, tag, txt))
        return ev

    @staticmethod
    def _ev(layer, a, b, st, tag, txt):
        return f"Dialogue: {layer},{ts(a)},{ts(b)},{st},,0,0,0,,{{{tag}}}{txt}"

    def ass(self):
        cab = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {self.w}", f"PlayResY: {self.h}",
               "WrapStyle: 2", "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
               "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
               "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
               "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"]
        return "\n".join(cab + self.estilos() + ["", "[Events]",
                "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
                + self.eventos()) + "\n"

    # ---------- fundo: cores por corte + paineis ----------
    def filtro_fundo(self):
        """drawbox pinta o quadro inteiro a partir de cada corte; painel e um overlay deslizante."""
        f = []
        for fd in self.fundos[1:]:
            c = fd["cor"].lstrip("#")
            f.append(f"drawbox=c=0x{c}:t=fill:enable='gte(t,{fd['t']})'")
        return ",".join(f)

    def entradas_paineis(self):
        ent, filt = [], []
        for n, p in enumerate(self.paineis):
            c = p["cor"].lstrip("#"); t0 = p["t"]; d = p.get("dur", 0.25); de = p.get("de", "esq")
            ent += ["-f", "lavfi", "-i", f"color=c=0x{c}:s={self.w}x{self.h}:r={self.fps}"]
            prog = f"min(1,max(0,(t-{t0})/{d}))"
            if de == "esq":
                x, y = f"-W+W*{prog}", "0"
            elif de == "dir":
                x, y = f"W-W*{prog}", "0"
            elif de == "cima":
                x, y = "0", f"-H+H*{prog}"
            else:
                x, y = "0", f"H-H*{prog}"
            fim = p.get("ate", t0 + d + 0.05)
            filt.append((x, y, t0, fim))
        return ent, filt


def montar_comando(r, base, saida, fontes, com_texto=True, ass_path=None):
    ent = []
    if base:
        ent += ["-i", base]
    else:
        c0 = r.fundos[0]["cor"].lstrip("#")
        ent += ["-f", "lavfi", "-i", f"color=c=0x{c0}:s={r.w}x{r.h}:r={r.fps}:d={r.dur}"]
    pen, pfilt = r.entradas_paineis()
    ent += pen
    cadeia = "[0:v]"
    fb = r.filtro_fundo()
    passos = []
    if fb and not base:
        passos.append(f"{cadeia}{fb}[b0]"); cadeia = "[b0]"
    elif not base:
        passos.append(f"{cadeia}null[b0]"); cadeia = "[b0]"
    else:
        passos.append(f"{cadeia}scale={r.w}:{r.h},setsar=1[b0]"); cadeia = "[b0]"
    for n, (x, y, t0, fim) in enumerate(pfilt):
        passos.append(f"{cadeia}[{n+1}:v]overlay=x='{x}':y='{y}':enable='between(t,{t0},{fim})'[p{n}]")
        cadeia = f"[p{n}]"
    if com_texto:
        fd = f":fontsdir={fontes}" if fontes else ""
        passos.append(f"{cadeia}ass={ass_path}{fd}[v]")
    else:
        passos.append(f"{cadeia}null[v]")
    return [FF, "-y", "-v", "error"] + ent + ["-filter_complex", ";".join(passos), "-map", "[v]",
            "-t", str(r.dur), "-r", str(r.fps), "-c:v", "libx264", "-crf", "17", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-an", saida]


def main():
    ap = argparse.ArgumentParser(add_help=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nome in ("render", "ass", "fundo"):
        p = sub.add_parser(nome); p.add_argument("roteiro"); p.add_argument("--out", required=True)
        p.add_argument("--base"); p.add_argument("--fontes")
    sub.add_parser("exemplo")
    a = ap.parse_args()
    if a.cmd == "exemplo":
        print(EXEMPLO); return
    r = Roteiro(json.load(open(a.roteiro)))
    if a.cmd == "ass":
        open(a.out, "w").write(r.ass()); print(f"-> {a.out}"); return
    ass_path = os.path.splitext(a.out)[0] + ".ass"
    open(ass_path, "w").write(r.ass())
    cmd = montar_comando(r, a.base, a.out, a.fontes, com_texto=(a.cmd == "render"), ass_path=ass_path)
    subprocess.run(cmd, check=True)
    print(f"-> {a.out}  ({ass_path})")


if __name__ == "__main__":
    main()
