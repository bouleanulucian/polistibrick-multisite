# Migrarea polistibrick.fr — starea la 01.09.2026, seara

FĂCUT (Claude, prin API cu tokenul «migrare-fr-claude», păstrat în Keychain-ul Mac-ului
ca `cf-migrare-fr`; formularul de onboarding din dashboard pica, s-a lucrat prin API):
1. Site-ul nou construit și publicat: https://polistibrick-fr.pages.dev (proiect polistibrick-fr,
   ramura git `lansare-fr` — NU s-a atins România).
2. Zona polistibrick.fr creată în Cloudflare — zone_id 8b22ea965e118ec296ca44c4c393e5e1,
   nameservere: anita.ns.cloudflare.com + owen.ns.cloudflare.com. Status: PENDING până la pasul de mai jos.
3. Înregistrări DNS puse: cele 5 MX Google + SPF (identice cu zona veche, poșta nu se atinge),
   DMARC p=none cu rapoartele la contact@polistibrick.fr (înainte mergeau la vali.email),
   apex + www → CNAME polistibrick-fr.pages.dev (prin proxy).
4. Domeniile polistibrick.fr + www legate de proiectul Pages (status «initializing» până la activare).

RĂMAS — UN SINGUR PAS, AL PATRONULUI (One.com cere parola lui):
  one.com → Panneau de Configuration → domeniul polistibrick.fr → Nameservers / DNS →
  «utiliser des serveurs de noms personnalisés» și pune EXACT:
      anita.ns.cloudflare.com
      owen.ns.cloudflare.com
  Restul se activează singur în 1–4 ore (site nou live + poșta neschimbată). Claude verifică după.

ÎNTOARCEREA din orice problemă: la One.com se pun înapoi ns01.one.com + ns02.one.com —
site-ul vechi de pe Hetzner (49.12.212.73) e neatins și totul revine ca înainte.
