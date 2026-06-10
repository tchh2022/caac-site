const crypto = require('crypto');
const db = require('../database/db');

const ADMIN_USER = process.env.ADMIN_USERNAME || 'admin';
const ADMIN_PASS = process.env.ADMIN_PASSWORD || 'caac2024';
const TOKEN_SECRET = process.env.TOKEN_SECRET || 'caac-admin-secret-2024';
const TOKEN_EXPIRY = 86400000; // 24h

function generateToken() {
  const payload = JSON.stringify({ user: ADMIN_USER, exp: Date.now() + TOKEN_EXPIRY });
  const sig = crypto.createHmac('sha256', TOKEN_SECRET).update(payload).digest('hex');
  return Buffer.from(payload + '.' + sig).toString('base64');
}

function verifyToken(tokenStr) {
  try {
    const raw = Buffer.from(tokenStr, 'base64').toString();
    const dot = raw.indexOf('.');
    if (dot === -1) return null;
    const payload = raw.substring(0, dot);
    const sig = raw.substring(dot + 1);
    const expected = crypto.createHmac('sha256', TOKEN_SECRET).update(payload).digest('hex');
    if (sig !== expected) return null;
    const data = JSON.parse(payload);
    if (data.exp < Date.now()) return null;
    return data;
  } catch { return null; }
}

function authenticate(req) {
  const header = req.headers.authorization || req.headers.Authorization;
  if (!header) return null;
  return verifyToken(header.replace(/^Bearer\s+/i, ''));
}

function adminRoutes(router) {
  // ---- Login ----
  router.post('/api/admin/login', (req, body) => {
    if (body.username === ADMIN_USER && body.password === ADMIN_PASS) {
      return { body: { success: true, token: generateToken() } };
    }
    return { status: 401, body: { success: false, message: '用户名或密码错误' } };
  });

  // ---- Verify token ----
  router.get('/api/admin/verify', (req) => {
    if (authenticate(req)) return { body: { success: true } };
    return { status: 401, body: { success: false, message: '未登录' } };
  });

  // ---- Stats ----
  router.get('/api/admin/stats', (req) => {
    if (!authenticate(req)) return { status: 401, body: { success: false, message: '未登录' } };
    return {
      body: {
        registrations: db.count('registrations'),
        pendingRegistrations: db.count('registrations', r => r.status === 'pending'),
        trials: db.count('trials'),
        unreadMessages: db.count('contacts', r => r.status === 'unread'),
        recentRegistrations: db.recent('registrations', 5),
        recentTrials: db.recent('trials', 5),
        recentMessages: db.recent('contacts', 5),
      }
    };
  });

  // ---- Delete ----
  router.delete('/api/admin/registrations/:id', (req) => {
    if (!authenticate(req)) return { status: 401, body: { success: false, message: '未登录' } };
    db.delete('registrations', req.params.id);
    return { body: { success: true } };
  });

  router.delete('/api/admin/trials/:id', (req) => {
    if (!authenticate(req)) return { status: 401, body: { success: false, message: '未登录' } };
    db.delete('trials', req.params.id);
    return { body: { success: true } };
  });

  router.delete('/api/admin/contacts/:id', (req) => {
    if (!authenticate(req)) return { status: 401, body: { success: false, message: '未登录' } };
    db.delete('contacts', req.params.id);
    return { body: { success: true } };
  });
}

module.exports = adminRoutes;
