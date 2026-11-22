# Calculators that people search for in Chinese and Russian: China salary tax, Russia NDFL salary,
# Russia property tax deduction, mortgage with annuity vs equal-principal repayment.
from tools_property import TOOLS

TABLE_CSS = ""

# ---------------- China: individual income tax on salary (个税) ----------------
TOOLS.append(dict(
group="uae", slug="china-income-tax-calculator", icon="money",
name="China Salary Income Tax Calculator",
title="China Income Tax Calculator 2026: Salary After Tax, Social Insurance & Special Deductions",
desc="Monthly take-home pay in China after individual income tax, social insurance and housing fund. Uses the 5,000 yuan threshold, 3–45% brackets, cumulative monthly withholding and the seven special additional deductions.",
keywords="china income tax calculator, china salary after tax, iit calculator china, china individual income tax 2026, five insurances one fund calculator, special additional deductions china",
h1="China salary income tax calculator",
lede="See tax withheld each month, take-home pay and the year's total, using China's cumulative withholding method.",
card="Take-home pay after tax and social insurance",
sources=[("State Taxation Administration", "https://www.chinatax.gov.cn/")],
tool="""
<div class="inputs">
 <div class="row2"><div><label for="g">Monthly salary before tax (¥)</label><input id="g" inputmode="decimal" value="20000"></div>
 <div><label for="b">Contribution base (¥)</label><input id="b" inputmode="decimal" value="0"><div class="hint">0 = same as salary. Cities set a minimum and maximum base.</div></div></div>
 <div class="row2"><div><label for="si">Social insurance, your share (%)</label><input id="si" inputmode="decimal" value="10.5"><div class="hint">Usually pension 8% + medical 2% + unemployment 0.5%.</div></div>
 <div><label for="hf">Housing fund, your share (%)</label><input id="hf" inputmode="decimal" value="12"><div class="hint">5–12%, set by your employer.</div></div></div>
 <div class="row2"><div><label for="ch">Children in education</label><input id="ch" inputmode="numeric" value="0"></div>
 <div><label for="inf">Children under 3</label><input id="inf" inputmode="numeric" value="0"></div></div>
 <div class="row2"><div><label for="old">Supporting parents aged 60+</label><select id="old"><option value="0">No</option><option value="3000">Yes, only child (3,000)</option><option value="1500">Yes, shared (up to 1,500)</option></select></div>
 <div><label for="home">Housing</label><select id="home"><option value="0">None</option><option value="1000">First-home loan interest (1,000)</option><option value="1500">Rent, large city (1,500)</option><option value="1100">Rent, mid-size city (1,100)</option><option value="800">Rent, smaller city (800)</option></select></div></div>
 <div class="row2"><div><label for="ce">Continuing education</label><select id="ce"><option value="0">None</option><option value="400">Degree study (400 a month)</option></select></div>
 <div><label for="oth">Other monthly deductions (¥)</label><input id="oth" inputmode="decimal" value="0"><div class="hint">e.g. private pension, enterprise annuity.</div></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Average take-home pay a month</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <div class="scroll"><table class="sched"><thead><tr><th>Month</th><th>Tax withheld</th><th>Take-home</th></tr></thead><tbody id="rows"></tbody></table></div>
</div>""",
js=r"""
const BR = [[36000, 0.03, 0], [144000, 0.10, 2520], [300000, 0.20, 16920], [420000, 0.25, 31920], [660000, 0.30, 52920], [960000, 0.35, 85920], [Infinity, 0.45, 181920]];
const tax = x => { if (x <= 0) return 0; for (const [hi, r, q] of BR) if (x <= hi) return x * r - q; return 0; };
const Y = x => '¥' + (Number.isFinite(x) ? x : 0).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
function calc() {
  const g = V('g'), base = V('b') || g, si = base * V('si') / 100, hf = base * V('hf') / 100, ins = si + hf;
  const sp = V('ch') * 2000 + V('inf') * 2000 + +$('old').value + +$('home').value + +$('ce').value + V('oth');
  let prev = 0, rows = '', totTax = 0;
  for (let m = 1; m <= 12; m++) {
    const cum = tax(m * (g - ins - 5000 - sp)), t = Math.max(0, cum - prev); prev = cum; totTax += t;
    rows += `<tr><td>${m}</td><td>${Y(t)}</td><td>${Y(g - ins - t)}</td></tr>`;
  }
  const net = g * 12 - ins * 12 - totTax;
  $('out').textContent = Y(net / 12);
  $('rows').innerHTML = rows;
  $('lines').innerHTML = [['Social insurance a month', Y(si)], ['Housing fund a month', Y(hf)], ['Special deductions a month', Y(sp)],
    ['Income tax for the year', Y(totTax)], ['Take-home for the year', Y(net)], ['Tax as % of salary', F(g ? totTax / (g * 12) * 100 : 0, 2) + '%']]
    .map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
}
document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>How salary tax is worked out in China</h2>
<p>Employers withhold tax each month using the <strong>cumulative method</strong>: from January, add up salary, minus 5,000 yuan a month, minus your social insurance and housing fund, minus special additional deductions. Tax on that running total uses the annual brackets, and each month you pay the difference from last month. That is why tax often rises later in the year as you move into a higher bracket.</p>
<div class="scroll"><table><thead><tr><th>Annual taxable income (¥)</th><th>Rate</th><th>Quick deduction (¥)</th></tr></thead><tbody>
<tr><td>Up to 36,000</td><td>3%</td><td>0</td></tr><tr><td>36,000–144,000</td><td>10%</td><td>2,520</td></tr><tr><td>144,000–300,000</td><td>20%</td><td>16,920</td></tr>
<tr><td>300,000–420,000</td><td>25%</td><td>31,920</td></tr><tr><td>420,000–660,000</td><td>30%</td><td>52,920</td></tr><tr><td>660,000–960,000</td><td>35%</td><td>85,920</td></tr><tr><td>Over 960,000</td><td>45%</td><td>181,920</td></tr></tbody></table></div>
<h3>Special additional deductions (per month)</h3>
<ul><li>Child education and children under 3: 2,000 yuan per child.</li><li>Supporting parents aged 60 or over: 3,000 yuan for an only child; siblings share 3,000, at most 1,500 each.</li>
<li>First-home loan interest 1,000 yuan, or rent 1,500, 1,100 or 800 yuan depending on city size.</li><li>Degree-level continuing education 400 yuan.</li></ul>
<h3>Example</h3><p>Salary 20,000 yuan, 22.5% social insurance and housing fund (4,500), no special deductions: taxable income is 10,500 a month, 126,000 a year. Tax for the year is 126,000 × 10% − 2,520 = 10,080 yuan, about 840 a month on average.</p>
<p>Contribution bases, caps and rates differ by city. Year-end bonuses can be taxed separately; this calculator covers monthly salary.</p>""",
faqs=[("What is the tax-free threshold in China?", "5,000 yuan a month (60,000 a year), before social insurance, housing fund and special additional deductions."),
      ("Why is my tax higher in later months?", "Withholding is cumulative. As your year-to-date taxable income crosses a bracket, the rate on new income goes up."),
      ("How much can I deduct for children?", "2,000 yuan a month per child in education, and 2,000 per child under 3. Parents can split it 50/50 or one parent takes 100%.")]))

# ---------------- Russia: NDFL on salary ----------------
TOOLS.append(dict(
group="uae", slug="russia-salary-tax-calculator", icon="money",
name="Russia Salary Tax (NDFL) Calculator",
title="Russia NDFL Calculator 2026: Salary After Tax with the 13–22% Progressive Scale",
desc="Net salary in Russia after personal income tax (NDFL) on the 2026 progressive scale: 13% up to 2.4 million roubles a year, then 15%, 18%, 20% and 22%. Includes child deductions and a month-by-month table.",
keywords="russia income tax calculator, ndfl calculator, russia salary after tax, progressive tax russia 2026, ndfl 13 15 percent",
h1="Russia salary tax (NDFL) calculator",
lede="Enter the salary before tax. See NDFL withheld each month as your income moves through the progressive scale, and what reaches your account.",
card="Net salary on the 13–22% scale",
sources=[("Federal Tax Service of Russia", "https://www.nalog.gov.ru/")],
tool="""
<div class="inputs">
 <div class="row2"><div><label for="g">Monthly salary before tax (₽)</label><input id="g" inputmode="decimal" value="250000"></div>
 <div><label for="bon">Annual bonus (₽)</label><input id="bon" inputmode="decimal" value="0"><div class="hint">Paid in December.</div></div></div>
 <div class="row2"><div><label for="k1">Children (first and second)</label><select id="k1"><option value="0">None</option><option value="1">One</option><option value="2">Two</option></select></div>
 <div><label for="k3">Third and further children</label><input id="k3" inputmode="numeric" value="0"></div></div>
 <p class="hint">Child deductions: 1,400 ₽ for the first, 2,800 ₽ for the second, 6,000 ₽ for each further child a month, until income since January passes 450,000 ₽.</p>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Net pay for the year</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <div class="scroll"><table class="sched"><thead><tr><th>Month</th><th>NDFL</th><th>Net pay</th></tr></thead><tbody id="rows"></tbody></table></div>
</div>""",
js=r"""
const BR = [[2400000, 0.13], [5000000, 0.15], [20000000, 0.18], [50000000, 0.20], [Infinity, 0.22]];
const nd = x => { let t = 0, lo = 0; for (const [hi, r] of BR) { if (x > lo) t += (Math.min(x, hi) - lo) * r; lo = hi; } return t; };
const R = x => Math.round(x).toLocaleString('ru-RU') + ' ₽';
function calc() {
  const g = V('g'), k1 = +$('k1').value, k3 = V('k3');
  const kid = (k1 >= 1 ? 1400 : 0) + (k1 >= 2 ? 2800 : 0) + k3 * 6000;
  let inc = 0, ded = 0, prev = 0, rows = '', tot = 0, net = 0;
  for (let m = 1; m <= 12; m++) {
    const pay = g + (m === 12 ? V('bon') : 0); inc += pay;
    if (inc <= 450000) ded += kid;
    const cum = Math.round(nd(Math.max(0, inc - ded))), t = cum - prev; prev = cum; tot += t; net += pay - t;
    rows += `<tr><td>${m}</td><td>${R(t)}</td><td>${R(pay - t)}</td></tr>`;
  }
  $('out').textContent = R(net); $('rows').innerHTML = rows;
  const top = BR.find(b => inc - ded <= b[0]);
  $('lines').innerHTML = [['Income for the year', R(inc)], ['NDFL for the year', R(tot)], ['Average net pay a month', R(net / 12)],
    ['Effective tax rate', F(inc ? tot / inc * 100 : 0, 2) + '%'], ['Top rate reached', (top ? top[1] * 100 : 22) + '%']]
    .map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
}
document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>The progressive NDFL scale</h2>
<p>Since 2025, salary is taxed on a five-step scale. Each rate applies only to the part of the year's income inside its band, counted from January.</p>
<div class="scroll"><table><thead><tr><th>Income for the year</th><th>Rate on that part</th><th>Tax at the top of the band</th></tr></thead><tbody>
<tr><td>Up to 2.4 million ₽</td><td>13%</td><td>312,000 ₽</td></tr><tr><td>2.4–5 million ₽</td><td>15%</td><td>702,000 ₽</td></tr><tr><td>5–20 million ₽</td><td>18%</td><td>3,402,000 ₽</td></tr>
<tr><td>20–50 million ₽</td><td>20%</td><td>9,402,000 ₽</td></tr><tr><td>Over 50 million ₽</td><td>22%</td><td>—</td></tr></tbody></table></div>
<h3>Example</h3><p>Salary 250,000 ₽ a month: 3 million ₽ a year. NDFL is 13% × 2.4 million + 15% × 600,000 = 312,000 + 90,000 = 402,000 ₽. NDFL is 32,500 ₽ a month until September. In October income since January passes 2.4 million ₽, so that month's NDFL is 34,500 ₽, and from November it is 37,500 ₽.</p>
<p>Different rules apply to some income, such as northern allowances, dividends and interest, and to non-residents. This calculator covers ordinary salary of a tax resident.</p>""",
faqs=[("What is the NDFL rate in 2026?", "13% on salary up to 2.4 million roubles a year, 15% from 2.4 to 5 million, 18% from 5 to 20 million, 20% from 20 to 50 million and 22% above."),
      ("Is the higher rate charged on my whole salary?", "No. Only the part of the year's income above each threshold is taxed at the higher rate.")]))

# ---------------- Russia: property tax deduction ----------------
TOOLS.append(dict(
group="india", slug="russia-property-tax-deduction-calculator", icon="india",
name="Russia Home Purchase Tax Refund Calculator",
title="Russia Property Tax Deduction Calculator: Refund for a Flat and Mortgage Interest",
desc="How much NDFL you can get back after buying a home in Russia: up to 2 million roubles of the price and 3 million of mortgage interest, at your NDFL rate, and how many years it takes.",
keywords="russia property tax deduction calculator, tax refund buying apartment russia, mortgage interest deduction russia, imushchestvenny vychet calculator",
h1="Russia home purchase tax refund calculator",
lede="Work out the refund for the purchase price and mortgage interest, and how long it takes when your yearly NDFL is the limit.",
card="Refund for the flat price and mortgage interest",
sources=[("Federal Tax Service: property deduction", "https://www.nalog.gov.ru/")],
tool="""
<div class="inputs">
 <div class="row2"><div><label for="pr">Price of the home (₽)</label><input id="pr" inputmode="decimal" value="8000000"><div class="hint">Your share, if bought with a spouse.</div></div>
 <div><label for="int">Mortgage interest paid (₽)</label><input id="int" inputmode="decimal" value="1500000"><div class="hint">Total so far or planned. 0 if no mortgage.</div></div></div>
 <div class="row2"><div><label for="inc">Salary for the year before tax (₽)</label><input id="inc" inputmode="decimal" value="1800000"></div>
 <div><label for="used">Deduction already used (₽)</label><input id="used" inputmode="decimal" value="0"><div class="hint">From an earlier purchase, out of the 2 million limit.</div></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Total refund</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <div class="scroll"><table class="sched"><thead><tr><th>Year</th><th>Refund</th><th>Deduction left</th></tr></thead><tbody id="rows"></tbody></table></div>
</div>""",
js=r"""
const BR = [[2400000, 0.13], [5000000, 0.15], [20000000, 0.18], [50000000, 0.20], [Infinity, 0.22]];
const nd = x => { let t = 0, lo = 0; for (const [hi, r] of BR) { if (x > lo) t += (Math.min(x, hi) - lo) * r; lo = hi; } return t; };
const R = x => Math.round(x).toLocaleString('ru-RU') + ' ₽';
function calc() {
  const inc = V('inc');
  let prop = Math.max(0, Math.min(V('pr'), 2000000 - V('used'))), intr = Math.min(V('int'), 3000000);
  const startP = prop, startI = intr;
  let y = 0, rows = '', tot = 0, rp = 0, ri = 0;
  while ((prop > 0 || intr > 0) && y < 40 && inc > 0) {
    y++; let room = inc;
    const dp = Math.min(prop, room); room -= dp; const di = Math.min(intr, room);
    const r1 = nd(inc) - nd(inc - dp), r2 = nd(inc - dp) - nd(inc - dp - di);
    prop -= dp; intr -= di; rp += r1; ri += r2; tot += r1 + r2;
    if (y <= 12) rows += `<tr><td>${y}</td><td>${R(r1 + r2)}</td><td>${R(prop + intr)}</td></tr>`;
  }
  $('out').textContent = R(tot); $('rows').innerHTML = rows;
  $('lines').innerHTML = [['Deduction for the price', R(startP)], ['Refund for the price', R(rp)], ['Deduction for interest', R(startI)], ['Refund for interest', R(ri)],
    ['NDFL you pay a year', R(nd(inc))], ['Years to receive it all', y ? String(y) : '—']].map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
}
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>How the property deduction works</h2>
<p>When you buy or build a home in Russia, you can get back NDFL you have paid. Two separate limits apply per person:</p>
<ul><li><strong>Purchase price:</strong> up to 2 million ₽ of spending, once in a lifetime, but it can be spread over several homes until used up.</li>
<li><strong>Mortgage interest:</strong> up to 3 million ₽ of interest, for one home.</li></ul>
<p>The refund equals the tax you paid on that much income. At 13% that is up to 260,000 ₽ for the price and 390,000 ₽ for interest. With the progressive scale, people whose income is taxed at 15–22% get back more. You can never get back more than the NDFL you paid in a year; the rest carries over to later years.</p>
<h3>Example</h3><p>A flat for 8 million ₽ with 1.5 million ₽ of mortgage interest, salary 1.8 million ₽ a year (NDFL 234,000 ₽). The deductions total 3.5 million ₽: 455,000 ₽ back, spread over two years.</p>
<p>A husband and wife can each claim their own limit. You can claim for the last three years of tax paid. Check the details with the tax service or in your personal account on nalog.gov.ru.</p>""",
faqs=[("How much can I get back for buying a flat in Russia?", "Up to 260,000 roubles for the price (13% of 2 million) and up to 390,000 for mortgage interest (13% of 3 million). More if part of your income is taxed above 13%."),
      ("Can spouses both claim?", "Yes. Each spouse has their own 2 million rouble limit for the price, so a couple can receive up to 520,000 roubles at 13%.")]))

# ---------------- Mortgage: annuity vs equal principal ----------------
TOOLS.append(dict(
group="everyday", slug="mortgage-calculator", icon="money",
name="Mortgage Calculator (Equal Payments vs Equal Principal)",
title="Mortgage Calculator: Equal Monthly Payments vs Equal Principal, Total Interest & Schedule",
desc="Compare the two ways banks repay a home loan: equal monthly payments (annuity) and equal principal (decreasing payments). See monthly payment, total interest and a yearly schedule.",
keywords="mortgage calculator, annuity vs differentiated payment, equal principal vs equal installment, mortgage repayment calculator, home loan interest calculator, decreasing payment mortgage",
h1="Mortgage calculator: equal payments vs equal principal",
lede="Same loan, two repayment methods. Equal payments are easier to budget; equal principal costs less interest. See both side by side.",
card="Annuity vs equal principal, total interest",
tool="""
<div class="inputs">
 <div class="row3"><div><label for="P">Loan amount</label><input id="P" inputmode="decimal" value="300000"></div>
 <div><label for="r">Interest (% a year)</label><input id="r" inputmode="decimal" value="6"></div>
 <div><label for="n">Years</label><input id="n" inputmode="decimal" value="25"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Equal monthly payment</div><div class="big" id="out">—</div>
 <div class="scroll"><table class="sched"><thead><tr><th></th><th>Equal payments</th><th>Equal principal</th></tr></thead><tbody id="cmp"></tbody></table></div>
 <p class="hint" id="save"></p>
 <div class="scroll"><table class="sched"><thead><tr><th>Year</th><th>Equal payments: balance</th><th>Equal principal: balance</th></tr></thead><tbody id="rows"></tbody></table></div>
</div>""",
js=r"""
const L0 = document.documentElement.lang, LOC = { zh: 'zh-CN', ru: 'ru-RU', hi: 'en-IN', ml: 'en-IN' }[L0] || undefined;
const D = { zh: [1000000, 3.05, 30], ru: [6000000, 6, 20] }[L0];
if (D) { $('P').value = D[0]; $('r').value = D[1]; $('n').value = D[2]; }
const N = x => Math.round(x).toLocaleString(LOC);
function calc() {
  const P = V('P'), i = V('r') / 1200, m = Math.round(V('n') * 12);
  if (!(P > 0 && m > 0)) return;
  const A = i ? P * i / (1 - Math.pow(1 + i, -m)) : P / m;
  const totA = A * m - P, pr = P / m, first = pr + P * i, last = pr + pr * i, totB = i * pr * m * (m + 1) / 2;
  $('out').textContent = N(A);
  $('cmp').innerHTML = [['Monthly payment', N(A), N(first) + ' → ' + N(last)], ['Total interest', N(totA), N(totB)], ['Total repaid', N(A * m), N(P + totB)]]
    .map(([a, b, c]) => `<tr><td>${a}</td><td>${b}</td><td>${c}</td></tr>`).join('');
  $('save').textContent = 'Equal principal saves ' + N(totA - totB) + ' in interest, but the first payment is ' + N(first - A) + ' higher.';
  let bA = P, bB = P, rows = '';
  for (let k = 1; k <= m; k++) { bA = bA * (1 + i) - A; bB -= pr; if (k % 12 === 0 || k === m) rows += `<tr><td>${Math.ceil(k / 12)}</td><td>${N(Math.max(0, bA))}</td><td>${N(Math.max(0, bB))}</td></tr>`; }
  $('rows').innerHTML = rows;
}
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>Two ways to repay a home loan</h2>
<p><strong>Equal payments (annuity)</strong>: the same amount every month. Early payments are mostly interest; later ones mostly principal. Formula: payment = P × i ÷ (1 − (1 + i)<sup>−n</sup>), where i is the monthly rate and n the number of months.</p>
<p><strong>Equal principal</strong>: you repay the same slice of principal each month, plus interest on what is left. The first payment is the highest and each one is a little smaller. Total interest is lower because the balance falls faster.</p>
<h3>Example</h3><p>300,000 at 6% for 25 years: equal payments of about 1,933 a month and about 279,900 total interest. Equal principal starts at 2,500 and ends at 1,005, with about 225,750 total interest, about 54,000 less.</p>
<h3>Which to choose</h3><ul><li>Choose equal payments if you want a steady, lower starting payment.</li><li>Choose equal principal if you can afford higher payments early and want to pay less interest.</li><li>Either way, extra prepayments early in the loan cut interest the most.</li></ul>""",
faqs=[("Which is cheaper, equal payments or equal principal?", "Equal principal, because you repay the loan faster and pay interest on a smaller balance. Equal payments have a lower starting payment."),
      ("What is an annuity payment?", "A fixed monthly payment that covers interest and principal so the loan is repaid exactly at the end of the term.")]))
