#!/usr/bin/env python3
"""Batch 2 Spanish translation for countries/es HTML files."""
from pathlib import Path

BASE = Path("countries/es")

def mr(text, pairs):
    for old, new in pairs:
        text = text.replace(old, new)
    return text

def translate_presupuesto(t):
    return t  # already Spanish

def translate_contact(t):
    return mr(t, [
        ("<title>Contactoooooo · Polistibrick — 9 países europeos</title>", "<title>Contacto · Polistibrick — 9 países europeos</title>"),
        ('content="Contactoooooez l\'équipe Polistibrick de votre pays. Sélectionnez le drapeau du pays où vous construisez et recevez le contact direct."',
         'content="Contacta con el equipo Polistibrick de tu país. Selecciona la bandera del país donde construyes y obtén el contacto directo."'),
        ("Contactooooo", "Contacto"),
        ("Contactoooooo", "Contacto"),
        ('aria-label="Sélectionnez le pays"', 'aria-label="Selecciona el país"'),
        ("<span>Espagne</span>", "<span>España</span>"),
        ("<span>Belgique</span>", "<span>Bélgica</span>"),
        ("<span>Italie</span>", "<span>Italia</span>"),
        ("<span>Autriche</span>", "<span>Austria</span>"),
        ("<span>Royaume-Uni</span>", "<span>Reino Unido</span>"),
        ("<h2>Des spécialistes <em>à un clic.</em></h2>", "<h2>Especialistas <em>a un clic.</em></h2>"),
        ("Nous répondons à vos questions techniques, préparons des devis personnalisés et offrons un conseil gratuit pour tout projet.",
         "Respondemos a tus preguntas técnicas, preparamos presupuestos personalizados y ofrecemos asesoramiento gratuito para cualquier proyecto."),
        ("Sélectionnez le pays où vous construisez pour voir le contact de l'équipe locale et lui envoyer votre message directement.",
         "Selecciona el país donde construyes para ver el contacto del equipo local y enviarle tu mensaje directamente."),
        ("<h3>Écrivez-nous directement.</h3>", "<h3>Escríbenos directamente.</h3>"),
        ("Votre message arrive directement à l'équipe du pays sélectionné.", "Tu mensaje llega directamente al equipo del país seleccionado."),
        ('for="cname">Nom *</label>', 'for="cname">Nombre *</label>'),
        ('placeholder="Votre nom"', 'placeholder="Tu nombre"'),
        ('placeholder="email@exemple.fr"', 'placeholder="email@ejemplo.es"'),
        ('for="crole">Vous êtes</label>', 'for="crole">Eres</label>'),
        ('<option value="">— Sélectionnez —</option>', '<option value="">— Selecciona —</option>'),
        ('<option value="architecte">Architecte</option>', '<option value="architecte">Arquitecto</option>'),
        ('<option value="bet">Bureau d\'études (BET)</option>', '<option value="bet">Oficina de estudios (BET)</option>'),
        ('<option value="constructeur">Constructeur / Entrepreneur</option>', '<option value="constructeur">Constructor / Empresa</option>'),
        ('<option value="particulier">Particulier / Propriétaire</option>', '<option value="particulier">Particular / Propietario</option>'),
        ('<option value="promoteur">Promoteur / Investisseur</option>', '<option value="promoteur">Promotor / Inversor</option>'),
        ('<option value="autre">Autre</option>', '<option value="autre">Otro</option>'),
        ('for="csubject">Sujet</label>', 'for="csubject">Asunto</label>'),
        ("<option>Demande de documentation</option>", "<option>Solicitud de documentación</option>"),
        ("<option>Support produit</option>", "<option>Soporte de producto</option>"),
        ("<option>Devenez partenaire</option>", "<option>Hazte socio</option>"),
        ("<option>Demande de devis</option>", "<option>Solicitud de presupuesto</option>"),
        ("<option>Autre</option>", "<option>Otro</option>"),
        ('for="cmsg">Message *</label>', 'for="cmsg">Mensaje *</label>'),
        ('placeholder="Comment pouvons-nous vous aider ?"', 'placeholder="¿Cómo podemos ayudarte?"'),
        ("PDF · DWG · DXF · JPG · PNG · ZIP — max 10 MB / fichier", "PDF · DWG · DXF · JPG · PNG · ZIP — máx. 10 MB / archivo"),
        ("Envoyer le message</button>", "Enviar mensaje</button>"),
        ("J'accepte que mes données soient traitées conformément à la <a href=\"../legal/privacidad/\" target=\"_blank\" rel=\"noopener\">politique de confidentialité (RGPD)</a>. *",
         "Acepto que mis datos sean tratados conforme a la <a href=\"../legal/privacidad/\" target=\"_blank\" rel=\"noopener\">política de privacidad (RGPD)</a>. *"),
        ("<h3>Message envoyé ✓</h3>", "<h3>Mensaje enviado ✓</h3>"),
        ("Merci ! Notre équipe vous répond sous 24 heures ouvrées.", "¡Gracias! Nuestro equipo te responde en un máximo de 24 horas laborables."),
        ("RO: { flag: '🇷🇴', name: 'Roumanie'", "RO: { flag: '🇷🇴', name: 'Rumanía'"),
        ("ES: { flag: '🇪🇸', name: 'Espagne'", "ES: { flag: '🇪🇸', name: 'España'"),
        ("FR: { flag: '🇫🇷', name: 'France'", "FR: { flag: '🇫🇷', name: 'Francia'"),
        ("BE: { flag: '🇧🇪', name: 'Belgique'", "BE: { flag: '🇧🇪', name: 'Bélgica'"),
        ("IT: { flag: '🇮🇹', name: 'Italie'", "IT: { flag: '🇮🇹', name: 'Italia'"),
        ("AT: { flag: '🇦🇹', name: 'Autriche'", "AT: { flag: '🇦🇹', name: 'Austria'"),
        ("GB: { flag: '🇬🇧', name: 'Royaume-Uni'", "GB: { flag: '🇬🇧', name: 'Reino Unido'"),
        ("badge: 'Siège RO'", "badge: 'Sede RO'"),
        ("badge: 'Siège ES'", "badge: 'Sede ES'"),
        ("badge: 'Siège FR'", "badge: 'Sede FR'"),
        ("badge: 'Siège BE'", "badge: 'Sede BE'"),
        ("badge: 'Siège IT'", "badge: 'Sede IT'"),
        ("badge: 'En ligne'", "badge: 'En línea'"),
        ("badge: 'En ligne · Support RO'", "badge: 'En línea · Soporte RO'"),
        ("address: 'Contact via formulaire en ligne<br>ou via polistibrick.at'", "address: 'Contacto mediante formulario en línea<br>o vía polistibrick.at'"),
        ("city: 'Servi depuis la Roumanie'", "city: 'Atendido desde Rumanía'"),
        ("address: 'Contact via polistibrick.uk<br>ou directement depuis la Roumanie'", "address: 'Contacto vía polistibrick.uk<br>o directamente desde Rumanía'"),
        ('aria-label="Supprimer"', 'aria-label="Eliminar"'),
        ('alert(`Le fichier "${file.name}" est trop volumineux', 'alert(`El archivo "${file.name}" es demasiado grande'),
        ("Maximum 10 MB par fichier.`);", "Máximo 10 MB por archivo.`);"),
        ("if (subjectSelect.options[i].text === 'Demande de documentation')", "if (subjectSelect.options[i].text === 'Solicitud de documentación')"),
        ("else if (role === 'bet') roleText = 'bureau d\\'études (BET)';", "else if (role === 'bet') roleText = 'oficina de estudios (BET)';"),
        ("else if (role === 'constructeur') roleText = 'constructeur';", "else if (role === 'constructeur') roleText = 'constructor';"),
        ("else if (role === 'promoteur') roleText = 'promoteur / investisseur';", "else if (role === 'promoteur') roleText = 'promotor / inversor';"),
        ("msg = 'Bonjour,\\n\\nEn tant que ' + roleText + ', je souhaite recevoir le document suivant :\\n\\n• ' + doc + '\\n\\nMerci d\\'avance.';",
         "msg = 'Hola,\\n\\nComo ' + roleText + ', deseo recibir el siguiente documento:\\n\\n• ' + doc + '\\n\\nGracias de antemano.';"),
        ("msg = 'Bonjour,\\n\\nJe souhaite recevoir le document suivant :\\n\\n• ' + doc + '\\n\\nMerci d\\'avance.';",
         "msg = 'Hola,\\n\\nDeseo recibir el siguiente documento:\\n\\n• ' + doc + '\\n\\nGracias de antemano.';"),
        ("msg = 'Bonjour,\\n\\nDemande : ' + subject + '\\n\\nMerci d\\'avance.';",
         "msg = 'Hola,\\n\\nSolicitud: ' + subject + '\\n\\nGracias de antemano.';"),
    ])

# Import extended translations from companion module if present
try:
    from _translate_batch2_ext import EXTRA_FILES
    FILES = {
        "presupuesto/index.html": translate_presupuesto,
        "contact/index.html": translate_contact,
        **EXTRA_FILES,
    }
except ImportError:
    FILES = {
        "presupuesto/index.html": translate_presupuesto,
        "contact/index.html": translate_contact,
    }

if __name__ == "__main__":
    for rel, fn in FILES.items():
        p = BASE / rel
        t = p.read_text(encoding='utf-8')
        p.write_text(fn(t), encoding='utf-8')
        print(f"OK {rel}")
