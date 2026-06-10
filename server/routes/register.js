const db = require('../database/db');

function registerRoutes(router) {
  router.post('/api/register', (req, body) => {
    const { name, gender, phone, idcard, education, foundation, course, expected_date, notes, province, city, district } = body;
    if (!name || !phone || !course) {
      return { status: 400, body: { success: false, message: '姓名、手机号和课程为必填项' } };
    }
    const { province, city, district } = body;
    db.insert('registrations', { name, gender, phone, idcard, education, foundation, course, expected_date, notes, province, city, district, status: 'pending' });
    return { body: { success: true, message: '报名提交成功！' } };
  });

  router.get('/api/register', () => {
    return { body: db.findAll('registrations') };
  });

  router.put('/api/register/:id', (req, body) => {
    db.update('registrations', req.params.id, { status: body.status || 'contacted' });
    return { body: { success: true } };
  });
}

module.exports = registerRoutes;
