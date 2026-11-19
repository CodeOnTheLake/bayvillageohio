# Jennifer Halaska — Real Estate Website

Static site (plain HTML/CSS/JS, no build step needed to host). Ready for GitHub Pages.

## Pages
index, about, bay-village, areas (Communities), buyers, sellers, home-value, vendors, contact, 404 + sitemap.xml, robots.txt.

## Editing
All pages are generated from `_build/build.py` (shared header/footer, SEO tags, schema).
Edit the CONFIG block at the top, then run: `python3 _build/build.py`.
(You can also edit the HTML files directly; re-running the build overwrites them.)

## Placeholders to fill before launch
- `EMAIL` / `EMAIL_SHOWN` — Jennifer's email (not on her Howard Hanna page).
- `LICENSE` — Ohio license number (footer).
- Phone: primary (330) 807-6374 (Jennifer), secondary office (440) 793-0100.
- `FORMSPREE` — create a free form at formspree.io and paste the form ID. Until then the form falls back to mailto.
- About page bio details ([add bio details]).
- Recommended Vendors: 2 placeholder cards per category (search for "PLACEHOLDER").
- Vendor disclosure language — confirm with brokerage compliance (RESPA).
- Testimonials intentionally omitted (add only real, approved reviews).

## Domain & hosting
Live domain: https://bayvillageohio.com (SITE_URL in _build/build.py). `CNAME` file contains `bayvillageohio.com`.
GitHub Pages: deploy from branch `main`, folder `/ (root)`, custom domain `bayvillageohio.com`, then Enforce HTTPS.
GoDaddy DNS: A @ -> 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153;
optional AAAA @ -> 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153;
CNAME www -> codeonthelake.github.io. Remove GoDaddy's default parked A record / forwarding for @.

## Brand
Own brand (no brokerage theming): wordmark "JENNIFER HALASKA / Real Estate · Bay Village, Ohio",
palette warm white #faf8f4, stone #f1ede6, charcoal #1f2326, lake blue-gray accent #5d7686.
Fonts: Cormorant Garamond (headings) + Jost (body) via Google Fonts.
Brokerage named only in plain text in the footer and on the About page (compliance).

## Image credits (Unsplash License)
- Hero / Lakewood card / OG image: AI-edited (mirrored, people removed, converted to daylight, 2x EDSR upscale to 2560x1440) from a Lake Erie photo (Edgewater Dr, Lakewood OH) by Dan Crile — https://unsplash.com/photos/cKwfDLa5XXw
- Bay Village card, Bay Village & Home Value headers, value band: Megs Harrison — https://unsplash.com/photos/Dq3b6rRN6GM
- Avon Lake card: Megs Harrison — https://unsplash.com/photos/rZB9PkayhJQ
- Rocky River card: Ally Griffin (Rocky River, OH) — https://unsplash.com/photos/Fd6k4VZR9JA
- Greater Cleveland card: DJ Johnson (Edgewater Beach, Cleveland) — https://unsplash.com/photos/qQLg8lPYU1k
- Westlake card: Josh Lemmon (generic home, location not stated) — https://unsplash.com/photos/CnbbCRH71Wg
- Headshot: from Jennifer's brokerage agent profile.
