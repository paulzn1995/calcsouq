from tools_trading import TOOLS

UNITS = [("sqft", "Square feet", 1), ("cent", "Cent", 435.6), ("acre", "Acre", 43560), ("sqm", "Square metre", 10.7639104),
         ("are", "Are", 1076.39104), ("hectare", "Hectare", 107639.104), ("sqyd", "Square yard", 9)]
unit_opts = "".join(f'<option value="{k}"{" selected" if k=="cent" else ""}>{n}</option>' for k, n, _ in UNITS)
UJS = "{" + ",".join(f'{k}:["{n}",{f}]' for k, n, f in UNITS) + "}"

TOOLS.append(dict(
group="india", slug="kerala-land-converter",
name="Kerala Land Area Converter",
title="Cent to Square Feet Converter: Kerala Land Area Calculator (Cent, Acre, Are, Hectare)",
desc="Convert Kerala land measurements instantly: cent to square feet, acre to cent, are to cent, hectare, square metre and square yard. 1 cent = 435.6 sq ft.",
keywords="cent to square feet, cent to sq ft, kerala land calculator, acre to cent, cent to acre, are to cent, cent to square metre, land area converter kerala, 1 cent in sq ft, hectare to cent",
h1="Kerala land area converter",
lede="Convert between cents, acres, ares, hectares, square feet, square metres and square yards.",
card="Cent, acre, are, sq ft and more",
tool=f"""
<div class="inputs">
 <div class="row2"><div><label for="val">Area</label><input id="val" inputmode="decimal" value="10"></div><div><label for="unit">Unit</label><select id="unit">{unit_opts}</select></div></div>
 <p class="hint">1 cent = 435.6 sq ft = 40.47 m². 100 cents = 1 acre. 1 are = 2.471 cents.</p>
</div>
<div class="result" aria-live="polite">
 <div class="big-label" id="bigLabel">In square feet</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
</div>""",
js=r"""
const U = """ + UJS + r""";
const pl = n => /feet$/i.test(n) ? n : n + 's';
function calc() {
  const sq = V('val') * U[$('unit').value][1];
  const tgt = $('unit').value === 'sqft' ? 'cent' : 'sqft';
  $('bigLabel').textContent = 'In ' + pl(U[tgt][0]).toLowerCase();
  $('out').textContent = F(sq / U[tgt][1], tgt === 'sqft' ? 0 : 3);
  $('lines').innerHTML = Object.entries(U).filter(([k]) => k !== $('unit').value).map(([k, [n, f]]) => `<li><span>${pl(n)}</span><b>${F(sq / f, sq / f < 10 ? 4 : 2)}</b></li>`).join('');
}
document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>Land measurement units used in Kerala</h2>
<div class="scroll"><table><thead><tr><th>Unit</th><th class="n">Square feet</th><th class="n">Cents</th></tr></thead><tbody>
<tr><td>1 cent</td><td class="n">435.6</td><td class="n">1</td></tr>
<tr><td>1 are</td><td class="n">1,076.39</td><td class="n">2.471</td></tr>
<tr><td>1 acre</td><td class="n">43,560</td><td class="n">100</td></tr>
<tr><td>1 hectare</td><td class="n">1,07,639</td><td class="n">247.1</td></tr>
<tr><td>1 square metre</td><td class="n">10.764</td><td class="n">0.0247</td></tr></tbody></table></div>
<p>Land in Kerala is usually sold by the <strong>cent</strong>, while revenue records (the thandaper and the Bhoomi records) often list area in <strong>ares</strong> and <strong>hectares</strong>. One are is 100 square metres, and one hectare is 100 ares.</p>
<h3>Quick examples</h3>
<ul><li>5 cents = 2,178 sq ft, about the size of a typical house plot.</li><li>10 cents = 4,356 sq ft = 404.7 m².</li><li>50 cents = half an acre = 21,780 sq ft.</li></ul>
""",
faqs=[
("How many square feet are in 1 cent?", "One cent is 435.6 square feet, or about 40.47 square metres."),
("How many cents are in 1 acre?", "There are 100 cents in one acre."),
("How many cents are in 1 are?", "One are is 100 square metres, which is about 2.471 cents."),
("How do I convert hectare to cent?", "Multiply hectares by 247.1. For example, 0.5 hectare is about 123.55 cents."),
]))

TOOLS.append(dict(
group="india", slug="kerala-stamp-duty-calculator",
name="Kerala Stamp Duty Calculator",
title="Kerala Stamp Duty & Registration Fee Calculator 2026 (8% + 2%)",
desc="Calculate stamp duty and registration charges for land and property in Kerala. 8% stamp duty plus 2% registration fee on the higher of fair value and sale price.",
keywords="kerala stamp duty calculator, land registration fee kerala, kerala registration charges, stamp duty kerala 2026, property registration kerala calculator, fair value kerala, land registration cost kerala, panchayat land registration fee",
h1="Kerala stamp duty calculator",
lede="Estimate the government charges to register a sale deed in Kerala.",
card="8% stamp duty + 2% registration fee",
tool="""
<div class="inputs">
 <div><label for="fv">Fair value of the land (₹)</label><input id="fv" inputmode="decimal" value="2500000"><div class="hint">The government-notified fair value. Check it on the Kerala Registration Department website.</div></div>
 <div><label for="sp">Sale price in the deed (₹)</label><input id="sp" inputmode="decimal" value="3000000"></div>
 <div class="row2"><div><label for="sd">Stamp duty (%)</label><input id="sd" inputmode="decimal" value="8"></div><div><label for="rf">Registration fee (%)</label><input id="rf" inputmode="decimal" value="2"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Total government charges</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul><p class="formula">Charges are worked out on the higher of fair value and sale price.</p>
</div>""",
js=r"""
function calc() {
  const base = Math.max(V('fv'), V('sp')), sd = base * V('sd') / 100, rf = base * V('rf') / 100;
  $('out').textContent = '₹' + F(sd + rf, 0);
  $('lines').innerHTML = [['Value used', base], ['Stamp duty', sd], ['Registration fee', rf], ['Total cost of the property', base + sd + rf]].map(([a, v]) => `<li><span>${a}</span><b>₹${F(v, 0)}</b></li>`).join('');
}
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>Stamp duty and registration charges in Kerala</h2>
<p>For an ordinary sale deed in Kerala, the Registration Department charges <strong>8% stamp duty</strong> and a <strong>2% registration fee</strong>, about 10% in total. Both are worked out on the <strong>higher</strong> of the government fair value and the sale price in the deed. The rate is the same for men, women and joint buyers, and in panchayat, municipality and corporation areas.</p>
<h3>Worked example</h3>
<p>Fair value ₹25 lakh, sale price ₹30 lakh. Charges are worked out on ₹30 lakh: stamp duty ₹2,40,000 + registration fee ₹60,000 = <strong>₹3,00,000</strong>.</p>
<h3>Other deeds</h3>
<p>Gift, settlement and partition deeds between family members, and lease deeds, have different and often much lower rates. Document writer fees and e-stamp charges are extra. Confirm the current rates with the sub-registrar office or keralaregistration.gov.in before registering.</p>
<h3>Buying land in Kerala from the Gulf</h3>
<p>NRIs can buy residential and commercial land in India, but not agricultural land, plantations or farmhouses. If you cannot travel, a registered power of attorney attested at the Indian embassy or consulate lets a relative sign on your behalf.</p>
""",
faqs=[
("What is the stamp duty in Kerala?", "Stamp duty on a sale deed is 8% of the higher of fair value and sale price, plus a 2% registration fee."),
("Is there a lower stamp duty for women in Kerala?", "No. Kerala charges the same 8% stamp duty and 2% registration fee for all buyers."),
("What is fair value in Kerala?", "Fair value is the minimum land value notified by the government for each survey number. Charges are based on whichever is higher: the fair value or the deed value."),
("Can an NRI buy land in Kerala?", "Yes, NRIs can buy residential and commercial property, but not agricultural land, plantations or farmhouses."),
]))
