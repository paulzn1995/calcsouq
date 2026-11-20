from tools_photo import TOOLS

ROW = "`<li><span>${a}</span><b>${v}</b></li>`"

# ---------------- Image to PDF ----------------
TOOLS.append(dict(
group="docs", slug="image-to-pdf", icon="guide",
name="Image to PDF (JPG to PDF)",
title="JPG to PDF: Convert Images to PDF Online, Free and Private",
desc="Combine photos and scans into one PDF on your phone or computer. Reorder pages, choose A4 or original size, set quality. Nothing is uploaded.",
keywords="jpg to pdf, image to pdf, convert photo to pdf, png to pdf, combine images into pdf, jpg to pdf on mobile, scan to pdf, picture to pdf free",
h1="Image to PDF converter",
lede="Turn photos, screenshots and scanned pages into a single PDF. Reorder the pages, pick the page size and download. Your files never leave your device.",
card="Combine photos into one PDF, private",
tool="""
<div class="inputs">
 <div class="photo-pick" style="margin:0"><label class="btn primary pick-btn">Add images<input type="file" id="files" accept="image/*" multiple></label><span class="hint" id="cnt" style="margin:0">JPG, PNG or WebP. Add as many as you need.</span></div>
 <ol class="pdf-list" id="list"></ol>
 <div class="row2"><div><label for="psize">Page size</label><select id="psize"><option value="a4">A4</option><option value="letter">US Letter</option><option value="fit">Same as image</option></select></div>
 <div><label for="orient">Orientation</label><select id="orient"><option value="auto">Automatic</option><option value="p">Portrait</option><option value="l">Landscape</option></select></div></div>
 <div class="row2"><div><label for="margin">Margin</label><select id="margin"><option value="0">None</option><option value="20" selected>Small</option><option value="40">Large</option></select></div>
 <div><label for="qual">Quality</label><select id="qual"><option value="h">High (larger file)</option><option value="m" selected>Medium</option><option value="s">Small file</option></select></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Your PDF</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p style="margin:14px 0 0"><button type="button" class="btn primary" id="make" disabled>Create PDF</button> <a class="btn" id="dl" href="#" download="images.pdf" hidden>Download PDF</a></p>
 <p class="formula">Pages appear in the order shown. Use the arrows to move a page.</p>
</div>""",
js=r"""
let items = [], url = null;
const SIZES = { a4: [595.28, 841.89], letter: [612, 792] }, Q = { h: [2400, 0.9], m: [1700, 0.82], s: [1200, 0.7] };
function render() {
  $('list').innerHTML = items.map((it, i) => `<li><img src="${it.url}" alt=""><span>${i + 1}. ${it.name}</span><button type="button" data-a="up" data-i="${i}" aria-label="Move up">↑</button><button type="button" data-a="dn" data-i="${i}" aria-label="Move down">↓</button><button type="button" data-a="rm" data-i="${i}" aria-label="Remove">✕</button></li>`).join('');
  $('cnt').textContent = items.length ? items.length + (items.length === 1 ? ' image' : ' images') + ' added' : 'JPG, PNG or WebP. Add as many as you need.';
  $('make').disabled = !items.length; $('dl').hidden = true; $('out').textContent = items.length ? items.length + (items.length === 1 ? ' page' : ' pages') : '—'; $('lines').innerHTML = '';
}
$('list').addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b) return; const i = +b.dataset.i;
  if (b.dataset.a === 'rm') { URL.revokeObjectURL(items[i].url); items.splice(i, 1); }
  if (b.dataset.a === 'up' && i > 0) [items[i - 1], items[i]] = [items[i], items[i - 1]];
  if (b.dataset.a === 'dn' && i < items.length - 1) [items[i + 1], items[i]] = [items[i], items[i + 1]];
  render();
});
$('files').addEventListener('change', e => { [...e.target.files].forEach(f => items.push({ file: f, name: f.name, url: URL.createObjectURL(f) })); e.target.value = ''; render(); });
['psize', 'orient', 'margin', 'qual'].forEach(id => $(id).addEventListener('change', () => { $('dl').hidden = true; }));
function loadImg(src) { return new Promise((ok, no) => { const im = new Image(); im.onload = () => ok(im); im.onerror = no; im.src = src; }); }
async function toJpeg(it) {
  const im = await loadImg(it.url), [max, q] = Q[$('qual').value], k = Math.min(1, max / Math.max(im.width, im.height));
  const c = document.createElement('canvas'); c.width = Math.round(im.width * k); c.height = Math.round(im.height * k);
  const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height); x.drawImage(im, 0, 0, c.width, c.height);
  const b = await new Promise(r => c.toBlob(r, 'image/jpeg', q));
  return { w: c.width, h: c.height, bytes: new Uint8Array(await b.arrayBuffer()) };
}
function pdf(imgs) {
  const te = new TextEncoder(), parts = [], offs = []; let len = 0;
  const push = x => { const b = typeof x === 'string' ? te.encode(x) : x; parts.push(b); len += b.length; };
  const obj = (n, f) => { offs[n] = len; push(n + ' 0 obj\n'); f(); push('\nendobj\n'); };
  push('%PDF-1.4\n'); push(new Uint8Array([37, 226, 227, 207, 211, 10]));
  const n = imgs.length, size = $('psize').value, m = +$('margin').value, o = $('orient').value;
  obj(1, () => push('<< /Type /Catalog /Pages 2 0 R >>'));
  obj(2, () => push('<< /Type /Pages /Kids [' + imgs.map((_, i) => (3 + 3 * i) + ' 0 R').join(' ') + '] /Count ' + n + ' >>'));
  imgs.forEach((im, i) => {
    let pw, ph, mg = m;
    if (size === 'fit') { pw = im.w * 0.75; ph = im.h * 0.75; mg = 0; }
    else { [pw, ph] = SIZES[size]; const land = o === 'l' || (o === 'auto' && im.w > im.h); if (land) [pw, ph] = [ph, pw]; }
    const s = Math.min((pw - 2 * mg) / im.w, (ph - 2 * mg) / im.h), dw = im.w * s, dh = im.h * s, x = (pw - dw) / 2, y = (ph - dh) / 2, p = 3 + 3 * i;
    obj(p, () => push(`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pw.toFixed(2)} ${ph.toFixed(2)}] /Resources << /XObject << /Im${i} ${p + 2} 0 R >> >> /Contents ${p + 1} 0 R >>`));
    const cs = `q ${dw.toFixed(2)} 0 0 ${dh.toFixed(2)} ${x.toFixed(2)} ${y.toFixed(2)} cm /Im${i} Do Q`;
    obj(p + 1, () => push(`<< /Length ${cs.length} >>\nstream\n${cs}\nendstream`));
    obj(p + 2, () => { push(`<< /Type /XObject /Subtype /Image /Width ${im.w} /Height ${im.h} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${im.bytes.length} >>\nstream\n`); push(im.bytes); push('\nendstream'); });
  });
  const total = 3 + 3 * n, xref = len;
  let t = 'xref\n0 ' + total + '\n0000000000 65535 f \n';
  for (let k = 1; k < total; k++) t += String(offs[k]).padStart(10, '0') + ' 00000 n \n';
  push(t); push('trailer\n<< /Size ' + total + ' /Root 1 0 R >>\nstartxref\n' + xref + '\n%%EOF\n');
  return new Blob(parts, { type: 'application/pdf' });
}
$('make').addEventListener('click', async () => {
  if (!items.length) return;
  $('make').disabled = true; $('make').textContent = 'Working…';
  try {
    const imgs = []; for (const it of items) imgs.push(await toJpeg(it));
    const b = pdf(imgs); if (url) URL.revokeObjectURL(url); url = URL.createObjectURL(b);
    $('out').textContent = F(b.size / 1024 / (b.size > 1048576 ? 1024 : 1), 1) + (b.size > 1048576 ? ' MB' : ' KB');
    $('lines').innerHTML = [['Pages', imgs.length], ['Page size', $('psize').selectedOptions[0].text]].map(([a, v]) => """ + ROW + r""").join('');
    $('dl').href = url; $('dl').hidden = false;
  } catch (e) { $('out').textContent = 'Could not read one of the images'; }
  $('make').disabled = false; $('make').textContent = 'Create PDF';
});
render();
""",
body="""
<h2>How it works</h2>
<p>Each image is redrawn as a JPEG inside your browser and placed on its own PDF page, centred and scaled to fit. No upload, no account and no watermark.</p>
<ol><li>Tap <em>Add images</em> and pick one or more photos. You can add more in several goes.</li><li>Use the arrows to put the pages in order, or ✕ to remove one.</li><li>Choose A4 for printing or forms, or <em>Same as image</em> to keep each picture's shape.</li><li>Tap <em>Create PDF</em>, then <em>Download PDF</em>.</li></ol>
<h3>Keeping the file small</h3>
<div class="scroll"><table><thead><tr><th>Quality</th><th>Longest side</th><th>Typical size per page</th></tr></thead><tbody>
<tr><td>High</td><td>2,400 px</td><td>400–900 KB</td></tr><tr><td>Medium</td><td>1,700 px</td><td>200–450 KB</td></tr><tr><td>Small file</td><td>1,200 px</td><td>80–200 KB</td></tr></tbody></table></div>
<p>Typical ranges for phone photos; plain scanned pages are smaller. If an upload portal has a size limit, choose <em>Small file</em> and fewer pages.</p>
<h3>Good for</h3><ul><li>Scanned certificates and ID copies for applications.</li><li>Receipts and invoices for expense claims.</li><li>Notes, worksheets and assignments photographed on a phone.</li></ul>
""",
faqs=[("How do I convert JPG to PDF on my phone?", "Open this page, tap Add images, select your photos, arrange them and tap Create PDF. The PDF downloads to your phone."),
      ("Are my images uploaded to a server?", "No. The PDF is built entirely in your browser."),
      ("Can I combine several images into one PDF?", "Yes. Each image becomes one page, in the order shown in the list."),
      ("How do I make the PDF smaller?", "Choose Quality: Small file. It reduces each image to 1,200 pixels on the longest side.")]))

# ---------------- Age calculator ----------------
TOOLS.append(dict(
group="everyday", slug="age-calculator", icon="guide",
name="Age Calculator",
title="Age Calculator: Exact Age in Years, Months and Days (As On Any Date)",
desc="Find your exact age in years, months and days, your age on any date (for exam and job eligibility), total days lived and the days to your next birthday.",
keywords="age calculator, age calculator as on date, exact age calculator, how old am i, date of birth calculator, age in days, age eligibility calculator, next birthday countdown",
h1="Age calculator",
lede="Exact age in years, months and days, on today's date or on any cut-off date an application asks for.",
card="Exact age on any date, next birthday",
tool="""
<div class="inputs">
 <div><label for="dob">Date of birth</label><input id="dob" type="date" value="1995-06-15"></div>
 <div><label for="on">Age as on</label><input id="on" type="date"><div class="hint">Defaults to today. Set the cut-off date from a job or exam notification to check eligibility.</div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Age</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
</div>""",
js=r"""
const pd = s => { const [y, m, d] = s.split('-').map(Number); return new Date(Date.UTC(y, m - 1, d)); };
const dim = (y, m) => new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
function calc() {
  if (!$('dob').value || !$('on').value) return;
  const a = pd($('dob').value), b = pd($('on').value);
  if (b < a) { $('out').textContent = 'Check the dates'; $('lines').innerHTML = ''; return; }
  let y = b.getUTCFullYear() - a.getUTCFullYear(), m = b.getUTCMonth() - a.getUTCMonth(), d = b.getUTCDate() - a.getUTCDate();
  if (d < 0) { m--; d += dim(b.getUTCFullYear(), b.getUTCMonth() - 1 < 0 ? 11 : b.getUTCMonth() - 1); }
  if (m < 0) { y--; m += 12; }
  const days = Math.round((b - a) / 864e5);
  let nb = new Date(Date.UTC(b.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate())); if (nb < b) nb = new Date(Date.UTC(b.getUTCFullYear() + 1, a.getUTCMonth(), a.getUTCDate()));
  const to = Math.round((nb - b) / 864e5), wd = a.toLocaleDateString('en-GB', { weekday: 'long', timeZone: 'UTC' });
  $('out').textContent = `${y} years ${m} months ${d} days`;
  $('lines').innerHTML = [['Total months', F(y * 12 + m, 0)], ['Total weeks', F(Math.floor(days / 7), 0) + ' weeks ' + (days % 7) + ' days'], ['Total days', F(days, 0)],
    ['Next birthday', to === 0 ? 'Today' : 'in ' + F(to, 0) + ' days (turns ' + (y + 1) + ')'], ['Born on a', wd]].map(([a, v]) => """ + ROW + r""").join('');
}
$('on').value = new Date().toISOString().slice(0, 10);
['dob', 'on'].forEach(id => $(id).addEventListener('input', calc)); calc();
""",
body="""
<h2>How exact age is worked out</h2>
<p>Age is counted in whole years first, then whole months, then the remaining days. If the day of the month has not yet been reached, one month is borrowed and the number of days in the previous month is added.</p>
<h3>Example</h3>
<p>Born 15 June 1995, age as on 1 January 2026: from 15 June 1995 to 15 December 2025 is 30 years 6 months, and from 15 December to 1 January is 17 days, so the age is <strong>30 years 6 months 17 days</strong>.</p>
<h3>Checking eligibility for a job or exam</h3>
<p>Notifications usually state an age limit <em>as on</em> a fixed date, such as 1 January of the year. Enter that date in <em>Age as on</em>. A candidate born on the cut-off date itself is usually counted as completing that age on that day, but the notification's own wording decides edge cases and any relaxations for reserved categories.</p>
""",
faqs=[("How do I calculate my exact age?", "Enter your date of birth. The calculator counts full years, then full months, then remaining days up to today or any date you choose."),
      ("How do I check age as on a specific date?", "Change the 'Age as on' field to the cut-off date in your notification."),
      ("How many days old am I?", "The 'Total days' line shows the number of days from your birth date to the chosen date.")]))

# ---------------- Percentage calculator ----------------
TOOLS.append(dict(
group="everyday", slug="percentage-calculator", icon="money",
name="Percentage Calculator",
title="Percentage Calculator: % of a Number, Percentage Change, Increase & Decrease",
desc="Work out X% of a number, what percentage one number is of another, percentage increase or decrease, and add or subtract a percentage. Shows the formula for each.",
keywords="percentage calculator, percent of a number, percentage change calculator, percentage increase calculator, percentage decrease, what percent is x of y, marks percentage calculator, discount percentage",
h1="Percentage calculator",
lede="Four everyday percentage sums in one place, each with its formula.",
card="% of, % change, increase and decrease",
tool="""
<div class="inputs pct">
 <div class="pct-row"><b>What is</b><input id="a1" inputmode="decimal" value="18" aria-label="Percent"><b>% of</b><input id="b1" inputmode="decimal" value="2500" aria-label="Number"><output id="r1"></output></div>
 <div class="pct-row"><input id="a2" inputmode="decimal" value="432" aria-label="Part"><b>is what % of</b><input id="b2" inputmode="decimal" value="500" aria-label="Whole"><output id="r2"></output></div>
 <div class="pct-row"><b>From</b><input id="a3" inputmode="decimal" value="80" aria-label="Old value"><b>to</b><input id="b3" inputmode="decimal" value="92" aria-label="New value"><output id="r3"></output></div>
 <div class="pct-row"><input id="a4" inputmode="decimal" value="1200" aria-label="Number"><select id="op4" aria-label="Increase or decrease"><option value="1">plus</option><option value="-1">minus</option></select><input id="b4" inputmode="decimal" value="15" aria-label="Percent"><b>%</b><output id="r4"></output></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Formulas</div>
 <ul class="lines" id="lines"></ul>
 <p class="formula">Marks: (marks obtained ÷ total marks) × 100. Discount: price × (1 − discount ÷ 100).</p>
</div>""",
js=r"""
function calc() {
  const r1 = V('a1') / 100 * V('b1'), r2 = V('b2') ? V('a2') / V('b2') * 100 : 0, r3 = V('a3') ? (V('b3') - V('a3')) / Math.abs(V('a3')) * 100 : 0, r4 = V('a4') * (1 + (+$('op4').value) * V('b4') / 100);
  $('r1').textContent = '= ' + F(r1, 2); $('r2').textContent = '= ' + F(r2, 2) + '%';
  $('r3').textContent = (r3 >= 0 ? '↑ ' : '↓ ') + F(Math.abs(r3), 2) + '%'; $('r4').textContent = '= ' + F(r4, 2);
  $('lines').innerHTML = [['X% of Y', 'X ÷ 100 × Y'], ['X as % of Y', 'X ÷ Y × 100'], ['% change', '(new − old) ÷ old × 100'], ['Add / subtract X%', 'Y × (1 ± X ÷ 100)']].map(([a, v]) => """ + ROW + r""").join('');
}
document.querySelectorAll('.pct input, .pct select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>The four percentage sums</h2>
<div class="scroll"><table><thead><tr><th>Question</th><th>Formula</th><th>Example</th></tr></thead><tbody>
<tr><td>What is 18% of 2,500?</td><td>18 ÷ 100 × 2,500</td><td>450</td></tr>
<tr><td>432 is what % of 500?</td><td>432 ÷ 500 × 100</td><td>86.4%</td></tr>
<tr><td>% change from 80 to 92</td><td>(92 − 80) ÷ 80 × 100</td><td>15% increase</td></tr>
<tr><td>1,200 plus 15%</td><td>1,200 × 1.15</td><td>1,380</td></tr></tbody></table></div>
<h3>Common mistakes</h3>
<ul><li>A 20% rise followed by a 20% fall does not return to the start: 100 → 120 → 96.</li><li>To remove a percentage that was added (for example tax included in a price), divide, do not subtract: 1,180 ÷ 1.18 = 1,000.</li><li>Percentage points are not percentages: a rate moving from 4% to 5% is a 1 percentage point rise but a 25% increase.</li></ul>
""",
faqs=[("How do I calculate a percentage of a number?", "Divide the percentage by 100 and multiply by the number. 18% of 2,500 = 0.18 × 2,500 = 450."),
      ("How do I calculate marks percentage?", "Divide marks obtained by total marks and multiply by 100. 432 out of 500 = 86.4%."),
      ("How do I work out percentage increase?", "Subtract the old value from the new value, divide by the old value and multiply by 100.")]))

# ---------------- SIP calculator ----------------
TOOLS.append(dict(
group="uae", slug="sip-calculator", icon="trading",
name="SIP Calculator (with Step-Up)",
title="SIP Calculator with Annual Step-Up: Mutual Fund Returns Estimate",
desc="Estimate what a monthly SIP could grow to, with an optional yearly step-up. Shows amount invested, estimated gains and a year-by-year table. Works in any currency.",
keywords="sip calculator, step up sip calculator, mutual fund sip calculator, sip return calculator, monthly investment calculator, sip calculator india, systematic investment plan calculator",
h1="SIP calculator with step-up",
lede="See how a fixed monthly investment, raised a little each year, could grow at an assumed rate of return.",
card="Monthly investing with yearly step-up",
tool="""
<div class="inputs">
 <div><label for="amt">Monthly investment</label><input id="amt" inputmode="decimal" value="10000"></div>
 <div class="row2"><div><label for="ret">Expected return (% a year)</label><input id="ret" inputmode="decimal" value="12"></div>
 <div><label for="yrs">Years</label><input id="yrs" inputmode="decimal" value="15"></div></div>
 <div><label for="step">Increase SIP each year by (%)</label><input id="step" inputmode="decimal" value="10"><div class="hint">0 for a flat SIP.</div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Estimated value</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <div class="scroll" style="margin-top:14px;max-height:260px;overflow:auto"><table id="tbl"></table></div>
 <p class="formula">Monthly compounding, instalment at the start of each month. Returns are not guaranteed.</p>
</div>""",
js=r"""
function calc() {
  const r = V('ret') / 1200, n = Math.min(Math.round(V('yrs')), 50), st = V('step') / 100;
  let bal = 0, inv = 0, sip = V('amt'), rows = [];
  for (let y = 1; y <= n; y++) {
    for (let m = 0; m < 12; m++) { bal = (bal + sip) * (1 + r); inv += sip; }
    rows.push([y, sip, inv, bal]); sip *= 1 + st;
  }
  $('out').textContent = F(bal, 0);
  $('lines').innerHTML = [['Total invested', F(inv, 0)], ['Estimated gains', F(bal - inv, 0)], ['Final monthly SIP', F(rows.length ? rows[rows.length - 1][1] : 0, 0)], ['Value ÷ invested', F(inv ? bal / inv : 0, 2) + '×']].map(([a, v]) => """ + ROW + r""").join('');
  $('tbl').innerHTML = '<thead><tr><th>Year</th><th class="n">Monthly SIP</th><th class="n">Invested</th><th class="n">Value</th></tr></thead><tbody>' + rows.map(x => `<tr><td>${x[0]}</td><td class="n">${F(x[1], 0)}</td><td class="n">${F(x[2], 0)}</td><td class="n">${F(x[3], 0)}</td></tr>`).join('') + '</tbody>';
}
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>How a SIP grows</h2>
<p>A systematic investment plan (SIP) puts the same amount into a fund every month. Each instalment then grows for the months that remain. With a <strong>step-up</strong>, the monthly amount rises by a fixed percentage once a year, usually in line with salary increases.</p>
<h3>Example</h3>
<p>10,000 a month for 15 years at an assumed 12% a year: flat, about 18 lakh invested grows to roughly 50 lakh. With a 10% yearly step-up, about 38 lakh invested grows to roughly 87 lakh. Use the calculator for exact figures.</p>
<h3>Points to keep in mind</h3>
<ul><li>Equity fund returns vary year to year and can be negative; the rate you enter is an assumption, not a promise.</li><li>Fund expenses and taxes on gains reduce what you keep.</li><li>Starting earlier usually matters more than the amount.</li></ul>
<p>For information only, not investment advice.</p>
""",
faqs=[("How is SIP return calculated?", "Each monthly instalment is compounded monthly at the assumed annual rate ÷ 12 until the end of the period; the values are added together."),
      ("What is a step-up SIP?", "A SIP whose monthly amount increases by a set percentage each year, for example 10%."),
      ("Is the result guaranteed?", "No. It is an estimate based on the return you enter. Actual fund returns vary.")]))

# ---------------- Compound interest / FD ----------------
TOOLS.append(dict(
group="uae", slug="compound-interest-calculator", icon="money",
name="Compound Interest & FD Calculator",
title="Compound Interest Calculator & FD Maturity Calculator (Monthly, Quarterly)",
desc="Calculate compound interest and fixed deposit maturity with yearly, half-yearly, quarterly, monthly or daily compounding, plus optional monthly additions.",
keywords="compound interest calculator, fd calculator, fixed deposit calculator, fd maturity calculator, quarterly compounding calculator, savings growth calculator, interest calculator",
h1="Compound interest and FD calculator",
lede="See what a deposit grows to with compound interest, and how much of it is interest.",
card="FD maturity and compound growth",
tool="""
<div class="inputs">
 <div><label for="p">Starting amount</label><input id="p" inputmode="decimal" value="100000"></div>
 <div class="row2"><div><label for="rate">Interest rate (% a year)</label><input id="rate" inputmode="decimal" value="7"></div>
 <div><label for="yrs">Years</label><input id="yrs" inputmode="decimal" value="5"></div></div>
 <div class="row2"><div><label for="cmp">Compounding</label><select id="cmp"><option value="1">Yearly</option><option value="2">Half-yearly</option><option value="4" selected>Quarterly</option><option value="12">Monthly</option><option value="365">Daily</option></select></div>
 <div><label for="add">Add each month</label><input id="add" inputmode="decimal" value="0"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Maturity value</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p class="formula">A = P × (1 + r/n)<sup>n×t</sup>. Monthly additions are added at the end of each month. Before tax.</p>
</div>""",
js=r"""
function calc() {
  const P = V('p'), r = V('rate') / 100, n = +$('cmp').value, t = V('yrs'), add = V('add');
  const months = Math.round(t * 12), mr = Math.pow(1 + r / n, n / 12) - 1;
  let bal = P; for (let i = 0; i < months; i++) bal = bal * (1 + mr) + add;
  const inv = P + add * months, eff = (Math.pow(1 + r / n, n) - 1) * 100;
  $('out').textContent = F(bal, 2);
  $('lines').innerHTML = [['Total deposited', F(inv, 2)], ['Interest earned', F(bal - inv, 2)], ['Effective annual rate', F(eff, 2) + '%'], ['Simple interest would give', F(P * (1 + r * t) + add * months, 2)]].map(([a, v]) => """ + ROW + r""").join('');
}
document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>Compound interest formula</h2>
<p><strong>A = P × (1 + r ÷ n)<sup>n × t</sup></strong>, where P is the deposit, r the annual rate, n the number of times interest is added each year and t the number of years. The more often interest is compounded, the higher the <strong>effective annual rate</strong>.</p>
<h3>Example: a 5-year fixed deposit</h3>
<p>1,00,000 at 7% a year, compounded quarterly: 1,00,000 × (1 + 0.07 ÷ 4)<sup>20</sup> = <strong>1,41,478</strong>. Interest earned is 41,478 and the effective annual rate is 7.19%.</p>
<h3>Things that change the real return</h3>
<ul><li>Tax on interest (in India, FD interest is added to your income; TDS may be deducted).</li><li>Some banks pay interest out quarterly instead of reinvesting it; then use simple interest.</li><li>Breaking a deposit early usually reduces the rate.</li></ul>
""",
faqs=[("How is FD maturity calculated?", "With compound interest: principal × (1 + rate ÷ compounding periods) raised to the number of periods. Most Indian bank FDs compound quarterly."),
      ("What is the effective annual rate?", "The yearly return after compounding. 7% compounded quarterly equals 7.19% a year."),
      ("Does this include tax?", "No. Results are before tax.")]))

# ---------------- GST calculator (India) ----------------
TOOLS.append(dict(
group="uae", slug="gst-calculator", icon="money",
name="GST Calculator (India, 2026 Rates)",
title="GST Calculator India 2026: Add or Remove GST (5%, 18%, 40%), CGST & SGST",
desc="Add GST to a price or remove it from a GST-inclusive amount at the current slabs of 5%, 18% and 40%, with the CGST/SGST or IGST split.",
keywords="gst calculator, gst calculator india, reverse gst calculator, gst inclusive calculator, cgst sgst calculator, gst 18 percent calculator, gst 5 percent, new gst rates 2026",
h1="GST calculator (India)",
lede="Add GST to a price, or work back from a GST-inclusive total, using the rate slabs in force since 22 September 2025.",
card="Add or remove GST, CGST/SGST split",
tool="""
<div class="inputs">
 <div><label for="amt">Amount (₹)</label><input id="amt" inputmode="decimal" value="10000"></div>
 <div><label>This amount is</label><div class="seg" id="mode"><button type="button" data-v="ex" aria-pressed="true">Before GST</button><button type="button" data-v="in" aria-pressed="false">Including GST</button></div></div>
 <div class="row2"><div><label for="rate">GST rate</label><select id="rate"><option value="5">5%</option><option value="18" selected>18%</option><option value="40">40%</option><option value="3">3% (gold, silver)</option><option value="0">0% (nil)</option><option value="c">Other</option></select></div>
 <div><label for="crate">Other rate (%)</label><input id="crate" inputmode="decimal" value="12"></div></div>
 <div><label>Supply</label><div class="seg" id="sup"><button type="button" data-v="intra" aria-pressed="true">Within the state</button><button type="button" data-v="inter" aria-pressed="false">Between states</button></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label" id="lbl">Price including GST</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p class="formula">Add: amount × (1 + rate). Remove: amount ÷ (1 + rate). Check your item's rate before invoicing.</p>
</div>""",
js=r"""
const mode = seg('mode', () => calc()), sup = seg('sup', () => calc());
function calc() {
  const rv = $('rate').value, r = (rv === 'c' ? V('crate') : +rv) / 100, a = V('amt');
  $('crate').closest('div').style.opacity = rv === 'c' ? 1 : .45;
  const base = mode() === 'ex' ? a : a / (1 + r), gst = base * r, tot = base + gst;
  $('lbl').textContent = mode() === 'ex' ? 'Price including GST' : 'Price before GST';
  $('out').textContent = '₹' + F(mode() === 'ex' ? tot : base);
  const split = sup() === 'intra' ? [['CGST (' + F(r * 50, 2) + '%)', '₹' + F(gst / 2)], ['SGST (' + F(r * 50, 2) + '%)', '₹' + F(gst / 2)]] : [['IGST (' + F(r * 100, 2) + '%)', '₹' + F(gst)]];
  $('lines').innerHTML = [['Taxable value', '₹' + F(base)], ...split, ['Total GST', '₹' + F(gst)], ['Total', '₹' + F(tot)]].map(([a, v]) => """ + ROW + r""").join('');
}
document.querySelectorAll('.inputs input, .inputs select').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>GST rates since 22 September 2025</h2>
<p>Under the GST 2.0 changes recommended by the 56th GST Council meeting, most goods and services now fall into two main slabs, <strong>5%</strong> and <strong>18%</strong>, with a <strong>40%</strong> rate for a narrow list of luxury and "sin" goods and <strong>0%</strong> for nil-rated essentials. The old 12% and 28% slabs were largely removed. Some special rates remain, such as 3% on gold and silver.</p>
<h3>Adding and removing GST</h3>
<div class="scroll"><table><thead><tr><th>Task</th><th>Formula</th><th>Example at 18%</th></tr></thead><tbody>
<tr><td>Add GST</td><td>amount × 1.18</td><td>₹10,000 → ₹11,800</td></tr>
<tr><td>Remove GST</td><td>amount ÷ 1.18</td><td>₹11,800 → ₹10,000</td></tr>
<tr><td>GST inside an inclusive price</td><td>amount × 18 ÷ 118</td><td>₹11,800 → ₹1,800</td></tr></tbody></table></div>
<h3>CGST, SGST and IGST</h3>
<p>For a sale within one state, GST is split equally between central (CGST) and state (SGST) tax. For a sale between states, the whole amount is IGST.</p>
<p>Rates depend on the HSN/SAC classification of the item; check the current rate notification for your product or service.</p>
""",
faqs=[("What are the GST rates in India in 2026?", "The main slabs are 5% and 18%, with 40% for selected luxury and sin goods and 0% for nil-rated items, effective from 22 September 2025."),
      ("How do I remove GST from a price?", "Divide the GST-inclusive price by 1 plus the rate. At 18%, ₹11,800 ÷ 1.18 = ₹10,000."),
      ("How is GST split into CGST and SGST?", "For sales within a state, half of the GST is CGST and half is SGST. Sales between states carry IGST at the full rate.")],
sources=[("CBIC GST portal", "https://cbic-gst.gov.in"), ("Press Information Bureau: 56th GST Council recommendations", "https://pib.gov.in")]))

# ---------------- Days between dates ----------------
TOOLS.append(dict(
group="everyday", slug="date-calculator", icon="guide",
name="Days Between Dates & Date Calculator",
title="Days Between Dates Calculator: Count Days, Weeks, Working Days, Add Days",
desc="Count the days, weeks, months and working days between two dates, or add and subtract days from a date. For notice periods, deadlines, visas and travel.",
keywords="days between dates, date calculator, day counter, working days calculator, add days to date, how many days until, date difference calculator, business days between dates",
h1="Days between dates",
lede="Count calendar days and working days between two dates, or find the date a number of days from now.",
card="Days, working days, add or subtract days",
tool="""
<div class="inputs">
 <div class="row2"><div><label for="d1">Start date</label><input id="d1" type="date"></div><div><label for="d2">End date</label><input id="d2" type="date"></div></div>
 <label class="chk"><input type="checkbox" id="incl"> Include the end date</label>
 <hr style="border:0;border-top:1px solid var(--line);margin:4px 0">
 <div class="row2"><div><label for="d3">From date</label><input id="d3" type="date"></div><div><label for="n">Add days (use − to subtract)</label><input id="n" inputmode="numeric" value="90"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Between the dates</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <div class="big-label" style="margin-top:18px">Date after adding days</div><div class="big" id="out2" style="font-size:28px">—</div>
</div>""",
js=r"""
const pd = s => { const [y, m, d] = s.split('-').map(Number); return new Date(Date.UTC(y, m - 1, d)); };
const fmt = d => d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' });
function calc() {
  if ($('d1').value && $('d2').value) {
    let a = pd($('d1').value), b = pd($('d2').value), sign = 1; if (b < a) { [a, b] = [b, a]; sign = -1; }
    let days = Math.round((b - a) / 864e5) + ($('incl').checked ? 1 : 0), work = 0;
    for (let i = 0, t = new Date(a); i < days; i++, t.setUTCDate(t.getUTCDate() + 1)) { const w = t.getUTCDay(); if (w && w < 6) work++; }
    let m = (b.getUTCFullYear() - a.getUTCFullYear()) * 12 + b.getUTCMonth() - a.getUTCMonth(); if (b.getUTCDate() < a.getUTCDate()) m--;
    $('out').textContent = (sign < 0 ? '−' : '') + F(days, 0) + ' days';
    $('lines').innerHTML = [['Weeks', Math.floor(days / 7) + ' weeks ' + (days % 7) + ' days'], ['Whole months', F(Math.max(m, 0), 0)], ['Working days (Mon–Fri)', F(work, 0)], ['Weekend days', F(days - work, 0)]].map(([a, v]) => """ + ROW + r""").join('');
  }
  if ($('d3').value) { const d = pd($('d3').value); d.setUTCDate(d.getUTCDate() + Math.round(V('n'))); $('out2').textContent = fmt(d); }
}
const t = new Date(), iso = x => x.toISOString().slice(0, 10), later = new Date(t); later.setDate(t.getDate() + 30);
$('d1').value = iso(t); $('d2').value = iso(later); $('d3').value = iso(t);
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>Counting days correctly</h2>
<p>By default the start date is counted and the end date is not, so 1 March to 2 March is 1 day. Tick <em>Include the end date</em> when both days count, for example a hotel stay counted in days, a leave application, or a visa that is valid through its last day.</p>
<h3>Working days</h3>
<p>Working days here are Monday to Friday. Public holidays differ by country and employer, so subtract them yourself. In countries with a Friday–Saturday or Saturday–Sunday weekend, check which days your employer counts.</p>
<h3>Examples</h3>
<ul><li><strong>Notice period:</strong> 30 days from 20 November 2026 is 20 December 2026.</li><li><strong>90-day visa:</strong> entering on 1 January, day 90 is 31 March in a non-leap year (count with the end date included).</li></ul>
""",
faqs=[("How many days are between two dates?", "Enter both dates. The result counts the start date but not the end date unless you tick Include the end date."),
      ("How do I add 90 days to a date?", "Use the second section: choose the date and enter 90. Use a minus sign to go back in time."),
      ("Does it count public holidays?", "No. Working days are Monday to Friday; subtract public holidays separately.")]))

# ---------------- Word counter ----------------
TOOLS.append(dict(
group="everyday", slug="word-counter", icon="guide",
name="Word & Character Counter",
title="Word Counter & Character Counter: Words, Characters, Reading Time",
desc="Count words, characters (with and without spaces), sentences and paragraphs, and see reading and speaking time and the most used words. Text stays on your device.",
keywords="word counter, character counter, word count tool, count characters online, letter counter, essay word count, sop word count, reading time calculator",
h1="Word and character counter",
lede="Paste or type your text to count words and characters for essays, statements of purpose, applications and posts.",
card="Words, characters, reading time",
tool="""
<div class="inputs">
 <label for="txt">Your text</label>
 <textarea id="txt" rows="12" style="width:100%;font:16px/1.55 var(--body);padding:12px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink);resize:vertical" placeholder="Type or paste text here"></textarea>
 <p style="margin:0"><button type="button" class="btn" id="clr">Clear</button></p>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Words</div><div class="big" id="out">0</div>
 <ul class="lines" id="lines"></ul>
 <div class="big-label" style="margin-top:16px">Most used words</div><p id="top" class="hint">—</p>
</div>""",
js=r"""
const STOP = new Set('the a an and or but of to in on at for with is are was were be been it this that as by from i you he she we they my your our their not no so if then than there here have has had do does did will would can could should'.split(' '));
function calc() {
  const t = $('txt').value, w = t.match(/[\p{L}\p{N}'’-]+/gu) || [], words = w.length;
  const sent = (t.match(/[^.!?]+[.!?]+/g) || []).length || (t.trim() ? 1 : 0), paras = t.split(/\n\s*\n/).filter(p => p.trim()).length;
  $('out').textContent = F(words, 0);
  const mins = x => { const s = Math.round(words / x * 60); return s < 60 ? s + ' sec' : Math.floor(s / 60) + ' min ' + (s % 60) + ' sec'; };
  $('lines').innerHTML = [['Characters', F(t.length, 0)], ['Characters (no spaces)', F(t.replace(/\s/g, '').length, 0)], ['Sentences', F(sent, 0)], ['Paragraphs', F(paras, 0)], ['Reading time', mins(230)], ['Speaking time', mins(130)]].map(([a, v]) => """ + ROW + r""").join('');
  const c = {}; w.forEach(x => { x = x.toLowerCase(); if (x.length > 2 && !STOP.has(x)) c[x] = (c[x] || 0) + 1; });
  const top = Object.entries(c).sort((a, b) => b[1] - a[1]).slice(0, 8);
  $('top').textContent = top.length ? top.map(([k, v]) => k + ' (' + v + ')').join(', ') : '—';
}
try { $('txt').value = sessionStorage.getItem('wc') || ''; } catch (e) {}
$('txt').addEventListener('input', () => { calc(); try { sessionStorage.setItem('wc', $('txt').value); } catch (e) {} });
$('clr').addEventListener('click', () => { $('txt').value = ''; try { sessionStorage.removeItem('wc'); } catch (e) {} calc(); });
calc();
""",
body="""
<h2>What is counted</h2>
<ul><li><strong>Words:</strong> runs of letters or numbers, including words with apostrophes and hyphens (for example <em>don't</em> and <em>well-known</em> count as one word each).</li><li><strong>Characters:</strong> every letter, space and symbol. Many forms and social platforms limit characters, not words.</li><li><strong>Reading time:</strong> about 230 words a minute; <strong>speaking time:</strong> about 130 words a minute.</li></ul>
<h3>Typical limits</h3>
<div class="scroll"><table><thead><tr><th>Text</th><th>Usual length</th></tr></thead><tbody>
<tr><td>Statement of purpose</td><td>800–1,000 words (check the university's limit)</td></tr><tr><td>Cover letter</td><td>250–400 words</td></tr><tr><td>Meta description for a web page</td><td>about 150–160 characters</td></tr></tbody></table></div>
<p>Your text is counted in your browser and is not sent anywhere.</p>
""",
faqs=[("How are words counted?", "Each run of letters or numbers counts as one word; hyphenated words and contractions count as one."),
      ("Does it count spaces as characters?", "The Characters line includes spaces; the next line shows the count without spaces."),
      ("Is my text saved?", "Only in this browser tab, so it survives a refresh. Closing the tab or tapping Clear removes it.")]))

# ---------------- BMI ----------------
TOOLS.append(dict(
group="everyday", slug="bmi-calculator", icon="guide",
name="BMI Calculator",
title="BMI Calculator: Body Mass Index in kg/cm or lb/ft, With Healthy Weight Range",
desc="Calculate body mass index (BMI) for adults in metric or imperial units, see the WHO category and the weight range that gives a BMI of 18.5 to 24.9 for your height.",
keywords="bmi calculator, body mass index calculator, bmi calculator kg cm, bmi calculator feet inches, healthy weight for height, bmi chart, ideal weight calculator",
h1="BMI calculator",
lede="Body mass index for adults, with the WHO category and the healthy-weight range for your height.",
card="BMI, category and healthy weight range",
tool="""
<div class="inputs">
 <div><label>Units</label><div class="seg" id="u"><button type="button" data-v="m" aria-pressed="true">kg / cm</button><button type="button" data-v="i" aria-pressed="false">lb / ft-in</button></div></div>
 <div class="row2" id="mm"><div><label for="cm">Height (cm)</label><input id="cm" inputmode="decimal" value="170"></div><div><label for="kg">Weight (kg)</label><input id="kg" inputmode="decimal" value="68"></div></div>
 <div id="ii" hidden><div class="row2"><div><label for="ft">Height (ft)</label><input id="ft" inputmode="decimal" value="5"></div><div><label for="inch">Height (in)</label><input id="inch" inputmode="decimal" value="7"></div></div>
 <div style="margin-top:12px"><label for="lb">Weight (lb)</label><input id="lb" inputmode="decimal" value="150"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Your BMI</div><div class="big" id="out">—</div>
 <div class="bmi-bar"><i id="mk"></i></div>
 <ul class="lines" id="lines"></ul>
 <p class="formula">BMI = weight (kg) ÷ height (m)². For adults aged 18 and over. Not a diagnosis.</p>
</div>""",
js=r"""
const u = seg('u', () => { $('mm').hidden = u() !== 'm'; $('ii').hidden = u() !== 'i'; calc(); });
function calc() {
  const hm = u() === 'm' ? V('cm') / 100 : (V('ft') * 12 + V('inch')) * 0.0254, kg = u() === 'm' ? V('kg') : V('lb') * 0.45359237;
  if (!hm || !kg) return;
  const b = kg / (hm * hm), cat = b < 18.5 ? 'Underweight' : b < 25 ? 'Healthy weight' : b < 30 ? 'Overweight' : 'Obesity';
  const lo = 18.5 * hm * hm, hi = 24.9 * hm * hm, w = x => u() === 'm' ? F(x, 1) + ' kg' : F(x / 0.45359237, 0) + ' lb';
  $('out').textContent = F(b, 1) + ' · ' + cat;
  $('mk').style.left = Math.max(0, Math.min(100, (b - 15) / 25 * 100)) + '%';
  $('lines').innerHTML = [['Healthy range for your height', w(lo) + ' – ' + w(hi)], [kg < lo ? 'To reach the range' : kg > hi ? 'Above the range by' : 'Within the range', kg < lo ? '+' + w(lo - kg) : kg > hi ? w(kg - hi) : '✓']].map(([a, v]) => """ + ROW + r""").join('');
}
$('mm').hidden = u() !== 'm'; $('ii').hidden = u() !== 'i';
document.querySelectorAll('.inputs input').forEach(i => i.addEventListener('input', calc)); calc();
""",
body="""
<h2>BMI categories for adults (WHO)</h2>
<div class="scroll"><table><thead><tr><th>BMI</th><th>Category</th></tr></thead><tbody>
<tr><td>Below 18.5</td><td>Underweight</td></tr><tr><td>18.5 – 24.9</td><td>Healthy weight</td></tr><tr><td>25.0 – 29.9</td><td>Overweight</td></tr><tr><td>30 and above</td><td>Obesity</td></tr></tbody></table></div>
<h3>Example</h3>
<p>Height 170 cm and weight 68 kg: 68 ÷ (1.70 × 1.70) = <strong>23.5</strong>, in the healthy range. For 170 cm, that range is about 53.5 kg to 72.0 kg.</p>
<h3>Limits of BMI</h3>
<ul><li>BMI does not separate muscle from fat, so very muscular people can show a high BMI.</li><li>For people of South Asian and some other ethnic backgrounds, health risks can start at lower BMI values; some health services use lower cut-offs.</li><li>It is not designed for children, teenagers or pregnancy. Speak to a doctor about your own health.</li></ul>
""",
faqs=[("How is BMI calculated?", "Weight in kilograms divided by height in metres squared. 68 kg at 1.70 m gives 23.5."),
      ("What is a healthy BMI?", "For adults, the WHO classes 18.5 to 24.9 as a healthy weight range."),
      ("Is BMI accurate for everyone?", "No. It is a screening number that does not measure body fat directly; muscle, age and ethnicity affect what it means.")],
sources=[("World Health Organization: obesity and overweight", "https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight")]))
