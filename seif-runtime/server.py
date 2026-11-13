"""Seif settings + persistent interval worker. Python 3.10+, standard library."""
import json
import os
import secrets
import signal
import threading
import time
import urllib.request
from urllib.parse import urlparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get('SEIF_DATA_DIR', str(ROOT)))
DATA.mkdir(parents=True, exist_ok=True)
CONFIG = DATA / 'runtime-config.json'
N8N_BASE = os.environ.get('SEIF_N8N_BASE_URL', 'http://127.0.0.1:5678').rstrip('/')
N8N_UI = os.environ.get('SEIF_N8N_UI_URL', 'http://127.0.0.1:5678')
LOCK = threading.RLock()
WAKE = threading.Event()
STOP = threading.Event()
TOKEN = secrets.token_urlsafe(32)
STATE = {'interval_seconds': 60, 'dispatch_enabled': False, 'endpoint': '', 'task': '', 'settings': []}
STATUS = {'ticks': 0, 'last_tick': None, 'last_result': 'waiting', 'scheduler_running': True}
if CONFIG.exists():
    STATE.update(json.loads(CONFIG.read_text(encoding='utf-8')))

def snapshot():
    with LOCK:
        return {**STATE, **STATUS}

def persist():
    tmp = CONFIG.with_suffix('.tmp')
    tmp.write_text(json.dumps(STATE, ensure_ascii=False, indent=2), encoding='utf-8')
    os.chmod(tmp, 0o600)
    tmp.replace(CONFIG)

def worker():
    # One job at a time. Each next interval begins after the preceding job ends.
    while not STOP.is_set():
        with LOCK:
            interval = STATE['interval_seconds']
        if WAKE.wait(interval):
            WAKE.clear()
            continue
        if STOP.is_set():
            break
        with LOCK:
            cfg = dict(STATE)
            STATUS['ticks'] += 1
            STATUS['last_tick'] = datetime.now(timezone.utc).isoformat()
            tick = STATUS['ticks']
        result = 'tick recorded; workflow dispatch disabled'
        if cfg['dispatch_enabled'] and cfg['endpoint']:
            headers = {'Content-Type': 'application/json', 'Idempotency-Key': secrets.token_hex(16)}
            credential = os.environ.get('SEIF_PROVIDER_TOKEN')
            if credential:
                headers['Authorization'] = 'Bearer ' + credential
            payload = json.dumps({'task': cfg['task'], 'tick': tick, 'settings': cfg['settings']}).encode()
            req = urllib.request.Request(cfg['endpoint'], data=payload, headers=headers, method='POST')
            try:
                # No automatic retries: downstream side effects may already have occurred.
                with urllib.request.urlopen(req, timeout=20) as response:
                    result = 'provider HTTP ' + str(response.status)
            except Exception as exc:
                result = 'provider result unconfirmed: ' + type(exc).__name__
        with LOCK:
            STATUS['last_result'] = result
        print(json.dumps({'tick': tick, 'result': result}), flush=True)
    with LOCK:
        STATUS['scheduler_running'] = False

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def send(self, code, payload, content_type='application/json'):
        data = payload.encode() if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', content_type + '; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def allowed(self):
        return self.headers.get('Host') in {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}

    def do_GET(self):
        if not self.allowed():
            return self.send(403, {'error': 'invalid host'})
        if self.path == '/api/payment':
            with LOCK:
                link = next((x.get('value') for x in STATE['settings'] if x.get('id') == 'payment_link'), '') or ''
            parsed = urlparse(link)
            supported = parsed.scheme == 'https' and parsed.hostname in {'paypal.com', 'www.paypal.com', 'paypal.me', 'www.paypal.me'} and not parsed.username and not parsed.password
            return self.send(200, {'configured': supported, 'checkout_url': link if supported else None, 'payment_received': None})
        if self.path == '/api/n8n':
            healthy = False
            try:
                with urllib.request.urlopen(N8N_BASE + '/healthz/readiness', timeout=3) as r:
                    healthy = r.status == 200
            except Exception:
                pass
            return self.send(200, {'healthy': healthy, 'ui_url': N8N_UI, 'repository': 'https://github.com/s-os-agency/n8n'})
        if self.path == '/api/status':
            return self.send(200, snapshot())
        if self.path == '/':
            html = (ROOT / 'index.html').read_text(encoding='utf-8')
            return self.send(200, html.replace('__SEIF_CSRF__', TOKEN), 'text/html')
        self.send(404, {'error': 'not found'})

    def do_POST(self):
        if not self.allowed() or self.headers.get('X-Seif-Token') != TOKEN:
            return self.send(403, {'error': 'invalid session'})
        if self.path != '/api/config':
            return self.send(404, {'error': 'not found'})
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length < 1 or length > 1000000:
                raise ValueError('invalid payload size')
            body = json.loads(self.rfile.read(length))
            interval = body['interval_seconds']
            if type(interval) is not int or not 1 <= interval <= 86400:
                raise ValueError('interval must be 1..86400 seconds')
            enabled = body['dispatch_enabled']
            if type(enabled) is not bool:
                raise ValueError('dispatch_enabled must be boolean')
            endpoint = body.get('endpoint', '').strip()
            if endpoint and not (endpoint.startswith('https://') or endpoint.startswith(N8N_BASE + '/webhook/')):
                raise ValueError('use HTTPS, or a webhook on the configured local n8n service')
            if enabled and (not endpoint or not body.get('task', '').strip()):
                raise ValueError('define task and provider endpoint before dispatch')
            settings = body.get('settings', [])
            if not isinstance(settings, list) or len(settings) > 200 or any(not isinstance(x, dict) for x in settings):
                raise ValueError('invalid settings')
            payment_link = next((x.get('value') for x in settings if x.get('id') == 'payment_link'), '') or ''
            if payment_link:
                parsed = urlparse(payment_link)
                if parsed.scheme != 'https' or parsed.hostname not in {'paypal.com', 'www.paypal.com', 'paypal.me', 'www.paypal.me'} or parsed.username or parsed.password:
                    raise ValueError('use the original HTTPS PayPal payment link')
            with LOCK:
                STATE.update(interval_seconds=interval, dispatch_enabled=enabled, endpoint=endpoint,
                             task=body.get('task', ''), settings=settings)
                persist()
            WAKE.set()
            self.send(200, snapshot())
        except (ValueError, TypeError, KeyError, AttributeError) as exc:
            self.send(400, {'error': str(exc)})

if __name__ == '__main__':
    port = int(os.environ.get('SEIF_PORT', '8765'))
    server = ThreadingHTTPServer((os.environ.get('SEIF_BIND', '127.0.0.1'), port), Handler)
    threading.Thread(target=worker, daemon=True).start()
    def shutdown(*_):
        STOP.set()
        WAKE.set()
        threading.Thread(target=server.shutdown, daemon=True).start()
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    print(f'Seif runtime: http://127.0.0.1:{port} (interval: {STATE["interval_seconds"]} seconds)', flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()
        STOP.set()
        WAKE.set()
