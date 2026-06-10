const fs = require('fs');
const path = require('path');

const DB_PATH = path.join(__dirname, 'data.json');

// ---- Simple mutex for write safety ---------------------------------------
let writeQueue = Promise.resolve();

function withLock(fn) {
  writeQueue = writeQueue.then(fn, fn);
  return writeQueue;
}

// ---- Timestamp ------------------------------------------------------------
function timestamp() {
  const d = new Date();
  const offset = d.getTime() + 8 * 3600000;
  return new Date(offset).toISOString().replace('T', ' ').split('.')[0];
}

// ---- Atomic read / write --------------------------------------------------
function readDB() {
  try {
    const raw = fs.readFileSync(DB_PATH, 'utf-8');
    return JSON.parse(raw);
  } catch (e) {
    return null;
  }
}

function writeDB(data) {
  const tmp = DB_PATH + '.tmp.' + process.pid;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2), 'utf-8');
  fs.renameSync(tmp, DB_PATH);
}

// ---- Collection helpers ---------------------------------------------------
function getCollection(collection) {
  const data = readDB();
  return data ? data[collection] : null;
}

function saveCollection(collection, list) {
  return withLock(function () {
    const data = readDB() || { registrations: [], trials: [], contacts: [], courses: [] };
    data[collection] = list;
    writeDB(data);
  });
}

// ---- Init: seed defaults --------------------------------------------------
const DEFAULT = {
  registrations: [],
  trials: [],
  contacts: [],
  courses: [
    { name: '\u591A\u65CB\u7FFC\u89C6\u8DDD\u5185\u9A7E\u9A76\u5458', category: 'multirotor', duration: '20\u5929', price: '\u00A58,800', description: '\u96F6\u57FA\u7840\u53EF\u5B66' },
    { name: '\u591A\u65CB\u7FFC\u8D85\u89C6\u8DDD\u9A7E\u9A76\u5458', category: 'multirotor', duration: '25\u5929', price: '\u00A512,800', description: '\u8D85\u89C6\u8DDD\u98DE\u884C' },
    { name: '\u591A\u65CB\u7FFC\u6559\u5458\u6267\u7167', category: 'multirotor', duration: '30\u5929', price: '\u00A518,800', description: '\u6559\u5B66\u80FD\u529B\u57F9\u8BAD' },
    { name: '\u56FA\u5B9A\u7FFC\u8D85\u89C6\u8DDD\u9A7E\u9A76\u5458', category: 'fixedwing', duration: '25\u5929', price: '\u00A514,800', description: '\u957F\u822A\u65F6\u98DE\u884C' },
    { name: '\u56FA\u5B9A\u7FFC\u6559\u5458\u6267\u7167', category: 'fixedwing', duration: '35\u5929', price: '\u00A522,800', description: '\u6559\u5B66\u8D44\u8D28\u57F9\u8BAD' },
    { name: '\u5782\u76F4\u8D77\u964D\u56FA\u5B9A\u7FFC\u8D85\u89C6\u8DDD', category: 'vtol', duration: '28\u5929', price: '\u00A516,800', description: '\u590D\u5408\u7FFC\u57F9\u8BAD' },
    { name: '\u8003\u524D\u5F3A\u5316\u51B2\u523A\u73ED', category: 'instructor', duration: '5\u5929', price: '\u00A53,800', description: '\u8003\u524D\u5F3A\u5316' },
    { name: '\u591A\u65CB\u7FFC\u5468\u672B\u73ED', category: 'multirotor', duration: '8\u5468', price: '\u00A59,800', description: '\u7075\u6D3B\u57F9\u8BAD' },
  ]
};

(function init() {
  if (!fs.existsSync(DB_PATH)) {
    writeDB(DEFAULT);
  }
})();

// ---- Public API ------------------------------------------------------------
const api = {
  insert(collection, record) {
    const list = getCollection(collection) || [];
    const maxId = list.reduce(function (m, r) { return Math.max(m, r.id || 0); }, 0);
    const now = timestamp();
    const newRecord = { id: maxId + 1, ...record, created_at: now };
    list.unshift(newRecord);
    saveCollection(collection, list);
    return newRecord;
  },

  findAll(collection) {
    return getCollection(collection) || [];
  },

  findById(collection, id) {
    const list = getCollection(collection);
    if (!list) return null;
    return list.find(function (r) { return r.id === Number(id); }) || null;
  },

  update(collection, id, fields) {
    const list = getCollection(collection);
    if (!list) return null;
    const idx = list.findIndex(function (r) { return r.id === Number(id); });
    if (idx === -1) return null;
    Object.assign(list[idx], fields);
    saveCollection(collection, list);
    return list[idx];
  },

  delete(collection, id) {
    const list = getCollection(collection);
    if (!list) return false;
    const idx = list.findIndex(function (r) { return r.id === Number(id); });
    if (idx === -1) return false;
    list.splice(idx, 1);
    saveCollection(collection, list);
    return true;
  },

  count(collection, predicate) {
    const list = getCollection(collection);
    if (!list) return 0;
    if (!predicate) return list.length;
    return list.filter(predicate).length;
  },

  recent(collection, n) {
    if (n === undefined) n = 5;
    const list = getCollection(collection);
    if (!list) return [];
    return list.slice(0, n);
  },
};

module.exports = api;
