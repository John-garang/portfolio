#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def start_server():
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"[OK] Server starting at http://localhost:{PORT}")
            print(f"[INFO] Serving files from: {os.getcwd()}")
            print(f"[INFO] Opening browser...")
            
            # Open browser automatically
            webbrowser.open(f'http://localhost:{PORT}')
            
            print(f"[RUNNING] Server is running! Press Ctrl+C to stop.")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[STOPPED] Server stopped by user")
    except OSError as e:
        if e.errno == 10048:  # Port already in use
            print(f"[ERROR] Port {PORT} is already in use. Try a different port.")
        else:
            print(f"[ERROR] Error starting server: {e}")

if __name__ == "__main__":
    start_server()