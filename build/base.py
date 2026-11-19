# Shared layout pieces for the CalcSouq site generator.
import json, html

SITE_NAME = "CalcSouq"
TAGLINE = "Free calculators for UAE & India"

CSS = r"""/*
VOICE: a calm, exact reference desk, like a well-made almanac of everyday money sums.
IDEA: the ruled ledger page: each tool is an entry with its sum, its rule and its notes.
PICTURE: on every tool page the live result, set large beside the inputs.
COLOUR and TYPE: white ground, ink, ultramarine accent; green and red only for gains and losses. Spectral headings, Inter text.
LAYOUT: slim header, tool first under a modest title, ad band, explainer, FAQ, related tools, footer.
*/
:root{color-scheme:light dark;--bg:light-dark(#ffffff,#0d0e18);--ink:light-dark(#14110f,#ecebf3);--mute:light-dark(#5d6170,#9a9db0);--line:light-dark(#e3e4ea,#262838);--panel:light-dark(#f4f5f9,#151726);--blue:light-dark(#1d2bd8,#8d96ff);--up:light-dark(#0a7a3e,#3fcf82);--dn:light-dark(#c2261d,#ff6b62)}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Inter,system-ui,sans-serif;overflow-x:clip}
h1,h2,h3{font-family:Spectral,Georgia,serif;font-weight:600;text-wrap:balance}
h1{font-size:clamp(32px,4.6vw,46px);line-height:1.06;margin:0 0 10px}
h2{font-size:28px;line-height:1.15;margin:40px 0 8px}
h3{font-size:20px;margin:24px 0 4px}
a{color:var(--blue)}
.wrap{max-width:1180px;margin:0 auto;padding:0 max(4vw,16px)}
header.top{border-bottom:1px solid var(--line);background:var(--bg)}
header.top .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:6px 24px;padding-block:12px}
.logo{font:600 26px Spectral,serif;color:var(--ink);text-decoration:none}.logo b{color:var(--blue);font-weight:600}
.logo small{display:block;font:400 13px Inter,sans-serif;color:var(--mute)}
header nav{display:flex;flex-wrap:wrap;gap:0 18px;font-size:15px}header nav a{color:var(--mute);text-decoration:none;padding:10px 0}header nav a:hover{color:var(--blue)}
.crumbs{font-size:14px;color:var(--mute);padding-top:20px}.crumbs a{color:var(--mute)}
.lede{color:var(--mute);font-size:18px;max-width:62ch;margin:0 0 22px}
.tool{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.inputs{padding:24px;display:grid;gap:16px;align-content:start}
.result{padding:24px;background:var(--panel);border-left:1px solid var(--line)}
label{display:block;font-size:15px;font-weight:500;margin-bottom:6px}
.hint{font-size:13px;color:var(--mute);margin-top:4px}
input,select{width:100%;font:16px Inter,sans-serif;min-height:46px;padding:10px 12px;border:1px solid var(--line);border-radius:7px;background:var(--bg);color:var(--ink)}
input:focus-visible,select:focus-visible,button:focus-visible,a:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.row2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px}
.seg{display:flex;flex-wrap:wrap;gap:6px}.seg button{flex:1 1 auto;font:500 15px Inter,sans-serif;min-height:44px;padding:0 14px;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:7px;cursor:pointer}
.seg button[aria-pressed=true]{background:var(--blue);border-color:var(--blue);color:#fff}
.check{display:flex;gap:10px;align-items:center;font-size:15px}.check input{width:22px;min-height:22px}
.big{font:600 clamp(38px,6vw,58px)/1.05 Spectral,serif;margin:4px 0 6px;font-variant-numeric:tabular-nums;overflow-wrap:anywhere}
.big-label{font-size:15px;color:var(--mute)}
.lines{margin:18px 0 0;padding:0;list-style:none;border-top:1px solid var(--line)}
.lines li{display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-size:15px}
.lines li b{font-variant-numeric:tabular-nums;white-space:nowrap}
.formula{font-size:14px;color:var(--mute);margin-top:14px}
.warn{color:var(--dn);font-size:15px;margin-top:10px}
.up{color:var(--up)}.dn{color:var(--dn)}
.ad{display:flex;align-items:center;justify-content:center;min-height:100px;margin:28px 0;background:var(--panel);border:1px dashed var(--line);border-radius:8px;color:var(--mute);font-size:13px}
.has-ads .ad{display:none}
article{max-width:72ch}
article p,article li{color:var(--ink)}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;font-size:15px}
th{text-align:left;font-weight:500;color:var(--mute);border-bottom:1px solid var(--ink);padding:8px 6px}
td{border-bottom:1px solid var(--line);padding:9px 6px}td.n,th.n{text-align:right;white-space:nowrap}
.faq details{border-bottom:1px solid var(--line);padding:12px 0}.faq summary{cursor:pointer;font-weight:600;min-height:28px}
.faq details p{margin:8px 0 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.card{display:block;border:1px solid var(--line);border-radius:10px;padding:18px;text-decoration:none;color:var(--ink);background:var(--bg)}
.card:hover{border-color:var(--blue)}.card b{font:600 20px Spectral,serif;display:block;margin-bottom:4px}.card span{font-size:15px;color:var(--mute)}
.group-title{font-size:15px;color:var(--mute);margin:34px 0 10px}
.related{margin-top:44px}
footer.site{border-top:1px solid var(--line);margin-top:56px;padding:28px 0 40px;color:var(--mute);font-size:14px}
footer.site nav{display:flex;flex-wrap:wrap;gap:4px 18px;margin-bottom:10px}footer.site a{color:var(--mute)}
.scroll{overflow-x:auto}
@media(max-width:760px){.tool{grid-template-columns:minmax(0,1fr)}.result{border-left:0;border-top:1px solid var(--line)}}
@media(max-width:420px){.row2{grid-template-columns:minmax(0,1fr)}table{font-size:13px}}
"""

JS = r"""// Shared helpers: formatting, remembered inputs, year.
window.F = (n, d = 2) => (Number.isFinite(n) ? n : 0).toLocaleString('en-IN', { minimumFractionDigits: d, maximumFractionDigits: d });
window.FX = (n, d = 2) => (Number.isFinite(n) ? n : 0).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
window.$ = id => document.getElementById(id);
window.V = id => parseFloat(String($(id).value).replace(/,/g, '')) || 0;
(() => {
  const key = 'calcsouq:' + location.pathname;
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(key) || '{}'); } catch (e) {}
  document.querySelectorAll('.inputs input, .inputs select').forEach(el => {
    if (el.id && saved[el.id] != null) { if (el.type === 'checkbox') el.checked = saved[el.id]; else el.value = saved[el.id]; }
    el.addEventListener('input', () => {
      saved[el.id] = el.type === 'checkbox' ? el.checked : el.value;
      try { localStorage.setItem(key, JSON.stringify(saved)); } catch (e) {}
    });
  });
  window.seg = (groupId, onChange) => {
    const g = $(groupId), btns = [...g.querySelectorAll('button')];
    let v = saved[groupId] || btns.find(b => b.getAttribute('aria-pressed') === 'true').dataset.v;
    const set = val => { v = val; btns.forEach(b => b.setAttribute('aria-pressed', b.dataset.v === v)); saved[groupId] = v; try { localStorage.setItem(key, JSON.stringify(saved)); } catch (e) {} onChange(v); };
    btns.forEach(b => b.addEventListener('click', () => set(b.dataset.v)));
    btns.forEach(b => b.setAttribute('aria-pressed', b.dataset.v === v));
    return () => v;
  };
  document.querySelectorAll('.yr').forEach(e => e.textContent = new Date().getFullYear());
})();
"""

NAV = [("UAE", "/#uae"), ("Trading", "/#trading"), ("India & Kerala", "/#india"), ("GIFT Nifty", "/gift-nifty/"), ("Guides", "/guides/")]


def head(cfg, title, desc, path, keywords, jsonld):
    url = cfg["url"].rstrip("/") + path
    ads = ""
    if cfg["adsense"]:
        ads = ('<meta name="google-adsense-account" content="%s">\n'
               '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=%s" crossorigin="anonymous"></script>\n'
               % (cfg["adsense"], cfg["adsense"]))
    gsc = '<meta name="google-site-verification" content="%s">\n' % cfg["gsc"] if cfg.get("gsc") else ""
    ld = "".join('<script type="application/ld+json">%s</script>\n' % json.dumps(j, ensure_ascii=False) for j in jsonld)
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(keywords)}">
<link rel="canonical" href="{e(url)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#1d2bd8">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{gsc}{ads}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Spectral:wght@600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
{ld}</head>
<body{' class="has-ads"' if cfg["adsense"] else ''}>
<header class="top"><div class="wrap">
<a class="logo" href="/">Calc<b>Souq</b><small>{TAGLINE}</small></a>
<nav aria-label="Main">{''.join(f'<a href="{h}">{n}</a>' for n, h in NAV)}</nav>
</div></header>
"""


def ad(label="Advertisement"):
    return f'<div class="ad" role="complementary" aria-label="Advertisement">{label}</div>'


def foot(extra_js=""):
    return f"""<footer class="site"><div class="wrap">
<nav aria-label="Footer"><a href="/">All calculators</a><a href="/guides/">Guides</a><a href="/about/">About</a><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms</a><a href="/contact/">Contact</a></nav>
<p>© <span class="yr">2026</span> {SITE_NAME}. Results are estimates for general information, not legal, tax or investment advice.</p>
</div></footer>
<script src="/assets/site.js"></script>
{extra_js}
</body>
</html>
"""


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def crumbs_ld(cfg, name, path):
    u = cfg["url"].rstrip("/")
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": u + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": u + path}]}


def app_ld(cfg, name, desc, path):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "description": desc,
            "url": cfg["url"].rstrip("/") + path, "applicationCategory": "FinanceApplication",
            "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}


def article_ld(cfg, title, desc, path, date):
    return {"@context": "https://schema.org", "@type": "Article", "headline": title[:110], "description": desc,
            "mainEntityOfPage": cfg["url"].rstrip("/") + path, "datePublished": date, "dateModified": date,
            "author": {"@type": "Organization", "name": SITE_NAME}, "publisher": {"@type": "Organization", "name": SITE_NAME}}
