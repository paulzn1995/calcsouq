from tools_india import TOOLS

# ---------------- UAE: leave encashment ----------------
TOOLS.append(dict(
group="uae", slug="uae-leave-encashment-calculator",
name="UAE Leave Encashment Calculator",
title="UAE Leave Encashment Calculator: Unused Annual Leave Pay (2026)",
desc="Calculate payment for unused annual leave in the UAE under Federal Decree-Law 33 of 2021: based on basic salary, including leave earned in your final part year.",
keywords="leave encashment calculator uae, unused leave salary uae, annual leave encashment dubai, leave salary calculator uae, final settlement leave calculation, mohre leave calculation",
h1="UAE leave encashment calculator",
lede="Work out what you should be paid for unused annual leave when you leave a job in the UAE, or when your employer pays leave in cash.",
card="Pay for unused annual leave, on basic salary",
tool="""
<div class="inputs">
 <div><label for="basic">Basic monthly salary (AED)</label><input id="basic" inputmode="decimal" value="8000"><div class="hint">Leave encashment uses basic salary only.</div></div>
 <div class="row2"><div><label for="carried">Unused days from earlier years</label><input id="carried" inputmode="decimal" value="10"></div>
 <div><label for="months">Months worked in final year</label><input id="months" inputmode="decimal" value="6"><div class="hint">Earns 30 days ÷ 12 per month.</div></div></div>
 <div><label for="taken">Leave already taken this year (days)</label><input id="taken" inputmode="decimal" value="5"></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Leave encashment</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p class="formula">Pay = (basic ÷ 30) × unused days. Your contract may give more than the law's 30 days.</p>
</div>""",
js=r"""
function calc() {
  const b = V('basic'), daily = b / 30, earned = Math.min(V('months'), 12) * 2.5, days = Math.max(V('carried') + earned - V('taken'), 0);
  $('out').textContent = 'AED ' + F(daily * days);
  $('lines').innerHTML = [['Daily basic wage', 'AED ' + F(daily)], ['Leave earned this year', F(earned, 1) + ' days'], ['Unused days to be paid', F(days, 1) + ' days']].map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
}
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>How unused leave is paid in the UAE</h2>
<p>Private-sector employees earn <strong>30 calendar days of paid annual leave</strong> for each year of service. When your employment ends, you are entitled to be paid for every unused day, including leave earned in your final, incomplete year, and the payment is calculated on your <strong>basic salary</strong> (Article 29 of Federal Decree-Law No. 33 of 2021 and Article 19 of Cabinet Resolution No. 1 of 2022).</p>
<h3>Worked example</h3>
<p>Basic salary AED 8,000 → daily wage AED 266.67. You carried 10 unused days, worked 6 months of the final year (earning 15 days) and took 5 days. Unused days = 10 + 15 − 5 = 20. Payment = 266.67 × 20 = <strong>AED 5,333</strong>.</p>
<h3>Carrying leave forward</h3>
<p>During employment you can usually carry forward up to half of your annual leave to the next year, or agree with your employer to be paid for it. Your employer cannot stop you from taking accrued leave for more than two years unless you choose to carry it over or be paid instead.</p>
<h3>Leave pay vs leave encashment</h3>
<p>When you <em>take</em> annual leave, you receive your normal wage for those days. When unused leave is <em>encashed</em>, the law uses basic salary. Some contracts are more generous, and the better terms apply.</p>
""",
faqs=[("Is leave encashment calculated on basic or gross salary in UAE?", "On basic salary, under Article 19 of Cabinet Resolution No. 1 of 2022."),
      ("Do I get paid for unused leave if I resign?", "Yes. Unused leave, including leave earned in your final part year, must be paid when your service ends."),
      ("How many annual leave days do UAE employees get?", "30 calendar days for each completed year of service, earned pro rata in a part year.")]))

# ---------------- Gold units ----------------
GU = [("g", "Grams", 1), ("tola", "Tola", 11.6638), ("pavan", "Pavan (sovereign)", 8), ("ozt", "Troy ounce", 31.1035), ("kg", "Kilogram", 1000)]
gu_opts = "".join(f'<option value="{k}"{" selected" if k=="tola" else ""}>{n}</option>' for k, n, _ in GU)
GUJS = "{" + ",".join(f'{k}:["{n}",{f}]' for k, n, f in GU) + "}"
TOOLS.append(dict(
group="uae", slug="gold-tola-pavan-converter",
name="Gold Tola & Pavan Converter",
title="Tola to Gram & Pavan to Gram Converter: Gold Weight and Value",
desc="Convert gold between tola, pavan (sovereign), grams, troy ounces and kilograms, and see the value at your gram rate. 1 tola = 11.66 g, 1 pavan = 8 g.",
keywords="tola to gram, 1 tola gold in grams, pavan to gram, 1 pavan gold, sovereign gold grams, gold tola price dubai, troy ounce to gram, gold weight converter",
h1="Gold tola and pavan converter",
lede="Convert gold weights used in Dubai, India and Kerala, and value them at today's rate.",
card="Tola, pavan, grams and troy ounces",
tool=f"""
<div class="inputs">
 <div class="row2"><div><label for="val">Weight</label><input id="val" inputmode="decimal" value="1"></div><div><label for="unit">Unit</label><select id="unit">{gu_opts}</select></div></div>
 <div><label for="rate">Gold rate per gram (optional)</label><input id="rate" inputmode="decimal" value=""><div class="hint">Enter today's rate in AED or ₹ to see the value.</div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">In grams</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
</div>""",
js=r"""
const U = """ + GUJS + r""";
function calc() {
  const g = V('val') * U[$('unit').value][1], r = V('rate');
  $('out').textContent = F(g, 3) + ' g';
  const rows = Object.entries(U).filter(([k]) => k !== 'g' && k !== $('unit').value).map(([k, [n, f]]) => [n, F(g / f, 4)]);
  if (r) rows.push(['Value at your rate', F(g * r)]);
  $('lines').innerHTML = rows.map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
}
document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>Gold weight units</h2>
<div class="scroll"><table><thead><tr><th>Unit</th><th class="n">Grams</th><th>Where it's used</th></tr></thead><tbody>
<tr><td>1 tola</td><td class="n">11.664</td><td>Dubai gold souq, India, Pakistan</td></tr>
<tr><td>1 pavan (sovereign)</td><td class="n">8</td><td>Kerala and Tamil Nadu jewellery</td></tr>
<tr><td>1 troy ounce</td><td class="n">31.103</td><td>International gold price (XAU/USD)</td></tr>
<tr><td>10 tola bar (TT bar)</td><td class="n">116.64</td><td>Popular bar size in the Gulf</td></tr></tbody></table></div>
<h3>Quick answers</h3>
<ul><li>1 tola ≈ 1.458 pavan.</li><li>10 pavan = 80 g ≈ 6.86 tola.</li><li>1 troy ounce ≈ 2.667 tola.</li></ul>
<p>Prices quoted per tola or pavan are usually for a specific purity (24K or 22K). Make sure the gram rate you enter matches the purity you're valuing.</p>
""",
faqs=[("How many grams is 1 tola of gold?", "11.6638 grams."),
      ("How many grams is 1 pavan?", "8 grams. A pavan is also called a sovereign."),
      ("How many tola is a troy ounce?", "About 2.667 tola.")]))

# ---------------- EMI ----------------
TOOLS.append(dict(
group="uae", slug="loan-emi-calculator",
name="Loan EMI Calculator (AED & ₹)",
title="EMI Calculator: Car, Personal & Home Loan EMI in AED or INR",
desc="Calculate your monthly EMI, total interest and total payment for any loan in AED or rupees. Works for UAE personal and car loans and Indian home loans.",
keywords="emi calculator, loan emi calculator uae, personal loan calculator dubai, car loan calculator uae, home loan emi calculator india, emi calculator aed, reducing balance emi",
h1="Loan EMI calculator",
lede="See your monthly instalment, total interest and total cost for a reducing-balance loan.",
card="Monthly instalment and total interest",
tool="""
<div class="inputs">
 <div><label>Currency</label><div class="seg" id="cur"><button type="button" data-v="AED " aria-pressed="true">AED</button><button type="button" data-v="₹" aria-pressed="false">₹ INR</button></div></div>
 <div><label for="amt">Loan amount</label><input id="amt" inputmode="decimal" value="100000"></div>
 <div class="row2"><div><label for="rate">Interest rate (% per year)</label><input id="rate" inputmode="decimal" value="6.5"><div class="hint">Use the reducing-balance rate.</div></div>
 <div><label for="yrs">Tenure (years)</label><input id="yrs" inputmode="decimal" value="4"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Monthly EMI</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p class="formula">EMI = P × r × (1 + r)ⁿ ÷ ((1 + r)ⁿ − 1), where r is the monthly rate and n the number of months.</p>
</div>""",
js=r"""
const cur = seg('cur', () => calc());
function calc() {
  const P = V('amt'), r = V('rate') / 1200, n = Math.round(V('yrs') * 12), c = cur();
  const emi = !n ? 0 : r ? P * r * (1 + r) ** n / ((1 + r) ** n - 1) : P / n, tot = emi * n;
  const d = c === '₹' ? 0 : 2;
  $('out').textContent = c + F(emi, d);
  $('lines').innerHTML = [['Months', n], ['Total interest', c + F(tot - P, d)], ['Total payment', c + F(tot, d)], ['Interest as % of loan', F(P ? (tot - P) / P * 100 : 0, 1) + '%']].map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
}
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>How EMI is calculated</h2>
<p>An EMI (equated monthly instalment) repays a loan in equal monthly amounts. Early instalments are mostly interest; later ones mostly repay the principal. This calculator uses the standard <strong>reducing-balance</strong> formula used by banks in the UAE and India.</p>
<h3>Flat rate vs reducing rate</h3>
<p>Some UAE car and personal loans are advertised at a <strong>flat rate</strong>, where interest is charged on the original amount for the whole term. A flat rate costs much more than the same number as a reducing rate, often close to double. Ask the bank for the reducing-balance rate (or APR) and enter that here.</p>
<h3>Ways to pay less interest</h3>
<ul><li>Choose a shorter tenure if the EMI is affordable.</li><li>Make part-prepayments, checking any early settlement fee first.</li><li>Compare offers by total interest, not just the monthly figure.</li></ul>
""",
faqs=[("What is the EMI on a 100,000 loan at 6.5% for 4 years?", "About 2,371 per month, with total interest of around 13,800."),
      ("What is the difference between flat and reducing interest?", "A flat rate charges interest on the full original loan for the whole term; a reducing rate charges interest only on the balance still owed, so it costs less for the same headline rate.")]))

# ---------------- Risk-reward ----------------
TOOLS.append(dict(
group="trading", slug="risk-reward-calculator",
name="Risk–Reward Calculator",
title="Risk Reward Ratio Calculator: R-Multiple and Breakeven Win Rate",
desc="Enter entry, stop loss and take profit to get your risk–reward ratio, R-multiple and the win rate you need to break even. Works for forex, gold, indices and stocks.",
keywords="risk reward calculator, risk reward ratio, r multiple calculator, breakeven win rate, stop loss take profit calculator, trading risk reward forex gold",
h1="Risk–reward calculator",
lede="Check whether a trade is worth taking before you place it.",
card="R-multiple and breakeven win rate",
tool="""
<div class="inputs">
 <div><label>Direction</label><div class="seg" id="dir"><button type="button" data-v="long" aria-pressed="true">Long (buy)</button><button type="button" data-v="short" aria-pressed="false">Short (sell)</button></div></div>
 <div><label for="en">Entry price</label><input id="en" inputmode="decimal" value="2650"></div>
 <div class="row2"><div><label for="sl">Stop loss</label><input id="sl" inputmode="decimal" value="2640"></div><div><label for="tp">Take profit</label><input id="tp" inputmode="decimal" value="2675"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Risk : reward</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p class="formula" id="msg"></p>
</div>""",
js=r"""
const dir = seg('dir', () => calc());
function calc() {
  const s = dir() === 'long' ? 1 : -1, risk = (V('en') - V('sl')) * s, rew = (V('tp') - V('en')) * s;
  if (risk <= 0 || rew <= 0) { $('out').textContent = '—'; $('lines').innerHTML = ''; $('msg').textContent = dir() === 'long' ? 'For a long trade, stop loss must be below entry and take profit above it.' : 'For a short trade, stop loss must be above entry and take profit below it.'; return; }
  const R = rew / risk, be = 1 / (1 + R) * 100;
  $('out').textContent = '1 : ' + F(R, 2);
  $('lines').innerHTML = [['Risk per unit', FX(risk, 4).replace(/\.?0+$/, '')], ['Reward per unit', FX(rew, 4).replace(/\.?0+$/, '')], ['Breakeven win rate', F(be, 1) + '%']].map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
  $('msg').textContent = `You need to win more than ${F(be, 0)}% of trades like this to profit, before costs.`;
}
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>What risk–reward tells you</h2>
<p>Risk–reward compares how much you could lose (entry to stop loss) with how much you could gain (entry to take profit). A 1:2.5 trade risks 1 to make 2.5. This is often written as a <strong>2.5R</strong> target.</p>
<h3>Breakeven win rate</h3>
<p><strong>Breakeven win rate = 1 ÷ (1 + R)</strong>. At 1:1 you must win over 50% of trades; at 1:2, over 33%; at 1:3, over 25%. Spreads, commission and slippage push the real figure a little higher.</p>
<div class="scroll"><table><thead><tr><th>Risk : reward</th><th class="n">Breakeven win rate</th></tr></thead><tbody>
""" + "".join(f'<tr><td>1 : {r:g}</td><td class="n">{100/(1+r):.1f}%</td></tr>' for r in (0.5, 1, 1.5, 2, 3, 4)) + """</tbody></table></div>
<p>Pair this with the <a href="/position-size-calculator/">position size calculator</a> so each trade risks only the amount you planned.</p>
""",
faqs=[("What is a good risk–reward ratio?", "Many traders look for at least 1:1.5 or 1:2, but what matters is the ratio together with your real win rate."),
      ("What win rate do I need at 1:2 risk–reward?", "More than 33.3% of trades, before trading costs.")]))
