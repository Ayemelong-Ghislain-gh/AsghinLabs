/* =====================================================================
   Keep-alive for free Supabase projects (Vercel Cron, see vercel.json)

   Supabase pauses free projects after about a week with no activity.
   Vercel calls this function once a day; it runs one tiny read query on
   each project, which counts as activity, so they never get paused.

   The keys below are the PUBLIC anon/publishable keys that each app
   already ships to every visitor's browser. Row Level Security still
   protects the data. Never put a service_role / secret key here.
   ===================================================================== */

const PROJECTS = [
  { name: 'StudentStay', url: 'https://mbjplutwsxtmdmmwdoxs.supabase.co', key: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ianBsdXR3c3h0bWRtbXdkb3hzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYzOTg2NDQsImV4cCI6MjEwMTk3NDY0NH0.KFpy5AgQ3j57tH8-HNn8jlCpoWzaZ6hHUZ0RIHr4wSQ', table: 'rooms' },
  { name: 'Ride Along', url: 'https://gkakwjfebfkcwofzbwsi.supabase.co', key: 'sb_publishable_JycYC4ZZgHa6VRyBcXaR2w_FKY5yO4o', table: 'notifications' },
];

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  const results = await Promise.all(PROJECTS.map(async (p) => {
    const headers = { apikey: p.key };
    if (p.key.startsWith('eyJ')) headers.Authorization = 'Bearer ' + p.key;
    try {
      const r = await fetch(`${p.url}/rest/v1/${p.table}?select=*&limit=1`, { headers });
      return { project: p.name, status: r.status };
    } catch (err) {
      return { project: p.name, error: String(err && err.message || err) };
    }
  }));
  console.log('keepalive', JSON.stringify(results));
  res.status(200).json({ ok: true, at: new Date().toISOString(), results });
};
