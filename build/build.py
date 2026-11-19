# Usage: python3 build.py OUTDIR [SITE_URL] [ADSENSE_CLIENT] [SEARCH_CONSOLE_CODE]
import os, sys, shutil, html, datetime, json
sys.path.insert(0, os.path.dirname(__file__))
from base import CSS, JS, head, foot, ad, faq_ld, crumbs_ld, app_ld, article_ld, SITE_NAME, TAGLINE
from articles import ARTICLES
import base
from tools_india import TOOLS

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
GROUPS = [("uae", "UAE money tools"), ("trading", "Trading calculators"), ("india", "India & Kerala")]

if os.path.exists(out):
    shutil.rmtree(out)
os.makedirs(out + "/assets")
w = lambda p, s: (os.makedirs(os.path.dirname(os.path.join(out, p)), exist_ok=True), open(os.path.join(out, p), "w").write(s))
w("assets/site.css", CSS)
w("assets/site.js", JS)
w("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1d2bd8"/><text x="32" y="45" font-family="Georgia,serif" font-size="38" font-weight="700" fill="#fff" text-anchor="middle">C</text></svg>')
paths = []

def related(t):
    same = [x for x in TOOLS if x["group"] == t["group"] and x is not t]
    other = [x for x in TOOLS if x["group"] != t["group"]][:2]
    return '<section class="related"><h2>Related calculators</h2><div class="grid">' + "".join(
        f'<a class="card" href="/{x["slug"]}/"><b>{x["name"]}</b><span>{x["card"]}</span></a>' for x in (same + other)[:6]) + "</div></section>"

for t in TOOLS:
    p = f"/{t['slug']}/"
    paths.append((p, "weekly", "0.9"))
    faqs = t["faqs"]
    page = head(cfg, t["title"], t["desc"], p, t["keywords"], [app_ld(cfg, t["name"], t["desc"], p), crumbs_ld(cfg, t["name"], p), faq_ld(faqs)])
    page += f'<main class="wrap"><div class="crumbs"><a href="/">Home</a> › {t["name"]}</div>\n<h1>{t["h1"]}</h1><p class="lede">{t["lede"]}</p>\n'
    page += f'<section class="tool" aria-label="{html.escape(t["name"])}">{t["tool"]}</section>\n{ad()}\n'
    page += f'<article>{t["body"]}<p class="hint">Last reviewed {today:%d %B %Y}.</p></article>\n{ad()}\n'
    page += '<section class="faq"><h2>Frequently asked questions</h2>' + "".join(
        f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faqs) + "</section>\n"
    gl = [a for a in ARTICLES if a["tool"] == t["slug"]]
    if gl:
        page += '<section class="related"><h2>Guides</h2><ul>' + "".join(f'<li><a href="/guides/{a["slug"]}/">{a["h1"]}</a></li>' for a in gl) + "</ul></section>"
    page += related(t) + "</main>\n"
    page += foot("<script>\n{" + t["js"] + "}\n</script>")
    w(p.strip("/") + "/index.html", page)

# Home
hd = f"Free UAE gratuity, VAT, gold, remittance, forex pip, lot size, margin and Kerala land calculators. Fast, accurate and free, with no sign-up."
ld_site = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": cfg["url"].rstrip("/") + "/", "description": hd}
home = head(cfg, f"{SITE_NAME}: Free Calculators for UAE & India (Gratuity, VAT, Gold, Forex)", hd, "/",
            "uae calculators, gratuity calculator, vat calculator uae, gold price calculator dubai, aed to inr, pip calculator, lot size calculator, cent to sq ft, kerala stamp duty", [ld_site])
home += '<main class="wrap"><section style="padding:36px 0 8px"><h1>Everyday money sums for the UAE and India, done right</h1>'
home += '<p class="lede">Free calculators for expats, traders and families back home. Every formula is explained, and each page shows its worked example.</p></section>'
home += '<a class="card" href="/gift-nifty/" style="background:var(--panel);margin:10px 0 6px"><b>GIFT Nifty today</b><span>Delayed GIFT Nifty price, implied Nifty 50 opening gap and global cues before 9:15 IST.</span></a>'
for g, gt in GROUPS:
    home += f'<h2 id="{g}" class="group-title" style="font:600 26px Spectral,serif;color:var(--ink)">{gt}</h2><div class="grid">'
    home += "".join(f'<a class="card" href="/{t["slug"]}/"><b>{t["name"]}</b><span>{t["card"]}</span></a>' for t in TOOLS if t["group"] == g)
    home += "</div>"
    if g == "uae": home += ad()
home += '<h2 id="guides" class="group-title" style="font:600 26px Spectral,serif;color:var(--ink)">Guides</h2><div class="grid">' + "".join(f'<a class="card" href="/guides/{a["slug"]}/"><b>{a["h1"]}</b><span>{a["desc"][:90].rsplit(" ",1)[0]}…</span></a>' for a in ARTICLES[:9]) + '</div><p><a href="/guides/">All guides →</a></p>'
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
    pg += f'<a class="card" href="/{t["slug"]}/" style="background:var(--panel);margin:8px 0 20px"><b>Try the {t["name"]} →</b><span>{t["card"]}</span></a>'
    pg += a["body"] + ad() + '<section class="faq"><h2>Frequently asked questions</h2>' + "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(x)}</p></details>" for q, x in a["faqs"]) + "</section>"
    pg += f'<p class="hint">Updated {today:%d %B %Y}. General information only, not legal, tax or investment advice.</p></article>'
    more = [b for b in ARTICLES if b["group"] == a["group"] and b is not a][:4]
    pg += '<section class="related"><h2>More guides</h2><div class="grid">' + "".join(f'<a class="card" href="/guides/{b["slug"]}/"><b>{b["h1"]}</b></a>' for b in more) + "</div></section></main>" + foot()
    w(p.strip("/") + "/index.html", pg)
gi = head(cfg, f"Guides: UAE Gratuity, VAT, Gold, Forex Trading & Kerala Property · {SITE_NAME}", "Plain-English guides for expats and traders in the UAE and India: gratuity, VAT, gold, remittances, forex risk, futures, GIFT Nifty and Kerala land.", "/guides/", "uae guides, gratuity guide, forex guide, kerala land guide", [])
gi += '<main class="wrap"><section style="padding:36px 0 8px"><h1>Guides</h1><p class="lede">Short, exact answers to the questions behind our calculators.</p></section>'
for g, gt in GROUPS:
    gi += f'<h2 class="group-title" style="font:600 26px Spectral,serif;color:var(--ink)">{gt}</h2><div class="grid">' + "".join(f'<a class="card" href="/guides/{a["slug"]}/"><b>{a["h1"]}</b><span>{a["lede"][:110]}</span></a>' for a in ARTICLES if a["group"] == g) + "</div>"
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

# GIFT Nifty page (adapted from the standalone page)
g = open(os.path.join(os.path.dirname(__file__), "giftnifty_index.html")).read()
gd = "GIFT Nifty live today (delayed): price, change, implied Nifty 50 opening gap, global cues and GIFT Nifty trading timings in IST and UAE time."
seo = (f'<meta name="keywords" content="gift nifty, gift nifty live, sgx nifty, sgx nifty live, gift nifty today, nifty pre market, gift nifty timings, nse ix">\n'
       f'<link rel="canonical" href="{cfg["url"].rstrip("/")}/gift-nifty/">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n')
if cfg["adsense"]:
    seo += f'<meta name="google-adsense-account" content="{cfg["adsense"]}">\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={cfg["adsense"]}" crossorigin="anonymous"></script>\n<style>.ad{{display:none!important}}</style>\n'
g = g.replace("<title>PreOpen · GIFT Nifty</title>", "<title>GIFT Nifty Live Today (Delayed): Price, Pre-Open Gap & Timings · CalcSouq</title>")
g = g.replace('<meta name="description" content="GIFT Nifty price (delayed), implied Nifty 50 opening gap, global market cues and session timings.">', f'<meta name="description" content="{gd}">\n' + seo)
g = g.replace('<a class="logo" href="#top">Pre<b>Open</b></a>', '<a class="logo" href="/">Calc<b>Souq</b></a>')
g = g.replace('<nav><a href="#quote">', '<nav><a href="/">All calculators</a><a href="#quote">')
g = g.replace('PreOpen is not affiliated', 'CalcSouq is not affiliated').replace('© <span id="yr"></span> PreOpen', '© <span id="yr"></span> CalcSouq')
for a, b in [("/about.html", "/about/"), ("/privacy.html", "/privacy/"), ("/terms.html", "/terms/"), ("/contact.html", "/contact/")]:
    g = g.replace(a, b)
THEME_OVERRIDE = """<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..600&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>:root{--bg:light-dark(#f6f6f4,#0c0c0d);--ink:light-dark(#111,#fff);--mute:light-dark(#66666b,#a0a0a6);--line:light-dark(#e2e2de,rgba(255,255,255,.1));--panel:light-dark(#fbf8ee,rgba(245,195,0,.06));--blue:light-dark(#8a6c00,#f5c300)}
body{font-family:Figtree,system-ui,sans-serif}h1,h2,.serif,.price,.logo,.times b{font-family:"Bodoni Moda",Georgia,serif!important;font-weight:400!important}
.logo b{font-style:italic;color:var(--blue)}.tabs button[aria-pressed=true]{background:#f5c300;color:#111;border-color:#f5c300}
.ad{border-radius:22px;border:1px solid var(--line)!important;background:var(--panel)!important}
header{background:color-mix(in srgb,var(--bg) 88%,transparent)!important;backdrop-filter:blur(10px)}</style>
"""
g = g.replace("</head>", THEME_OVERRIDE + "</head>", 1)
assert "Calc<b>Souq" in g and "canonical" in g
w("gift-nifty/index.html", g)
paths.insert(1, ("/gift-nifty/", "hourly", "0.9"))
os.makedirs(out + "/api", exist_ok=True)
shutil.copy(os.path.join(os.path.dirname(__file__), "quote.js"), out + "/api/quote.js")

# SEO files
u = cfg["url"].rstrip("/")
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"<url><loc>{u}{p}</loc><lastmod>{today}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n" for p, c, pr in paths) + "</urlset>\n")
w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: {u}/sitemap.xml\n")
pub = cfg["adsense"].removeprefix("ca-") if cfg["adsense"] else "pub-XXXXXXXXXXXXXXXX"
w("ads.txt", f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
w("vercel.json", '{\n  "trailingSlash": true,\n  "headers": [{ "source": "/assets/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=86400" }] }]\n}\n')
w("package.json", '{ "name": "calcsouq", "private": true, "engines": { "node": ">=18" } }\n')
w("404.html", head(cfg, "Page not found · " + SITE_NAME, "Page not found", "/404.html", "", []) + '<main class="wrap"><article style="padding-top:36px"><h1>Page not found</h1><p><a href="/">See all calculators</a></p></article></main>' + foot())
print(len(paths), "pages")
