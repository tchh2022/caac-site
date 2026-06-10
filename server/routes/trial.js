const db = require('../database/db');

function trialRoutes(router) {
  router.post('/api/trial', (req, body) => {
    const { name, phone, date, time, interest, notes } = body;
    if (!name || !phone) {
      return { status: 400, body: { success: false, message: '姓名和手机号为必填项' } };
    }
    db.insert('trials', { name, phone, date, time, interest, notes, status: 'pending' });
    return { body: { success: true, message: '体验课预约成功！我们会尽快与您确认安排。' } };
  });

  router.get('/api/trial', () => {
    return { body: db.findAll('trials') };
  });
}

module.exports = trialRoutes;
