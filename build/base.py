# Shared layout pieces for the CalcSouq site generator.
import json, html, hashlib

SITE_NAME = "CalcSouq"
TAGLINE = "Free calculators for UAE & India"

CSS = r"""/*
VOICE: Kootu's Nila family: ink and ivory, one gold accent, calm and precise.
IDEA: a gold souq at dusk: each calculator is a stall, each result weighed out in gold type.
PICTURE: the live result set large in Bodoni on a softly gilded panel beside the inputs.
COLOUR and TYPE: ivory #f6f6f4 / night #0c0c0d, ink, gold #f5c300 with antique #8a6c00 for text. Bodoni Moda display, Figtree body.
LAYOUT: brand + nav, gold hairline, tool first, stall (ad) bands, explainer, FAQ, related cards, footer.
*/
:root{color-scheme:light dark;
--bg:light-dark(#f6f6f4,#0c0c0d);--surface:light-dark(#ffffff,rgba(255,255,255,.05));--panel:light-dark(#fbf8ee,rgba(245,195,0,.06));
--ink:light-dark(#111111,#ffffff);--mute:light-dark(#66666b,#a0a0a6);--line:light-dark(#e2e2de,rgba(255,255,255,.1));
--champ:light-dark(#8a6c00,#f5c300);--act:#f5c300;--act-ink:#111;--blue:var(--champ);
--aa:light-dark(rgba(245,195,0,.2),rgba(245,195,0,.12));--ab:light-dark(rgba(17,17,17,.05),rgba(255,255,255,.05));
--shadow:light-dark(0 24px 48px -32px rgba(20,22,27,.28),0 30px 60px -36px rgba(0,0,0,.9));
--up:light-dark(#0a7a3e,#3fcf82);--dn:light-dark(#c2261d,#ff6b62);
--display:"Bodoni Moda","Didot","Bodoni 72",Georgia,serif;--body:"Figtree",system-ui,sans-serif;--ease:cubic-bezier(.22,1,.36,1)}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
html{scroll-padding-top:24px}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 var(--body);overflow-x:clip;position:relative}
body::before{content:"";position:fixed;inset:-25vmax;z-index:-1;pointer-events:none;background:radial-gradient(42vmax 42vmax at 78% 18%,var(--aa),transparent 68%),radial-gradient(48vmax 48vmax at 12% 82%,var(--ab),transparent 70%);animation:aura 32s ease-in-out infinite alternate}
@keyframes aura{from{transform:translate3d(-3%,-2%,0) rotate(0)}to{transform:translate3d(4%,3%,0) rotate(10deg) scale(1.08)}}
h1,h2,h3{font-family:var(--display);text-wrap:balance;letter-spacing:-.015em}
h1{font-weight:400;font-size:clamp(2.3rem,7vw,3.6rem);line-height:1.02;margin:0 0 12px;animation:unveil 1.1s var(--ease) both .15s}
h2{font-weight:500;font-size:1.7rem;line-height:1.12;margin:44px 0 10px}
h3{font-weight:500;font-size:1.25rem;margin:26px 0 6px}
@keyframes unveil{from{clip-path:inset(0 0 100% 0);transform:translate3d(0,30%,0);opacity:0}to{clip-path:inset(-10% 0 -10% 0);transform:none;opacity:1}}
a{color:var(--champ);text-underline-offset:3px}
.wrap{max-width:1140px;margin:0 auto;padding:0 max(4vw,18px)}
main.wrap>*{animation:settle .8s var(--ease) both}main.wrap>*:nth-child(2){animation-delay:.08s}main.wrap>*:nth-child(3){animation-delay:.16s}main.wrap>*:nth-child(4){animation-delay:.24s}main.wrap>*:nth-child(n+5){animation-delay:.32s}
@keyframes settle{from{opacity:0;transform:translate3d(0,26px,0)}to{opacity:1;transform:none}}
header.top{position:relative}
header.top .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:6px 24px;padding-block:18px}
header.top::after{content:"";display:block;height:1px;max-width:1140px;margin:0 auto;background:linear-gradient(90deg,transparent,var(--champ) 18%,var(--champ) 82%,transparent);opacity:.6}
.logo{font:400 30px/1 var(--display);letter-spacing:-.02em;color:var(--ink);text-decoration:none}
.logo b{font-style:italic;font-weight:500;color:var(--champ)}
.logo small{display:block;font:500 13px var(--body);letter-spacing:0;color:var(--mute);margin-top:4px}
header nav{display:flex;flex-wrap:wrap;gap:2px 6px;font-size:15px}
header nav a{color:var(--ink);text-decoration:none;padding:9px 13px;border-radius:999px;transition:background .25s var(--ease)}
header nav a:hover{background:var(--ab)}
.crumbs{font-size:14px;color:var(--mute);padding-top:24px}.crumbs a{color:var(--mute)}
.lede{color:var(--mute);font-size:18px;max-width:62ch;margin:0 0 26px}
.tool{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);background:var(--surface);border:1px solid var(--line);border-radius:26px;overflow:hidden;box-shadow:var(--shadow)}
.inputs{padding:26px;display:grid;gap:18px;align-content:start}
.result{padding:28px 26px;background:linear-gradient(160deg,var(--panel),transparent 80%);border-left:1px solid var(--line);position:relative}
.result::before{content:"";position:absolute;left:26px;right:26px;top:0;height:2px;background:linear-gradient(90deg,transparent,var(--act),transparent);opacity:.8}
label{display:block;font-size:15px;font-weight:600;margin-bottom:7px}
.hint{font-size:13.5px;color:var(--mute);margin-top:5px}
input,select{width:100%;font:16px var(--body);min-height:50px;padding:11px 14px;border:1px solid var(--line);border-radius:14px;background:var(--bg);color:var(--ink);transition:border-color .2s,box-shadow .2s}
input:focus,select:focus{outline:none;border-color:var(--champ);box-shadow:0 0 0 4px var(--aa)}
button:focus-visible,a:focus-visible{outline:2px solid var(--champ);outline-offset:3px}
.row2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px}
.seg{display:flex;flex-wrap:wrap;gap:4px;padding:4px;background:var(--ab);border-radius:16px}
.seg button{flex:1 1 auto;font:600 15px var(--body);min-height:44px;padding:0 14px;border:0;background:transparent;color:var(--ink);border-radius:12px;cursor:pointer;transition:background .3s var(--ease),transform .22s cubic-bezier(.34,1.45,.5,1)}
.seg button:active{transform:scale(.96)}
.seg button[aria-pressed=true]{background:var(--act);color:var(--act-ink);box-shadow:0 6px 16px -8px rgba(138,108,0,.6)}
.check{display:flex;gap:10px;align-items:center;font-size:15px;font-weight:500}.check input{width:22px;min-height:22px;accent-color:#f5c300}
.big{font:400 clamp(40px,6.4vw,64px)/1.04 var(--display);letter-spacing:-.02em;margin:6px 0 8px;font-variant-numeric:lining-nums tabular-nums;overflow-wrap:anywhere}
.big.pop{animation:pop .45s var(--ease)}
@keyframes pop{0%{opacity:.35;transform:translate3d(0,8px,0)}100%{opacity:1;transform:none}}
.big-label{font-family:var(--display);font-style:italic;font-size:18px;color:var(--champ)}
.lines{margin:20px 0 0;padding:0;list-style:none;border-top:1px solid var(--line)}
.lines li{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid var(--line);font-size:15px}
.lines li b{font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap}
.formula{font-size:14px;color:var(--mute);margin-top:14px}
.up{color:var(--up)}.dn{color:var(--dn)}
article{max-width:72ch}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;font-size:15px}
th{text-align:left;font-weight:600;color:var(--mute);border-bottom:1px solid var(--ink);padding:9px 6px}
td{border-bottom:1px solid var(--line);padding:10px 6px}td.n,th.n{text-align:right;white-space:nowrap}
.faq details{border-bottom:1px solid var(--line);padding:14px 0}
.faq summary{cursor:pointer;font-weight:600;min-height:28px;list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::after{content:"+";font:400 24px/1 var(--display);color:var(--champ);transition:transform .3s var(--ease)}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{margin:8px 0 0;color:var(--mute)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.card{display:block;background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:20px 22px;text-decoration:none;color:var(--ink);box-shadow:var(--shadow);transition:transform .35s var(--ease),border-color .35s}
.card:hover{transform:translate3d(0,-4px,0);border-color:var(--champ)}
.card b{font:500 21px/1.2 var(--display);display:block;margin-bottom:6px}.card span{font-size:15px;color:var(--mute)}
.group-title{scroll-margin-top:20px}
.related{margin-top:48px}.related ul{padding-left:20px}
/* Ad stalls: a framed, labelled space that is clearly separate from the tools */
.stall{margin:40px 0;border-radius:24px;padding:1px;background:linear-gradient(120deg,var(--line),var(--champ),var(--line),var(--line));background-size:300% 100%;animation:sheen 9s linear infinite}
@keyframes sheen{to{background-position:-300% 0}}
.stall-in{border-radius:23px;background:var(--bg);padding:12px 16px 16px}
.stall-label{display:flex;align-items:center;gap:10px;font-size:12.5px;color:var(--mute);margin-bottom:10px}
.stall-label::before,.stall-label::after{content:"";flex:1;height:1px;background:var(--line)}
.stall-body{min-height:90px;display:grid;place-items:center}
.stall:has(ins[data-ad-status=unfilled]){display:none}
.house{display:grid;gap:4px;text-align:center;padding:10px 6px}
.house b{font:500 22px/1.2 var(--display)}.house b i{color:var(--champ)}
.house span{font-size:14px;color:var(--mute)}
footer.site{margin-top:64px;padding:28px 0 44px;color:var(--mute);font-size:14px}
footer.site::before{content:"";display:block;height:1px;max-width:1140px;margin:0 auto 26px;background:linear-gradient(90deg,transparent,var(--champ) 18%,var(--champ) 82%,transparent);opacity:.5}
footer.site nav{display:flex;flex-wrap:wrap;gap:4px 18px;margin-bottom:10px}footer.site a{color:var(--mute)}
.scroll{overflow-x:auto}
@media(max-width:760px){.tool{grid-template-columns:minmax(0,1fr)}.result{border-left:0;border-top:1px solid var(--line)}}
@media(max-width:600px){table{font-size:13px}.stack thead{display:none}.stack tr{display:grid;padding-block:10px}.stack td{display:flow-root;border:0;padding:3px 0;padding-inline-start:8em;text-align:start;white-space:normal}.stack td::before{content:attr(data-l);float:inline-start;width:7.5em;margin-inline-start:-8em;color:var(--mute)}.stack td:empty{display:none}}
@media(max-width:600px){header nav{flex-wrap:nowrap;overflow-x:auto;margin:0 -6px;scrollbar-width:none;width:100%}header nav::-webkit-scrollbar{display:none}header nav a{flex:none;background:var(--ab)}}
@media(max-width:420px){.row2{grid-template-columns:minmax(0,1fr)}}
.share{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:16px 0 0}
.share span{font-size:14px;color:var(--mute);margin-right:4px}
.share a,.share button{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font:600 14.5px var(--body);text-decoration:none;cursor:pointer;transition:transform .22s cubic-bezier(.34,1.45,.5,1),border-color .25s}
.share a:active,.share button:active{transform:scale(.96)}
.share .wa{background:#25d366;border-color:#25d366;color:#08311b}
.share svg{width:18px;height:18px}
.install{display:none;margin:18px 0 0}.install.show{display:flex}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
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
  // result numbers glide in when they change
  const bigObs = new MutationObserver(ms => ms.forEach(m => { const el = m.target.nodeType === 1 ? m.target.closest('.big') : m.target.parentElement && m.target.parentElement.closest('.big'); if (el) { el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop'); } }));
  document.querySelectorAll('.big').forEach(b => bigObs.observe(b, { childList: true, characterData: true, subtree: true }));
  // label table cells for the stacked phone layout
  const label = () => document.querySelectorAll('.stack').forEach(t => { const h = [...t.querySelectorAll('thead th')].map(x => x.textContent); t.querySelectorAll('tbody tr').forEach(r => [...r.cells].forEach((c, i) => c.dataset.l = h[i] || '')); });
  label(); const stackObs = new MutationObserver(label); document.querySelectorAll('.stack tbody').forEach(b => stackObs.observe(b, { childList: true }));
  // share bar: WhatsApp, native share, copy link
  const shareText = () => { const h = document.querySelector('h1'), b = document.querySelector('.big'), l = document.querySelector('.big-label');
    return (b && b.textContent.trim() && b.textContent.trim() !== '—' ? `${h ? h.textContent.trim() : 'CalcSouq'}: ${l ? l.textContent.trim() + ' ' : ''}${b.textContent.trim()}. Try yours: ` : `${document.title}: `) + location.origin + location.pathname; };
  const wa = document.querySelector('.share .wa');
  const syncWa = () => { if (wa) wa.href = 'https://wa.me/?text=' + encodeURIComponent(shareText()); };
  syncWa(); const waObs = new MutationObserver(syncWa); document.querySelectorAll('.big').forEach(b => waObs.observe(b, { childList: true, characterData: true, subtree: true }));
  const nat = document.querySelector('.share .native');
  if (nat) { if (!navigator.share) nat.hidden = true; nat.addEventListener('click', () => navigator.share({ title: document.title, text: shareText(), url: location.href }).catch(() => {})); }
  const cp = document.querySelector('.share .copy');
  if (cp) cp.addEventListener('click', () => { (navigator.clipboard ? navigator.clipboard.writeText(location.href) : Promise.reject()).then(() => { cp.lastChild.textContent = 'Link copied'; setTimeout(() => cp.lastChild.textContent = 'Copy link', 1800); }).catch(() => { cp.lastChild.textContent = location.href; }); });
  // installable app
  if ('serviceWorker' in navigator && location.protocol === 'https:') navigator.serviceWorker.register('/sw.js').catch(() => {});
  let deferred; const ib = document.querySelector('.install');
  window.addEventListener('beforeinstallprompt', e => { e.preventDefault(); deferred = e; if (ib) ib.classList.add('show'); });
  if (ib) { const ios = /iphone|ipad|ipod/i.test(navigator.userAgent) && !navigator.standalone; if (ios) { ib.classList.add('show'); ib.querySelector('button').hidden = true; ib.querySelector('.ios').hidden = false; }
    ib.querySelector('button').addEventListener('click', () => { if (deferred) { deferred.prompt(); deferred = null; ib.classList.remove('show'); } }); }
})();
"""

VER = hashlib.md5((CSS + JS).encode()).hexdigest()[:8]

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
<meta name="theme-color" content="#f5c300">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="apple-touch-icon" href="/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="CalcSouq">
{gsc}{ads}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..600&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={VER}">
{ld}</head>
<body>
<header class="top"><div class="wrap">
<a class="logo" href="/">Calc<b>Souq</b><small>{TAGLINE}</small></a>
<nav aria-label="Main">{''.join(f'<a href="{h}">{n}</a>' for n, h in NAV)}</nav>
</div></header>
"""


AD = {"client": "", "slot": ""}

HOUSE = ['<b>Your brand in this <i>stall</i></b><span>Reach UAE expats, NRIs and traders. Write to us via the Contact page.</span>',
         '<b>Advertise on <i>CalcSouq</i></b><span>Calculators used by expats and traders across the Gulf and India.</span>']
_n = [0]

def ad(label="Advertisement"):
    _n[0] += 1
    if AD["client"] and AD["slot"]:
        body = (f'<ins class="adsbygoogle" style="display:block;width:100%" data-ad-client="{AD["client"]}" data-ad-slot="{AD["slot"]}" '
                'data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>')
    else:
        body = f'<a class="house" href="/contact/" style="text-decoration:none;color:inherit">{HOUSE[_n[0] % 2]}</a>'
    return f'<aside class="stall" aria-label="Advertisement"><div class="stall-in"><div class="stall-label">{label}</div><div class="stall-body">{body}</div></div></aside>'


def foot(extra_js=""):
    return f"""<footer class="site"><div class="wrap">
<nav aria-label="Footer"><a href="/">All calculators</a><a href="/guides/">Guides</a><a href="/about/">About</a><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms</a><a href="/contact/">Contact</a></nav>
<p>© <span class="yr">2026</span> {SITE_NAME}. Results are estimates for general information, not legal, tax or investment advice.</p>
</div></footer>
<script src="/assets/site.js?v={VER}"></script>
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


WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.7 11.7 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3z"/></svg>'

def share_bar():
    return ('<div class="share" aria-label="Share"><span>Share your result</span>'
            f'<a class="wa" href="https://wa.me/" rel="noopener">{WA_SVG}WhatsApp</a>'
            '<button type="button" class="native">Share</button>'
            '<button type="button" class="copy"><span hidden></span>Copy link</button></div>')
