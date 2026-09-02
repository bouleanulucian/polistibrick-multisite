#!/usr/bin/env python3
"""Server static pentru previzualizare locală, cu cache DEZACTIVAT.
Folosire: python3 serveste-fara-cache.py <director> <port>
Chrome ține index.html din cache la localhost → patronul vede versiunea veche după modificări."""
import sys, os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class FaraCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    def log_message(self, *a):  # liniște în consolă
        pass

if __name__ == '__main__':
    director, port = sys.argv[1], int(sys.argv[2])
    os.chdir(director)
    ThreadingHTTPServer(('', port), FaraCache).serve_forever()
