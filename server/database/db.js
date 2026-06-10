const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const DB_PATH = path.join(__dirname, 'data.db');
const JSON_PATH = path.join(__dirname, 'data.json');
let db;

function timestamp() {
  var d = new Date();
  var offset = d.getTime() + 8 * 3600000;
  return new Date(offset).toISOString().replace('T', ' ').split('.')[0];
}

// ---- Schema ----------------------------------------------------------------
var TABLES = {
  registrations: [
    'id INTEGER PRIMARY KEY AUTOINCREMENT',
    'name TEXT NOT NULL', 'gender TEXT', 'phone TEXT NOT NULL',
    'idcard TEXT', 'education TEXT', 'foundation TEXT',
    'course TEXT NOT NULL', 'expected_date TEXT', 'notes TEXT',
    "status TEXT NOT NULL DEFAULT 'pending'", 'created_at TEXT NOT NULL',
  ].join(', '),

  trials: [
    'id INTEGER PRIMARY KEY AUTOINCREMENT',
    'name TEXT NOT NULL', 'phone TEXT NOT NULL',
    'date TEXT', 'time TEXT', 'interest TEXT', 'notes TEXT',
    "status TEXT NOT NULL DEFAULT 'pending'", 'created_at TEXT NOT NULL',
  ].join(', '),

  contacts: [
    'id INTEGER PRIMARY KEY AUTOINCREMENT',
    'name TEXT NOT NULL', 'contact TEXT NOT NULL', 'message TEXT NOT NULL',
    "status TEXT NOT NULL DEFAULT 'unread'", 'created_at TEXT NOT NULL',
  ].join(', '),

  courses: [
    'id INTEGER PRIMARY KEY AUTOINCREMENT',
    'name TEXT NOT NULL', 'category TEXT NOT NULL',
    'duration TEXT NOT NULL', 'price TEXT NOT NULL', 'description TEXT',
  ].join(', '),
};

var COURSES_SEED = [
  { name: '多旋翼视距内驾驶员', category: 'multirotor', duration: '20天', price: '¥8,800', description: '零基础可学' },
  { name: '多旋翼超视距驾驶员', category: 'multirotor', duration: '25天', price: '¥12,800', description: '超视距飞行' },
  { name: '多旋翼教员执照', category: 'multirotor', duration: '30天', price: '¥18,800', description: '教学能力培训' },
  { name: '固定翼超视距驾驶员', category: 'fixedwing', duration: '25天', price: '¥14,800', description: '长航时飞行' },
  { name: '固定翼教员执照', category: 'fixedwing', duration: '35天', price: '¥22,800', description: '教学资质培训' },
  { name: '垂直起降固定翼超视距', category: 'vtol', duration: '28天', price: '¥16,800', description: '复合翼培训' },
  { name: '考前强化冲刺班', category: 'instructor', duration: '5天', price: '¥3,800', description: '考前强化' },
  { name: '多旋翼周末班', category: 'multirotor', duration: '8周', price: '¥9,800', description: '灵活培训' },
];

// ---- Migrate from data.json ------------------------------------------------
function migrate() {
  if (!fs.existsSync(JSON_PATH)) return;

  var raw;
  try { raw = fs.readFileSync(JSON_PATH, 'utf-8'); } catch (e) { return; }
  var oldData;
  try { oldData = JSON.parse(raw); } catch (e) { return; }

  var total = 0;

  function copyTable(name, cols) {
    var list = oldData[name];
    if (!list || list.length === 0) return;
    var ph = cols.map(function () { return '?'; }).join(', ');
    var stmt = db.prepare('INSERT OR IGNORE INTO ' + name + ' (' + cols.join(', ') + ') VALUES (' + ph + ')');
    var tx = db.transaction(function () {
      for (var i = 0; i < list.length; i++) {
        var row = list[i];
        var vals = cols.map(function (c) { return row[c] !== undefined ? row[c] : null; });
        stmt.run.apply(stmt, vals);
      }
    });
    tx();
    total += list.length;
  }

  copyTable('registrations', ['id', 'name', 'gender', 'phone', 'idcard', 'education', 'foundation', 'course', 'expected_date', 'notes', 'status', 'created_at']);
  copyTable('trials', ['id', 'name', 'phone', 'date', 'time', 'interest', 'notes', 'status', 'created_at']);
  copyTable('contacts', ['id', 'name', 'contact', 'message', 'status', 'created_at']);

  try {
    fs.renameSync(JSON_PATH, JSON_PATH + '.bak');
    console.log('  => Migrated ' + total + ' records from data.json (backed up as data.json.bak)');
  } catch (e) {
    console.log('  => Migrated ' + total + ' records from data.json');
  }
}

// ---- Init ----------------------------------------------------------------
function init() {
  db = new Database(DB_PATH);
  db.pragma('journal_mode = WAL');
  db.pragma('foreign_keys = ON');

  for (var name in TABLES) {
    db.exec('CREATE TABLE IF NOT EXISTS ' + name + ' (' + TABLES[name] + ')');
  }

  var count = db.prepare('SELECT COUNT(*) AS c FROM courses').get();
  if (count.c === 0) {
    var stmt = db.prepare('INSERT INTO courses (name, category, duration, price, description) VALUES (@name, @category, @duration, @price, @description)');
    var tx = db.transaction(function () {
      for (var i = 0; i < COURSES_SEED.length; i++) {
        stmt.run(COURSES_SEED[i]);
      }
    });
    tx();
  }

  migrate();
}

// ---- Collections API (same interface) ------------------------------------
var api = {
  insert: function (collection, record) {
    var cols = Object.keys(record);
    var vals = Object.values(record);
    var now = timestamp();
    var q = cols.map(function () { return '?'; }).join(', ');
    var stmt = db.prepare('INSERT INTO ' + collection + ' (' + cols.join(', ') + ', created_at) VALUES (' + q + ', ?)');
    var result = stmt.run.apply(stmt, vals.concat([now]));
    return { id: Number(result.lastInsertRowid), created_at: now };
  },

  findAll: function (collection) {
    return db.prepare('SELECT * FROM ' + collection + ' ORDER BY created_at DESC').all();
  },

  findById: function (collection, id) {
    return db.prepare('SELECT * FROM ' + collection + ' WHERE id = ?').get(Number(id));
  },

  update: function (collection, id, fields) {
    var cols = Object.keys(fields);
    if (cols.length === 0) return null;
    var vals = cols.map(function (c) { return fields[c]; });
    var stmt = db.prepare('UPDATE ' + collection + ' SET ' + cols.map(function (c) { return c + ' = ?'; }).join(', ') + ' WHERE id = ?');
    var result = stmt.run.apply(stmt, vals.concat([Number(id)]));
    if (result.changes === 0) return null;
    return this.findById(collection, id);
  },

  delete: function (collection, id) {
    return db.prepare('DELETE FROM ' + collection + ' WHERE id = ?').run(Number(id)).changes > 0;
  },

  count: function (collection, predicate) {
    if (!predicate) return db.prepare('SELECT COUNT(*) AS c FROM ' + collection).get().c;
    return this.findAll(collection).filter(predicate).length;
  },

  recent: function (collection, n) {
    if (n === undefined) n = 5;
    return db.prepare('SELECT * FROM ' + collection + ' ORDER BY created_at DESC LIMIT ?').all(n);
  },
};

init();
module.exports = api;
