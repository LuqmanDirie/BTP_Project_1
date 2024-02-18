from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class NoteHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        # Placeholder for GET request handling
        self._set_headers()
        self.wfile.write(json.dumps({'message': 'This is a GET request'}).encode('utf-8'))

    def do_POST(self):
        # Placeholder for POST request handling
        self._set_headers()
        self.wfile.write(json.dumps({'message': 'This is a POST request'}).encode('utf-8'))

    def do_PUT(self):
        # Placeholder for PUT request handling
        self._set_headers()
        self.wfile.write(json.dumps({'message': 'This is a PUT request'}).encode('utf-8'))

    def do_DELETE(self):
        # Placeholder for DELETE request handling
        self._set_headers()
        self.wfile.write(json.dumps({'message': 'This is a DELETE request'}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=NoteHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
