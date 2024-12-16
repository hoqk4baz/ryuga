import http.server
import socketserver

PORT = 1055
DIRECTORY = "."

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def end_headers(self):
        self.send_header("Content-Type", "text/html; charset=utf-8")
        super().end_headers()

with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    print(f"Sunucu http://127.0.0.1:{PORT} adresinde çalışıyor.")
    httpd.serve_forever()
