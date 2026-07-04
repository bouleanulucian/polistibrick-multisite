# Aplicații Polistibrick (lângă multisite)

## polistibrick-devis-app

Configurator AI de oferte / devis (Next.js 14).

**Locație:** `../polistibrick-devis-app` (sibling folder, nu în interiorul site-ului static)

### Development local (site + app)

Terminal 1 — app devis:

```bash
cd "../polistibrick-devis-app"
npm install
npm run dev
# → http://localhost:3100
```

Terminal 2 — site RO sau FR:

```bash
python3 build/build.py ro
cd build/ro && python3 -m http.server 8080
# → http://localhost:8080/oferta/
```

Pe localhost, pagina `/oferta/` (RO) sau `/devis/` (FR) încarcă automat app-ul de pe port **3100**.

### Production

1. Deploy app Next.js (Vercel, Railway, VPS) pe:
   - `https://devis.polistibrick.ro` (RO)
   - `https://devis.polistibrick.fr` (FR)
2. URL-urile sunt în `countries/ro/_config.json` și `countries/fr/_config.json` → `devis_app.url`
3. Rebuild site: `python3 build/build.py ro fr`

### Variabile de mediu (app)

- `ANTHROPIC_API_KEY` — chat + analiză planuri
- `RESEND_API_KEY` — trimitere email PDF
- `LEAD_EMAIL` / `FROM_EMAIL` — destinatar lead-uri
