import os
from tools_more import TOOLS

ROW = "`<li><span>${a}</span><b>${v}</b></li>`"
# QR encoder (byte, numeric and alphanumeric modes, versions 1-40, levels L/M/Q/H), written for CalcSouq.
QR_JS = open(os.path.join(os.path.dirname(__file__), "qr_encoder.js")).read()

# ---------------- QR code generator ----------------
TOOLS.append(dict(
group="docs", slug="qr-code-generator", icon="qr",
name="QR Code Generator",
title="QR Code Generator Free: Wi-Fi, WhatsApp, Link, UPI (PNG and SVG)",
desc="Make a QR code for a link, text, Wi-Fi network, WhatsApp chat, email, phone number or UPI payment. Pick colours and size, download PNG or SVG. No sign-up, made in your browser.",
keywords="qr code generator free, wifi qr code generator, whatsapp qr code, qr code for link, upi qr code generator, qr code svg download, qr code generator no sign up, create qr code",
h1="QR code generator (free)",
lede="Create a QR code for a link, Wi-Fi network, WhatsApp chat, email, phone number, UPI payment or plain text. Download it as PNG or SVG. The code is made on your device and never expires.",
card="Wi-Fi, WhatsApp, link and UPI codes, PNG/SVG",
tool="""
<div class="inputs">
 <div><label for="kind">What should the code open?</label><select id="kind">
  <option value="url">Website link (URL)</option><option value="wifi">Wi-Fi network</option><option value="wa">WhatsApp chat</option><option value="text">Plain text</option><option value="email">Email</option><option value="tel">Phone number</option><option value="upi">UPI payment (India)</option></select></div>
 <div data-k="url"><label for="url">Link</label><input id="url" type="url" inputmode="url" value="https://www.calcsouq.com" autocomplete="off" spellcheck="false"></div>
 <div data-k="text" hidden><label for="txt">Text</label><textarea id="txt" rows="4" style="width:100%;font:16px/1.5 var(--body);padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink);resize:vertical">Hello from CalcSouq</textarea></div>
 <div data-k="wifi" hidden style="display:grid;gap:12px">
  <div><label for="ssid">Network name (SSID)</label><input id="ssid" value="" autocomplete="off" spellcheck="false" placeholder="e.g. Home WiFi"></div>
  <div class="row2" style="margin:0"><div><label for="wpass">Password</label><input id="wpass" type="text" autocomplete="off" spellcheck="false"></div>
  <div><label for="wsec">Security</label><select id="wsec"><option value="WPA">WPA / WPA2 / WPA3</option><option value="WEP">WEP (old)</option><option value="nopass">None (open)</option></select></div></div>
  <label class="chk"><input type="checkbox" id="whid"> Hidden network</label>
  <div class="hint">The password is not saved by this page.</div>
 </div>
 <div data-k="wa" hidden style="display:grid;gap:12px">
  <div><label for="wanum">WhatsApp number with country code</label><input id="wanum" inputmode="tel" placeholder="e.g. 971501234567 or +91 98470 12345"></div>
  <div><label for="wamsg">Message typed in for them (optional)</label><input id="wamsg" value="Hello, I saw your QR code"></div>
 </div>
 <div data-k="email" hidden style="display:grid;gap:12px">
  <div><label for="mto">Email address</label><input id="mto" type="email" inputmode="email" placeholder="name@example.com"></div>
  <div class="row2" style="margin:0"><div><label for="msub">Subject (optional)</label><input id="msub"></div><div><label for="mbody">Message (optional)</label><input id="mbody"></div></div>
 </div>
 <div data-k="tel" hidden><label for="tel">Phone number with country code</label><input id="tel" inputmode="tel" placeholder="e.g. +44 20 7946 0000"></div>
 <div data-k="upi" hidden style="display:grid;gap:12px">
  <div class="row2" style="margin:0"><div><label for="upa">UPI ID</label><input id="upa" autocomplete="off" spellcheck="false" placeholder="name@bank"></div><div><label for="upn">Payee name</label><input id="upn" placeholder="Name shown to the payer"></div></div>
  <div class="row2" style="margin:0"><div><label for="uam">Amount in ₹ (optional)</label><input id="uam" inputmode="decimal"></div><div><label for="utn">Note (optional)</label><input id="utn"></div></div>
 </div>
 <div class="row2"><div><label for="ecl">Error correction</label><select id="ecl"><option value="L">L: low (7%)</option><option value="M" selected>M: medium (15%)</option><option value="Q">Q: quartile (25%)</option><option value="H">H: high (30%)</option></select></div>
 <div><label for="px">Image size</label><select id="px"><option value="256">256 px</option><option value="512">512 px</option><option value="1024" selected>1024 px</option><option value="2048">2048 px (print)</option></select></div></div>
 <div class="row2"><div><label for="fg">Code colour</label><input id="fg" type="color" value="#000000" style="padding:4px"></div><div><label for="bg">Background</label><input id="bg" type="color" value="#ffffff" style="padding:4px"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Your QR code</div>
 <div style="margin:10px 0 4px;text-align:center"><canvas id="cv" width="1024" height="1024" role="img" aria-label="QR code preview" style="width:100%;max-width:260px;height:auto;image-rendering:pixelated;border:1px solid var(--line);border-radius:8px;background:#fff"></canvas></div>
 <p class="warn" id="err" hidden></p>
 <ul class="lines" id="lines"></ul>
 <p style="margin:14px 0 0;display:flex;gap:8px;flex-wrap:wrap"><a class="btn primary" id="dpng" href="#" download="qr-code.png">Download PNG</a><a class="btn" id="dsvg" href="#" download="qr-code.svg">Download SVG</a></p>
 <p class="formula" style="overflow-wrap:anywhere">Encoded text: <code id="raw"></code></p>
</div>""",
js=QR_JS + r"""
// keep the Wi-Fi password out of the page's saved inputs
{ const p0 = $('wpass'), p = p0.cloneNode(); p.value = ''; p0.replaceWith(p); }
const NAMES = { url: 'Link', text: 'Text', wifi: 'Wi-Fi', wa: 'WhatsApp', email: 'Email', tel: 'Phone', upi: 'UPI payment' };
const ECP = { L: '7%', M: '15%', Q: '25%', H: '30%' };
const esc = s => s.replace(/([\\;,:"])/g, '\\$1');
let pngUrl = null, svgUrl = null, timer = null;
function payload() {
  const k = $('kind').value, v = id => $(id).value.trim(), warn = [];
  if (k === 'url') { let u = v('url'); if (!u) return { err: 'Enter a link.' };
    if (!/^[a-z][a-z0-9+.-]*:/i.test(u)) { if (!/\./.test(u)) return { err: 'This does not look like a link. Choose Plain text for other words.' }; u = 'https://' + u; warn.push('Added https:// so phones open it as a link.'); }
    if (/\s/.test(u)) warn.push('The link contains spaces; check it opens correctly.'); return { s: u, warn }; }
  if (k === 'text') { const t = $('txt').value; return t ? { s: t, warn } : { err: 'Enter some text.' }; }
  if (k === 'wifi') { const ss = $('ssid').value, pw = $('wpass').value, sec = $('wsec').value;
    if (!ss) return { err: 'Enter the Wi-Fi network name exactly as it appears on your phone.' };
    if (sec !== 'nopass' && !pw) return { err: 'Enter the Wi-Fi password, or choose Security: None for an open network.' };
    if (sec === 'WPA' && (pw.length < 8 || pw.length > 63)) warn.push('WPA passwords are usually 8 to 63 characters. Check the password.');
    if (ss !== ss.trim() || pw !== pw.trim()) warn.push('The name or password starts or ends with a space. Keep it only if your network really has one.');
    return { s: 'WIFI:T:' + sec + ';S:' + esc(ss) + ';' + (sec !== 'nopass' ? 'P:' + esc(pw) + ';' : '') + ($('whid').checked ? 'H:true;' : '') + ';', warn }; }
  if (k === 'wa') { const raw = v('wanum'); let n = raw.replace(/[^\d]/g, '');
    if (raw.startsWith('00')) n = n.replace(/^00/, '');
    if (!n) return { err: 'Enter the WhatsApp number with its country code.' };
    if (n.length < 8 || n.length > 15) return { err: 'International numbers have 8 to 15 digits including the country code. You entered ' + n.length + '.' };
    if (n[0] === '0') warn.push('Numbers should start with the country code (for example 91 or 971), not 0.');
    const m = v('wamsg'); return { s: 'https://wa.me/' + n + (m ? '?text=' + encodeURIComponent(m) : ''), warn }; }
  if (k === 'email') { const a = v('mto'); if (!a) return { err: 'Enter an email address.' };
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(a)) return { err: 'Check the email address.' };
    const q = [['subject', v('msub')], ['body', v('mbody')]].filter(x => x[1]).map(([a, b]) => a + '=' + encodeURIComponent(b)).join('&');
    return { s: 'mailto:' + a + (q ? '?' + q : ''), warn }; }
  if (k === 'tel') { const t = v('tel'), n = t.replace(/[^\d+]/g, '').replace(/(?!^)\+/g, '');
    if (n.replace('+', '').length < 3) return { err: 'Enter a phone number.' };
    if (n[0] !== '+') warn.push('Add + and the country code so the number works from abroad.'); return { s: 'tel:' + n, warn }; }
  if (k === 'upi') { const pa = v('upa'), pn = v('upn'), am = v('uam');
    if (!pa) return { err: 'Enter the UPI ID that should receive the money.' };
    if (!/^[\w.\-]{2,}@[a-z][a-z0-9.\-]*$/i.test(pa)) return { err: 'A UPI ID looks like name@bank. Check it.' };
    if (am && !(+am > 0)) return { err: 'Enter the amount as a number, for example 250 or 99.50, or leave it empty.' };
    const p = [['pa', pa], ['pn', pn], ['am', am ? (+am).toFixed(2) : ''], ['cu', 'INR'], ['tn', v('utn')]].filter(x => x[1]);
    if (!pn) warn.push('Add the payee name so the payer can check who they are paying.');
    return { s: 'upi://pay?' + p.map(([a, b]) => a + '=' + encodeURIComponent(b)).join('&'), warn }; }
}
const hex = c => [1, 3, 5].map(i => parseInt(c.substr(i, 2), 16) / 255);
const lum = c => { const [r, g, b] = hex(c).map(x => x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4)); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
function show(warns, isErr) { const e = $('err'); e.hidden = !warns.length; e.innerHTML = warns.map(w => (isErr ? '' : '⚠ ') + w).join('<br>'); e.style.color = isErr ? 'var(--dn)' : ''; }
function off(on) { ['dpng', 'dsvg'].forEach(id => { const a = $(id); a.style.opacity = on ? '' : '.45'; a.style.pointerEvents = on ? '' : 'none'; a.setAttribute('aria-disabled', !on); }); }
function blank() { const c = $('cv'), x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height); $('lines').innerHTML = ''; $('raw').textContent = ''; off(false); }
function calc() {
  document.querySelectorAll('[data-k]').forEach(d => d.hidden = d.dataset.k !== $('kind').value);
  const p = payload(); if (p.err) { show([p.err], true); blank(); return; }
  const e = $('ecl').value, r = QR.encode(p.s, e);
  if (r.error) { const unit = r.mode === 'byte' ? 'bytes' : 'characters';
    show(['Too long for one QR code at level ' + e + ': ' + F(r.n, 0) + ' ' + unit + ', the limit is ' + F(r.max, 0) + ' ' + unit + '. Shorten it' + (e !== 'L' ? ' or choose a lower error-correction level' : '') + '. Long text is easier to scan as a link to a web page.'], true); blank(); return; }
  const fg = $('fg').value, bg = $('bg').value, lf = lum(fg), lb = lum(bg), cr = (Math.max(lf, lb) + 0.05) / (Math.min(lf, lb) + 0.05), warns = p.warn.slice();
  if (lf > lb) warns.push('The code is lighter than the background. Many scanners cannot read inverted codes; use a dark code on a light background.');
  else if (cr < 4) warns.push('Low contrast (' + F(cr, 1) + ':1). Some phones may not read it; aim for a dark code on a light background.');
  if (r.version > 25) warns.push('This is a dense code. Print it large, or shorten the content (a short link scans more easily).');
  show(warns, false);
  const n = r.size, q = 4, tot = n + 2 * q, want = Math.max(+$('px').value, tot), mod = Math.floor(want / tot), side = want, off0 = Math.floor((side - mod * tot) / 2) + q * mod;
  const c = $('cv'); c.width = side; c.height = side; const x = c.getContext('2d');
  x.fillStyle = bg; x.fillRect(0, 0, side, side); x.fillStyle = fg;
  for (let y = 0; y < n; y++) for (let i = 0; i < n; i++) if (r.M[y][i]) x.fillRect(off0 + i * mod, off0 + y * mod, mod, mod);
  let d = ''; for (let y = 0; y < n; y++) for (let i = 0; i < n; i++) if (r.M[y][i]) { let j = i; while (j < n && r.M[y][j]) j++; d += 'M' + (i + q) + ' ' + (y + q) + 'h' + (j - i) + 'v1h-' + (j - i) + 'z'; i = j; }
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + tot + ' ' + tot + '" width="' + side + '" height="' + side + '" shape-rendering="crispEdges"><rect width="100%" height="100%" fill="' + bg + '"/><path fill="' + fg + '" d="' + d + '"/></svg>';
  if (svgUrl) URL.revokeObjectURL(svgUrl); svgUrl = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' })); $('dsvg').href = svgUrl;
  c.toBlob(b => { if (!b) return; if (pngUrl) URL.revokeObjectURL(pngUrl); pngUrl = URL.createObjectURL(b); $('dpng').href = pngUrl; }, 'image/png');
  const name = 'qr-' + $('kind').value; $('dpng').download = name + '.png'; $('dsvg').download = name + '.svg';
  const unit = r.mode === 'byte' ? 'bytes' : 'characters', left = r.max - r.n;
  $('lines').innerHTML = [['Opens', NAMES[$('kind').value]], ['Content', F(r.n, 0) + ' ' + unit], ['Code size', 'version ' + r.version + ', ' + n + ' × ' + n + ' squares'], ['Survives damage up to', 'about ' + ECP[e]], ['Image', side + ' × ' + side + ' px'], ['Room left at level ' + e, F(left, 0) + ' ' + unit]].map(([a, v]) => """ + ROW + r""").join('');
  $('raw').textContent = p.s; off(true);
}
const later = () => { clearTimeout(timer); timer = setTimeout(calc, 120); };
document.querySelectorAll('.inputs input, .inputs select, .inputs textarea').forEach(el => el.addEventListener('input', later));
calc();
""",
body="""
<h2>How to make a QR code</h2>
<ol><li>Choose what the code should open: a link, a Wi-Fi network, a WhatsApp chat, an email, a phone call, a UPI payment or plain text.</li><li>Fill in the details. The preview updates as you type.</li><li>Pick a colour and size, then tap <em>Download PNG</em> for phones, documents and social posts, or <em>Download SVG</em> for printing and design software (it stays sharp at any size).</li><li>Scan the downloaded code with your own phone before you print it.</li></ol>
<p>The code is drawn by this page on your device. Nothing you type is sent to a server, there is no account, and the code never expires because it contains the information itself rather than a redirect link.</p>
<h3>What each type puts inside the code</h3>
<div class="scroll"><table><thead><tr><th>Type</th><th>Text stored in the code</th><th>What the phone does</th></tr></thead><tbody>
<tr><td>Link</td><td>https://www.example.com</td><td>Offers to open the page</td></tr>
<tr><td>Wi-Fi</td><td>WIFI:T:WPA;S:Home;P:secret123;;</td><td>Offers to join the network</td></tr>
<tr><td>WhatsApp</td><td>https://wa.me/971501234567?text=Hello</td><td>Opens a chat with the message typed in</td></tr>
<tr><td>Email</td><td>mailto:name@example.com?subject=Hi</td><td>Opens a new email</td></tr>
<tr><td>Phone</td><td>tel:+442079460000</td><td>Offers to call</td></tr>
<tr><td>UPI</td><td>upi://pay?pa=name@bank&amp;pn=Name&amp;am=250.00&amp;cu=INR</td><td>Opens a UPI app with the payee filled in</td></tr></tbody></table></div>
<h3>Worked example: a Wi-Fi QR code</h3>
<p>Network <em>Sharma Home</em>, WPA2, password <em>mango;tree42</em>. The semicolon is a separator in the Wi-Fi format, so it is written as <code>\\;</code>, and the code holds <code>WIFI:T:WPA;S:Sharma Home;P:mango\\;tree42;;</code>, which is 42 bytes. At level M that fits in a version 3 code of 29 × 29 squares; at level H it needs version 5, 37 × 37 squares. Guests point their camera at it and tap <em>Join</em>. Backslashes, semicolons, commas, colons and double quotes are escaped automatically.</p>
<h3>Error correction: which level?</h3>
<div class="scroll"><table><thead><tr><th>Level</th><th>Damage it can survive</th><th>Best for</th></tr></thead><tbody>
<tr><td>L</td><td>about 7%</td><td>Long text on screens</td></tr><tr><td>M</td><td>about 15%</td><td>Most uses (default)</td></tr><tr><td>Q</td><td>about 25%</td><td>Printed signs and stickers</td></tr><tr><td>H</td><td>about 30%</td><td>Codes that may get scratched or dirty</td></tr></tbody></table></div>
<p>Higher levels make the pattern denser, so they need a larger print to scan from the same distance. The largest QR code holds 2,953 bytes at level L and 1,273 at level H; this page tells you when your content is too long.</p>
<h3>Tips for codes that scan first time</h3>
<ul><li>Keep a dark code on a light background with strong contrast. Light-on-dark codes fail on many scanners.</li><li>Leave the white border (quiet zone). The download includes the standard four-square margin; do not crop it.</li><li>For long text, put it on a web page and make a QR code for the link instead.</li><li>For UPI, check the name your UPI app shows before paying. Shops that need payment records should use the QR code issued by their bank or UPI app.</li></ul>
""",
faqs=[("How do I make a QR code for my Wi-Fi?", "Choose Wi-Fi network, type the network name and password exactly, pick the security type (WPA for most home routers) and download the code. Phones that scan it offer to join the network."),
      ("Do these QR codes expire?", "No. The link, text or Wi-Fi details are stored inside the code itself, so it keeps working for as long as the information in it is correct. There is no redirect service that can be switched off."),
      ("Should I download PNG or SVG?", "PNG is an image for phones, documents, WhatsApp and social posts. SVG is a vector file that stays sharp at any size, so it is better for printing posters, menus and stickers."),
      ("Is my Wi-Fi password or data uploaded?", "No. The code is created in your browser and nothing you type is sent anywhere. The Wi-Fi password is not saved by the page either.")],
sources=[("ZXing: barcode contents (Wi-Fi, email and phone formats)", "https://github.com/zxing/zxing/wiki/Barcode-Contents"),
         ("WhatsApp Help Center: how to use click to chat", "https://whatsapp.com/faq/en/general/26000030"),
         ("Google Pay for Business (India): UPI payment link parameters", "https://developers.google.com/pay/india/api/android/in-app-payments"),
         ("KEYENCE: QR code basics (error-correction levels, margin, capacity)", "https://www.keyence.com/ss/products/auto_id/codereader/basic_2d/qr.jsp")]))
