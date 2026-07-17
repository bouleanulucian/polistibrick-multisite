#!/usr/bin/env python3
"""Second-pass cleanup: remaining Italian/French visible text in ES focus files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "countries/es"

FILES = {
    "para/propietarios/index.html": [
        ("<h2>Concretamente, <em>cada día.</em></em></h2>", "<h2>Concretamente, <em>cada día.</em></h2>"),
        ("<h2>Trabajamos con su arquitecto — <em>en su interés.</em></em></h2>", "<h2>Trabajamos con su arquitecto — <em>en su interés.</em></h2>"),
        ("<h3>Ponemos a su disposición <em>todo el material necesario.</em></em></h3>", "<h3>Ponemos a su disposición <em>todo el material necesario.</em></h3>"),
        ("colaborará con nosotros — <strong>en su interés.</em></strong>", "colaborará con nosotros — <strong>en su interés.</strong>"),
        ("<h3>Polistibrick se comporta <em>como un encofrado clásico.</em></em></h3>", "<h3>Polistibrick se comporta <em>como un encofrado clásico.</em></h3>"),
        ("A1 antincendio,", "A1 resistencia al fuego,"),
        ("Tempo costruzione (struttura portante)", "Tiempo de construcción (estructura portante)"),
        ('alt="Villa Polistibrick — Île-de-France, consegna 2025"', 'alt="Villa Polistibrick — Île-de-France, entrega 2025"'),
        (
            "Architettura moderna su R+1, zona residenziale premium vicino a Parigi. Muros Polistibrick MBK 300, prestazione Passivhaus certificata, consegna estate 2025.",
            "Arquitectura moderna en R+1, zona residencial premium cerca de París. Muros Polistibrick MBK 300, rendimiento Passivhaus certificado, entrega verano 2025.",
        ),
        (
            "La struttura portante richiede <strong>4-6 semanas</strong> per una casa di 150-200 m² (vs 4-5 meses en ladrillo classico). In totale, ti trasferisci in <strong>5-7 mesi</strong> (in base alle finiture e al permesso). È 2-3 volte più veloce di una construcción clásica.",
            "La estructura portante requiere <strong>4-6 semanas</strong> para una casa de 150-200 m² (frente a 4-5 meses en ladrillo clásico). En total, se muda en <strong>5-7 meses</strong> (según los acabados y el permiso). Es 2-3 veces más rápido que una construcción clásica.",
        ),
        ("<strong>cemento armato</strong>", "<strong>hormigón armado</strong>"),
        ("mismo hormigón armado, vertido en un", "mismo hormigón armado, vertido en un"),  # no-op guard
    ],
    "para/arquitectos/index.html": [
        ("<h3>Cemento armato <em>classico.</em></h3>", "<h3>Hormigón armado <em>clásico.</em></h3>"),
        ("<h3>Da RE2020 <em>a Passiv+.</em></h3>", "<h3>De RE2020 <em>a Passiv+.</em></h3>"),
        (
            "MBK 210 per RE2020 standard, MBK 270 per passivo, MBK 300 per passivo premium. Elija in base al progetto.",
            "MBK 210 para RE2020 estándar, MBK 270 para pasivo, MBK 300 para pasivo premium. Elija según el proyecto.",
        ),
    ],
    "para/constructores/index.html": [
        (
            "(struttura portante, aislamiento, impermeabilización, acustica e finiture)",
            "(estructura portante, aislamiento, impermeabilización, acústica y acabados)",
        ),
        (
            "Ti <strong>trasmettiamo lead qualificati</strong> da architetti e privati nel tuopartimento. Benefici inoltre del co-branding sui nostri supporti regionali.",
            "Le <strong>enviamos clientes potenciales cualificados</strong> de arquitectos y particulares en su departamento. Además, se beneficia del co-branding en nuestros soportes regionales.",
        ),
    ],
    "productos/forjados-pbk/index.html": [
        ("polistirolo + fibrocemento + hormigón armato", "poliestireno + fibrocemento + hormigón armado"),
        ("<strong>Hormigón armato strutturale</strong>", "<strong>Hormigón armado estructural</strong>"),
        ("strati polistirolo + fibrocemento + hormigón", "capas de poliestireno + fibrocemento + hormigón"),
        (
            "Cassaforma isolante a perdere con 3 modelli (210/270/300). Muros passive A+++ in un unico getto.",
            "Encofrado aislante perdido con 3 modelos (210/270/300). Muros pasivos A+++ en un único vertido.",
        ),
    ],
    "proyectos/conjunto-lyon/index.html": [
        ('6<small> mesi</small>', '6<small> meses</small>'),
        ("<strong>tempi</strong>", "<strong>plazos</strong>"),
        ("<strong>prevedibilità</strong> (pannelli prefabbricati, nessuna sorpresa in cantiere)", "<strong>previsibilidad</strong> (paneles prefabricados, sin sorpresas en obra)"),
        ("Costo totale del progetto", "Costo total del proyecto"),
        ("[Foto: Interno 1]", "[Foto: Interior 1]"),
        ("[Foto: Recepción chiavi]", "[Foto: Entrega de llaves]"),
        ("[Foto: Occupazione]", "[Foto: Ocupación]"),
    ],
    "polistibrick-mercury-style.html": [
        ("<span class=\"pane-tag\">Classico</span>", "<span class=\"pane-tag\">Clásico</span>"),
        (
            "Muros EPS erette e fissate con puntellatura laterale in legno sulla fondazione. Senza malta, senza perdite di aislamiento.",
            "Muros EPS erigidos y fijados con apuntalamiento lateral de madera sobre la cimentación. Sin mortero, sin pérdidas de aislamiento.",
        ),
        ('aria-label="Recensioni e testimonianze dei costruttori"', 'aria-label="Reseñas y testimonios de constructores"'),
        ("Recensioni verificate · Costruttori", "Reseñas verificadas · Constructores"),
        ("Testimonianza video", "Testimonio en vídeo"),
        ('aria-label="Riproduci il video"', 'aria-label="Reproducir el vídeo"'),
        ('aria-label="5 su 5"', 'aria-label="5 de 5"'),
        (
            "L'abbiamo testato sul primo cantiere e, francamente, <em>è una meraviglia</em>. El muro se levanta casi solo — no volvemos atrás.",
            "Lo probamos en la primera obra y, sinceramente, <em>es una maravilla</em>. El muro se levanta casi solo — no volvemos atrás.",
        ),
        (
            "L'abbiamo testato sul primo cantiere e, francamente, <em>è una meraviglia</em>. I ragazzi hanno preso la mano in due giorni, il muro si alza quasi da solo. Non torniamo indietro.",
            "Lo probamos en la primera obra y, sinceramente, <em>es una maravilla</em>. El equipo cogió el ritmo en dos días, el muro se levanta casi solo. No volvemos atrás.",
        ),
        ("Constructor verificato", "Constructor verificado"),
        ("Cliente verificato", "Cliente verificado"),
        ("<em>consumi quasi nulli</em>", "<em>consumos casi nulos</em>"),
        ('aria-label="Recensione ', 'aria-label="Reseña '),
        ('aria-label="Recensione precedente"', 'aria-label="Reseña anterior"'),
        ('aria-label="Recensione successiva"', 'aria-label="Reseña siguiente"'),
        (
            'alt="Casa costruita da un\'impresa con il sistema Polistibrick"',
            'alt="Casa construida por una empresa con el sistema Polistibrick"',
        ),
        (
            'alt="Casa realizzata da un costruttore con il sistema Polistibrick"',
            'alt="Casa realizada por un constructor con el sistema Polistibrick"',
        ),
        (
            'alt="Programma di case realizzato da un\'impresa con il sistema Polistibrick"',
            'alt="Programa de casas realizado por una empresa con el sistema Polistibrick"',
        ),
        ('aria-label="Testimonianza precedente"', 'aria-label="Testimonio anterior"'),
        ('aria-label="Testimonianza successiva"', 'aria-label="Testimonio siguiente"'),
        ('aria-label="Testimonianza 1"', 'aria-label="Testimonio 1"'),
        ('aria-label="Testimonianza 2"', 'aria-label="Testimonio 2"'),
        ('aria-label="Testimonianza 3"', 'aria-label="Testimonio 3"'),
        ('<span class="wm-half wm-top">Contact</span>', '<span class="wm-half wm-top">Contacto</span>'),
        ('<span class="wm-half wm-bottom">Contact</span>', '<span class="wm-half wm-bottom">Contacto</span>'),
        ("Comparte tu experiencia con Polistibrick.</em> Publicado", "Comparte tu experiencia con Polistibrick. Publicado"),
        ("<label>La tua valutazione</label>", "<label>Su valoración</label>"),
        ('aria-label="Valutazione"', 'aria-label="Valoración"'),
        ('aria-label="1 stella"', 'aria-label="1 estrella"'),
        ('aria-label="2 stelle"', 'aria-label="2 estrellas"'),
        ('aria-label="3 stelle"', 'aria-label="3 estrellas"'),
        ('aria-label="4 stelle"', 'aria-label="4 estrellas"'),
        ('aria-label="5 stelle"', 'aria-label="5 estrellas"'),
        ("<label for=\"avisRole\">Sei</label>", "<label for=\"avisRole\">Usted es</label>"),
        ("<option>Auto-costruttore</option>", "<option>Autoconstructor</option>"),
        ("<option>Propietarioso</option>", "<option>Propietario</option>"),
        ("<label>Tipo recensione</label>", "<label>Tipo de reseña</label>"),
        ("✍️ Testo + foto", "✍️ Texto + foto"),
        ("<span id=\"avisMsgLabel\">La tua recensione</span>", "<span id=\"avisMsgLabel\">Su reseña</span>"),
        ('placeholder="Descrivi il tuo progetto e la tua esperienza…"', 'placeholder="Describa su proyecto y su experiencia…"'),
        ("msgLabel.textContent = 'La tua recensione (opzionale)'", "msgLabel.textContent = 'Su reseña (opcional)'"),
        ("msgLabel.textContent = 'La tua recensione'", "msgLabel.textContent = 'Su reseña'"),
    ],
}


def main():
    total = 0
    per_file = {}
    for rel, pairs in FILES.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        count = 0
        for old, new in pairs:
            if old == new:
                continue
            if old not in text:
                print(f"  SKIP (not found): {rel!r} … {old[:60]!r}")
                continue
            n = text.count(old)
            text = text.replace(old, new)
            count += n
        if count:
            path.write_text(text, encoding="utf-8")
        per_file[rel] = count
        total += count
        print(f"{rel}: {count} replacements")
    print(f"\nPASS2B TOTAL: {total}")
    return total


if __name__ == "__main__":
    main()
