/* =====================================================================
   Academy shop payments with Fapshi (MTN MoMo + Orange Money)
   Vercel serverless function.

   POST /api/pay                → creates an order and a Fapshi payment link
                                  body: { items: {id: qty}, name, phone, town,
                                          delivery, note, lang }
   GET  /api/pay?order=<id>     → checks the payment with Fapshi and returns
                                  the order status (pending / paid / failed)
   POST /api/pay?webhook=1      → Fapshi webhook (set it in the Fapshi
                                  dashboard). The status is always re-checked
                                  with Fapshi, the webhook body is never trusted.

   Security:
   - Prices are read on the server from academy-data.js, never from the browser.
   - A payment only counts when Fapshi's own payment-status says SUCCESSFUL.
   - The Fapshi key lives only in Vercel environment variables.

   Environment variables (Vercel → Settings → Environment Variables):
     FAPSHI_API_USER, FAPSHI_API_KEY
       Sandbox keys start with FAK_TEST_ and use https://sandbox.fapshi.com,
       live keys use https://live.fapshi.com (picked automatically).
     KV_REST_API_URL + KV_REST_API_TOKEN (same Upstash database as /api/feedback)
   ===================================================================== */

const vm = require('vm');

const SITE = 'https://www.asghinlabs.com';
const DB_URL = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const DB_TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
const F_USER = process.env.FAPSHI_API_USER;
const F_KEY = process.env.FAPSHI_API_KEY;
const F_BASE = process.env.FAPSHI_BASE_URL ||
  (String(F_KEY || '').startsWith('FAK_TEST') ? 'https://sandbox.fapshi.com' : 'https://live.fapshi.com');
const HASH = 'academy-orders';           // order id → order JSON
const MAX_PER_HOUR = 10;                 // new orders per network, to stop abuse

async function redis(command) {
  const r = await fetch(DB_URL, {
    method: 'POST',
    headers: { Authorization: `Bearer ${DB_TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(command),
  });
  const data = await r.json();
  if (data.error) throw new Error(data.error);
  return data.result;
}

async function fapshi(path, method, body) {
  const r = await fetch(F_BASE + path, {
    method,
    headers: { apiuser: F_USER, apikey: F_KEY, 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  let data = {};
  try { data = await r.json(); } catch (e) { /* empty body */ }
  if (!r.ok) {
    const err = new Error('fapshi ' + r.status + ' ' + (data && data.message || ''));
    err.status = r.status;
    throw err;
  }
  return data;
}

// Read the workbook list (with prices) from the public data file the shop uses.
const bookCache = {};
async function loadBooks(lang) {
  const file = lang === 'fr' ? 'academy-data-fr.js' : 'academy-data.js';
  const now = Date.now();
  if (bookCache[file] && now - bookCache[file].at < 5 * 60 * 1000) return bookCache[file].books;
  const code = await fetch(`${SITE}/${file}`, { cache: 'no-store' }).then(r => r.text());
  const ctx = {};
  vm.createContext(ctx);
  const books = vm.runInContext(code + '\n;ACADEMY_WORKBOOKS', ctx, { timeout: 1000 });
  const list = Array.from(books || []).map(b => ({ id: b.id, title: b.title, subject: b.subject, price: +b.price || 0 }));
  bookCache[file] = { at: now, books: list };
  return list;
}

const line = (v, max) => String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, max);

function readBody(req) {
  let body = req.body || {};
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  return body;
}

// Cameroon mobile number → 9 digits starting with 6, or '' if invalid.
function cmPhone(v) {
  let d = String(v || '').replace(/\D/g, '');
  if (d.startsWith('00237')) d = d.slice(5);
  else if (d.startsWith('237') && d.length === 12) d = d.slice(3);
  return /^6\d{8}$/.test(d) ? d : '';
}

// Public view of an order (no phone number, no note).
const publicOrder = (o) => ({
  id: o.id, status: o.status, total: o.total, lang: o.lang,
  name: o.name, delivery: o.delivery, town: o.town,
  items: o.items.map(i => ({ title: i.title, subject: i.subject, qty: i.qty, price: i.price })),
});

// Ask Fapshi for the real status and update the stored order.
async function refreshStatus(order) {
  if (order.status === 'paid' || !order.transId) return order;
  const st = await fapshi(`/payment-status/${encodeURIComponent(order.transId)}`, 'GET');
  const s = String(st.status || '').toUpperCase();
  let next = order.status;
  if (s === 'SUCCESSFUL' && Number(st.amount) >= order.total) next = 'paid';
  else if (s === 'FAILED' || s === 'EXPIRED') next = 'failed';
  else next = 'pending';
  if (next !== order.status) {
    order.status = next;
    if (next === 'paid') order.paidAt = new Date().toISOString();
    await redis(['HSET', HASH, order.id, JSON.stringify(order)]);
  }
  return order;
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (!DB_URL || !DB_TOKEN || !F_USER || !F_KEY) {
    return res.status(503).json({ ok: false, error: 'not_configured' });
  }

  try {
    // ---------- Fapshi webhook ----------
    if (req.method === 'POST' && req.query && req.query.webhook) {
      const body = readBody(req);
      const id = line(body.externalId, 60);
      const current = id && await redis(['HGET', HASH, id]);
      if (current) {
        const order = JSON.parse(current);
        if (!order.transId && body.transId) order.transId = line(body.transId, 60);
        await refreshStatus(order);
      }
      return res.status(200).json({ ok: true });
    }

    // ---------- Create an order + payment link ----------
    if (req.method === 'POST') {
      const body = readBody(req);
      const lang = body.lang === 'fr' ? 'fr' : 'en';
      const name = line(body.name, 80);
      const phone = cmPhone(body.phone);
      if (!name || !phone) return res.status(400).json({ ok: false, error: 'contact' });

      const books = await loadBooks(lang);
      const byId = Object.fromEntries(books.map(b => [b.id, b]));
      const wanted = body.items && typeof body.items === 'object' ? body.items : {};
      const items = [];
      for (const [id, qRaw] of Object.entries(wanted).slice(0, 40)) {
        const b = byId[id];
        const qty = Math.floor(Number(qRaw));
        if (!b || !(qty >= 1 && qty <= 50)) return res.status(400).json({ ok: false, error: 'items' });
        if (!b.price) return res.status(400).json({ ok: false, error: 'unpriced' });
        items.push({ id, title: b.title, subject: b.subject, qty, price: b.price });
      }
      const total = items.reduce((a, i) => a + i.price * i.qty, 0);
      if (!items.length || total < 100) return res.status(400).json({ ok: false, error: 'items' });

      const ip = line((req.headers['x-forwarded-for'] || '').split(',')[0] || 'unknown', 60);
      const rateKey = 'pay-rate:' + ip;
      const count = await redis(['INCR', rateKey]);
      if (count === 1) await redis(['EXPIRE', rateKey, 3600]);
      if (count > MAX_PER_HOUR) return res.status(429).json({ ok: false, error: 'too_many' });

      const id = 'AL' + Date.now().toString(36).toUpperCase() + Math.random().toString(36).slice(2, 6).toUpperCase();
      const page = lang === 'fr' ? '/academie' : '/academy';
      const pay = await fapshi('/initiate-pay', 'POST', {
        amount: total,
        redirectUrl: `${SITE}${page}?order=${id}`,
        externalId: id,
        message: `AsghinLabs Academy ${id}`.slice(0, 100),
      });
      if (!pay.link || !pay.transId) throw new Error('fapshi: no link');

      const order = {
        id, lang, items, total, name, phone,
        town: line(body.town, 80),
        delivery: body.delivery === 'Pickup' ? 'Pickup' : 'Delivery',
        note: line(body.note, 300),
        transId: String(pay.transId),
        status: 'pending',
        at: new Date().toISOString(),
      };
      await redis(['HSET', HASH, id, JSON.stringify(order)]);
      return res.status(200).json({ ok: true, order: id, link: pay.link });
    }

    // ---------- Check an order after payment ----------
    if (req.method === 'GET') {
      const id = line(req.query && req.query.order, 40);
      const current = id && await redis(['HGET', HASH, id]);
      if (!current) return res.status(404).json({ ok: false, error: 'not_found' });
      const order = await refreshStatus(JSON.parse(current));
      return res.status(200).json({ ok: true, order: publicOrder(order) });
    }

    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ ok: false, error: 'method' });
  } catch (err) {
    console.error('pay error', err);
    return res.status(502).json({ ok: false, error: 'payment_provider' });
  }
};
