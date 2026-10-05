/* =====================================================================
   Lesson feedback API (Vercel serverless function)

   POST /api/feedback   → a student sends feedback from a lesson page
   GET  /api/feedback   → the teacher dashboard reads it
                          (needs the header  x-admin-key: <FEEDBACK_ADMIN_KEY>)

   Storage: Upstash Redis, connected in Vercel → Storage.
   Environment variables (Vercel → Settings → Environment Variables):
     KV_REST_API_URL + KV_REST_API_TOKEN      (added automatically by Vercel)
       or UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN
     FEEDBACK_ADMIN_KEY                       (your dashboard password)
   ===================================================================== */

const DB_URL = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const DB_TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
const ADMIN_KEY = process.env.FEEDBACK_ADMIN_KEY;
const LIST = 'lesson-feedback';
const MAX_KEEP = 5000;          // keep the newest 5 000 messages
const MAX_PER_HOUR = 15;        // per device/network, to stop spam

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

const text = (v, max) => String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, max);

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (!DB_URL || !DB_TOKEN) return res.status(503).json({ ok: false, error: 'not_configured' });

  try {
    if (req.method === 'POST') {
      let body = req.body || {};
      if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
      if (body.website) return res.status(200).json({ ok: true });          // hidden spam trap

      const entry = {
        lesson: text(body.lesson, 60).replace(/[^a-z0-9-]/gi, ''),
        understood: ['yes', 'partly', 'no'].includes(body.understood) ? body.understood : '',
        hard: text(body.hard, 600),
        question: text(body.question, 600),
        name: text(body.name, 40),
        level: text(body.level, 20),
        at: new Date().toISOString(),
      };
      if (!entry.lesson || (!entry.understood && !entry.hard && !entry.question)) {
        return res.status(400).json({ ok: false, error: 'empty' });
      }

      const ip = text((req.headers['x-forwarded-for'] || '').split(',')[0] || 'unknown', 60);
      const rateKey = 'fb-rate:' + ip;
      const count = await redis(['INCR', rateKey]);
      if (count === 1) await redis(['EXPIRE', rateKey, 3600]);
      if (count > MAX_PER_HOUR) return res.status(429).json({ ok: false, error: 'too_many' });

      await redis(['LPUSH', LIST, JSON.stringify(entry)]);
      await redis(['LTRIM', LIST, 0, MAX_KEEP - 1]);
      return res.status(200).json({ ok: true });
    }

    if (req.method === 'GET') {
      if (!ADMIN_KEY || req.headers['x-admin-key'] !== ADMIN_KEY) {
        return res.status(401).json({ ok: false, error: 'wrong_key' });
      }
      const raw = await redis(['LRANGE', LIST, 0, MAX_KEEP - 1]);
      const items = (raw || []).map(s => { try { return JSON.parse(s); } catch (e) { return null; } }).filter(Boolean);
      return res.status(200).json({ ok: true, items });
    }

    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ ok: false, error: 'method' });
  } catch (err) {
    console.error('feedback error', err);
    return res.status(500).json({ ok: false, error: 'server' });
  }
};
