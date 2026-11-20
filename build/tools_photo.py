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
 <label class="btn primary" for="file">Choose photo</label>
 <input type="file" id="file" accept="image/*" style="position:absolute;width:1px;height:1px;opacity:0">
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
  if (!img) { pc.fillStyle = '#8a8f98'; pc.textAlign = 'center'; pc.textBaseline = 'middle'; pc.font = '600 ' + Math.round(pv.width / 14) + 'px Inter, Arial, sans-serif'; pc.fillText('Choose a photo', pv.width / 2, pv.height / 2); }
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
$('file').addEventListener('change', e => {
  const f = e.target.files[0]; if (!f) return;
  const u = URL.createObjectURL(f), im = new Image();
  im.onload = () => { img = im; rot = 0; ox = oy = 0; zoom = 1; $('zoom').value = 100; $('fname').textContent = f.name + ' · ' + im.width + ' × ' + im.height + ' px'; applyPreset(); };
  im.onerror = () => { $('fname').textContent = 'This file could not be opened. Use a JPG or PNG (iPhone HEIC photos: share as JPG first).'; };
  im.src = u;
});
const pts = new Map(); let pinch = 0;
pv.addEventListener('pointerdown', e => { pv.setPointerCapture(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]); });
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
