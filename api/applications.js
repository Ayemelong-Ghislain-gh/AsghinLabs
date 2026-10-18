/* =====================================================================
   Team applications API (Vercel serverless function)

   POST  /api/applications  → the /join form saves an application
                              (it also opens WhatsApp, so you get both)
   GET   /api/applications  → the admin dashboard lists them
   PATCH /api/applications  → the dashboard changes an application's status
                              (GET and PATCH need the header
                               x-admin-key: <FEEDBACK_ADMIN_KEY>)

   Uses the same Upstash Redis database and password as /api/feedback,
   so nothing new has to be set up in Vercel.
   ===================================================================== */

const DB_URL = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const DB_TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
const ADMIN_KEY = process.env.FEEDBACK_ADMIN_KEY;
const HASH = 'team-applications';          // id → application JSON
const MAX_PER_HOUR = 5;                    // per device/network, to stop spam
const ROLES = ['Developer & client getter', 'Content creator & brand seller', 'Academy tutor & ambassador'];
const STATUSES = ['new', 'shortlisted', 'called', 'trial', 'rejected'];

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

const line = (v, max) => String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, max);
const para = (v, max) => String(v == null ? '' : v).replace(/\r/g, '').replace(/\n{3,}/g, '\n\n').trim().slice(0, max);

function readBody(req) {
  let body = req.body || {};
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  return body;
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (!DB_URL || !DB_TOKEN) return res.status(503).json({ ok: false, error: 'not_configured' });

  try {
    if (req.method === 'POST') {
      const body = readBody(req);
      if (body.website) return res.status(200).json({ ok: true });          // hidden spam trap

      const app = {
        id: Date.now().toString(36) + Math.random().toString(36).slice(2, 7),
        role: ROLES.includes(body.role) ? body.role : '',
        name: line(body.name, 80),
        city: line(body.city, 60),
        phone: line(body.phone, 30),
        work: line(body.work, 300),
        pitch: para(body.pitch, 1200),
        hours: line(body.hours, 30),
        why: para(body.why, 1200),
        status: 'new',
        note: '',
        at: new Date().toISOString(),
      };
      if (!app.role || !app.name || !app.phone || !app.pitch) {
        return res.status(400).json({ ok: false, error: 'missing' });
      }

      const ip = line((req.headers['x-forwarded-for'] || '').split(',')[0] || 'unknown', 60);
      const rateKey = 'app-rate:' + ip;
      const count = await redis(['INCR', rateKey]);
      if (count === 1) await redis(['EXPIRE', rateKey, 3600]);
      if (count > MAX_PER_HOUR) return res.status(429).json({ ok: false, error: 'too_many' });

      await redis(['HSET', HASH, app.id, JSON.stringify(app)]);
      return res.status(200).json({ ok: true });
    }

    if (!ADMIN_KEY || req.headers['x-admin-key'] !== ADMIN_KEY) {
      return res.status(401).json({ ok: false, error: 'wrong_key' });
    }

    if (req.method === 'GET') {
      const raw = await redis(['HVALS', HASH]) || [];
      const items = raw.map(s => { try { return JSON.parse(s); } catch (e) { return null; } })
        .filter(Boolean).sort((a, b) => (a.at < b.at ? 1 : -1));
      return res.status(200).json({ ok: true, items });
    }

    if (req.method === 'PATCH') {
      const body = readBody(req);
      const id = line(body.id, 40);
      const current = id && await redis(['HGET', HASH, id]);
      if (!current) return res.status(404).json({ ok: false, error: 'not_found' });
      const app = JSON.parse(current);
      if (body.status !== undefined) {
        if (!STATUSES.includes(body.status)) return res.status(400).json({ ok: false, error: 'status' });
        app.status = body.status;
      }
      if (body.note !== undefined) app.note = para(body.note, 600);
      await redis(['HSET', HASH, id, JSON.stringify(app)]);
      return res.status(200).json({ ok: true, item: app });
    }

    res.setHeader('Allow', 'GET, POST, PATCH');
    return res.status(405).json({ ok: false, error: 'method' });
  } catch (err) {
    console.error('applications error', err);
    return res.status(500).json({ ok: false, error: 'server' });
  }
};
