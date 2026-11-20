// Shared helpers: formatting, remembered inputs, year.
(() => {
  document.documentElement.classList.add('js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const h = document.querySelector('header.top');
  const onScroll = () => h && h.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (!reduce) {
  // Desktop ambience: drifting math symbols and parallax hero art
  if (innerWidth >= 900) {
    const fx = document.createElement('div'); fx.className = 'bgfx'; fx.setAttribute('aria-hidden', 'true');
    const sy = ['%', '+', '÷', '×', '=', '∑', '$', '€', '₹', '¥', '£', '√', 'π', '%', '+', '−', '∞', '¢'];
    sy.forEach((c, i) => { const e = document.createElement('span'); e.textContent = c;
      e.style.cssText = `left:${(i * 53 + 7) % 100}vw;--s:${18 + (i * 7) % 26}px;--t:${45 + (i * 11) % 40}s;--dl:-${(i * 13) % 60}s;--x:${((i % 5) - 2) * 6}vw;--r:${((i % 7) - 3) * 30}deg`;
      fx.appendChild(e); });
    document.body.appendChild(fx);
    const art = document.querySelector('.hero-art');
    if (art) {
      const ls = [...art.querySelectorAll('.pl')];
      addEventListener('pointermove', e => { const x = e.clientX / innerWidth - .5, y = e.clientY / innerHeight - .5;
        ls.forEach(l => { const d = +l.dataset.d || 10; l.style.transform = `translate(${x * d}px,${y * d}px)`; }); }, { passive: true });
      const keys = [...art.querySelectorAll('.key')]; let k = 0;
      setInterval(() => { keys.forEach(x => x.classList.remove('on')); if (keys.length) keys[(k = (k * 7 + 3) % keys.length)].classList.add('on'); }, 650);
    }
  }
  }
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
