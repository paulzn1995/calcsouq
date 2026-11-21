# Futures and options margin calculator: NSE, BSE, LME, CME and US-listed options.
# Lot sizes are facts that change by exchange circular: CHECKED date below must be updated when verified.
# Margin rates change daily; the tool never presents a margin as live. Each contract links to the official live source.
from tools_world import TOOLS

CHECKED = "21 Nov 2026"

TOOLS.append(dict(
group="trading", slug="futures-options-margin-calculator", unique=True, icon="trading",
name="Futures & Options Margin Calculator",
title="F&O Margin Calculator: Futures, Calendar Spreads & Option Strategies (NSE, BSE, LME, CME, US Options)",
desc="Margin for futures, calendar spreads and option strategies (spreads, straddles, strangles, iron condors) with current lot sizes for NSE, BSE, LME, CME and US-listed options. Links to each exchange's live margin figures.",
keywords="f&o margin calculator, option strategy margin calculator, futures margin calculator, nifty margin calculator, bank nifty lot size, lme margin, lme lot size, cme margin calculator, iron condor margin, short strangle margin, calendar spread margin, reg t option margin",
h1="Futures & options margin calculator",
lede="Pick the exchange and contract, then a futures trade, a calendar spread or an option strategy. Lot sizes are filled in; margin rates are editable, with a link to the exchange's live figure.",
card="Futures, spreads and option strategies, all markets",
sources=[("NSE: SPAN margin calculator", "https://www.nseindia.com/"), ("BSE: derivatives margins", "https://www.bseindia.com/"),
         ("LME Clear: margin parameters", "https://www.lme.com/en/lme-clear"), ("CME Group: performance bonds / margins", "https://www.cmegroup.com/clearing/margins.html"),
         ("Cboe: strategy-based margin", "https://www.cboe.com/markets/us/options/margin/strategy-based-margin")],
tool="""
<div class="inputs">
 <div class="row2"><div><label for="mk">Exchange</label><select id="mk">
  <option value="NSE">NSE (India)</option><option value="BSE">BSE (India)</option><option value="LME">LME (London metals)</option>
  <option value="CME">CME Group (US futures)</option><option value="US">US-listed options (Nasdaq, Cboe, NYSE)</option><option value="OT">Other exchange</option></select></div>
 <div><label for="ct">Contract</label><select id="ct"></select></div></div>
 <div class="row2"><div><label for="lot">Lot size / multiplier</label><input id="lot" inputmode="decimal"><div class="hint" id="lotnote"></div></div>
 <div><label for="md">Trade type</label><select id="md"><option value="fut">Futures: outright</option><option value="spr">Futures: calendar spread</option><option value="opt">Options strategy</option></select></div></div>
 <div class="row2"><div><label for="px" id="pxl">Futures price</label><input id="px" inputmode="decimal"></div>
 <div><label for="n">Number of lots</label><input id="n" inputmode="decimal" value="1"></div></div>
 <div id="futw" style="display:grid;gap:14px"><div class="row2"><div><label for="mm">Margin method</label><select id="mm"><option value="pct">% of contract value</option><option value="fix">Fixed amount per lot</option></select></div>
  <div><label for="mr" id="mrl">Initial margin (%)</label><input id="mr" inputmode="decimal"><div class="hint" id="mrh"></div></div></div></div>
 <div id="sprw" hidden style="display:grid;gap:14px"><div class="row2"><div><label for="px2">Far-month price</label><input id="px2" inputmode="decimal"></div>
  <div><label for="sc">Spread benefit vs outright (%)</label><input id="sc" inputmode="decimal" value="75"><div class="hint">Exchanges charge less for a calendar spread than for two outright legs. Enter the credit from the exchange or broker.</div></div></div></div>
 <div id="optw" hidden style="display:grid;gap:14px">
  <div><label for="st">Strategy</label><select id="st">
   <option value="lc">Long call</option><option value="lp">Long put</option><option value="sc">Short call</option><option value="sp">Short put</option>
   <option value="bcs">Bull call spread (debit)</option><option value="bps">Bear put spread (debit)</option><option value="bpc">Bull put spread (credit)</option><option value="bcc">Bear call spread (credit)</option>
   <option value="ss">Short straddle</option><option value="sg">Short strangle</option><option value="ic">Iron condor (short)</option><option value="lst">Long straddle</option></select></div>
  <div class="row2" id="k1w"><div><label for="k1" id="k1l">Strike</label><input id="k1" inputmode="decimal"></div><div><label for="p1" id="p1l">Premium</label><input id="p1" inputmode="decimal"></div></div>
  <div class="row2" id="k2w"><div><label for="k2" id="k2l">Strike 2</label><input id="k2" inputmode="decimal"></div><div><label for="p2" id="p2l">Premium 2</label><input id="p2" inputmode="decimal"></div></div>
  <div class="row2" id="k3w"><div><label for="k3" id="k3l">Strike 3</label><input id="k3" inputmode="decimal"></div><div><label for="p3" id="p3l">Premium 3</label><input id="p3" inputmode="decimal"></div></div>
  <div class="row2" id="k4w"><div><label for="k4" id="k4l">Strike 4</label><input id="k4" inputmode="decimal"></div><div><label for="p4" id="p4l">Premium 4</label><input id="p4" inputmode="decimal"></div></div>
  <div class="row2" id="rw"><div><label for="sr">Short option margin (% of underlying)</label><input id="sr" inputmode="decimal"><div class="hint" id="srh"></div></div>
   <div><label for="ub">Underlying type</label><select id="ub"><option value="eq">Stock or ETF</option><option value="ix">Broad-based index</option></select></div></div>
 </div>
 <p class="hint" id="src"></p>
</div>
<div class="result" aria-live="polite">
 <div class="big-label" id="outl">Margin required</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p class="hint" id="warn"></p>
</div>""",
js=r"""
const C = {
 NSE: { cur: '₹', loc: 'en-IN', mr: 12, sr: 12, link: 'NSE SPAN margin calculator (nseindia.com) or your broker', rule: 'span',
   c: [['NIFTY', 'Nifty 50', 65, 26000], ['BANKNIFTY', 'Nifty Bank', 30, 58000], ['FINNIFTY', 'Nifty Financial Services', 60, 27000], ['MIDCPNIFTY', 'Nifty Midcap Select', 120, 13500], ['NIFTYNXT50', 'Nifty Next 50', 25, 69000], ['STK', 'Stock F&O (enter lot size)', 1, 1000]] },
 BSE: { cur: '₹', loc: 'en-IN', mr: 12, sr: 12, link: 'BSE derivatives margin files (bseindia.com) or your broker', rule: 'span',
   c: [['SENSEX', 'Sensex (20; 25 from Jan 2027 expiries)', 20, 85000], ['BANKEX', 'Bankex', 30, 64000], ['SENSEX50', 'Sensex 50', 75, 27000]] },
 LME: { cur: '$', loc: 'en-US', mr: 10, sr: 10, unit: 'tonnes', link: 'LME Clear margin parameters (lme.com, LME Clear section)', rule: 'span',
   c: [['CA', 'Copper (25 t)', 25, 10000], ['AH', 'Aluminium (25 t)', 25, 2600], ['ZS', 'Zinc (25 t)', 25, 2900], ['PB', 'Lead (25 t)', 25, 2000], ['NI', 'Nickel (6 t)', 6, 15500], ['SN', 'Tin (5 t)', 5, 33000]] },
 CME: { cur: '$', loc: 'en-US', mr: 8, sr: 8, link: 'CME Group margins page (cmegroup.com/clearing/margins)', rule: 'span',
   c: [['ES', 'E-mini S&P 500 ($50 × index)', 50, 6000], ['MES', 'Micro E-mini S&P 500 ($5 × index)', 5, 6000], ['NQ', 'E-mini Nasdaq-100 ($20 × index)', 20, 21000], ['MNQ', 'Micro E-mini Nasdaq-100 ($2 × index)', 2, 21000],
       ['YM', 'E-mini Dow ($5 × index)', 5, 44000], ['CL', 'Crude oil WTI (1,000 barrels)', 1000, 65], ['GC', 'Gold (100 troy oz)', 100, 3500], ['MGC', 'Micro gold (10 troy oz)', 10, 3500], ['SI', 'Silver (5,000 troy oz)', 5000, 40]] },
 US: { cur: '$', loc: 'en-US', mr: 50, sr: 20, link: 'Cboe strategy-based margin rules; your broker may ask for more', rule: 'regt', opt: 1,
   c: [['STK', 'Stock or ETF option (100 shares)', 100, 200], ['SPX', 'S&P 500 index option (SPX, $100 × index)', 100, 6000], ['NDX', 'Nasdaq-100 index option (NDX, $100 × index)', 100, 21000]] },
 OT: { cur: '', loc: undefined, mr: 10, sr: 10, link: 'your exchange or broker', rule: 'span', c: [['X', 'Custom contract', 1, 100]] }
};
let M = C.NSE;
const A = x => M.cur + (Number.isFinite(x) ? x : 0).toLocaleString(M.loc, { maximumFractionDigits: 0 });
const show = (id, on) => { $(id).hidden = !on; };
function setMarket() {
  M = C[$('mk').value];
  $('ct').innerHTML = M.c.map(([v, n]) => `<option value="${v}">${n}</option>`).join('');
  if (M.opt) { $('md').value = 'opt'; } else if ($('mk').value === 'LME' && $('md').value === 'opt') { /* LME options allowed */ }
  [...$('md').options].forEach(o => o.disabled = M.opt && o.value !== 'opt');
  $('mr').value = M.mr; $('sr').value = M.sr; $('ub').value = 'eq';
  $('src').textContent = 'Live margins: ' + M.link + '. Rates here are starting estimates — replace them with today’s figure.';
  setContract();
}
function setContract() {
  const c = M.c.find(x => x[0] === $('ct').value) || M.c[0];
  $('lot').value = c[2]; $('px').value = c[3]; $('px2').value = Math.round(c[3] * 1.006 * 100) / 100;
  $('lotnote').textContent = M.unit ? 'Tonnes per lot.' : (M.opt ? 'Shares or index multiplier per contract.' : 'Units per lot or value per point.');
  $('ub').value = ['SPX', 'NDX'].includes(c[0]) ? 'ix' : 'eq';
  setStrikes();
}
function setStrikes() {
  const S = V('px') || 100, step = S > 20000 ? 100 : S > 2000 ? 50 : S > 200 ? 5 : 1, r = v => Math.round(v / step) * step;
  const atm = r(S), w = step * (S > 20000 ? 5 : 4);
  const P = (k, call) => { const itm = Math.max(call ? S - k : k - S, 0), d = Math.abs(S - k); return Math.max(+(itm + S * 0.015 * Math.exp(-d / (S * 0.03))).toFixed(2), 0.05); };
  const st = $('st').value;
  const setK = (arr) => arr.forEach(([k, call], i) => { $('k' + (i + 1)).value = k; $('p' + (i + 1)).value = P(k, call).toFixed(2); });
  const T = { lc: [[atm, 1]], lp: [[atm, 0]], sc: [[r(S + w), 1]], sp: [[r(S - w), 0]], bcs: [[atm, 1], [r(S + w), 1]], bps: [[atm, 0], [r(S - w), 0]],
    bpc: [[r(S - w), 0], [r(S - 2 * w), 0]], bcc: [[r(S + w), 1], [r(S + 2 * w), 1]], ss: [[atm, 1], [atm, 0]], sg: [[r(S + w), 1], [r(S - w), 0]],
    ic: [[r(S - w), 0], [r(S - 2 * w), 0], [r(S + w), 1], [r(S + 2 * w), 1]], lst: [[atm, 1], [atm, 0]] };
  setK(T[st]); layout(); calc();
}
const LBL = { lc: ['Call strike', 'Call premium'], lp: ['Put strike', 'Put premium'], sc: ['Call strike (sold)', 'Premium received'], sp: ['Put strike (sold)', 'Premium received'],
  bcs: ['Buy call strike', 'Premium paid', 'Sell call strike (higher)', 'Premium received'], bps: ['Buy put strike', 'Premium paid', 'Sell put strike (lower)', 'Premium received'],
  bpc: ['Sell put strike', 'Premium received', 'Buy put strike (lower)', 'Premium paid'], bcc: ['Sell call strike', 'Premium received', 'Buy call strike (higher)', 'Premium paid'],
  ss: ['Call strike (sold)', 'Call premium', 'Put strike (sold)', 'Put premium'], sg: ['Call strike (sold)', 'Call premium', 'Put strike (sold)', 'Put premium'],
  ic: ['Sell put strike', 'Premium received', 'Buy put strike (lower)', 'Premium paid', 'Sell call strike', 'Premium received', 'Buy call strike (higher)', 'Premium paid'],
  lst: ['Call strike', 'Call premium', 'Put strike', 'Put premium'] };
function layout() {
  const md = $('md').value, st = $('st').value, L = LBL[st], legs = L.length / 2;
  show('futw', md !== 'opt'); show('sprw', md === 'spr'); show('optw', md === 'opt');
  $('pxl').textContent = md === 'opt' ? 'Underlying price' : (md === 'spr' ? 'Near-month price' : 'Futures price');
  for (let i = 1; i <= 4; i++) { show('k' + i + 'w', i <= legs); if (i <= legs) { $('k' + i + 'l').textContent = L[2 * i - 2]; $('p' + i + 'l').textContent = L[2 * i - 1]; } }
  const regt = M.rule === 'regt';
  $('sr').closest('div').hidden = regt; show('ub', regt); $('ub').previousElementSibling.hidden = !regt;
  $('srh').textContent = 'SPAN-style estimate for one short option, as % of underlying value. Use the exchange or broker figure for today.';
  const fix = $('mm').value === 'fix'; $('mrl').textContent = fix ? 'Initial margin per lot' : 'Initial margin (%)';
  $('mrh').textContent = fix ? 'From the exchange margin page for this contract.' : 'Estimate. Replace with today’s exchange figure.';
}
function calc() {
  const md = $('md').value, lot = V('lot'), n = V('n'), q = lot * n, S = V('px');
  const lines = []; let marg = 0, warn = '';
  if (md !== 'opt') {
    const cv = S * q, perLot = $('mm').value === 'fix' ? V('mr') : S * lot * V('mr') / 100;
    if (md === 'fut') {
      marg = perLot * n;
      lines.push(['Contract value', A(cv)], ['Margin per lot', A(perLot)], ['Leverage', (marg ? (cv / marg).toFixed(1) : '—') + '×'], ['Profit or loss for a 1% move', A(cv * 0.01)], ['Value of a 1-point move', A(q)]);
    } else {
      const S2 = V('px2'), outright = perLot * n * 2;
      marg = outright * (1 - V('sc') / 100);
      lines.push(['Spread (far − near)', (S2 - S).toLocaleString(M.loc, { maximumFractionDigits: 2 })], ['Spread value', A((S2 - S) * q)], ['Two outright legs would need', A(outright)], ['Saved by spread treatment', A(outright - marg)], ['P&L when the spread moves 1 point', A(q)]);
      warn = 'Spread margin depends on the exchange’s inter-month spread charge. Near expiry the benefit can be withdrawn.';
    }
  } else {
    const st = $('st').value, k = [V('k1'), V('k2'), V('k3'), V('k4')], p = [V('p1'), V('p2'), V('p3'), V('p4')];
    const regt = M.rule === 'regt', r = $('ub').value === 'ix' ? 0.15 : 0.20;
    const unc = (call, K, prem) => regt ? prem + Math.max(r * S - Math.max(call ? K - S : S - K, 0), 0.10 * (call ? S : K)) : S * V('sr') / 100;
    let credit = 0, maxP = 0, maxL = 0, be = [];
    const width = (a, b) => Math.abs(a - b);
    switch (st) {
      case 'lc': credit = -p[0]; maxL = p[0]; maxP = Infinity; be = [k[0] + p[0]]; marg = p[0]; break;
      case 'lp': credit = -p[0]; maxL = p[0]; maxP = k[0] - p[0]; be = [k[0] - p[0]]; marg = p[0]; break;
      case 'sc': credit = p[0]; maxP = p[0]; maxL = Infinity; be = [k[0] + p[0]]; marg = unc(1, k[0], p[0]); break;
      case 'sp': credit = p[0]; maxP = p[0]; maxL = k[0] - p[0]; be = [k[0] - p[0]]; marg = unc(0, k[0], p[0]); break;
      case 'bcs': case 'bps': { const d = p[0] - p[1]; credit = -d; maxL = d; maxP = width(k[0], k[1]) - d; be = [st === 'bcs' ? k[0] + d : k[0] - d]; marg = d; break; }
      case 'bpc': case 'bcc': { const c = p[0] - p[1]; credit = c; maxP = c; maxL = width(k[0], k[1]) - c; be = [st === 'bpc' ? k[0] - c : k[0] + c]; marg = regt ? width(k[0], k[1]) : maxL; break; }
      case 'ss': case 'sg': { const c = p[0] + p[1]; credit = c; maxP = c; maxL = Infinity; be = [k[1] - c, k[0] + c];
        marg = regt ? Math.max(unc(1, k[0], p[0]) + p[1], unc(0, k[1], p[1]) + p[0]) : S * V('sr') / 100 + Math.min(p[0], p[1]); break; }
      case 'ic': { const c = p[0] - p[1] + p[2] - p[3], wd = Math.max(width(k[0], k[1]), width(k[2], k[3])); credit = c; maxP = c; maxL = wd - c; be = [k[0] - c, k[2] + c]; marg = regt ? wd : maxL; break; }
      case 'lst': { const d = p[0] + p[1]; credit = -d; maxL = d; maxP = Infinity; be = [k[1] - d, k[0] + d]; marg = d; break; }
    }
    marg *= q;
    const f = x => x === Infinity ? 'Unlimited' : A(x * q);
    lines.push([credit >= 0 ? 'Net premium received' : 'Net premium paid', A(Math.abs(credit) * q)], ['Maximum profit', f(maxP)], ['Maximum loss', f(maxL)],
      ['Breakeven', be.map(x => x.toLocaleString(M.loc, { maximumFractionDigits: 2 })).join(' and ')], ['Quantity', q.toLocaleString(M.loc) + (M.unit ? ' ' + M.unit : ' units')]);
    if (credit > 0 && regt && ['bpc', 'bcc', 'ic'].includes(st)) lines.push(['Cash needed after premium', A(Math.max(0, marg - credit * q))]);
    warn = regt ? 'Cboe/FINRA minimums for a margin account. Brokers can ask for more.' :
      (['bpc', 'bcc', 'ic'].includes(st) ? 'Hedged (defined-risk) position: exchanges using SPAN usually ask for close to the maximum loss. Check with your broker’s calculator.' :
      (['lc', 'lp', 'bcs', 'bps', 'lst'].includes(st) ? 'You pay the premium in full; no further margin.' : 'Short options: estimate from the % above. Use today’s exchange or broker figure.'));
  }
  $('out').textContent = A(marg); $('warn').textContent = warn;
  $('lines').innerHTML = lines.map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
}
$('mk').addEventListener('change', setMarket); $('ct').addEventListener('change', setContract); $('st').addEventListener('change', setStrikes);
$('md').addEventListener('change', () => { layout(); calc(); }); $('mm').addEventListener('change', () => { layout(); calc(); }); $('ub').addEventListener('change', calc);
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc));
const LG = { hi: 'NSE', ml: 'NSE', zh: 'LME', ru: 'LME' }[document.documentElement.lang];
const TZ = { 'Asia/Kolkata': 'NSE', 'Asia/Calcutta': 'NSE', 'Europe/London': 'LME', 'America/New_York': 'CME', 'America/Chicago': 'CME', 'America/Los_Angeles': 'US' }[(Intl.DateTimeFormat().resolvedOptions().timeZone || '')];
$('mk').value = LG || TZ || 'NSE'; setMarket();
""",
body="""
<h2>How margin works for each trade type</h2>
<ul><li><strong>Futures:</strong> initial margin is a share of the contract value (price × lot size × lots), or a fixed amount per lot. Exchanges set it from their risk models and change it often, sometimes several times a day.</li>
<li><strong>Calendar spreads:</strong> buying one month and selling another carries much less risk than two outright positions, so exchanges charge a reduced spread margin.</li>
<li><strong>Option buyers</strong> pay the premium in full. <strong>Option sellers</strong> post margin. Defined-risk strategies (credit spreads, iron condors) usually need about the maximum loss; naked short options and short straddles or strangles need the most.</li></ul>
<h3>Lot sizes (checked """ + CHECKED + """)</h3>
<div class="scroll"><table><thead><tr><th>Exchange</th><th>Contract</th><th>Lot size</th></tr></thead><tbody>
<tr><td>NSE</td><td>Nifty 50</td><td>65</td></tr><tr><td>NSE</td><td>Nifty Bank</td><td>30</td></tr><tr><td>NSE</td><td>Nifty Financial Services</td><td>60</td></tr><tr><td>NSE</td><td>Nifty Midcap Select</td><td>120</td></tr><tr><td>NSE</td><td>Nifty Next 50</td><td>25</td></tr>
<tr><td>BSE</td><td>Sensex</td><td>20 (25 for expiries from January 2027)</td></tr><tr><td>BSE</td><td>Bankex</td><td>30</td></tr><tr><td>BSE</td><td>Sensex 50</td><td>75</td></tr>
<tr><td>LME</td><td>Copper, aluminium, zinc, lead</td><td>25 tonnes</td></tr><tr><td>LME</td><td>Nickel</td><td>6 tonnes</td></tr><tr><td>LME</td><td>Tin</td><td>5 tonnes</td></tr>
<tr><td>CME</td><td>E-mini S&amp;P 500 / Micro</td><td>$50 / $5 × index</td></tr><tr><td>CME</td><td>E-mini Nasdaq-100 / Micro</td><td>$20 / $2 × index</td></tr><tr><td>CME</td><td>WTI crude oil</td><td>1,000 barrels</td></tr><tr><td>CME (CBOT)</td><td>E-mini Dow</td><td>$5 × index</td></tr><tr><td>CME (COMEX)</td><td>Gold / Micro gold</td><td>100 / 10 troy oz</td></tr><tr><td>CME (COMEX)</td><td>Silver</td><td>5,000 troy oz</td></tr>
<tr><td>US options</td><td>Stock and ETF options</td><td>100 shares</td></tr></tbody></table></div>
<p>Stock F&amp;O lot sizes in India change by exchange circular; enter the lot size shown in your order window.</p>
<h3>US option margin rules (Cboe / FINRA minimum)</h3>
<p>A naked short equity option needs the premium plus 20% of the underlying value, less any out-of-the-money amount, with a floor of the premium plus 10% (of the share price for calls, of the strike for puts). Broad-based index options use 15% instead of 20%. A credit spread needs the difference between the strikes; an iron condor needs the wider of its two spreads, because only one side can lose at expiry.</p>
<h3>India, LME and CME</h3>
<p>These exchanges use SPAN-type risk models. Margin for a short option or futures position is the SPAN requirement plus any exposure or additional margin, and hedged positions get a benefit. The calculator gives an estimate from the percentage you enter; for the exact figure, use the exchange's file or your broker's calculator, linked under Sources.</p>
<h3>Example</h3>
<p>Nifty iron condor, 1 lot of 65: sell 25,800 put at 90, buy 25,600 put at 45, sell 26,200 call at 85, buy 26,400 call at 40. Net credit 90 points (₹5,850). Maximum loss is 200 − 90 = 110 points (₹7,150), which is roughly what a SPAN-based broker will block for this hedged position.</p>
""",
faqs=[("What is the Nifty lot size now?", "65 for Nifty 50 contracts from the January 2026 expiry. Bank Nifty is 30, FinNifty 60 and Midcap Select 120."),
      ("How much margin is needed for an iron condor?", "Under US rules, the width of the wider spread. On NSE and other SPAN exchanges, usually close to the maximum loss, because the bought wings cap the risk."),
      ("Why is calendar spread margin lower?", "The two legs move together most of the time, so the exchange's risk model gives a large offset. The benefit can shrink near expiry of the near month."),
      ("What is the LME lot size for copper and nickel?", "Copper, aluminium, zinc and lead are 25 tonnes per lot. Nickel is 6 tonnes and tin is 5 tonnes.")]))
