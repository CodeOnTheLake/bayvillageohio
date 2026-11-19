#!/usr/bin/env python3
"""Generates the static site. Edit CONFIG, then run: python3 _build/build.py
Output is plain HTML/CSS/JS (no build step needed to host on GitHub Pages)."""
import json, os, datetime, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------- CONFIG (replace placeholders) ----------------
SITE_URL    = "https://bayvillageohio.com"      # live domain (GoDaddy) — used in canonical/OG/schema/sitemap/robots
FORM_EMAIL  = "jhalaska0625@gmail.com"          # FormSubmit delivery address (never shown as text on the site)
FORM_ACTION = "https://formsubmit.co/" + FORM_EMAIL  # FormSubmit endpoint (activate via one-time email on first submission)
PHONE_DISP  = "(330) 807-6374"                  # Jen's direct phone (primary)
PHONE_TEL   = "+13308076374"
OFFICE_DISP = "(440) 793-0100"                  # brokerage office line (secondary)
OFFICE_TEL  = "+14407930100"
LICENSE     = "2025007585"                       # Ohio real estate license number
BROKERAGE   = "Howard Hanna Real Estate Services"   # compliance mention (plain text, footer + About only)
SEARCH_URL  = "https://jenniferhalaska.howardhanna.com/"  # REAL: her listing-search page
OFFICE = {"street":"2055 Crocker Rd., Suite 101","city":"Westlake","region":"OH","zip":"44145"}
# ---------------------------------------------------------------

NAV = [("about.html","About"),("relocation.html","Relocation"),("bay-village.html","Bay Village"),("areas.html","Communities"),
       ("buyers.html","Buy"),("sellers.html","Sell"),("vendors.html","Vendors"),("contact.html","Contact")]

CREDITS = [
 ("Hero image","Dan Crile","https://unsplash.com/@dancrile","https://unsplash.com/photos/cKwfDLa5XXw"),
 ("Sunset over the water","Megs Harrison","https://unsplash.com/@mharrisonphotography","https://unsplash.com/photos/Dq3b6rRN6GM"),
 ("Cleveland skyline from Edgewater Beach","DJ Johnson","https://unsplash.com/@dj_johns1","https://unsplash.com/photos/qQLg8lPYU1k"),
 ("Huntington Beach at sunrise, Bay Village (CC BY 2.0)","Erik Drost","https://www.flickr.com/photos/edrost88/","https://commons.wikimedia.org/wiki/File:Brown_sunrise_at_Huntington_Beach.jpg"),
 ("Rocky River Reservation hike/bike bridge (CC BY-SA 4.0)","Chris Light","https://commons.wikimedia.org/wiki/User:CLight","https://commons.wikimedia.org/wiki/File:Rocky_River_Reservation_PC270039_nr_Little_Cedar_Point.JPG"),
 ("Crocker Park, Westlake (public domain)","Darryl Whitehead","https://commons.wikimedia.org/wiki/File:Crocker_Summer_080_(2).jpg","https://commons.wikimedia.org/wiki/File:Crocker_Summer_080_(2).jpg"),
 ("Sunset at Veterans Park, Avon Lake (CC BY-SA 3.0)","Robert Chriss","https://commons.wikimedia.org/wiki/File:Sunset_at_Veterans_Park_AL.JPG","https://commons.wikimedia.org/wiki/File:Sunset_at_Veterans_Park_AL.JPG"),
 ("Historic Town Hall at French Creek, Avon (CC BY-SA 4.0)","Tiburd","https://commons.wikimedia.org/wiki/User:Tiburd","https://commons.wikimedia.org/wiki/File:Avon_Town_Hall,_Avon,_Ohio_01.jpg"),
 ("Solstice Steps at Lakewood Park (CC BY-SA 4.0)","Drawing With Light","https://commons.wikimedia.org/wiki/User:Drawing_With_Light","https://commons.wikimedia.org/wiki/File:Solstice_Steps_Sunset.jpg"),
]

def pic(name, alt, cls, eager=False, w=2400, h=1400):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<picture><source srcset="assets/img/{name}.webp" type="image/webp"><img class="{cls}" src="assets/img/{name}.jpg" width="{w}" height="{h}" alt="{alt}" {load} decoding="async"></picture>'

AREAS_SERVED = ["Bay Village","Westlake","Rocky River","Avon Lake","Lakewood","Fairview Park","North Olmsted","Avon","Cleveland"]
LICENSE_LD = {"@type":"EducationalOccupationalCredential","credentialCategory":"license","name":"Ohio Real Estate License","identifier":LICENSE,
              "recognizedBy":{"@type":"GovernmentOrganization","name":"Ohio Department of Commerce, Division of Real Estate & Professional Licensing"}}
def schema(extra=None):
    biz = {"@type":["RealEstateAgent","LocalBusiness"],"@id":SITE_URL+"/#business",
      "name":"Jen Halaska, REALTOR®","alternateName":["Jennifer Halaska","Jen Halaska Real Estate"],
      "description":"Bay Village, Ohio REALTOR® specializing in out-of-town buyers and families relocating to Cleveland: matching newcomers to the right suburb, then the right home.",
      "url":SITE_URL+"/","image":SITE_URL+"/assets/img/jennifer-halaska-realtor-bay-village.jpg","logo":SITE_URL+"/assets/img/favicon.svg",
      "telephone":PHONE_TEL,
      "contactPoint":[{"@type":"ContactPoint","telephone":PHONE_TEL,"contactType":"sales","areaServed":"US-OH","availableLanguage":"English"},{"@type":"ContactPoint","telephone":OFFICE_TEL,"contactType":"office"}],
      "address":{"@type":"PostalAddress","streetAddress":OFFICE["street"],"addressLocality":OFFICE["city"],"addressRegion":OFFICE["region"],"postalCode":OFFICE["zip"],"addressCountry":"US"},
      "areaServed":[{"@type":"City","name":c+", OH"} for c in AREAS_SERVED]+[{"@type":"AdministrativeArea","name":"Cuyahoga County, OH"},{"@type":"AdministrativeArea","name":"Lorain County, OH"}],
      "employee":{"@id":SITE_URL+"/#jen"},"parentOrganization":{"@type":"Organization","name":BROKERAGE},
      "knowsAbout":["Relocating to Cleveland, Ohio","Moving to Cleveland","Best Cleveland suburbs for families","West side Cleveland suburbs","Bay Village real estate","Home valuation"],
      "sameAs":[SEARCH_URL]}
    person = {"@type":"Person","@id":SITE_URL+"/#jen","name":"Jen Halaska","alternateName":"Jennifer Halaska","jobTitle":"REALTOR®",
      "url":SITE_URL+"/about.html","image":SITE_URL+"/assets/img/jennifer-halaska-realtor-bay-village.jpg","telephone":PHONE_TEL,
      "homeLocation":{"@type":"Place","name":"Bay Village, Ohio"},"worksFor":{"@type":"Organization","name":BROKERAGE},
      "hasCredential":LICENSE_LD,"knowsAbout":biz["knowsAbout"]}
    site = {"@type":"WebSite","@id":SITE_URL+"/#website","url":SITE_URL+"/","name":"Jen Halaska | Bay Village & Cleveland Relocation Real Estate","inLanguage":"en-US","publisher":{"@id":SITE_URL+"/#business"}}
    out=[{"@context":"https://schema.org","@graph":[biz,person,site]}]
    if extra: out += (extra if isinstance(extra,list) else [extra])
    return "\n".join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>' for x in out)

def faq_ld(qs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub(r"<[^>]+>","",a)}} for q,a in qs]}
def faq_html(qs, title="Frequently asked questions"):
    items="".join(f'<div class="faq-item"><h2 class="q">{q}</h2><p>{a}</p></div>' for q,a in qs)
    return f'<section class="bg-white faq"><div class="container narrow"><span class="kicker">FAQ</span><div class="rule"></div><p class="faq-title">{title}</p>{items}</div></section>'

PRELOAD = {"index.html":"hero-lake-erie-daylight","why-bay-village.html":"hero-lake-erie-daylight","bay-village.html":"lake-erie-sunset-shore","home-value.html":"lake-erie-sunset-shore","relocation.html":"relocation-cleveland-skyline"}

def crumbs_ld(name,path):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":SITE_URL+"/"},
      {"@type":"ListItem","position":2,"name":name,"item":SITE_URL+"/"+path}]}

def wordmark(tag="a"):
    return '<a class="wordmark" href="index.html" aria-label="Jen Halaska Real Estate — home"><span class="wm-name">Jen Halaska</span><span class="wm-sub">Real Estate · Bay Village, Ohio</span></a>'

def head(path,title,desc,extra=None,body_class="",robots="index, follow"):
    url = SITE_URL+"/"+("" if path=="index.html" else path)
    navl = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==path else ""}>{n}</a></li>' for h,n in NAV)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#1f2326">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Jen Halaska Real Estate">
<meta name="author" content="Jen Halaska">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta name="geo.region" content="US-OH"><meta name="geo.placename" content="Bay Village">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
{f'<link rel="preload" as="image" href="assets/img/{PRELOAD[path]}.webp" type="image/webp" fetchpriority="high">' if path in PRELOAD else ''}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
{schema(extra)}
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
 <nav class="container nav" aria-label="Main">
  {wordmark()}
  <ul class="nav-links" id="nav-links">{navl}</ul>
  <div class="nav-cta">
   <a class="btn btn-outline btn-sm" href="tel:{PHONE_TEL}">{PHONE_DISP}</a>
   <a class="btn btn-dark btn-sm" href="home-value.html">Home Value</a>
   <button class="menu-btn" aria-expanded="false" aria-controls="nav-links">Menu</button>
  </div>
 </nav>
</header>
<main id="main">
'''

def foot():
    cr = " · ".join(f'{t}: <a href="{u}" rel="noopener" target="_blank">{n}</a>' for t,n,_,u in CREDITS)
    return f'''</main>
<footer class="site-footer">
 <div class="container">
  <div class="footer-top">
   {wordmark()}
   <div class="btn-row" style="margin:0"><a class="btn btn-white btn-sm" href="contact.html">Contact Jen</a><a class="btn btn-ghost-light btn-sm" href="home-value.html">What's my home worth?</a></div>
  </div>
  <div class="footer-grid">
   <div>
    <h3>Jen Halaska, REALTOR®</h3>
    <p>Bay Village realtor and relocation specialist, helping out-of-town buyers and families moving to Cleveland find the right suburb and the right home.</p>
    <p>{OFFICE["street"]}<br>{OFFICE["city"]}, {OFFICE["region"]} {OFFICE["zip"]}</p>
   </div>
   <div>
    <h3>Contact</h3>
    <ul>
     <li><a href="tel:{PHONE_TEL}">{PHONE_DISP}</a></li>
     <li><a href="tel:{OFFICE_TEL}" style="color:#b7bdc2">Office: {OFFICE_DISP}</a></li>
     <li><a href="contact.html">Send a message</a></li>
     <li><a href="contact.html?topic=Consultation#contact-form">Schedule a consultation</a></li>
     <li><a href="{SEARCH_URL}" target="_blank" rel="noopener">Search homes for sale ↗</a></li>
    </ul>
   </div>
   <div>
    <h3>Explore</h3>
    <ul><li><a href="index.html">Home</a></li>{"".join(f'<li><a href="{h}">{n}</a></li>' for h,n in NAV)}<li><a href="why-bay-village.html">Why Bay Village</a></li><li><a href="home-value.html">Home Value</a></li></ul>
   </div>
  </div>
  <div class="legal">
   <span>© <span id="year">{datetime.date.today().year}</span> Jen Halaska, REALTOR®. Brokered by {BROKERAGE}. Ohio License #{LICENSE}.</span>
   <span>Equal Housing Opportunity. Information deemed reliable but not guaranteed.</span>
  </div>
  <p class="credits">Photography credits — {cr}. Full source and license notes: <a href="https://github.com/CodeOnTheLake/bayvillageohio/blob/main/_build/IMAGE_CREDITS.md">image credits</a>.</p>
 </div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''

def page_hero(kicker,h1,lead,crumb,img=None,alt=""):
    if img:
        return f'''<section class="page-hero has-img">{pic(img,alt,"ph-img",True)}<div class="container"><div class="crumbs"><a href="index.html">Home</a> / {crumb}</div><span class="kicker">{kicker}</span><h1>{h1}</h1><p class="lead">{lead}</p></div></section>'''
    return f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="index.html">Home</a> / {crumb}</div><span class="kicker">{kicker}</span><h1>{h1}</h1><p class="lead">{lead}</p></div></section>'''

def cta(h="Let's talk about your next move.", p="A relaxed, no-pressure conversation about your goals, timing and options."):
    return f'''<section class="cta"><div class="container"><span class="kicker">Get in touch</span><h2>{h}</h2><p class="lead" style="margin-inline:auto">{p}</p>
<div class="btn-row"><a class="btn btn-dark" href="contact.html?topic=Consultation#contact-form">Schedule a consultation</a><a class="btn btn-outline" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a><a class="btn btn-outline" href="relocation.html">Relocation guide</a></div></div></section>'''

AREAS = [
 ("Bay Village","Cuyahoga County","Jen's hometown: a lakefront community on Lake Erie with Huntington Reservation, Cahoon Memorial Park and the Bay Village City Schools.","card-bay-village","Sunrise over Lake Erie from Huntington Beach in Bay Village, with the Cleveland skyline beyond the breakwall"),
 ("Rocky River","Cuyahoga County","A lakefront suburb at the mouth of the Rocky River, bordered by the Rocky River Reservation of the Cleveland Metroparks.","card-rocky-river","Hike-and-bike bridge over the Rocky River in the Rocky River Reservation of the Cleveland Metroparks"),
 ("Westlake","Cuyahoga County","A suburb about 12 miles west of downtown Cleveland with established neighborhoods, newer developments and Crocker Park shopping and dining.","card-westlake","The main street at Crocker Park in Westlake, Ohio"),
 ("Avon Lake","Lorain County","Lake Erie shoreline living just west of Bay Village, with a mix of lakefront streets and family neighborhoods.","card-avon-lake","Sunset over Lake Erie at Veterans Park in Avon Lake, Ohio"),
 ("Avon","Lorain County","A growing Lorain County city along the I-90 corridor, with a historic French Creek center, newer construction and established subdivisions.","card-avon","Avon's historic 1871 Town Hall in the French Creek area"),
 ("Lakewood","Cuyahoga County","Cleveland's walkable inner-ring neighbor on the lake, known for historic streets, Lakewood Park, the Solstice Steps and busy Detroit and Madison avenues.","card-lakewood","Sunset over Lake Erie from the Solstice Steps at Lakewood Park"),
 ("Greater Cleveland","Cuyahoga County & beyond","From west-side city neighborhoods to the wider metro — Jen helps clients wherever their search leads in Greater Cleveland.","card-cleveland","Cleveland skyline across the water from Edgewater Beach"),
 ("Fairview Park","Cuyahoga County","A residential suburb along the Rocky River Reservation with tree-lined streets and quick access to I-480 and I-90.",None,None),
 ("North Olmsted","Cuyahoga County","A west-side suburb with a wide range of home styles and price points, close to Great Northern shopping and I-480.",None,None),
]
FEATURED_COMMUNITIES = ["Bay Village","Rocky River","Westlake","Avon Lake","Avon","Lakewood"]
def slug(n): return n.lower().replace(" ","-")
def comm_cards():
    featured = [a for a in AREAS if a[0] in FEATURED_COMMUNITIES]
    featured.sort(key=lambda a: FEATURED_COMMUNITIES.index(a[0]))
    return "".join(f'<a class="comm" href="{"bay-village.html" if n=="Bay Village" else "areas.html#"+slug(n)}">{pic(img,alt,"",False,720,920)}<div class="comm-body"><span>{c}</span><h3>{n}</h3></div></a>' for n,c,b,img,alt in featured)

pages={}

# ---------------- HOME ----------------
HOME_FAQ = [
 ("Can Jen help if I'm moving to Cleveland from out of state?","Yes. Helping out-of-town buyers and families relocating to Cleveland is Jen's specialty. She starts by learning your commute, school, budget and lifestyle priorities, recommends the suburbs that fit, and then helps you find and buy the right home, including by video tour when you can't be here in person."),
 ("What are the best Cleveland suburbs for families?","It depends on your priorities, but many west side Cleveland suburbs pair strong schools with parks and lake access. On the 2024–25 Ohio School Report Card, Bay Village, Rocky River and Avon districts earned five stars, and Westlake, Avon Lake and Fairview Park earned 4.5. See the <a href=\"relocation.html\">relocation guide</a> for a side-by-side comparison."),
 ("Why do people choose Bay Village?","Bay Village combines Lake Erie shoreline, tree-lined streets (it's been a Tree City USA for 26 consecutive years), Huntington Beach, a five-star school district and a roughly 20–25 minute drive to Cleveland Hopkins Airport. Read <a href=\"why-bay-village.html\">13 reasons to live in Bay Village</a>."),
 ("Is Jen a Bay Village realtor?","Yes. Jen lives in Bay Village and is a licensed Ohio REALTOR® (License #2025007585) serving Bay Village and all of Greater Cleveland, including Westlake, Rocky River, Lakewood, Avon Lake, Fairview Park, North Olmsted and Avon."),
]
pages["index.html"] = head("index.html","Moving to Cleveland? Bay Village Realtor & Relocation Specialist | Jen Halaska",
 "Relocating to Cleveland, Ohio? Jen Halaska is a Bay Village realtor who helps out-of-town buyers and families find the right west side Cleveland suburb — then the right home.", faq_ld(HOME_FAQ), body_class="home") + f'''
<section class="hero" aria-label="Introduction">
 {pic("hero-lake-erie-daylight","Sunlit Lake Erie shoreline with a rocky breakwall and sandy beach under a clear blue sky","hero-img",True,2560,1440)}
 <div class="container hero-inner">
  <span class="kicker">Bay Village &amp; Greater Cleveland Real Estate</span>
  <h1>Moving to Cleveland? Start here.</h1>
  <p class="lead">Jen Halaska is a Bay Village realtor who specializes in out-of-town buyers and families relocating to Cleveland, Ohio. She helps you find the suburb that fits your commute, schools, lake access, budget and lifestyle, then the right home in it.</p>
  <div class="btn-row">
   <a class="btn btn-white" href="relocation.html">Find your suburb</a>
   <a class="btn btn-ghost-light" href="contact.html?topic=Relocating%20to%20Cleveland#contact-form">Plan my move</a>
   <a class="btn btn-ghost-light" href="home-value.html">What's my home worth?</a>
  </div>
 </div>
 <p class="hero-credit">Photo by <a href="https://unsplash.com/photos/cKwfDLa5XXw" target="_blank" rel="noopener">Dan Crile (Unsplash)</a></p>
</section>

<section>
 <div class="container split wide-left">
  <div>
   <span class="kicker">Meet Jen</span>
   <div class="rule"></div>
   <h2>A neighbor who knows <em>the lake, the streets</em> and the market.</h2>
   <p class="lead">Bay Village isn't just a market Jen works in — it's home. That everyday, on-the-ground familiarity with its neighborhoods, lakefront parks and schools shapes the advice she gives every client, from first-time buyers to longtime homeowners ready for what's next.</p>
   <p>While Bay Village is home base, Jen serves all of Greater Cleveland, including Westlake, Rocky River, Lakewood, Avon Lake, Fairview Park, North Olmsted and Avon.</p>
   <div class="btn-row"><a class="btn btn-dark" href="about.html">About Jen</a><a class="btn btn-outline" href="why-bay-village.html">Why Bay Village?</a></div>
  </div>
  <figure class="portrait" style="margin:0">
   <picture><source srcset="assets/img/jennifer-halaska-realtor-bay-village.webp" type="image/webp"><img src="assets/img/jennifer-halaska-realtor-bay-village.jpg" width="622" height="628" loading="lazy" alt="Portrait of Jen Halaska, REALTOR® in Bay Village, Ohio"></picture>
   <figcaption>Jen Halaska, REALTOR®</figcaption>
  </figure>
 </div>
</section>

<section class="bg-white niche" aria-labelledby="niche-h">
 <div class="container">
  <div class="section-head"><div><span class="kicker">Relocation specialist</span><h2 id="niche-h">New to Cleveland? <em>Find the suburb that fits</em> before you find the house.</h2>
  <p class="lead">Most people moving to Cleveland don't know a local agent, or which of the dozens of suburbs is right for them. Jen's focus is newcomers: she compares west side Cleveland suburbs and the wider metro against what matters to you, then guides you home.</p></div>
  <a class="link-arrow" href="relocation.html">Relocation guide →</a></div>
  <div class="grid g5">
   <div class="pillar"><span class="num">01</span><h3>Commute</h3><p>Downtown, the airport, the Clinic, I-90 or I-480. Jen maps your daily drive.</p></div>
   <div class="pillar"><span class="num">02</span><h3>Schools</h3><p>District ratings and school boundaries, explained.</p></div>
   <div class="pillar"><span class="num">03</span><h3>Lake access</h3><p>Beaches, parks and lakefront suburbs, or quiet streets inland.</p></div>
   <div class="pillar"><span class="num">04</span><h3>Budget</h3><p>Which areas match your price range and taxes.</p></div>
   <div class="pillar"><span class="num">05</span><h3>Lifestyle</h3><p>Walkable downtowns, new construction or a classic neighborhood.</p></div>
  </div>
  <div class="btn-row"><a class="btn btn-dark" href="relocation.html">Which Cleveland suburb fits you?</a><a class="btn btn-outline" href="tel:{PHONE_TEL}">Call or text {PHONE_DISP}</a></div>
 </div>
</section>

<section>
 <div class="container">
  <div class="section-head"><div><span class="kicker">Featured communities</span><h2>Where Jen helps clients <em>live well</em></h2></div><div style="display:flex;gap:2rem;flex-wrap:wrap"><a class="link-arrow" href="why-bay-village.html">Why live in Bay Village →</a><a class="link-arrow" href="areas.html">All communities →</a></div></div>
  <div class="grid g3">{comm_cards()}</div>
 </div>
</section>

<section class="value-band">
 {pic("lake-erie-sunset-shore","Sun setting over the lake","vb-img",False)}
 <div class="container">
  <span class="kicker" style="color:rgba(255,255,255,.85)">For homeowners</span>
  <h2>What's your home worth <em style="color:#dfe6ea">today?</em></h2>
  <p class="lead">Online estimates can't see your updates, your lot or your street. Get a personal, local valuation from Jen — no obligation.</p>
  <form class="value-form" action="home-value.html" method="get">
   <label class="hp" for="hv-address">Property address</label>
   <input id="hv-address" name="address" placeholder="Enter your home address" autocomplete="street-address" required>
   <button class="btn btn-white" type="submit">Get my home value</button>
  </form>
 </div>
</section>

<section class="bg-white">
 <div class="container">
  <div class="section-head"><div><span class="kicker">The experience</span><h2>Personal service, <em>start to finish</em></h2></div></div>
  <div class="grid g4">
   <div class="pillar"><span class="num">01</span><h3>Local insight</h3><p>Street-by-street knowledge of Bay Village and its neighboring communities.</p></div>
   <div class="pillar"><span class="num">02</span><h3>Clear guidance</h3><p>Straight answers, honest advice and a plan you understand at every step.</p></div>
   <div class="pillar"><span class="num">03</span><h3>Thoughtful marketing</h3><p>Professional presentation that helps a home make the right first impression.</p></div>
   <div class="pillar"><span class="num">04</span><h3>A trusted network</h3><p>Introductions to <a href="vendors.html">lenders, inspectors and trades</a> from Jen's network.</p></div>
  </div>
 </div>
</section>

<section class="bg-stone">
 <div class="container split">
  <div>
   <span class="kicker">Buying</span><div class="rule"></div>
   <h2>Find the right home — and the right street.</h2>
   <p class="lead">Search current listings across Northeast Ohio, then let Jen add the local context you won't find online.</p>
   <div class="btn-row"><a class="btn btn-dark" href="{SEARCH_URL}" target="_blank" rel="noopener">Search homes ↗</a><a class="link-arrow" style="align-self:center" href="buyers.html">The buying process →</a></div>
  </div>
  <div>
   <span class="kicker">Selling</span><div class="rule"></div>
   <h2>Sell with a plan, a price and a strategy.</h2>
   <p class="lead">Pricing grounded in local data, practical preparation advice and polished marketing.</p>
   <div class="btn-row"><a class="btn btn-dark" href="home-value.html">Request a valuation</a><a class="link-arrow" style="align-self:center" href="sellers.html">The selling process →</a></div>
  </div>
 </div>
</section>
<!-- PLACEHOLDER: Testimonials intentionally omitted until Jen supplies real, client-approved reviews. -->
{faq_html(HOME_FAQ,"Moving to Cleveland: common questions")}
{cta()}
''' + foot()

# ---------------- ABOUT ----------------
pages["about.html"] = head("about.html","About Jen Halaska | Bay Village Realtor & Cleveland Relocation Specialist",
 "Meet Jen Halaska, a Bay Village, Ohio REALTOR® (License #2025007585) who specializes in helping out-of-town buyers and families relocating to Cleveland.", crumbs_ld("About","about.html")) + page_hero("About","Meet Jen Halaska","A Bay Village resident helping buyers and sellers across Greater Cleveland.","About") + f'''
<section class="bg-white">
 <div class="container split wide-left" style="align-items:start">
  <div class="prose">
   <span class="kicker">Bay Village · Greater Cleveland</span><div class="rule"></div>
   <h2 style="margin-top:0">Hello, I'm Jen.</h2>
   <!-- PLACEHOLDER: Replace/extend with Jen's own bio in her voice (years in Bay Village, family, background, why she loves real estate). Her brokerage "About Me" page is currently blank. -->
   <p class="lead">Bay Village isn't just a market I work in — it's where I live. Living here gives me an everyday, on-the-ground feel for its neighborhoods, lakefront parks and schools, and I bring that local perspective to every client I work with.</p>
   <p>My specialty is people who are new to the area. If you're moving to Cleveland for a job, family or a fresh start, I'll help you compare the west side Cleveland suburbs and the wider metro, from commute and schools to lake access, budget and lifestyle, then find the right home. See my <a href="relocation.html">relocation guide</a>.</p>
   <p>While Bay Village is home base, I help buyers and sellers throughout Greater Cleveland, including Westlake, Rocky River, Lakewood, Avon Lake, Fairview Park, North Olmsted and Avon.</p>
   <p>I'm a member of the Erin Knapp team in Westlake, and I'm licensed with {BROKERAGE}.</p>
   <p class="notice"><strong>[add bio details]</strong> — designations, years licensed, community involvement and a personal note from Jen.</p>
   <div class="signature">Jen</div>
   <div class="btn-row"><a class="btn btn-dark" href="contact.html">Contact Jen</a><a class="btn btn-outline" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a></div>
  </div>
  <figure class="portrait" style="margin:0">
   <picture><source srcset="assets/img/jennifer-halaska-realtor-bay-village.webp" type="image/webp"><img src="assets/img/jennifer-halaska-realtor-bay-village.jpg" width="622" height="628" fetchpriority="high" alt="Portrait of Jen Halaska, REALTOR®"></picture>
   <figcaption>Jen Halaska, REALTOR®</figcaption>
  </figure>
 </div>
</section>
<section>
 <div class="container">
  <div class="section-head"><div><span class="kicker">How I work</span><h2>What you can expect</h2></div></div>
  <div class="grid g3">
   <div class="pillar"><span class="num">01</span><h3>Responsive communication</h3><p>Updates by call, text or email — whichever you prefer.</p></div>
   <div class="pillar"><span class="num">02</span><h3>Local market insight</h3><p>Context on neighborhoods, streets and recent activity so decisions are grounded in local reality.</p></div>
   <div class="pillar"><span class="num">03</span><h3>A coordinated process</h3><p>Help lining up lenders, inspectors and <a href="vendors.html">trusted local vendors</a> so things keep moving.</p></div>
  </div>
 </div>
</section>
{cta()}
''' + foot()

# ---------------- BAY VILLAGE ----------------
BV_FAQ = [
 ("Is Bay Village a good place to live?","Many families think so. Bay Village sits on Lake Erie with Huntington Reservation and Cahoon Memorial Park, has been a Tree City USA for 26 consecutive years, and its school district earned five stars on the 2024–25 Ohio School Report Card."),
 ("What school district serves Bay Village?","Bay Village City Schools: Normandy Elementary (K–2), Westerly Elementary (3–4), Bay Middle School (5–8) and Bay High School (9–12), plus the Glenview Center for preschool."),
 ("How far is Bay Village from the Cleveland airport and downtown?","Cleveland Hopkins International Airport is roughly 9–10 miles away (about 20–25 minutes by car), and downtown Cleveland is about 15 miles east, roughly 25 minutes depending on traffic."),
]
pages["bay-village.html"] = head("bay-village.html","Bay Village, Ohio Guide | Homes, Schools & Parks | Bay Village Realtor Jen Halaska",
 "A local's guide to living in Bay Village, Ohio: the Lake Erie shoreline, Huntington Reservation, Cahoon Memorial Park, Bay Village City Schools and more, from REALTOR® Jen Halaska.", [crumbs_ld("Bay Village Guide","bay-village.html"),faq_ld(BV_FAQ)]) + page_hero("Community guide","Living in Bay Village, Ohio","A lakefront suburb on Lake Erie's southern shore on Cleveland's west side — and the place Jen calls home.","Bay Village","lake-erie-sunset-shore","Sun setting over the lake") + f'''
<section class="bg-white">
 <div class="container">
  <div class="facts">
   <div class="fact"><b>16,163</b><span>Residents · 2020 Census</span></div>
   <div class="fact"><b>Lake Erie</b><span>Northern shoreline</span></div>
   <div class="fact"><b>~100 acres</b><span>Huntington Reservation</span></div>
   <div class="fact"><b>116 acres</b><span>Cahoon Memorial Park</span></div>
  </div>
  <p class="source">Sources: U.S. Census Bureau QuickFacts; Cleveland Metroparks; Ohio Department of Natural Resources Lake Erie public access guide.</p>
 </div>
</section>
<section style="padding-top:0" class="bg-white">
 <div class="container guide-grid">
  <nav class="toc" aria-label="On this page"><a href="why-bay-village.html" style="color:var(--lake-d)">Why live here →</a><a href="#lakefront">The lakefront</a><a href="#huntington">Huntington Reservation</a><a href="#cahoon">Cahoon Memorial Park</a><a href="#schools">Schools</a><a href="#homes">Homes</a></nav>
  <div class="prose narrow">
   <h2 id="lakefront" style="margin-top:0">The lakefront</h2>
   <p>Bay Village sits along the southern shore of Lake Erie in western Cuyahoga County, bordering Westlake, Rocky River and Avon Lake. Lake Road (US Route 6) follows the shoreline through the city, connecting its two signature lakefront parks.</p>
   <h2 id="huntington">Huntington Reservation</h2>
   <p>Part of Cleveland Metroparks since 1925, Huntington Reservation includes Huntington Beach — a public swimming beach reached by staircases down the bluff — along with picnic areas overlooking the lake, wooded trails along Porter Creek, a historic water tower and Karen's Way Play Space. The reservation is also home to <strong>Lake Erie Nature &amp; Science Center</strong> (with its Schuele Planetarium) and <strong>BAYarts</strong>, the community arts campus.</p>
   <h2 id="cahoon">Cahoon Memorial Park</h2>
   <p>Next door, Cahoon Memorial Park stretches from Lake Erie to Wolf Road. It has a paved path along the lakefront bluff, sports fields, a skate park, a disc golf course and the historic <strong>Rose Hill Museum</strong>, operated by the Bay Village Historical Society.</p>
   <h2 id="schools">Schools</h2>
   <p>Bay Village is served by the Bay Village City School District, whose campuses include Normandy Elementary (K–2), Westerly Elementary (3–4), Bay Middle School (5–8) and Bay High School (9–12), plus the Glenview Center for preschool. Confirm current boundaries and programs directly with the district at <a href="https://www.bayvillageschools.com/" target="_blank" rel="noopener">bayvillageschools.com</a>.</p>
   <h2 id="homes">Homes in Bay Village</h2>
   <p>Most homes in Bay Village are owner-occupied single-family houses on established, tree-lined streets, ranging from mid-century colonials and ranches to lakefront and near-lake properties. Every street has its own character — which is where local knowledge makes a difference.</p>
   <!-- PLACEHOLDER: Add Jen's own neighborhood tips (favorite streets, coffee spots, community traditions) in her voice. -->
   <p class="notice">Thinking about a move? See <a href="why-bay-village.html">13 reasons people love living in Bay Village</a>.</p>
   <div class="btn-row"><a class="btn btn-dark" href="{SEARCH_URL}" target="_blank" rel="noopener">Search Bay Village homes ↗</a><a class="btn btn-outline" href="home-value.html">Bay Village home value</a></div>
  </div>
 </div>
</section>
{faq_html(BV_FAQ,"Bay Village questions")}
{cta("Buying or selling in Bay Village?","Talk with someone who lives here.")}
''' + foot()

# ---------------- AREAS ----------------
def area_article(n,c,b,img,alt):
    link = '<a class="link-arrow" href="bay-village.html">Read the Bay Village guide →</a>' if n=="Bay Village" else f'<a class="link-arrow" href="contact.html?topic={n.replace(" ","%20")}#contact-form">Ask about {n} →</a>'
    media = f'<div style="aspect-ratio:16/10;overflow:hidden;margin:-2rem -2rem 1.6rem">{pic(img,alt,"",False,720,920).replace("<img ","<img style=\"width:100%;height:100%;object-fit:cover\" ")}</div>' if img else ""
    return f'<article class="card" id="{slug(n)}">{media}<span class="kicker" style="margin-bottom:.5rem">{c}</span><h3>{n}</h3><p>{b}</p>{link}</article>'
pages["areas.html"] = head("areas.html","West Side Cleveland Suburbs | Bay Village, Westlake, Rocky River, Lakewood Homes | Jen Halaska",
 "Jen Halaska helps buyers and sellers in Bay Village, Westlake, Avon Lake, Rocky River, Lakewood, Fairview Park, North Olmsted, Avon and across Greater Cleveland.", crumbs_ld("Communities","areas.html")) + page_hero("Communities","Greater Cleveland, west side and beyond","Bay Village is home base. Jen also helps clients buy and sell throughout these neighboring communities and the wider Cleveland area.","Communities") + f'''
<section><div class="container"><div class="grid g3">{"".join(area_article(*a) for a in AREAS)}</div>
<p class="source" style="margin-top:2rem">Don't see your community? Jen serves all of Greater Cleveland. <a href="contact.html">Get in touch</a>.</p></div></section>
{cta()}
''' + foot()

# ---------------- BUYERS ----------------
pages["buyers.html"] = head("buyers.html","Buying a Home in Bay Village & Greater Cleveland | Jen Halaska, REALTOR®",
 "Buying a home in Bay Village, Westlake or Greater Cleveland, or relocating from out of town? Jen Halaska guides buyers from pre-approval to closing.", crumbs_ld("Buy","buyers.html")) + page_hero("Buying","Find the right home — and the right street","A clear, step-by-step process with a local guide who helps you see beyond the listing photos.","Buy") + f'''
<section class="bg-white">
 <div class="container split wide-left" style="align-items:start">
  <div>
   <h2>How we'll find your home</h2>
   <ol class="steps">
    <li><div><strong>Consultation</strong><span>Talk through your must-haves, timeline, budget and favorite areas.</span></div></li>
    <li><div><strong>Get pre-approved</strong><span>Know your buying power before you shop. A <a href="vendors.html#lenders">lender from Jen's network</a> can help.</span></div></li>
    <li><div><strong>Search &amp; tour</strong><span>See new listings as they hit the market and tour with local context.</span></div></li>
    <li><div><strong>Write a strong offer</strong><span>Price and terms grounded in local data and a strategy that fits the situation.</span></div></li>
    <li><div><strong>Inspections &amp; appraisal</strong><span>Coordinate inspections and next steps with trusted professionals.</span></div></li>
    <li><div><strong>Close &amp; move in</strong><span>Title, final walk-through and keys — with support through settling in.</span></div></li>
   </ol>
  </div>
  <div class="card" style="background:var(--stone)">
   <h3>Buyer checklist</h3>
   <ul class="checklist"><li>Mortgage pre-approval letter</li><li>Down payment and closing-cost plan</li><li>Must-haves vs. nice-to-haves</li><li>Preferred communities and school districts</li><li>Moving timeline</li><li>Home inspector lined up</li></ul>
   <div class="btn-row"><a class="btn btn-dark" href="{SEARCH_URL}" target="_blank" rel="noopener">Search homes ↗</a><a class="btn btn-outline" href="contact.html?topic=Buying#contact-form">Start my search</a></div>
  </div>
 </div>
</section>
{cta("Ready to start your home search?")}
''' + foot()

# ---------------- SELLERS ----------------
pages["sellers.html"] = head("sellers.html","Sell Your Home in Bay Village & Greater Cleveland | Jen Halaska, REALTOR®",
 "Selling in Bay Village, Westlake, Rocky River or Greater Cleveland? Get local pricing insight, preparation advice and polished marketing with Jen Halaska.", crumbs_ld("Sell","sellers.html")) + page_hero("Selling","Sell with a plan, a price and a strategy","Pricing, preparation and marketing built around your home, your street and your timeline.","Sell") + f'''
<section class="bg-white">
 <div class="container split wide-left" style="align-items:start">
  <div>
   <h2>The selling process</h2>
   <ol class="steps">
    <li><div><strong>Walk-through &amp; goals</strong><span>Tour your home together and discuss timing and priorities.</span></div></li>
    <li><div><strong>Pricing strategy</strong><span>A local comparative market analysis to position your home correctly from day one.</span></div></li>
    <li><div><strong>Prepare to shine</strong><span>Practical repair, staging and curb-appeal guidance, with <a href="vendors.html">trusted vendors</a> if you need help.</span></div></li>
    <li><div><strong>Market it well</strong><span>Professional photography and a thoughtful marketing plan.</span></div></li>
    <li><div><strong>Negotiate</strong><span>Review offers side by side and negotiate the terms that matter to you.</span></div></li>
    <li><div><strong>Close</strong><span>Coordinate inspections, appraisal and title through closing day.</span></div></li>
   </ol>
  </div>
  <div>
   <div class="card" style="background:var(--char);color:#d9dcde;border:0"><h3 style="color:#fff">What's my home worth?</h3><p>Online estimates can't see your updates, your lot or your street. Request a personal valuation.</p><a class="btn btn-white" href="home-value.html">Request my home value</a></div>
   <div class="card" style="margin-top:1.6rem"><h3>Seller prep checklist</h3><ul class="checklist"><li>Declutter and depersonalize</li><li>Small repairs and touch-up paint</li><li>Boost curb appeal</li><li>Gather utility bills and improvement records</li><li>Plan for showings</li></ul></div>
  </div>
 </div>
</section>
{cta("Thinking about selling?","Start with a conversation about your goals and timing.")}
''' + foot()

# ---------------- HOME VALUE ----------------
def lead_form(subject, fields_html, button, form_id="contact-form"):
    # FormSubmit: delivers to FORM_EMAIL. First submission triggers a one-time activation email that must be clicked.
    return f'''<form id="{form_id}" class="lead-form" action="{FORM_ACTION}" method="POST">
 <input type="hidden" name="_subject" value="{subject} — bayvillageohio.com">
 <input type="hidden" name="_template" value="table">
 <input type="hidden" name="_captcha" value="false">
 <input type="hidden" name="_next" value="{SITE_URL}/thank-you.html">
 <div class="hp" aria-hidden="true"><label for="{form_id}-honey">Leave blank</label><input type="text" id="{form_id}-honey" name="_honey" tabindex="-1" autocomplete="off"></div>
 {fields_html}
 <button class="btn btn-dark" type="submit">{button}</button>
 <p class="form-note" style="margin-top:1.2rem">Prefer to talk? Call or text <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a>.</p>
</form>'''
NAME_FIELDS = '''<div class="row"><div class="field"><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div><div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div></div>
 <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>'''
hv_fields = '''<div class="field"><label for="address">Property address</label><input id="address" name="address" autocomplete="street-address" required></div>
 <div class="row"><div class="field"><label for="beds">Bedrooms</label><input id="beds" name="bedrooms" inputmode="numeric"></div><div class="field"><label for="baths">Bathrooms</label><input id="baths" name="bathrooms" inputmode="decimal"></div></div>
 <div class="row"><div class="field"><label for="timeline">Thinking of selling</label><select id="timeline" name="timeline"><option>Just curious</option><option>0–3 months</option><option>3–6 months</option><option>6–12 months</option><option>12+ months</option></select></div><div class="field"><label for="updates">Recent updates</label><input id="updates" name="updates" placeholder="Kitchen, roof, baths…"></div></div>
 ''' + NAME_FIELDS
pages["home-value.html"] = head("home-value.html","What's My Home Worth? Bay Village & Cleveland Home Valuation | Jen Halaska",
 "Request a free, personal home valuation for your Bay Village, Westlake, Rocky River or Greater Cleveland home from local REALTOR® Jen Halaska.", crumbs_ld("Home Value","home-value.html")) + page_hero("Home valuation","What's your home worth?","A personal, local valuation — not an algorithm. Share a few details and Jen will follow up with a no-obligation analysis.","Home Value","lake-erie-sunset-shore","Sun setting over the lake") + f'''
<section class="bg-white">
 <div class="container contact-grid">
  <div>
   <span class="kicker">Why a personal valuation</span><div class="rule"></div>
   <h2>Your home is more than its square footage.</h2>
   <ul class="checklist" style="margin-top:1.5rem"><li>Reflects updates, condition and lot details online tools miss</li><li>Grounded in recent local sales and current competition</li><li>Includes practical advice on what would add value before listing</li><li>No cost and no obligation</li></ul>
  </div>
  <div class="form-card"><h2 style="font-size:2.2rem">Request my home value</h2>{lead_form("Home value request", hv_fields, "Request my valuation")}</div>
 </div>
</section>
''' + foot()

# ---------------- WHY BAY VILLAGE ----------------
REASONS = [
 ("Tree-covered streets","Bay Village has been recognized as a Tree City USA by the Arbor Day Foundation for 26 consecutive years, and earned Tree City USA Growth Awards in 2023 and 2024. Mature canopies shade its established residential streets, and the city maintains an inventory of more than 3,000 city trees.","City of Bay Village"),
 ("Lake Erie views","The city's entire northern edge is Lake Erie shoreline. Lake Road (US Route 6) follows the water, and a paved path along the bluff at Cahoon Memorial Park offers some of the best sunset views on the west side.","ODNR Lake Erie public access guide"),
 ("Lake Erie Nature &amp; Science Center","A local favorite for families: free general admission to live-animal exhibits and natural-history displays, a wildlife rehabilitation program for injured and orphaned animals, and the Schuele Planetarium.","lensc.org"),
 ("Huntington Beach &amp; Reservation","Part of Cleveland Metroparks since 1925, Huntington Reservation includes Huntington Beach, a public swimming beach on Lake Erie, plus wooded trails along Porter Creek, lakeview picnic areas, the historic water tower and Karen's Way Play Space.","Cleveland Metroparks"),
 ("Kids ride bikes to school","Bay Village's compact, close-knit neighborhood schools make walking and biking a real option. The city runs a Safe Routes to School program, which upgraded five school-route intersections in 2023, and the schools hold an annual Bike to School Challenge.","City of Bay Village; Bay Village City Schools"),
 ("A short drive to the airport","Cleveland Hopkins International Airport (CLE) is roughly 9–10 miles away, typically about a 20–25 minute drive depending on traffic and your starting point.","Route planners (OSRM, Travelmath)"),
 ("Five-star public schools","Bay Village City Schools earned a five-star overall rating on the 2024–25 Ohio School Report Card. The district reports that its performance index ranks 4th in Cuyahoga County.","Ohio Dept. of Education &amp; Workforce; Bay Village City Schools"),
 ("BAYarts &amp; the former Huntington Playhouse","The BAYarts campus inside Huntington Reservation offers classes, galleries and events for artists of all ages. Its historic buildings include the former Huntington Playhouse, a community theater from 1958 to 2015 that BAYarts is renovating for cultural programming.","BAYarts"),
 ("Cahoon Memorial Park &amp; Rose Hill Museum","The 116-acre park stretches from the lake to Wolf Road, with sports fields, a skate park, disc golf and the bluff-top path. It's also home to the Rose Hill Museum, run by the Bay Village Historical Society.","ODNR; Bay Village Historical Society"),
 ("Bay Days on the Fourth of July","Since the 1960s, the Kiwanis Club of Bay Village has hosted Bay Days at Cahoon Memorial Park: a multi-day Independence Day festival with rides, free gazebo concerts, a children's bike, trike and wagon parade, and fireworks on the Fourth.","Bay Village Kiwanis"),
 ("A safe community","Bay Village was named among Ohio's safest cities in SafeWise's 2025 ranking, based on FBI crime data.","SafeWise 2025"),
 ("Close to downtown Cleveland","Downtown Cleveland is about 15 miles east. Residents can be at a game, a show or the office in roughly 25 minutes, then back home by the lake.","Route estimates"),
 ("A brand-new library","The Cuyahoga County Public Library Bay Village Branch opened in 2022 at 27400 Wolf Road: two stories and 17,000 square feet with teen and children's rooms, a maker space with 3D printers, and a rooftop patio.","City of Bay Village"),
]
def reason_cards():
    return "".join(f'<article class="reason"><span class="num">{i:02d}</span><h3>{t}</h3><p>{b}</p><span class="src">Source: {src}</span></article>' for i,(t,b,src) in enumerate(REASONS,1))
LIST_LD = {"@context":"https://schema.org","@type":"ItemList","name":"Reasons to live in Bay Village, Ohio",
          "itemListElement":[{"@type":"ListItem","position":i,"name":t.replace("&amp;","&")} for i,(t,_,_) in enumerate(REASONS,1)]}
pages["why-bay-village.html"] = head("why-bay-village.html","Why Live in Bay Village, Ohio | Jen Halaska",
 "13 reasons to live in Bay Village, Ohio: tree-lined streets, Lake Erie views, Huntington Beach, the Nature &amp; Science Center, five-star schools, kids biking to school and a short drive to Cleveland Hopkins Airport.", LIST_LD) + page_hero("Why Bay Village","Why live in Bay Village, Ohio?","Lake Erie on one side, tree-lined streets on the other, and a small-town spirit just minutes from Cleveland. Here's why Jen, and so many families, call Bay Village home.","<a href=\"bay-village.html\">Bay Village</a> / Why Bay Village","hero-lake-erie-daylight","Sunlit Lake Erie shoreline with a rocky breakwall and sandy beach") + f'''
<section class="bg-white" style="padding-bottom:3rem">
 <div class="container split wide-left">
  <div>
   <span class="kicker">At a glance</span><div class="rule"></div>
   <h2>A lakefront hometown with <em>big-city access</em></h2>
   <p class="lead">Bay Village pairs the feel of a close-knit village with parks, beaches and arts on the shore of Lake Erie, plus quick drives to the airport and downtown.</p>
  </div>
  <div class="facts" style="grid-template-columns:repeat(2,1fr);margin:0">
   <div class="fact"><b>26 yrs</b><span>Tree City USA</span></div>
   <div class="fact"><b>5 stars</b><span>Ohio School Report Card 2024–25</span></div>
   <div class="fact"><b>~20–25 min</b><span>To Cleveland Hopkins (CLE)</span></div>
   <div class="fact"><b>Lake Erie</b><span>Northern shoreline</span></div>
  </div>
 </div>
</section>
<section class="bg-white" style="padding-top:2rem">
 <div class="container"><div class="reasons">{reason_cards()}</div></div>
</section>
<section class="bg-stone">
 <div class="container split">
  <figure style="margin:0" class="portrait">{pic("card-bay-village","Sunrise over Lake Erie from Huntington Beach in Bay Village","",False,720,920)}</figure>
  <div>
   <span class="kicker">Living here</span><div class="rule"></div>
   <h2>Seasons, sunsets and <em>Saturday mornings</em></h2>
   <p class="lead">Summer days at Huntington Beach, fall color on tree-lined streets, winter walks along the lake and the Fourth of July at Bay Days. Life in Bay Village follows the seasons.</p>
   <div class="btn-row"><a class="btn btn-dark" href="bay-village.html">Read the Bay Village guide</a><a class="btn btn-outline" href="{SEARCH_URL}" target="_blank" rel="noopener">See homes for sale ↗</a></div>
  </div>
 </div>
</section>
<section class="bg-white" style="padding:3rem 0">
 <div class="container"><p class="source">Sources: City of Bay Village (Tree City USA; Safe Routes to School; Bay Village Library), Ohio Department of Education &amp; Workforce and Bay Village City Schools (2024–25 report card), Cleveland Metroparks, Lake Erie Nature &amp; Science Center, BAYarts, Bay Village Historical Society, Kiwanis Club of Bay Village, SafeWise (2025 Safest Cities in Ohio), Ohio DNR, and route-planning estimates for drive times. Facts current as of November 2026; details can change.</p></div>
</section>
{cta("Ready to make Bay Village home?","Jen lives here and would love to show you around: streets, schools, parks and homes.")}
''' + foot()

# ---------------- RELOCATION ----------------
RELO_FAQ = [
 ("What are the best west side Cleveland suburbs for families?","It depends on what you value most. On the 2024–25 Ohio School Report Card, Bay Village, Rocky River and Avon districts earned five stars and Westlake, Avon Lake and Fairview Park earned 4.5 stars. Bay Village, Rocky River, Avon Lake and Lakewood also have Lake Erie shoreline."),
 ("Which Cleveland suburbs are close to the airport?","Westlake, North Olmsted and Fairview Park sit near I-480 and Cleveland Hopkins International Airport. Westlake reports the airport is about six miles away, North Olmsted is about eight miles by road, and Bay Village is roughly 9–10 miles."),
 ("Can I buy a home in Cleveland before I move?","Yes. Many relocating buyers tour by live video, review disclosures and inspections remotely, and coordinate with a lender and title company by phone and e-signature. Jen will explain which steps may still need an in-person or notarized signature for your situation."),
 ("Which suburb is closest to downtown Cleveland?","Lakewood borders the city of Cleveland on its west side, making it one of the closest suburbs to downtown, with walkable commercial streets and Lakewood Park on the lake. Rocky River and Fairview Park are next door."),
 ("Do I need a local realtor if I'm relocating to Cleveland, Ohio?","A local agent helps you avoid guessing about neighborhoods you've never seen. Jen lives in Bay Village and focuses on newcomers: she'll narrow the suburbs to your short list, preview homes for you and guide you from offer to closing."),
]
SUBURBS = [
 ("Bay Village","Cuyahoga","Yes","5★","Tree City USA; Huntington Beach &amp; Metroparks; ~9–10 mi to CLE","bay-village.html"),
 ("Rocky River","Cuyahoga","Yes","5★","Rocky River Reservation (Cleveland Metroparks); lakefront at the river's mouth",None),
 ("Westlake","Cuyahoga","No (about 1 mile south of the lake)","4.5★","Crocker Park; I-90 &amp; I-480 access; ~6 mi to CLE (city of Westlake)",None),
 ("Avon Lake","Lorain","Yes","4.5★","Lake Erie shoreline living just west of Bay Village; Veterans Park",None),
 ("Avon","Lorain","No","5★","Historic French Creek center; newer construction along the I-90 corridor",None),
 ("Lakewood","Cuyahoga","Yes","4★","Borders Cleveland; walkable Detroit &amp; Madison avenues; Lakewood Park and the Solstice Steps",None),
 ("Fairview Park","Cuyahoga","No","4.5★","Borders the Rocky River Reservation; quick I-480 &amp; I-90 access",None),
 ("North Olmsted","Cuyahoga","No","3.5★","Wide range of price points; Great Northern shopping; ~8 mi to CLE",None),
]
def suburb_rows():
    return "".join(f'<tr><th scope="row">{f"<a href=\"{l}\">{n}</a>" if l else n}</th><td>{c}</td><td>{lake}</td><td>{sch}</td><td>{k}</td></tr>' for n,c,lake,sch,k,l in SUBURBS)
reloc_fields = '''<div class="row"><div class="field"><label for="from">Moving from</label><input id="from" name="moving_from" placeholder="City, state"></div><div class="field"><label for="when">Target move date</label><input id="when" name="move_date" placeholder="e.g., summer 2027"></div></div>
 <div class="row"><div class="field"><label for="budget">Budget range</label><input id="budget" name="budget" placeholder="e.g., $350k–$500k"></div><div class="field"><label for="work">Work / commute to</label><input id="work" name="commute_to" placeholder="Downtown, airport, hospital…"></div></div>
 <div class="field"><label for="priorities">What matters most?</label><textarea id="priorities" name="priorities" rows="3" placeholder="Schools, lake access, walkability, new construction…"></textarea></div>
 <input type="hidden" name="topic" value="Relocating to Cleveland">
 ''' + NAME_FIELDS
pages["relocation.html"] = head("relocation.html","Relocating to Cleveland, Ohio | Which Suburb Fits You? | Jen Halaska",
 "Moving to Cleveland? Compare west side Cleveland suburbs (Bay Village, Westlake, Rocky River, Avon Lake, Lakewood and more) by schools, lake access and commute, with relocation help from Bay Village realtor Jen Halaska.",
 [crumbs_ld("Relocating to Cleveland","relocation.html"),faq_ld(RELO_FAQ)]) + page_hero("Relocation","Relocating to Cleveland, Ohio","New to Northeast Ohio? Jen helps out-of-town buyers and families figure out which Cleveland suburb fits their life, then find the right home in it.","Relocating to Cleveland","relocation-cleveland-skyline","Cleveland skyline across Lake Erie from Edgewater Beach") + f'''
<section class="bg-white">
 <div class="container split wide-left" style="align-items:start">
  <div>
   <span class="kicker">Start here</span><div class="rule"></div>
   <h2>How do I choose the right Cleveland suburb?</h2>
   <p class="lead">Start with five questions: where you'll commute, what you need from schools, how close you want to be to Lake Erie, your budget, and the lifestyle you want day to day. Each Greater Cleveland suburb answers them differently, and Jen's job is to match yours to the right short list.</p>
   <p>Most of Jen's clients are moving to Cleveland from out of town. They don't yet know a local agent, or the difference between Westlake and Lakewood. That's exactly where she helps.</p>
  </div>
  <div class="card" style="background:var(--stone)">
   <h3>Quick matcher</h3>
   <ul class="checklist">
    <li><strong>Lakefront &amp; beaches:</strong> Bay Village, Rocky River, Avon Lake, Lakewood</li>
    <li><strong>Close to the airport:</strong> Westlake, North Olmsted, Fairview Park</li>
    <li><strong>Walkable &amp; close to downtown:</strong> Lakewood</li>
    <li><strong>Newer construction:</strong> Avon</li>
    <li><strong>Five-star school districts (2024–25):</strong> Bay Village, Rocky River, Avon</li>
   </ul>
  </div>
 </div>
</section>
<section>
 <div class="container">
  <div class="section-head"><div><span class="kicker">Close to home</span><h2>West side communities Jen knows <em>best</em></h2></div><a class="link-arrow" href="areas.html">All communities →</a></div>
  <div class="grid g3">{comm_cards()}</div>
 </div>
</section>
<section class="bg-stone">
 <div class="container">
  <div class="section-head"><div><span class="kicker">Which suburb fits you?</span><h2>West side Cleveland suburbs, <em>side by side</em></h2></div></div>
  <div class="table-wrap"><table class="compare">
   <caption class="sr-only">Comparison of west side Cleveland suburbs</caption>
   <thead><tr><th scope="col">Suburb</th><th scope="col">County</th><th scope="col">Lake Erie shoreline</th><th scope="col">District rating<br><small>Ohio Report Card 2024–25</small></th><th scope="col">Known for</th></tr></thead>
   <tbody>{suburb_rows()}</tbody>
  </table></div>
  <p class="source" style="margin-top:1rem">District ratings are overall star ratings from the 2024–25 Ohio School Report Cards (Ohio Department of Education &amp; Workforce, as reported by Cleveland 19, Fox 8 and district websites). Distances from route planners and city sources. Always confirm current ratings, boundaries and drive times.</p>
  <h3 style="margin-top:2.5rem">Considering the east side?</h3>
  <p>East-side suburbs such as Shaker Heights, Cleveland Heights, Beachwood, Solon and Chagrin Falls are also popular with newcomers. Jen can help you compare east versus west, and connect you with trusted east-side colleagues if that's where your search leads.</p>
 </div>
</section>
<section class="bg-white">
 <div class="container split" style="align-items:start">
  <div>
   <h2>What does relocating with Jen look like?</h2>
   <ol class="steps">
    <li><div><strong>Discovery call</strong><span>Your timeline, budget, commute and must-haves.</span></div></li>
    <li><div><strong>Suburb short list</strong><span>Two or three suburbs that fit, with honest pros and cons.</span></div></li>
    <li><div><strong>Get pre-approved</strong><span>Connect with a local lender from <a href="vendors.html#lenders">Jen's network</a>.</span></div></li>
    <li><div><strong>Tour: in person or by video</strong><span>Neighborhood drive-throughs and live video home tours.</span></div></li>
    <li><div><strong>Offer, inspection &amp; closing</strong><span>Guided step by step, with e-signatures wherever possible.</span></div></li>
    <li><div><strong>Move in &amp; settle</strong><span>Movers, utilities, schools, and a local guide for your first months.</span></div></li>
   </ol>
  </div>
  <div>
   <div class="card" style="background:var(--char);color:#d9dcde;border:0">
    <h3 style="color:#fff">Buying from out of town?</h3>
    <p>Can't get to Cleveland yet? Jen can tour homes for you by live video, send neighborhood walk-throughs, and coordinate inspections, appraisal and closing with your lender and title company, so you can act quickly when the right home appears.</p>
    <a class="btn btn-white" href="#relocation-form">Start my relocation plan</a>
   </div>
  </div>
 </div>
</section>
{faq_html(RELO_FAQ,"Relocating to Cleveland: FAQ")}
<section class="bg-stone" id="relocation-form">
 <div class="container contact-grid">
  <div>
   <span class="kicker">Relocation inquiry</span><div class="rule"></div>
   <h2>Tell Jen about your move</h2>
   <p class="lead">Share a few details and Jen will follow up with a suburb short list and next steps. No obligation.</p>
   <p>Prefer to talk? Call or text <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a>.</p>
  </div>
  <div class="form-card">{lead_form("Relocation inquiry", reloc_fields, "Send my relocation details", "relocation-inquiry")}</div>
 </div>
</section>
''' + foot()

pages["thank-you.html"] = head("thank-you.html","Thank You | Jen Halaska","Thanks for reaching out to Jen Halaska.",robots="noindex, nofollow") + page_hero("Thank you","Thanks, your message is on its way.","Jen will be in touch soon. If it's urgent, call or text (330) 807-6374.","Thank you") + f'''
<section class="bg-white"><div class="container"><div class="btn-row" style="margin:0"><a class="btn btn-dark" href="index.html">Back to home</a><a class="btn btn-outline" href="relocation.html">Relocation guide</a><a class="btn btn-outline" href="why-bay-village.html">Why Bay Village</a></div></div></section>
''' + foot()

# ---------------- VENDORS ----------------
CATS = [("lenders","Mortgage Lenders"),("inspectors","Home Inspectors"),("title","Title Companies"),("attorneys","Real Estate Attorneys"),
        ("contractors","Contractors & Trades"),("movers","Movers"),("stagers","Home Stagers"),("photographers","Real Estate Photographers"),("insurance","Insurance Agents")]
def vcard(cat):
    return f'''<article class="vendor-card"><!-- PLACEHOLDER: replace with a real vendor from Jen's network ({cat}) --><span class="ph">Placeholder</span><h3>[Vendor business name]</h3><p>[One-line description and why Jen recommends them.]</p><dl><dt>Contact</dt><dd>[Contact name]</dd><dt>Phone</dt><dd>[Phone]</dd><dt>Web</dt><dd>[Website]</dd><dt>Serves</dt><dd>[Areas served]</dd></dl></article>'''
vsecs = "".join(f'<section class="vendor-cat" id="{i}" aria-labelledby="h-{i}" style="padding-bottom:0"><div class="vc-head"><h2 id="h-{i}">{n}</h2><span>Trusted network</span></div><div class="grid g3">{vcard(n)}{vcard(n)}</div></section>' for i,n in CATS)
pages["vendors.html"] = head("vendors.html","Recommended Vendors in Greater Cleveland | Lenders, Inspectors & More | Jen Halaska",
 "Jen Halaska's recommended vendors for Bay Village and Greater Cleveland homeowners: lenders, inspectors, title, attorneys, contractors, movers, stagers, photographers and insurance.", crumbs_ld("Recommended Vendors","vendors.html")) + page_hero("Recommended vendors","Jen's trusted local network","Good professionals make every move smoother. These are vendors from Jen's trusted network across Bay Village and Greater Cleveland.","Vendors") + f'''
<section class="bg-white" style="padding-top:3.5rem">
 <div class="container">
  <nav class="vendor-nav" aria-label="Vendor categories">{"".join(f'<a href="#{i}">{n}</a>' for i,n in CATS)}</nav>
  <p class="notice">Vendors listed here are from Jen's trusted professional network. Recommendations are provided as a courtesy; you are free to choose any provider. <!-- PLACEHOLDER: confirm disclosure language with the brokerage's compliance team (RESPA / affiliated business disclosures) before publishing. --></p>
  {vsecs}
  <div class="card" style="margin-top:4rem;background:var(--stone)"><h3>Are you a local professional?</h3><p>Jen is always glad to meet reliable local professionals who take great care of clients. <a href="contact.html?topic=Vendor%20network#contact-form">Introduce yourself</a>.</p></div>
 </div>
</section>
{cta()}
''' + foot()

# ---------------- CONTACT ----------------
topics = ["General question","Relocating to Cleveland","Buying","Selling","Home value","Consultation","Showing","Bay Village","Vendor network"]
c_fields = NAME_FIELDS + f'''
 <div class="row"><div class="field"><label for="topic">I'm interested in</label><select id="topic" name="topic">{"".join(f'<option>{t}</option>' for t in topics)}</select></div><div class="field"><label for="timeline">Timeline</label><select id="timeline" name="timeline"><option>Just exploring</option><option>0–3 months</option><option>3–6 months</option><option>6–12 months</option><option>12+ months</option></select></div></div>
 <div class="field"><label for="message">Message</label><textarea id="message" name="message" rows="5" placeholder="Tell Jen what you're looking for, or suggest times for a consultation."></textarea></div>
 '''
pages["contact.html"] = head("contact.html","Contact Jen Halaska | Bay Village & Greater Cleveland REALTOR®",
 "Contact Jen Halaska, Bay Village realtor and Cleveland relocation specialist. Call (330) 807-6374 or send a message to plan your move or schedule a consultation.", crumbs_ld("Contact","contact.html")) + page_hero("Contact","Let's talk about your next move","Call (330) 807-6374 or send a note below — Jen will be in touch. Moving from out of town? Tell her where you're coming from.","Contact") + f'''
<section class="bg-white">
 <div class="container contact-grid">
  <div>
   <span class="kicker">Get in touch</span><div class="rule"></div>
   <h2>Jen Halaska, REALTOR®</h2>
   <ul class="contact-list">
    <li><span class="lbl">Phone</span><a href="tel:{PHONE_TEL}">{PHONE_DISP}</a><br><span class="form-note">Office: <a style="font-family:var(--sans);font-size:.85rem" href="tel:{OFFICE_TEL}">{OFFICE_DISP}</a></span></li>
    <li><span class="lbl">Message</span><a href="#contact-form">Use the form →</a></li>
    <li><span class="lbl">Office</span><span style="font-family:var(--serif);font-size:1.3rem;color:var(--char)">{OFFICE["street"]}, {OFFICE["city"]}, {OFFICE["region"]} {OFFICE["zip"]}</span><br><a class="link-arrow" style="font-family:var(--sans);font-size:.72rem" href="https://www.google.com/maps/search/?api=1&amp;query=2055+Crocker+Rd+Suite+101+Westlake+OH+44145" target="_blank" rel="noopener">Directions ↗</a></li>
    <li><span class="lbl">Search homes</span><a href="{SEARCH_URL}" target="_blank" rel="noopener">View current listings ↗</a></li>
   </ul>
   <img src="assets/img/jennifer-halaska-sm.jpg" width="300" height="303" loading="lazy" alt="Jen Halaska, REALTOR®" style="width:150px;height:150px;object-fit:cover;border-radius:50%">
  </div>
  <div class="form-card" id="message-form"><h2 style="font-size:2.2rem">Send a message</h2>{lead_form("New inquiry from website", c_fields, "Send message")}</div>
 </div>
</section>
''' + foot()

pages["404.html"] = head("404.html","Page not found | Jen Halaska Real Estate","The page you were looking for could not be found.",robots="noindex") + page_hero("404","Page not found","Sorry, that page doesn't exist. Try the <a href=\"index.html\">home page</a> or <a href=\"contact.html\">contact Jen</a>.","Not found") + foot()

for name,html in pages.items():
    open(os.path.join(ROOT,name),"w",encoding="utf-8").write(html)
today=datetime.date.today().isoformat()
NOINDEX={"404.html","thank-you.html"}
pri={"index.html":"1.0","relocation.html":"0.9","why-bay-village.html":"0.9","contact.html":"0.9","bay-village.html":"0.9","home-value.html":"0.8"}
with open(os.path.join(ROOT,"sitemap.xml"),"w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for n in pages:
        if n in NOINDEX: continue
        f.write(f"  <url><loc>{SITE_URL}/{'' if n=='index.html' else n}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{pri.get(n,'0.7')}</priority></url>\n")
    f.write("</urlset>\n")
BOTS=["GPTBot","ChatGPT-User","OAI-SearchBot","PerplexityBot","ClaudeBot","Claude-Web","Google-Extended","Googlebot","Bingbot","Applebot","Applebot-Extended"]
robots="".join(f"User-agent: {b}\nAllow: /\n\n" for b in BOTS)+"User-agent: *\nAllow: /\nDisallow: /_build/\nDisallow: /thank-you.html\n\nSitemap: "+SITE_URL+"/sitemap.xml\n"
open(os.path.join(ROOT,"robots.txt"),"w").write(robots)
llms=f"""# Jen Halaska — Bay Village Realtor & Cleveland Relocation Specialist

> Jen Halaska (Jennifer Halaska) is a licensed Ohio REALTOR® (Ohio License #{LICENSE}) who lives in Bay Village, Ohio. She specializes in helping out-of-town buyers and families relocating to Cleveland choose the right suburb (commute, schools, lake access, budget, lifestyle) and then find and buy the right home. Brokered by {BROKERAGE}.

## Contact
- Phone / text: {PHONE_DISP}
- Contact form: {SITE_URL}/contact.html
- Office: {OFFICE["street"]}, {OFFICE["city"]}, {OFFICE["region"]} {OFFICE["zip"]}

## Areas served
Bay Village, Westlake, Rocky River, Avon Lake, Lakewood, Fairview Park, North Olmsted, Avon, Cleveland and Greater Cleveland (Cuyahoga and Lorain counties).

## Key pages
- [Home]({SITE_URL}/): Moving to Cleveland? Start here.
- [Relocating to Cleveland]({SITE_URL}/relocation.html): which-suburb-fits-you guide comparing west side Cleveland suburbs, relocation process, remote buying, FAQ
- [Why live in Bay Village]({SITE_URL}/why-bay-village.html): 13 sourced reasons
- [Bay Village guide]({SITE_URL}/bay-village.html): lakefront, parks, schools, homes
- [Communities]({SITE_URL}/areas.html): west side Cleveland suburbs
- [Buying]({SITE_URL}/buyers.html) · [Selling]({SITE_URL}/sellers.html) · [Home value]({SITE_URL}/home-value.html)
- [Recommended vendors]({SITE_URL}/vendors.html)
- [About Jen]({SITE_URL}/about.html) · [Contact]({SITE_URL}/contact.html)

## Facts used on this site (sources)
- Bay Village: 16,163 residents (2020 U.S. Census); Tree City USA 26 consecutive years (City of Bay Village); five-star district on 2024–25 Ohio School Report Card (Ohio DEW).
- Cleveland Hopkins International Airport is roughly 9–10 miles / 20–25 minutes from Bay Village (route planners).
"""
open(os.path.join(ROOT,"llms.txt"),"w").write(llms)
print("built",len(pages),"pages")
