> **Referință din 04.07.2026.** Procesul actual de publicare e în `map/processes/publica.md` (RO automat la push pe `main`, FR prin `gh workflow run`). Secțiunea 2 privește app-ul de devize, care e alt repo (`polistibrick-devis-app`). Portul 8080 / `dev-local.sh` nu se mai folosesc — vezi `map/objects/previzualizare-locala.md`.

# Polistibrick — Ghid deploy (pentru cine publică)

Proiectul constă din **două părți** create local de dezvoltator. Ambele trebuie publicate.

| Parte | Folder | Ce e |
|-------|--------|------|
| **Site static** | `polistibrick-multisite/` | HTML RO, FR, … (marketing, pagini) |
| **App devis AI** | `polistibrick-devis-app/` | Next.js — oferte, planuri, PDF, email |

---

## 1. Site static (Cloudflare Pages recomandat)

```bash
cd polistibrick-multisite
python3 build/build.py ro    # → build/ro/
python3 build/build.py fr    # → build/fr/
```

**Deploy:**
- `build/ro/` → `polistibrick.ro` (Cloudflare Pages, output dir = `build/ro`)
- `build/fr/` → `polistibrick.fr`

**După deploy — completează în `_config.json` (sursă, apoi rebuild):**
- `forms.access_key` — Web3Forms (formular contact RO)
- date firmă / echipă dacă lipsesc

**Pagini cu app devis integrat (iframe):**
- RO: `/oferta/`
- FR: `/devis/`

URL app în config (`devis_app.url`) — vezi secțiunea 2.

---

## 2. App devis (Vercel recomandat)

```bash
cd polistibrick-devis-app
npm install
npm run build    # trebuie să treacă fără erori
```

**Import proiect Vercel** → framework Next.js → root = acest folder.

### Variabile de mediu (obligatorii în Vercel Dashboard)

| Variabilă | Descriere |
|-----------|-----------|
| `ANTHROPIC_API_KEY` | Chat + analiză planuri |
| `RESEND_API_KEY` | Trimitere email PDF |
| `LEAD_EMAIL` | Adresa care primește lead-urile (ex. devis@…) |
| `FROM_EMAIL` | Expeditor verificat în Resend (ex. `Polistibrick Devis <devis@polistibrick.fr>`) |

Opțional: `ANTHROPIC_MODEL`, `ANTHROPIC_CHAT_MODEL`, `ANTHROPIC_VISION_MODEL`

### Subdomenii DNS

| Țară | App URL | Actualizează în |
|------|---------|-----------------|
| RO | `https://devis.polistibrick.ro` | `countries/ro/_config.json` → `devis_app.url` |
| FR | `https://devis.polistibrick.fr` | `countries/fr/_config.json` → `devis_app.url` |

După schimbare URL → **rebuild site** (secțiunea 1).

### Python (planuri DXF/DWG)

App folosește `scripts/prepare_plan.py` pentru convertire planuri.
- Pe **Vercel**: verificați că Python 3 e disponibil sau folosiți **Docker / VPS** dacă upload planuri e critic.
- Alternativ: deploy app pe **Railway / Fly.io** cu Python în imagine.

---

## 3. Verificare după deploy

- [ ] `https://polistibrick.ro/oferta/` — iframe încarcă app devis
- [ ] `https://polistibrick.fr/devis/` — idem, limba FR
- [ ] Parcurgeți wizard → PDF → email la `LEAD_EMAIL`
- [ ] Formular contact RO trimite (Web3Forms key setat)
- [ ] SSL activ pe toate subdomeniile

---

## 4. Development local (referință)

```bash
./scripts/dev-local.sh ro
```

- Site: http://localhost:8080/oferta/ (RO) sau /devis/ (FR)
- App: http://localhost:3100 (iframe detectează localhost automat)

---

## 5. MCP (Cursor — opțional, pentru SEO/conținut)

```bash
cd polistibrick-multisite/mcp
pip install -r requirements.txt
```

Config Cursor: `.cursor/mcp.json` (deja în repo).

---

## Contact tehnic

- Site: structură `countries/[cod]/`, build `build/build.py`
- App: README în `polistibrick-devis-app/README.md`
- Integrare: `shared/js/devis-embed.js`, `_archive/pre-multisite/apps/README.md`
