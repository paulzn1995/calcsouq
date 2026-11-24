// CalcSouq QR code encoder: byte, numeric and alphanumeric modes, versions 1-40, error-correction levels L/M/Q/H, automatic mask choice.
const QR = (() => {
  const ECC = { L: [7,10,15,20,26,18,20,24,30,18,20,24,26,30,22,24,28,30,28,28,28,28,30,30,26,28,30,30,30,30,30,30,30,30,30,30,30,30,30,30],
    M: [10,16,26,18,24,16,18,22,22,26,30,22,22,24,24,28,28,26,26,26,26,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28],
    Q: [13,22,18,26,18,24,18,22,20,24,28,26,24,20,30,24,28,28,26,30,28,30,30,30,30,28,30,30,30,30,30,30,30,30,30,30,30,30,30,30],
    H: [17,28,22,16,22,28,26,26,24,28,24,28,22,24,24,30,28,28,26,28,30,24,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30] };
  const BLK = { L: [1,1,1,1,1,2,2,2,2,4,4,4,4,4,6,6,6,6,7,8,8,9,9,10,12,12,12,13,14,15,16,17,18,19,19,20,21,22,24,25],
    M: [1,1,1,2,2,4,4,4,5,5,5,8,9,9,10,10,11,13,14,16,17,17,18,20,21,23,25,26,28,29,31,33,35,37,38,40,43,45,47,49],
    Q: [1,1,2,2,4,4,6,6,8,8,8,10,12,16,12,17,16,18,21,20,23,23,25,27,29,34,34,35,38,40,43,45,48,51,53,56,59,62,65,68],
    H: [1,1,2,4,4,4,5,6,8,8,11,11,16,16,18,16,19,21,25,25,25,34,30,32,35,37,40,42,45,48,51,54,57,60,63,66,70,74,77,81] };
  const FMT = { L: 1, M: 0, Q: 3, H: 2 }, ALNUM = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:';
  const raw = v => { let r = (16 * v + 128) * v + 64; if (v >= 2) { const n = Math.floor(v / 7) + 2; r -= (25 * n - 10) * n - 55; if (v >= 7) r -= 36; } return r; };
  const dataCw = (v, e) => Math.floor(raw(v) / 8) - ECC[e][v - 1] * BLK[e][v - 1];
  const mul = (x, y) => { let z = 0; for (let i = 7; i >= 0; i--) { z = (z << 1) ^ ((z >>> 7) * 0x11d); z ^= ((y >>> i) & 1) * x; } return z & 255; };
  function rsDiv(n) { const r = new Array(n).fill(0); r[n - 1] = 1; let root = 1;
    for (let i = 0; i < n; i++) { for (let j = 0; j < n; j++) { r[j] = mul(r[j], root); if (j + 1 < n) r[j] ^= r[j + 1]; } root = mul(root, 2); } return r; }
  function rsRem(data, div) { const r = new Array(div.length).fill(0);
    for (const b of data) { const f = b ^ r.shift(); r.push(0); div.forEach((c, i) => { r[i] ^= mul(c, f); }); } return r; }
  function mode(s) { return /^\d*$/.test(s) ? 'num' : [...s].every(c => ALNUM.includes(c)) ? 'alnum' : 'byte'; }
  function ccBits(m, v) { const k = v < 10 ? 0 : v < 27 ? 1 : 2; return { num: [10, 12, 14], alnum: [9, 11, 13], byte: [8, 16, 16] }[m][k]; }
  function segBits(s) { // returns {m, n, bits[]}
    const m = mode(s), bits = [], put = (val, len) => { for (let i = len - 1; i >= 0; i--) bits.push((val >>> i) & 1); };
    let n;
    if (m === 'num') { n = s.length; for (let i = 0; i < s.length; i += 3) { const g = s.substr(i, 3); put(+g, g.length * 3 + 1); } }
    else if (m === 'alnum') { n = s.length; for (let i = 0; i + 1 < s.length; i += 2) put(ALNUM.indexOf(s[i]) * 45 + ALNUM.indexOf(s[i + 1]), 11); if (s.length % 2) put(ALNUM.indexOf(s[s.length - 1]), 6); }
    else { const b = new TextEncoder().encode(s); n = b.length; b.forEach(x => put(x, 8)); }
    return { m, n, bits };
  }
  // max characters at version 40 for each mode
  function limit(m, e) { const cap = dataCw(40, e) * 8 - 4 - ccBits(m, 40); return m === 'num' ? Math.floor(cap / 10) * 3 + (cap % 10 >= 7 ? 2 : cap % 10 >= 4 ? 1 : 0) : m === 'alnum' ? Math.floor(cap / 11) * 2 + (cap % 11 >= 6 ? 1 : 0) : Math.floor(cap / 8); }
  function encode(text, e, forceMask) {
    const sg = segBits(text); let v = 1, need;
    for (; v <= 40; v++) { need = 4 + ccBits(sg.m, v) + sg.bits.length; if (need <= dataCw(v, e) * 8) break; }
    if (v > 40) return { error: 'too-long', mode: sg.m, n: sg.n, max: limit(sg.m, e) };
    const cap = dataCw(v, e) * 8, bits = [], put = (val, len) => { for (let i = len - 1; i >= 0; i--) bits.push((val >>> i) & 1); };
    put({ num: 1, alnum: 2, byte: 4 }[sg.m], 4); put(sg.n, ccBits(sg.m, v)); bits.push(...sg.bits);
    put(0, Math.min(4, cap - bits.length)); put(0, (8 - bits.length % 8) % 8);
    for (let p = 0xec; bits.length < cap; p ^= 0xec ^ 0x11) put(p, 8);
    const data = []; for (let i = 0; i < bits.length; i += 8) { let b = 0; for (let j = 0; j < 8; j++) b = (b << 1) | bits[i + j]; data.push(b); }
    // blocks and interleave
    const nb = BLK[e][v - 1], el = ECC[e][v - 1], rc = Math.floor(raw(v) / 8), ns = nb - rc % nb, sl = Math.floor(rc / nb), div = rsDiv(el), blocks = [];
    for (let i = 0, k = 0; i < nb; i++) { const dl = sl - el + (i < ns ? 0 : 1), d = data.slice(k, k + dl); k += dl; const ec = rsRem(d, div); if (i < ns) d.push(0); blocks.push(d.concat(ec)); }
    const cw = []; for (let i = 0; i < blocks[0].length; i++) blocks.forEach((b, j) => { if (i !== sl - el || j >= ns) cw.push(b[i]); });
    // matrix
    const size = v * 4 + 17, M = [], fn = [];
    for (let y = 0; y < size; y++) { M.push(new Array(size).fill(false)); fn.push(new Array(size).fill(false)); }
    const set = (x, y, d) => { M[y][x] = d; fn[y][x] = true; };
    for (let i = 0; i < size; i++) { set(6, i, i % 2 === 0); set(i, 6, i % 2 === 0); }
    [[3, 3], [size - 4, 3], [3, size - 4]].forEach(([cx, cy]) => { for (let dy = -4; dy <= 4; dy++) for (let dx = -4; dx <= 4; dx++) { const d = Math.max(Math.abs(dx), Math.abs(dy)), x = cx + dx, y = cy + dy; if (x >= 0 && x < size && y >= 0 && y < size) set(x, y, d !== 2 && d !== 4); } });
    if (v > 1) { const n = Math.floor(v / 7) + 2, step = v === 32 ? 26 : Math.ceil((v * 4 + 4) / (n * 2 - 2)) * 2, pos = [6];
      for (let p = size - 7; pos.length < n; p -= step) pos.splice(1, 0, p);
      pos.forEach((ax, i) => pos.forEach((ay, j) => { if ((i === 0 && j === 0) || (i === 0 && j === n - 1) || (i === n - 1 && j === 0)) return; for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) set(ax + dx, ay + dy, Math.max(Math.abs(dx), Math.abs(dy)) !== 1); })); }
    const fmt = m => { const d = FMT[e] << 3 | m; let r = d; for (let i = 0; i < 10; i++) r = (r << 1) ^ ((r >>> 9) * 0x537); const b = (d << 10 | r) ^ 0x5412, g = i => ((b >>> i) & 1) === 1;
      for (let i = 0; i <= 5; i++) set(8, i, g(i)); set(8, 7, g(6)); set(8, 8, g(7)); set(7, 8, g(8)); for (let i = 9; i < 15; i++) set(14 - i, 8, g(i));
      for (let i = 0; i < 8; i++) set(size - 1 - i, 8, g(i)); for (let i = 8; i < 15; i++) set(8, size - 15 + i, g(i)); set(8, size - 8, true); };
    fmt(0);
    if (v >= 7) { let r = v; for (let i = 0; i < 12; i++) r = (r << 1) ^ ((r >>> 11) * 0x1f25); const b = v << 12 | r;
      for (let i = 0; i < 18; i++) { const d = ((b >>> i) & 1) === 1, a = size - 11 + i % 3, c = Math.floor(i / 3); set(a, c, d); set(c, a, d); } }
    let i = 0; for (let right = size - 1; right >= 1; right -= 2) { if (right === 6) right = 5;
      for (let vt = 0; vt < size; vt++) for (let j = 0; j < 2; j++) { const x = right - j, up = ((right + 1) & 2) === 0, y = up ? size - 1 - vt : vt;
        if (!fn[y][x] && i < cw.length * 8) { M[y][x] = ((cw[i >>> 3] >>> (7 - (i & 7))) & 1) === 1; i++; } } }
    const MASK = [(x, y) => (x + y) % 2 === 0, (x, y) => y % 2 === 0, (x, y) => x % 3 === 0, (x, y) => (x + y) % 3 === 0, (x, y) => (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0,
      (x, y) => x * y % 2 + x * y % 3 === 0, (x, y) => (x * y % 2 + x * y % 3) % 2 === 0, (x, y) => ((x + y) % 2 + x * y % 3) % 2 === 0];
    const apply = m => { for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) if (!fn[y][x] && MASK[m](x, y)) M[y][x] = !M[y][x]; };
    const penalty = () => { let s = 0, dark = 0;
      const line = get => { let run = 1, prev = get(0); const arr = [];
        for (let k = 0; k < size; k++) arr.push(get(k));
        for (let k = 1; k < size; k++) { if (arr[k] === prev) { run++; if (run === 5) s += 3; else if (run > 5) s++; } else { run = 1; prev = arr[k]; } }
        const pad = [false, false, false, false, ...arr, false, false, false, false];
        for (let k = 0; k + 11 <= pad.length; k++) { const w = pad.slice(k, k + 11).map(b => b ? 1 : 0).join('');
          if (w === '10111010000' || w === '00001011101') s += 40; } };
      for (let y = 0; y < size; y++) line(k => M[y][k]);
      for (let x = 0; x < size; x++) line(k => M[k][x]);
      for (let y = 0; y < size - 1; y++) for (let x = 0; x < size - 1; x++) { const c = M[y][x]; if (c === M[y][x + 1] && c === M[y + 1][x] && c === M[y + 1][x + 1]) s += 3; }
      for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) if (M[y][x]) dark++;
      const t = size * size; s += (Math.ceil(Math.abs(dark * 20 - t * 10) / t) - 1) * 10; return s; };
    let mask = forceMask;
    if (mask == null) { let best = Infinity; for (let m = 0; m < 8; m++) { apply(m); fmt(m); const p = penalty(); if (p < best) { best = p; mask = m; } apply(m); } }
    apply(mask); fmt(mask);
    return { size, M, version: v, mode: sg.m, n: sg.n, mask, max: limit(sg.m, e) };
  }
  return { encode, limit, dataCw };
})();
