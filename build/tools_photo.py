from tools_unique import TOOLS

# ---------------- Photos & documents: photo resizer ----------------
TOOLS.append(dict(
group="docs", slug="photo-resizer", icon="photo",
name="Photo Resizer for Applications",
title="Photo Resizer: Crop, Resize & Compress to KB for Kerala PSC, SSC, Visa Forms",
desc="Crop, resize and compress a photo or signature to the exact pixels and KB an online form asks for: Kerala PSC 150×200 under 30 KB, 3.5×4.5 cm, US visa 600×600, UAE visa 43×55 mm. Works in your browser; nothing is uploaded.",
keywords="photo resizer, resize photo to 20kb, resize photo to 50kb, kerala psc photo resize, psc photo 150x200 30kb, passport size photo 3.5x4.5, signature resize 20kb, us visa photo 600x600, uae visa photo size, photo compressor kb, university application photo size",
h1="Photo resizer for applications",
lede="Crop, resize and compress your photo or signature to the exact size an online form asks for. Your photo stays on your phone: nothing is uploaded.",
card="Crop, resize, compress to KB, add name & date",
tool="""
<div class="photo-pick">
 <label class="btn primary pick-btn">Choose photo<input type="file" id="file" accept="image/*"></label>
 <span class="hint" id="fname">JPG, PNG or WebP from your gallery or camera.</span>
</div>
<div class="inputs">
 <div><label for="preset">Size for</label>
 <select id="preset">
  <option value="psc">Kerala PSC photo: 150 × 200 px, up to 30 KB</option>
  <option value="pp">Passport size 3.5 × 4.5 cm: 413 × 531 px, 20–50 KB</option>
  <option value="bank">Bank / RBI exam photo: 200 × 230 px, 20–50 KB</option>
  <option value="sign">Signature: 140 × 60 px, 10–20 KB</option>
  <option value="us">US visa (DS-160): 600 × 600 px, up to 240 KB</option>
  <option value="uae">UAE visa 43 × 55 mm: 508 × 650 px</option>
  <option value="sq">Square profile photo: 800 × 800 px</option>
  <option value="orig">Keep original shape (resize only)</option>
  <option value="custom">Custom size</option>
 </select></div>
 <div class="row2"><div><label for="pw">Width (px)</label><input id="pw" inputmode="numeric" value="150"></div>
 <div><label for="ph">Height (px)</label><input id="ph" inputmode="numeric" value="200"></div></div>
 <div class="row2"><div><label for="minkb">Minimum size (KB)</label><input id="minkb" inputmode="decimal" value="0"></div>
 <div><label for="maxkb">Maximum size (KB)</label><input id="maxkb" inputmode="decimal" value="30"><div class="hint">0 = no limit</div></div></div>
 <div class="row2"><div><label for="fmt">Format</label><select id="fmt"><option value="jpg">JPG</option><option value="png">PNG</option></select></div>
 <div><label for="bg">Background</label><select id="bg"><option value="#ffffff">White</option><option value="#f2f2f2">Light grey</option></select></div></div>
</div>
<div class="crop-wrap"><canvas id="pv" width="300" height="400" aria-label="Crop preview: drag to move the photo"></canvas></div>
<p class="hint" style="text-align:center;margin:6px 0 10px">Drag the photo to position it. Use the zoom slider (or pinch) to fit your face.</p>
<div class="inputs">
 <div><label for="zoom">Zoom</label><input type="range" id="zoom" min="100" max="400" value="100"></div>
 <div><label for="br">Brightness</label><input type="range" id="br" min="70" max="140" value="100"></div>
</div>
<div class="photo-actions"><button type="button" class="btn" id="rot">Rotate 90°</button><button type="button" class="btn" id="reset">Reset position</button></div>
<div class="photo-band">
 <label class="chk"><input type="checkbox" id="band"> Add name and date at the bottom</label>
 <div class="row2" id="bandf" hidden><div><label for="nm">Name</label><input id="nm" autocomplete="name" placeholder="Your name"></div>
 <div><label for="dt">Date of photo</label><input id="dt" type="date"></div></div>
</div>
<div class="result" aria-live="polite">
 <div class="big-label">Your file</div><div class="big" id="out">—</div>
 <ul class="lines" id="lines"></ul>
 <p id="warn" class="formula"></p>
 <p style="margin:12px 0 0"><a class="btn primary" id="dl" href="#" download hidden>Download photo</a></p>
</div>""",
js=r"""
const PRE = { psc: [150, 200, 0, 30, 1], pp: [413, 531, 20, 50, 0], bank: [200, 230, 20, 50, 0], sign: [140, 60, 10, 20, 0],
  us: [600, 600, 0, 240, 0], uae: [508, 650, 0, 0, 0], sq: [800, 800, 0, 0, 0] };
let img = null, rot = 0, zoom = 1, ox = 0, oy = 0, url = null, timer = null;
const pv = $('pv'), pc = pv.getContext('2d');
const dims = () => [Math.min(4000, Math.max(16, Math.round(V('pw')) || 16)), Math.min(4000, Math.max(16, Math.round(V('ph')) || 16))];
function srcSize() { return rot % 180 ? [img.height, img.width] : [img.width, img.height]; }
function bandOn() { return $('band').checked; }
function dateText() { const v = $('dt').value; if (!v) return ''; const [y, m, d] = v.split('-'); return d + '/' + m + '/' + y; }
function draw(ctx, w, h) {
  ctx.save(); ctx.fillStyle = $('bg').value; ctx.fillRect(0, 0, w, h);
  if (img) {
    const [sw, sh] = srcSize(), s = Math.max(w / sw, h / sh) * zoom;
    ctx.translate(w / 2 + ox * w, h / 2 + oy * h); ctx.rotate(rot * Math.PI / 180); ctx.scale(s, s);
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(img, -img.width / 2, -img.height / 2);
  }
  ctx.restore();
  const b = V('br') / 100;
  if (img && b !== 1) {
    const d = ctx.getImageData(0, 0, w, h), p = d.data;
    for (let i = 0; i < p.length; i += 4) { p[i] = Math.min(255, p[i] * b); p[i + 1] = Math.min(255, p[i + 1] * b); p[i + 2] = Math.min(255, p[i + 2] * b); }
    ctx.putImageData(d, 0, 0);
  }
  if (bandOn()) {
    const bh = Math.max(14, Math.round(h * 0.17)), lines = [$('nm').value.trim().toUpperCase(), dateText()].filter(Boolean);
    ctx.fillStyle = '#ffffff'; ctx.fillRect(0, h - bh, w, bh);
    ctx.fillStyle = '#000000'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    lines.forEach((t, i) => {
      let fs = Math.max(7, Math.floor(bh / (lines.length > 1 ? 2.4 : 1.8)));
      do { ctx.font = '700 ' + fs + 'px Arial, Helvetica, sans-serif'; fs--; } while (ctx.measureText(t).width > w * 0.94 && fs > 6);
      ctx.fillText(t, w / 2, h - bh + bh * (lines.length > 1 ? (i ? 0.72 : 0.3) : 0.5));
    });
  }
}
function preview() {
  const [w, h] = dims(), k = 520 / Math.max(w, h);
  pv.width = Math.round(w * k); pv.height = Math.round(h * k);
  pv.style.aspectRatio = w + ' / ' + h;
  draw(pc, pv.width, pv.height);
  if (!img) { pc.fillStyle = '#8a8f98'; pc.textAlign = 'center'; pc.textBaseline = 'middle'; pc.font = '600 ' + Math.round(pv.width / 14) + 'px Inter, Arial, sans-serif'; pc.fillText('Tap here to choose', pv.width / 2, pv.height / 2 - pv.width / 22); pc.fillText('a photo', pv.width / 2, pv.height / 2 + pv.width / 22); }
}
const enc = (c, type, q) => new Promise(r => c.toBlob(r, type, q));
async function make() {
  preview();
  const [w, h] = dims(), mx = V('maxkb') * 1024, mn = V('minkb') * 1024, png = $('fmt').value === 'png';
  if (!img) { $('out').textContent = '—'; $('lines').innerHTML = ''; $('warn').textContent = ''; $('dl').hidden = true; return; }
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  let b, q = 0.92;
  if (png) b = await enc(c, 'image/png');
  else {
    b = await enc(c, 'image/jpeg', q);
    if (mx > 0 && b.size > mx) {
      let lo = 0.05, hi = 0.92, best = null, bq = 0.05;
      for (let i = 0; i < 9; i++) { const mid = (lo + hi) / 2, t = await enc(c, 'image/jpeg', mid); if (t.size <= mx) { best = t; bq = mid; lo = mid; } else hi = mid; }
      if (best) { b = best; q = bq; } else { b = await enc(c, 'image/jpeg', 0.05); q = 0.05; }
    } else if (mn > 0 && b.size < mn) {
      for (const tq of [0.95, 0.97, 0.98, 0.99, 1]) {
        const t = await enc(c, 'image/jpeg', tq);
        if (mx > 0 && t.size > mx) break;
        b = t; q = tq; if (t.size >= mn) break;
      }
    }
  }
  const kb = b.size / 1024;
  $('out').textContent = F(kb, 1) + ' KB';
  $('lines').innerHTML = [['Size in pixels', w + ' × ' + h], ['Format', png ? 'PNG' : 'JPG'], ...(png ? [] : [['JPG quality', Math.round(q * 100) + '%']]), ['At 300 DPI', F(w / 300 * 2.54, 2) + ' × ' + F(h / 300 * 2.54, 2) + ' cm']]
    .map(([a, v]) => `<li><span>${a}</span><b>${v}</b></li>`).join('');
  let warn = '';
  if (mx > 0 && b.size > mx) warn = 'Still above ' + F(V('maxkb'), 0) + ' KB. Reduce the width and height, or choose JPG.';
  else if (mn > 0 && b.size < mn) warn = 'Below the ' + F(V('minkb'), 0) + ' KB minimum. Increase the width and height a little.';
  else warn = 'Matches the size you set. Check the form\'s own instructions for background, face size and date rules.';
  $('warn').textContent = warn;
  if (url) URL.revokeObjectURL(url);
  url = URL.createObjectURL(b);
  const a = $('dl'); a.href = url; a.download = 'photo-' + w + 'x' + h + (png ? '.png' : '.jpg'); a.hidden = false;
}
const later = () => { preview(); clearTimeout(timer); timer = setTimeout(make, 250); };
function applyPreset() {
  const p = $('preset').value;
  if (PRE[p]) { const [w, h, mn, mx, band] = PRE[p]; $('pw').value = w; $('ph').value = h; $('minkb').value = mn; $('maxkb').value = mx; $('band').checked = !!band; }
  if (p === 'orig' && img) { const [sw, sh] = srcSize(); $('ph').value = Math.round(V('pw') * sh / sw); $('minkb').value = 0; $('maxkb').value = 0; }
  $('bandf').hidden = !bandOn(); later();
}
$('preset').addEventListener('change', applyPreset);
['pw', 'ph', 'minkb', 'maxkb', 'nm', 'dt'].forEach(id => $(id).addEventListener('input', () => {
  if (id === 'pw' && $('preset').value === 'orig' && img) { const [sw, sh] = srcSize(); $('ph').value = Math.round(V('pw') * sh / sw); }
  later();
}));
['fmt', 'bg'].forEach(id => $(id).addEventListener('change', later));
$('band').addEventListener('change', () => { $('bandf').hidden = !bandOn(); later(); });
$('zoom').addEventListener('input', () => { zoom = V('zoom') / 100; later(); });
$('br').addEventListener('input', later);
$('rot').addEventListener('click', () => { rot = (rot + 90) % 360; if ($('preset').value === 'orig') applyPreset(); else later(); });
$('reset').addEventListener('click', () => { ox = oy = 0; zoom = 1; $('zoom').value = 100; later(); });
$('file').addEventListener('change', e => { const f = e.target.files[0]; if (f) load(f); e.target.value = ''; });
function load(f) {
  const u = URL.createObjectURL(f), im = new Image();
  im.onload = () => { img = im; rot = 0; ox = oy = 0; zoom = 1; $('zoom').value = 100; $('fname').textContent = f.name + ' · ' + im.width + ' × ' + im.height + ' px'; applyPreset(); };
  im.onerror = () => { $('fname').textContent = 'This file could not be opened. Use a JPG or PNG (iPhone HEIC photos: share as JPG first).'; };
  im.src = u;
}
const pts = new Map(); let pinch = 0;
pv.addEventListener('click', () => { if (!img) $('file').click(); });
pv.addEventListener('pointerdown', e => { if (!img) return; try { pv.setPointerCapture(e.pointerId); } catch (x) {} pts.set(e.pointerId, [e.clientX, e.clientY]); });
const wrap = document.querySelector('.crop-wrap');
wrap.addEventListener('dragover', e => e.preventDefault());
wrap.addEventListener('drop', e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) load(f); });
pv.addEventListener('pointermove', e => {
  if (!pts.has(e.pointerId) || !img) return;
  const r = pv.getBoundingClientRect(), [px, py] = pts.get(e.pointerId);
  if (pts.size === 1) { ox += (e.clientX - px) / r.width; oy += (e.clientY - py) / r.height; }
  pts.set(e.pointerId, [e.clientX, e.clientY]);
  if (pts.size === 2) {
    const [a, b] = [...pts.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]);
    if (pinch) { zoom = Math.min(4, Math.max(1, zoom * d / pinch)); $('zoom').value = Math.round(zoom * 100); }
    pinch = d;
  }
  later();
});
const up = e => { pts.delete(e.pointerId); if (pts.size < 2) pinch = 0; };
pv.addEventListener('pointerup', up); pv.addEventListener('pointercancel', up);
pv.addEventListener('wheel', e => { if (!img) return; e.preventDefault(); zoom = Math.min(4, Math.max(1, zoom * Math.pow(1.1, -e.deltaY / 100))); $('zoom').value = Math.round(zoom * 100); later(); }, { passive: false });
$('dt').value = new Date().toISOString().slice(0, 10);
$('bandf').hidden = !bandOn();
preview(); make();
""",
body="""
<h2>How to get a photo accepted first time</h2>
<p>Online forms check four things separately: the <strong>size in pixels</strong>, the <strong>file size in KB</strong>, the <strong>file format</strong> and, for many exams, a <strong>name and date</strong> on the photo. This tool handles all four in one step:</p>
<ol><li>Choose your photo and pick the form from the list, or enter your own width, height and KB limits.</li>
<li>Drag and zoom until your face fills most of the frame, with a little space above the head.</li>
<li>Tick <em>Add name and date</em> if the notification asks for it.</li>
<li>Download. The tool lowers the JPG quality only as far as needed to fit under the maximum KB.</li></ol>
<h3>Common sizes</h3>
<div class="scroll"><table><thead><tr><th>Form</th><th>Pixels (W × H)</th><th>File size</th></tr></thead><tbody>
<tr><td>Kerala PSC (One Time Registration)</td><td>150 × 200</td><td>up to 30 KB, JPG, name and date at the bottom</td></tr>
<tr><td>Passport-size 3.5 × 4.5 cm (many Indian exams)</td><td>413 × 531 at 300 DPI</td><td>often 20–50 KB</td></tr>
<tr><td>Bank and RBI exams (photo)</td><td>200 × 230</td><td>20–50 KB</td></tr>
<tr><td>Bank and RBI exams (signature)</td><td>140 × 60</td><td>10–20 KB</td></tr>
<tr><td>US visa, DS-160</td><td>600 × 600 to 1200 × 1200, square</td><td>up to 240 KB, JPG</td></tr>
<tr><td>UAE visa (43 × 55 mm print size)</td><td>508 × 650 at 300 DPI</td><td>check the portal's limit</td></tr>
</tbody></table></div>
<p>Rules differ between notifications and change over time. Always follow the instructions in the notification or portal you are applying through.</p>
<h3>Worked example: Kerala PSC</h3>
<p>A phone photo of 3024 × 4032 pixels is about 3 MB. Choose <em>Kerala PSC photo</em>, zoom so your face fills the frame, add your name and today's date, and download: the result is 150 × 200 pixels and typically 8–15 KB, well under the 30 KB limit.</p>
<h3>Tips</h3>
<ul><li>Stand facing a plain light wall in daylight; avoid shadows behind you.</li><li>For a signature, sign in black ink on white paper, photograph it flat, then choose <em>Signature</em>.</li><li>If a portal says the file is too small, raise the width and height slightly; some portals count 1 KB as 1,000 bytes rather than 1,024.</li></ul>
<h3>Privacy</h3>
<p>Your photo is processed by your own browser. It is not uploaded to CalcSouq or anyone else.</p>
""",
faqs=[("How do I reduce a photo to under 50 KB?", "Choose your photo, set the maximum size to 50 KB and download. The tool lowers the JPG quality step by step until the file fits, keeping the pixel size you chose."),
      ("What is the Kerala PSC photo size?", "150 pixels wide by 200 pixels high, JPG, up to 30 KB, with the candidate's name and the date of the photo printed at the bottom."),
      ("What size is 3.5 × 4.5 cm in pixels?", "About 413 × 531 pixels at 300 DPI. Some portals use 200 DPI (about 276 × 354 pixels); follow the pixel size in your notification if one is given."),
      ("Is my photo uploaded anywhere?", "No. Cropping, resizing and compression happen in your browser on your own device.")],
sources=[("Kerala PSC", "https://www.keralapsc.gov.in"), ("US Department of State: digital image requirements", "https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/photos/digital-image-requirements.html"),
         ("UAE ICP", "https://icp.gov.ae"), ("Reserve Bank of India: photo and signature scanning guidelines (exam notice)", "https://website.rbi.org.in/documents/87730/39016390/RPJECE07012019_AN1.pdf")],
))

# ---------- Focused landing pages: same tool, preset chosen, own text ----------
_BASE = TOOLS[-1]
def _variant(slug, preset, w, h, mn, mx, band, **k):
    t = dict(_BASE); t.update(k); t["slug"] = slug
    html_ = _BASE["tool"].replace('<option value="psc">', '<option value="psc">').replace(f'<option value="{preset}">', f'<option value="{preset}" selected>')
    html_ = html_.replace('id="pw" inputmode="numeric" value="150"', f'id="pw" inputmode="numeric" value="{w}"').replace('id="ph" inputmode="numeric" value="200"', f'id="ph" inputmode="numeric" value="{h}"')
    html_ = html_.replace('id="minkb" inputmode="decimal" value="0"', f'id="minkb" inputmode="decimal" value="{mn}"').replace('id="maxkb" inputmode="decimal" value="30"', f'id="maxkb" inputmode="decimal" value="{mx}"')
    if band: html_ = html_.replace('<input type="checkbox" id="band">', '<input type="checkbox" id="band" checked>')
    t["tool"] = html_
    TOOLS.append(t)

_COMMON_TIPS = """<h3>Before you upload</h3>
<ul><li>Use a recent photo against a plain light wall, in daylight, with no shadow behind you.</li>
<li>If the portal says the file is too small, raise the width and height a little; if it is too large, lower the maximum KB.</li>
<li>Your photo is processed in your own browser and is not uploaded anywhere.</li>
<li>Rules can change between notifications: check the one you are applying under.</li></ul>
<p>Need a different size? Use the <a href="/photo-resizer/">full photo resizer</a> with all presets.</p>"""

_variant("kerala-psc-photo-resizer", "psc", 150, 200, 0, 30, True,
 name="Kerala PSC Photo Resizer (150×200, 30 KB, Name & Date)",
 title="Kerala PSC Photo Resizer: 150×200 px, Under 30 KB, With Name & Date",
 desc="Make a Kerala PSC One Time Registration photo in seconds: 150 × 200 pixels, JPG under 30 KB, with your name and the photo date printed at the bottom. Free, works on your phone.",
 keywords="kerala psc photo resizer, psc photo resize 150x200, psc photo 30kb, kerala psc photo with name and date, thulasi photo upload size, psc photo editor online, psc photo name and date online",
 h1="Kerala PSC photo resizer",
 lede="Turn any phone photo into a Kerala PSC-ready JPG: 150 × 200 pixels, under 30 KB, with your name and the date of the photo in a white band at the bottom.",
 card="150 × 200 px, under 30 KB, name and date added",
 body="""<h2>Kerala PSC photo rules</h2>
<p>For One Time Registration on the Thulasi portal, Kerala PSC asks for a JPG photo <strong>150 pixels wide and 200 pixels high</strong>, no larger than <strong>30 KB</strong>, with the <strong>candidate's name and the date the photo was taken</strong> printed at the bottom. The photo must be recent; new registrations need a photo taken within the last six months.</p>
<h3>How to do it here</h3>
<ol><li>Tap <em>Choose photo</em> and pick a clear front-facing photo.</li>
<li>Drag and zoom until your head and the top of your shoulders fill the frame above the white band.</li>
<li>Type your name exactly as in your PSC profile and set the date the photo was taken.</li>
<li>Download. The file is 150 × 200 px and typically 8–20 KB.</li></ol>
<h3>Common rejection reasons</h3>
<ul><li>Name or date missing, or a date that does not match when the photo was taken.</li><li>Wrong pixel size (for example 200 × 150 instead of 150 × 200).</li><li>File above 30 KB, or saved as PNG instead of JPG.</li><li>Dark or patterned background.</li></ul>""" + _COMMON_TIPS,
 faqs=[("What is the photo size for Kerala PSC?", "150 pixels wide × 200 pixels high, JPG, up to 30 KB, with name and date of photo at the bottom."),
       ("How do I add name and date to a PSC photo?", "Tick 'Add name and date at the bottom', type your name and the photo date, then download. The band is added inside the 150 × 200 image."),
       ("How long is a PSC photo valid?", "Kerala PSC notifications say a photo uploaded meeting all requirements is valid for 10 years from the date of uploading; new registrations need a photo taken within the last six months.")])

_variant("resize-photo-to-20kb", "custom", 300, 400, 0, 20, False,
 name="Resize Photo to 20 KB",
 title="Resize Photo to 20 KB Online (Free, Keeps Quality, No Upload)",
 desc="Reduce any photo or signature to under 20 KB in one step. Choose the pixel size, set 20 KB and download a sharp JPG. Free, works on mobile, nothing uploaded.",
 keywords="resize photo to 20kb, compress photo to 20kb, reduce photo size to 20kb, photo 20kb converter, signature 20kb, image to 20kb jpg, 10kb to 20kb photo",
 h1="Resize photo to 20 KB",
 lede="Compress a photo or signature to under 20 KB without making it blurry. Set the size in pixels, and the tool finds the best JPG quality that fits.",
 card="Compress any photo to under 20 KB",
 body="""<h2>How to get a photo under 20 KB</h2>
<p>File size depends mostly on the <strong>number of pixels</strong> and the <strong>JPG quality</strong>. A phone photo of 12 megapixels cannot fit in 20 KB at full size, but a 300 × 400 pixel version easily can.</p>
<ol><li>Choose your photo. The maximum is already set to 20 KB.</li><li>Keep 300 × 400 px, or type the size your form asks for.</li><li>The tool tries quality levels until the file is just under 20 KB, so you keep as much detail as possible.</li></ol>
<div class="scroll"><table><thead><tr><th>Pixel size</th><th>Typical JPG size at good quality</th></tr></thead><tbody>
<tr><td>140 × 60 (signature)</td><td>3–8 KB</td></tr><tr><td>150 × 200</td><td>8–15 KB</td></tr><tr><td>300 × 400</td><td>18–35 KB</td></tr><tr><td>600 × 800</td><td>60–120 KB</td></tr></tbody></table></div>
<p>These are typical ranges; busy backgrounds make files larger. If 20 KB still is not reached, lower the pixel size.</p>
<h3>Forms that ask for 10–20 KB</h3><p>Signatures for bank and many government exams are commonly 10–20 KB. Choose <em>Signature</em> in the list for 140 × 60 px.</p>""" + _COMMON_TIPS,
 faqs=[("How can I reduce a photo to 20 KB?", "Choose the photo, keep the maximum at 20 KB and download. If the result is still too big, lower the width and height."),
       ("Will reducing to 20 KB make my photo blurry?", "Only slightly at small pixel sizes. The tool uses the highest JPG quality that fits, and keeping the pixel size to what the form asks for keeps it sharp."),
       ("Why is my file below the minimum KB?", "Some forms ask for 10–20 KB. Set the minimum to 10 and increase the pixel size a little if the file is too small.")])

_variant("resize-photo-to-50kb", "pp", 413, 531, 20, 50, False,
 name="Resize Photo to 50 KB",
 title="Resize Photo to 50 KB (20–50 KB) for Exam & Job Forms, Free",
 desc="Resize and compress a photo to between 20 KB and 50 KB at 3.5 × 4.5 cm (413 × 531 px), the size many exam and job forms ask for. Free, mobile-friendly, no upload.",
 keywords="resize photo to 50kb, compress photo to 50kb, photo 20kb to 50kb, reduce photo size to 50kb, passport photo 50kb, ssc photo 50kb, exam photo resize",
 h1="Resize photo to 50 KB",
 lede="Get a passport-size photo between 20 KB and 50 KB, the range used by many exam, bank and job portals.",
 card="Photo between 20 and 50 KB, passport size",
 body="""<h2>Photos between 20 KB and 50 KB</h2>
<p>Many recruitment and exam portals accept a JPG photo of <strong>3.5 × 4.5 cm</strong> between <strong>20 KB and 50 KB</strong>. At 300 DPI, 3.5 × 4.5 cm is about <strong>413 × 531 pixels</strong>, which is preset here.</p>
<ol><li>Choose your photo.</li><li>Zoom so your face fills about three quarters of the height.</li><li>Download: the tool keeps the file inside 20–50 KB.</li></ol>
<h3>If your form gives pixels instead of centimetres</h3><p>Some portals ask for 200 × 230 px (common for bank exams) or another size. Type it in the width and height boxes; the KB limits stay the same.</p>""" + _COMMON_TIPS,
 faqs=[("How do I make a photo between 20 KB and 50 KB?", "Set minimum 20 and maximum 50 KB (already set on this page), choose your photo and download."),
       ("What is 3.5 × 4.5 cm in pixels?", "About 413 × 531 pixels at 300 DPI, or 276 × 354 at 200 DPI.")])

_variant("signature-resizer", "sign", 140, 60, 10, 20, False,
 name="Signature Resizer (10–20 KB)",
 title="Signature Resizer: Resize Signature to 140×60 px, 10–20 KB Online",
 desc="Resize a signature photo for online application forms: 140 × 60 pixels, between 10 KB and 20 KB, white background, JPG. Crop from a phone photo in seconds.",
 keywords="signature resizer, resize signature 20kb, signature 140x60, signature size for online form, signature 10kb to 20kb, compress signature online, signature photo resize",
 h1="Signature resizer",
 lede="Photograph your signature on white paper and turn it into the small JPG online forms ask for: 140 × 60 px, 10–20 KB.",
 card="Signature to 140 × 60 px, 10–20 KB",
 body="""<h2>Making a clean signature file</h2>
<ol><li>Sign in <strong>black ink</strong> on plain white paper, a little larger than usual.</li>
<li>Photograph it flat in daylight, straight from above.</li>
<li>Choose the photo, zoom and drag so the signature fills the box with a small margin.</li>
<li>Raise <em>Brightness</em> until the paper looks white, then download.</li></ol>
<p>The preset is 140 × 60 pixels and 10–20 KB, used by many bank and RBI exam forms. Other forms use sizes such as 3.5 × 1.5 cm or 4 × 2 cm; type the pixel size your notification gives.</p>""" + _COMMON_TIPS,
 faqs=[("What is the signature size for online forms?", "It varies. 140 × 60 pixels at 10–20 KB is common for bank exams; always check your notification."),
       ("How do I make the paper background white?", "Photograph in daylight and increase the Brightness slider before downloading.")])

_variant("passport-size-photo-maker", "pp", 413, 531, 0, 0, False,
 name="Passport Size Photo Maker (3.5 × 4.5 cm)",
 title="Passport Size Photo Maker Online: 3.5 × 4.5 cm (413×531 px), Free",
 desc="Make a 3.5 × 4.5 cm passport-size photo from your phone photo: crop, white background, exact pixels and KB for online forms. Free, private, no upload.",
 keywords="passport size photo maker, passport size photo online, 3.5 x 4.5 cm photo, passport photo 413x531, passport size photo for online form, make passport photo on mobile",
 h1="Passport size photo maker",
 lede="Crop any phone photo to the standard 3.5 × 4.5 cm passport size, at the exact pixels and file size an online form asks for.",
 card="3.5 × 4.5 cm photo from your phone",
 body="""<h2>What "passport size" means</h2>
<p>In India and the Gulf, passport size usually means <strong>3.5 cm wide × 4.5 cm high</strong>. For online forms that equals about <strong>413 × 531 pixels</strong> at 300 DPI. The face should fill roughly 70–80% of the height, with a plain light background.</p>
<p>This page makes the digital file for online applications. Passport offices and visa centres often take their own photo or require prints from a studio, so check their instructions.</p>
<h3>Other common photo sizes</h3>
<div class="scroll"><table><thead><tr><th>Use</th><th>Size</th></tr></thead><tbody><tr><td>Kerala PSC</td><td>150 × 200 px, up to 30 KB</td></tr><tr><td>US visa (DS-160)</td><td>600 × 600 px, up to 240 KB</td></tr><tr><td>UAE visa</td><td>43 × 55 mm print size</td></tr></tbody></table></div>""" + _COMMON_TIPS,
 faqs=[("What size is a passport size photo?", "Usually 3.5 × 4.5 cm, about 413 × 531 pixels at 300 DPI."),
       ("Can I use this for my actual passport application?", "Use it for online forms that accept an uploaded photo. For passports, follow your passport office's own photo rules.")])

_variant("us-visa-photo-resizer", "us", 600, 600, 0, 240, False,
 name="US Visa Photo Resizer (600×600, DS-160)",
 title="US Visa Photo Resizer for DS-160: 600×600 px, Under 240 KB",
 desc="Prepare your DS-160 photo: square 600 × 600 pixels, JPG, under 240 KB, white background, as set out by the US Department of State. Free, no upload.",
 keywords="us visa photo resizer, ds-160 photo size, ds160 photo 600x600, us visa photo 240kb, us visa photo online, ds-160 photo upload",
 h1="US visa photo resizer (DS-160)",
 lede="Make your DS-160 photo square, 600 × 600 pixels and under 240 KB, as the US Department of State requires for online visa applications.",
 card="DS-160 photo: 600 × 600 px, under 240 KB",
 body="""<h2>DS-160 digital photo requirements</h2>
<ul><li>Square: height equal to width, from <strong>600 × 600</strong> up to <strong>1200 × 1200</strong> pixels.</li><li><strong>JPG</strong>, colour, <strong>240 KB or less</strong>.</li><li>Plain white or off-white background, full face, eyes open, no glasses.</li><li>Taken within the last six months.</li></ul>
<p>Choose your photo, zoom so your head fills about half to two thirds of the height, and download. The US Department of State also has its own photo tool; the embassy or consulate decides whether a photo is accepted.</p>""" + _COMMON_TIPS,
 faqs=[("What is the DS-160 photo size?", "Square, between 600 × 600 and 1200 × 1200 pixels, JPG, no more than 240 KB."),
       ("Can I wear glasses in a US visa photo?", "No. Glasses are not allowed in US visa photos except in rare medical cases.")])

_variant("uae-visa-photo-resizer", "uae", 508, 650, 0, 0, False,
 name="UAE Visa Photo Resizer (43 × 55 mm)",
 title="UAE Visa Photo Size Resizer: 43×55 mm, White Background, Free",
 desc="Prepare a UAE visa or residency photo at the 43 × 55 mm proportion (508 × 650 px at 300 DPI) with a white background. Free, private, works on your phone.",
 keywords="uae visa photo size, uae visa photo resizer, dubai visa photo 43x55, uae residence visa photo, emirates id photo size, icp photo specifications",
 h1="UAE visa photo resizer",
 lede="Crop your photo to the 43 × 55 mm UAE visa proportion with a white background, ready to upload to ICP, GDRFA or a typing centre.",
 card="43 × 55 mm, white background",
 body="""<h2>UAE visa photo basics</h2>
<p>UAE visa photos are commonly 43 × 55 mm with a plain white background, the face filling about 70–80% of the photo, and taken within the last six months. ICP's own specifications for Emirates ID photos give a width of 35 to 40 mm, so check which one your application asks for.</p>
<p>The preset here is 508 × 650 pixels (43 × 55 mm at 300 DPI). If a portal asks for a specific pixel size or KB limit, type it in.</p>""" + _COMMON_TIPS,
 faqs=[("What is the UAE visa photo size?", "Commonly 43 × 55 mm with a white background. Portals differ in pixel and file-size limits, so follow the one you upload to."),
       ("What background is needed?", "Plain white, with no patterns or shadows.")])
