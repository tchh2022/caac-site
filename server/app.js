const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3001;
const ROOT = path.join(__dirname, '..');

// ---- Simple URL router ----
class Router {
  constructor() {
    this.routes = { GET: [], POST: [], PUT: [], DELETE: [] };
  }

  get(pattern, handler) { this.routes.GET.push({ pattern, handler }); return this; }
  post(pattern, handler) { this.routes.POST.push({ pattern, handler }); return this; }
  put(pattern, handler) { this.routes.PUT.push({ pattern, handler }); return this; }
  delete(pattern, handler) { this.routes.DELETE.push({ pattern, handler }); return this; }

  resolve(method, url) {
    const routes = this.routes[method];
    if (!routes) return null;

    for (const { pattern, handler } of routes) {
      const patternParts = pattern.split('/');
      const urlParts = url.split('/');

      if (patternParts.length !== urlParts.length) continue;

      const params = {};
      let match = true;
      for (let i = 0; i < patternParts.length; i++) {
        if (patternParts[i].startsWith(':')) {
          params[patternParts[i].slice(1)] = urlParts[i];
        } else if (patternParts[i] !== urlParts[i]) {
          match = false;
          break;
        }
      }

      if (match) return { handler, params };
    }
    return null;
  }
}

const router = new Router();

// ---- MIME types ----
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
};

// ---- Register API routes ----
require('./routes/register')(router);
require('./routes/trial')(router);
require('./routes/contact')(router);
require('./routes/admin')(router);

// ---- Parse JSON body ----
function parseBody(req) {
  return new Promise((resolve) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try { resolve(JSON.parse(body)); }
      catch (e) { resolve({}); }
    });
  });
}

// ---- Send JSON response ----
function sendJSON(res, status, data) {
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  });
  res.end(JSON.stringify(data));
}

// ---- Serve static file ----
function serveStatic(res, urlPath) {
  let filePath = path.join(ROOT, urlPath === '/' ? 'index.html' : urlPath);

  // If path ends with /, serve index.html
  if (filePath.endsWith('/')) filePath = path.join(filePath, 'index.html');

  // If file doesn't exist, try .html
  if (!fs.existsSync(filePath) && !path.extname(filePath)) {
    const htmlPath = filePath + '.html';
    if (fs.existsSync(htmlPath)) filePath = htmlPath;
  }

  // Handle admin page
  if (urlPath === '/admin/' || urlPath === '/admin') {
    filePath = path.join(__dirname, 'public', 'index.html');
  }

  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME[ext] || 'application/octet-stream';
    const content = fs.readFileSync(filePath);
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(content);
  } else {
    // Try as HTML page name
    const htmlTry = path.join(ROOT, urlPath);
    if (fs.existsSync(htmlTry + '.html')) {
      const content = fs.readFileSync(htmlTry + '.html');
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(content);
    } else {
      sendJSON(res, 404, { error: 'Not Found' });
    }
  }
}

// ---- Server ----
const server = http.createServer(async (req, res) => {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    return res.end();
  }

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = url.pathname;

  // API routes
  if (pathname.startsWith('/api/')) {
    const match = router.resolve(req.method, pathname);
    if (match) {
      try {
        const body = (req.method === 'POST' || req.method === 'PUT') ? await parseBody(req) : {};
        const result = match.handler({ params: match.params, query: url.searchParams, body }, body);
        const status = result.status || 200;
        sendJSON(res, status, result.body);
      } catch (e) {
        console.error('API error:', e);
        sendJSON(res, 500, { success: false, message: '服务器内部错误' });
      }
    } else {
      sendJSON(res, 404, { success: false, message: '接口未找到' });
    }
    return;
  }

  // Health check
  if (pathname === '/health') {
    sendJSON(res, 200, { status: 'ok', time: new Date().toISOString() });
    return;
  }

  // Static files
  serveStatic(res, pathname);
});

server.listen(PORT, () => {
  console.log('==========================================');
  console.log('  CAAC 无人机培训报名系统已启动');
  console.log(`  前台: http://localhost:${PORT}`);
  console.log(`  管理后台: http://localhost:${PORT}/admin/`);
  console.log('==========================================');
});

