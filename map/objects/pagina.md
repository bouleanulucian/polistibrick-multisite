---
type: object
cluster: continut
universe: live
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
entity: countries/<cod>/**/index.html
---

# Pagină

O pagină = un `index.html` într-un folder al țării. Nav-ul și footer-ul NU sunt în pagină: sunt monturi `data-include` umplute la build din `shared/js/site.js` (`build/build.py:276-290`).

## De ce are forma asta

HTML static, o pagină pe folder, URL-uri în limba țării (SEO local). CSS-ul specific unei secțiuni stă inline în pagină (`<style>` lângă secțiune), ca secțiunea să poată fi mutată sau ștearsă fără să atingă `site.css`.

## Forma (FR ca referință; RO are aceleași tipuri, cu foldere în română)

| Tip | FR | RO | Ce are înăuntru |
|---|---|---|---|
| acasă | `countries/fr/index.html` | `countries/ro/index.html` | eroul `.h4` `#heroSection` (`:509`, stilul `#hero4` `:113`); **doar FR:** `#livrable` „un seul coffrage" (`:561`); video „Dans le mur" `#cinq` (`:649`), `#cinqVideo` (`:655`), replica roșie `#cinqReplica` (`:662`) |
| catalog | `projets/` | `proiecte/` | 48 de modele: card `.case-photo` (`projets/index.html:374`), pilula `.var-nota` „prix du système seul" (`:385`), fișa `#detail-N` (`:389`), popup `#notaModal` cu butonul „Voir tout le projet" |
| produse, prețuri | `produits/`, `prix/` | `produse/`, `preturi/` | cele trei sisteme (Polistibrick, Polistiwall, PolistiSIP) |
| pentru cine | `pour/` | `pentru/` | proprietari, arhitecți, constructori, investitori |
| ofertă | `devis/` | `oferta/` | iframe spre app-ul de devize (alt repo); URL-ul în `_config.json` → `devis_app` (`countries/fr/_config.json:81`), lipit de `shared/js/devis-embed.js` |
| legal | `legal/conditions`, `legal/mentions-legales`, `legal/confidentialite` | `legal/termeni`, … | clauze cu planurile trimise; medierea CM2C (doar FR) |
| presă | 6 foldere la rădăcina `countries/fr/` | — | articole identice cu site-ul vechi |
| montaj, resurse, contact, partener, despre, economii | `montage/`, `ressources/`, `contact/`, `devenir-partenaire/`, `a-propos/`, `economies/` | `montaj/`, `resurse/`, `contact/`, `devino-partener/`, `despre/`, `economii/` | |
| tehnice | `404.html`, `llms.txt`, `_redirects` (FR) | `404.html`, `llms.txt`, `favicon.ico` | |

Placeholder-ele `{{cheie.subcheie}}` din pagini se umplu din `_config.json` (`build/build.py:72-110`). Datele structurate: `scripts/date-structurate.py` (34 de pagini RO îl citează în comentarii).

## Legat de

- **deținut de:** `tara.md`
- **se leagă cu:** `sablon-partajat.md` (nav/footer intră la build), `config-tara.md` (placeholders), `imagini.md`, `model-casa.md` (catalogul)
- **seamănă dar nu e:** `build/<cod>/**/index.html` — produsul, cu nav/footer deja lipite; nu se editează

## Dacă schimbi asta

- **Mișcă:** doar pagina aceea a țării aceleia; sitemap-ul (lastmod din git log, `build/build.py:364`).
- **Nu mișcă:** aceeași pagină în cealaltă limbă (copie separată, se schimbă de mână); nav/footer (vezi `sablon-partajat.md`).

## Suprafețe

| Cine | Rol |
|---|---|
| Claude / Cursor | scriu |
| `build/build.py` | transformă (placeholders, nav/footer, SEO, optimizări) |
| patronul | vede pe local înainte de publicare |

## Vezi

- Sursa: `countries/fr/index.html`, `countries/fr/projets/index.html`
