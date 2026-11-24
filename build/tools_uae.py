TOOLS = []

TOOLS.append(dict(
group="uae", slug="uae-gratuity-calculator",
name="UAE Gratuity Calculator",
title="UAE Gratuity Calculator 2026: End of Service Benefits (New Labour Law)",
desc="Free UAE gratuity calculator for 2026. Work out your end of service benefit under the new UAE Labour Law: 21 days' basic salary for the first 5 years, 30 days after, capped at 2 years.",
keywords="uae gratuity calculator, gratuity calculator uae 2026, end of service calculator uae, eosb calculator, mohre gratuity calculator, dubai gratuity calculator, abu dhabi gratuity, gratuity after resignation uae, new labour law gratuity",
h1="UAE gratuity calculator",
lede="Enter your last basic salary and your joining and leaving dates to estimate your end-of-service gratuity under Federal Decree-Law No. 33 of 2021.",
card="End-of-service benefit under the new labour law",
tool="""
<div class="inputs">
 <div><label for="basic">Last basic monthly salary (AED)</label><input id="basic" inputmode="decimal" value="8000"><div class="hint">Basic salary only, without housing, transport or other allowances.</div></div>
 <div class="row2"><div><label for="start">Joining date</label><input id="start" type="date" value="2021-03-01"></div><div><label for="end">Last working day</label><input id="end" type="date" value="2026-11-20"></div></div>
 <div><label for="unpaid">Unpaid leave days</label><input id="unpaid" inputmode="numeric" value="0"><div class="hint">Days of unpaid absence are not counted as service.</div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Estimated gratuity</div><div class="big" id="out">—</div>
 <div id="msg" class="formula"></div>
 <ul class="lines" id="lines"></ul>
</div>""",
js=r"""
const calc = () => {
  const b = V('basic'), s = new Date($('start').value), e = new Date($('end').value), unpaid = V('unpaid');
  const L = $('lines'), M = $('msg');
  if (!b || isNaN(s) || isNaN(e) || e <= s) { $('out').textContent = 'AED 0.00'; L.innerHTML = ''; M.textContent = 'Enter your basic salary and both dates.'; return; }
  const days = Math.round((e - s) / 864e5) + 1 - unpaid, yrs = days / 365, daily = b / 30;
  if (yrs < 1) { $('out').textContent = 'AED 0.00'; L.innerHTML = ''; M.textContent = 'Less than one year of continuous service, so no gratuity is due.'; return; }
  const y1 = Math.min(yrs, 5), y2 = Math.max(yrs - 5, 0), p1 = daily * 21 * y1, p2 = daily * 30 * y2, cap = b * 24;
  const raw = p1 + p2, tot = Math.min(raw, cap);
  $('out').textContent = 'AED ' + FX(tot);
  M.textContent = raw > cap ? 'Capped at two years of basic salary.' : 'Paid within 14 days of the end of your contract.';
  L.innerHTML = [
    ['Service counted', F(yrs, 2) + ' years (' + days.toLocaleString() + ' days)'],
    ['Daily basic wage', 'AED ' + FX(daily)],
    ['First 5 years: 21 days × ' + F(y1, 2) + ' yrs', 'AED ' + FX(p1)],
    ['After 5 years: 30 days × ' + F(y2, 2) + ' yrs', 'AED ' + FX(p2)],
    ['Maximum (24 × basic)', 'AED ' + FX(cap)]
  ].map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
};
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>How UAE gratuity is calculated</h2>
<p>Under Article 51 of the UAE Labour Law (Federal Decree-Law No. 33 of 2021), a full-time employee in the private sector who completes at least one year of continuous service is entitled to an end-of-service gratuity based on their last <strong>basic</strong> wage:</p>
<ul><li><strong>21 days' basic salary</strong> for each of the first five years of service.</li>
<li><strong>30 days' basic salary</strong> for each year after the fifth.</li>
<li>Part years are paid pro rata once you pass one year.</li>
<li>The total cannot exceed <strong>two years' basic salary</strong>.</li></ul>
<p>The daily wage is your monthly basic salary divided by 30. Days of unpaid leave are taken out of your service period.</p>
<h3>Worked example</h3>
<p>Basic salary AED 8,000, service of 3 years and 6 months. Daily wage = 8,000 ÷ 30 = AED 266.67. Gratuity = 266.67 × 21 × 3.5 = <strong>AED 19,600</strong>.</p>
<h3>Resignation vs termination</h3>
<p>Under the new law, resigning no longer reduces gratuity. You receive the same amount whether you resign or are terminated, and gratuity is still payable even after a dismissal without notice under Article 44 (under the old law it could be forfeited). Your employer may deduct amounts you genuinely owe them.</p>
<h3>Who this calculator does not cover</h3>
<p>UAE nationals in GPSSA pension schemes, government employees, DIFC and ADGM employees (who have their own schemes, such as DEWS) and domestic workers follow different rules. Check with your HR team or MOHRE for your exact entitlement.</p>
""",
faqs=[
("How much gratuity will I get after 5 years in the UAE?", "After exactly five years you get 21 days' basic salary for each year, which is 105 days' basic pay. With a basic salary of AED 10,000 that is 10,000 ÷ 30 × 105 = AED 35,000."),
("Is gratuity calculated on basic or gross salary?", "On your last basic salary only. Housing, transport and other allowances are not included unless your contract says otherwise."),
("Do I get gratuity if I resign before one year?", "No. Gratuity is only due after at least one year of continuous service."),
("Is gratuity reduced if I resign under the new labour law?", "No. The old reductions for resigning (one third or two thirds) were removed for private-sector employees on the new limited contracts."),
("Is there a maximum gratuity amount?", "Yes. The total end-of-service gratuity cannot exceed two years' wages."),
("When must my employer pay my gratuity?", "Your employer must pay all end-of-service dues within 14 days of the end of your contract."),
]))

TOOLS.append(dict(
group="uae", slug="uae-vat-calculator",
name="UAE VAT Calculator",
title="UAE VAT Calculator: Add or Remove 5% VAT Online",
desc="Free UAE VAT calculator. Add 5% VAT to a price or remove VAT from a VAT-inclusive amount in AED instantly. Also works for Saudi 15% and other GCC rates.",
keywords="uae vat calculator, vat calculator uae, 5% vat calculator, remove vat calculator, reverse vat calculator uae, vat inclusive calculator, dubai vat calculator, how to calculate vat in uae, ksa vat calculator 15%",
h1="UAE VAT calculator",
lede="Add 5% VAT to a net price, or take the VAT out of a price that already includes it.",
card="Add or remove 5% VAT in AED",
tool="""
<div class="inputs">
 <div><label>What do you want to do?</label><div class="seg" id="mode"><button type="button" data-v="add" aria-pressed="true">Add VAT</button><button type="button" data-v="remove" aria-pressed="false">Remove VAT</button></div></div>
 <div><label for="amt" id="amtLabel">Amount before VAT (AED)</label><input id="amt" inputmode="decimal" value="1000"></div>
 <div><label for="rate">VAT rate (%)</label><select id="rate"><option value="5" selected>5% · UAE, Oman</option><option value="15">15% · Saudi Arabia</option><option value="10">10% · Bahrain</option><option value="0">0% · zero-rated</option></select></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label" id="bigLabel">Total including VAT</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p class="formula" id="formula"></p>
</div>""",
js=r"""
let mode = seg('mode', () => calc());
function calc() {
  const a = V('amt'), r = V('rate') / 100, m = mode();
  $('amtLabel').textContent = m === 'add' ? 'Amount before VAT (AED)' : 'Amount including VAT (AED)';
  const net = m === 'add' ? a : a / (1 + r), vat = net * r, gross = net + vat;
  $('bigLabel').textContent = m === 'add' ? 'Total including VAT' : 'Amount before VAT';
  $('out').textContent = 'AED ' + FX(m === 'add' ? gross : net);
  $('lines').innerHTML = [['Net amount', net], ['VAT at ' + (r * 100) + '%', vat], ['Gross amount', gross]].map(([k, v]) => `<li><span>${k}</span><b>AED ${FX(v)}</b></li>`).join('');
  $('formula').textContent = m === 'add' ? `Gross = net × ${1 + r}` : `Net = gross ÷ ${1 + r}; VAT = gross − net`;
}
document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>How to calculate VAT in the UAE</h2>
<p>The standard VAT rate in the UAE is <strong>5%</strong>, administered by the Federal Tax Authority (FTA).</p>
<ul><li><strong>To add VAT:</strong> multiply the net price by 1.05. AED 1,000 + 5% = AED 1,050.</li>
<li><strong>To remove VAT:</strong> divide the VAT-inclusive price by 1.05. AED 1,050 ÷ 1.05 = AED 1,000, so the VAT is AED 50.</li>
<li>A common mistake is to take 5% off the gross price. That gives AED 997.50, which is wrong.</li></ul>
<h3>Zero-rated and exempt items</h3>
<p>Some supplies are zero-rated, including exports, international transport, certain education and healthcare services, and investment-grade precious metals. Residential rent and local passenger transport are exempt. Retail gold jewellery is charged at 5%.</p>
<h3>GCC VAT rates</h3>
<table><thead><tr><th>Country</th><th class="n">Standard VAT</th></tr></thead><tbody>
<tr><td>United Arab Emirates</td><td class="n">5%</td></tr><tr><td>Saudi Arabia</td><td class="n">15%</td></tr><tr><td>Bahrain</td><td class="n">10%</td></tr><tr><td>Oman</td><td class="n">5%</td></tr></tbody></table>
""",
faqs=[
("How do I calculate 5% VAT on a price?", "Multiply the price by 0.05 to get the VAT, or by 1.05 to get the total including VAT."),
("How do I remove VAT from a total in the UAE?", "Divide the total by 1.05. The result is the price before VAT, and the difference is the VAT amount."),
("Is VAT charged on rent in Dubai?", "Residential rent is exempt from VAT. Commercial rent is charged at 5%."),
("Can tourists get a VAT refund in the UAE?", "Yes. Tourists can claim back VAT on eligible purchases from shops in the Planet tax-free scheme when they leave the UAE, minus a processing fee."),
]))

TOOLS.append(dict(
group="uae", slug="gold-price-calculator",
name="Gold Jewellery Price Calculator",
title="Gold Price Calculator UAE & India: Jewellery Price with Making Charges & VAT/GST",
desc="Calculate the final price of gold jewellery in Dubai or India: gold rate per gram × weight + making charges + 5% UAE VAT or 3% GST. Works for 24K, 22K, 21K and 18K.",
keywords="gold price calculator, gold jewellery price calculator, gold rate calculator dubai, 22k gold price calculator, making charges calculator, gold calculator uae, gold price calculator india gst, gold rate per gram calculator, gold vat uae",
h1="Gold jewellery price calculator",
lede="Work out what a piece of gold jewellery should cost from today's rate, its weight, the jeweller's making charge and tax.",
card="Rate × weight + making charge + VAT or GST",
tool="""
<div class="inputs">
 <div><label>Where are you buying?</label><div class="seg" id="ctry"><button type="button" data-v="uae" aria-pressed="true">UAE (AED)</button><button type="button" data-v="in" aria-pressed="false">India (₹)</button></div></div>
 <div class="row2"><div><label for="karat">Purity</label><select id="karat"><option value="24">24K (99.9%)</option><option value="22" selected>22K (91.6%)</option><option value="21">21K (87.5%)</option><option value="18">18K (75%)</option></select></div>
 <div><label for="wt">Weight (grams)</label><input id="wt" inputmode="decimal" value="10"></div></div>
 <div><label for="rate" id="rateLabel">Rate per gram</label><input id="rate" inputmode="decimal" value="320"><div class="hint">Sample rate. Enter today's rate from your jeweller or the gold association.</div></div>
 <label class="check"><input type="checkbox" id="is24"> The rate I entered is the 24K rate (convert it to my purity)</label>
 <div><label>Making charge</label><div class="seg" id="mk"><button type="button" data-v="pct" aria-pressed="true">% of gold value</button><button type="button" data-v="gram" aria-pressed="false">Per gram</button></div></div>
 <div class="row2"><div><label for="mkv">Making charge value</label><input id="mkv" inputmode="decimal" value="8"></div><div><label for="tax" id="taxLabel">VAT (%)</label><input id="tax" inputmode="decimal" value="5"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Final price</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p class="formula" id="note"></p>
</div>""",
js=r"""
const PUR = { 24: 0.999, 22: 0.916, 21: 0.875, 18: 0.75 };
let lastC = null;
const ctry = seg('ctry', c => { if (lastC && lastC !== c) $('tax').value = c === 'uae' ? 5 : 3; lastC = c; calc(); });
const mk = seg('mk', () => calc());
lastC = ctry();
function calc() {
  const c = ctry(), cur = c === 'uae' ? 'AED ' : '₹', k = +$('karat').value;
  $('taxLabel').textContent = c === 'uae' ? 'VAT (%)' : 'GST (%)';
  $('rateLabel').textContent = `Rate per gram (${c === 'uae' ? 'AED' : '₹'})`;
  const rate = $('is24').checked ? V('rate') * PUR[k] / PUR[24] : V('rate');
  const gold = rate * V('wt'), making = mk() === 'pct' ? gold * V('mkv') / 100 : V('mkv') * V('wt');
  const tax = (gold + making) * V('tax') / 100, tot = gold + making + tax;
  const F = c === 'uae' ? FX : window.F;
  $('out').textContent = cur + F(tot);
  $('lines').innerHTML = [[`${k}K rate per gram`, rate], ['Gold value', gold], ['Making charge', making], [(c === 'uae' ? 'VAT ' : 'GST ') + V('tax') + '%', tax]].map(([a, v]) => `<li><span>${a}</span><b>${cur}${F(v)}</b></li>`).join('');
  $('note').textContent = c === 'uae' ? 'UAE: 5% VAT applies to the full price of jewellery, including making charges. Tourists can reclaim it at departure.' : 'India: 3% GST applies to the value of the jewellery, including making charges.';
}
document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>How the price of gold jewellery is worked out</h2>
<p><strong>Final price = (gold rate per gram × weight) + making charges + tax</strong></p>
<ul><li><strong>Gold rate:</strong> the published rate for the purity you are buying (24K, 22K, 21K or 18K).</li>
<li><strong>Making charge:</strong> the jeweller's fee for crafting the piece. It is quoted either as a percentage of the gold value or as a fixed amount per gram, and is often negotiable.</li>
<li><strong>UAE:</strong> 5% VAT is charged on the full price, including making charges. Investment bullion of 99% purity or more is zero-rated.</li>
<li><strong>India:</strong> 3% GST is charged on the jewellery value, including making charges.</li></ul>
<h3>Converting the 24K rate to other purities</h3>
<p>If you only know the 24K rate, multiply it by the purity: 22K ≈ 91.6%, 21K = 87.5% and 18K = 75%. Tick the box in the calculator to do this automatically. Jewellers' published 22K rates can differ slightly from this conversion.</p>
<h3>Tips before you buy</h3>
<ul><li>Ask for the gold value, making charge and tax as separate lines on the invoice.</li>
<li>Check for hallmarking: BIS HUID in India, or the Dubai Central Laboratory hallmark in Dubai.</li>
<li>Stone weight should not be charged at the gold rate.</li></ul>
""",
faqs=[
("How is the gold jewellery price calculated in Dubai?", "Multiply the gold rate per gram for your purity by the weight, add the making charge, then add 5% VAT on the total."),
("Is VAT charged on making charges in the UAE?", "Yes. Retail gold jewellery carries 5% VAT on the full sale value, including making charges."),
("What is the GST on gold jewellery in India?", "3% GST is charged on the value of gold jewellery, including making charges."),
("What are typical making charges?", "They vary widely by design and shop, from a few percent for plain chains to 20% or more for intricate pieces. Always compare and negotiate."),
]))

TOOLS.append(dict(
group="uae", slug="aed-to-inr-calculator",
name="AED to INR Remittance Calculator",
title="AED to INR Calculator: Compare Exchange Rates & Fees for Sending Money to India",
desc="Free AED to INR remittance calculator. Enter the rate and fee from each exchange house or app and see exactly how many rupees reach India and which option gives the best effective rate.",
keywords="aed to inr calculator, dirham to rupee calculator, uae to india money transfer calculator, remittance calculator uae, best exchange rate aed to inr, send money to india from uae, aed inr effective rate, exchange house comparison uae",
h1="AED to INR remittance calculator",
lede="Compare up to three exchange houses or apps. Enter the rate and fee each one quotes you, and see which one actually delivers the most rupees.",
card="Compare exchange houses by rupees received",
tool="""
<div class="inputs">
 <div><label for="amt">Amount to send (AED)</label><input id="amt" inputmode="decimal" value="5000"></div>
 <div class="row2"><div><label for="n1">Option 1</label><input id="n1" value="Exchange house"></div><div class="row2"><div><label for="r1">Rate (₹ per AED)</label><input id="r1" inputmode="decimal" value="24.10"></div><div><label for="f1">Fee (AED)</label><input id="f1" inputmode="decimal" value="22"></div></div></div>
 <div class="row2"><div><label for="n2">Option 2</label><input id="n2" value="Bank app"></div><div class="row2"><div><label for="r2">Rate (₹ per AED)</label><input id="r2" inputmode="decimal" value="24.02"></div><div><label for="f2">Fee (AED)</label><input id="f2" inputmode="decimal" value="0"></div></div></div>
 <div class="row2"><div><label for="n3">Option 3</label><input id="n3" value="Online transfer app"></div><div class="row2"><div><label for="r3">Rate (₹ per AED)</label><input id="r3" inputmode="decimal" value="24.16"></div><div><label for="f3">Fee (AED)</label><input id="f3" inputmode="decimal" value="15"></div></div></div>
 <div class="hint">Sample rates and fees. Enter the quotes you see today.</div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label" id="bestLabel">Best option</div><div class="big" id="out">—</div>
 <div class="scroll"><table><thead><tr><th>Option</th><th class="n">₹ received</th><th class="n">Effective rate</th></tr></thead><tbody id="tb"></tbody></table></div>
 <p class="formula">Effective rate = rupees received ÷ total AED paid, including the fee.</p>
</div>""",
js=r"""
function calc() {
  const a = V('amt');
  const rows = [1, 2, 3].map(i => ({ n: $('n' + i).value || 'Option ' + i, r: V('r' + i), f: V('f' + i) })).filter(o => o.r > 0)
    .map(o => ({ ...o, inr: a * o.r, eff: a + o.f > 0 ? a * o.r / (a + o.f) : 0 })).sort((x, y) => y.eff - x.eff);
  if (!rows.length || !a) { $('out').textContent = '₹0'; $('tb').innerHTML = ''; return; }
  const b = rows[0];
  $('bestLabel').textContent = 'Best: ' + b.n;
  $('out').textContent = '₹' + F(b.inr, 0);
  $('tb').innerHTML = rows.map((o, i) => `<tr><td>${o.n.replace(/[<>&]/g, '')}${i ? `<br><small class="dn">₹${F((b.eff - o.eff) * (a + o.f), 0)} less</small>` : ''}</td><td class="n">₹${F(o.inr, 0)}</td><td class="n">${F(o.eff, 4)}</td></tr>`).join('');
}
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>Why the headline rate isn't the whole story</h2>
<p>Exchange houses and apps make money in two ways: the <strong>exchange rate margin</strong> and a <strong>fixed transfer fee</strong>. A provider with a slightly lower rate but no fee can beat one with a better rate and a high fee, especially for smaller amounts.</p>
<p>This calculator converts every quote into an <strong>effective rate</strong>: the rupees your family actually receives divided by everything you pay in dirhams. The highest effective rate is the best deal.</p>
<h3>Tips for sending money from the UAE to India</h3>
<ul><li>Compare quotes on the same day and at the same time, because rates move during the day.</li>
<li>Larger transfers dilute the fixed fee. Combining two small transfers into one usually saves money.</li>
<li>Remittances to an NRE account can be repatriated. Money sent to an NRO account may face limits on taking it back out.</li>
<li>The AED is pegged to the US dollar at 3.6725, so the AED/INR rate moves with USD/INR.</li></ul>
""",
faqs=[
("How do I calculate AED to INR?", "Multiply the dirham amount by the rupees-per-dirham rate. For example, AED 1,000 × 24.10 = ₹24,100."),
("What is an effective exchange rate?", "It is the rupees received divided by the total dirhams you pay, including fees. It lets you compare providers fairly."),
("Is it cheaper to send money through an app or an exchange house?", "It depends on the day's rate and fee. Enter both quotes in this calculator to see which delivers more rupees."),
("Why is the AED to INR rate linked to the US dollar?", "The UAE dirham is pegged to the US dollar at 3.6725, so AED/INR moves almost exactly with USD/INR."),
]))
