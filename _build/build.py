#!/usr/bin/env python3
"""Generates the static site. Edit CONFIG, then run: python3 _build/build.py
Output is plain HTML/CSS/JS (no build step needed to host on GitHub Pages)."""
import json, os, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------- CONFIG (replace placeholders) ----------------
SITE_URL    = "https://bayvillageohio.com"      # live domain (GoDaddy) — used in canonical/OG/schema/sitemap/robots
EMAIL       = "your-email@example.com"          # PLACEHOLDER: Jennifer's email (not on her brokerage page)
EMAIL_SHOWN = "[add email address]"             # PLACEHOLDER: visible email text on Contact page
PHONE_DISP  = "(330) 807-6374"                  # Jennifer's direct phone (primary)
PHONE_TEL   = "+13308076374"
OFFICE_DISP = "(440) 793-0100"                  # brokerage office line (secondary)
OFFICE_TEL  = "+14407930100"
LICENSE     = "[add Ohio license #]"            # PLACEHOLDER
BROKERAGE   = "Howard Hanna Real Estate Services"   # compliance mention (plain text, footer + About only)
FORMSPREE   = "https://formspree.io/f/YOUR_FORM_ID" # PLACEHOLDER: free form ID from formspree.io
SEARCH_URL  = "https://jenniferhalaska.howardhanna.com/"  # REAL: her listing-search page
OFFICE = {"street":"2055 Crocker Rd., Suite 101","city":"Westlake","region":"OH","zip":"44145"}
# ---------------------------------------------------------------

NAV = [("about.html","About"),("bay-village.html","Bay Village"),("why-bay-village.html","Why Bay Village"),("areas.html","Communities"),
       ("buyers.html","Buy"),("sellers.html","Sell"),("vendors.html","Vendors"),("contact.html","Contact")]

CREDITS = [
 ("Hero image: AI-edited (mirrored, daylight, people removed) from a photo by","Dan Crile","https://unsplash.com/@dancrile","https://unsplash.com/photos/cKwfDLa5XXw"),
 ("Sunset over the water","Megs Harrison","https://unsplash.com/@mharrisonphotography","https://unsplash.com/photos/Dq3b6rRN6GM"),
 ("Sunset over the water and rocks","Megs Harrison","https://unsplash.com/@mharrisonphotography","https://unsplash.com/photos/rZB9PkayhJQ"),
 ("Pond with fall leaves and a bridge, Rocky River, OH","Ally Griffin","https://unsplash.com/@studio_a","https://unsplash.com/photos/Fd6k4VZR9JA"),
 ("Cleveland skyline from Edgewater Beach","DJ Johnson","https://unsplash.com/@dj_johns1","https://unsplash.com/photos/qQLg8lPYU1k"),
 ("White house with front porch","Josh Lemmon","https://unsplash.com/@wolfie_website","https://unsplash.com/photos/CnbbCRH71Wg"),
]

def pic(name, alt, cls, eager=False, w=2400, h=1400):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<picture><source srcset="assets/img/{name}.webp" type="image/webp"><img class="{cls}" src="assets/img/{name}.jpg" width="{w}" height="{h}" alt="{alt}" {load} decoding="async"></picture>'

def schema(extra=None):
    d = {"@context":"https://schema.org","@type":"RealEstateAgent","@id":SITE_URL+"/#agent",
      "name":"Jennifer Halaska","jobTitle":"REALTOR®","url":SITE_URL+"/",
      "image":SITE_URL+"/assets/img/jennifer-halaska-realtor-bay-village.jpg","telephone":PHONE_TEL,
      "contactPoint":[{"@type":"ContactPoint","telephone":PHONE_TEL,"contactType":"sales","areaServed":"US-OH"},{"@type":"ContactPoint","telephone":OFFICE_TEL,"contactType":"office"}],
      "worksFor":{"@type":"RealEstateAgent","name":BROKERAGE},
      "address":{"@type":"PostalAddress","streetAddress":OFFICE["street"],"addressLocality":OFFICE["city"],"addressRegion":OFFICE["region"],"postalCode":OFFICE["zip"],"addressCountry":"US"},
      "areaServed":[{"@type":"City","name":c+", OH"} for c in ["Bay Village","Westlake","Avon Lake","Rocky River","Lakewood","Fairview Park","North Olmsted","Avon","Cleveland"]],
      "sameAs":[SEARCH_URL],
      "knowsAbout":["Bay Village real estate","Greater Cleveland homes","Lakefront homes","Home valuation"]}
    out=[d]+([extra] if extra else [])
    return "\n".join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>' for x in out)

def crumbs_ld(name,path):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":SITE_URL+"/"},
      {"@type":"ListItem","position":2,"name":name,"item":SITE_URL+"/"+path}]}

def wordmark(tag="a"):
    return '<a class="wordmark" href="index.html" aria-label="Jennifer Halaska Real Estate — home"><span class="wm-name">Jennifer Halaska</span><span class="wm-sub">Real Estate · Bay Village, Ohio</span></a>'

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
<meta property="og:site_name" content="Jennifer Halaska Real Estate">
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
   <div class="btn-row" style="margin:0"><a class="btn btn-white btn-sm" href="contact.html">Contact Jennifer</a><a class="btn btn-ghost-light btn-sm" href="home-value.html">What's my home worth?</a></div>
  </div>
  <div class="footer-grid">
   <div>
    <h3>Jennifer Halaska, REALTOR®</h3>
    <p>Bay Village resident and local market specialist, helping buyers and sellers across Greater Cleveland.</p>
    <p>{OFFICE["street"]}<br>{OFFICE["city"]}, {OFFICE["region"]} {OFFICE["zip"]}</p>
   </div>
   <div>
    <h3>Contact</h3>
    <ul>
     <li><a href="tel:{PHONE_TEL}">{PHONE_DISP}</a></li>
     <li><a href="tel:{OFFICE_TEL}" style="color:#b7bdc2">Office: {OFFICE_DISP}</a></li>
     <li><a href="mailto:{EMAIL}">Email Jennifer</a></li>
     <li><a href="contact.html">Send a message</a></li>
     <li><a href="contact.html?topic=Consultation#contact-form">Schedule a consultation</a></li>
     <li><a href="{SEARCH_URL}" target="_blank" rel="noopener">Search homes for sale ↗</a></li>
    </ul>
   </div>
   <div>
    <h3>Explore</h3>
    <ul><li><a href="index.html">Home</a></li>{"".join(f'<li><a href="{h}">{n}</a></li>' for h,n in NAV)}<li><a href="home-value.html">Home Value</a></li></ul>
   </div>
  </div>
  <div class="legal">
   <span>© <span id="year">{datetime.date.today().year}</span> Jennifer Halaska, REALTOR®. Brokered by {BROKERAGE}. Ohio license {LICENSE}.</span>
   <span>Equal Housing Opportunity. Information deemed reliable but not guaranteed.</span>
  </div>
  <p class="credits">Photography via Unsplash (Unsplash License) — {cr}.</p>
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
<div class="btn-row"><a class="btn btn-dark" href="contact.html?topic=Consultation#contact-form">Schedule a consultation</a><a class="btn btn-outline" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a><a class="btn btn-outline" href="mailto:{EMAIL}">Email</a></div></div></section>'''

AREAS = [
 ("Bay Village","Cuyahoga County","Jennifer's hometown: a lakefront community on Lake Erie with Huntington Reservation, Cahoon Memorial Park and the Bay Village City Schools.","card-bay-village","Sun setting over calm water"),
 ("Westlake","Cuyahoga County","A suburb about 12 miles west of downtown Cleveland with established neighborhoods, newer developments and Crocker Park shopping and dining.","card-westlake","White two-story house with a front porch"),
 ("Rocky River","Cuyahoga County","A lakefront suburb at the mouth of the Rocky River, bordered by the Rocky River Reservation of the Cleveland Metroparks.","card-rocky-river","Pond framed by autumn leaves in Rocky River, Ohio"),
 ("Lakewood","Cuyahoga County","Cleveland's walkable inner-ring neighbor on the lake, known for historic homes, Lakewood Park and busy Detroit and Madison avenues.","card-lakewood","Sunlit Lake Erie shoreline with a rocky breakwall"),
 ("Avon Lake","Lorain County","Lake Erie shoreline living just west of Bay Village, with a mix of lakefront streets and family neighborhoods.","card-avon-lake","Sun setting over a rocky shoreline"),
 ("Greater Cleveland","Cuyahoga County & beyond","From west-side city neighborhoods to the wider metro — Jennifer helps clients wherever their search leads in Greater Cleveland.","card-cleveland","Cleveland skyline across the water from Edgewater Beach"),
 ("Fairview Park","Cuyahoga County","A residential suburb along the Rocky River Reservation with tree-lined streets and quick access to I-480 and I-90.",None,None),
 ("North Olmsted","Cuyahoga County","A west-side suburb with a wide range of home styles and price points, close to Great Northern shopping and I-480.",None,None),
 ("Avon","Lorain County","A growing Lorain County city along the I-90 corridor with newer construction and established subdivisions.",None,None),
]
def slug(n): return n.lower().replace(" ","-")
def comm_cards():
    return "".join(f'<a class="comm" href="{"bay-village.html" if n=="Bay Village" else "areas.html#"+slug(n)}">{pic(img,alt,"",False,720,920)}<div class="comm-body"><span>{c}</span><h3>{n}</h3></div></a>' for n,c,b,img,alt in AREAS if img)

pages={}

# ---------------- HOME ----------------
pages["index.html"] = head("index.html","Bay Village & Greater Cleveland Real Estate | Jennifer Halaska, REALTOR®",
 "Jennifer Halaska is a Bay Village, Ohio REALTOR® helping buyers and sellers in Bay Village, Westlake, Rocky River, Lakewood, Avon Lake and across Greater Cleveland.", body_class="home") + f'''
<section class="hero" aria-label="Introduction">
 {pic("hero-lake-erie-daylight","Sunlit Lake Erie shoreline with a rocky breakwall and sandy beach under a clear blue sky","hero-img",True,2560,1440)}
 <div class="container hero-inner">
  <span class="kicker">Bay Village · Greater Cleveland</span>
  <h1>Bay Village &amp; Greater Cleveland Real Estate</h1>
  <p class="lead">Lakefront living, thoughtful guidance. Jennifer Halaska lives in Bay Village and helps buyers and sellers across Cleveland's west side make confident moves.</p>
  <div class="btn-row">
   <a class="btn btn-white" href="home-value.html">What's my home worth?</a>
   <a class="btn btn-ghost-light" href="{SEARCH_URL}" target="_blank" rel="noopener">Search homes ↗</a>
   <a class="btn btn-ghost-light" href="contact.html">Contact Jennifer</a>
  </div>
 </div>
 <p class="hero-credit">Hero image: AI-edited from a photo by <a href="https://unsplash.com/photos/cKwfDLa5XXw" target="_blank" rel="noopener">Dan Crile (Unsplash)</a></p>
</section>

<section class="bg-white">
 <div class="container split wide-left">
  <div>
   <span class="kicker">Meet Jennifer</span>
   <div class="rule"></div>
   <h2>A neighbor who knows <em>the lake, the streets</em> and the market.</h2>
   <p class="lead">Bay Village isn't just a market Jennifer works in — it's home. That everyday, on-the-ground familiarity with its neighborhoods, lakefront parks and schools shapes the advice she gives every client, from first-time buyers to longtime homeowners ready for what's next.</p>
   <p>While Bay Village is home base, Jennifer serves all of Greater Cleveland, including Westlake, Rocky River, Lakewood, Avon Lake, Fairview Park, North Olmsted and Avon.</p>
   <div class="btn-row"><a class="btn btn-dark" href="about.html">About Jennifer</a><a class="btn btn-outline" href="why-bay-village.html">Why Bay Village?</a></div>
  </div>
  <figure class="portrait" style="margin:0">
   <picture><source srcset="assets/img/jennifer-halaska-realtor-bay-village.webp" type="image/webp"><img src="assets/img/jennifer-halaska-realtor-bay-village.jpg" width="622" height="628" loading="lazy" alt="Portrait of Jennifer Halaska, REALTOR® in Bay Village, Ohio"></picture>
   <figcaption>Jennifer Halaska, REALTOR®</figcaption>
  </figure>
 </div>
</section>

<section>
 <div class="container">
  <div class="section-head"><div><span class="kicker">Featured communities</span><h2>Where Jennifer helps clients <em>live well</em></h2></div><div style="display:flex;gap:2rem;flex-wrap:wrap"><a class="link-arrow" href="why-bay-village.html">Why live in Bay Village →</a><a class="link-arrow" href="areas.html">All communities →</a></div></div>
  <div class="grid g3">{comm_cards()}</div>
 </div>
</section>

<section class="value-band">
 {pic("lake-erie-sunset-shore","Sun setting over the lake","vb-img",False)}
 <div class="container">
  <span class="kicker" style="color:rgba(255,255,255,.85)">For homeowners</span>
  <h2>What's your home worth <em style="color:#dfe6ea">today?</em></h2>
  <p class="lead">Online estimates can't see your updates, your lot or your street. Get a personal, local valuation from Jennifer — no obligation.</p>
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
   <div class="pillar"><span class="num">04</span><h3>A trusted network</h3><p>Introductions to <a href="vendors.html">lenders, inspectors and trades</a> from Jennifer's network.</p></div>
  </div>
 </div>
</section>

<section class="bg-stone">
 <div class="container split">
  <div>
   <span class="kicker">Buying</span><div class="rule"></div>
   <h2>Find the right home — and the right street.</h2>
   <p class="lead">Search current listings across Northeast Ohio, then let Jennifer add the local context you won't find online.</p>
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
<!-- PLACEHOLDER: Testimonials intentionally omitted until Jennifer supplies real, client-approved reviews. -->
{cta()}
''' + foot()

# ---------------- ABOUT ----------------
pages["about.html"] = head("about.html","About Jennifer Halaska | Bay Village, Ohio REALTOR®",
 "Meet Jennifer Halaska, a Bay Village, Ohio resident and REALTOR® serving home buyers and sellers throughout Greater Cleveland.", crumbs_ld("About","about.html")) + page_hero("About","Meet Jennifer Halaska","A Bay Village resident helping buyers and sellers across Greater Cleveland.","About") + f'''
<section class="bg-white">
 <div class="container split wide-left" style="align-items:start">
  <div class="prose">
   <span class="kicker">Bay Village · Greater Cleveland</span><div class="rule"></div>
   <h2 style="margin-top:0">Hello, I'm Jennifer.</h2>
   <!-- PLACEHOLDER: Replace/extend with Jennifer's own bio in her voice (years in Bay Village, family, background, why she loves real estate). Her brokerage "About Me" page is currently blank. -->
   <p class="lead">Bay Village isn't just a market I work in — it's where I live. Living here gives me an everyday, on-the-ground feel for its neighborhoods, lakefront parks and schools, and I bring that local perspective to every client I work with.</p>
   <p>While Bay Village is home base, I help buyers and sellers throughout Greater Cleveland, including Westlake, Rocky River, Lakewood, Avon Lake, Fairview Park, North Olmsted and Avon.</p>
   <p>I'm a member of the Erin Knapp team in Westlake, and I'm licensed with {BROKERAGE}.</p>
   <p class="notice"><strong>[add bio details]</strong> — designations, years licensed, community involvement and a personal note from Jennifer.</p>
   <div class="signature">Jennifer</div>
   <div class="btn-row"><a class="btn btn-dark" href="contact.html">Contact Jennifer</a><a class="btn btn-outline" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a></div>
  </div>
  <figure class="portrait" style="margin:0">
   <picture><source srcset="assets/img/jennifer-halaska-realtor-bay-village.webp" type="image/webp"><img src="assets/img/jennifer-halaska-realtor-bay-village.jpg" width="622" height="628" fetchpriority="high" alt="Portrait of Jennifer Halaska, REALTOR®"></picture>
   <figcaption>Jennifer Halaska, REALTOR®</figcaption>
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
pages["bay-village.html"] = head("bay-village.html","Bay Village, Ohio Neighborhood Guide | Homes, Schools & Parks | Jennifer Halaska",
 "A local's guide to living in Bay Village, Ohio: the Lake Erie shoreline, Huntington Reservation, Cahoon Memorial Park, Bay Village City Schools and more, from REALTOR® Jennifer Halaska.", crumbs_ld("Bay Village Guide","bay-village.html")) + page_hero("Community guide","Living in Bay Village, Ohio","A lakefront suburb on Lake Erie's southern shore on Cleveland's west side — and the place Jennifer calls home.","Bay Village","lake-erie-sunset-shore","Sun setting over the lake") + f'''
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
   <!-- PLACEHOLDER: Add Jennifer's own neighborhood tips (favorite streets, coffee spots, community traditions) in her voice. -->
   <p class="notice">Thinking about a move? See <a href="why-bay-village.html">13 reasons people love living in Bay Village</a>.</p>
   <div class="btn-row"><a class="btn btn-dark" href="{SEARCH_URL}" target="_blank" rel="noopener">Search Bay Village homes ↗</a><a class="btn btn-outline" href="home-value.html">Bay Village home value</a></div>
  </div>
 </div>
</section>
{cta("Buying or selling in Bay Village?","Talk with someone who lives here.")}
''' + foot()

# ---------------- AREAS ----------------
def area_article(n,c,b,img,alt):
    link = '<a class="link-arrow" href="bay-village.html">Read the Bay Village guide →</a>' if n=="Bay Village" else f'<a class="link-arrow" href="contact.html?topic={n.replace(" ","%20")}#contact-form">Ask about {n} →</a>'
    media = f'<div style="aspect-ratio:16/10;overflow:hidden;margin:-2rem -2rem 1.6rem">{pic(img,alt,"",False,720,920).replace("<img ","<img style=\"width:100%;height:100%;object-fit:cover\" ")}</div>' if img else ""
    return f'<article class="card" id="{slug(n)}">{media}<span class="kicker" style="margin-bottom:.5rem">{c}</span><h3>{n}</h3><p>{b}</p>{link}</article>'
pages["areas.html"] = head("areas.html","Communities | Bay Village, Westlake, Rocky River, Lakewood & Avon Lake Real Estate | Jennifer Halaska",
 "Jennifer Halaska helps buyers and sellers in Bay Village, Westlake, Avon Lake, Rocky River, Lakewood, Fairview Park, North Olmsted, Avon and across Greater Cleveland.", crumbs_ld("Communities","areas.html")) + page_hero("Communities","Greater Cleveland, west side and beyond","Bay Village is home base. Jennifer also helps clients buy and sell throughout these neighboring communities and the wider Cleveland area.","Communities") + f'''
<section><div class="container"><div class="grid g3">{"".join(area_article(*a) for a in AREAS)}</div>
<p class="source" style="margin-top:2rem">Don't see your community? Jennifer serves all of Greater Cleveland. <a href="contact.html">Get in touch</a>.</p></div></section>
{cta()}
''' + foot()

# ---------------- BUYERS ----------------
pages["buyers.html"] = head("buyers.html","Buying a Home in Bay Village & Greater Cleveland | Jennifer Halaska, REALTOR®",
 "Thinking about buying a home in Bay Village, Westlake or Greater Cleveland? Jennifer Halaska guides buyers from pre-approval to closing.", crumbs_ld("Buy","buyers.html")) + page_hero("Buying","Find the right home — and the right street","A clear, step-by-step process with a local guide who helps you see beyond the listing photos.","Buy") + f'''
<section class="bg-white">
 <div class="container split wide-left" style="align-items:start">
  <div>
   <h2>How we'll find your home</h2>
   <ol class="steps">
    <li><div><strong>Consultation</strong><span>Talk through your must-haves, timeline, budget and favorite areas.</span></div></li>
    <li><div><strong>Get pre-approved</strong><span>Know your buying power before you shop. A <a href="vendors.html#lenders">lender from Jennifer's network</a> can help.</span></div></li>
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
pages["sellers.html"] = head("sellers.html","Sell Your Home in Bay Village & Greater Cleveland | Jennifer Halaska, REALTOR®",
 "Selling in Bay Village, Westlake, Rocky River or Greater Cleveland? Get local pricing insight, preparation advice and polished marketing with Jennifer Halaska.", crumbs_ld("Sell","sellers.html")) + page_hero("Selling","Sell with a plan, a price and a strategy","Pricing, preparation and marketing built around your home, your street and your timeline.","Sell") + f'''
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
def lead_form(subject, fields_html, button):
    return f'''<!-- PLACEHOLDER: create a free form at https://formspree.io and replace YOUR_FORM_ID. Until then, submitting opens the visitor's email app (mailto fallback). -->
<form id="contact-form" class="lead-form" action="{FORMSPREE}" method="POST" data-mailto="{EMAIL}" data-subject="{subject}">
 <input type="hidden" name="_subject" value="{subject}">
 <div class="hp" aria-hidden="true"><label for="_gotcha">Leave blank</label><input type="text" id="_gotcha" name="_gotcha" tabindex="-1" autocomplete="off"></div>
 {fields_html}
 <button class="btn btn-dark" type="submit">{button}</button>
 <p class="form-note" style="margin-top:1.2rem">Prefer to talk? Call <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a> or <a href="mailto:{EMAIL}">email Jennifer</a>.</p>
</form>'''
NAME_FIELDS = '''<div class="row"><div class="field"><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div><div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div></div>
 <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>'''
hv_fields = '''<div class="field"><label for="address">Property address</label><input id="address" name="address" autocomplete="street-address" required></div>
 <div class="row"><div class="field"><label for="beds">Bedrooms</label><input id="beds" name="bedrooms" inputmode="numeric"></div><div class="field"><label for="baths">Bathrooms</label><input id="baths" name="bathrooms" inputmode="decimal"></div></div>
 <div class="row"><div class="field"><label for="timeline">Thinking of selling</label><select id="timeline" name="timeline"><option>Just curious</option><option>0–3 months</option><option>3–6 months</option><option>6–12 months</option><option>12+ months</option></select></div><div class="field"><label for="updates">Recent updates</label><input id="updates" name="updates" placeholder="Kitchen, roof, baths…"></div></div>
 ''' + NAME_FIELDS
pages["home-value.html"] = head("home-value.html","What's My Home Worth? Bay Village & Cleveland Home Valuation | Jennifer Halaska",
 "Request a free, personal home valuation for your Bay Village, Westlake, Rocky River or Greater Cleveland home from local REALTOR® Jennifer Halaska.", crumbs_ld("Home Value","home-value.html")) + page_hero("Home valuation","What's your home worth?","A personal, local valuation — not an algorithm. Share a few details and Jennifer will follow up with a no-obligation analysis.","Home Value","lake-erie-sunset-shore","Sun setting over the lake") + f'''
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
pages["why-bay-village.html"] = head("why-bay-village.html","Why Live in Bay Village, Ohio | Jennifer Halaska",
 "13 reasons to live in Bay Village, Ohio: tree-lined streets, Lake Erie views, Huntington Beach, the Nature &amp; Science Center, five-star schools, kids biking to school and a short drive to Cleveland Hopkins Airport.", LIST_LD) + page_hero("Why Bay Village","Why live in Bay Village, Ohio?","Lake Erie on one side, tree-lined streets on the other, and a small-town spirit just minutes from Cleveland. Here's why Jennifer, and so many families, call Bay Village home.","<a href=\"bay-village.html\">Bay Village</a> / Why Bay Village","hero-lake-erie-daylight","Sunlit Lake Erie shoreline with a rocky breakwall and sandy beach") + f'''
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
  <figure style="margin:0" class="portrait">{pic("card-rocky-river","Autumn trees reflected in a quiet pond","",False,720,920)}</figure>
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
{cta("Ready to make Bay Village home?","Jennifer lives here and would love to show you around: streets, schools, parks and homes.")}
''' + foot()

# ---------------- VENDORS ----------------
CATS = [("lenders","Mortgage Lenders"),("inspectors","Home Inspectors"),("title","Title Companies"),("attorneys","Real Estate Attorneys"),
        ("contractors","Contractors & Trades"),("movers","Movers"),("stagers","Home Stagers"),("photographers","Real Estate Photographers"),("insurance","Insurance Agents")]
def vcard(cat):
    return f'''<article class="vendor-card"><!-- PLACEHOLDER: replace with a real vendor from Jennifer's network ({cat}) --><span class="ph">Placeholder</span><h3>[Vendor business name]</h3><p>[One-line description and why Jennifer recommends them.]</p><dl><dt>Contact</dt><dd>[Contact name]</dd><dt>Phone</dt><dd>[Phone]</dd><dt>Web</dt><dd>[Website]</dd><dt>Serves</dt><dd>[Areas served]</dd></dl></article>'''
vsecs = "".join(f'<section class="vendor-cat" id="{i}" aria-labelledby="h-{i}" style="padding-bottom:0"><div class="vc-head"><h2 id="h-{i}">{n}</h2><span>Trusted network</span></div><div class="grid g3">{vcard(n)}{vcard(n)}</div></section>' for i,n in CATS)
pages["vendors.html"] = head("vendors.html","Recommended Vendors in Greater Cleveland | Lenders, Inspectors & More | Jennifer Halaska",
 "Jennifer Halaska's recommended vendors for Bay Village and Greater Cleveland homeowners: lenders, inspectors, title, attorneys, contractors, movers, stagers, photographers and insurance.", crumbs_ld("Recommended Vendors","vendors.html")) + page_hero("Recommended vendors","Jennifer's trusted local network","Good professionals make every move smoother. These are vendors from Jennifer's trusted network across Bay Village and Greater Cleveland.","Vendors") + f'''
<section class="bg-white" style="padding-top:3.5rem">
 <div class="container">
  <nav class="vendor-nav" aria-label="Vendor categories">{"".join(f'<a href="#{i}">{n}</a>' for i,n in CATS)}</nav>
  <p class="notice">Vendors listed here are from Jennifer's trusted professional network. Recommendations are provided as a courtesy; you are free to choose any provider. <!-- PLACEHOLDER: confirm disclosure language with the brokerage's compliance team (RESPA / affiliated business disclosures) before publishing. --></p>
  {vsecs}
  <div class="card" style="margin-top:4rem;background:var(--stone)"><h3>Are you a local professional?</h3><p>Jennifer is always glad to meet reliable local professionals who take great care of clients. <a href="contact.html?topic=Vendor%20network#contact-form">Introduce yourself</a>.</p></div>
 </div>
</section>
{cta()}
''' + foot()

# ---------------- CONTACT ----------------
topics = ["General question","Buying","Selling","Home value","Consultation","Showing","Bay Village","Vendor network"]
c_fields = NAME_FIELDS + f'''
 <div class="row"><div class="field"><label for="topic">I'm interested in</label><select id="topic" name="topic">{"".join(f'<option>{t}</option>' for t in topics)}</select></div><div class="field"><label for="timeline">Timeline</label><select id="timeline" name="timeline"><option>Just exploring</option><option>0–3 months</option><option>3–6 months</option><option>6–12 months</option><option>12+ months</option></select></div></div>
 <div class="field"><label for="message">Message</label><textarea id="message" name="message" rows="5" placeholder="Tell Jennifer what you're looking for, or suggest times for a consultation."></textarea></div>
 '''
pages["contact.html"] = head("contact.html","Contact Jennifer Halaska | Bay Village & Greater Cleveland REALTOR®",
 "Contact Jennifer Halaska, REALTOR® in Bay Village and Greater Cleveland. Call (330) 807-6374, email, or send a message to schedule a consultation.", crumbs_ld("Contact","contact.html")) + page_hero("Contact","Let's talk about your next move","Call, email or send a note below — Jennifer will be in touch.","Contact") + f'''
<section class="bg-white">
 <div class="container contact-grid">
  <div>
   <span class="kicker">Get in touch</span><div class="rule"></div>
   <h2>Jennifer Halaska, REALTOR®</h2>
   <ul class="contact-list">
    <li><span class="lbl">Phone</span><a href="tel:{PHONE_TEL}">{PHONE_DISP}</a><br><span class="form-note">Office: <a style="font-family:var(--sans);font-size:.85rem" href="tel:{OFFICE_TEL}">{OFFICE_DISP}</a></span></li>
    <li><span class="lbl">Email</span><a href="mailto:{EMAIL}">{EMAIL_SHOWN}</a></li>
    <li><span class="lbl">Office</span><span style="font-family:var(--serif);font-size:1.3rem;color:var(--char)">{OFFICE["street"]}, {OFFICE["city"]}, {OFFICE["region"]} {OFFICE["zip"]}</span><br><a class="link-arrow" style="font-family:var(--sans);font-size:.72rem" href="https://www.google.com/maps/search/?api=1&amp;query=2055+Crocker+Rd+Suite+101+Westlake+OH+44145" target="_blank" rel="noopener">Directions ↗</a></li>
    <li><span class="lbl">Search homes</span><a href="{SEARCH_URL}" target="_blank" rel="noopener">View current listings ↗</a></li>
   </ul>
   <img src="assets/img/jennifer-halaska-sm.jpg" width="300" height="303" loading="lazy" alt="Jennifer Halaska, REALTOR®" style="width:150px;height:150px;object-fit:cover;border-radius:50%">
  </div>
  <div class="form-card" id="message-form"><h2 style="font-size:2.2rem">Send a message</h2>{lead_form("New inquiry from website", c_fields, "Send message")}</div>
 </div>
</section>
''' + foot()

pages["404.html"] = head("404.html","Page not found | Jennifer Halaska Real Estate","The page you were looking for could not be found.",robots="noindex") + page_hero("404","Page not found","Sorry, that page doesn't exist. Try the <a href=\"index.html\">home page</a> or <a href=\"contact.html\">contact Jennifer</a>.","Not found") + foot()

for name,html in pages.items():
    open(os.path.join(ROOT,name),"w",encoding="utf-8").write(html)
today=datetime.date.today().isoformat()
pri={"index.html":"1.0","why-bay-village.html":"0.9","contact.html":"0.9","bay-village.html":"0.9","home-value.html":"0.9"}
with open(os.path.join(ROOT,"sitemap.xml"),"w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for n in pages:
        if n=="404.html": continue
        f.write(f"  <url><loc>{SITE_URL}/{'' if n=='index.html' else n}</loc><lastmod>{today}</lastmod><priority>{pri.get(n,'0.7')}</priority></url>\n")
    f.write("</urlset>\n")
open(os.path.join(ROOT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\nDisallow: /screenshots/\n\nSitemap: {SITE_URL}/sitemap.xml\n")
print("built",len(pages),"pages")
