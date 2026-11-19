// Vercel serverless function: GET /api/quote
// Calls your LICENSED market-data vendor, reshapes the reply into the format
// index.html expects, and lets Vercel's edge cache it for 60 seconds so you
// make about one vendor call per minute no matter how many visitors you have.
//
// Set these in Vercel → Project → Settings → Environment Variables:
//   VENDOR_QUOTE_URL   full URL of the vendor's GIFT Nifty quote endpoint
//   VENDOR_API_KEY     your vendor key (never put it in index.html)
//   VENDOR_KEY_HEADER  header name the vendor wants, default "Authorization"
//   NIFTY_SPOT_URL     (optional) vendor endpoint for the Nifty 50 index close
//   CUES_URL           (optional) vendor endpoint for global indices / FX / commodities
//   DELAY_MINUTES      delay your licence requires, default 15
//
// If nothing is configured the function answers 503 and the page shows
// labelled sample data instead.

const pick = (o, keys, dflt) => {
  for (const k of keys) {
    const v = k.split('.').reduce((a, p) => (a == null ? a : a[p]), o);
    if (v != null && v !== '') return v;
  }
  return dflt;
};
const num = v => (v == null ? undefined : Number(v));

async function getJSON(url) {
  const header = process.env.VENDOR_KEY_HEADER || 'Authorization';
  const key = process.env.VENDOR_API_KEY || '';
  const r = await fetch(url, { headers: key ? { [header]: header === 'Authorization' ? `Bearer ${key}` : key } : {} });
  if (!r.ok) throw new Error(`Vendor ${r.status}`);
  return r.json();
}

// Adjust the key lists below to match your vendor's field names.
function mapQuote(q) {
  const series = pick(q, ['intraday', 'candles', 'data.candles', 'bars'], []);
  return {
    symbol: 'GIFTNIFTY',
    last: num(pick(q, ['last', 'ltp', 'lastPrice', 'close', 'data.ltp'])),
    prevClose: num(pick(q, ['prevClose', 'previousClose', 'prev_close', 'pc', 'data.prevClose'])),
    high: num(pick(q, ['high', 'dayHigh', 'h', 'data.high'])),
    low: num(pick(q, ['low', 'dayLow', 'l', 'data.low'])),
    asOf: pick(q, ['asOf', 'timestamp', 'time', 'lastTradeTime', 'data.time'], new Date().toISOString()),
    intraday: series.map(c => (Array.isArray(c) ? [c[0], Number(c[4] ?? c[1])] : [c.time || c.t, Number(c.close ?? c.c)]))
  };
}

module.exports = async (req, res) => {
  const url = process.env.VENDOR_QUOTE_URL;
  if (!url) {
    res.status(503).json({ error: 'Data vendor not configured yet' });
    return;
  }
  try {
    const [q, spot, cues] = await Promise.all([
      getJSON(url),
      process.env.NIFTY_SPOT_URL ? getJSON(process.env.NIFTY_SPOT_URL) : null,
      process.env.CUES_URL ? getJSON(process.env.CUES_URL) : null
    ]);
    const out = mapQuote(q);
    out.delayMinutes = Number(process.env.DELAY_MINUTES || 15);
    out.niftySpotClose = num(spot ? pick(spot, ['close', 'prevClose', 'last', 'ltp']) : pick(q, ['niftySpotClose'])) ?? out.prevClose;
    out.cues = cues ? pick(cues, ['cues', 'data', 'items'], []).map(c => ({ name: c.name, last: Number(c.last ?? c.ltp), chg: Number(c.chg ?? c.change) })) : [];
    out.history = pick(q, ['history'], []);
    if (out.high == null && out.intraday.length) out.high = Math.max(...out.intraday.map(p => p[1]));
    if (out.low == null && out.intraday.length) out.low = Math.min(...out.intraday.map(p => p[1]));
    if (!Number.isFinite(out.last) || !Number.isFinite(out.prevClose)) throw new Error('Vendor reply missing price fields');
    res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=120');
    res.status(200).json(out);
  } catch (e) {
    res.setHeader('Cache-Control', 's-maxage=15');
    res.status(502).json({ error: String(e.message || e) });
  }
};
