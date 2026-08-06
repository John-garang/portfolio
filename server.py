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

    def _route(self):
        """Resolve URL path to a file path in templates/."""
        clean = self.path.split('?')[0]
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
                self.send_response(404)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<h1>404 Not Found</h1>')
                self.path = None  # signal that response is already sent

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
