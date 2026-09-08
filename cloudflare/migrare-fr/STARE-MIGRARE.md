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

## 08.09.2026 — audit total, procedură cu procedură (la cererea patronului; colegul zice «a transferat tot»)
| Pas | Stare | Dovadă |
|---|---|---|
| Registrar | One.com A/S (transferul de la Wix e făcut, last-update 28.02.2026) | whois AFNIC |
| Nameservere la AFNIC | ns01/ns02.one.com — NEschimbate | `dig NS @d.nic.fr` |
| Ce vede lumea | ns01/ns02.one.com la 8.8.8.8, 1.1.1.1, 9.9.9.9, OpenDNS; A → 49.12.212.73 | dig |
| DNSSEC | ACTIV (DS 63650 13 2; flag `ad`) — DS trebuie scos la schimbare | `dig DS @d.nic.fr`, `dig +dnssec` |
| Contactul titularului | AFNIC: `reachstatus: not identified` pe un contact → e-mailul titularului nu e confirmat (releul Wix) | whois |
| Panou One.com | plan «Domaine uniquement»; DNS = doar «Mettre à niveau»; fără tab nameservere; clickurile extensiei nu deschid meniurile | Chrome |
| Jurnal One.com | nicio cerere de nameservere; ultimele acțiuni = DNS Resend 19.06.2026 (IP francez, cont bouleanu.lc) | Chrome |
| Cloudflare zonă | `pending`, anita/owen, 9 înregistrări (MX×5, SPF, DMARC, apex+www) | API |
| Cloudflare Pages | polistibrick-fr, deploy fbeb7f6 din 04.09 = conținutul curent; domeniile pending | API |
| Site nou | polistibrick-fr.pages.dev 200, secțiunea nouă prezentă | curl |
| Site vechi | polistibrick.fr 200 de pe Hetzner 49.12.212.73 | curl |
| Poșta | MX Google ×5 + SPF, identice la One.com și Cloudflare | dig / API |

**GĂSIT: 8 înregistrări lipsă din zona Cloudflare** (vezi completarea din dns-snapshot-inainte.txt): Resend
(send TXT+MX, resend._domainkey) = e-mailurile cu oferte din app-ul de devize; SendGrid ×4; DKIM Wix.
Adăugarea lor prin API a fost BLOCATĂ de clasificatorul de permisiuni (scriere într-un cont extern) →
cerut acordul patronului; lista gata de rulat: scratchpad `onecom-ns/inregistrari-lipsa-cloudflare.json`.
Concluzia auditului: «a transferat tot» = transferul registrarului (Wix → One.com, februarie). Schimbarea
nameserverelor e o operațiune separată care nu a fost făcută niciodată; singura cale = formularul PDF semnat.
