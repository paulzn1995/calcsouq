# Usage: python3 build.py OUTDIR [SITE_URL] [ADSENSE_CLIENT] [SEARCH_CONSOLE_CODE]
import os, sys, shutil, html, datetime, json
sys.path.insert(0, os.path.dirname(__file__))
from base import CSS, JS, head, foot, ad, faq_ld, crumbs_ld, app_ld, article_ld, share_bar, feedback, ICONS, SITE_NAME, TAGLINE
from articles import ARTICLES
import base
from tools_unique import TOOLS

out = sys.argv[1]
_conf = json.load(open(os.path.join(os.path.dirname(__file__), "config.json")))
cfg = {"url": sys.argv[2] if len(sys.argv) > 2 else _conf["url"],
       "adsense": sys.argv[3] if len(sys.argv) > 3 else _conf.get("adsense", ""),
       "gsc": sys.argv[4] if len(sys.argv) > 4 else _conf.get("gsc", "")}
if len(sys.argv) <= 5 and _conf.get("slot"):
    sys.argv[5:] = [_conf["slot"]]
base.AD["client"] = cfg["adsense"]
base.AD["slot"] = sys.argv[5] if len(sys.argv) > 5 else ""
host = cfg["url"].split("//")[1].split("/")[0].removeprefix("www.")
EMAIL = "contact@" + host
today = datetime.date.today()
GROUPS = [("uae", "UAE work & money"), ("trading", "Trading"), ("india", "India, Kerala & NRI")]
SRC = {"uae-gratuity-calculator": [("UAE Ministry of Human Resources & Emiratisation (MOHRE)", "https://www.mohre.gov.ae")], "uae-leave-encashment-calculator": [("UAE Government portal: annual leave", "https://u.ae/en/information-and-services/jobs/employment-in-the-private-sector/types-of-leaves-and-entitlements-in-the-private-sector/annual-leave")], "uae-vat-calculator": [("UAE Federal Tax Authority", "https://tax.gov.ae")], "gold-price-calculator": [("UAE Federal Tax Authority", "https://tax.gov.ae")], "kerala-stamp-duty-calculator": [("Kerala Registration Department", "https://keralaregistration.gov.in")], "futures-tick-value-calculator": [("CME Group contract specifications", "https://www.cmegroup.com")]}

if os.path.exists(out):
    shutil.rmtree(out)
os.makedirs(out + "/assets")
w = lambda p, s: (os.makedirs(os.path.dirname(os.path.join(out, p)), exist_ok=True), open(os.path.join(out, p), "w").write(s))
w("assets/site.css", CSS)
w("assets/site.js", JS)
w("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#f5c300"/><text x="32" y="45" font-family="Arial,Helvetica,sans-serif" font-size="38" font-weight="800" fill="#15171a" text-anchor="middle">C</text></svg>')
paths = []

def ic(t):
    return ICONS.get(t.get("icon") or ("gold" if "gold" in t["slug"] else t["group"]), ICONS["money"])

def card(t):
    tag = '<em class="tag">New</em>' if t.get("unique") else ""
    return f'<a class="card" href="/{t["slug"]}/"><div class="ic">{ic(t)}</div><div><b>{t["name"]}{tag}</b><span>{t["card"]}</span></div></a>'

def related(t):
    same = [x for x in TOOLS if x["group"] == t["group"] and x is not t]
    other = [x for x in TOOLS if x["group"] != t["group"]][:2]
    return '<section class="related"><h2>Related calculators</h2><div class="grid">' + "".join(card(x) for x in (same + other)[:6]) + "</div></section>"

for t in TOOLS:
    p = f"/{t['slug']}/"
    paths.append((p, "weekly", "0.9"))
    faqs = t["faqs"]
    page = head(cfg, t["title"], t["desc"], p, t["keywords"], [app_ld(cfg, t["name"], t["desc"], p), crumbs_ld(cfg, t["name"], p), faq_ld(faqs)])
    srcs = t.get("sources") or SRC.get(t["slug"], [])
    grp = dict(GROUPS)[t["group"]]
    page += f'<main class="wrap"><div class="crumbs"><a href="/">Home</a> › <a href="/#{t["group"]}">{grp}</a></div>\n<h1>{t["h1"]}</h1><p class="lede">{t["lede"]}</p>\n'
    page += f'<div class="meta"><span>Updated {today:%d %b %Y}</span><span>Free, no sign-up</span>' + ('<a href="#sources">Sources</a>' if srcs else '<a href="#how">How it works</a>') + '</div>\n'
    page += f'<section class="tool" aria-label="{html.escape(t["name"])}">{t["tool"]}</section>\n' + (share_bar() if t["slug"] != "market-hours" else "") + f'\n{ad()}\n'
    sb = ('<div class="sources" id="sources"><b>Sources</b><ul>' + "".join(f'<li><a href="{u}" rel="noopener">{n}</a></li>' for n, u in srcs) + '</ul></div>') if srcs else ""
    page += f'<article id="how">{t["body"]}{sb}{feedback()}</article>\n{ad()}\n'
    page += '<section class="faq"><h2>Frequently asked questions</h2>' + "".join(
        f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faqs) + "</section>\n"
    gl = [a for a in ARTICLES if a["tool"] == t["slug"]]
    if gl:
        page += '<section class="related"><h2>Guides</h2><ul>' + "".join(f'<li><a href="/guides/{a["slug"]}/">{a["h1"]}</a></li>' for a in gl) + "</ul></section>"
    page += related(t) + "</main>\n"
    page += foot("<script>\n{" + t["js"] + "}\n</script>")
    w(p.strip("/") + "/index.html", page)

# Home
hd = "Free calculators for life in the UAE and back home in India: final settlement, gratuity, gold, EMI, remittances, trading risk and Kerala property costs."
ld_site = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": cfg["url"].rstrip("/") + "/", "description": hd}
home = head(cfg, f"{SITE_NAME}: UAE & India Calculators (Gratuity, Final Settlement, Gold, EMI, Trading)", hd, "/",
            "uae calculators, final settlement calculator uae, gratuity calculator, gold tola calculator, emi calculator uae, aed to inr, lot size calculator, kerala land cost calculator", [ld_site])
home += '<main class="wrap"><section class="hero"><h1>Calculators for working in the UAE and planning back home</h1>'
home += '<p class="lede">Settlement and gratuity, gold, loans, remittances, trading risk and Kerala property, with the rules explained and sources linked.</p>'
home += base.SEARCH.replace('placeholder="Search calculators and guides"', 'placeholder="What do you want to calculate? e.g. gratuity, gold tola, EMI"')
home += '<div class="chips">' + "".join(f'<a href="/{x}/">{n}</a>' for n, x in [("Final settlement", "uae-final-settlement-calculator"), ("Gratuity", "uae-gratuity-calculator"), ("Gold price", "gold-price-calculator"), ("AED to INR", "aed-to-inr-calculator"), ("Lot size", "position-size-calculator"), ("Cent to sq ft", "kerala-land-converter")]) + '</div></section>'
home += '<div class="install card" style="margin:22px 0 0;align-items:center;flex-wrap:wrap"><div class="ic">' + ICONS["money"] + '</div><div style="flex:1 1 200px"><b>Add CalcSouq to your home screen</b><span>Open any calculator in one tap.</span><span class="ios" hidden> On iPhone: tap Share, then Add to Home Screen.</span></div><button type="button" class="btn primary">Install</button></div>'
uq = [t for t in TOOLS if t.get("unique")]
home += '<h2 class="group-title" id="calculators">Only on CalcSouq</h2><p class="lede" style="font-size:15px;margin-top:-6px">Tools that combine several calculations you\'d otherwise do separately.</p><div class="grid">' + "".join(card(t) for t in uq) + '</div>'
for g, gt in GROUPS:
    home += f'<h2 id="{g}" class="group-title">{gt}</h2><div class="grid">' + "".join(card(t) for t in TOOLS if t["group"] == g and not t.get("unique")) + "</div>"
    if g == "uae": home += ad()
home += '<h2 id="guides" class="group-title">Popular guides</h2><div class="grid">' + "".join(f'<a class="card" href="/guides/{a["slug"]}/"><div class="ic">{ICONS["guide"]}</div><div><b>{a["h1"]}</b></div></a>' for a in ARTICLES[:9]) + '</div><p><a href="/guides/">All guides →</a></p>'
home += ad() + "</main>" + foot()
w("index.html", home)
paths.insert(0, ("/", "daily", "1.0"))

# Guides
TOOLS_BY = {t["slug"]: t for t in TOOLS}
for a in ARTICLES:
    p = f"/guides/{a['slug']}/"; paths.append((p, "monthly", "0.7"))
    t = TOOLS_BY[a["tool"]]
    pg = head(cfg, a["title"], a["desc"], p, a["keywords"], [article_ld(cfg, a["title"], a["desc"], p, str(today)), crumbs_ld(cfg, a["h1"], p), faq_ld(a["faqs"])])
    pg += f'<main class="wrap"><div class="crumbs"><a href="/">Home</a> › <a href="/guides/">Guides</a></div><article style="padding-top:8px"><h1>{a["h1"]}</h1><p class="lede">{a["lede"]}</p>'
    pg += f'<p class="meta"><span>Updated {today:%d %b %Y}</span></p><a class="card" href="/{t["slug"]}/" style="margin:4px 0 22px"><div class="ic">{ic(t)}</div><div><b>Use the {t["name"]} →</b><span>{t["card"]}</span></div></a>'
    pg += a["body"] + ad() + '<section class="faq"><h2>Frequently asked questions</h2>' + "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(x)}</p></details>" for q, x in a["faqs"]) + "</section>"
    pg += f'<p class="hint">Updated {today:%d %B %Y}. General information only, not legal, tax or investment advice.</p></article>'
    more = [b for b in ARTICLES if b["group"] == a["group"] and b is not a][:4]
    pg += '<section class="related"><h2>More guides</h2><div class="grid">' + "".join(f'<a class="card" href="/guides/{b["slug"]}/"><b>{b["h1"]}</b></a>' for b in more) + "</div></section></main>" + foot()
    w(p.strip("/") + "/index.html", pg)
gi = head(cfg, f"Guides: UAE Gratuity, VAT, Gold, Forex Trading & Kerala Property · {SITE_NAME}", "Plain-English guides for expats and traders in the UAE and India: gratuity, VAT, gold, remittances, forex risk, futures and Kerala land.", "/guides/", "uae guides, gratuity guide, forex guide, kerala land guide", [])
gi += '<main class="wrap"><section style="padding:36px 0 8px"><h1>Guides</h1><p class="lede">Short, exact answers to the questions behind our calculators.</p></section>'
for g, gt in GROUPS:
    gi += f'<h2 class="group-title">{gt}</h2><div class="grid">' + "".join(f'<a class="card" href="/guides/{a["slug"]}/"><div class="ic">{ICONS["guide"]}</div><div><b>{a["h1"]}</b><span>{a["lede"][:110]}</span></div></a>' for a in ARTICLES if a["group"] == g) + "</div>"
gi += ad() + "</main>" + foot()
w("guides/index.html", gi); paths.append(("/guides/", "weekly", "0.8"))

# Info pages
INFO = {
"about": ("About " + SITE_NAME, f"""<p>{SITE_NAME} is a free collection of calculators for people who live, work and invest between the UAE and India: end-of-service gratuity, VAT, gold jewellery prices, remittances, trading risk and Kerala property.</p>
<h2>How we build the tools</h2><p>Each calculator follows the published rule it is based on, such as the UAE Labour Law for gratuity, the FTA for VAT, or exchange contract specifications for futures, and shows the formula and a worked example so you can check the result yourself. Pages are reviewed when rules change.</p>
<h2>Who runs the site</h2><p>{SITE_NAME} is run by a dealing and operations professional with several years' experience across forex, CFDs, futures and equities at a regulated broker in Dubai.</p>
<h2>Independence</h2><p>The site is funded by advertising and is not affiliated with any bank, exchange house, broker or government body.</p>"""),
"privacy": ("Privacy policy", f"""<p>This policy explains what information {SITE_NAME} collects when you visit the site and how it is used.</p>
<h2>Information we collect</h2><p>You do not need an account. The numbers you type into calculators are processed in your browser and are not sent to us; some are remembered in your own browser's storage so the page reopens where you left it. Our hosting provider keeps standard server logs (IP address, browser type, pages visited, time of visit) for security and performance.</p>
<h2>Cookies and advertising</h2><p>We use Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on your previous visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this site and other sites on the internet.</p>
<p>You can opt out of personalised advertising in <a href="https://adssettings.google.com">Google Ads Settings</a>, or opt out of some third-party vendors' cookies at <a href="https://www.aboutads.info/choices/">aboutads.info</a>. See also <a href="https://policies.google.com/technologies/partner-sites">how Google uses information from sites that use its services</a>.</p>
<p>Visitors in the EEA, UK and Switzerland are shown a consent message before personalised ads or cookies are used.</p>
<h2>Children</h2><p>The site is not directed at children under 13 and we do not knowingly collect their information.</p>
<h2>Contact</h2><p>Questions about this policy: <a href="mailto:{EMAIL}">{EMAIL}</a> ({EMAIL}).</p>"""),
"terms": ("Terms of use", """<p>By using this site you agree to these terms.</p>
<h2>Information only</h2><p>Calculator results are estimates for general information. They are not legal, tax, financial or investment advice. Rules, rates and contract specifications change; confirm important figures with your employer, the relevant authority, your bank or your broker. Trading leveraged products carries a high risk of loss.</p>
<h2>No warranty</h2><p>We aim for accuracy but make no warranty that results are correct, complete or current, and we are not liable for any loss arising from their use.</p>
<h2>Market data</h2><p>Any market prices shown are delayed and licensed for display only. You may not copy, scrape, store or redistribute them.</p>
<h2>Changes</h2><p>We may update these terms at any time. Continued use of the site means you accept the current version.</p>"""),
"contact": ("Contact", f"""<p>For corrections, suggestions for new calculators or advertising enquiries, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p><p class="hint">Email address: {EMAIL}</p><p>We usually reply within two working days.</p>"""),
}
for k, (t, b) in INFO.items():
    p = f"/{k}/"; paths.append((p, "yearly", "0.3"))
    w(k + "/index.html", head(cfg, f"{t} · {SITE_NAME}", f"{t} for {SITE_NAME}, free calculators for the UAE and India.", p, "", [])
      + f'<main class="wrap"><article style="padding-top:36px"><h1>{t}</h1><p class="hint">Last updated {today:%d %B %Y}</p>{b}</article></main>' + foot())

# PWA
w("manifest.webmanifest", json.dumps({"name": "CalcSouq: calculators for UAE & India", "short_name": "CalcSouq", "start_url": "/", "scope": "/", "display": "standalone",
    "background_color": "#f6f6f4", "theme_color": "#f5c300", "description": "Free UAE, trading and Kerala calculators.",
    "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
              {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, indent=1))
w("sw.js", """// CalcSouq service worker: pages network-first, assets cache-first, offline fallback to cache.
const C = 'calcsouq-""" + base.VER + """';
self.addEventListener('install', e => { self.skipWaiting(); e.waitUntil(caches.open(C).then(c => c.addAll(['/', '/assets/site.css?v=""" + base.VER + """', '/assets/site.js?v=""" + base.VER + """']))); });
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin || u.pathname.startsWith('/api/')) return;
  if (u.pathname.startsWith('/assets/') || /\\.(png|svg|webmanifest)$/.test(u.pathname)) {
    e.respondWith(caches.match(r).then(m => m || fetch(r).then(res => { const cp = res.clone(); caches.open(C).then(c => c.put(r, cp)); return res; })));
  } else if (r.mode === 'navigate') {
    e.respondWith(fetch(r).then(res => { const cp = res.clone(); caches.open(C).then(c => c.put(r, cp)); return res; }).catch(() => caches.match(r).then(m => m || caches.match('/'))));
  }
});
""")
from PIL import Image, ImageDraw, ImageFont
for sz in (192, 512):
    im = Image.new("RGB", (sz, sz), "#f5c300"); d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(sz * .58))
    bb = d.textbbox((0, 0), "C", font=f); d.text(((sz - bb[2] - bb[0]) / 2, (sz - bb[3] - bb[1]) / 2), "C", font=f, fill="#111111")
    im.save(os.path.join(out, f"icon-{sz}.png"))

# Search index
idx = [{"t": t["name"], "u": f"/{t['slug']}/", "c": "Calculator", "d": t["card"], "k": t["keywords"]} for t in TOOLS]
idx += [{"t": a["h1"], "u": f"/guides/{a['slug']}/", "c": "Guide", "d": a["lede"][:90], "k": a["keywords"]} for a in ARTICLES]
w("search-index.json", json.dumps(idx, ensure_ascii=False))

# SEO files
u = cfg["url"].rstrip("/")
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"<url><loc>{u}{p}</loc><lastmod>{today}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n" for p, c, pr in paths) + "</urlset>\n")
w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: {u}/sitemap.xml\n")
pub = cfg["adsense"].removeprefix("ca-") if cfg["adsense"] else "pub-XXXXXXXXXXXXXXXX"
w("ads.txt", f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
w("vercel.json", '{\n  "trailingSlash": true,\n  "redirects": [{ "source": "/gift-nifty", "destination": "/", "permanent": true }, { "source": "/gift-nifty/:path*", "destination": "/", "permanent": true }],\n  "headers": [{ "source": "/assets/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=86400" }] }]\n}\n')
w("package.json", '{ "name": "calcsouq", "private": true, "engines": { "node": ">=18" } }\n')
w("404.html", head(cfg, "Page not found · " + SITE_NAME, "Page not found", "/404.html", "", []) + '<main class="wrap"><article style="padding-top:36px"><h1>Page not found</h1><p><a href="/">See all calculators</a></p></article></main>' + foot())
print(len(paths), "pages")
