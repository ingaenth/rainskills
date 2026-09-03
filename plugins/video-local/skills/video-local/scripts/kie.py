#!/usr/bin/env python3
"""Cliente kie.ai para o pipeline do filme de la.

    kie.py upload  <arquivo>
    kie.py imagem  "<prompt>" [--out saida.png] [--ar 16:9|9:16]
    kie.py editar  <url_ou_arquivo> "<mudanca>" [--ref URL] [--out saida.png]
    kie.py base    <img_url> "<prompt>" [--ref URL]... [--dur 6] [--out cena.mp4]
    kie.py extend  <task_id> <extend_at> <6|10> "<prompt>" [--out cena.mp4]
    kie.py voz     "<texto>" [--voz Daniel] [--out bloco.mp3]
    kie.py musica  "<descricao>" [--out faixa]

Chave: variavel KIE_KEY, ou ~/.config/kie/key.
Sempre 720p - 1080p falha em clipe longo.
"""
import argparse, base64, json, os, sys, time, urllib.request

API = "https://api.kie.ai/api/v1"
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


KEY = None


def _hdr():
    return {"Authorization": "Bearer " + KEY, "Content-Type": "application/json",
            "User-Agent": UA}


def post(url, body):
    r = urllib.request.Request(url, json.dumps(body).encode(), _hdr())
    return json.load(urllib.request.urlopen(r, timeout=180))


def get(url):
    r = urllib.request.Request(url, headers={"Authorization": "Bearer " + KEY,
                                             "User-Agent": UA})
    return json.load(urllib.request.urlopen(r, timeout=90))


def baixar(url, destino):
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=300) as s, open(destino, "wb") as f:
        f.write(s.read())
    print(f"-> {destino} ({os.path.getsize(destino)//1024} KB)", file=sys.stderr)
    return destino


def upload(caminho):
    ext = os.path.splitext(caminho)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    d = base64.b64encode(open(caminho, "rb").read()).decode()
    r = post(UPLOAD, {"base64Data": f"data:{mime};base64,{d}",
                      "uploadPath": "images/filme", "fileName": os.path.basename(caminho)})
    return r["data"]["downloadUrl"]


def _poll(url_consulta, campo_estado, ok, falha, rotulo, limite=120, espera=8):
    for _ in range(limite):
        time.sleep(espera)
        d = get(url_consulta)["data"]
        st = d.get(campo_estado)
        if st in ok:
            return d
        if st in falha:
            sys.exit(f"{rotulo} falhou: {d.get('failMsg') or d.get('errorMessage')}")
    sys.exit(f"{rotulo}: tempo esgotado")


def _urls(d):
    if d.get("resultJson"):
        return json.loads(d["resultJson"])["resultUrls"]
    return d["response"].get("resultUrls") or d["response"]["fullResultUrls"]


def playground(modelo, entrada, rotulo):
    t = post(f"{API}/playground/createTask",
             {"model": modelo, "input": entrada})["data"]["taskId"]
    print(f"{rotulo}: {t}", file=sys.stderr)
    d = _poll(f"{API}/playground/recordInfo?taskId={t}", "state",
              {"success"}, {"fail"}, rotulo)
    print(f"{rotulo}: {d.get('creditsConsumed')} cr", file=sys.stderr)
    return _urls(d)[0]


def jobs(modelo, entrada, rotulo):
    t = post(f"{API}/jobs/createTask",
             {"model": modelo, "input": entrada})["data"]["taskId"]
    print(f"{rotulo}: {t}", file=sys.stderr)
    d = _poll(f"{API}/jobs/recordInfo?taskId={t}", "state",
              {"success"}, {"fail"}, rotulo, limite=120, espera=15)
    print(f"{rotulo}: {d.get('creditsConsumed')} cr", file=sys.stderr)
    return t, _urls(d)[0]


def main():
    global KEY
    ap = argparse.ArgumentParser(add_help=False)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("upload"); p.add_argument("arquivo")
    p = sub.add_parser("imagem"); p.add_argument("prompt"); p.add_argument("--out")
    p.add_argument("--ar", default="16:9")
    p = sub.add_parser("editar"); p.add_argument("origem"); p.add_argument("prompt")
    p.add_argument("--ref"); p.add_argument("--out"); p.add_argument("--ar", default="16:9")
    p = sub.add_parser("base"); p.add_argument("img")
    p.add_argument("prompt"); p.add_argument("--ref", action="append",
                   help="ate 6 referencias extras; viram @image2, @image3, ...")
    p.add_argument("--dur", default="6"); p.add_argument("--out")
    p.add_argument("--ar", default="16:9")
    p = sub.add_parser("extend"); p.add_argument("task"); p.add_argument("at")
    p.add_argument("times"); p.add_argument("prompt"); p.add_argument("--out")
    p = sub.add_parser("voz"); p.add_argument("texto"); p.add_argument("--voz", default="Daniel")
    p.add_argument("--vel", default="1.0"); p.add_argument("--out")
    p = sub.add_parser("musica"); p.add_argument("prompt"); p.add_argument("--out", default="musica")
    a = ap.parse_args()
    KEY = chave()

    if a.cmd == "upload":
        print(upload(a.arquivo))

    elif a.cmd == "imagem":
        u = playground("google/nano-banana",
                       {"prompt": a.prompt, "output_format": "png", "image_size": a.ar},
                       "imagem")
        print(baixar(u, a.out) if a.out else u)

    elif a.cmd == "editar":
        origem = a.origem if a.origem.startswith("http") else upload(a.origem)
        urls = [origem] + ([a.ref] if a.ref else [])
        u = playground("google/nano-banana-edit",
                       {"prompt": a.prompt, "image_urls": urls,
                        "output_format": "png", "image_size": a.ar}, "edicao")
        print(baixar(u, a.out) if a.out else u)

    elif a.cmd == "base":
        urls = [a.img] + [r for r in (a.ref or []) if r and r != "-"]
        if len(urls) > 7:
            sys.exit(f"{len(urls)} imagens - o limite em 720p e 7")
        t, u = jobs("grok-imagine/image-to-video",
                    {"image_urls": urls, "prompt": a.prompt, "mode": "normal",
                     "resolution": "720p", "duration": str(a.dur),
                     "aspect_ratio": a.ar}, "base")
        if a.out:
            baixar(u, a.out)
        print(json.dumps({"task_id": t, "url": u}))

    elif a.cmd == "extend":
        if str(a.times) not in ("6", "10"):
            sys.exit("extend_times deve ser 6 ou 10")
        t, u = jobs("grok-imagine/extend",
                    {"task_id": a.task, "extend_at": float(a.at),
                     "extend_times": str(a.times), "prompt": a.prompt}, "extend")
        if a.out:
            baixar(u, a.out)
        print(json.dumps({"task_id": t, "url": u}))

    elif a.cmd == "voz":
        t, u = jobs("elevenlabs/text-to-speech-turbo-2-5",
                    {"text": a.texto, "voice": a.voz, "language_code": "pt",
                     "stability": 0.45, "similarity_boost": 0.8, "style": 0.35,
                     "speed": float(a.vel)}, "voz")
        print(baixar(u, a.out) if a.out else u)

    elif a.cmd == "musica":
        r = post(f"{API}/generate",
                 {"prompt": a.prompt, "customMode": False, "instrumental": True,
                  "model": "V4_5", "callBackUrl": "https://example.com/cb"})
        t = r["data"]["taskId"]
        print(f"musica: {t}", file=sys.stderr)
        for _ in range(120):
            time.sleep(15)
            d = get(f"{API}/generate/record-info?taskId={t}")["data"]
            if d["status"] == "SUCCESS":
                faixas = [x["audioUrl"] for x in d["response"]["sunoData"] if x.get("audioUrl")]
                for n, u in enumerate(faixas, 1):
                    baixar(u, f"{a.out}_{n}.mp3")
                print(json.dumps(faixas)); return
            if "FAIL" in str(d["status"]) or "ERROR" in str(d["status"]):
                sys.exit(f"musica falhou: {d.get('errorMessage')}")
        sys.exit("musica: tempo esgotado")


if __name__ == "__main__":
    main()
