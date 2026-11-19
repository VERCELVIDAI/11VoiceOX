import http.server
import socketserver
import os
import sys
import mimetypes

PORT = int(os.environ.get("PORT", 3000))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('application/manifest+json', '.webmanifest')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('video/mp4', '.mp4')
mimetypes.add_type('application/json', '.json')

class CleanRouteHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Clean URL support: /clone -> /clone/index.html or /clone.html
        path = self.path.split('?')[0].split('#')[0]
        full_path = os.path.join(DIRECTORY, path.lstrip('/').replace('/', os.sep))
        
        if not os.path.exists(full_path):
            if os.path.exists(full_path + ".html"):
                self.path = path + ".html"
            elif os.path.exists(os.path.join(full_path, "index.html")):
                self.path = path.rstrip('/') + "/index.html"
                
        return super().do_GET()

    def end_headers(self):
        # Enable CORS and caching headers for assets
        self.send_header('Access-Control-Allow-Origin', '*')
        if self.path.startswith('/assets/'):
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        else:
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), CleanRouteHTTPRequestHandler) as httpd:
        print(f"11VoiceOX.in website server running at http://localhost:{PORT}")
        print(f"Serving directory: {DIRECTORY}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
