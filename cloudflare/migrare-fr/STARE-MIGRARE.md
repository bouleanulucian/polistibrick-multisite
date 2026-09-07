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

## 07.09.2026 — procedura reluată de la cap (Claude)
- Stare: NEschimbat. AFNIC: nserver ns01/ns02.one.com, last-update 28.02.2026. Cloudflare: zona `pending`
  (anita/owen), cele 9 înregistrări DNS puse (MX Google ×5, SPF, DMARC, apex+www → pages.dev), domeniile
  Pages `pending`. polistibrick.fr servește încă site-ul vechi de pe Hetzner (49.12.212.73).
- Panoul One.com, verificat din nou în Chrome-ul patronului: planul e «Domaine uniquement»; pagina DNS a
  domeniului arată DOAR «Mettre à niveau pour créer une redirection» — fără tab de nameservere. Deci
  ruta din panou (Paramètres avancés → Configuration DNS → Serveurs de noms) NU există pentru acest plan.
- Ruta oficială One.com când panoul nu oferă opțiunea: formularul PDF «Request to change name servers»
  (help.one.com, articolul 360000841638), semnat CU PIXUL de registrant (Lucian Bouleanu), scanat, trimis
  la sales@one.com. Răspuns în 24 h, procesare până la 3 zile lucrătoare. Formularul completat:
  scratchpad-ul sesiunii + trimis patronului pe 07.09.
- De ce a picat încercarea din panou din 02.09: One.com trimite un e-mail de aprobare REGISTRANTULUI când
  datele lui diferă de ale abonatului — iar e-mailul registrantului e proxy-ul Wix
  (polistibrick.fr@wix-domains.com). Formularul semnat ocolește acest e-mail.
- CAPCANĂ găsită: domeniul are DNSSEC activ la AFNIC (DS 63650 13 2 …). Dacă nameserverele s-ar schimba
  fără scoaterea DS-ului, site + poștă ar da SERVFAIL. One.com documentează că DNSSEC se dezactivează
  automat la trecerea pe nameservere externe; în e-mailul către One.com se cere explicit și scoaterea DS.
  După schimbare, verificare obligatorie: `dig +short DS polistibrick.fr @8.8.8.8` trebuie să fie GOL
  (apoi, opțional, DNSSEC se reactivează din Cloudflare, cu DS pus la One.com — tab «DS Records»).
- Zona veche mai are `sel1._domainkey` → CNAME Wix (DKIM vechi, inutil): nu se reproduce.
