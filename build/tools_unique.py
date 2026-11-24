from tools_extra import TOOLS

MOHRE = ("UAE Ministry of Human Resources & Emiratisation (MOHRE)", "https://www.mohre.gov.ae")
UAE_LEAVE = ("UAE Government portal: annual leave", "https://u.ae/en/information-and-services/jobs/employment-in-the-private-sector/types-of-leaves-and-entitlements-in-the-private-sector/annual-leave")
KERALA_REG = ("Kerala Registration Department", "https://keralaregistration.gov.in")

# ---------------- UAE final settlement (combined) ----------------
TOOLS.insert(0, dict(
group="uae", slug="uae-final-settlement-calculator", unique=True, icon="money",
name="UAE Final Settlement Calculator",
title="UAE Final Settlement Calculator 2026: Gratuity + Leave + Notice + Salary",
desc="Work out your full UAE final settlement in one place: gratuity, unused leave, final month's salary, notice pay and deductions, with a printable statement.",
keywords="final settlement calculator uae, full and final settlement uae, end of service settlement dubai, final settlement calculation resignation uae, notice period pay uae, final settlement statement",
h1="UAE final settlement calculator",
lede="Everything your employer owes you when you leave, in one statement: gratuity, unused leave, unpaid salary days and notice pay, minus any deductions.",
card="Gratuity, leave, notice and salary in one statement",
sources=[MOHRE, UAE_LEAVE],
tool="""
<div class="inputs">
 <div class="row2"><div><label for="basic">Basic salary (AED/month)</label><input id="basic" inputmode="decimal" value="8000"></div>
 <div><label for="gross">Total salary (AED/month)</label><input id="gross" inputmode="decimal" value="13000"><div class="hint">Basic + allowances.</div></div></div>
 <div class="row2"><div><label for="start">Joining date</label><input id="start" type="date" value="2021-03-01"></div><div><label for="end">Last working day</label><input id="end" type="date" value="2026-11-20"></div></div>
 <div class="row2"><div><label for="unpaid">Unpaid leave taken (days)</label><input id="unpaid" inputmode="numeric" value="0"></div>
 <div><label for="leave">Unused annual leave (days)</label><input id="leave" inputmode="decimal" value="18"></div></div>
 <div class="row2"><div><label for="saldays">Unpaid salary days</label><input id="saldays" inputmode="numeric" value="20"><div class="hint">Days worked in the final month not yet paid.</div></div>
 <div><label for="nshort">Notice days not served</label><input id="nshort" inputmode="numeric" value="0"></div></div>
 <div><label for="nwho">If notice was cut short, who ended it early?</label><select id="nwho"><option value="employer">My employer (they pay me for those days)</option><option value="me">I did (the days are deducted from me)</option></select></div>
 <div class="row2"><div><label for="other">Other amounts owed to you (AED)</label><input id="other" inputmode="decimal" value="0"><div class="hint">Bonus, air ticket, expenses.</div></div>
 <div><label for="ded">Deductions (AED)</label><input id="ded" inputmode="decimal" value="0"><div class="hint">Loans, advances, damages.</div></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Estimated final settlement</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p class="formula">Gratuity and leave use basic salary; salary days and notice use total salary. All daily rates are monthly ÷ 30.</p>
</div>""",
js=r"""
function calc() {
  const b = V('basic'), g = V('gross'), s = new Date($('start').value), e = new Date($('end').value);
  let gr = 0, yrs = 0;
  if (!isNaN(s) && !isNaN(e) && e > s) { yrs = (Math.round((e - s) / 864e5) + 1 - V('unpaid')) / 365; if (yrs >= 1) gr = Math.min(b / 30 * (21 * Math.min(yrs, 5) + 30 * Math.max(yrs - 5, 0)), b * 24); }
  const leave = b / 30 * V('leave'), sal = g / 30 * V('saldays'), notice = g / 30 * V('nshort') * ($('nwho').value === 'employer' ? 1 : -1), other = V('other'), ded = V('ded');
  const tot = gr + leave + sal + notice + other - ded;
  $('out').textContent = 'AED ' + FX(tot);
  const row = (a, v, cls) => `<li${cls ? ' class="' + cls + '"' : ''}><span>${a}</span><b>${v < 0 ? '−' : ''}AED ${FX(Math.abs(v))}</b></li>`;
  $('lines').innerHTML = row(`Gratuity (${F(yrs, 2)} yrs)${yrs < 1 ? ', under 1 year' : ''}`, gr) + row('Unused leave', leave) + row('Unpaid salary days', sal) + (V('nshort') ? row('Notice pay', notice) : '') + (other ? row('Other amounts', other) : '') + (ded ? row('Deductions', -ded) : '') + row('Total', tot, 'total');
}
document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>What goes into a UAE final settlement</h2>
<p>When your employment ends, your employer must pay all your dues within <strong>14 days</strong>. Most settlements are made of five parts, and this calculator puts them on one statement you can print or share:</p>
<ol><li><strong>End-of-service gratuity:</strong> 21 days' basic salary per year for the first five years, 30 days per year after that, capped at two years' basic salary. You need at least one year of service.</li>
<li><strong>Unused annual leave:</strong> paid on basic salary, including leave earned in your final part year.</li>
<li><strong>Salary for days worked</strong> in the final month that haven't been paid yet.</li>
<li><strong>Notice period:</strong> if the notice period is cut short, whoever ended it early normally pays the other side the total salary for the unserved days.</li>
<li><strong>Other dues and deductions:</strong> bonuses, air tickets or expenses your contract promises, minus loans or advances you owe.</li></ol>
<h3>Worked example</h3>
<p>Basic AED 8,000, total AED 13,000, 5 years 9 months of service, 18 unused leave days and 20 unpaid salary days: gratuity ≈ AED 33,830, leave AED 4,800 and salary AED 8,667, a total of about <strong>AED 47,297</strong>.</p>
<h3>Before you sign</h3>
<ul><li>Check the basic salary used matches your latest contract or MOHRE offer letter.</li><li>Ask for an itemised settlement sheet and compare it with this one.</li><li>If dues aren't paid, you can complain to MOHRE through its app, website or call centre.</li></ul>
""",
faqs=[("How long does my employer have to pay my final settlement?", "All end-of-service dues must be paid within 14 days of the end of the contract."),
      ("Is the final settlement calculated on basic or total salary?", "Gratuity and unused leave use basic salary. Unpaid salary days and notice pay use your total salary."),
      ("Do I lose gratuity if I resign?", "No. Under the new UAE labour law, gratuity is the same whether you resign or are terminated.")]))

# ---------------- Gulf savings & return planner ----------------
TOOLS.insert(1, dict(
group="uae", slug="gulf-savings-return-planner", unique=True, icon="money",
name="Savings Goal Planner (Abroad to Home)",
title="Gulf Return Planner: How Many Years to Save Your Target in India",
desc="Plan your return from the UAE to India: monthly savings in AED, exchange rate, investment growth and gratuity, and see exactly when you reach your target in rupees.",
keywords="how many years to work in gulf, nri savings calculator, uae savings to india calculator, return to india planner, gulf malayali savings, nri retirement corpus calculator, save 1 crore uae",
h1="Gulf savings and return-home planner",
lede="How long do you need to work in the UAE to reach your savings goal back home? Combine monthly savings, growth and your gratuity in one plan.",
card="How long until you reach your savings target, with growth and currency",
tool="""
<div class="inputs">
 <div class="row2"><div><label for="target">Target savings (₹ lakh)</label><input id="target" inputmode="decimal" value="100"><div class="hint">100 lakh = ₹1 crore.</div></div>
 <div><label for="now">Savings you have now (₹ lakh)</label><input id="now" inputmode="decimal" value="10"></div></div>
 <div class="row2"><div><label for="mon">You save each month (AED)</label><input id="mon" inputmode="decimal" value="4000"></div>
 <div><label for="fx">₹ per AED</label><input id="fx" inputmode="decimal" value="24"><div class="hint">Sample rate. Enter today's.</div></div></div>
 <div class="row2"><div><label for="ret">Expected return (% a year)</label><input id="ret" inputmode="decimal" value="7"></div>
 <div><label for="inc">Savings increase (% a year)</label><input id="inc" inputmode="decimal" value="3"></div></div>
 <label class="check"><input type="checkbox" id="gon" checked> Count my UAE gratuity when I leave</label>
 <div class="row2"><div><label for="basic">Basic salary (AED)</label><input id="basic" inputmode="decimal" value="8000"></div>
 <div><label for="done">Years already with employer</label><input id="done" inputmode="decimal" value="3"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">You reach your target in</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <div class="fig"><svg id="chart" role="img" aria-label="Savings growth chart"></svg></div>
 <p class="formula">Returns are not guaranteed. Use a conservative rate and revisit the plan each year.</p>
</div>""",
js=r"""
const L = x => x >= 1e7 ? '₹' + F(x / 1e7, 2) + ' crore' : '₹' + F(x / 1e5, 1) + ' lakh';
let series = [];
function calc() {
  const T = V('target') * 1e5, fx = V('fx'), r = V('ret') / 1200, inc = V('inc') / 100, b = V('basic'), done = V('done'), gon = $('gon').checked;
  let bal = V('now') * 1e5, mon = V('mon'), contrib = bal, hit = -1, gAt = 0; series = [[0, bal + (gon ? grat(done) * fx : 0)]];
  function grat(y) { return y < 1 ? 0 : Math.min(b / 30 * (21 * Math.min(y, 5) + 30 * Math.max(y - 5, 0)), b * 24); }
  for (let m = 1; m <= 480; m++) {
    if (m > 1 && (m - 1) % 12 === 0) mon *= 1 + inc;
    bal = bal * (1 + r) + mon * fx; contrib += mon * fx;
    const g = gon ? grat(done + m / 12) * fx : 0;
    if (m % 12 === 0) series.push([m / 12, bal + g]);
    if (hit < 0 && bal + g >= T) { hit = m; gAt = g; if (m % 12) series.push([m / 12, bal + g]); break; }
  }
  if (hit < 0) { $('out').textContent = 'Over 40 years'; $('lines').innerHTML = '<li><span>Try saving more, a longer horizon or a lower target.</span><b></b></li>'; draw(T); return; }
  const y = Math.floor(hit / 12), mo = hit % 12, total = series[series.length - 1][1];
  $('out').textContent = `${y} yr${y === 1 ? '' : 's'}${mo ? ' ' + mo + ' mo' : ''}`;
  const yr = new Date().getFullYear() + Math.ceil(hit / 12);
  $('lines').innerHTML = [['Target year (about)', yr], ['Total at that point', L(total)], ['Of which your savings', L(contrib)], ['Of which growth', L(Math.max(total - contrib - gAt, 0))], ['Of which gratuity', L(gAt)]].map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
  draw(T);
}
const svg = $('chart');
function draw(T) {
  const W = svg.clientWidth, H = svg.clientHeight; if (!W || series.length < 2) { svg.innerHTML = ''; return; }
  const xm = series[series.length - 1][0] || 1, ym = Math.max(T, ...series.map(p => p[1])) * 1.08, pl = 6, pb = 18;
  const x = v => pl + v / xm * (W - pl - 6), y = v => 6 + (1 - v / ym) * (H - 6 - pb);
  const d = series.map((p, i) => (i ? 'L' : 'M') + x(p[0]).toFixed(1) + ',' + y(p[1]).toFixed(1)).join('');
  svg.innerHTML = `<line x1="${pl}" x2="${W - 6}" y1="${y(T)}" y2="${y(T)}" stroke="currentColor" stroke-dasharray="4 4" opacity=".45"/><text x="${W - 8}" y="${y(T) - 6}" text-anchor="end" font-size="12" fill="currentColor" opacity=".7">Target</text><path d="${d}L${x(xm)},${H - pb}L${pl},${H - pb}Z" fill="#f5c300" opacity=".18"/><path d="${d}" fill="none" stroke="#c99a00" stroke-width="2.5"/><text x="${pl}" y="${H - 3}" font-size="12" fill="currentColor" opacity=".6">Now</text><text x="${W - 8}" y="${H - 3}" text-anchor="end" font-size="12" fill="currentColor" opacity=".6">${F(xm, 1)} yrs</text>`;
}
const ro = new ResizeObserver(() => draw(V('target') * 1e5)); ro.observe(svg);
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>How the plan is worked out</h2>
<p>Each month, your AED savings are converted to rupees at the rate you enter and added to an investment growing at your expected return. Your monthly savings rise once a year by the percentage you set, reflecting pay rises. If you tick the gratuity box, your UAE end-of-service gratuity at the time you'd leave is added too, using the standard 21/30-day rule.</p>
<h3>Choosing realistic numbers</h3>
<ul><li><strong>Return:</strong> bank fixed deposits in India have recently paid roughly 6–7%; equity funds have historically returned more over long periods but with big swings. Using a lower figure keeps the plan safe.</li>
<li><strong>Exchange rate:</strong> the rupee has tended to weaken against the dirham over time, which helps Gulf savers, but don't count on it.</li>
<li><strong>Inflation:</strong> a target of ₹1 crore will buy less in ten years. Consider raising your target for inflation.</li></ul>
<h3>Ways to reach the goal sooner</h3>
<p>Raising monthly savings has the biggest effect, followed by starting early and keeping costs low. Moving money through an NRE account keeps interest tax-free in India while you're an NRI.</p>
""",
faqs=[("How long does it take to save ₹1 crore working in the UAE?", "With ₹10 lakh already saved, AED 4,000 saved a month at ₹24 per AED, 7% growth, a 3% yearly increase in savings and gratuity on an AED 8,000 basic salary, it takes about 5 years. Use the planner with your own numbers."),
      ("Should I include gratuity in my savings plan?", "Yes, if you expect to receive it. It is often a large lump sum after several years of service.")]))

# ---------------- Kerala plot & house budget ----------------
TOOLS.append(dict(
group="india", slug="kerala-plot-house-budget-calculator", icon="india",
name="Kerala Plot & House Budget Planner",
title="Kerala Land and House Cost Calculator: Plot, Registration, Construction",
desc="Total cost of buying a plot and building a house in Kerala: price per cent, 8% stamp duty + 2% registration on fair value, broker, legal costs and construction per sq ft.",
keywords="kerala house construction cost calculator, land cost per cent kerala, total cost of buying land kerala, kerala plot registration cost, house construction cost per sq ft kerala, nri house budget kerala",
h1="Kerala plot and house budget planner",
lede="Add up the real cost of buying land and building a house in Kerala: the plot, government charges, broker and legal fees, and construction.",
card="Land, registration and construction in one budget",
sources=[KERALA_REG],
tool="""
<div class="inputs">
 <div class="row2"><div><label for="cents">Plot size (cents)</label><input id="cents" inputmode="decimal" value="10"></div>
 <div><label for="ppc">Price per cent (₹)</label><input id="ppc" inputmode="decimal" value="300000"></div></div>
 <div class="row2"><div><label for="fv">Fair value per cent (₹)</label><input id="fv" inputmode="decimal" value="150000"><div class="hint">Government fair value for the survey number.</div></div>
 <div><label for="brk">Broker fee (%)</label><input id="brk" inputmode="decimal" value="2"></div></div>
 <div class="row3"><div><label for="sd">Stamp duty %</label><input id="sd" inputmode="decimal" value="8"></div><div><label for="rf">Registration %</label><input id="rf" inputmode="decimal" value="2"></div><div><label for="legal">Legal & docs (₹)</label><input id="legal" inputmode="decimal" value="20000"></div></div>
 <div class="row2"><div><label for="sqft">House built-up area (sq ft)</label><input id="sqft" inputmode="decimal" value="1500"><div class="hint">Enter 0 for land only.</div></div>
 <div><label for="cps">Construction cost per sq ft (₹)</label><input id="cps" inputmode="decimal" value="2500"></div></div>
 <div><label for="extra">Permit, connections, wall & gate (₹)</label><input id="extra" inputmode="decimal" value="300000"></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Total budget</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <div class="bars" id="bars"></div>
</div>""",
js=r"""
const L = x => x >= 1e7 ? '₹' + F(x / 1e7, 2) + ' cr' : '₹' + F(x / 1e5, 2) + ' lakh';
function calc() {
  const c = V('cents'), land = c * V('ppc'), base = Math.max(land, c * V('fv')), govt = base * (V('sd') + V('rf')) / 100, brk = land * V('brk') / 100, legal = V('legal'), build = V('sqft') * V('cps'), extra = V('extra');
  const parts = [['Land', land], ['Stamp & registration', govt], ['Broker', brk], ['Legal & documents', legal], ['Construction', build], ['Permits & extras', extra]];
  const tot = parts.reduce((a, p) => a + p[1], 0);
  $('out').textContent = L(tot);
  $('lines').innerHTML = parts.filter(p => p[1]).map(([a, v]) => `<li><span>${a}</span><b>₹${F(v, 0)}</b></li>`).join('') + `<li><span>Plot area</span><b>${F(c * 435.6, 0)} sq ft</b></li><li><span>Effective cost per sq ft built</span><b>${V('sqft') ? '₹' + F(tot / V('sqft'), 0) : '—'}</b></li>`;
  $('bars').innerHTML = parts.filter(p => p[1]).map(([a, v]) => `<div><span>${a}</span><i style="width:${(v / tot * 100).toFixed(1)}%"></i><b>${F(v / tot * 100, 0)}%</b></div>`).join('');
}
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<p class="hint">Buying elsewhere in India or abroad? Use the <a href="/property-buying-cost-calculator/">property buying cost calculator</a> with state and country rates.</p>
<h2>What the budget includes</h2>
<ul><li><strong>Land:</strong> plot size in cents × agreed price per cent.</li>
<li><strong>Stamp duty and registration:</strong> 8% + 2% of the <em>higher</em> of the sale price and the government fair value.</li>
<li><strong>Broker:</strong> commonly 1–2% of the land price in Kerala, often charged to both buyer and seller.</li>
<li><strong>Legal and documents:</strong> document writer or advocate, encumbrance certificate, copies and mutation.</li>
<li><strong>Construction:</strong> built-up area × cost per square foot. Costs vary widely with finish, location and labour, so get quotes from local contractors.</li>
<li><strong>Extras:</strong> building permit fees, KSEB and water connections, compound wall, gate and well or borewell.</li></ul>
<h3>Tips for NRIs building from the Gulf</h3>
<ul><li>Check the land classification first. Paddy land and wetland have strict conversion rules.</li><li>Pay through banking channels from your NRE/NRO account and keep every receipt.</li><li>Release construction payments in stages against work completed and photographs.</li></ul>
""",
faqs=[("What is the total cost of registering land in Kerala?", "About 10% of the higher of fair value and sale price (8% stamp duty + 2% registration), plus document writer and other small fees."),
      ("How many sq ft is 10 cents?", "4,356 square feet.")]))

# ---------------- Trading strategy simulator ----------------
TOOLS.append(dict(
group="trading", slug="trading-strategy-simulator", unique=True, icon="trading",
name="Trading Strategy Simulator",
title="Trading Monte Carlo Simulator: Drawdown, Losing Streaks & Risk of Ruin",
desc="Simulate 1,000 futures for your trading strategy from win rate, risk–reward and risk per trade. See likely drawdowns, losing streaks and the chance of ending in profit.",
keywords="trading monte carlo simulator, drawdown calculator, risk of ruin calculator, losing streak probability trading, win rate risk reward simulator, forex strategy simulator, prop firm drawdown",
h1="Trading strategy simulator",
lede="Your win rate and risk–reward tell you the average. This shows the range: 1,000 simulated runs of your next trades, with the drawdowns and losing streaks you should be ready for.",
card="1,000 simulated runs: drawdown and risk of ruin",
tool="""
<div class="inputs">
 <div class="row2"><div><label for="bal">Starting balance</label><input id="bal" inputmode="decimal" value="10000"></div>
 <div><label for="risk">Risk per trade (%)</label><input id="risk" inputmode="decimal" value="1"></div></div>
 <div class="row2"><div><label for="win">Win rate (%)</label><input id="win" inputmode="decimal" value="45"></div>
 <div><label for="rr">Average reward (R)</label><input id="rr" inputmode="decimal" value="2"><div class="hint">2 means winners make twice what losers lose.</div></div></div>
 <div class="row2"><div><label for="n">Trades per run</label><input id="n" inputmode="numeric" value="200"></div>
 <div><label for="cost">Costs per trade (R)</label><input id="cost" inputmode="decimal" value="0.05"><div class="hint">Spread + commission as a fraction of risk.</div></div></div>
 <div><label for="dd">Drawdown limit to test (%)</label><input id="dd" inputmode="decimal" value="10"><div class="hint">For example a prop-firm maximum loss.</div></div>
 <button type="button" class="btn primary" id="again">Run again</button>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Chance of ending in profit</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <div class="fig"><svg id="chart" role="img" aria-label="Simulated equity curves"></svg></div>
 <p class="formula" id="msg"></p>
</div>""",
js=r"""
let curves = [], med = [];
function q(a, p) { const s = [...a].sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.floor(p * s.length))]; }
function calc() {
  const B = V('bal') || 1, rk = V('risk') / 100, w = V('win') / 100, R = V('rr'), N = Math.min(Math.max(Math.round(V('n')), 1), 2000), c = V('cost'), lim = V('dd') / 100, RUNS = 1000;
  const ends = [], dds = [], streaks = []; let hitLim = 0; curves = [];
  for (let k = 0; k < RUNS; k++) {
    let eq = B, peak = B, mdd = 0, st = 0, mst = 0, hit = false; const cv = k < 40 ? [B] : null;
    for (let t = 0; t < N; t++) {
      const r = eq * rk;
      if (Math.random() < w) { eq += r * (R - c); st = 0; } else { eq -= r * (1 + c); st++; if (st > mst) mst = st; }
      if (eq > peak) peak = eq; const dd = (peak - eq) / peak; if (dd > mdd) mdd = dd; if (!hit && (B - eq) / B >= lim) hit = true;
      if (cv) cv.push(eq);
    }
    ends.push(eq); dds.push(mdd); streaks.push(mst); if (hit) hitLim++; if (cv) curves.push(cv);
  }
  const prof = ends.filter(e => e > B).length / RUNS, exp = w * R - (1 - w) - c;
  $('out').textContent = (prof > .99 && prof < 1 ? '>99' : prof < .01 && prof > 0 ? '<1' : F(prof * 100, 0)) + '%';
  $('lines').innerHTML = [['Expectancy per trade', F(exp, 2) + ' R'], ['Median ending balance', F(q(ends, .5), 0)], ['Range (5th–95th percentile)', F(q(ends, .05), 0) + ' – ' + F(q(ends, .95), 0)], ['Typical worst drawdown', F(q(dds, .5) * 100, 1) + '%'], ['Bad-luck drawdown (1 in 20)', F(q(dds, .95) * 100, 1) + '%'], ['Typical longest losing streak', q(streaks, .5) + ' trades'], [`Runs that lost ${F(lim * 100, 0)}% of the start`, F(hitLim / RUNS * 100, 1) + '%']].map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
  $('msg').textContent = exp <= 0 ? 'This strategy loses money on average after costs. No position size fixes negative expectancy.' : 'Thin lines show 40 sample runs. Results assume each trade is independent; real markets can be streakier.';
  draw();
}
const svg = $('chart');
function draw() {
  const W = svg.clientWidth, H = svg.clientHeight; if (!W || !curves.length) return;
  const all = curves.flat(), lo = Math.min(...all), hi = Math.max(...all), n = curves[0].length - 1 || 1, B = curves[0][0];
  const x = i => 4 + i / n * (W - 8), y = v => 6 + (1 - (v - lo) / ((hi - lo) || 1)) * (H - 12);
  const path = cv => cv.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ',' + y(v).toFixed(1)).join('');
  svg.innerHTML = `<line x1="4" x2="${W - 4}" y1="${y(B)}" y2="${y(B)}" stroke="currentColor" stroke-dasharray="4 4" opacity=".4"/>` + curves.map(cv => `<path d="${path(cv)}" fill="none" stroke="${cv[cv.length - 1] >= B ? '#c99a00' : '#c2261d'}" stroke-width="1" opacity=".35"/>`).join('');
}
const ro = new ResizeObserver(draw); ro.observe(svg);
$('again').addEventListener('click', calc);
let tm; document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', () => { clearTimeout(tm); tm = setTimeout(calc, 250); })); calc();
""",
body="""
<h2>Why simulate instead of using averages</h2>
<p>Expectancy, meaning win rate × reward minus loss rate × risk, tells you whether a strategy makes money on average. It doesn't tell you how rough the ride will be. Two traders with the same edge can have very different months purely through the order of wins and losses. This simulator plays out your next trades 1,000 times with random order, so you can see the spread of outcomes.</p>
<h3>How to read the results</h3>
<ul><li><strong>Typical worst drawdown:</strong> the peak-to-trough fall in half of the runs. Expect at least this.</li>
<li><strong>Bad-luck drawdown (1 in 20):</strong> plan your risk so you could survive this.</li>
<li><strong>Losing streak:</strong> even a 50% win rate regularly produces runs of 6–8 losses in 200 trades.</li>
<li><strong>Drawdown limit:</strong> the share of runs that hit your limit, for example a prop-firm's maximum loss from the starting balance.</li></ul>
<h3>Worked example</h3>
<p>Win rate 45%, reward 2R, costs 0.05R: expectancy = 0.45 × 2 − 0.55 − 0.05 = <strong>+0.30R per trade</strong>. At 1% risk that edge is solid, but the simulator typically still shows double-digit drawdowns along the way.</p>
<p>Pair this with the <a href="/position-size-calculator/">position size calculator</a> and the <a href="/risk-reward-calculator/">risk–reward calculator</a>. This tool is educational and not investment advice.</p>
""",
faqs=[("What is a Monte Carlo simulation in trading?", "It replays your strategy many times in random order to show the range of possible results, drawdowns and losing streaks, not just the average."),
      ("How do I lower my drawdown?", "Lower the risk per trade. Halving risk roughly halves drawdowns, and expectancy per trade stays the same.")]))
