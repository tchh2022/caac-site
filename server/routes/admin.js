const db = require('../database/db');

function adminRoutes(router) {
  router.get('/api/admin/stats', () => {
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

  router.delete('/api/admin/registrations/:id', (req) => {
    db.delete('registrations', req.params.id);
    return { body: { success: true } };
  });

  router.delete('/api/admin/trials/:id', (req) => {
    db.delete('trials', req.params.id);
    return { body: { success: true } };
  });

  router.delete('/api/admin/contacts/:id', (req) => {
    db.delete('contacts', req.params.id);
    return { body: { success: true } };
  });
}

module.exports = adminRoutes;
