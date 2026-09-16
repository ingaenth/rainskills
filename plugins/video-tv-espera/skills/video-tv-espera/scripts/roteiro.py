#!/usr/bin/env python3
"""Gera o "Roteiro do vídeo" — o artefato de aprovação que o cliente abre num link.

Não é só a grade de imagens: é o plano completo — o que acontece do segundo X ao Y,
o movimento de cada plano, a transição entre eles, a cartela e o áudio. HTML único e
auto-contido (thumbs em base64), pronto para publicar em qualquer pasta servida.

Uso:  python3 roteiro.py plano.json roteiro-do-video.html

plano.json:
{
  "titulo": "Vídeo TV — Nome do Cliente",
  "formato": "16:9 · 1920×1080 · 1:22 em loop",
  "trilha": "música suave 50% + ambiência de sala contínua + vapor aos 43s · -14 LUFS",
  "obs": "frase livre (opcional)",
  "planos": [
    {"img": "caminho/quadro.png",
     "inicio": "0:00", "fim": "0:09",
     "titulo": "Entrada",
     "cartela": "Logo (fade in 1,2s, fade out no fim do plano)",
     "movimento": "micro push-in 2%, câmera travada; plantas balançam de leve",
     "transicao": "dissolve 0,7s para o próximo",
     "audio": "só trilha (opcional)"}
  ]
}
"""
import base64, io, json, sys

try:
    from PIL import Image
except ImportError:
    Image = None


def thumb64(path, w=560):
    if Image is None:
        return ""
    im = Image.open(path).convert("RGB")
    im.thumbnail((w, w))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main(plano_json, saida):
    p = json.load(open(plano_json))
    rows = []
    for i, s in enumerate(p["planos"], 1):
        img = f'<img src="{thumb64(s["img"])}" alt="">' if s.get("img") else ""
        audio = f'<div class="lin"><b>Áudio</b> {s["audio"]}</div>' if s.get("audio") else ""
        rows.append(f"""
    <div class="plano">
      <div class="thumb">{img}<span class="num">{i}</span></div>
      <div class="info">
        <div class="tempo">{s["inicio"]} → {s["fim"]}</div>
        <h3>{s["titulo"]}</h3>
        <div class="lin"><b>Na tela</b> {s.get("cartela", "—")}</div>
        <div class="lin"><b>Movimento</b> {s.get("movimento", "—")}</div>
        <div class="lin"><b>Transição</b> {s.get("transicao", "—")}</div>
        {audio}
      </div>
    </div>""")
    obs = f'<p class="obs">{p["obs"]}</p>' if p.get("obs") else ""
    html = f"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>Roteiro do vídeo — {p["titulo"]}</title>
<style>
 body{{margin:0;background:#1F1D1A;color:#FAF7F2;font:16px/1.5 Georgia,serif}}
 .wrap{{max-width:760px;margin:0 auto;padding:28px 16px 60px}}
 h1{{font-size:26px;margin:0 0 4px}} .sub{{color:#D9CFBE;font-family:system-ui;font-size:13px}}
 .meta{{border-left:3px solid #B08D57;padding:8px 14px;margin:18px 0;color:#D9CFBE;font-family:system-ui;font-size:14px}}
 .plano{{display:flex;gap:14px;margin:22px 0;background:#28251f;border-radius:12px;overflow:hidden}}
 .thumb{{position:relative;flex:0 0 42%}} .thumb img{{width:100%;height:100%;object-fit:cover;display:block}}
 .num{{position:absolute;top:8px;left:8px;background:#B08D57;color:#1F1D1A;font-family:system-ui;
      font-weight:700;font-size:13px;border-radius:99px;padding:2px 9px}}
 .info{{padding:12px 14px 12px 0;flex:1}}
 .tempo{{color:#B08D57;font-family:ui-monospace,monospace;font-size:13px}}
 h3{{margin:2px 0 8px;font-size:19px}}
 .lin{{font-family:system-ui;font-size:13px;color:#D9CFBE;margin:3px 0}}
 .lin b{{color:#FAF7F2;font-weight:600;display:inline-block;min-width:84px}}
 .obs{{color:#D9CFBE;font-family:system-ui;font-size:14px}}
 @media(max-width:560px){{.plano{{flex-direction:column}}.thumb{{flex:none}}.info{{padding:0 14px 14px}}}}
</style></head><body><div class="wrap">
<h1>Roteiro do vídeo</h1><div class="sub">{p["titulo"]}</div>
<div class="meta">{p["formato"]}<br>Som: {p.get("trilha", "—")}</div>
{obs}
{''.join(rows)}
<p class="obs">Aprovando este roteiro, os planos são animados e o vídeo montado
exatamente nesta ordem e nestes tempos. Ajustes de texto, ordem e ritmo continuam
gratuitos depois.</p>
</div></body></html>"""
    open(saida, "w").write(html)
    print(f"roteiro ok: {saida} ({len(p['planos'])} planos)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
