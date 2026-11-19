from tools_uae import TOOLS

PAIRS = [("EURUSD", 1.0850), ("GBPUSD", 1.2700), ("USDJPY", 150.00), ("USDCHF", 0.8800), ("AUDUSD", 0.6600),
         ("USDCAD", 1.3800), ("NZDUSD", 0.6000), ("EURGBP", 0.8550), ("EURJPY", 162.00), ("GBPJPY", 190.00),
         ("AUDJPY", 99.00), ("EURCHF", 0.9500), ("USDINR", 84.50), ("XAUUSD", 2650.00)]
ACCS = ["USD", "AED", "EUR", "GBP", "INR"]

pair_opts = "".join(f'<option value="{p}"{" selected" if p=="EURUSD" else ""}>{p[:3]}/{p[3:]}</option>' for p, _ in PAIRS)
acc_opts = "".join(f'<option value="{a}">{a}</option>' for a in ACCS)
PRICES = "{" + ",".join(f"{p}:{v}" for p, v in PAIRS) + "}"

FX_INPUTS = f"""
 <div class="row2"><div><label for="pair">Instrument</label><select id="pair">{pair_opts}</select></div>
 <div><label for="price">Current price</label><input id="price" inputmode="decimal" value="1.0850"></div></div>
 <div class="row2"><div><label for="acc">Account currency</label><select id="acc">{acc_opts}</select></div>
 <div id="convBox"><label for="conv" id="convLabel">Conversion rate</label><input id="conv" inputmode="decimal" value="1"></div></div>
"""

FXLIB = r"""
const PRICES = %s;
const spec = p => ({ base: p.slice(0, 3), quote: p.slice(3), pip: p === 'XAUUSD' ? 0.01 : (p.endsWith('JPY') || p === 'USDINR') ? 0.01 : 0.0001, cs: p === 'XAUUSD' ? 100 : 100000 });
const USDV = { USD: 1, AED: 1 / 3.6725, EUR: PRICES.EURUSD, GBP: PRICES.GBPUSD, JPY: 1 / PRICES.USDJPY, CHF: 1 / PRICES.USDCHF, AUD: PRICES.AUDUSD, CAD: 1 / PRICES.USDCAD, NZD: PRICES.NZDUSD, INR: 1 / PRICES.USDINR };
let lastPair = $('pair').value;
// factor that turns an amount in the QUOTE currency into the ACCOUNT currency
function quoteToAcc() {
  const s = spec($('pair').value), a = $('acc').value, px = V('price');
  const show = on => { $('convBox').hidden = !on; };
  if (s.quote === a) { show(false); return 1; }
  if (s.base === a) { show(false); return px ? 1 / px : 0; }
  const qUsd = s.quote === 'USD' ? 1 : s.base === 'USD' ? (px ? 1 / px : 0) : null;
  if (qUsd !== null && (a === 'USD' || a === 'AED')) { show(false); return qUsd / USDV[a]; }
  show(true);
  $('convLabel').textContent = `1 ${s.quote} = ? ${a} (enter today's rate)`;
  return V('conv');
}
function fxWire(calc) {
  $('pair').addEventListener('change', () => { const p = $('pair').value; if (p !== lastPair) { $('price').value = PRICES[p]; lastPair = p; } fillConv(); calc(); });
  $('acc').addEventListener('change', () => { fillConv(); calc(); });
  document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc));
  calc();
}
function fillConv() { const s = spec($('pair').value); $('conv').value = +(USDV[s.quote] / USDV[$('acc').value]).toPrecision(6); }
""" % PRICES

TOOLS.append(dict(
group="trading", slug="forex-pip-value-calculator",
name="Pip Value Calculator",
title="Pip Value Calculator: Forex & Gold Pip Value per Lot in USD, AED, EUR, GBP",
desc="Free forex pip value calculator. Find the value of one pip for any lot size on EUR/USD, GBP/JPY, XAU/USD and more, in USD, AED, EUR, GBP or INR account currency.",
keywords="pip value calculator, forex pip calculator, pip calculator, gold pip value calculator, xauusd pip value, value of a pip per lot, pip value jpy pairs, mt5 pip calculator, pip value in aed",
h1="Pip value calculator",
lede="See what one pip is worth for your trade size and account currency.",
card="Value of one pip per lot in your currency",
tool=f"""
<div class="inputs">{FX_INPUTS}
 <div><label for="lots">Trade size (lots)</label><input id="lots" inputmode="decimal" value="1"><div class="hint">1 standard lot = 100,000 units of currency; 1 lot of gold = 100 oz.</div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Value of 1 pip</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul><p class="formula" id="formula"></p>
</div>""",
js=FXLIB + r"""
function calc() {
  const s = spec($('pair').value), lots = V('lots'), k = quoteToAcc(), a = $('acc').value;
  const pv = s.pip * s.cs * lots * k;
  $('out').textContent = a + ' ' + FX(pv, 2);
  $('lines').innerHTML = [['Pip size', s.pip], ['Units', FX(s.cs * lots, 0)], ['Per standard lot', a + ' ' + FX(s.pip * s.cs * k, 2)], ['Per mini lot (0.1)', a + ' ' + FX(s.pip * s.cs * k / 10, 2)], ['Per micro lot (0.01)', a + ' ' + FX(s.pip * s.cs * k / 100, 3)]].map(([x, y]) => `<li><span>${x}</span><b>${y}</b></li>`).join('');
  $('formula').textContent = `Pip value = pip size × units × (${s.quote} → ${a} rate)` + ($('pair').value === 'XAUUSD' ? '. Gold: many brokers call 0.10 a pip; multiply by 10 if yours does.' : '');
}
fxWire(calc);
""",
body="""
<h2>How pip value is calculated</h2>
<p><strong>Pip value = pip size × position size in units</strong>, which gives a value in the pair's quote currency. Convert that to your account currency if they differ.</p>
<ul><li>For most pairs a pip is <strong>0.0001</strong>. For JPY pairs it is <strong>0.01</strong>.</li>
<li>For any pair quoted in USD (EUR/USD, GBP/USD, AUD/USD), one standard lot is worth <strong>$10 per pip</strong>.</li>
<li>For USD/JPY at 150.00, one pip on one lot is ¥1,000, which is about $6.67.</li>
<li>For gold (XAU/USD, 100 oz per lot), a $0.01 move is worth $1 per lot.</li></ul>
<h3>Pip value in AED</h3>
<p>Because the dirham is pegged at 3.6725 per dollar, a $10 pip is worth AED 36.73. Select AED as your account currency and the calculator fills in the peg for you.</p>
""",
faqs=[
("How much is 1 pip worth on EUR/USD?", "On one standard lot (100,000 EUR) one pip is $10. On a mini lot it is $1 and on a micro lot $0.10."),
("How do I calculate pip value for JPY pairs?", "Multiply 0.01 by the position size to get the value in yen, then divide by the USD/JPY rate to get dollars."),
("What is a pip in gold?", "Brokers differ. In this calculator a pip on XAU/USD is $0.01, worth $1 per 100 oz lot. Many MT5 brokers call $0.10 a pip, which is $10 per lot."),
]))

TOOLS.append(dict(
group="trading", slug="position-size-calculator",
name="Position Size Calculator",
title="Position Size Calculator: Lot Size from Risk % and Stop Loss (Forex & Gold)",
desc="Free lot size calculator for forex and gold. Enter account balance, risk percentage and stop loss in pips to get the correct position size in lots for MT4/MT5.",
keywords="position size calculator, lot size calculator, forex lot size calculator, risk calculator forex, gold lot size calculator, mt5 lot size calculator, how many lots should i trade, risk management calculator, xauusd lot size",
h1="Position size calculator",
lede="Size every trade so that hitting your stop loss costs exactly the share of your account you planned to risk.",
card="Lot size from account risk and stop loss",
tool=f"""
<div class="inputs">
 <div class="row2"><div><label for="bal">Account balance</label><input id="bal" inputmode="decimal" value="10000"></div><div><label for="risk">Risk per trade (%)</label><input id="risk" inputmode="decimal" value="1"></div></div>
 <div><label for="sl">Stop loss (pips)</label><input id="sl" inputmode="decimal" value="25"></div>
 {FX_INPUTS}
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Position size</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul><p class="formula">Lots = (balance × risk %) ÷ (stop loss in pips × pip value per lot)</p>
</div>""",
js=FXLIB + r"""
function calc() {
  const s = spec($('pair').value), k = quoteToAcc(), a = $('acc').value;
  const riskAmt = V('bal') * V('risk') / 100, pvLot = s.pip * s.cs * k, sl = V('sl');
  const lots = sl && pvLot ? riskAmt / (sl * pvLot) : 0, rounded = Math.floor(lots * 100) / 100;
  $('out').textContent = FX(rounded, 2) + ' lots';
  $('lines').innerHTML = [['Amount at risk', a + ' ' + FX(riskAmt)], ['Pip value per lot', a + ' ' + FX(pvLot)], ['Exact size', FX(lots, 4) + ' lots'], ['Units', FX(rounded * s.cs, 0)], ['Loss if stopped out', a + ' ' + FX(rounded * sl * pvLot)]].map(([x, y]) => `<li><span>${x}</span><b>${y}</b></li>`).join('');
}
fxWire(calc);
""",
body="""
<h2>Why position sizing matters</h2>
<p>Most professional traders risk a fixed <strong>1–2% of their account</strong> per trade. The stop loss decides <em>where</em> you are wrong, and the position size decides <em>how much</em> being wrong costs you. Sizing every trade this way keeps a losing streak survivable.</p>
<h3>Worked example</h3>
<p>Balance $10,000, risk 1% = $100. Stop loss 25 pips on EUR/USD, where one lot is worth $10 a pip. Lots = 100 ÷ (25 × 10) = <strong>0.40 lots</strong>.</p>
<p>The calculator rounds <em>down</em> to the nearest 0.01 lot, so you never risk more than you planned. Spreads and commission add a little extra cost on top.</p>
""",
faqs=[
("How do I calculate lot size in forex?", "Divide the amount you are willing to lose by the stop loss in pips multiplied by the pip value per lot."),
("What percentage should I risk per trade?", "Many traders use 0.5–2%. Lower risk means smaller drawdowns during losing streaks."),
("Does this work for gold on MT5?", "Yes. Choose XAU/USD and enter your stop loss in $0.01 pips. If your broker counts $0.10 as a pip, multiply your stop by 10 first."),
]))

TOOLS.append(dict(
group="trading", slug="forex-margin-calculator",
name="Forex Margin Calculator",
title="Forex Margin Calculator: Required Margin by Leverage (1:30, 1:100, 1:500)",
desc="Free forex and gold margin calculator. Find the margin required to open a trade for any lot size and leverage, in USD, AED, EUR, GBP or INR.",
keywords="margin calculator, forex margin calculator, required margin calculator, leverage calculator, gold margin calculator, xauusd margin, margin for 1 lot, mt5 margin calculator, margin calculator 1:500",
h1="Forex margin calculator",
lede="Find how much margin your broker will lock up to open a position.",
card="Required margin for any lot size and leverage",
tool=f"""
<div class="inputs">{FX_INPUTS}
 <div class="row2"><div><label for="lots">Trade size (lots)</label><input id="lots" inputmode="decimal" value="1"></div>
 <div><label for="lev">Leverage</label><select id="lev"><option value="1">1:1</option><option value="10">1:10</option><option value="20">1:20</option><option value="30">1:30</option><option value="50">1:50</option><option value="100" selected>1:100</option><option value="200">1:200</option><option value="400">1:400</option><option value="500">1:500</option></select></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Required margin</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul><p class="formula">Margin = lots × contract size × price ÷ leverage, converted to your account currency</p>
</div>""",
js=FXLIB + r"""
function calc() {
  const s = spec($('pair').value), k = quoteToAcc(), a = $('acc').value, lev = V('lev') || 1;
  const notionalQ = V('lots') * s.cs * V('price'), notional = notionalQ * k, m = notional / lev;
  $('out').textContent = a + ' ' + FX(m);
  $('lines').innerHTML = [['Position value', a + ' ' + FX(notional)], ['Units', FX(V('lots') * s.cs, 0)], ['Margin rate', FX(100 / lev, 2) + '%']].map(([x, y]) => `<li><span>${x}</span><b>${y}</b></li>`).join('');
}
fxWire(calc);
""",
body="""
<h2>How margin works</h2>
<p>Margin is the deposit your broker holds while a leveraged position is open. With 1:100 leverage you put up 1% of the position's value. One standard lot of EUR/USD at 1.0850 is worth $108,500, so the margin at 1:100 is <strong>$1,085</strong>.</p>
<h3>Leverage limits</h3>
<p>Regulators cap retail leverage. In the UAE, the SCA sets limits by asset class for retail clients, and EU and UK rules cap major FX pairs at 1:30 for retail traders. Your broker's own margin requirements may be higher than this calculator shows, especially over weekends and news events.</p>
<h3>Free margin and margin level</h3>
<p>Margin level = equity ÷ used margin × 100%. Most brokers send a margin call around 100% and start closing positions at a stop-out level of 50% or lower.</p>
""",
faqs=[
("How much margin do I need for 1 lot of EUR/USD?", "At 1:100 leverage and a price of 1.0850, you need about $1,085. At 1:30 you need about $3,617."),
("How is margin calculated for gold?", "One lot of XAU/USD is 100 oz. At $2,650 the position is worth $265,000, so at 1:100 the margin is $2,650."),
("What happens if my margin level falls too low?", "You may get a margin call, and below the stop-out level the broker will automatically close positions."),
]))

TOOLS.append(dict(
group="trading", slug="swap-calculator",
name="Forex Swap Calculator",
title="Forex Swap Calculator: Overnight Rollover Cost incl. Triple Swap Wednesday",
desc="Free swap calculator for forex, gold and CFDs. Estimate overnight rollover charges or credits for your holding period, including the triple swap on Wednesday.",
keywords="swap calculator, forex swap calculator, rollover calculator, overnight swap cost, triple swap wednesday, mt5 swap calculator, gold swap calculator, cfd overnight financing calculator, swap long swap short",
h1="Forex swap calculator",
lede="Estimate the total overnight swap on a position held for several days.",
card="Overnight rollover with triple-swap days",
tool="""
<div class="inputs">
 <div class="row2"><div><label for="lots">Trade size (lots)</label><input id="lots" inputmode="decimal" value="1"></div>
 <div><label for="swap">Swap per lot per night</label><input id="swap" inputmode="decimal" value="-7.5"><div class="hint">In your account currency. Negative is a charge.</div></div></div>
 <div class="row2"><div><label for="open">Open date</label><input id="open" type="date" value="2026-11-16"></div><div><label for="close">Close date</label><input id="close" type="date" value="2026-11-23"></div></div>
 <div><label for="triple">Triple swap charged on</label><select id="triple"><option value="3" selected>Wednesday (forex, metals)</option><option value="5">Friday (many indices and CFDs)</option><option value="-1">No triple day</option></select></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Total swap</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul><p class="formula">Each weekday rollover counts once; the triple day counts three times to cover the weekend.</p>
</div>""",
js=r"""
function calc() {
  const o = new Date($('open').value + 'T12:00:00'), c = new Date($('close').value + 'T12:00:00'), t = +$('triple').value;
  let nights = 0, rolls = 0;
  if (!isNaN(o) && !isNaN(c)) for (let d = new Date(o); d < c; d.setDate(d.getDate() + 1)) { const w = d.getDay(); if (w === 0 || w === 6) continue; rolls++; nights += w === t ? 3 : 1; }
  const tot = V('lots') * V('swap') * nights;
  $('out').innerHTML = `<span class="${tot >= 0 ? 'up' : 'dn'}">${tot >= 0 ? '+' : '−'}${FX(Math.abs(tot))}</span>`;
  $('lines').innerHTML = [['Rollovers held', rolls], ['Swap nights charged', nights], ['Per night on your size', FX(V('lots') * V('swap'))]].map(([x, y]) => `<li><span>${x}</span><b>${y}</b></li>`).join('');
}
document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>What is a swap?</h2>
<p>A swap (or rollover) is the interest adjustment applied when you hold a leveraged position past the daily rollover, usually 5 pm New York time. It reflects the interest-rate difference between the two currencies, plus the broker's markup. It can be a charge or a credit.</p>
<h3>Why Wednesday is triple</h3>
<p>Spot forex settles two business days after the trade (T+2). A position held through Wednesday's rollover settles over the weekend, so three days of swap are applied at once. Many index and commodity CFDs apply the triple charge on Friday instead.</p>
<h3>Where to find your swap rates</h3>
<p>In MT4 and MT5, right-click the symbol in Market Watch, choose Specification, and read "Swap long" and "Swap short". If they are quoted in points, multiply by the pip value per point to get money per lot.</p>
""",
faqs=[
("How is forex swap calculated?", "Swap = lots × swap rate per lot per night × number of nights, with the triple-swap day counted as three nights."),
("Why is swap charged three times on Wednesday?", "Because of T+2 settlement, Wednesday's rollover covers the weekend, so three nights are charged together."),
("Are there swap-free accounts?", "Many brokers offer Islamic (swap-free) accounts, which may charge a fixed admin fee instead."),
]))

FUT = [("ES", "E-mini S&P 500", 0.25, 12.50), ("MES", "Micro E-mini S&P 500", 0.25, 1.25), ("NQ", "E-mini Nasdaq-100", 0.25, 5.00),
       ("MNQ", "Micro E-mini Nasdaq-100", 0.25, 0.50), ("YM", "E-mini Dow", 1, 5.00), ("CL", "Crude oil (WTI)", 0.01, 10.00),
       ("NG", "Natural gas", 0.001, 10.00), ("GC", "Gold", 0.10, 10.00), ("MGC", "Micro gold", 0.10, 1.00),
       ("SI", "Silver", 0.005, 25.00), ("6E", "Euro FX", 0.00005, 6.25)]
fut_opts = "".join(f'<option value="{s}">{s} · {n}</option>' for s, n, _, _ in FUT) + '<option value="custom">Custom contract</option>'
FUTJS = "{" + ",".join(f"'{s}':[{t},{v}]" for s, _, t, v in FUT) + "}"

TOOLS.append(dict(
group="trading", slug="futures-tick-value-calculator",
name="Futures Tick Value Calculator",
title="Futures Tick Value & P&L Calculator: ES, NQ, CL, GC, Micro Futures",
desc="Free futures tick value calculator. See tick size, tick value and profit or loss for E-mini S&P (ES), Nasdaq (NQ), crude oil (CL), gold (GC), micros and custom contracts.",
keywords="futures tick value calculator, futures profit calculator, es tick value, nq tick value, cl tick value, gold futures tick value, micro futures calculator, cme tick size, futures p&l calculator",
h1="Futures tick value calculator",
lede="Pick a contract, enter your entry and exit, and see how many ticks you made or lost and what they are worth.",
card="Tick value and P&L for CME contracts",
tool=f"""
<div class="inputs">
 <div><label for="ct">Contract</label><select id="ct">{fut_opts}</select></div>
 <div class="row2"><div><label for="ts">Tick size</label><input id="ts" inputmode="decimal" value="0.25"></div><div><label for="tv">Tick value (USD)</label><input id="tv" inputmode="decimal" value="12.50"></div></div>
 <div><label>Direction</label><div class="seg" id="dir"><button type="button" data-v="long" aria-pressed="true">Long (buy)</button><button type="button" data-v="short" aria-pressed="false">Short (sell)</button></div></div>
 <div class="row2"><div><label for="en">Entry price</label><input id="en" inputmode="decimal" value="6000.00"></div><div><label for="ex">Exit price</label><input id="ex" inputmode="decimal" value="6012.50"></div></div>
 <div class="row2"><div><label for="qty">Contracts</label><input id="qty" inputmode="numeric" value="2"></div><div><label for="fee">Round-turn fees per contract (USD)</label><input id="fee" inputmode="decimal" value="4.5"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Net profit / loss</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
</div>""",
js=r"""
const FUT = """ + FUTJS + r""";
let lastCt = $('ct').value;
$('ct').addEventListener('change', () => { const c = $('ct').value; if (FUT[c] && c !== lastCt) { $('ts').value = FUT[c][0]; $('tv').value = FUT[c][1].toFixed(2); } lastCt = c; calc(); });
const dir = seg('dir', () => calc());
function calc() {
  const ts = V('ts'), tv = V('tv'), q = V('qty'), mv = (V('ex') - V('en')) * (dir() === 'long' ? 1 : -1);
  const ticks = ts ? mv / ts : 0, gross = ticks * tv * q, net = gross - V('fee') * q;
  $('out').innerHTML = `<span class="${net >= 0 ? 'up' : 'dn'}">${net >= 0 ? '+' : '−'}$${FX(Math.abs(net))}</span>`;
  $('lines').innerHTML = [['Price move', FX(mv, 5).replace(/0+$/, '').replace(/\.$/, '')], ['Ticks', FX(ticks, 1)], ['Point value', '$' + FX(ts ? tv / ts : 0)], ['Gross P&L', '$' + FX(gross)], ['Fees', '$' + FX(V('fee') * q)]].map(([x, y]) => `<li><span>${x}</span><b>${y}</b></li>`).join('');
}
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>Tick size and tick value</h2>
<p>The <strong>tick size</strong> is the smallest price step a contract can move, and the <strong>tick value</strong> is what one tick is worth per contract. P&L = (exit − entry) ÷ tick size × tick value × contracts.</p>
<div class="scroll"><table><thead><tr><th>Symbol</th><th>Contract</th><th class="n">Tick size</th><th class="n">Tick value</th></tr></thead><tbody>
""" + "".join(f'<tr><td>{s}</td><td>{n}</td><td class="n">{t}</td><td class="n">${v:,.2f}</td></tr>' for s, n, t, v in FUT) + """
</tbody></table></div>
<p>Contract specifications can change. Check the exchange (CME Group) or your broker's contract specs before trading.</p>
""",
faqs=[
("What is the tick value of ES?", "The E-mini S&P 500 moves in 0.25-point ticks worth $12.50, which is $50 per full point."),
("What is the tick value of NQ?", "The E-mini Nasdaq-100 moves in 0.25-point ticks worth $5.00, which is $20 per point."),
("What is the tick value of crude oil futures (CL)?", "CL moves in $0.01 ticks worth $10 per contract, which is $1,000 per $1 move."),
("What is the tick value of gold futures (GC)?", "GC moves in $0.10 ticks worth $10 per contract."),
]))

MKTS = [
    ("NSE / BSE India", "Asia/Kolkata", [("09:15", "15:30")], [1, 2, 3, 4, 5]),
    ("GIFT Nifty (NSE IX)", "Asia/Kolkata", [("06:30", "15:40"), ("16:35", "02:45")], [1, 2, 3, 4, 5]),
    ("DFM / ADX (UAE)", "Asia/Dubai", [("10:00", "15:00")], [1, 2, 3, 4, 5]),
    ("Tadawul (Saudi)", "Asia/Riyadh", [("10:00", "15:00")], [0, 1, 2, 3, 4]),
    ("Tokyo (TSE)", "Asia/Tokyo", [("09:00", "11:30"), ("12:30", "15:30")], [1, 2, 3, 4, 5]),
    ("Hong Kong (HKEX)", "Asia/Hong_Kong", [("09:30", "12:00"), ("13:00", "16:00")], [1, 2, 3, 4, 5]),
    ("Shanghai (SSE)", "Asia/Shanghai", [("09:30", "11:30"), ("13:00", "15:00")], [1, 2, 3, 4, 5]),
    ("Singapore (SGX)", "Asia/Singapore", [("09:00", "12:00"), ("13:00", "17:00")], [1, 2, 3, 4, 5]),
    ("London (LSE)", "Europe/London", [("08:00", "16:30")], [1, 2, 3, 4, 5]),
    ("Frankfurt (Xetra)", "Europe/Berlin", [("09:00", "17:30")], [1, 2, 3, 4, 5]),
    ("New York (NYSE, Nasdaq)", "America/New_York", [("09:30", "16:00")], [1, 2, 3, 4, 5]),
    ("Forex: Sydney session", "Australia/Sydney", [("07:00", "16:00")], [1, 2, 3, 4, 5]),
    ("Forex: Tokyo session", "Asia/Tokyo", [("09:00", "18:00")], [1, 2, 3, 4, 5]),
    ("Forex: London session", "Europe/London", [("08:00", "17:00")], [1, 2, 3, 4, 5]),
    ("Forex: New York session", "America/New_York", [("08:00", "17:00")], [1, 2, 3, 4, 5]),
]
import json as _j
MKTJS = _j.dumps([[n, tz, s, d] for n, tz, s, d in MKTS])

TOOLS.append(dict(
group="trading", slug="market-hours",
name="World Market Hours",
title="Stock Market & Forex Session Hours Now: NSE, DFM, NYSE, London, Tokyo in UAE & IST Time",
desc="Live market hours clock. See which stock exchanges and forex sessions are open right now, with opening and closing times in Dubai (GST), India (IST) or your local time.",
keywords="market hours, forex market hours, stock market timings, is the market open now, nse timings, dfm trading hours, nyse hours in uae time, london session time in dubai, forex sessions ist, gift nifty timings",
h1="World market hours",
lede="Which exchanges and forex sessions are open right now, with every time converted to your chosen zone.",
card="Which markets are open right now",
tool="""
<div class="inputs" style="grid-column:1/-1">
 <div class="row2"><div><label for="tz">Show times in</label><select id="tz"><option value="local">My local time</option><option value="Asia/Dubai">Dubai (GST, UTC+4)</option><option value="Asia/Kolkata">India (IST, UTC+5:30)</option><option value="UTC">UTC / GMT</option></select></div>
 <div><div class="big-label">Time now</div><div class="big" id="now" style="font-size:36px">—</div></div></div>
 <div class="scroll"><table class="stack"><thead><tr><th>Market</th><th>Status</th><th>Opens – closes</th></tr></thead><tbody id="tb"></tbody></table></div>
 <p class="hint">Regular sessions only. Public holidays, pre-market and after-hours trading are not shown.</p>
</div>""",
js=r"""
const M = """ + MKTJS + r""";
const offset = (tz, d) => { const p = new Intl.DateTimeFormat('en-US', { timeZone: tz, hourCycle: 'h23', year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' }).formatToParts(d).reduce((a, x) => (a[x.type] = +x.value, a), {}); return Date.UTC(p.year, p.month - 1, p.day, p.hour, p.minute, p.second) - Math.floor(d / 1000) * 1000; };
const parts = (tz, d) => new Intl.DateTimeFormat('en-US', { timeZone: tz, hourCycle: 'h23', weekday: 'short', year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric' }).formatToParts(d).reduce((a, x) => (a[x.type] = x.value, a), {});
const WD = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
const at = (tz, y, m, dd, hm) => { const [h, mi] = hm.split(':').map(Number), g = Date.UTC(y, m - 1, dd, h, mi); return new Date(g - offset(tz, new Date(g))); };
function fmt(d) { const z = $('tz').value; return d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', ...(z === 'local' ? {} : { timeZone: z }) }); }
function draw() {
  const now = new Date(), z = $('tz').value;
  $('now').textContent = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', ...(z === 'local' ? {} : { timeZone: z }) });
  $('tb').innerHTML = M.map(([name, tz, sess, days]) => {
    const p = parts(tz, now), y = +p.year, mo = +p.month, d = +p.day, wd = WD[p.weekday];
    let open = false;
    const spans = sess.map(([a, b]) => {
      const s = at(tz, y, mo, d, a); let e = at(tz, y, mo, d, b);
      if (b < a) { e = new Date(e.getTime() + 864e5); const ps = new Date(s.getTime() - 864e5), pe = new Date(e.getTime() - 864e5); if (now >= ps && now < pe && days.includes((wd + 6) % 7)) open = true; }
      if (now >= s && now < e && days.includes(wd)) open = true;
      return fmt(s) + '–' + fmt(e);
    }).join(', ');
    return `<tr><td>${name}</td><td class="${open ? 'up' : 'dn'}">${open ? 'Open' : 'Closed'}</td><td>${spans}</td></tr>`;
  }).join('');
}
$('tz').addEventListener('input', draw); draw(); setInterval(draw, 30000);
""",
body="""
<h2>Key market hours in UAE and India time</h2>
<ul><li><strong>NSE and BSE India:</strong> 09:15–15:30 IST (07:45–14:00 in Dubai).</li>
<li><strong>GIFT Nifty:</strong> 06:30–15:40 and 16:35–02:45 IST, almost 21 hours a day.</li>
<li><strong>DFM and ADX:</strong> 10:00–15:00 Gulf Standard Time, Monday to Friday.</li>
<li><strong>London:</strong> 08:00–16:30 UK time, which is 12:00–20:30 in Dubai in winter.</li>
<li><strong>New York:</strong> 09:30–16:00 Eastern, which is 18:30–01:00 in Dubai in winter and 17:30–00:00 in summer.</li></ul>
<h3>Forex sessions</h3>
<p>The forex market runs 24 hours a day, five days a week, passing from Sydney to Tokyo, London and New York. Liquidity and volatility are highest during the London–New York overlap. The times above change when the US, UK and Australia switch daylight saving, and this clock adjusts for that automatically.</p>
""",
faqs=[
("What time does the US stock market open in Dubai?", "NYSE and Nasdaq open at 9:30 am New York time: 6:30 pm in Dubai in winter, 5:30 pm during US daylight saving time."),
("What are the NSE market timings in UAE time?", "NSE trades 9:15 am to 3:30 pm IST, which is 7:45 am to 2:00 pm in the UAE."),
("When is the London session in IST?", "London opens at 8:00 am UK time: 1:30 pm IST in winter and 12:30 pm IST in British Summer Time."),
("Is the forex market open on weekends?", "No. Forex trading opens on Monday morning in Sydney (Sunday evening in Europe and the US) and closes on Friday at 5 pm New York time."),
]))
