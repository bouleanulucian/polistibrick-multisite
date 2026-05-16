# 🌍 Polistibrick Multi-site

Multi-country, multi-language website system for Polistibrick.
**One source repo → 7 country sites deployed to 7 domains.**

---

## 📁 Structure

```
polistibrick-multisite/
│
├── shared/                       ← COMMON: edit once, applied to all countries
│   ├── css/site.css              ← Shared CSS
│   ├── js/site.js                ← Shared JS (nav, gallery, etc.)
│   └── images/                   ← Shared images (logo, robot, products, etc.)
│
├── countries/                    ← Per-country sites (translated HTML)
│   ├── ro/                       → polistibrick.ro    (Romanian, current canonical)
│   ├── en/                       → polistibrick.com   (English — UK + EU)
│   ├── fr/                       → polistibrick.fr    (French)
│   ├── it/                       → polistibrick.it    (Italian)
│   ├── es/                       → polistibrick.es    (Spanish)
│   ├── nl/                       → polistibrick.be    (Dutch — Belgium)
│   └── de/                       → polistibrick.ch    (German — Switzerland)
│
│   Each country folder contains:
│   - _config.json                ← Country-specific data (phone, email, address, team)
│   - index.html, polistibrick-mercury-style.html, etc.
│   - All site pages (despre/, produse/, etc.)
│
├── translations/                 ← (Future) Language translation files
│
├── build/                        ← OUTPUT — auto-generated, ready to deploy
│   ├── ro/                       → Upload to polistibrick.ro hosting
│   ├── en/                       → Upload to polistibrick.com hosting
│   └── ...
│
└── build/build.py                ← Build script
```

---

## 🚀 Build & Deploy

### Build all countries
```bash
python3 build/build.py
```

### Build single country
```bash
python3 build/build.py ro
python3 build/build.py ro en fr
```

### What happens
1. Reads `countries/[country]/_config.json` for country data
2. Copies country HTML → `build/[country]/`
3. Copies `shared/` assets → `build/[country]/assets/` + `images/`
4. Replaces `{{placeholders}}` in HTML with config values
5. Generates `sitemap.xml` + `robots.txt`

---

## 🎨 Placeholder syntax

Anywhere in HTML, you can use `{{key.subkey}}` to inject config values.

Examples:
```html
<a href="tel:{{contact.phone_raw}}">{{contact.phone_display}}</a>
<a href="mailto:{{contact.email_general}}">{{contact.email_general}}</a>
<address>{{company.address_street}}, {{company.address_city}}</address>
```

Build script replaces these per country. RO build gets RO config, EN gets EN config, etc.

---

## 🌐 Domain mapping

| Country | Folder | Domain | Languages spoken |
|---|---|---|---|
| 🇷🇴 România | `countries/ro/` | polistibrick.ro | RO, EN |
| 🇬🇧 UK | `countries/en/` | polistibrick.com | EN |
| 🇫🇷 France | `countries/fr/` | polistibrick.fr | FR, EN |
| 🇮🇹 Italy | `countries/it/` | polistibrick.it | IT, EN |
| 🇪🇸 Spain | `countries/es/` | polistibrick.es | ES, EN |
| 🇧🇪 Belgium | `countries/nl/` | polistibrick.be | NL, FR, EN |
| 🇨🇭 Switzerland | `countries/de/` | polistibrick.ch | DE, FR, IT, EN |

---

## 📝 Adding a new country

1. Create folder: `countries/[code]/`
2. Copy `_config.json` from another country, fill in:
   - `lang`, `country`, `country_name`, `domain`, `domain_url`
   - `company.*` (legal name, VAT, address)
   - `contact.*` (phone, email, hours)
   - `team[]` (managers per country)
3. Copy HTML files from `countries/ro/` and translate text
4. Run: `python3 build/build.py [code]`
5. Upload `build/[code]/` to the country's domain hosting

---

## 🔄 Updating shared assets

Edit `shared/css/site.css`, `shared/js/site.js`, or `shared/images/*`.

Run `python3 build/build.py` → changes appear in **all 7 country builds**.

---

## 🌍 Deployment options

### Option A: Netlify (recommended)
- 1 Netlify site per country
- Each site's "base directory" = `build/[country]/`
- Each site's custom domain = country's domain (.ro, .fr, .it, etc.)
- Deploy on git push automatically

### Option B: GitHub Pages
- 1 GitHub repo per country
- Push `build/[country]/` to that repo's `gh-pages` branch
- Configure CNAME for custom domain

### Option C: Traditional FTP/SFTP
- Upload `build/[country]/` to country's web host
- Update on each change via FTP

---

## 🤝 Forms routing

Each country's forms (`/oferta/`, `/contact/`, `/devino-partener/`) post to that country's email
(`contact.form_submit_email` in `_config.json`).

- RO forms → `contact@polistibrick.ro`
- FR forms → `contact@polistibrick.fr`
- ES forms → `info@polistibrick.es`
- EN/BE/CH/IT forms → fallback to `contact@polistibrick.com`

CC always to `info@polistibrick.eu` for central tracking.

---

## 📚 Next steps

- [ ] Fill in real contact info in each `_config.json` (currently placeholders)
- [ ] Translate `countries/en/` HTML files from RO → EN
- [ ] Translate `countries/fr/`, `it/`, `es/`, `nl/`, `de/`
- [ ] Connect forms to backend (Netlify Forms, Formspree, etc.)
- [ ] Set up DNS for each domain to point to its hosting
- [ ] Add Google Analytics + Search Console per country
- [ ] (Optional) Add CMS for content editing (Decap CMS)
- [ ] (Optional) Build SEO agents (separate project)

---

## 🛠️ Tech stack

- **HTML/CSS/JS** static (no framework, no build step beyond placeholders)
- **Python 3** build script (zero dependencies, uses stdlib only)
- **Netlify** or **GitHub Pages** hosting (free)
- **DNS** per domain (Cloudflare, OVH, GoDaddy, etc.)

---

## 📞 Support

For questions about this setup, see `docs/` folder (TBD) or contact the developer.
