#!/usr/bin/env python3
"""Grade de batidas: o motion corta no beat, e o beat vem da musica - ou a musica
e pedida no BPM que o roteiro precisa.

    batidas.py grade  --bpm 120 --dur 20 [--sub 2] [--offset 0.0]
        Imprime os instantes das batidas (e subdivisoes) para planejar cortes.

    batidas.py musica faixa.mp3 [--ini 0 --dur 30]
        Estima o BPM e o offset da primeira batida forte a partir do envelope
        de energia (autocorrelacao dos onsets). Sem numpy: so ffmpeg e stdlib.

    batidas.py alinhar roteiro.json --bpm 120 [--offset 0.0] [--sub 2] [--out roteiro.json]
        Puxa cada `t` e `fim` das linhas, fundos e paineis para a batida mais
        proxima. E o que faz o texto "cair" no beat.

    batidas.py cortes --bpm 120 --dur 20 "4,2,2,4,2,2,4"
        Converte uma lista de duracoes em batidas para tempos de corte absolutos.
"""
import argparse, json, math, os, re, subprocess, sys

FF = os.environ.get("FFMPEG") or ("ffmpeg" if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0 else "./ffmpeg")


def grade(bpm, dur, sub=1, offset=0.0):
    passo = 60.0 / bpm / sub
    t, out = offset, []
    while t <= dur + 1e-6:
        out.append(round(t, 3)); t += passo
    return out


def envelope(faixa, ini, dur, hz=50):
    """RMS em janelas de 1/hz s, via astats."""
    n = int(48000 / hz)
    s = subprocess.run([FF, "-v", "error", "-ss", str(ini), "-t", str(dur), "-i", faixa,
                        "-af", f"aformat=channel_layouts=mono,aresample=48000,"
                               f"astats=metadata=1:reset={n},ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
                        "-f", "null", "-"], capture_output=True, text=True).stdout
    vals = []
    for m in re.finditer(r"RMS_level=(-?[\d.]+|-inf)", s):
        v = m.group(1)
        vals.append(-90.0 if v == "-inf" else float(v))
    return vals


def onsets(env):
    """Diferenca positiva do envelope (subida de energia) = onset."""
    lin = [10 ** (v / 20) for v in env]
    d = [max(0.0, lin[i] - lin[i - 1]) for i in range(1, len(lin))]
    m = max(d) or 1.0
    return [x / m for x in d]


def bpm_por_autocorrelacao(on, hz=50, lo=70, hi=180):
    n = len(on)
    med = sum(on) / n
    x = [v - med for v in on]
    melhor, melhor_lag = -1, None
    for lag in range(int(hz * 60 / hi), int(hz * 60 / lo) + 1):
        s = sum(x[i] * x[i - lag] for i in range(lag, n))
        if s > melhor:
            melhor, melhor_lag = s, lag
    return 60.0 * hz / melhor_lag, melhor_lag


def offset_da_grade(on, lag):
    """Fase da grade que casa com mais onsets fortes."""
    melhor, melhor_ph = -1, 0
    for ph in range(lag):
        s = sum(on[i] for i in range(ph, len(on), lag))
        if s > melhor:
            melhor, melhor_ph = s, ph
    return melhor_ph


def cmd_musica(a):
    hz = 50
    env = envelope(a.faixa, a.ini, a.dur, hz)
    if len(env) < hz * 4:
        sys.exit("faixa curta demais para medir")
    on = onsets(env)
    bpm, lag = bpm_por_autocorrelacao(on, hz)
    ph = offset_da_grade(on, lag)
    off = a.ini + ph / hz
    print(f"{os.path.basename(a.faixa)}: ~{bpm:.1f} BPM  (batida = {60/bpm:.3f}s)  primeira batida forte em {off:.2f}s")
    print(f"  grade: batidas.py grade --bpm {bpm:.1f} --offset {off:.2f} --dur {a.dur}")
    print("  confira de ouvido: toque a faixa junto com efeitos.sh timeline 'clique@t' nas batidas.")


def cmd_grade(a):
    g = grade(a.bpm, a.dur, a.sub, a.offset)
    passo = 60 / a.bpm
    print(f"BPM {a.bpm}: batida {passo:.3f}s | compasso de 4 = {4*passo:.2f}s | 2 compassos = {8*passo:.2f}s")
    for i, t in enumerate(g):
        marca = "  <- compasso" if a.sub and (i % (4 * a.sub)) == 0 else ""
        print(f"  {t:6.2f}{marca}")


def cmd_cortes(a):
    passo = 60 / a.bpm
    t, out = a.offset, []
    for b in [float(x) for x in a.lista.split(",")]:
        out.append((round(t, 3), round(t + b * passo, 3), b)); t += b * passo
    print(" plano   inicio     fim   batidas  duracao")
    for n, (i, f, b) in enumerate(out, 1):
        print(f"  {n:2d}    {i:6.2f}  {f:6.2f}   {b:5.1f}   {f-i:5.2f}s")
    print(f"total {t:.2f}s" + (f"  (roteiro pede {a.dur}s)" if a.dur else ""))
    # duracoes que o Omni entrega: 4, 6, 8, 10
    for n, (i, f, b) in enumerate(out, 1):
        d = f - i
        opc = min((4, 6, 8, 10), key=lambda o: (o < d, abs(o - d)))
        if d > 10:
            print(f"  plano {n}: {d:.1f}s > 10s - dividir em dois clipes ou usar --continua")
        elif opc - d > 0.05:
            print(f"  plano {n}: pedir {opc}s ao Omni e cortar em {d:.2f}s (montar.sh cortar)")


def snap(t, bpm, sub, offset):
    passo = 60 / bpm / sub
    return round(offset + round((t - offset) / passo) * passo, 3)


def cmd_alinhar(a):
    d = json.load(open(a.roteiro))
    for L in d.get("linhas", []):
        for k in ("t", "fim"):
            if k in L:
                L[k] = snap(float(L[k]), a.bpm, a.sub, a.offset)
    for k in ("fundos", "paineis"):
        for x in d.get(k, []):
            x["t"] = snap(float(x["t"]), a.bpm, a.sub, a.offset)
    out = a.out or a.roteiro
    json.dump(d, open(out, "w"), indent=1, ensure_ascii=False)
    print(f"-> {out} (alinhado a {a.bpm} BPM, sub {a.sub}, offset {a.offset})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(add_help=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("grade"); p.add_argument("--bpm", type=float, required=True)
    p.add_argument("--dur", type=float, required=True); p.add_argument("--sub", type=int, default=1)
    p.add_argument("--offset", type=float, default=0.0); p.set_defaults(fn=cmd_grade)
    p = sub.add_parser("musica"); p.add_argument("faixa"); p.add_argument("--ini", type=float, default=0.0)
    p.add_argument("--dur", type=float, default=30.0); p.set_defaults(fn=cmd_musica)
    p = sub.add_parser("alinhar"); p.add_argument("roteiro"); p.add_argument("--bpm", type=float, required=True)
    p.add_argument("--offset", type=float, default=0.0); p.add_argument("--sub", type=int, default=2)
    p.add_argument("--out"); p.set_defaults(fn=cmd_alinhar)
    p = sub.add_parser("cortes"); p.add_argument("lista"); p.add_argument("--bpm", type=float, required=True)
    p.add_argument("--dur", type=float); p.add_argument("--offset", type=float, default=0.0)
    p.set_defaults(fn=cmd_cortes)
    a = ap.parse_args(); a.fn(a)
