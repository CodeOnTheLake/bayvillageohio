# Jen Halaska — Real Estate Website

Static site (plain HTML/CSS/JS) for [bayvillageohio.com](https://bayvillageohio.com). Hosted on GitHub Pages from the `main` branch, root folder. Rebuild after editing `_build/build.py` with `python3 _build/build.py`.

## Brand
Jen Halaska, REALTOR® (schema `alternateName`: Jennifer Halaska). Ohio License #2025007585. Bay Village resident serving Greater Cleveland, with a focus on out-of-town clients relocating to the west-side suburbs.

Own brand — no Howard Hanna theming. Brokerage is named only as a plain-text compliance line in the footer and on the About page: “Brokered by Howard Hanna Real Estate Services.”

Palette: warm white, charcoal, lake blue-gray. Fonts: Cormorant Garamond (headings) + Jost (body).

## Contact
- Primary: (330) 807-6374
- Office (secondary): (440) 793-0100
- No visible email on the site. Forms post through FormSubmit to `jhalaska0625@gmail.com` and redirect to `thank-you.html`. The first submission sends an activation email that must be clicked.

## Pages
Home, About, Relocation, Why Bay Village, Bay Village, Communities, Buy, Sell, Home Value, Vendors, Contact, Thank you, 404, plus `sitemap.xml`, `robots.txt` (AI bots allowed), and `llms.txt`.

Featured community cards (in this order): Bay Village, Rocky River, Westlake, Avon Lake, Avon, Lakewood. Photos are landmarks, lakefront, parks, or main streets — not houses. Sources and licenses are in `_build/IMAGE_CREDITS.md`.

## Still open
- Longer bio details on the About page
- Real vendor names (cards are placeholders)
- Swap in Jen’s own Bay Village photographs when available
- Testimonials omitted on purpose — add only real, approved reviews
- First FormSubmit activation click after a real form is submitted

## Domain & hosting
`CNAME` file must stay `bayvillageohio.com`.

GitHub Pages: branch `main`, folder `/` (root), custom domain `bayvillageohio.com`, then Enforce HTTPS once the certificate is approved.

GoDaddy DNS:
- A `@` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
- optional AAAA `@` → 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153
- CNAME `www` → `codeonthelake.github.io`
