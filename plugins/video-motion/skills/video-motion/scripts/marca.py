#!/usr/bin/env python3
"""Kit de marca: prepara e sobe as imagens de referencia que a IA vai usar.

    marca.py kit --logo logo.png [--tela shot1.png --tela shot2.png]
                 [--estilo ref.jpg] [--primaria "#0B5FFF"] [--fundo "#0B0D10"]
                 [--out marca.json]
        Apara, normaliza e faz upload de tudo. Devolve marca.json com as URLs
        ja na ordem em que viram @image1, @image2, ... no prompt.

    marca.py prompt <marca.json>
        Imprime o bloco de referencias pronto para colar no inicio do prompt.

    marca.py conferir <quadro.png> <marca.json> [--regiao x,y,w,h]
        Recorta a regiao onde a logo saiu e monta um comparativo com o original,
        para julgar de olho se as formas das letras se mantiveram.

    marca.py contraste <cor1> <cor2>
        Razao WCAG entre duas cores. Texto pede 4.5:1.

    marca.py paleta "#F9A03F,#F1602E,#2DBECD,#1C1A20" [--out paleta.png]
        Monta a imagem de amostras de cor (sem texto) e sobe. E assim que a cor
        exata entra no Omni: CODIGO HEX NO PROMPT VIRA TEXTO NA TELA (testado).

Sem dependencia externa: so ffmpeg e a biblioteca padrao.
"""
import argparse, base64, json, os, re, subprocess, sys, tempfile, urllib.request

FF = "ffmpeg" if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0 \
     else "./ffmpeg"
UPLOAD = "https://kieai.redpandaai.co/api/file-base64-upload"
UA = "Mozilla/5.0"


def chave():
    k = os.environ.get("KIE_KEY")
    if k:
        return k.strip()
    p = os.path.expanduser("~/.config/kie/key")
    if os.path.exists(p):
        return open(p).read().strip()
    sys.exit("KIE_KEY nao definida (env ou ~/.config/kie/key)")


def _ff(args):
    return subprocess.run([FF] + args, capture_output=True, text=True).stderr


def dimensoes(img):
    m = re.search(r'(\d{2,5})x(\d{2,5})', _ff(["-i", img]))
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def tem_alpha(img):
    return bool(re.search(r'(rgba|argb|pal8|ya8)', _ff(["-i", img])))


def hexrgb(c):
    c = c.strip().lstrip("#")
    if len(c) == 3:
        c = "".join(x * 2 for x in c)
    if not re.fullmatch(r'[0-9a-fA-F]{6}', c):
        sys.exit(f"cor invalida: {c}")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def nome_cor(hexcor):
    """Nome aproximado da cor, para o prompt do Omni (hex no prompt vira texto na tela)."""
    r, g, b = (x / 255 for x in hexrgb(hexcor))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    d = mx - mn
    if d < 0.08:
        return "near-black" if l < 0.15 else "dark grey" if l < 0.4 else "light grey" if l < 0.85 else "off-white"
    s_ = d / (1 - abs(2 * l - 1))
    h = (60 * (((g - b) / d) % 6) if mx == r else 60 * ((b - r) / d + 2) if mx == g else 60 * ((r - g) / d + 4)) % 360
    nome = ("red" if h < 12 or h >= 345 else "orange" if h < 26 else "amber" if h < 50 else
            "yellow" if h < 68 else "lime" if h < 90 else "green" if h < 160 else "teal" if h < 190 else
            "cyan" if h < 200 else "blue" if h < 250 else "violet" if h < 280 else "purple" if h < 300 else
            "magenta" if h < 330 else "pink")
    tom = "deep " if l < 0.3 else "pale " if l > 0.75 else "vivid " if s_ > 0.6 else "muted "
    return tom + nome


def contraste(c1, c2):
    def lum(rgb):
        def ch(v):
            v /= 255
            return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
        r, g, b = (ch(x) for x in rgb)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    a, b = lum(hexrgb(c1)), lum(hexrgb(c2))
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def aparar(entrada, saida):
    """Remove a moldura transparente. cropdetect so decide com varias passagens."""
    if not tem_alpha(entrada):
        subprocess.run([FF, "-y", "-v", "error", "-i", entrada, saida], check=True)
        return None
    with tempfile.TemporaryDirectory() as d:
        a = os.path.join(d, "a.png")
        subprocess.run([FF, "-y", "-v", "error", "-i", entrada,
                        "-vf", "alphaextract", "-frames:v", "1", a], check=True)
        s = _ff(["-loop", "1", "-i", a, "-t", "0.3",
                 "-vf", "cropdetect=limit=0.02:round=2:reset=0", "-f", "null", "-"])
        crops = re.findall(r'crop=(\d+:\d+:\d+:\d+)', s)
    if not crops:
        subprocess.run([FF, "-y", "-v", "error", "-i", entrada, saida], check=True)
        return None
    subprocess.run([FF, "-y", "-v", "error", "-i", entrada, "-vf", f"crop={crops[-1]}",
                    "-pix_fmt", "rgba", saida], check=True)
    return crops[-1]


def cartao(entrada, saida, fundo="#FFFFFF", lado=1024, margem=0.12):
    """Assenta a arte num cartao opaco.

    Referencia com fundo transparente costuma sair com o alfa interpretado como
    preto. Um cartao com margem generosa da ao modelo a forma isolada e limpa.
    """
    w, h = dimensoes(entrada)
    if not w:
        sys.exit(f"nao consegui ler {entrada}")
    livre = int(lado * (1 - 2 * margem))
    esc = min(livre / w, livre / h)
    nw, nh = max(2, int(w * esc) // 2 * 2), max(2, int(h * esc) // 2 * 2)
    subprocess.run([FF, "-y", "-v", "error",
                    "-f", "lavfi", "-i", f"color=c={fundo.replace('#','0x')}:s={lado}x{lado}",
                    "-i", entrada,
                    "-filter_complex",
                    f"[1:v]scale={nw}:{nh}[a];[0:v][a]overlay=(W-w)/2:(H-h)/2",
                    "-frames:v", "1", saida], check=True)
    return saida


def paleta(saida, cores, larg=300, alt=400):
    """Amostras lado a lado, sem texto nenhum."""
    ent, filt = [], ""
    for i, c in enumerate(cores):
        ent += ["-f", "lavfi", "-i", f"color=c=0x{hexrgb(c) and c.lstrip('#')}:s={larg}x{alt}"]
        filt += f"[{i}]"
    filt += f"hstack={len(cores)}" if len(cores) > 1 else "null"
    subprocess.run([FF, "-y", "-v", "error"] + ent + ["-filter_complex", filt, "-frames:v", "1", saida], check=True)
    return saida


def cmd_paleta(a):
    cores = [c.strip() for c in a.cores.split(",") if c.strip()]
    paleta(a.out, cores)
    print(f"-> {a.out}: " + ", ".join(f"{c} = {nome_cor(c)}" for c in cores))
    print(upload(a.out))


def upload(caminho):
    ext = os.path.splitext(caminho)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    d = base64.b64encode(open(caminho, "rb").read()).decode()
    body = {"base64Data": f"data:{mime};base64,{d}",
            "uploadPath": "images/motion", "fileName": os.path.basename(caminho)}
    r = urllib.request.Request(UPLOAD, json.dumps(body).encode(),
                               {"Authorization": "Bearer " + chave(),
                                "Content-Type": "application/json", "User-Agent": UA})
    return json.load(urllib.request.urlopen(r, timeout=180))["data"]["downloadUrl"]


def cmd_kit(a):
    refs, avisos = [], []

    if a.logo:
        w, h = dimensoes(a.logo)
        print(f"logo: {w}x{h}  alfa: {'sim' if tem_alpha(a.logo) else 'NAO'}")
        if max(w, h) < 512:
            avisos.append(f"logo em {w}x{h} - baixa demais para o modelo reproduzir "
                          "as letras; peca em 1024px ou mais")
        ap = "ref_logo_aparado.png"
        c = aparar(a.logo, ap)
        print(f"  aparado{' (crop=' + c + ')' if c else ' (nada a aparar)'}")
        cart = cartao(ap, "ref_logo.png", a.cartao)
        print(f"  cartao: {cart}")
        refs.append({"papel": "logo", "arquivo": cart, "origem": os.path.abspath(a.logo)})

    for n, t in enumerate(a.tela or [], 1):
        w, h = dimensoes(t)
        print(f"tela {n}: {w}x{h}")
        if w < 1000:
            avisos.append(f"screenshot {os.path.basename(t)} em {w}px - o texto da "
                          "interface vai sair ilegivel; peca em resolucao maior")
        refs.append({"papel": f"tela{n}", "arquivo": os.path.abspath(t),
                     "origem": os.path.abspath(t)})

    for n, e in enumerate(a.produto or [], 1):
        refs.append({"papel": f"produto{n}", "arquivo": os.path.abspath(e),
                     "origem": os.path.abspath(e)})

    for n, e in enumerate(a.estilo or [], 1):
        refs.append({"papel": f"estilo{n}", "arquivo": os.path.abspath(e),
                     "origem": os.path.abspath(e)})

    cores = [c.strip() for c in (a.paleta or "").split(",") if c.strip()]
    if not cores and a.primaria:
        cores = [a.primaria, a.fundo]
    if cores:
        paleta("ref_paleta.png", cores)
        refs.append({"papel": "paleta", "arquivo": "ref_paleta.png", "cores": cores,
                     "nomes": [nome_cor(c) for c in cores]})

    if len(refs) > 7:
        sys.exit(f"{len(refs)} referencias - o limite em 720p e 7")

    print("\nsubindo...")
    for r in refs:
        r["url"] = upload(r["arquivo"])
        print(f"  @image{refs.index(r)+1}  {r['papel']:8s} {r['url']}")

    kit = {"referencias": refs, "primaria": a.primaria, "fundo": a.fundo, "cores": cores,
           "claim": a.claim, "cta": a.cta, "url_marca": a.url,
           "direcao": a.direcao, "evitar": a.evitar}

    if a.primaria and a.fundo:
        print("\ncontraste:")
        for nome, par in (("primaria sobre fundo", (a.primaria, a.fundo)),
                          ("branco sobre fundo", ("#FFFFFF", a.fundo)),
                          ("branco sobre primaria", ("#FFFFFF", a.primaria))):
            r = contraste(*par)
            print(f"  {nome:22s} {r:5.2f}:1  "
                  f"{'ok' if r >= 4.5 else 'limite' if r >= 3 else 'REPROVA'}")

    if avisos:
        print("\navisos:", file=sys.stderr)
        for x in avisos:
            print(f"  ! {x}", file=sys.stderr)

    json.dump(kit, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"\n-> {a.out}")
    print("\nbloco para o prompt:\n")
    print(bloco(kit))


def bloco(kit):
    linhas = []
    for n, r in enumerate(kit["referencias"], 1):
        p = r["papel"]
        if p == "logo":
            linhas.append(f"@image{n} is the brand logo. Reproduce it EXACTLY as shown - "
                          "same letterforms, same proportions, same spacing. Do not "
                          "redraw, restyle, translate or invent any part of it.")
        elif p.startswith("tela"):
            linhas.append(f"@image{n} is a real screenshot of the product interface. "
                          "Show it on the screen exactly as given, without altering its "
                          "layout or text.")
        elif p.startswith("produto"):
            linhas.append(f"@image{n} is the real product. Reproduce its shape, colours, materials "
                          "and whatever is on its screen EXACTLY as given. Do not redesign it and do "
                          "not add text to it.")
        elif p == "paleta":
            nomes = ", ".join(f"{i+1} {nm}" for i, nm in enumerate(r["nomes"]))
            linhas.append(f"@image{n} is the brand colour palette, swatches left to right: {nomes}. "
                          "Use exactly these colours for everything in the scene. Never display the "
                          "swatch image itself and never write any colour name or code on screen.")
        else:
            linhas.append(f"@image{n} is a style reference for lighting, colour and "
                          "material - match its mood, not its content.")
    if kit.get("primaria") and not any(r["papel"] == "paleta" for r in kit["referencias"]):
        linhas.append(f"Brand colour: {nome_cor(kit['primaria'])} should lead the palette"
                      + (f", against {nome_cor(kit['fundo'])}." if kit.get("fundo") else "."))
    if kit.get("direcao"):
        linhas.append("\nVISUAL DIRECTION: " + kit["direcao"])
    if kit.get("evitar"):
        linhas.append("NEVER: " + kit["evitar"])
    return "\n".join(linhas)


def cmd_prompt(a):
    print(bloco(json.load(open(a.marca))))


def cmd_conferir(a):
    kit = json.load(open(a.marca))
    orig = next((r["arquivo"] for r in kit["referencias"] if r["papel"] == "logo"), None)
    if not orig:
        sys.exit("nao ha logo no kit")
    rec = "conferir_recorte.png"
    if a.regiao:
        x, y, w, h = a.regiao.split(",")
        subprocess.run([FF, "-y", "-v", "error", "-i", a.quadro,
                        "-vf", f"crop={w}:{h}:{x}:{y},scale=520:-1", rec], check=True)
    else:
        subprocess.run([FF, "-y", "-v", "error", "-i", a.quadro,
                        "-vf", "scale=520:-1", rec], check=True)
    out = "conferir.png"
    subprocess.run([FF, "-y", "-v", "error", "-i", orig, "-i", rec,
                    "-filter_complex",
                    "[0]scale=520:-1,pad=520:ih+40:0:20:color=white[a];"
                    "[1]pad=520:ih+40:0:20:color=white[b];[a][b]vstack",
                    out], check=True)
    print(f"-> {out}  (original em cima, gerado embaixo)")
    print("compare as formas das letras. Se derivou, regere o plano; se persistir,\n"
          "componha a logo em pos com montar.sh.", file=sys.stderr)


def cmd_contraste(a):
    r = contraste(a.cor1, a.cor2)
    print(f"{r:.2f}:1  " + ("ok para texto" if r >= 4.5 else
                            "so para texto grande" if r >= 3 else "reprova"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(add_help=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("kit")
    p.add_argument("--logo"); p.add_argument("--tela", action="append")
    p.add_argument("--produto", action="append", help="recorte do produto (maquininha, cartao, celular)")
    p.add_argument("--estilo", action="append")
    p.add_argument("--primaria"); p.add_argument("--fundo", default="#0B0D10")
    p.add_argument("--cartao", default="#FFFFFF")
    p.add_argument("--claim"); p.add_argument("--cta"); p.add_argument("--url")
    p.add_argument("--paleta", help="lista de hex separada por virgula; vira imagem de amostras")
    p.add_argument("--direcao", help="direcao visual em ingles, saida do briefing")
    p.add_argument("--evitar", help="o que a marca nao aceita, em ingles")
    p.add_argument("--out", default="marca.json"); p.set_defaults(fn=cmd_kit)
    p = sub.add_parser("prompt"); p.add_argument("marca"); p.set_defaults(fn=cmd_prompt)
    p = sub.add_parser("conferir"); p.add_argument("quadro"); p.add_argument("marca")
    p.add_argument("--regiao"); p.set_defaults(fn=cmd_conferir)
    p = sub.add_parser("contraste"); p.add_argument("cor1"); p.add_argument("cor2")
    p.set_defaults(fn=cmd_contraste)
    p = sub.add_parser("paleta"); p.add_argument("cores"); p.add_argument("--out", default="ref_paleta.png")
    p.set_defaults(fn=cmd_paleta)
    a = ap.parse_args()
    a.fn(a)
