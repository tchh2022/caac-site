const db = require('../database/db');

function contactRoutes(router) {
  router.post('/api/contact', (req, body) => {
    const { name, contact, message, province, city, district } = body;
    if (!name || !contact || !message) {
      return { status: 400, body: { success: false, message: '请填写完整信息' } };
    }
    db.insert('contacts', { name, contact, message, province, city, district, status: 'unread' });
    return { body: { success: true, message: '留言提交成功！我们会尽快回复。' } };
  });

  router.get('/api/contact', () => {
    return { body: db.findAll('contacts') };
  });

  router.put('/api/contact/:id', (req) => {
    db.update('contacts', req.params.id, { status: 'read' });
    return { body: { success: true } };
  });
}

module.exports = contactRoutes;
