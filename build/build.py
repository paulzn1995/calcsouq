# Usage: python3 build.py OUTDIR [SITE_URL] [ADSENSE_CLIENT] [SEARCH_CONSOLE_CODE]
import os, sys, shutil, html, datetime, json
sys.path.insert(0, os.path.dirname(__file__))
from base import CSS, JS, head, foot, ad, faq_ld, crumbs_ld, app_ld, article_ld, share_bar, feedback, ICONS, SITE_NAME, TAGLINE
from articles import ARTICLES
import base
from tools_margin import TOOLS
from ml import ML, COMMON

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
GROUPS = [("everyday", "Everyday calculators"), ("docs", "Photos & documents"), ("uae", "Money, tax & salary"), ("trading", "Trading & investing"), ("india", "Property & land")]
SRC = {"uae-gratuity-calculator": [("UAE Ministry of Human Resources & Emiratisation (MOHRE)", "https://www.mohre.gov.ae")], "uae-leave-encashment-calculator": [("UAE Government portal: annual leave", "https://u.ae/en/information-and-services/jobs/employment-in-the-private-sector/types-of-leaves-and-entitlements-in-the-private-sector/annual-leave")], "uae-vat-calculator": [("UAE Federal Tax Authority", "https://tax.gov.ae")], "gold-price-calculator": [("UAE Federal Tax Authority", "https://tax.gov.ae")], "kerala-stamp-duty-calculator": [("Kerala Registration Department", "https://keralaregistration.gov.in")], "futures-tick-value-calculator": [("CME Group contract specifications", "https://www.cmegroup.com")]}

if os.path.exists(out):
    shutil.rmtree(out)
os.makedirs(out + "/assets")
w = lambda p, s: (os.makedirs(os.path.dirname(os.path.join(out, p)), exist_ok=True), open(os.path.join(out, p), "w").write(s))
w("assets/site.css", CSS)
_static = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(_static):
    shutil.copytree(_static, out, dirs_exist_ok=True)  # e.g. build/static/media/ig/*.mp4 -> site/media/ig/
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

# Translated pages (hi, zh, ru, ml)
from i18n import LANGS, ORDER as LORDER
TOOLS_ALL = {t["slug"]: t for t in TOOLS}
def tr(s, reps):
    for a, b in sorted(reps, key=lambda r: -len(r[0])):
        s = s.replace(a, b)
    return s
def lang_alts(slug):
    a = [("en", f"/{slug}/")] + [(c, f"/{c}/{slug}/") for c in LORDER if slug in LANGS[c]["tools"]]
    return a + [("x-default", f"/{slug}/")] if len(a) > 1 else None
HOME_ALTS = [("en", "/")] + [(c, f"/{c}/") for c in LORDER] + [("x-default", "/")]
def lcard(code, slug):
    m, t = LANGS[code]["tools"][slug], TOOLS_ALL[slug]
    return f'<a class="card" href="/{code}/{slug}/"><div class="ic">{ic(t)}</div><div><b>{m["name"]}</b><span>{m["card"]}</span></div></a>'
def lang_switch(cur, slug=None):
    out = []
    for c in ["en"] + LORDER:
        if c == cur: continue
        if c == "en": out.append(f'<a href="/{slug + "/" if slug else ""}" lang="en">English</a>')
        elif slug is None or slug in LANGS[c]["tools"]:
            out.append(f'<a href="/{c}/{slug + "/" if slug else ""}" lang="{c}">{LANGS[c]["native"]}</a>')
    return out
for t in TOOLS:
    p = f"/{t['slug']}/"
    paths.append((p, "weekly", "0.9"))
    faqs = t["faqs"]
    alts = lang_alts(t["slug"])
    page = head(cfg, t["title"], t["desc"], p, t["keywords"], [app_ld(cfg, t["name"], t["desc"], p), crumbs_ld(cfg, t["name"], p), faq_ld(faqs)], alts=alts)
    srcs = t.get("sources") or SRC.get(t["slug"], [])
    grp = dict(GROUPS)[t["group"]]
    page += f'<main class="wrap"><div class="crumbs"><a href="/">Home</a> › <a href="/#{t["group"]}">{grp}</a></div>\n<h1>{t["h1"]}</h1><p class="lede">{t["lede"]}</p>\n'
    page += f'<div class="meta"><span>Updated {today:%d %b %Y}</span><span>Free, no sign-up</span>' + "".join(lang_switch("en", t["slug"])) if alts else "" + ('<a href="#sources">Sources</a>' if srcs else '<a href="#how">How it works</a>') + '</div>\n'
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


for code in LORDER:
    L = LANGS[code]; T = L["tools"]
    for slug, m in T.items():
        t = TOOLS_ALL[slug]
        for a, _ in m["rep"]:
            if a not in t["tool"] + t["js"]: print(f"  {code} miss:", slug, repr(a[:60]))
        p = f"/{code}/{slug}/"; paths.append((p, "weekly", "0.8"))
        page = head(cfg, m["title"], m["desc"], p, m["keywords"], [app_ld(cfg, m["name"], m["desc"], p), crumbs_ld(cfg, m["name"], p), faq_ld(m["faqs"])], lang=code, alts=lang_alts(slug))
        page += f'<main class="wrap"><div class="crumbs"><a href="/{code}/">{L["native"]}</a> › {m["name"]}</div>\n<h1>{m["h1"]}</h1><p class="lede">{m["lede"]}</p>\n'
        page += f'<div class="meta"><span>{L["updated"]} {today:%d.%m.%Y}</span><span>Free, no sign-up</span>' + "".join(lang_switch(code, slug)) + '</div>\n'
        page += f'<section class="tool" aria-label="{html.escape(m["name"])}">{tr(t["tool"], m["rep"])}</section>\n' + share_bar() + f'\n{ad()}\n'
        srcs = t.get("sources") or SRC.get(slug, [])
        sb = ('<div class="sources" id="sources"><b>Sources</b><ul>' + "".join(f'<li><a href="{u}" rel="noopener">{n}</a></li>' for n, u in srcs) + '</ul></div>') if srcs else ""
        page += f'<article id="how">{m["body"]}{sb}{feedback()}</article>\n{ad()}\n'
        page += '<section class="faq"><h2>Frequently asked questions</h2>' + "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in m["faqs"]) + "</section>\n"
        page += '<section class="related"><h2>Related calculators</h2><div class="grid">' + "".join(lcard(code, x) for x in T if x != slug) + "</div></section></main>\n"
        page += foot("<script>\n{" + tr(t["js"], m["rep"]) + "}\n</script>")
        page = tr(page, L["common_rep"])
        w(p.strip("/") + "/index.html", page)
    mh = head(cfg, L["home_title"], L["home_desc"], f"/{code}/", L["home_kw"], [], lang=code, alts=HOME_ALTS)
    mh += f'<main class="wrap"><section class="hero split"><div class="hero-txt"><h1>{L["home_h1"]}</h1><p class="lede">{L["home_lede"]}</p><div class="langrow">' + base.GLOBE + "".join(f'<a href="{"/" if c == "en" else "/" + c + "/"}" lang="{c}">{n}</a>' for c, n, _ in base.LANG_UI if c != code) + '</div></div>' + base.HERO_ART + '</section>'
    mh += '<div class="grid" style="margin-top:22px">' + "".join(lcard(code, x) for x in T) + '</div>' + ad()
    mh += f'<p class="hint" style="margin-top:22px">{L["english_more"]} <a href="/" lang="en">CalcSouq (English)</a> · ' + " · ".join(lang_switch(code)[1:]) + '</p></main>' + foot()
    mh = tr(mh, L["common_rep"])
    w(f"{code}/index.html", mh); paths.append((f"/{code}/", "weekly", "0.8"))
LANG_BAR = " · ".join(f'<a href="/{c}/" lang="{c}">{LANGS[c]["native"]}</a>' for c in LORDER)
LANGROW = '<div class="langrow">' + base.GLOBE + '<span>Also in your language:</span>' + "".join(f'<a href="/{c}/" lang="{c}" hreflang="{c}">{LANGS[c]["native"]}</a>' for c in LORDER) + '</div>'

# Home
hd = "Free online calculators and tools: photo resizer, loan EMI, gold price, currency, salary and end-of-service pay, trading risk and property costs. Formulas explained, sources linked, no sign-up."
ld_site = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": cfg["url"].rstrip("/") + "/", "description": hd}
home = head(cfg, f"{SITE_NAME}: Free Online Calculators & Tools (Photo Resizer, EMI, Gold, Gratuity, Trading)", hd, "/",
            "free online calculators, photo resizer, resize photo to kb, emi calculator, gold price calculator, gratuity calculator, final settlement calculator, position size calculator, currency calculator, land area converter", [ld_site], alts=HOME_ALTS)
home += '<main class="wrap"><section class="hero split"><div class="hero-txt"><h1>Free calculators and tools for <em>money, work and everyday forms</em></h1>'
home += '<p class="lede">Resize photos for applications, plan loans and savings, price gold, check salary and end-of-service pay, size trades and cost a property. Each tool shows its formula and sources, and works without sign-up.</p>'
home += base.SEARCH.replace('placeholder="Search calculators and guides"', 'placeholder="What do you want to calculate? e.g. resize photo, EMI, gold, gratuity"')
home += '<div class="chips">' + "".join(f'<a href="/{x}/">{n}</a>' for n, x in [("Photo resizer", "photo-resizer"), ("JPG to PDF", "image-to-pdf"), ("Age", "age-calculator"), ("Percentage", "percentage-calculator"), ("SIP", "sip-calculator"), ("GST", "gst-calculator"), ("Loan EMI", "loan-emi-calculator"), ("Gold price", "gold-price-calculator")]) + '</div>' + LANGROW + '</div>' + base.HERO_ART + '</section>'
home += '<div class="install card" style="margin:22px 0 0;align-items:center;flex-wrap:wrap"><div class="ic">' + ICONS["money"] + '</div><div style="flex:1 1 200px"><b>Add CalcSouq to your home screen</b><span>Open any calculator in one tap.</span><span class="ios" hidden> On iPhone: tap Share, then Add to Home Screen.</span></div><button type="button" class="btn primary">Install</button></div>'
_ord = ["trading-strategy-simulator", "gulf-savings-return-planner", "uae-final-settlement-calculator", "property-buying-cost-calculator"]
uq = sorted([t for t in TOOLS if t.get("unique")], key=lambda t: _ord.index(t["slug"]) if t["slug"] in _ord else 99)
home += '<h2 class="group-title" id="calculators">Only on CalcSouq</h2><p class="lede" style="font-size:15px;margin-top:-6px">Tools that combine several calculations you\'d otherwise do separately.</p><div class="grid">' + "".join(card(t) for t in uq) + '</div>'
for g, gt in GROUPS:
    home += f'<h2 id="{g}" class="group-title">{gt}</h2><div class="grid">' + "".join(card(t) for t in TOOLS if t["group"] == g and not t.get("unique")) + "</div>"
    if g == "docs": home += ad()
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
gi = head(cfg, f"Guides: Gratuity, VAT, Gold, Forex Trading & Property · {SITE_NAME}", "Plain-English guides behind our calculators: salary and gratuity, VAT, gold, currency transfers, forex and futures risk, and land measurement.", "/guides/", "uae guides, gratuity guide, forex guide, kerala land guide", [])
gi += '<main class="wrap"><section style="padding:36px 0 8px"><h1>Guides</h1><p class="lede">Short, exact answers to the questions behind our calculators.</p></section>'
for g, gt in GROUPS:
    if not any(a["group"] == g for a in ARTICLES): continue
    gi += f'<h2 class="group-title">{gt}</h2><div class="grid">' + "".join(f'<a class="card" href="/guides/{a["slug"]}/"><div class="ic">{ICONS["guide"]}</div><div><b>{a["h1"]}</b><span>{a["lede"][:110]}</span></div></a>' for a in ARTICLES if a["group"] == g) + "</div>"
gi += ad() + "</main>" + foot()
w("guides/index.html", gi); paths.append(("/guides/", "weekly", "0.8"))


# Templates (paid spreadsheets; links come from config.json "gumroad")
GR = _conf.get("gumroad", {})
TPL = [("settlement", "UAE Final Settlement Workbook (Excel)", "uae-final-settlement-calculator",
        "The same calculation as our final settlement calculator, in a spreadsheet you keep: inputs sheet, line-by-line statement, and a leave log that totals unpaid leave for you.",
        ["Gratuity under Article 51 with the 2-year cap", "Unused leave, unpaid salary and notice in or out", "Leave log with dropdowns", "Works in Excel, Google Sheets and Numbers"]),
       ("journal", "Trading Journal & R-Multiple Tracker (Excel)", "trading-strategy-simulator",
        "Log every closed trade and see what your method is really doing: R-multiple per trade, win rate, expectancy, profit factor, drawdown and results by setup.",
        ["500-row journal with automatic balance and drawdown", "Risk vs plan check on every trade", "Stats by setup", "Works in Excel, Google Sheets and Numbers"])]
tp = head(cfg, f"Spreadsheet templates: UAE final settlement, trading journal · {SITE_NAME}", "Excel templates from CalcSouq: a UAE final settlement and gratuity workbook, and a trading journal with R-multiples, expectancy and drawdown.", "/templates/", "uae final settlement excel, gratuity excel template, trading journal excel, r multiple tracker", [])
tp += '<main class="wrap"><section style="padding:36px 0 8px"><h1>Spreadsheet templates</h1><p class="lede">Our most-used calculators as spreadsheets you can keep, edit and share. The free calculators stay free.</p></section><div class="grid">'
for k, name, tool, d, feats in TPL:
    link = GR.get(k, "")
    btn = f'<a class="btn primary" href="{link}" rel="noopener">Buy on Gumroad</a>' if link else f'<a class="btn" href="mailto:{EMAIL}?subject=Notify%20me:%20{name.replace(" ", "%20")}">Email me when it is available</a>'
    tp += f'<div class="card" style="display:block"><b>{name}</b><p>{d}</p><ul>' + "".join(f"<li>{x}</li>" for x in feats) + f'</ul><p>{btn} <a href="/{tool}/">Try the free calculator</a></p></div>'
tp += '</div>' + ad() + "</main>" + foot()
w("templates/index.html", tp); paths.append(("/templates/", "monthly", "0.5"))

# Info pages
INFO = {
"about": ("About " + SITE_NAME, f"""<p>{SITE_NAME} is a free collection of online calculators and tools for everyday money, work and paperwork: resizing photos for applications, loan EMIs, gold prices, currency transfers, salary and end-of-service pay, trading risk and property costs. New tools are added regularly.</p>
<h2>How we build the tools</h2><p>Each calculator follows the published rule it is based on, such as the UAE Labour Law for gratuity, the FTA for VAT, or exchange contract specifications for futures, and shows the formula and a worked example so you can check the result yourself. Pages are reviewed when rules change.</p>
<h2>Who runs the site</h2><p>{SITE_NAME} is built and maintained by a finance professional with several years' experience in multi-asset dealing and operations across forex, CFDs, futures and equities.</p>
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
    w(k + "/index.html", head(cfg, f"{t} · {SITE_NAME}", f"{t} for {SITE_NAME}, free online calculators and tools.", p, "", [])
      + f'<main class="wrap"><article style="padding-top:36px"><h1>{t}</h1><p class="hint">Last updated {today:%d %B %Y}</p>{b}</article></main>' + foot())

# PWA
w("manifest.webmanifest", json.dumps({"name": "CalcSouq: free calculators & tools", "short_name": "CalcSouq", "start_url": "/", "scope": "/", "display": "standalone",
    "background_color": "#f6f6f4", "theme_color": "#f5c300", "description": "Free online calculators and photo tools.",
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
og = Image.new("RGB", (1200, 630), "#f6f6f4"); d = ImageDraw.Draw(og)
IF = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
fb = ImageFont.truetype(IF if os.path.exists(IF) else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 76)
fr = ImageFont.truetype(IF.replace("Bold", "Regular") if os.path.exists(IF) else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)
d.rounded_rectangle([80, 80, 190, 190], 28, fill="#f5c300"); d.text((135, 135), "C", font=fb, fill="#15171a", anchor="mm")
d.text((220, 135), "CalcSouq", font=fb, fill="#15171a", anchor="lm")
d.text((80, 300), "Free calculators & tools", font=fb, fill="#15171a"); d.text((80, 395), "Money · Work · Trading · Property · Photos", font=fr, fill="#555a62")
d.rectangle([80, 520, 280, 530], fill="#f5c300"); d.text((80, 560), "calcsouq.com", font=fr, fill="#15171a", anchor="lm")
og.save(os.path.join(out, "og.png"))

# Search index
idx = [{"t": t["name"], "u": f"/{t['slug']}/", "c": "Calculator", "d": t["card"], "k": t["keywords"]} for t in TOOLS]
idx += [{"t": m["name"], "u": f"/{c}/{k}/", "c": LANGS[c]["native"], "d": m["card"], "k": m["keywords"]} for c in LORDER for k, m in LANGS[c]["tools"].items()]
idx += [{"t": a["h1"], "u": f"/guides/{a['slug']}/", "c": "Guide", "d": a["lede"][:90], "k": a["keywords"]} for a in ARTICLES]
w("search-index.json", json.dumps(idx, ensure_ascii=False))

# SEO files
u = cfg["url"].rstrip("/")
INDEXNOW_KEY = "c4lcs0uq7e2b9f1a5d3e8c6b0a4f2d91"
def _alts_for(p):
    seg = [x for x in p.split("/") if x]
    if not seg: return HOME_ALTS
    if len(seg) == 1 and seg[0] in LANGS: return HOME_ALTS
    slug = seg[-1] if (len(seg) == 2 and seg[0] in LANGS) or len(seg) == 1 else None
    return lang_alts(slug) if slug and slug in TOOLS_ALL else None
def _sm(p, c, pr):
    a = _alts_for(p)
    x = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{u}{q}"/>' for l, q in (a or []))
    return f"<url><loc>{u}{p}</loc><lastmod>{today}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority>{x}</url>\n"
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "".join(_sm(p, c, pr) for p, c, pr in paths) + "</urlset>\n")
# llms.txt: plain list of every tool in every language, for AI assistants and answer engines
_ll = [f"# {SITE_NAME}", "", "> Free online calculators and tools. Every tool runs in the browser, shows its formula and needs no sign-up. Available in English, Hindi (hi), Chinese (zh), Russian (ru) and Malayalam (ml).", "", "## English"]
_ll += [f"- [{t['name']}]({u}/{t['slug']}/): {t['card']}" for t in TOOLS]
for c in LORDER:
    _ll += ["", f"## {LANGS[c]['native']} ({c})"] + [f"- [{m['name']}]({u}/{c}/{k}/): {m['card']}" for k, m in LANGS[c]["tools"].items()]
w("llms.txt", "\n".join(_ll) + "\n")
w(f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY)
# YouTube auto-upload feed: only items Paulson approved (build/youtube/uploads.json, status "approved").
# Zapier: "RSS by Zapier - New item in feed" (https://www.calcsouq.com/youtube/feed.xml) -> "YouTube - Upload video" (file = enclosure URL).
import email.utils as _eu
try:
    _yt = [x for x in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "youtube", "uploads.json"))) if x.get("status") == "approved"]
except Exception:
    _yt = []
def _x(v): return html.escape(str(v), quote=True)
_items = "".join(
    f"<item><title>{_x(v['title'])}</title><guid isPermaLink=\"false\">calcsouq-yt-{_x(v['id'])}</guid>"
    f"<link>{u}/media/yt/{_x(v['file'])}</link><description>{_x(v['description'])}</description>"
    f"<category>{_x(', '.join(v.get('tags', [])))}</category>"
    f"<pubDate>{_eu.format_datetime(datetime.datetime.fromisoformat(v['date'] + 'T12:00:00+04:00'))}</pubDate>"
    f"<enclosure url=\"{u}/media/yt/{_x(v['file'])}\" type=\"video/mp4\" length=\"{v.get('bytes', 0)}\"/></item>\n" for v in _yt)
w("youtube/feed.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>CalcSouq YouTube uploads</title>'
  f'<link>{u}/</link><description>Approved videos for the CalcSouq YouTube channel</description>\n{_items}</channel></rss>\n')
w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: {u}/sitemap.xml\n")
pub = cfg["adsense"].removeprefix("ca-") if cfg["adsense"] else "pub-XXXXXXXXXXXXXXXX"
w("ads.txt", f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
w("vercel.json", '{\n  "trailingSlash": true,\n  "redirects": [{ "source": "/gift-nifty", "destination": "/", "permanent": true }, { "source": "/gift-nifty/:path*", "destination": "/", "permanent": true }],\n  "headers": [{ "source": "/assets/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=86400" }] }]\n}\n')
w("package.json", '{ "name": "calcsouq", "private": true, "engines": { "node": ">=18" } }\n')
w("404.html", head(cfg, "Page not found · " + SITE_NAME, "Page not found", "/404.html", "", []) + '<main class="wrap"><article style="padding-top:36px"><h1>Page not found</h1><p><a href="/">See all calculators</a></p></article></main>' + foot())
print(len(paths), "pages")
