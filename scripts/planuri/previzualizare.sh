#!/bin/bash
# Reface pagina de previzualizare a modelelor noi în build/ro/planuri-noi/.
# Se rulează DUPĂ build.py, fiindcă build-ul şterge folderul de ieşire.
R="$(cd "$(dirname "$0")/../.." && pwd)"
D="$R/build/ro/planuri-noi"
mkdir -p "$D"
cp "$R"/shared/images/case/runa-*.jpg "$R"/shared/images/case/runa-plan.png "$R"/shared/images/case/lira-plan.png "$D/" 2>/dev/null
python3 - "$D" <<'PY'
import sys, pathlib
D = pathlib.Path(sys.argv[1])
CAP = [
 ("runa-fatada-strada.jpg", "Fațada spre stradă — peretele lung, tencuit alb, cu intrarea. Volumul e un dreptunghi de 15,60 × 8,80 m, coamă dreaptă pe toată lungimea, fără aripi."),
 ("runa-fatada-terasa.jpg", "Capătul dinspre grădină. Terasa e scobită în volum pe 1,60 m: pereții laterali și acoperișul merg până la capăt, fără niciun stâlp. Timpanul vitrat stă retras, la adăpost."),
 ("runa-living.jpg", "Livingul deschis, 41,1 m², cu bucătăria și dining-ul în aceeași cameră. Tavanul urmează șarpanta, fără plafon fals."),
 ("runa-bucatarie.jpg", "Bucătăria, pe peretele de sud, cu fereastră deasupra blatului. Insulă cu trei scaune spre living."),
 ("runa-dormitor.jpg", "Dormitor 1, 11,4 m², cu fereastră spre nord și una spre vest. Tavan drept, spre deosebire de living."),
 ("runa-baie.jpg", "Baia de 5,9 m², cu duș și fereastră proprie. Stă spate în spate cu a doua baie, pe aceeași coloană de instalații."),
]
g = "\n".join('  <figure><img src="%s" alt=""><figcaption>%s</figcaption></figure>' % c for c in CAP)
(D / "index.html").write_text(f"""<!doctype html><meta charset="utf-8"><title>Planuri noi — Polistibrick</title>
<style>
 body{{margin:0;background:#f7f5f1;font:15px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;color:#1a1714}}
 header{{padding:26px 32px;border-bottom:1px solid #ddd8d0;background:#fff}}
 h1{{margin:0;font-size:20px;letter-spacing:.06em;font-weight:500}}
 header p{{margin:6px 0 0;color:#8a8178}}
 section{{padding:28px 32px;max-width:1500px}}
 h2{{font-size:16px;letter-spacing:.12em;font-weight:500;margin:0 0 4px}}
 .sub{{color:#8a8178;margin:0 0 16px}}
 .grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}}
 @media(max-width:800px){{.grid{{grid-template-columns:1fr}}}}
 figure{{margin:0}} figcaption{{margin-top:7px;color:#8a8178;font-size:13.5px}}
 img{{width:100%;height:auto;border:1px solid #ddd8d0;background:#fff;display:block}}
</style>
<header><h1>PLANURI NOI</h1><p>Modele în lucru · imaginile stau în shared/images/case/</p></header>
<section><h2>RUNA</h2>
 <p class="sub">Casă pe un nivel, șarpantă clasică · volum sub acoperiș 15,60 × 8,80 m · casă închisă 123,2 m² · util 101,2 m² · terasă scobită 14,1 m² · 3 dormitoare</p>
 <img src="runa-plan.png" alt="Plan parter Runa"></section>
<section><h2>RUNA — randări</h2><p class="sub">Șase imagini, ca la celelalte modele din catalog</p>
 <div class="grid">
{g}
 </div></section>
<section><h2>LIRA</h2>
 <p class="sub">Casă pe un nivel pentru lot îngust · 9,75 m la stradă · amprentă 188,7 m² · util 160,0 m² · 4 dormitoare · randările urmează</p>
 <img src="lira-plan.png" alt="Plan parter Lira"></section>
""", encoding="utf-8")
print("pagina refăcută:", D)
PY
