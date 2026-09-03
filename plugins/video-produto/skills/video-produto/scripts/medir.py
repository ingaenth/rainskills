#!/usr/bin/env python3
"""Medicoes do pipeline. Nada aqui e estimado - tudo sai do arquivo.

    medir.py boca   <video.mp4> <voz.wav> [--crop L:A:X:Y]
        Cruza o movimento real dos labios com as janelas em que a narracao toca.
        Lista os trechos em que a voz corre com a boca parada.

    medir.py frases <voz.wav>
        Inicio e fim reais de cada frase, para cravar os cartoes 0,15s depois.

    medir.py musica <faixa.mp3> [--dur 32]
        Amostra a energia ao longo da faixa: menor variacao serve de cama neutra,
        maior crescimento serve de tensao dramatica.

    medir.py elenco <video.mp4> [--n 8]
        Extrai frames ao longo do filme para conferir a contagem de personagens.
"""
import argparse, os, re, subprocess, sys, tempfile

FF = "ffmpeg" if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0 \
     else "./ffmpeg"


def _ff(args):
    return subprocess.run([FF] + args, capture_output=True, text=True).stderr


def duracao(f):
    s = _ff(["-i", f])
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', s)
    h, mi, sg = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(sg)


def janelas_fala(wav, limiar="-38dB", minimo="0.20"):
    """Trechos com som, deduzidos das pausas."""
    s = _ff(["-i", wav, "-af", f"silencedetect=n={limiar}:d={minimo}", "-f", "null", "-"])
    ev = [(float(m.group(2)), m.group(1))
          for m in re.finditer(r'silence_(start|end): ([0-9.]+)', s)]
    dur, fala, cur = duracao(wav), [], 0.0
    for t, k in ev:
        if k == "start" and t > cur + 0.05:
            fala.append((cur, t))
        elif k == "end":
            cur = t
    if cur < dur - 0.05:
        fala.append((cur, dur))
    return fala


def cmd_frases(a):
    f = janelas_fala(a.voz)
    print(f"{len(f)} frases em {duracao(a.voz):.2f}s\n")
    print("  #   inicio    fim   dur   cartao entra")
    for n, (i, j) in enumerate(f, 1):
        print(f" {n:2d}  {i:6.2f}  {j:6.2f}  {j-i:5.2f}   {i+0.15:6.2f}")


def cmd_boca(a):
    with tempfile.TemporaryDirectory() as d:
        raw = os.path.join(d, "b.raw")
        subprocess.run([FF, "-y", "-v", "error", "-i", a.video, "-vf",
                        f"crop={a.crop},format=gray,scale=32:32,fps=12",
                        "-f", "rawvideo", raw], check=True)
        b = open(raw, "rb").read()
    n, mov, prev = 32 * 32, [], None
    for i in range(len(b) // n):
        f = b[i * n:(i + 1) * n]
        if prev is not None:
            mov.append(sum(abs(x - y) for x, y in zip(f, prev)) / n)
        prev = f

    voz = janelas_fala(a.voz)
    falando = lambda t: any(i <= t <= j for i, j in voz)
    ruins, cur = [], None
    for i in range(0, len(mov), 6):
        w = mov[i:i + 6]
        v = sum(w) / len(w)
        t = (i + 1) / 12
        mal = falando(t) and v < a.limiar
        if mal and cur is None:
            cur = t
        if not mal and cur is not None:
            ruins.append((cur, t)); cur = None
    if cur is not None:
        ruins.append((cur, len(mov) / 12))

    print(f"narracao em {len(voz)} blocos; movimento medido em {len(mov)} frames\n")
    graves = [(i, j) for i, j in ruins if j - i >= 1.0]
    for i, j in ruins:
        tag = "  <== CORRIGIR" if j - i >= 1.0 else "  ok, pausa natural"
        print(f"  {i:6.2f} -> {j:6.2f}  ({j-i:4.1f}s){tag}")
    if graves:
        print("\ncorte para detalhe nestes trechos, com um objeto que a frase cite:")
        for i, j in graves:
            print(f"  cortar.sh {a.video} {i:.2f} {j:.2f} <L:A:X:Y> saida.mp4")
    else:
        print("\nnenhum descompasso relevante.")


def cmd_musica(a):
    dur = duracao(a.faixa)
    print(f"{os.path.basename(a.faixa)} - {dur:.0f}s\n")
    print(" inicio   media    pico   variacao   crescimento")
    for ss in range(10, int(dur - a.dur), max(20, int(a.dur))):
        vals = []
        for off in (0, a.dur / 2):
            s = _ff(["-ss", str(ss + off), "-t", str(a.dur / 2), "-i", a.faixa,
                     "-af", "volumedetect", "-f", "null", "-"])
            mn = float(re.search(r'mean_volume: ([-0-9.]+)', s).group(1))
            mx = float(re.search(r'max_volume: ([-0-9.]+)', s).group(1))
            vals.append((mn, mx))
        (m1, x1), (m2, x2) = vals
        print(f"  {ss:5d}s  {(m1+m2)/2:6.1f}  {max(x1,x2):6.1f}   "
              f"{max(x1,x2)-(m1+m2)/2:6.1f}     {m2-m1:+6.1f} dB")
    print("\ncama neutra: menor variacao | tensao dramatica: maior crescimento")


def cmd_elenco(a):
    dur = duracao(a.video)
    passo = dur / (a.n + 1)
    saidas = []
    for k in range(1, a.n + 1):
        t = passo * k
        out = f"elenco_{t:05.1f}.png"
        subprocess.run([FF, "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", a.video,
                        "-frames:v", "1", "-vf", "scale=640:-1", out], check=True)
        saidas.append(out)
    print("\n".join(saidas))
    print("\nabra os frames e conte os personagens; devem ser sempre os mesmos.",
          file=sys.stderr)


def cmd_balanco(a):
    """Voz contra cama, ANTES do loudnorm. Medir depois nao serve:
    o loudnorm normaliza tudo e apaga justamente a diferenca."""
    import tempfile, re
    d = tempfile.mkdtemp()
    voz, mus, fx, amb = a.voz, a.musica, a.efeitos, a.ambiencia
    pv = os.path.join(d, "v.wav"); pc = os.path.join(d, "c.wav")
    subprocess.run([FF, "-y", "-v", "error", "-i", voz, "-af", "volume=1.7", pv])
    subprocess.run([FF, "-y", "-v", "error", "-i", voz, "-i", mus, "-i", fx,
        "-i", amb, "-filter_complex",
        "[0]volume=1.7,asplit=2[k1][k2];[1]volume=0.30[m];[2]volume=0.85[f];"
        "[3]volume=0.10[b];"
        "[m][k1]sidechaincompress=threshold=0.045:ratio=5:attack=40:release=550[md];"
        "[b][k2]sidechaincompress=threshold=0.04:ratio=8:attack=20:release=400[ad];"
        "[md][ad][f]amix=inputs=3:normalize=0[o]", "-map", "[o]", pc])

    def nivel(arq, ini, dur):
        out = subprocess.run([FF, "-hide_banner", "-ss", str(ini), "-t", str(dur),
                              "-i", arq, "-af", "volumedetect", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        m = re.search(r"mean_volume: (-?[\d.]+) dB", out)
        return float(m.group(1)) if m else None

    print("\n janela      voz      cama    diferenca")
    ruim = 0
    for ini in [float(x) for x in a.janelas.split(",")]:
        v = nivel(pv, ini, 3); c = nivel(pc, ini, 3)
        if v is None or c is None:
            continue
        dif = v - c
        marca = "  <== VOZ ABAFADA" if dif < 8 else ""
        if dif < 8:
            ruim += 1
        print(f"  {ini:5.1f}s  {v:7.1f}  {c:8.1f}  {dif:8.1f} dB{marca}")
    print("\nalvo: voz 10 a 15 dB acima da cama durante a fala")
    if ruim:
        print(f"{ruim} janela(s) com a cama por cima da voz — baixe a musica")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(add_help=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("boca"); p.add_argument("video"); p.add_argument("voz")
    p.add_argument("--crop", default="520:300:380:60"); p.add_argument("--limiar", type=float, default=1.6)
    p.set_defaults(fn=cmd_boca)
    p = sub.add_parser("frases"); p.add_argument("voz"); p.set_defaults(fn=cmd_frases)
    p = sub.add_parser("musica"); p.add_argument("faixa"); p.add_argument("--dur", type=float, default=32)
    p.set_defaults(fn=cmd_musica)
    p = sub.add_parser("elenco"); p.add_argument("video"); p.add_argument("--n", type=int, default=8)
    p.set_defaults(fn=cmd_elenco)
    p = sub.add_parser("balanco"); p.add_argument("voz"); p.add_argument("musica")
    p.add_argument("efeitos"); p.add_argument("ambiencia")
    p.add_argument("--janelas", default="5,18,26"); p.set_defaults(fn=cmd_balanco)
    a = ap.parse_args()
    a.fn(a)
