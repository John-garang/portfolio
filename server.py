#!/usr/bin/env python3
import http.server
import socketserver
import os
import gzip
import email.utils
import threading

PORT = int(os.environ.get('PORT', 8080))

CSP = ("default-src 'self'; "
       "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src 'self' https://fonts.gstatic.com; "
       "img-src 'self' data: https://*.google-analytics.com https://*.googletagmanager.com; "
       "connect-src 'self' https://api.emailjs.com https://*.google-analytics.com "
       "https://*.analytics.google.com https://*.googletagmanager.com;")

MIME = {
    '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8', '.json': 'application/json',
    '.xml': 'application/xml; charset=utf-8', '.xsl': 'text/xsl; charset=utf-8',
    '.txt': 'text/plain; charset=utf-8', '.svg': 'image/svg+xml',
    '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
    '.gif': 'image/gif', '.ico': 'image/x-icon', '.woff': 'font/woff', '.woff2': 'font/woff2',
    '.ttf': 'font/ttf', '.pdf': 'application/pdf',
}

SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
_gzip_cache = {}
_gzip_lock = threading.Lock()


class SmartCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    STATIC_ASSETS  = {'.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg',
                      '.webp', '.woff', '.woff2', '.ttf', '.eot', '.ico'}
    COMPRESSIBLE   = {'.html', '.css', '.js', '.json', '.xml', '.xsl', '.txt', '.svg'}

    def end_headers(self):
        ext = os.path.splitext(self.path or '')[1].lower()
        if ext in self.STATIC_ASSETS:
            # CSS/JS carry ?v= versions; images keep their names, so cache them long
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        else:
            # pages: browsers may keep a copy but must check it is still current
            self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Content-Security-Policy', CSP)
        if getattr(self, '_noindex', False):
            self.send_header('X-Robots-Tag', 'noindex')
        super().end_headers()

    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        return MIME.get(ext) or super().guess_type(path) or 'application/octet-stream'

    GONE_PATHS = {
        # old standalone poem pages
        '/an-unbalanced-man', '/an-unbalanced-man.html',
        '/learning-to-write-without-permission', '/learning-to-write-without-permission.html',
        '/the-price-of-truth', '/the-price-of-truth.html',
        '/if-equality-means-this', '/if-equality-means-this.html',
        '/making-of-dinka-woman', '/making-of-dinka-woman.html',
        '/when-educated-woman-says-no', '/when-educated-woman-says-no.html',
        '/the-son-mama-couldnt-save', '/the-son-mama-couldnt-save.html',
        '/a-sour-vow', '/a-sour-vow.html',
        '/a-fool-of-warmth', '/a-fool-of-warmth.html',
        '/the-words-i-never-said', '/the-words-i-never-said.html',
        '/the-boy-who-taught-his-nation-to-speak', '/the-boy-who-taught-his-nation-to-speak.html',
        # old experience/program pages
        '/education-bridge', '/education-bridge.html',
        '/africa-inventor-alliance', '/africa-inventor-alliance.html',
        '/nalafem-collective', '/nalafem-collective.html',
        '/surplus-people-project', '/surplus-people-project.html',
        '/uganics-repellents', '/uganics-repellents.html',
        '/take-action-lab', '/take-action-lab.html',
        '/unleash-innovation-lab', '/unleash-innovation-lab.html',
        '/african-leadership-university', '/african-leadership-university.html',
        '/cnn-academy', '/cnn-academy.html',
        '/accra-fusion', '/accra-fusion.html',
        '/yali-east-africa', '/yali-east-africa.html',

        # old article/blog pages
        '/article', '/articles', '/blogs',
        '/artefacts', '/artefacts.html',
        '/addressing-entrepreneurial-gaps-south-sudan', '/addressing-entrepreneurial-gaps-south-sudan.html',
        '/cape-town-travel-guide', '/cape-town-travel-guide.html',
        # articles retired from My Shelf (Nov 2026)
        '/travels/the-not-a-tourist-price',
        '/blog/jongleis-tragedy-is-intellectual',
        '/blog/2025-the-year-of-politics-shenanigans-and-professional-nonsense',
        '/blog/courtesy-is-not-weakness-youth-politics-in-bor-duk-and-twic',
        '/blog/do-not-decorate-this-with-culture',
        '/blog/bor-2013-the-stories-no-one-wrote-down',
        '/blog/build-with-someone-your-age',
        '/blog/dear-jieng-the-wife-is-not-the-enemy',
        # old misc pages
    }

    def _send_error_page(self, code):
        """Serve the styled error page with the correct HTTP status code."""
        error_path = 'templates/error.html'
        try:
            with open(error_path, 'rb') as f:
                raw = f.read()
            # Inject the error code so JS can customise the message
            raw = raw.replace(b'window.__errorCode === 410', f'window.__errorCode === {code}'.encode())
            raw = raw.replace(b"window.__errorCode = undefined", f"window.__errorCode = {code}".encode())
            # Set the JS variable before the check runs
            raw = raw.replace(b'<script>', f'<script>window.__errorCode = {code};'.encode(), 1)
        except FileNotFoundError:
            raw = f'<h1>{code}</h1>'.encode()
        self.path = ''  # error pages are never cached as static assets
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
        self.path = None

    REDIRECT_PATHS = {
        '/academia.html': '/academia',
        '/cv.html': '/cv',
        '/blog.html': '/blog',
        '/graphic-design.html': '/graphic-design',
        '/web-design.html': '/web-design',
        '/my-shelf.html': '/my-shelf',
        '/travels.html': '/travels',
    }

    def _redirect(self, location):
        self.send_response(301)
        self.send_header('Location', location)
        self.send_header('Content-Length', '0')
        self.end_headers()
        self.path = None

    def _route(self):
        """Resolve URL path to a file path in templates/."""
        self._noindex = False
        clean, _, query = self.path.partition('?')
        qs = ('?' + query) if query else ''
        # Redirects (301)
        if clean in self.REDIRECT_PATHS:
            self._redirect(self.REDIRECT_PATHS[clean] + qs)
            return
        # Always check GONE_PATHS first, before any file-serving logic
        if clean in self.GONE_PATHS:
            self._send_error_page(410)
            return
        # One address per page: drop trailing slashes and .html endings
        if clean != '/' and clean.endswith('/'):
            self._redirect(clean.rstrip('/') + qs)
            return
        if clean.endswith('.html') and not clean.startswith('/static/'):
            target = clean[:-5]
            if target.endswith('/index'):
                target = target[:-6] or '/'
            if os.path.isfile('templates/' + clean.lstrip('/')):
                self._redirect((target or '/') + qs)
                return
        # fragments and utility pages stay out of search results
        self._noindex = clean in ('/footer', '/search-results', '/error')
        if clean == '/':
            self.path = 'templates/index.html'
        elif '.' in clean.split('/')[-1]:
            self.path = 'templates/' + clean.lstrip('/')
        else:
            direct    = 'templates/' + clean.lstrip('/') + '.html'
            directory = 'templates/' + clean.lstrip('/') + '/index.html'
            if os.path.exists(direct):
                self.path = direct
            elif os.path.exists(directory):
                self.path = directory
            else:
                self._send_error_page(404)

    def _serve(self, head=False):
        self._route()
        if self.path is None:
            return  # redirect, 404 or 410 already sent

        fs = os.path.realpath(self.translate_path('/' + self.path))
        if not fs.startswith(SITE_ROOT + os.sep) or not os.path.isfile(fs):
            self._send_error_page(404)
            return

        st = os.stat(fs)
        mtime = int(st.st_mtime)
        ims = self.headers.get('If-Modified-Since')
        if ims:
            try:
                if email.utils.parsedate_to_datetime(ims).timestamp() >= mtime:
                    self.send_response(304)
                    self.end_headers()
                    return
            except (TypeError, ValueError, IndexError, OverflowError):
                pass

        ext = os.path.splitext(fs)[1].lower()
        gz = 'gzip' in self.headers.get('Accept-Encoding', '') and ext in self.COMPRESSIBLE
        if gz:
            key = (fs, st.st_mtime_ns)
            data = _gzip_cache.get(key)
            if data is None:
                with open(fs, 'rb') as f:
                    data = gzip.compress(f.read(), compresslevel=9)
                with _gzip_lock:
                    _gzip_cache[key] = data
        else:
            with open(fs, 'rb') as f:
                data = f.read()

        self.send_response(200)
        self.send_header('Content-Type', self.guess_type(fs))
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Last-Modified', email.utils.formatdate(mtime, usegmt=True))
        if ext in self.COMPRESSIBLE:
            self.send_header('Vary', 'Accept-Encoding')
        if gz:
            self.send_header('Content-Encoding', 'gzip')
        self.end_headers()
        if not head:
            self.wfile.write(data)

    def do_GET(self):
        self._serve()

    def do_HEAD(self):
        self._serve(head=True)

    def log_message(self, fmt, *args):
        if os.environ.get('QUIET_LOGS'):
            return
        super().log_message(fmt, *args)


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


with Server(("", PORT), SmartCacheHTTPRequestHandler) as httpd:
    print(f"✓ Server running at http://localhost:{PORT}")
    print(f"✓ Gzip compression + smart caching enabled")
    httpd.serve_forever()
