# Worldwide property buying cost calculator: country (and Indian state) presets, every rate editable.
from tools_qr import TOOLS

TOOLS.append(dict(
group="india", slug="property-buying-cost-calculator", unique=True, icon="india",
name="Property Buying Cost Calculator",
title="Property Buying Cost Calculator: Stamp Duty, Registration & Fees by Country and State",
desc="Total cost of buying a home or plot: stamp duty, registration, transfer tax, agent and legal fees, plus optional construction. India (state by state, including Kerala), UAE, UK, China, Russia and others.",
keywords="property buying cost calculator, stamp duty calculator, registration charges calculator, stamp duty by state india, kerala registration charges, dubai dld fee calculator, uk stamp duty calculator, china deed tax calculator, house buying costs",
h1="Property buying cost calculator",
lede="Choose the country (and state in India). The calculator fills in the usual government charges and fees, and adds construction if you are building. Every rate can be changed.",
card="Stamp duty, registration and fees for your country",
sources=[("Kerala Registration Department", "https://keralaregistration.gov.in/"), ("Dubai Land Department", "https://dubailand.gov.ae/"),
         ("GOV.UK: Stamp Duty Land Tax rates", "https://www.gov.uk/stamp-duty-land-tax/residential-property-rates"), ("Rosreestr (Russia)", "https://rosreestr.gov.ru/")],
tool="""
<div class="inputs">
 <div class="row2"><div><label for="ctry">Country</label><select id="ctry">
  <option value="IN">India</option><option value="AE">United Arab Emirates (Dubai)</option><option value="GB">United Kingdom (England)</option>
  <option value="CN">China</option><option value="RU">Russia</option><option value="XX">Other country</option></select></div>
 <div id="stw"><label for="st">State</label><select id="st">
  <option value="KL">Kerala</option><option value="MH">Maharashtra</option><option value="KA">Karnataka</option><option value="TN">Tamil Nadu</option>
  <option value="DL">Delhi</option><option value="UP">Uttar Pradesh</option><option value="GJ">Gujarat</option><option value="OT">Other state</option></select></div></div>
 <div class="row2"><div id="byw"><label for="by">Buyer</label><select id="by"></select></div>
 <div id="arw"><label for="ar">Floor area (m²)</label><input id="ar" inputmode="decimal" value="90"></div></div>
 <div class="row2"><div><label for="pr">Purchase price (<span class="cur">₹</span>)</label><input id="pr" inputmode="decimal" value="5000000"></div>
 <div id="gvw"><label for="gv">Government value (<span class="cur">₹</span>)</label><input id="gv" inputmode="decimal" value="0"><div class="hint">Fair, circle or guideline value. Duty is charged on the higher figure. 0 = same as price.</div></div></div>
 <div class="row3"><div><label for="t1" id="t1l">Stamp duty %</label><input id="t1" inputmode="decimal"></div><div><label for="t2" id="t2l">Registration %</label><input id="t2" inputmode="decimal"></div><div><label for="fx">Fixed government fees (<span class="cur">₹</span>)</label><input id="fx" inputmode="decimal"></div></div>
 <div class="row2"><div><label for="ag">Agent / broker %</label><input id="ag" inputmode="decimal"></div><div><label for="lg">Legal, notary & documents (<span class="cur">₹</span>)</label><input id="lg" inputmode="decimal"></div></div>
 <details class="build"><summary>Building a house too? Add construction</summary>
 <div class="row2"><div><label for="ba">Built-up area (sq ft)</label><input id="ba" inputmode="decimal" value="0"></div><div><label for="bc">Cost per sq ft (<span class="cur">₹</span>)</label><input id="bc" inputmode="decimal" value="2500"></div></div>
 <div><label for="bx">Permits, connections, wall & gate (<span class="cur">₹</span>)</label><input id="bx" inputmode="decimal" value="0"></div></details>
 <p class="hint" id="note"></p>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Total cost</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <div class="bars" id="bars"></div>
</div>""",
js=r"""
const IN_ST = { KL: [8, 8, 2, 0], MH: [6, 5, 1, 30000], KA: [5, 5, 1, 0], TN: [7, 7, 2, 0], DL: [6, 4, 1, 0], UP: [7, 6, 1, 0], GJ: [4.9, 4.9, 1, 0], OT: [6, 6, 1, 0] };
const C = {
  IN: { cur: '₹', loc: 'en-IN', price: 5000000, ag: 1, lg: 20000, fx: 0, buyers: [['m', 'Man'], ['w', 'Woman'], ['j', 'Joint (man and woman)']], unit: 'sq ft', bc: 2500,
        note: 'Typical rates for a residential sale deed. States change rates, cesses and women’s concessions; confirm with your state registration department or sub-registrar before paying.' },
  AE: { cur: 'AED ', loc: 'en-AE', price: 1500000, ag: 2.1, lg: 0, fx: 580, t1: 4, t2: 0, l1: 'DLD transfer fee %', l2: 'Other %', unit: 'sq ft', bc: 350,
        note: 'Dubai: 4% DLD transfer fee, about AED 580 admin and title deed fees, and a trustee office fee of AED 2,000 (under AED 500,000) or AED 4,000 plus 5% VAT, added automatically. Agent 2% + VAT is common. Other emirates differ.' },
  GB: { cur: '£', loc: 'en-GB', price: 350000, ag: 0, lg: 1800, fx: 0, buyers: [['h', 'Home mover (only home)'], ['f', 'First-time buyer'], ['a', 'Additional property']], t2: 0, l1: 'Extra SDLT %', l2: 'Other %', unit: 'sq ft', bc: 200,
        note: 'England and Northern Ireland Stamp Duty Land Tax bands from April 2025: 0% to £125,000, 2% to £250,000, 5% to £925,000, 10% to £1.5m, 12% above. First-time buyers pay 0% to £300,000 and 5% to £500,000 (no relief above £500,000). Additional properties pay 5% more on every band. Non-UK residents pay 2% more: add it in Extra SDLT %. Scotland and Wales use different taxes.' },
  CN: { cur: '¥', loc: 'zh-CN', price: 3000000, ag: 1, lg: 0, fx: 0, buyers: [['1', 'First home'], ['2', 'Second home']], t2: 0, l1: 'Deed tax %', l2: 'Other %', unit: 'm²', bc: 2500, area: 1,
        note: 'Deed tax since 1 Dec 2024: 1% for first and second homes up to 140 m²; above 140 m², 1.5% for a first home and 2% for a second. Rules for third homes, commercial property and local purchase limits differ by city.' },
  RU: { cur: '₽', loc: 'ru-RU', price: 9000000, ag: 0, lg: 0, fx: 2000, t1: 0, t2: 0, l1: 'Transfer tax %', l2: 'Notary %', unit: 'm²', bc: 60000,
        note: 'Russia has no transfer tax for buyers. The main government charge is the Rosreestr state duty of 2,000 roubles for an individual. A notary is needed only for some deals (for example shared ownership or a minor owner). Agent fees of 2–5% are agreed privately.' },
  XX: { cur: '', loc: undefined, price: 300000, ag: 2, lg: 2000, fx: 0, t1: 3, t2: 1, l1: 'Transfer tax / stamp duty %', l2: 'Registration %', unit: 'sq ft', bc: 150,
        note: 'Enter the rates for your country. Ask a local notary, lawyer or land registry for the current figures.' }
};
const TZ = { 'Asia/Dubai': 'AE', 'Asia/Muscat': 'AE', 'Europe/London': 'GB', 'Asia/Kolkata': 'IN', 'Asia/Calcutta': 'IN', 'Asia/Shanghai': 'CN', 'Asia/Chongqing': 'CN', 'Europe/Moscow': 'RU' };
const LG = { hi: 'IN', ml: 'IN', zh: 'CN', ru: 'RU' };
let cur = C.IN;
const M = x => { const v = (Number.isFinite(x) ? x : 0).toLocaleString(cur.loc, { maximumFractionDigits: 0 }); return cur.cur === '₽' ? v + ' ₽' : cur.cur + v; };
const show = (id, on) => { $(id).hidden = !on; };
function setCountry(first) {
  const k = $('ctry').value; cur = C[k];
  document.querySelectorAll('.cur').forEach(s => s.textContent = cur.cur.trim() || '¤');
  show('stw', k === 'IN'); show('gvw', k === 'IN'); show('arw', !!cur.area); show('byw', !!cur.buyers);
  $('by').innerHTML = (cur.buyers || []).map(([v, n]) => `<option value="${v}">${n}</option>`).join('');
  $('t1l').textContent = cur.l1 || 'Stamp duty %'; $('t2l').textContent = cur.l2 || 'Registration %';
  $('ba').closest('details').querySelector('label').textContent = 'Built-up area (' + cur.unit + ')';
  $('bc').previousElementSibling.firstChild.textContent = 'Cost per ' + cur.unit + ' (';
  if (!first) { $('pr').value = cur.price; $('gv').value = 0; $('bc').value = cur.bc; $('bx').value = 0; }
  $('ag').value = cur.ag; $('lg').value = cur.lg; $('fx').value = cur.fx;
  $('note').textContent = cur.note; rates();
}
function rates() {
  const k = $('ctry').value, b = $('by').value;
  if (k === 'IN') { const s = IN_ST[$('st').value]; $('t1').value = b === 'w' ? s[1] : b === 'j' ? (s[0] + s[1]) / 2 : s[0]; $('t2').value = s[2]; }
  else if (k === 'GB') { $('t1').value = b === 'a' ? 5 : 0; }
  else if (k === 'CN') { $('t1').value = V('ar') <= 140 ? 1 : (b === '2' ? 2 : 1.5); }
  else { $('t1').value = cur.t1; $('t2').value = cur.t2; }
  if (k !== 'IN') $('t2').value = cur.t2;
  calc();
}
function sdlt(p, ftb) {
  if (ftb && p <= 500000) return Math.max(0, Math.min(p, 500000) - 300000) * 0.05;
  const B = [[125000, 0], [250000, 0.02], [925000, 0.05], [1500000, 0.10], [Infinity, 0.12]];
  let t = 0, lo = 0; for (const [hi, r] of B) { if (p > lo) t += (Math.min(p, hi) - lo) * r; lo = hi; } return t;
}
function calc() {
  const k = $('ctry').value, p = V('pr'), base = Math.max(p, k === 'IN' ? V('gv') : 0), parts = [];
  if (k === 'GB') {
    const ftb = $('by').value === 'f';
    parts.push(['Stamp Duty Land Tax', sdlt(p, ftb) + p * V('t1') / 100]);
  } else {
    parts.push([$('t1l').textContent.replace(' %', ''), base * V('t1') / 100]);
    let reg = base * V('t2') / 100; if (k === 'IN' && IN_ST[$('st').value][3]) reg = Math.min(reg, IN_ST[$('st').value][3]);
    parts.push([$('t2l').textContent.replace(' %', ''), reg]);
  }
  if (k === 'AE') parts.push(['Trustee office fee + VAT', (p < 500000 ? 2000 : 4000) * 1.05]);
  parts.push(['Fixed government fees', V('fx')], ['Agent / broker', p * V('ag') / 100], ['Legal, notary & documents', V('lg')]);
  const build = V('ba') * V('bc') + V('bx'); parts.push(['Construction', build]);
  const fees = parts.reduce((a, x) => a + x[1], 0) - build, tot = p + fees + build;
  $('out').textContent = M(tot);
  $('lines').innerHTML = [['Purchase price', p]].concat(parts).filter(x => x[1]).map(([a, v]) => `<li><span>${a}</span><b>${M(v)}</b></li>`).join('')
    + `<li><span>Costs on top of the price</span><b>${M(fees)} (${F(p ? fees / p * 100 : 0, 1)}%)</b></li>`;
  const bp = [['Price', p]].concat(parts).filter(x => x[1] > 0);
  $('bars').innerHTML = bp.map(([a, v]) => `<div><span>${a}</span><i style="width:${(v / tot * 100).toFixed(1)}%"></i><b>${F(v / tot * 100, 1)}%</b></div>`).join('');
}
$('ctry').addEventListener('change', () => setCountry(false));
$('st').addEventListener('change', rates); $('by').addEventListener('change', rates); $('ar').addEventListener('input', rates);
document.querySelectorAll('.inputs input').forEach(i => { if (i.id !== 'ar') i.addEventListener('input', calc); });
let d = LG[document.documentElement.lang] || TZ[(Intl.DateTimeFormat().resolvedOptions().timeZone || '')] || 'IN';
try { const q = new URLSearchParams(location.search).get('country'); if (q && C[q.toUpperCase()]) d = q.toUpperCase(); } catch (e) {}
$('ctry').value = d; if (d === 'IN' && document.documentElement.lang === 'ml') $('st').value = 'KL';
setCountry(false);
""",
body="""
<h2>What you pay on top of the price</h2>
<p>Almost every country charges something when a property changes hands, but the amounts differ a lot. The calculator starts from the usual figures for the country you pick and lets you change each one.</p>
<div class="scroll"><table><thead><tr><th>Country</th><th>Main government charge (buyer)</th><th>Other usual costs</th></tr></thead><tbody>
<tr><td>India</td><td>Stamp duty 4.9–8% + registration about 1–2%, set by each state, on the higher of price and government value</td><td>Broker about 1–2%, document writer or lawyer</td></tr>
<tr><td>UAE (Dubai)</td><td>4% DLD transfer fee + about AED 580 admin + trustee fee</td><td>Agent 2% + VAT</td></tr>
<tr><td>UK (England)</td><td>Stamp Duty Land Tax in bands from 0% to 12%</td><td>Solicitor, survey</td></tr>
<tr><td>China</td><td>Deed tax 1–2% for homes</td><td>Agent fee</td></tr>
<tr><td>Russia</td><td>State duty of 2,000 roubles</td><td>Notary (some deals), agent</td></tr></tbody></table></div>
<h3>India: state by state</h3>
<p>Stamp duty is a state subject, so the rate depends on where the property is. In Kerala it is 8% stamp duty plus 2% registration on the higher of the sale price and the fair value. Several states, such as Delhi, Maharashtra and Uttar Pradesh, charge less when a woman is the buyer. Pick the state and the buyer, then check the figure with your sub-registrar.</p>
<h3>Example</h3>
<p>A ₹50 lakh plot in Kerala with a fair value of ₹40 lakh: stamp duty 8% of ₹50 lakh = ₹4 lakh, registration 2% = ₹1 lakh, broker 1% = ₹50,000 and documents ₹20,000. Total about ₹55.7 lakh, or 11.4% above the price.</p>
<h3>United Kingdom example</h3>
<p>A £350,000 home bought by a home mover in England: 0% on the first £125,000, 2% on the next £125,000 (£2,500) and 5% on the last £100,000 (£5,000). Stamp Duty Land Tax is £7,500.</p>
<p>Rates and fees change. Treat the result as a planning estimate and confirm the final figures with the registrar, land department or your lawyer.</p>
""",
faqs=[("What are stamp duty and registration charges in Kerala?", "8% stamp duty and 2% registration fee on the higher of the sale price and the government fair value."),
      ("Which Indian states charge less stamp duty for women?", "Several, including Delhi, Maharashtra and Uttar Pradesh. Choose 'Woman' as the buyer to apply the usual concession, and confirm with your state department."),
      ("How much does it cost to buy property in Dubai?", "About 4% DLD transfer fee, around AED 580 in admin fees and a trustee fee of AED 2,000–4,000 plus VAT, plus 2% agent fee if you use one."),
      ("Is there stamp duty when buying a flat in Russia?", "No. Buyers pay a state registration duty of 2,000 roubles for an individual, plus any notary and agent fees.")]))
