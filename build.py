#!/usr/bin/env python3
"""Static site generator for New Life Furniture. Run: python3 build.py  -> writes HTML into this folder.
Edit content in PAGES / SERVICES below; layout lives in page()."""
import json, os, html
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://www.newlifefurniture.com"  # production domain (canonical, sitemap, schema)
DIMS = json.load(open(ROOT / "dims.json"))

BIZ = dict(
    name="New Life Furniture Mfg.",
    phone="(954) 895-8504", tel="+19548958504",
    phone2="(786) 348-8650", tel2="+17863488650",
    email="Ian@newlifefurniture.com",
    street="380 NE 56th St, Unit 380", city="Miami", region="FL", zip="33137",
    whatsapp="19548958504",  # confirmed by client: main line has WhatsApp
    angi="",  # TODO: paste the client's Angi profile URL -> badges link to it and it's added to schema sameAs
    instagram="https://www.instagram.com/newlifefurnituremfg",
)
WA_TEXT = "Hi%20New%20Life%20Furniture%2C%20I%27d%20like%20a%20free%20estimate."
GTM_ID = "GTM-NW3P7QNL"        # existing container found on the live site
FORMSPREE_ID = ""             # TODO: create a Formspree form (or other endpoint) and paste its ID

e = html.escape

# ---------- components ----------
# What each photo actually shows (verified visually). img() always uses these, so alt text stays truthful.
ALT = {
    "armchair": "Carved wood armchair reupholstered in yellow fabric",
    "barchairs": "Rooftop terrace bar seating overlooking Miami",
    "beforeafter": "Mid-century lounge chairs being reupholstered in the workshop",
    "booth2": "Restaurant booths with patterned upholstered backs",
    "booths": "Tufted leather restaurant booth",
    "dining": "White dining chair reupholstered in floral fabric",
    "drapes": "Living room finished with custom sheer draperies",
    "drapes2": "Bright living room with custom sheer draperies",
    "hero": "Living room with lounge chairs reupholstered in blue fabric",
    "hospital": "Upholstered bench cushions in a clinic room",
    "leather": "Wood-frame lounge seating with custom cushions in a commercial space",
    "lounge": "Diamond-stitched orange booth seating in the workshop",
    "marine": "Blue marine-vinyl helm chair on a boat",
    "whaler": "Boston Whaler helm seats reupholstered in white and gray marine vinyl",
    "whaler2": "Boston Whaler bow seating with new marine-grade cushions",
    "whaler3": "Boat bench seat and backrest recovered in white marine vinyl",
    "marinechair": "Teak and stainless director's chair with new white marine fabric",
    "marinechair2": "Teak director's chair recovered in white marine fabric, rear view",
    "diningchair": "Modern dining chair reupholstered in charcoal leather",
    "diningset": "Dining set with four chairs reupholstered in charcoal leather",
    "drapes3": "Dining room with custom drapery panels framing plantation shutters",
    "drapes4": "Custom sheer draperies with an upholstered patterned cornice",
    "tufted": "Custom curved banquette in button-tufted oxblood leather",
    "loungechairs": "Pair of custom mid-century lounge chairs with cream cushions",
    "poufs": "Custom round upholstered poufs in green and blue vinyl",
    "louis": "French-style oval-back armchair upholstered in white",
    "bench": "Custom upholstered bench at the foot of a four-poster bed",
    "about": "Upholstery craftsman in the furniture workshop",
    "marine2": "Outdoor folding chair with marine-grade fabric",
    "outdoor": "Patio furniture with custom navy outdoor cushions",
    "outdoor2": "Poolside daybed with custom outdoor cushions",
    "patio": "Pool deck lounge chairs for a residential tower",
    "reception": "Curved commercial lounge seating in orange and green",
    "refin": "Refinished dining tables with upholstered banquette",
    "refindining": "Refinished dining set with upholstered chairs",
    "reup": "Leather lounge chairs reupholstered for a music room",
    "sectional": "Red leather armchair and ottoman",
    "sofa": "White sofa reupholstered for a waterfront living room",
    "team": "Traditional living room set reupholstered in gold fabric",
    "waiting": "L-shaped upholstered banquette",
    "yacht": "Yacht bar with diamond-stitched blue upholstery and stools",
}

def img(name, alt, sizes="(min-width: 900px) 50vw, 100vw", eager=False, cls=""):
    w, h = DIMS[name]
    alt = ALT.get(name, alt)
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="/img/{name}.webp" srcset="/img/{name}-700.webp 700w, /img/{name}.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" {load}{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>')

def cta_row(dark=False):
    return (f'<div class="cta-row"><a class="btn btn-primary" href="/contact-new-life-furniture-miami/">Request a Free Estimate</a>'
            f'<a class="btn {"btn-ghost-light" if dark else "btn-ghost"}" href="tel:{BIZ["tel"]}" data-ev="cta">Call {BIZ["phone"]}</a></div>')

def faq(items):
    out = "".join(f'<details><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in items)
    return f'<div class="faq">{out}</div>'

def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in items]}

SERVICE_OPTS = ["Furniture reupholstery", "Custom upholstered furniture", "Booths & banquettes",
                "Commercial / contract upholstery", "Marine upholstery", "Outdoor cushions",
                "Draperies & window treatments", "Furniture refinishing", "Other"]

def form(preselect=""):
    opts = "".join(f'<option{" selected" if o == preselect else ""}>{o}</option>' for o in SERVICE_OPTS)
    return f'''<form class="lead-form" novalidate data-endpoint="{FORMSPREE_ID}">
  <h3 class="form-title">Request a free estimate</h3>
  <p class="form-sub">Tell us about your piece or project. Most requests take less than a minute.</p>
  <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
  <div class="field-2">
    <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
    <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
  </div>
  <div class="field-2">
    <div class="field"><label for="f-service">Service</label><select id="f-service" name="service">{opts}</select></div>
    <fieldset class="field seg"><legend>Project type</legend>
      <label><input type="radio" name="project_type" value="Residential" checked> Residential</label>
      <label><input type="radio" name="project_type" value="Commercial"> Commercial</label>
    </fieldset>
  </div>
  <div class="field"><label for="f-msg">Project details <span class="opt">(optional)</span></label><textarea id="f-msg" name="message" rows="3" placeholder="e.g. 6 dining chairs, new fabric, Coral Gables"></textarea></div>
  <div class="hp" aria-hidden="true"><label>Leave empty<input name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
  <input type="hidden" name="gclid"><input type="hidden" name="gbraid"><input type="hidden" name="wbraid"><input type="hidden" name="page">
  <button class="btn btn-primary btn-block" type="submit">Send request</button>
  <p class="form-status" role="status" aria-live="polite"></p>
  <p class="fine">By submitting, you agree to be contacted about your request. We never share your information. Prefer to talk? Call <a href="tel:{BIZ["tel"]}" data-ev="form">{BIZ["phone"]}</a>.</p>
</form>'''

def card(href, image, title, text, alt):
    return (f'<a class="card" href="{href}"><div class="card-img">{img(image, alt, "(min-width: 900px) 40vw, 100vw")}</div>'
            f'<div class="card-body"><h3>{title}</h3><p>{text}</p><span class="arrow" aria-hidden="true">→</span></div></a>')

TESTIMONIALS = [
    ("Ian and Mercedes are excellent professionals. They provided very high-quality services and completed the work within the time frame we needed. The chair upholstery turned out excellent!", "Client review, April 2025"),
    ("Ian has extensive furniture experience, including custom construction and upholstery. My project involved recovering expensive outdoor cushions in hand-sewn Sunbrella fabric. They look great!", "Outdoor cushion client"),
    ("Ian was very professional. He helped us with our new patio replacement cushions. He was very honest and prompt in responding to our questions. The project turned out beautifully and was completed on time and within his original estimate.", "Patio cushion client"),
    ("My dining room chairs look like new! Everything was top-notch, from the initial consultation to choose the fabric, the time it took to complete the work, and the quality of the final product.", "Dining chair client, November 2022"),
]
ANGI = '<img src="/img/angi-2025.webp" width="359" height="400" alt="Angi Super Service Award 2025" class="angi-img"{}>'
def angi_badge(cls="", lazy=True):
    inner = f'{ANGI.format(" loading=lazy" if lazy else "")}<p><strong>Angi Super Service Award</strong><span>2025 winner{" · Read our Angi reviews →" if BIZ["angi"] else ""}</span></p>'
    if BIZ["angi"]:
        return f'<a class="angi {cls}" href="{BIZ["angi"]}" target="_blank" rel="noopener" data-ev="angi">{inner}</a>'
    return f'<div class="angi {cls}">{inner}</div>'

def car_ctrl(target, label, light=False):
    return (f'<div class="car-ctrl{" light" if light else ""}"><button type="button" class="car-btn" data-dir="-1" aria-controls="{target}" aria-label="Previous {label}">←</button>'
            f'<span class="car-count" aria-live="polite"></span><button type="button" class="car-btn" data-dir="1" aria-controls="{target}" aria-label="Next {label}">→</button></div>')

def testimonials(n=4):
    q = "".join(f'<figure class="quote"><blockquote>“{e(t)}”</blockquote><figcaption>{e(a)}</figcaption></figure>' for t, a in TESTIMONIALS[:n])
    return f'<section class="section sand"><div class="wrap"><p class="eyebrow">Client words</p><div class="car" data-car><div class="row-head"><h2>What our clients say</h2>{car_ctrl("quotes", "review")}</div><div class="quotes car-track" id="quotes" tabindex="0" aria-label="Client reviews">{q}</div></div></div></section>'

PROCESS = [
    ("Tell us about the piece", "Call, send the form, or share photos. We'll ask about size, use, and the look you want."),
    ("Consultation & fabric", "We review the furniture and help you choose fabric, leather, vinyl, or marine-grade material for how it will be used."),
    ("Clear written estimate", "You receive a free estimate with scope and timing before any work begins."),
    ("Crafted in our Miami shop", "Our craftsmen rebuild, re-pad, and upholster by hand, then deliver the finished piece."),
]
STEP_ICONS = [
    '<path d="M4 5h16v11H8l-4 4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
    '<path d="M5 4h14v16H5zM5 9h14M5 14h14" fill="none" stroke="currentColor" stroke-width="1.8"/>',
    '<path d="M7 3h7l4 4v14H7zM14 3v4h4M10 12h5M10 16h5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
    '<path d="M4 18c3-1 4-4 4-7h8c0 3 1 6 4 7M6 18h12v3H6zM9 11V7a3 3 0 016 0v4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
]
def process():
    s = "".join(f'<li><div class="step-mark"><span class="step-num">{i}</span><svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true">{STEP_ICONS[i-1]}</svg></div>'
                f'<div><p class="step-label">Step {i}</p><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for i, (t, d) in enumerate(PROCESS, 1))
    return f'''<section class="section process"><div class="wrap process-grid">
  <div class="process-intro"><p class="eyebrow">How it works</p><h2>From first call to finished piece in <em>4 simple steps</em></h2>
  <p class="lead">No surprises: you see the fabric, the price, and the timeline before we start.</p>
  <a class="btn btn-primary" href="/contact-new-life-furniture-miami/">Start with step 1</a></div>
  <ol class="timeline">{s}</ol>
</div></section>'''

def final_cta(title="Ready to give your furniture a new life?"):
    return f'''<section class="section dark final"><div class="wrap final-grid">
  <div><p class="eyebrow">Free estimates</p><h2>{title}</h2>
  <p class="lead">Send a few photos and details. We'll review them and get back to you with next steps.</p>
  {angi_badge("on-dark")}
  <ul class="contact-list"><li><a href="tel:{BIZ["tel"]}" data-ev="final">{BIZ["phone"]}</a></li><li><a href="mailto:{BIZ["email"]}" data-ev="final">{BIZ["email"]}</a></li><li>{BIZ["street"]}, {BIZ["city"]}, {BIZ["region"]} {BIZ["zip"]}</li></ul></div>
  {form()}
</div></section>'''

# ---------- service landing page template ----------
def service_page(s):
    bullets = "".join(f"<li>{b}</li>" for b in s["includes"])
    gallery = "".join(f'<figure>{img(g, a, "(min-width: 900px) 33vw, 50vw")}</figure>' for g, a in s["gallery"])
    related = "".join(card(*r) for r in s["related"])
    body = f'''
<section class="lp-hero photo"><div class="hero-bg">{img(s["image"], s["image_alt"], sizes="100vw", eager=True)}</div><div class="wrap lp-grid">
  <div class="lp-copy">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>{s["crumb"]}</span></nav>
    <h1>{s["h1"]}</h1>
    <p class="lead">{s["lead"]}</p>
    <ul class="ticks">{"".join(f"<li>{t}</li>" for t in s["ticks"])}</ul>
    {angi_badge("on-dark", lazy=False)}
    <a class="btn btn-ghost-light" href="tel:{BIZ["tel"]}" data-ev="hero">Call {BIZ["phone"]}</a>
  </div>
  <div class="lp-form">{form(s["service"])}</div>
</div></section>
<section class="section"><div class="wrap split">
  <div class="split-img">{img(s["gallery"][0][0], s["gallery"][0][1])}</div>
  <div><p class="eyebrow">{s["crumb"]}</p><h2>{s["h2"]}</h2>{s["body"]}<h3>What's included</h3><ul class="checks">{bullets}</ul></div>
</div></section>
<section class="section dark"><div class="wrap"><p class="eyebrow">Recent work</p><div class="car" data-car><div class="row-head"><h2>{s["gallery_title"]}</h2>{car_ctrl("svc-gal", "photo", light=True)}</div><div class="mosaic m3 car-track" id="svc-gal">{gallery}</div></div>
<p class="center"><a class="link light" href="/projects/">See more projects <span aria-hidden="true">→</span></a></p></div></section>
{process()}
<section class="section"><div class="wrap narrow"><p class="eyebrow">FAQ</p><h2>Common questions</h2>{faq(s["faq"])}</div></section>
{testimonials(2)}
<section class="section"><div class="wrap"><p class="eyebrow">Related services</p><h2>You may also need</h2><div class="cards">{related}</div></div></section>
{final_cta()}'''
    schema = [
        {"@type": "Service", "name": s["crumb"], "serviceType": s["crumb"], "provider": {"@id": SITE + "/#business"},
         "areaServed": {"@type": "AdministrativeArea", "name": "South Florida"}, "url": SITE + s["path"]},
        faq_schema(s["faq"]),
    ]
    return page(s["path"], s["title"], s["desc"], body, s["crumb"], schema, preload=s["image"], preload_sizes="100vw")

# ---------- shell ----------
NAV = [("/upholstery-re-upholstery/", "Furniture Reupholstery"), ("/custom-upholstered-furniture/", "Custom Upholstered Furniture"), ("/commercial/", "Commercial Upholstery"),
       ("/booths-banquettes/", "Booths & Banquettes"), ("/marine/", "Marine Upholstery"),
       ("/outdoor-cushions/", "Outdoor Cushions"), ("/draperies/", "Custom Draperies"), ("/projects/", "Projects"), ("/about/", "About")]

N_SERV = 7  # number of service pages at the start of NAV

def page(path, title, desc, body, crumb=None, extra_schema=(), preload=None, noindex=False, preload_sizes="(min-width: 900px) 50vw, 100vw"):
    url = SITE + path
    cur = lambda h: ' aria-current="page"' if h == path else ""
    subs = "".join(f'<li><a href="{h}"{cur(h)}>{t}</a></li>' for h, t in NAV[:N_SERV])
    in_services = any(h == path for h, _ in NAV[:N_SERV])
    nav = (f'<li class="has-sub"><button class="sub-btn{" active" if in_services else ""}" aria-expanded="false" aria-controls="sub-services">Services<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>'
           f'<ul class="sub" id="sub-services">{subs}</ul></li>'
           + "".join(f'<li><a href="{h}"{cur(h)}>{t}</a></li>' for h, t in NAV[N_SERV:])
           + f'<li><a href="/contact-new-life-furniture-miami/"{cur("/contact-new-life-furniture-miami/")}>Contact</a></li>')
    graph = [BUSINESS_SCHEMA, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BIZ["name"]}]
    if crumb:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]})
    graph += list(extra_schema)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    pre = f'<link rel="preload" as="image" href="/img/{preload}.webp" imagesrcset="/img/{preload}-700.webp 700w, /img/{preload}.webp {DIMS[preload][0]}w" imagesizes="{preload_sizes}" fetchpriority="high">' if preload else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{url}">'}
<meta property="og:type" content="website"><meta property="og:site_name" content="{BIZ["name"]}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/img/og.jpg"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#24221f">
<link rel="icon" href="/img/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&display=swap">
{pre}
<link rel="stylesheet" href="/styles.css">
<script>window.dataLayer=window.dataLayer||[];</script>
<!-- Google Tag Manager (existing container from the live site) -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-in">
  <a class="logo" href="/" aria-label="New Life Furniture home"><img src="/img/logo.png" width="768" height="294" alt="New Life Furniture"></a>
  <nav class="nav" aria-label="Main"><ul id="menu">{nav}</ul></nav>
  <div class="header-cta"><a class="call-btn" href="tel:{BIZ["tel"]}" data-ev="header" aria-label="Call {BIZ["phone"]}"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1z"/></svg><span>{BIZ["phone"]}</span></a><a class="btn btn-primary btn-sm" href="/contact-new-life-furniture-miami/">Free Estimate</a></div>
  <button class="menu-btn" aria-expanded="false" aria-controls="menu" aria-label="Open menu"><span></span><span></span></button>
</div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="wrap foot-grid">
  <div><img class="foot-logo" src="/img/logo.png" width="768" height="294" alt="New Life Furniture" loading="lazy">{angi_badge("on-dark foot-angi")}
  <p>Custom upholstery, reupholstery, and fabrication for homes and businesses across South Florida for more than 30 years.</p></div>
  <div><h2 class="foot-h">Services</h2><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV[:N_SERV])}<li><a href="/upholstery-re-upholstery/#refinishing">Refinishing</a></li></ul></div>
  <div><h2 class="foot-h">Visit or call</h2><address>{BIZ["name"]}<br>{BIZ["street"]}<br>{BIZ["city"]}, {BIZ["region"]} {BIZ["zip"]}</address>
  <ul><li><a href="tel:{BIZ["tel"]}" data-ev="footer">{BIZ["phone"]}</a></li><li><a href="tel:{BIZ["tel2"]}" data-ev="footer">{BIZ["phone2"]}</a></li><li><a href="mailto:{BIZ["email"]}" data-ev="footer">{BIZ["email"]}</a></li><li><a href="{BIZ["instagram"]}" rel="noopener" target="_blank">Instagram</a></li></ul></div>
</div><div class="wrap foot-bottom"><p>© <span id="yr">2026</span> {BIZ["name"]} · Miami, Florida</p><p><a href="/contact-new-life-furniture-miami/">Request an estimate</a></p></div></footer>
<div class="wa-wrap"><p class="wa-bubble" role="status"><button type="button" class="wa-close" aria-label="Dismiss">×</button><strong>Questions about your project?</strong><span>Send us photos on WhatsApp for a quick quote.</span></p>
<a class="wa-float" href="https://wa.me/{BIZ["whatsapp"]}?text={WA_TEXT}" target="_blank" rel="noopener" data-ev="float" aria-label="Chat with us on WhatsApp"><span class="wa-icon"><svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 00-11.2 19.6L3 29l6.6-1.7A13 13 0 1016 3zm0 23.7a10.7 10.7 0 01-5.5-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.7 10.7 0 1116 26.7zm5.9-8c-.3-.2-1.9-1-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.8 8.8 0 01-4.4-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 00-.9.4 3.7 3.7 0 00-1.1 2.7 6.4 6.4 0 001.3 3.4 14.6 14.6 0 005.6 5c2.1.9 2.9 1 4 .8a3.4 3.4 0 002.2-1.6 2.8 2.8 0 00.2-1.6c0-.2-.3-.3-.6-.5z"/></svg></span><span class="wa-label">Chat on WhatsApp</span><span class="wa-dot" aria-hidden="true"></span></a></div>
<a class="mobile-call" href="tel:{BIZ["tel"]}" data-ev="sticky"><span>Call now</span></a><a class="mobile-quote" href="/contact-new-life-furniture-miami/">Free estimate</a>
<script src="/main.js" defer></script>
</body>
</html>'''

BUSINESS_SCHEMA = {
    "@type": "HomeAndConstructionBusiness", "@id": SITE + "/#business", "name": BIZ["name"],
    "alternateName": "New Life Furniture", "url": SITE + "/", "logo": SITE + "/img/logo.png", "image": SITE + "/img/og.jpg",
    "telephone": BIZ["tel"], "email": BIZ["email"],
    "address": {"@type": "PostalAddress", "streetAddress": BIZ["street"], "addressLocality": BIZ["city"],
                "addressRegion": BIZ["region"], "postalCode": BIZ["zip"], "addressCountry": "US"},
    "areaServed": {"@type": "AdministrativeArea", "name": "South Florida"},
    "sameAs": [u for u in (BIZ["instagram"], BIZ["angi"]) if u],
    "award": "Angi Super Service Award 2025",
}

# ---------- content ----------
C = lambda *a: a  # related card tuple helper
R_REUP = C("/upholstery-re-upholstery/", "reup", "Reupholstery", "Sofas, chairs, and heirlooms rebuilt and recovered.", "Reupholstered armchair in new fabric")
R_COM = C("/commercial/", "reception", "Commercial", "Contract upholstery for hospitality, healthcare, and offices.", "Reupholstered reception sofa in a commercial lobby")
R_BOOTH = C("/booths-banquettes/", "booths", "Booths & Banquettes", "Built and reupholstered restaurant seating.", "Restaurant booths after reupholstery")
R_MAR = C("/marine/", "whaler", "Marine", "Boat and yacht seating in marine-grade vinyl.", "Custom marine bench upholstery")
R_OUT = C("/outdoor-cushions/", "outdoor", "Outdoor Cushions", "Patio cushions in performance outdoor fabrics.", "Custom outdoor patio cushions in Miami")
R_CUST = C("/custom-upholstered-furniture/", "tufted", "Custom Furniture", "Sofas, banquettes, benches, and chairs built to your measurements.", "")
R_DRP = C("/draperies/", "drapes4", "Draperies", "Custom draperies, shades, and window treatments.", "Custom draperies installed in a living room")

SERVICES = [
 dict(path="/upholstery-re-upholstery/", crumb="Furniture Reupholstery", service="Furniture reupholstery",
  title="Furniture Reupholstery in Miami | New Life Furniture",
  desc="Expert furniture reupholstery and custom upholstery in Miami and South Florida. Sofas, chairs, dining sets, and antiques. 30+ years. Free estimates.",
  h1="Furniture reupholstery in Miami, done by hand",
  lead="Keep the furniture you love and make it look, feel, and sit like new. We rebuild, re-pad, and recover sofas, chairs, sectionals, and heirlooms for homes across South Florida.",
  ticks=["30+ years of upholstery craftsmanship", "Fabrics, leather, and vinyl to choose from", "Free, no-obligation estimates"],
  image="sofa", image_alt="Living room sofa reupholstered in new fabric",
  h2="Better than new, often for less than replacement",
  body="<p>Well-built furniture is worth saving. Frames from decades ago are often stronger than what's sold today. Our upholsterers strip the piece to the frame, repair joints and springs, replace worn foam and padding, and recover it in the material you choose.</p><p>Not sure about fabric? We'll bring samples and guide you toward options that suit the room, the way you live, and South Florida's sun and humidity.</p><h3 id=\"refinishing\">Wood refinishing, too</h3><p>Exposed wood arms, legs, and dining tables can be refinished to match, so the whole piece looks complete.</p>",
  includes=["Sofas, loveseats, and sectionals", "Dining and accent chairs", "Headboards and ottomans", "Antique and heirloom pieces", "New foam, padding, and spring repair", "Wood touch-up and refinishing"],
  gallery_title="Residential reupholstery projects",
  gallery=[("diningset", ""), ("armchair", ""), ("diningchair", ""), ("reup", ""), ("team", ""), ("dining", "")],
  faq=[("Is it worth reupholstering my furniture instead of buying new?", "If the frame is solid hardwood and you like the shape and size, reupholstery usually gives you a better-built piece than a comparable new one. We'll tell you honestly if a piece isn't worth the investment."),
       ("How much does reupholstery cost?", "Cost depends on the size and style of the piece, the amount of fabric needed, the material you choose, and any frame or cushion repairs. Send us photos for a free estimate."),
       ("Can I supply my own fabric?", "Yes. We'll confirm the yardage you need before you order. We can also help you select fabric, leather, or vinyl."),
       ("How long does it take?", "Timing depends on the piece and material availability. Your written estimate includes the expected timeline."),
       ("Do you pick up and deliver?", "Ask us when you request your estimate and we'll confirm the options for your location.")],
  related=[R_CUST, R_OUT, R_DRP]),
 dict(path="/custom-upholstered-furniture/", crumb="Custom Upholstered Furniture", service="Custom upholstered furniture",
  title="Custom Upholstered Furniture Miami | New Life Furniture",
  desc="Custom upholstered furniture made in Miami: sofas, banquettes, benches, headboards, and chairs built to your size and style. Free estimates.",
  h1="Custom upholstered furniture, made to measure",
  lead="When the right piece doesn't exist, we build it. Sofas, banquettes, benches, headboards, and chairs designed around your space, your measurements, and your style, for homes and businesses across South Florida.",
  ticks=["Built to your exact dimensions", "Fine fabrics, leather, vinyl, and performance materials", "Free design consultation and estimate"],
  image="tufted", image_alt="",
  h2="A piece designed for your space, not a showroom",
  body="<p>Bring us a sketch, a photo you love, or a designer's drawing. We'll confirm dimensions, comfort, and construction details, help you choose the material, and build the piece in our Miami workshop.</p><p>We work with homeowners, interior designers, and businesses that need seating to fit an unusual layout or match an existing design.</p>",
  includes=["Sofas, sectionals, and loveseats", "Banquettes and built-in seating", "Upholstered benches and ottomans", "Headboards and bed frames", "Accent and dining chairs", "Designer and contract pieces built to spec"],
  gallery_title="Custom furniture projects",
  gallery=[("tufted", ""), ("bench", ""), ("loungechairs", ""), ("poufs", ""), ("louis", ""), ("reception", "")],
  faq=[("Can you build a piece from a photo or drawing?", "Yes. Share photos, sketches, or a designer's drawings with your dimensions and we'll quote it."),
       ("Can you match existing furniture or fabric?", "Yes. We can match a style, size, or fabric so the new piece fits in with what you already have."),
       ("Do you build for businesses as well as homes?", "Yes. We build custom seating for restaurants, hotels, offices, and healthcare spaces as well as residences."),
       ("How long does a custom piece take?", "It depends on the design and material availability. Your written estimate includes the expected timeline.")],
  related=[R_REUP, R_BOOTH, R_DRP]),
 dict(path="/commercial/", crumb="Commercial Upholstery", service="Commercial / contract upholstery",
  title="Commercial Upholstery Miami | Restaurants, Hotels & Healthcare",
  desc="Commercial and contract upholstery in South Florida for restaurants, hotels, hospitals, medical offices, senior living, and universities. Free estimates.",
  h1="Commercial upholstery for South Florida businesses",
  lead="Durable, good-looking seating for spaces that see heavy daily use. We reupholster and fabricate furniture for restaurants, hotels, hospitals, medical offices, retirement communities, and universities.",
  ticks=["Contract-grade fabrics, leather, and vinyl", "Booths, banquettes, lounge seating, and wall panels", "Free on-site estimates"],
  image="reception", image_alt="",
  h2="Seating that holds up and represents your brand",
  body="<p>Worn seating sends the wrong message to guests and patients. We help you refresh existing furniture or build new pieces to fit your space, using materials selected for cleanability and heavy traffic.</p><p>We work with owners, facility managers, designers, and contractors, and can plan around your operating schedule.</p>",
  includes=["Restaurant booths, banquettes, and bar stools", "Hotel lobby and guest-room seating", "Hospital and medical waiting-room furniture", "Senior living and university common areas", "Upholstered wall panels", "Commercial draperies and window treatments"],
  gallery_title="Commercial projects",
  gallery=[("leather", ""), ("hospital", ""), ("lounge", ""), ("barchairs", ""), ("waiting", ""), ("patio", "")],
  faq=[("What types of businesses do you work with?", "Restaurants, hotels, hospitals and medical offices, retirement communities, universities, and offices, along with the designers and contractors who serve them."),
       ("Can you work around our business hours?", "Tell us your schedule when you request an estimate and we'll plan the work to limit disruption."),
       ("Which materials work best for commercial seating?", "It depends on use. We'll recommend contract-grade vinyl, leather, or performance fabrics based on traffic, cleaning needs, and your design."),
       ("Do you handle large or multi-location projects?", "Contact us with the scope and we'll discuss capacity and timing for your project.")],
  related=[R_BOOTH, R_CUST, R_DRP]),
 dict(path="/booths-banquettes/", crumb="Booths & Banquettes", service="Booths & banquettes",
  title="Custom Restaurant Booths & Banquettes Miami | New Life Furniture",
  desc="Custom-built restaurant booths and banquettes plus booth reupholstery in Miami and South Florida. Kiln-dried hardwood frames, any style. Free estimates.",
  h1="Custom booths and banquettes, built to last",
  lead="We design and build booths and banquettes in virtually any style for restaurants, bars, hotels, and homes, and we reupholster existing booths to make them look new again.",
  ticks=["Kiln-dried hardwood frames that resist warping and cracking", "Laminates, veneers, and stains to finish your design", "New builds and booth reupholstery"],
  image="booth2", image_alt="Custom upholstered restaurant booth",
  h2="Made for your space and your guests",
  body="<p>Every booth is built to your measurements and layout: straight runs, corners, curves, and wall banquettes. Frames are made from kiln-dried hardwood for long-term stability in busy dining rooms.</p><p>Already have booths? Reupholstering them is a fast, cost-effective way to refresh a dining room without replacing the whole layout.</p>",
  includes=["Single, double, and corner booths", "Wall banquettes and curved seating", "Channel-tufted, button-tufted, and plain backs", "Commercial-grade vinyl, leather, and fabric", "Laminate, veneer, and stained wood finishes", "Reupholstery of existing booths"],
  gallery_title="Booth and banquette projects",
  gallery=[("booths", ""), ("booth2", ""), ("lounge", ""), ("waiting", ""), ("refin", ""), ("reception", "")],
  faq=[("Do you build new booths or only reupholster?", "Both. We build custom booths and banquettes and reupholster existing ones."),
       ("What are the frames made of?", "We build with kiln-dried hardwoods, which resist warping and cracking."),
       ("Can you match our design or a designer's drawings?", "Yes. Share your drawings, dimensions, or inspiration photos and we'll quote to your specifications."),
       ("Can you reupholster booths without closing the restaurant for long?", "Let us know your schedule and we'll discuss a plan that keeps downtime to a minimum.")],
  related=[R_COM, R_REUP, R_OUT]),
 dict(path="/marine/", crumb="Marine Upholstery", service="Marine upholstery",
  title="Marine Upholstery Miami | Boat & Yacht Seating | New Life Furniture",
  desc="Marine upholstery in Miami and South Florida: boat seats, yacht cushions, and benches in marine-grade vinyl and outdoor fabrics. Request a free estimate.",
  h1="Marine upholstery for boats and yachts",
  lead="Sun, salt, and water are hard on boat seating. We reupholster and fabricate seats, cushions, and benches for boats and yachts using marine-grade materials made for South Florida conditions.",
  ticks=["Marine-grade vinyl and outdoor fabrics", "Helm seats, cockpit cushions, and salon seating", "Free estimates"],
  image="whaler", image_alt="",
  h2="Comfortable, durable seating on the water",
  body="<p>We replace cracked, faded, or waterlogged upholstery with materials chosen to resist UV, mildew, and moisture. Worn foam can be replaced at the same time so seats look good and feel supportive.</p>",
  includes=["Helm and captain's chairs", "Cockpit and bow cushions", "Interior salon and cabin seating", "Benches and sun pads", "Foam replacement", "Matching interior and exterior pieces"],
  gallery_title="Marine projects",
  gallery=[("whaler", ""), ("whaler2", ""), ("whaler3", ""), ("marinechair", ""), ("marine", ""), ("yacht", "")],
  faq=[("What materials do you use for marine upholstery?", "We use marine-grade vinyl and outdoor performance fabrics designed to handle sun, salt, and moisture."),
       ("Can you replace the foam too?", "Yes. Worn or waterlogged foam can be replaced while the cushion is being recovered."),
       ("How do I get an estimate?", "Send photos of the seats or cushions, approximate sizes, and your boat's location using the form, or call us.")],
  related=[R_OUT, R_REUP, R_COM]),
 dict(path="/outdoor-cushions/", crumb="Outdoor Cushions", service="Outdoor cushions",
  title="Custom Outdoor & Patio Cushions Miami | New Life Furniture",
  desc="Custom outdoor and patio cushions made in Miami with performance fabrics such as Sunbrella. Replacement cushions for homes, condos, and hotels. Free estimates.",
  h1="Custom outdoor and patio cushions",
  lead="Replace faded, flattened patio cushions with custom-made ones that fit your furniture exactly, sewn in outdoor performance fabrics that stand up to the Florida sun.",
  ticks=["Made to fit your exact frames", "Performance fabrics such as Sunbrella", "For homes, condos, and hospitality"],
  image="outdoor", image_alt="Custom outdoor cushions on a Miami patio",
  h2="Made to measure, made for the outdoors",
  body="<p>We measure your frames, help you choose an outdoor fabric and fill, and sew cushions that fit properly and look tailored. Pool chaises, sectionals, dining chairs, and daybeds are all welcome.</p>",
  includes=["Seat and back cushions", "Chaise and daybed cushions", "Outdoor sofa and sectional cushions", "Outdoor-rated foam and fill", "Piping, welting, and ties", "Residential and commercial patios"],
  gallery_title="Outdoor projects",
  gallery=[("outdoor", ""), ("outdoor2", ""), ("patio", "")],
  faq=[("Which fabrics do you recommend outdoors?", "Solution-dyed performance fabrics such as Sunbrella resist fading and moisture. We'll help you compare options."),
       ("Can you match my existing cushions?", "Yes. We can use your current cushions as a template or measure your frames for a better fit."),
       ("Do you make cushions for hotels and condos?", "Yes. We handle residential and commercial outdoor seating.")],
  related=[R_MAR, R_REUP, R_DRP]),
 dict(path="/draperies/", crumb="Custom Draperies", service="Draperies & window treatments",
  title="Custom Draperies & Window Treatments Miami | New Life Furniture",
  desc="Custom draperies, blinds, shades, and window treatments for homes and businesses in Miami and South Florida. Fabrication and installation. Free estimates.",
  h1="Custom draperies and window treatments",
  lead="Tailored draperies, shades, and blinds that add privacy, control light, and finish a room, for homes and commercial interiors across South Florida.",
  ticks=["Custom draperies made to measure", "Blinds and shades", "Residential and commercial"],
  image="drapes4", image_alt="",
  h2="Window treatments made for your room",
  body="<p>We help you choose fabric, lining, and style, then fabricate draperies to your window measurements for a clean, finished look. Coordinate with reupholstered furniture for a cohesive room.</p>",
  includes=["Custom draperies and curtains", "Linings for light control and privacy", "Blinds and shades", "Commercial window treatments", "Coordinating fabrics for furniture"],
  gallery_title="Drapery projects",
  gallery=[("drapes4", ""), ("drapes3", ""), ("drapes2", "")],
  faq=[("Do you measure the windows?", "Contact us to arrange measuring. Accurate measurements are key to custom draperies."),
       ("Can draperies coordinate with my upholstery?", "Yes. We can help you select fabrics so draperies and furniture work together."),
       ("Do you work on commercial spaces?", "Yes. We provide window treatments for residential and commercial interiors.")],
  related=[R_REUP, R_COM, R_OUT]),
]

# ---------- pages ----------
MARQ = "".join(f"<span>{t}</span>" for t in ["Reupholstery", "Custom booths", "Banquettes", "Marine upholstery", "Outdoor cushions", "Draperies", "Refinishing", "Leather & vinyl", "Contract seating"])

def home():
    cards = "".join(card(*c) for c in [R_REUP, R_CUST, R_COM, R_BOOTH, R_MAR, R_OUT, R_DRP])
    gal = "".join(f'<figure>{img(g, a, "(min-width: 900px) 25vw, 50vw")}</figure>' for g, a in [
        ("armchair", ""), ("booths", ""), ("yacht", ""), ("reception", ""),
        ("outdoor2", ""), ("whaler", ""), ("diningset", ""), ("drapes2", "")])
    faqs = [("Do you offer free estimates?", "Yes. Send photos through the form or call us and we'll provide a free, no-obligation estimate."),
            ("What areas do you serve?", "We're based in Miami and serve residential and commercial clients across South Florida."),
            ("Do you work with businesses as well as homeowners?", "Yes. We serve homeowners, designers, and contractors, plus restaurants, hotels, hospitals, medical offices, retirement communities, and universities."),
            ("What materials can I choose from?", "Fine fabrics, leather, vinyl, marine-grade materials, and outdoor performance fabrics. We'll help you choose for the way the piece will be used."),
            ("Is reupholstering worth it?", "For well-built furniture you love, usually yes. We'll give you an honest recommendation with your estimate.")]
    body = f'''
<section class="hero">
  <div class="hero-bg">{img("hero", "Living room with chairs reupholstered in blue fabric by New Life Furniture", sizes="100vw", eager=True)}</div>
  <div class="hero-award" aria-hidden="true">{ANGI.format("")}</div>
  <div class="wrap hero-grid"><div class="hero-copy">
    <p class="eyebrow">Miami upholstery workshop · 30+ years</p>
    <h1>Custom upholstery that gives your furniture a <em>new life</em></h1>
    <p class="lead">Reupholstery, custom furniture, booths, marine seating, and draperies for homes and businesses across South Florida, handcrafted in our Miami shop.</p>
    {cta_row(dark=True)}
    <ul class="trust"><li class="trust-angi">{ANGI.format("")}<span><strong>Angi</strong> Super Service Award 2025</span></li><li><strong>30+</strong> years of craftsmanship</li><li><strong>Residential</strong> &amp; commercial</li><li><strong>Free</strong> estimates</li></ul>
  </div>
</div></section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{MARQ}{MARQ}</div></div>
<section class="section paths"><div class="wrap path-grid">
  <a class="path" href="/upholstery-re-upholstery/"><p class="eyebrow">For homeowners</p><h2>Restore the pieces you love</h2><p>Sofas, chairs, heirlooms, outdoor cushions, and draperies.</p><span class="link">Residential services <span aria-hidden="true">→</span></span></a>
  <a class="path dark" href="/commercial/"><p class="eyebrow">For businesses</p><h2>Seating built for heavy use</h2><p>Restaurants, hotels, healthcare, senior living, universities.</p><span class="link">Commercial services <span aria-hidden="true">→</span></span></a>
</div></section>
<section class="section"><div class="wrap"><p class="eyebrow">What we do</p><h2>Upholstery and fabrication services</h2><div class="bento">{cards}</div></div></section>
<section class="section dark"><div class="wrap"><div class="row-head"><div><p class="eyebrow">Our work</p><h2>Recent projects</h2></div>{car_ctrl("home-gal", "photo", light=True)}</div><div class="car" data-car><div class="mosaic car-track" id="home-gal">{gal}</div></div><p class="center"><a class="link light" href="/projects/">View all projects <span aria-hidden="true">→</span></a></p></div></section>
<section class="section"><div class="wrap split">
  <div class="split-img">{img("team", "")}</div>
  <div><p class="eyebrow">About New Life Furniture</p><h2>Three decades of handcrafted upholstery</h2>
  <p>New Life Furniture Mfg. specializes in custom upholstered furniture, reupholstery, and fabrication for residences and businesses across South Florida. For more than 30 years our team has delivered handcrafted quality with fine fabrics, leather, vinyl, and marine materials.</p>
  <p>Clients work directly with Ian and the team, from the first conversation and fabric selection to the finished piece.</p>
  <a class="link" href="/about/">More about us <span aria-hidden="true">→</span></a></div>
</div></section>
{process()}
{testimonials()}
<section class="section"><div class="wrap narrow"><p class="eyebrow">FAQ</p><h2>Questions we hear often</h2>{faq(faqs)}</div></section>
{final_cta()}'''
    return page("/", "Furniture Reupholstery & Custom Upholstery Miami | New Life Furniture",
                "Miami upholstery workshop, 30+ years. Furniture reupholstery, custom booths, marine upholstery, outdoor cushions, and draperies. Free estimates.",
                body, None, [faq_schema(faqs)], preload="hero", preload_sizes="100vw")

def projects():
    groups = [("Residential", [(n, ALT[n]) for n in ["diningset", "armchair", "diningchair", "sofa", "reup", "dining", "team", "sectional"]]),
              ("Commercial & hospitality", [(n, ALT[n]) for n in ["tufted", "booths", "booth2", "lounge", "reception", "poufs", "leather", "waiting"]]),
              ("Marine", [(n, ALT[n]) for n in ["whaler", "whaler2", "whaler3", "marinechair", "marinechair2", "marine", "yacht", "marine2"]]),
              ("Outdoor, draperies & refinishing", [(n, ALT[n]) for n in ["drapes4", "drapes3", "outdoor", "outdoor2", "patio", "barchairs", "drapes2", "refindining"]])]
    secs = "".join(f'<section class="section{" sand" if i % 2 else ""}"><div class="wrap"><h2>{t}</h2><div class="gallery g4">' +
                   "".join(f'<figure>{img(n, a, "(min-width: 900px) 25vw, 50vw")}<figcaption>{a}</figcaption></figure>' for n, a in g) + '</div></div></section>'
                   for i, (t, g) in enumerate(groups))
    body = f'''<section class="page-hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>Projects</span></nav>
<h1>Our projects</h1><p class="lead">A selection of residential, commercial, marine, and drapery work by New Life Furniture across South Florida.</p>{cta_row()}</div></section>{secs}{final_cta("Have a project like these?")}'''
    return page("/projects/", "Upholstery Projects & Gallery | New Life Furniture Miami",
                "See reupholstery, custom booth, commercial, marine, outdoor cushion, and drapery projects completed by New Life Furniture in South Florida.", body, "Projects")

def about():
    body = f'''<section class="page-hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>About</span></nav>
<h1>About New Life Furniture</h1><p class="lead">A Miami upholstery and fabrication workshop serving homes and businesses across South Florida for more than 30 years.</p></div></section>
<section class="section"><div class="wrap split"><div class="split-img">{img("about", "")}</div><div>
<h2>Craftsmanship you can see and feel</h2>
<p>At New Life Furniture Mfg., we specialize in custom upholstered furniture, reupholstery, and fabrication. Our team combines decades of hands-on experience with quality materials to create pieces tailored to each client's vision.</p>
<p>Our work spans custom upholstered furniture, reupholstery, fine fabrics, leather, vinyl, marine upholstery, and window treatments including blinds, shades, and custom draperies. We handle both contract work and fine residential projects.</p>
<p>We proudly serve restaurants, hotels, hospitals, medical offices, retirement communities, and universities, along with homeowners, designers, and contractors.</p>
{cta_row()}</div></div></section>
{process()}{testimonials()}{final_cta()}'''
    return page("/about/", "About Us | New Life Furniture Mfg. Miami Upholstery",
                "New Life Furniture Mfg. is a Miami upholstery and fabrication workshop with more than 30 years of experience serving South Florida homes and businesses.", body, "About")

def contact():
    body = f'''<section class="lp-hero"><div class="wrap lp-grid"><div class="lp-copy">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>Contact</span></nav>
<h1>Request a free estimate</h1>
<p class="lead">Tell us about your furniture or project. Photos help us give you a faster, more accurate estimate. You can also text or email them after you submit.</p>
<ul class="contact-list big"><li><span>Call</span><a href="tel:{BIZ["tel"]}" data-ev="contact">{BIZ["phone"]}</a></li><li><span>Alt. phone</span><a href="tel:{BIZ["tel2"]}" data-ev="contact">{BIZ["phone2"]}</a></li>
<li><span>Email</span><a href="mailto:{BIZ["email"]}" data-ev="contact">{BIZ["email"]}</a></li><li><span>Workshop</span>{BIZ["street"]}<br>{BIZ["city"]}, {BIZ["region"]} {BIZ["zip"]}</li></ul>
<p class="fine">Serving homes and businesses across South Florida.</p></div>
<div class="lp-form">{form()}</div></div></section>
<section class="section sand"><div class="wrap narrow">{faq([("What should I include in my request?", "The type of piece or project, approximate size or quantity, the material you have in mind, and your city. Photos are very helpful."), ("How quickly will you respond?", "We review every request and reply as soon as possible, usually by phone or email."), ("Is the estimate really free?", "Yes. Estimates are free and there's no obligation.")])}</div></section>'''
    return page("/contact-new-life-furniture-miami/", "Contact & Free Estimate | New Life Furniture Miami",
                f"Request a free upholstery estimate from New Life Furniture in Miami. Call {BIZ['phone']} or send photos and project details online.", body, "Contact")

def notfound():
    body = f'<section class="page-hero"><div class="wrap narrow"><h1>Page not found</h1><p class="lead">The page you are looking for has moved. Try one of our services below or request an estimate.</p>{cta_row()}<div class="cards" style="margin-top:3rem">{"".join(card(*c) for c in [R_REUP, R_COM, R_MAR])}</div></div></section>'
    return page("/404.html", "Page not found | New Life Furniture", "Page not found.", body, noindex=True)

BASE = os.environ.get("BASE", "")  # preview build under a sub-path, e.g. BASE=/new-life-furniture (noindex, no GTM)

def write(path, content):
    if BASE:
        content = content.replace('="/', f'="{BASE}/').replace(' /img/', f' {BASE}/img/').replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1)
        content = content.replace(f"'{GTM_ID}'", "''").replace(f'id={GTM_ID}', 'id=')
    out = ROOT / (path.strip("/") or ".") / "index.html" if not path.endswith(".html") else ROOT / path.strip("/")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(content)

if __name__ == "__main__":
    pages = {"/": home(), "/projects/": projects(), "/about/": about(), "/contact-new-life-furniture-miami/": contact(), "/404.html": notfound()}
    for s in SERVICES: pages[s["path"]] = service_page(s)
    for p, c in pages.items(): write(p, c)
    urls = [p for p in pages if p != "/404.html"]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", len(pages), "pages")
