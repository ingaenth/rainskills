#!/usr/bin/env python3
"""Cliente kie.ai para motion graphics com Gemini Omni Video.

    kie.py upload  <arquivo>                       imagem, video (mp4) ou audio
    kie.py omni    "<prompt>" [--ref URL]... [--dur 4|6|8|10] [--ar 16:9|9:16]
                   [--res 720p|1080p|4k] [--voz AUDIO_ID]... [--seed N]
                   [--continua URL[:ini:fim]] [--out clipe.mp4]
    kie.py veo     "<prompt>" --primeiro URL|K1.png --ultimo URL|K2.png [--modelo veo3_fast|veo3|veo3_lite]
                   [--ar 16:9|9:16] [--1080p] [--out clipe.mp4]     first + last frame nativo, 8s
    kie.py grok    <img_url|K1.png> "<prompt>" [--ref URL]... [--dur 6] [--ar 16:9] [--out clipe.mp4]
                   image-to-video do primeiro frame (sem last frame), 27 cr
    kie.py voz-omni --nome X [--base algenib] [--descricao "..."] [--exemplo "..."]
    kie.py tts     "<texto>" [--voz Algieba] [--estilo "Vocal Smile"] [--out bloco.mp3]
    kie.py imagem  "<prompt>" [--ref URL|arquivo]... [--ar 16:9] [--res 2K] [--out K1.png]
                   keyframes: K1 com produto+paleta+post; K_n+1 com --ref K_n ("NEXT keyframe")
    kie.py musica  "<descricao>" [--out faixa]
    kie.py status  <task_id> [--out arquivo]       recupera uma tarefa pelo id
    kie.py saldo                                   creditos na conta
    kie.py motores [--planos 5] [--formatos 1]     saldo, motores disponiveis e custo da peca em cada um

Chave: variavel KIE_KEY, ou ~/.config/kie/key.

Custos medidos (creditos): omni = 21 + 10,5/s em 720p OU 1080p (mesmo preco:
use sempre 1080p); 4k = 2,3x; --continua = 2x. Todo task_id vai para
tarefas.jsonl ANTES do polling - sem o id nao ha como recuperar um clipe pago.
"""
import argparse, base64, json, os, sys, time, urllib.request

API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-base64-upload"
UA = "Mozilla/5.0"
LOG = "tarefas.jsonl"
KEY = None


def chave():
    k = os.environ.get("KIE_KEY")
    if k:
        return k.strip()
    p = os.path.expanduser("~/.config/kie/key")
    if os.path.exists(p):
        return open(p).read().strip()
    sys.exit("KIE_KEY nao definida (env ou ~/.config/kie/key)")


def _hdr():
    return {"Authorization": "Bearer " + KEY, "Content-Type": "application/json",
            "User-Agent": UA}


def post(url, body):
    r = urllib.request.Request(url, json.dumps(body).encode(), _hdr())
    try:
        return json.load(urllib.request.urlopen(r, timeout=180))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} em {url}: {e.read()[:400].decode(errors='replace')}")


def get(url):
    r = urllib.request.Request(url, headers={"Authorization": "Bearer " + KEY, "User-Agent": UA})
    return json.load(urllib.request.urlopen(r, timeout=90))


def baixar(url, destino):
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=600) as s, open(destino, "wb") as f:
        f.write(s.read())
    print(f"-> {destino} ({os.path.getsize(destino)//1024} KB)", file=sys.stderr)
    return destino


MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
        ".mp4": "video/mp4", ".mov": "video/quicktime", ".mp3": "audio/mpeg", ".wav": "audio/wav"}


def _png_real(caminho):
    """WebP com extensao .png devolve 'Internal Error' no nano-banana-pro: reconverte."""
    with open(caminho, "rb") as f:
        cab = f.read(12)
    if caminho.lower().endswith(".png") and cab[:4] != b"\x89PNG":
        novo = caminho[:-4] + ".real.png"
        import subprocess
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", caminho, novo], check=True)
        print(f"! {caminho} nao era PNG; convertido em {novo}", file=sys.stderr)
        return novo
    return caminho


def upload(caminho):
    ext = os.path.splitext(caminho)[1].lower()
    mime = MIME.get(ext)
    if not mime:
        sys.exit(f"extensao nao suportada: {ext}")
    pasta = "videos/motion" if mime.startswith("video") else \
            "audios/motion" if mime.startswith("audio") else "images/motion"
    dados = open(caminho, "rb").read()
    d = base64.b64encode(dados).decode()
    # Nome unico por conteudo: um nome fixo (ref_logo.png) e sobrescrito por outro projeto
    # na mesma conta e o keyframe sai com a logo errada.
    import hashlib
    raiz, ext = os.path.splitext(os.path.basename(caminho))
    nome = f"{raiz}-{hashlib.md5(dados).hexdigest()[:8]}{ext}"
    r = post(UPLOAD, {"base64Data": f"data:{mime};base64,{d}",
                      "uploadPath": pasta, "fileName": nome})
    return r["data"]["downloadUrl"]


def _registrar(task_id, modelo, entrada, rotulo):
    with open(LOG, "a") as f:
        f.write(json.dumps({"task_id": task_id, "modelo": modelo, "rotulo": rotulo,
                            "quando": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "input": entrada}, ensure_ascii=False) + "\n")


def _urls(d):
    if d.get("resultJson"):
        return json.loads(d["resultJson"])["resultUrls"]
    return d["response"].get("resultUrls") or d["response"]["fullResultUrls"]


def _esperar(task_id, rotulo, limite=120, espera=10):
    for _ in range(limite):
        time.sleep(espera)
        d = get(f"{API}/jobs/recordInfo?taskId={task_id}")["data"]
        st = d.get("state")
        if st == "success":
            print(f"{rotulo}: {d.get('creditsConsumed')} cr", file=sys.stderr)
            return _urls(d)[0]
        if st == "fail":
            sys.exit(f"{rotulo} falhou: {d.get('failMsg') or d.get('errorMessage')}")
    sys.exit(f"{rotulo}: tempo esgotado - recupere depois com: kie.py status {task_id}")


def jobs(modelo, entrada, rotulo):
    t = post(f"{API}/jobs/createTask", {"model": modelo, "input": entrada})["data"]["taskId"]
    _registrar(t, modelo, entrada, rotulo)
    print(f"{rotulo}: {t}", file=sys.stderr)
    return t, _esperar(t, rotulo)


def cmd_omni(a):
    if a.dur not in ("4", "6", "8", "10"):
        sys.exit("--dur deve ser 4, 6, 8 ou 10")
    for c in ("#",):
        if c in a.prompt:
            print("! o prompt tem '#': codigo de cor no prompt VIRA TEXTO NA TELA. "
                  "Nomeie a cor ou passe a paleta como imagem (marca.py paleta).", file=sys.stderr)
    entrada = {"prompt": a.prompt, "duration": a.dur, "aspect_ratio": a.ar, "resolution": a.res}
    refs = [r for r in (a.ref or []) if r and r != "-"]
    if refs:
        entrada["image_urls"] = refs
    if a.voz:
        entrada["audio_ids"] = a.voz
    if a.seed is not None:
        entrada["seed"] = a.seed
    if a.continua:
        p = a.continua.split(":")
        url, ini, fim = p[0], float(p[1]) if len(p) > 1 else 0.0, float(p[2]) if len(p) > 2 else 10.0
        if not url.startswith("http"):
            url = upload(url)
        if fim - ini > 10:
            sys.exit("--continua: a janela do video de origem e de no maximo 10s")
        entrada["video_list"] = [{"url": url, "start": ini, "ends": fim}]
        print("continuacao: custa 2x e herda os defeitos do clipe de origem", file=sys.stderr)
    if len(refs) + (2 if a.continua else 0) > 7:
        sys.exit("limite de 7 slots: cada imagem usa 1, o video de origem usa 2")
    t, u = jobs("gemini-omni-video", entrada, "omni")
    if a.out:
        baixar(u, a.out)
    print(json.dumps({"task_id": t, "url": u}))


def cmd_veo(a):
    p = a.primeiro if a.primeiro.startswith("http") else upload(_png_real(a.primeiro))
    u = a.ultimo if a.ultimo.startswith("http") else upload(_png_real(a.ultimo))
    body = {"prompt": a.prompt, "model": a.modelo, "aspectRatio": a.ar, "enableTranslation": False,
            "imageUrls": [p, u], "generationType": "FIRST_AND_LAST_FRAMES_2_VIDEO"}
    t = post(f"{API}/veo/generate", body)["data"]["taskId"]
    _registrar(t, a.modelo, body, "veo")
    print(f"veo: {t}", file=sys.stderr)
    for _ in range(120):
        time.sleep(10)
        d = get(f"{API}/veo/record-info?taskId={t}")["data"]
        if d.get("successFlag") == 1:
            urls = (d.get("response") or {}).get("resultUrls") or []
            break
        if d.get("successFlag") in (2, 3) or d.get("errorMessage"):
            sys.exit(f"veo falhou: {d.get('errorMessage')}")
    else:
        sys.exit(f"veo: tempo esgotado - kie.py status nao serve aqui; consulte /veo/record-info?taskId={t}")
    url = urls[0]
    if a.hd:
        for _ in range(60):
            time.sleep(10)
            try:
                r = get(f"{API}/veo/get-1080p-video?taskId={t}")["data"]
            except Exception:
                r = {}
            if r and r.get("resultUrl"):
                url = r["resultUrl"]; break
        else:
            print("1080p nao ficou pronto; usando 720p", file=sys.stderr)
    if a.out:
        baixar(url, a.out)
    print(json.dumps({"task_id": t, "url": url}))


def cmd_grok(a):
    img = a.img if a.img.startswith("http") else upload(_png_real(a.img))
    urls = [img] + [r for r in (a.ref or []) if r and r != "-"]
    if len(urls) > 7:
        sys.exit("limite de 7 imagens")
    t, u = jobs("grok-imagine/image-to-video",
                {"image_urls": urls, "prompt": a.prompt, "mode": "normal", "resolution": "720p",
                 "duration": str(a.dur), "aspect_ratio": a.ar}, "grok")
    if a.out:
        baixar(u, a.out)
    print(json.dumps({"task_id": t, "url": u}))


def cmd_voz_omni(a):
    r = post(f"{API}/omni/audio/create",
             {"audio_id": a.base, "name": a.nome,
              "voice_description": a.descricao or "", "example_dialogue": a.exemplo or ""})
    vid = r["data"]["audioId"]
    reg = {}
    if os.path.exists("vozes.json"):
        reg = json.load(open("vozes.json"))
    reg[a.nome] = {"audio_id": vid, "base": a.base, "descricao": a.descricao}
    json.dump(reg, open("vozes.json", "w"), indent=1, ensure_ascii=False)
    print(vid)


def cmd_tts(a):
    entrada = {"temperature": 1,
               "scene": "Locucao publicitaria em portugues do Brasil.",
               "sample_context": "Narracao brasileira, natural, locutor nativo. "
                                 "Todo o texto e em portugues brasileiro.",
               "speakers": [{"speaker_id": "Speaker 1", "voice_name": a.voz,
                             "audio_profile": a.perfil, "accent": "Neutral",
                             "style": a.estilo, "pace": a.ritmo}],
               "dialogue_turns": [{"speaker_id": "Speaker 1", "text": a.texto}]}
    t, u = jobs("google/gemini-3-1-flash-tts", entrada, "tts")
    print(baixar(u, a.out) if a.out else u)


GERADORES = {
    "nano-banana-pro": "Google nano-banana-pro, 2K, 18 cr, escreve portugues com acento",
    "gpt-image-2": "OpenAI GPT Image 2 (o do ChatGPT), 1K/2K/4K, ate 16 referencias",
}


def cmd_imagem(a):
    refs = [r if r.startswith("http") else upload(_png_real(r)) for r in (a.ref or []) if r]
    if a.modelo == "gpt-image-2":
        # 'auto' so gera 1K; 1:1 nao aceita 4K; 4:5 e 5:4 so 1K.
        entrada = {"prompt": a.prompt, "aspect_ratio": a.ar, "resolution": a.res}
        modelo = "gpt-image-2-text-to-image"
        if refs:
            entrada["input_urls"] = refs
            modelo = "gpt-image-2-image-to-image"
    else:
        entrada = {"prompt": a.prompt, "aspect_ratio": a.ar, "resolution": a.res, "output_format": "png"}
        modelo = "nano-banana-pro"
        if refs:
            entrada["image_input"] = refs
    t, u = jobs(modelo, entrada, "imagem")
    print(baixar(u, a.out) if a.out else u)


def cmd_musica(a):
    r = post(f"{API}/generate", {"prompt": a.prompt, "customMode": False, "instrumental": True,
                                 "model": "V4_5", "callBackUrl": "https://example.com/cb"})
    t = r["data"]["taskId"]
    _registrar(t, "suno", {"prompt": a.prompt}, "musica")
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


def saldo():
    return get(f"{API}/chat/credit")["data"]


def cmd_saldo(a):
    print(saldo())


def cmd_motores(a):
    """Quais motores a conta alcanca agora, e quanto custa a peca em cada um."""
    cr = saldo()
    n, f = a.planos, a.formatos
    k = 18 * (n + 1) * f
    linhas = [("omni", "Gemini Omni 6s 1080p, first/last por referencia", 84, "texto e logo NA IMAGEM"),
              ("veo", "Veo 3.1 fast 8s 720p, first/last nativo", 65, "texto e logo EM POS"),
              ("grok", "Grok Imagine 6s 720p, so primeiro frame", 27, "texto e logo EM POS")]
    print(f"saldo: {cr} creditos | peca de {n} planos x {f} formato(s) | keyframes: {k} cr\n")
    print(f"{'motor':6} {'clipe':46} {'plano':>6} {'peca':>7}  cabe?  texto")
    for nome, desc, custo, texto in linhas:
        total = k + custo * n * f + 10
        ok = "sim" if cr >= total else "NAO"
        print(f"{nome:6} {desc:46} {custo:6} {total:7}  {ok:5}  {texto}")
    print("\nO motor decide o texto: Omni -> no keyframe; Veo/Grok -> tipo.py em pos.")
    print("Pergunte ao cliente qual motor, mostrando esta tabela. Nao escolha por ele.")


def cmd_status(a):
    d = get(f"{API}/jobs/recordInfo?taskId={a.task}")["data"]
    st = d.get("state")
    print(f"estado: {st}  creditos: {d.get('creditsConsumed')}", file=sys.stderr)
    if st == "success":
        u = _urls(d)[0]
        if a.out:
            baixar(u, a.out)
        print(u)
    elif st == "fail":
        print(d.get("failMsg") or d.get("errorMessage"))


def main():
    global KEY
    ap = argparse.ArgumentParser(add_help=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("upload"); p.add_argument("arquivo")
    p = sub.add_parser("omni"); p.add_argument("prompt")
    p.add_argument("--ref", action="append", help="ate 7 imagens; viram @image1, @image2, ...")
    p.add_argument("--dur", default="6"); p.add_argument("--ar", default="16:9")
    p.add_argument("--res", default="1080p"); p.add_argument("--voz", action="append")
    p.add_argument("--seed", type=int); p.add_argument("--continua")
    p.add_argument("--out"); p.set_defaults(fn=cmd_omni)
    p = sub.add_parser("veo"); p.add_argument("prompt"); p.add_argument("--primeiro", required=True)
    p.add_argument("--ultimo", required=True); p.add_argument("--modelo", default="veo3_fast")
    p.add_argument("--ar", default="16:9"); p.add_argument("--1080p", dest="hd", action="store_true")
    p.add_argument("--out"); p.set_defaults(fn=cmd_veo)
    p = sub.add_parser("grok"); p.add_argument("img"); p.add_argument("prompt")
    p.add_argument("--ref", action="append"); p.add_argument("--dur", default="6")
    p.add_argument("--ar", default="16:9"); p.add_argument("--out"); p.set_defaults(fn=cmd_grok)
    p = sub.add_parser("voz-omni"); p.add_argument("--nome", required=True)
    p.add_argument("--base", default="algenib"); p.add_argument("--descricao")
    p.add_argument("--exemplo"); p.set_defaults(fn=cmd_voz_omni)
    p = sub.add_parser("tts"); p.add_argument("texto"); p.add_argument("--voz", default="Algieba")
    p.add_argument("--perfil", default="Locutor brasileiro, voz calorosa e segura")
    p.add_argument("--estilo", default="Vocal Smile"); p.add_argument("--ritmo", default="Natural")
    p.add_argument("--out"); p.set_defaults(fn=cmd_tts)
    p = sub.add_parser("imagem"); p.add_argument("prompt"); p.add_argument("--ref", action="append",
                   help="ate 7 URLs ou arquivos; keyframe anterior, produto, paleta, post do cliente")
    p.add_argument("--ar", default="16:9"); p.add_argument("--res", default="2K")
    p.add_argument("--modelo", default="nano-banana-pro", choices=list(GERADORES),
                   help="gerador de imagem: pergunta do briefing; nano-banana-pro (padrao) ou gpt-image-2")
    p.add_argument("--out"); p.set_defaults(fn=cmd_imagem)
    p = sub.add_parser("musica"); p.add_argument("prompt"); p.add_argument("--out", default="musica")
    p.set_defaults(fn=cmd_musica)
    p = sub.add_parser("status"); p.add_argument("task"); p.add_argument("--out")
    p.set_defaults(fn=cmd_status)
    p = sub.add_parser("saldo"); p.set_defaults(fn=cmd_saldo)
    p = sub.add_parser("motores"); p.add_argument("--planos", type=int, default=5)
    p.add_argument("--formatos", type=int, default=1); p.set_defaults(fn=cmd_motores)
    a = ap.parse_args()
    KEY = chave()
    if a.cmd == "upload":
        print(upload(a.arquivo))
    else:
        a.fn(a)


if __name__ == "__main__":
    main()
