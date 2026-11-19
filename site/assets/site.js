// Shared helpers: formatting, remembered inputs, year.
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
})();
