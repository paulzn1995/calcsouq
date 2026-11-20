# Shared layout pieces for the CalcSouq site generator.
import json, html, hashlib

SITE_NAME = "CalcSouq"
TAGLINE = "Free online calculators and tools"

CSS = r"""/*
VOICE: a practical, trustworthy utility, like a bank's or Wise's calculator pages: plain words, exact numbers, no decoration for its own sake.
IDEA: a well-run souq stall of tools: everything findable from one search box, each tool a clean worksheet with its sources.
PICTURE: on each tool page, the result card with one large number and an itemised breakdown.
COLOUR and TYPE: warm white #f7f7f5 / graphite #0f1012, ink #15171a, one gold brand colour #f5c300 used sparingly; Inter throughout, tabular numbers.
LAYOUT: sticky header with search, compact tool grid with icons, worksheet + result, sources, FAQ, related.
*/
:root{color-scheme:light dark;
--bg:light-dark(#f7f7f5,#0f1012);--surface:light-dark(#ffffff,#17181b);--soft:light-dark(#f1f1ee,#1d1f23);
--ink:light-dark(#15171a,#f2f2f0);--mute:light-dark(#5f6368,#a3a6ad);--line:light-dark(#e4e4e0,#2a2c31);
--gold:#f5c300;--gold-ink:light-dark(#7a5f00,#f5c300);--champ:var(--gold-ink);--panel:var(--soft);--ab:var(--soft);
--up:light-dark(#0a7a3e,#3fcf82);--dn:light-dark(#c2261d,#ff6b62);--focus:light-dark(#1a56db,#7aa2ff);
--shadow:light-dark(0 1px 2px rgba(16,24,40,.04),0 1px 2px rgba(0,0,0,.4));--body:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
html{scroll-padding-top:80px}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--body);overflow-x:clip;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:var(--body);letter-spacing:-.02em;text-wrap:balance;color:var(--ink)}
h1{font-size:clamp(28px,4.4vw,40px);line-height:1.12;font-weight:700;margin:6px 0 10px}
h2{font-size:23px;line-height:1.25;font-weight:700;margin:40px 0 10px}
h3{font-size:18px;font-weight:650;margin:24px 0 6px}
a{color:var(--focus);text-underline-offset:3px}
.wrap{max-width:1120px;margin:0 auto;padding:0 max(4vw,16px)}
header.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--surface) 92%,transparent);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;gap:14px 20px;min-height:64px;flex-wrap:wrap;padding-block:8px}
.logo{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-weight:750;font-size:19px;letter-spacing:-.02em}
.logo i{display:grid;place-items:center;width:32px;height:32px;border-radius:9px;background:var(--gold);color:#15171a;font:800 18px/1 var(--body);font-style:normal}
.logo small{display:none}
.search{position:relative;flex:1 1 280px;max-width:460px}
.search input{width:100%;min-height:42px;padding:8px 14px 8px 38px;border-radius:10px;border:1px solid var(--line);background:var(--soft);color:var(--ink);font:15px var(--body)}
.search input:focus{outline:2px solid var(--focus);outline-offset:0;background:var(--surface)}
.search svg{position:absolute;left:12px;top:50%;width:16px;height:16px;transform:translateY(-50%);color:var(--mute)}
.results{position:absolute;left:0;right:0;top:calc(100% + 6px);background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:0 12px 32px -12px rgba(0,0,0,.25);padding:6px;display:none;max-height:60vh;overflow:auto}
.results.open{display:block}
.results a{display:block;padding:9px 10px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:15px}
.results a small{display:block;color:var(--mute);font-size:13px}
.results a:hover,.results a.sel{background:var(--soft)}
.results p{margin:8px 10px;color:var(--mute);font-size:14px}
header nav{display:flex;gap:4px;margin-left:auto}
header nav a{color:var(--ink);text-decoration:none;font-weight:550;font-size:15px;padding:8px 12px;border-radius:8px}
header nav a:hover{background:var(--soft)}
.crumbs{font-size:13.5px;color:var(--mute);padding-top:22px}.crumbs a{color:var(--mute)}
.lede{color:var(--mute);font-size:17px;max-width:64ch;margin:0 0 8px}
.meta{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:13.5px;color:var(--mute);margin:0 0 22px}
.meta a{color:var(--mute)}
.tool{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);background:var(--surface);border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:var(--shadow)}
.inputs{padding:24px;display:grid;gap:16px;align-content:start}
.result{padding:24px;background:var(--soft);border-left:1px solid var(--line)}
label{display:block;font-size:14px;font-weight:600;margin-bottom:6px}
[hidden]{display:none!important}
.hint{font-size:13px;color:var(--mute);margin-top:5px;line-height:1.45}
.pick-btn{position:relative;overflow:hidden}.pick-btn input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer;font-size:0}
.photo-pick{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:0 0 16px;position:relative}.photo-pick .hint{margin:0;min-width:0;overflow-wrap:anywhere}
.crop-wrap{display:flex;justify-content:center;margin:16px 0 0;padding:14px;background:var(--soft);border:1px solid var(--line);border-radius:12px}
#pv{display:block;cursor:pointer;width:auto;height:auto;max-width:100%;max-height:58vh;touch-action:none;cursor:grab;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.18)}
.photo-actions{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}.photo-band{margin:4px 0 16px}.photo-band .row2{margin-top:10px}
.chk{display:flex;align-items:center;gap:10px;font-weight:600;font-size:15px;cursor:pointer}.chk input{width:20px;height:20px;accent-color:var(--gold)}
input[type=range]{width:100%;accent-color:var(--gold)}
input,select{width:100%;font:16px var(--body);min-height:46px;padding:10px 12px;border:1px solid light-dark(#cfcfca,#3a3d43);border-radius:10px;background:var(--surface);color:var(--ink)}
input:focus,select:focus{outline:2px solid var(--focus);outline-offset:0;border-color:transparent}
button:focus-visible,a:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.row2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px}
.row3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.seg{display:flex;gap:0;padding:3px;background:var(--soft);border:1px solid var(--line);border-radius:11px}
.seg button{flex:1 1 0;font:600 14.5px var(--body);min-height:40px;padding:0 10px;border:0;background:transparent;color:var(--mute);border-radius:8px;cursor:pointer}
.seg button[aria-pressed=true]{background:var(--surface);color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.12)}
.check{display:flex;gap:10px;align-items:center;font-size:14.5px;font-weight:500}.check input{width:20px;min-height:20px;accent-color:var(--gold)}
.big{font:750 clamp(32px,5vw,46px)/1.1 var(--body);letter-spacing:-.025em;margin:6px 0 4px;font-variant-numeric:tabular-nums;overflow-wrap:anywhere}
.big.pop{animation:pop .35s ease-out}
@keyframes pop{from{opacity:.4}to{opacity:1}}
.big-label{font-size:13px;font-weight:600;color:var(--mute)}
.lines{margin:16px 0 0;padding:0;list-style:none;border-top:1px solid var(--line)}
.lines li{display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-size:14.5px}
.lines li b{font-weight:650;font-variant-numeric:tabular-nums;white-space:nowrap}
.lines li.total{border-bottom:0;font-size:16px}.lines li.total b{font-size:17px}
.formula{font-size:13px;color:var(--mute);margin-top:12px}
.warn{font-size:14px;color:var(--dn);margin-top:8px}
.up{color:var(--up)}.dn{color:var(--dn)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:42px;padding:0 16px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font:600 14.5px var(--body);cursor:pointer;text-decoration:none}
.btn.primary{background:var(--gold);border-color:var(--gold);color:#15171a}
.fig{position:relative;height:240px;margin-top:14px}.fig svg{position:absolute;inset:0;width:100%;height:100%}
.bars{display:grid;gap:8px;margin-top:14px}
.bars div{display:grid;grid-template-columns:7.5em minmax(0,1fr) auto;gap:10px;align-items:center;font-size:13.5px}
.bars i{display:block;height:10px;border-radius:5px;background:var(--gold)}
.bars b{font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap}
article{max-width:72ch}
article p,article li{line-height:1.7}
.sources{margin-top:28px;padding:16px 18px;border:1px solid var(--line);border-radius:12px;background:var(--surface);font-size:14px}
.sources b{display:block;margin-bottom:4px}.sources ul{margin:0;padding-left:18px}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;font-size:14.5px}
th{text-align:left;font-weight:600;color:var(--mute);border-bottom:1px solid var(--line);padding:8px 6px;font-size:13px}
td{border-bottom:1px solid var(--line);padding:9px 6px}td.n,th.n{text-align:right;white-space:nowrap}
.faq details{border-bottom:1px solid var(--line);padding:14px 0}
.faq summary{cursor:pointer;font-weight:600;list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::after{content:"+";color:var(--mute);font-size:20px;line-height:1}
.faq details[open] summary::after{content:"–"}
.faq details p{margin:8px 0 0;color:var(--mute)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.card{display:flex;gap:12px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px;text-decoration:none;color:var(--ink);transition:border-color .2s,box-shadow .2s}
.card:hover{border-color:light-dark(#c9c9c3,#44474e);box-shadow:0 4px 14px -8px rgba(0,0,0,.2)}
.card .ic{flex:none;display:grid;place-items:center;width:38px;height:38px;border-radius:10px;background:var(--soft);color:var(--gold-ink)}
.card .ic svg{width:20px;height:20px}
.card b{display:block;font-size:15.5px;font-weight:650;line-height:1.3;margin-bottom:2px}.card span{font-size:13.5px;color:var(--mute);line-height:1.4}
.tag{display:inline-block;font-size:11.5px;font-weight:700;color:#15171a;background:var(--gold);border-radius:6px;padding:1px 6px;margin-left:6px;vertical-align:2px}
.group-title{font-size:19px;font-weight:700;margin:34px 0 12px}
.hero{padding:40px 0 10px}
.hero h1{font-size:clamp(30px,5vw,44px)}
.hero .search{max-width:620px;margin-top:18px}.hero .search input{min-height:54px;font-size:17px;border-radius:12px;padding-left:44px;background:var(--surface)}
.hero .search svg{left:15px;width:18px;height:18px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chips a{font-size:14px;padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink);text-decoration:none}
.related{margin-top:44px}.related ul{padding-left:20px}
.stall{margin:32px 0;border:1px dashed var(--line);border-radius:12px;padding:10px 14px 14px;background:transparent}
.stall-in{display:block}
.stall-label{font-size:11.5px;letter-spacing:.02em;color:var(--mute);margin-bottom:6px}
.stall-body{min-height:70px;display:grid;place-items:center}
.stall:has(ins[data-ad-status=unfilled]){display:none}
.house{display:grid;gap:2px;text-align:center;padding:6px}
.house b{font-weight:650;font-size:15px}.house span{font-size:13.5px;color:var(--mute)}
.share{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:14px 0 0}
.share>span{font-size:13.5px;color:var(--mute);margin-right:4px}
.share a,.share button{display:inline-flex;align-items:center;gap:7px;min-height:40px;padding:0 14px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font:600 14px var(--body);text-decoration:none;cursor:pointer}
.share .wa{background:#25d366;border-color:#25d366;color:#07301a}
.share svg{width:17px;height:17px}
.fb{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:22px;font-size:14px;color:var(--mute)}
.install{display:none}.install.show{display:flex}
footer.site{margin-top:64px;padding:28px 0 40px;color:var(--mute);font-size:14px;border-top:1px solid var(--line);background:var(--surface)}
footer.site nav{display:flex;flex-wrap:wrap;gap:4px 18px;margin-bottom:10px}footer.site a{color:var(--mute)}
.scroll{overflow-x:auto}
@media(max-width:760px){.tool{grid-template-columns:minmax(0,1fr)}.result{border-left:0;border-top:1px solid var(--line)}header nav{display:none}.search{order:3;flex-basis:100%;max-width:none}}
@media(max-width:600px){table{font-size:13px}.stack thead{display:none}.stack tr{display:grid;padding-block:10px}.stack td{display:flow-root;border:0;padding:3px 0;padding-inline-start:8em;text-align:start;white-space:normal}.stack td::before{content:attr(data-l);float:inline-start;width:7.5em;margin-inline-start:-8em;color:var(--mute)}.stack td:empty{display:none}.row3{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
@media(max-width:420px){.row2{grid-template-columns:minmax(0,1fr)}}
@media print{header.top,footer.site,.stall,.share,.fb,.related,.faq,.install{display:none!important}.tool{box-shadow:none}body{background:#fff}}

/* ---- Motion & ambience ---- */
@view-transition{navigation:auto}
::view-transition-old(root){animation:vt-out .22s ease both}::view-transition-new(root){animation:vt-in .32s cubic-bezier(.2,.7,.2,1) both}
@keyframes vt-out{to{opacity:0;transform:translateY(-6px)}}@keyframes vt-in{from{opacity:0;transform:translateY(8px)}}
body::before,body::after{content:"";position:fixed;z-index:-1;pointer-events:none;border-radius:50%;will-change:transform}
body::before{width:72vmax;height:72vmax;left:-22vmax;top:-30vmax;background:radial-gradient(closest-side,light-dark(rgba(245,195,0,.30),rgba(245,195,0,.13)),transparent 72%);animation:drift-a 38s ease-in-out infinite alternate}
body::after{width:64vmax;height:64vmax;right:-24vmax;top:8vmax;background:radial-gradient(closest-side,light-dark(rgba(120,150,255,.22),rgba(110,140,255,.13)),transparent 72%);animation:drift-b 46s ease-in-out infinite alternate}
@keyframes drift-a{0%{transform:translate3d(0,0,0) scale(1)}50%{transform:translate3d(14vmax,8vmax,0) scale(1.12)}100%{transform:translate3d(4vmax,18vmax,0) scale(.95)}}
@keyframes drift-b{0%{transform:translate3d(0,0,0) scale(1)}50%{transform:translate3d(-12vmax,14vmax,0) scale(.92)}100%{transform:translate3d(-4vmax,-6vmax,0) scale(1.1)}}
.hero{position:relative}
.hero::before{content:"";position:absolute;inset:-40px -20vw 0;z-index:-1;pointer-events:none;background-image:radial-gradient(light-dark(rgba(21,23,26,.10),rgba(255,255,255,.08)) 1px,transparent 1.4px);background-size:22px 22px;-webkit-mask-image:radial-gradient(ellipse 60% 70% at 30% 30%,#000 10%,transparent 70%);mask-image:radial-gradient(ellipse 60% 70% at 30% 30%,#000 10%,transparent 70%);animation:grid-pan 60s linear infinite}
@keyframes grid-pan{to{background-position:220px 110px}}
.hero h1,.hero .lede,.hero .search,.hero .chips{animation:rise .7s cubic-bezier(.2,.7,.2,1) both}
.hero .lede{animation-delay:.08s}.hero .search{animation-delay:.16s}.hero .chips{animation-delay:.24s}
@keyframes rise{from{opacity:0;transform:translateY(14px)}}
.hero h1 em{font-style:normal;background:linear-gradient(90deg,var(--ink) 0%,var(--gold-ink) 45%,var(--ink) 90%);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:sheen 7s ease-in-out infinite}
@keyframes sheen{0%,100%{background-position:100% 0}50%{background-position:0 0}}
html.js .rv{opacity:0;transform:translateY(16px);transition:opacity .6s cubic-bezier(.2,.7,.2,1),transform .6s cubic-bezier(.2,.7,.2,1);transition-delay:var(--d,0s)}
html.js .rv.in{opacity:1;transform:none}
.card{transition:transform .25s cubic-bezier(.2,.7,.2,1),border-color .25s,box-shadow .25s,background .25s}
.card:hover{transform:translateY(-3px);border-color:light-dark(rgba(245,195,0,.65),rgba(245,195,0,.45));box-shadow:0 14px 30px -18px rgba(16,24,40,.35),0 0 0 3px light-dark(rgba(245,195,0,.12),rgba(245,195,0,.08))}
.card .ic{transition:background .25s,color .25s,transform .35s cubic-bezier(.2,.7,.2,1)}
.card:hover .ic{background:var(--gold);color:#15171a;transform:rotate(-6deg) scale(1.06)}
.btn{transition:transform .18s,box-shadow .2s,background .2s,border-color .2s;position:relative;overflow:hidden}
.btn:hover{transform:translateY(-1px);box-shadow:0 6px 16px -10px rgba(16,24,40,.45)}.btn:active{transform:translateY(0) scale(.98)}
.btn.primary::after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.55) 50%,transparent 70%);transform:translateX(-120%);transition:transform .7s ease}
.btn.primary:hover::after{transform:translateX(120%)}
.chips a{transition:transform .2s,border-color .2s,background .2s}.chips a:hover{transform:translateY(-2px);border-color:var(--gold)}
.tool{transition:box-shadow .35s,border-color .35s}
.tool:focus-within{border-color:light-dark(rgba(245,195,0,.6),rgba(245,195,0,.4));box-shadow:0 18px 40px -26px rgba(16,24,40,.45),0 0 0 4px light-dark(rgba(245,195,0,.10),rgba(245,195,0,.07))}
.result{position:relative}.result::before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,transparent,var(--gold),transparent);opacity:.8}
input,select{transition:border-color .2s,box-shadow .2s,background .2s}
header.top{transition:box-shadow .3s,background .3s}header.top.scrolled{box-shadow:0 8px 24px -18px rgba(16,24,40,.5)}
details{transition:background .2s}details[open] summary~*{animation:rise .35s cubic-bezier(.2,.7,.2,1) both}

@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
@media(prefers-reduced-motion:reduce){html.js .rv{opacity:1;transform:none}::view-transition-old(root),::view-transition-new(root){animation:none}}
"""

JS = r"""// Shared helpers: formatting, remembered inputs, year.
(() => {
  document.documentElement.classList.add('js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const h = document.querySelector('header.top');
  const onScroll = () => h && h.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (reduce || !('IntersectionObserver' in window)) return;
  const els = [...document.querySelectorAll('main .grid > *, main .tool, main .group-title, main article > h2, main article > h3, main .faq, main .stall, main .related > h2, main .install, main .share')];
  els.forEach(el => { el.classList.add('rv'); const g = el.parentElement; if (g && g.classList.contains('grid')) el.style.setProperty('--d', (([...g.children].indexOf(el) % 3) * 0.07) + 's'); });
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  els.forEach(el => { const r = el.getBoundingClientRect(); if (r.top < innerHeight) el.classList.add('in'); else io.observe(el); });
})();
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
  // site search (index built at deploy time)
  let IDX = null; const esc = x => String(x).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const load = () => IDX ? Promise.resolve(IDX) : fetch('/search-index.json').then(r => r.json()).then(j => (IDX = j));
  document.querySelectorAll('.search').forEach(box => {
    const inp = box.querySelector('input'), res = box.querySelector('.results'); let sel = 0;
    const run = () => load().then(ix => {
      const q = inp.value.trim().toLowerCase(); if (!q) { res.classList.remove('open'); return; }
      const ws = q.split(/\s+/);
      const hits = ix.map(it => { const hay = (it.t + ' ' + it.k + ' ' + it.d).toLowerCase(); let sc = 0; for (const w of ws) { if (!hay.includes(w)) return null; sc += it.t.toLowerCase().includes(w) ? 3 : 1; } return [sc + (it.c === 'Calculator' ? 1 : 0), it]; })
        .filter(Boolean).sort((a, b) => b[0] - a[0]).slice(0, 8).map(x => x[1]);
      sel = 0;
      res.innerHTML = hits.length ? hits.map((h, i) => `<a href="${h.u}"${i ? '' : ' class="sel"'}>${esc(h.t)}<small>${h.c} · ${esc(h.d)}</small></a>`).join('') : '<p>No matches. Try "gratuity", "gold", "EMI" or "lot size".</p>';
      res.classList.add('open');
    }).catch(() => {});
    inp.addEventListener('input', run);
    inp.addEventListener('focus', () => { load().catch(() => {}); if (inp.value) run(); });
    inp.addEventListener('keydown', e => {
      const as = [...res.querySelectorAll('a')];
      if ((e.key === 'ArrowDown' || e.key === 'ArrowUp') && as.length) { e.preventDefault(); as[sel] && as[sel].classList.remove('sel'); sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + as.length) % as.length; as[sel].classList.add('sel'); }
      if (e.key === 'Enter' && as[sel]) { e.preventDefault(); location.href = as[sel].href; }
      if (e.key === 'Escape') res.classList.remove('open');
    });
    document.addEventListener('click', e => { if (!box.contains(e.target)) res.classList.remove('open'); });
  });
  document.querySelectorAll('.print').forEach(b => b.addEventListener('click', () => { try { window.print(); } catch (e) {} }));
  document.querySelectorAll('.fb button').forEach(b => b.addEventListener('click', () => { b.parentElement.innerHTML = 'Thanks for the feedback. Spotted a mistake? Email contact@calcsouq.com.'; }));
})();
"""

VER = hashlib.md5((CSS + JS).encode()).hexdigest()[:8]

NAV = [("Calculators", "/#calculators"), ("Guides", "/guides/"), ("About", "/about/")]

SEARCH = ('<div class="search" role="search"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" d="M10.5 18a7.5 7.5 0 1 1 0-15 7.5 7.5 0 0 1 0 15zM16 16l5 5"/></svg>'
          '<input type="search" class="q" placeholder="Search calculators and guides" aria-label="Search calculators and guides" autocomplete="off"><div class="results" role="listbox"></div></div>')


def head(cfg, title, desc, path, keywords, jsonld, lang="en", alts=None):
    url = cfg["url"].rstrip("/") + path
    hl = "".join(f'<link rel="alternate" hreflang="{l}" href="{cfg["url"].rstrip("/") + p}">\n' for l, p in (alts or []))
    ads = ""
    if cfg["adsense"]:
        ads = ('<meta name="google-adsense-account" content="%s">\n'
               '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=%s" crossorigin="anonymous"></script>\n'
               % (cfg["adsense"], cfg["adsense"]))
    gsc = '<meta name="google-site-verification" content="%s">\n' % cfg["gsc"] if cfg.get("gsc") else ""
    ld = "".join('<script type="application/ld+json">%s</script>\n' % json.dumps(j, ensure_ascii=False) for j in jsonld)
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(keywords)}">
<link rel="canonical" href="{e(url)}">
{hl}<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{cfg["url"].rstrip("/")}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="apple-touch-icon" href="/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="CalcSouq">
{gsc}{ads}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"></noscript>
<link rel="stylesheet" href="/assets/site.css?v={VER}">
{ld}</head>
<body>
<header class="top"><div class="wrap">
<a class="logo" href="/" aria-label="CalcSouq home"><i>C</i>CalcSouq</a>
{SEARCH}
<nav aria-label="Main">{''.join(f'<a href="{h}">{n}</a>' for n, h in NAV)}</nav>
</div></header>
"""


AD = {"client": "", "slot": ""}

HOUSE = ['<b>Advertise on CalcSouq</b><span>Reach people planning their money, work and applications. Get in touch via the Contact page.</span>',
         '<b>Advertise on CalcSouq</b><span>Reach people planning their money, work and applications. Get in touch via the Contact page.</span>']
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
<nav aria-label="Footer"><a href="/#calculators">All calculators</a><a href="/guides/">Guides</a><a href="/templates/">Templates</a><a href="/ml/" lang="ml">മലയാളം</a><a href="/about/">About</a><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms</a><a href="/contact/">Contact</a></nav>
<p>© <span class="yr">2026</span> {SITE_NAME}. Results are estimates for general information, not legal, tax or investment advice. Found a mistake? Email contact@calcsouq.com.</p>
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
            '<button type="button" class="copy"><span hidden></span>Copy link</button>'
            '<button type="button" class="print">Print</button></div>')

def feedback():
    return '<div class="fb">Was this calculator useful? <button type="button" class="btn">Yes</button><button type="button" class="btn">No</button></div>'

ICONS = {
 "photo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="15" rx="2"/><circle cx="12" cy="12.5" r="3.5"/><path d="M8 5l1.5-2h5L16 5"/></svg>',
 "uae": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18"/></svg>',
 "trading": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20h18M5 16l4-5 4 3 6-8"/><path d="M15 6h4v4"/></svg>',
 "india": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>',
 "gold": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M4 18l2.5-6h11L20 18zM7.5 12L10 6h4l2.5 6"/></svg>',
 "money": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9.5v5M18 9.5v5"/></svg>',
 "guide": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5a2 2 0 0 1 2-2h12v18H6a2 2 0 0 1-2-2z"/><path d="M8 7h6M8 11h6"/></svg>',
}

