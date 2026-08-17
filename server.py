#!/usr/bin/env python3
import http.server
import socketserver
import os
import mimetypes
import gzip
import io

PORT = int(os.environ.get('PORT', 8080))

class SmartCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    STATIC_ASSETS  = {'.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg',
                      '.webp', '.woff', '.woff2', '.ttf', '.eot', '.ico'}
    COMPRESSIBLE   = {'.html', '.css', '.js', '.json', '.xml', '.txt', '.svg'}

    def end_headers(self):
        ext = os.path.splitext(self.path)[1].lower()
        if ext in self.STATIC_ASSETS:
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        else:
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://api.emailjs.com;")
        super().end_headers()

    def guess_type(self, path):
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type:
            return mime_type
        if path.endswith('.css'):   return 'text/css'
        if path.endswith('.js'):    return 'application/javascript'
        if path.endswith('.xml'):   return 'application/xml'
        if path.endswith('.txt'):   return 'text/plain'
        return 'application/octet-stream'

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
        '/cv', '/cv.html',
        '/academia', '/academia.html',
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
        '/work-portfolio', '/work-portfolio.html',
        # old article/blog pages
        '/article', '/articles', '/blog', '/blogs',
        '/artefacts', '/artefacts.html',
        '/addressing-entrepreneurial-gaps-south-sudan', '/addressing-entrepreneurial-gaps-south-sudan.html',
        '/development-trajectory-south-sudan', '/development-trajectory-south-sudan.html',
        '/entrepreneurial-gaps-south-sudan', '/entrepreneurial-gaps-south-sudan.html',
        '/cape-town-travel-guide', '/cape-town-travel-guide.html',
        # old misc pages
        '/my-shelf', '/my-shelf.html',
        '/travels', '/travels.html',
        '/graphic-design', '/graphic-design.html',
        '/web-design', '/web-design.html',
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
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
        self.path = None

    def _route(self):
        """Resolve URL path to a file path in templates/."""
        clean = self.path.split('?')[0]
        if clean in self.GONE_PATHS:
            self._send_error_page(410)
            return
        if clean == '/':
            self.path = 'templates/index.html'
        elif clean in ('/sitemap.xml', '/robots.txt'):
            self.path = 'templates/' + clean.lstrip('/')
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

    def do_GET(self):
        self._route()
        if self.path is None:
            return  # 404 already sent

        ext    = os.path.splitext(self.path)[1].lower()
        accept = self.headers.get('Accept-Encoding', '')

        if 'gzip' in accept and ext in self.COMPRESSIBLE and os.path.isfile(self.path):
            with open(self.path, 'rb') as f:
                raw = f.read()
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=6) as gz:
                gz.write(raw)
            data = buf.getvalue()
            self.send_response(200)
            self.send_header('Content-Type', self.guess_type(self.path))
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)


socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), SmartCacheHTTPRequestHandler) as httpd:
    print(f"✓ Server running at http://localhost:{PORT}")
    print(f"✓ Gzip compression + smart caching enabled")
    httpd.serve_forever()
