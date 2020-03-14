import json
from settings import group
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"huh?")

    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers["content-length"])))
        self.send_response(200)
        self.end_headers()
        if data.get("group_id") == int(group.get("GROUP_ID")) and data.get("secret") == group.get("WEBHOOK_SECRET"):
            if data.get("type") == "confirmation":
                self.wfile.write(group["CONFIRMATION"].encode("utf-8"))
            else:
                self.wfile.write(b"ok")
                if data.get("type") == "message_new":
                    from messages import MessageParser
                    MessageParser(data.get("object"))


# VK forces to use default port, meh
server = HTTPServer(('', 443), RequestHandler)

# SSL certificate
server.socket = ssl.wrap_socket(server.socket, keyfile=".settings/privkey.pem", certfile=".settings/cert.pem", server_side=True, ssl_version=ssl.PROTOCOL_SSLv23)
server.serve_forever()
