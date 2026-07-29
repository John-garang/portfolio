#!/usr/bin/env python3
import http.server
import socketserver
import os
import mimetypes

PORT = int(os.environ.get('PORT', 8080))

class SmartCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    # Static assets get long-term caching
    STATIC_ASSETS = {'.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg', 
                     '.webp', '.woff', '.woff2', '.ttf', '.eot', '.ico'}
    
    def end_headers(self):
        """Apply smart caching based on file type"""
        file_ext = os.path.splitext(self.path)[1].lower()
        
        if file_ext in self.STATIC_ASSETS:
            # Long-term caching for static assets (1 year)
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        else:
            # No caching for HTML files (always fetch fresh)
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        
        # Security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-XSS-Protection', '1; mode=block')
        
        super().end_headers()
    
    def guess_type(self, path):
        """Ensure correct MIME types"""
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type:
            return mime_type
        # Fallback for common types
        if path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.xml'):
            return 'application/xml'
        elif path.endswith('.txt'):
            return 'text/plain'
        return 'application/octet-stream'
    
    def do_GET(self):
        """Handle routing with HTML auto-append"""
        clean = self.path.split('?')[0]
        if clean == '/':
            self.path = 'templates/index.html'
        elif clean in ('/sitemap.xml', '/robots.txt'):
            # Serve sitemap and robots from templates/ with correct type
            self.path = 'templates/' + clean.lstrip('/')
        elif '.' in clean.split('/')[-1]:
            # Has a file extension — serve from templates/
            self.path = 'templates/' + clean.lstrip('/')
        else:
            # Try direct .html file first, then directory/index.html
            direct = 'templates/' + clean.lstrip('/') + '.html'
            if os.path.exists(direct):
                self.path = direct
            else:
                self.path = 'templates/' + clean.lstrip('/') + '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Enable address reuse
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), SmartCacheHTTPRequestHandler) as httpd:
    print(f"✓ Server running at http://localhost:{PORT}")
    print(f"✓ Smart caching enabled: HTML=no-cache, Assets=1yr cache")
    httpd.serve_forever()
