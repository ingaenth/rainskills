#!/usr/bin/env python3
"""Cartelas tipograficas em PNG transparente, para compor sobre o video.

Use quando a frase precisa sair perfeita: modelo de imagem erra letra em texto
corrido (visto: "piloot" no lugar de "piloto"). Logo e palavra unica costumam
sair certas pelo modelo; frase, nao.

    cartela.py texto "Implante em minutos" --marca marca.json --out c1.png
              [--fonte X.ttf] [--corpo 64] [--cor "#FFFFFF"] [--pos centro|esq|dir]
              [--fonte-info "Fonte: TCU, 2026"] [--largura 1280] [--altura 720]

    cartela.py fecho --marca marca.json --logo logo.png --out fecho.png
              [--claim "..."] [--cta "..."] [--url "..."]
"""
import argparse, json, os, subprocess, sys

FF = "ffmpeg" if subprocess.run(["which","ffmpeg"],capture_output=True).returncode==0 else "./ffmpeg"
PADRAO = "/System/Library/Fonts/Helvetica.ttc"


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace("%", "\\%")


def draw(txt, fonte, corpo, cor, x, y, alpha=1.0):
    return (f"drawtext=fontfile={fonte}:text='{esc(txt)}':fontsize={corpo}:"
            f"fontcolor={cor}@{alpha}:x={x}:y={y}:expansion=none:"
            f"shadowcolor=black@0.45:shadowx=2:shadowy=2")


def render(filtros, w, h, out):
    subprocess.run([FF, "-y", "-v", "error", "-f", "lavfi",
                    "-i", f"color=c=black@0.0:s={w}x{h},format=rgba",
                    "-vf", ",".join(filtros), "-frames:v", "1",
                    "-pix_fmt", "rgba", out], check=True)
    print(f"-> {out}")


def kit(p):
    return json.load(open(p)) if p and os.path.exists(p) else {}


def fonte_de(a, k):
    return a.fonte or k.get("fonte") or PADRAO


def cmd_texto(a):
    k = kit(a.marca); f = fonte_de(a, k)
    x = {"centro": "(w-tw)/2", "esq": "w*0.08", "dir": "w-tw-w*0.08"}[a.pos]
    fs = [draw(a.texto, f, a.corpo, a.cor, x, "(h-th)/2")]
    if a.fonte_info:
        fs.append(draw(a.fonte_info, f, max(16, a.corpo // 4), a.cor, x,
                       f"(h-th)/2+{int(a.corpo*1.5)}", 0.55))
    render(fs, a.largura, a.altura, a.out)


def cmd_fecho(a):
    k = kit(a.marca); f = fonte_de(a, k)
    w, h = a.largura, a.altura
    claim = a.claim or k.get("claim"); cta = a.cta or k.get("cta"); url = a.url or k.get("url_marca")
    fs, y = [], int(h * 0.52)
    if claim:
        fs.append(draw(claim, f, int(h*0.062), a.cor, "(w-tw)/2", str(y))); y += int(h*0.105)
    if cta:
        fs.append(draw(cta.upper(), f, int(h*0.030), k.get("primaria", "#FFFFFF"),
                       "(w-tw)/2", str(y))); y += int(h*0.062)
    if url:
        fs.append(draw(url, f, int(h*0.026), a.cor, "(w-tw)/2", str(y), 0.6))
    if not fs:
        sys.exit("nada para escrever: passe --claim, --cta ou --url")
    render(fs, w, h, a.out)
    if a.logo:
        # ffmpeg nao le e escreve o mesmo arquivo: passe por um temporario
        alvo = int(h * 0.11)
        tmp = a.out + ".tmp.png"
        os.replace(a.out, tmp)
        subprocess.run([FF, "-y", "-v", "error", "-i", tmp, "-i", a.logo,
                        "-filter_complex",
                        f"[1]scale=-1:{alvo}[l];[0][l]overlay=(W-w)/2:{int(h*0.30)}",
                        "-frames:v", "1", "-pix_fmt", "rgba", a.out], check=True)
        os.remove(tmp)
        print(f"   logo composta em {a.out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(add_help=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nome in ("texto", "fecho"):
        p = sub.add_parser(nome)
        if nome == "texto":
            p.add_argument("texto"); p.add_argument("--corpo", type=int, default=64)
            p.add_argument("--pos", default="centro", choices=["centro","esq","dir"])
            p.add_argument("--fonte-info"); p.set_defaults(fn=cmd_texto)
        else:
            p.add_argument("--claim"); p.add_argument("--cta"); p.add_argument("--url")
            p.add_argument("--logo"); p.set_defaults(fn=cmd_fecho)
        p.add_argument("--marca", default="marca.json"); p.add_argument("--fonte")
        p.add_argument("--cor", default="#FFFFFF"); p.add_argument("--out", required=True)
        p.add_argument("--largura", type=int, default=1280); p.add_argument("--altura", type=int, default=720)
    a = ap.parse_args(); a.fn(a)
