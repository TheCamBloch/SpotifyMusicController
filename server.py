import http.server
import socketserver
import threading
import os
from urllib.parse import urlparse

base_path = os.path.dirname(__file__)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global code
        self.send_response(200)
        self.end_headers()
        parsed = urlparse(self.path)
        self.wfile.write(b"")
        if "code=" in parsed.query:
            print("Server reicieved authorization code")
            code = parsed.query.strip("code=")
            stop_http.start()
        
    def log_message(self, format, *args):
        pass

server = socketserver.TCPServer(("127.0.0.1", 8000), QuietHandler)

start_http = threading.Thread(target=server.serve_forever, daemon=True)
stop_http = threading.Thread(target=server.shutdown, daemon=True)

if __name__ == "__main__":
    start_http.start()