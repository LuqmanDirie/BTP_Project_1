from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from db import create_user, get_user_by_id, get_all_users, update_user, delete_user
import hashlib

class UserHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]

        if len(path_parts) == 2 and path_parts[0] == 'users':
            user_id = int(path_parts[1])
            user = get_user_by_id(user_id)
            self.send_response(200 if user else 404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(user if user else {}).encode())
        elif self.path == '/users':
            try:
                users = get_all_users()
                self.send_response(200)
            except Exception as e:
                users = {'error': str(e)}
                self.send_response(500)
    
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(users).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_POST(self):
        if self.path == '/users':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))

            hashed_password = hashlib.sha256(post_data['password'].encode()).hexdigest()

            user_id = create_user(post_data['username'], hashed_password, post_data['full_name'], post_data['dob'], post_data['gender'])
            if user_id:
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'user_id': user_id}).encode())
                print(f"User successfully added with ID: {user_id}")
            else:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'User could not be created'}).encode())

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))

        if len(path_parts) == 2 and path_parts[0] == 'users':
            user_id = int(path_parts[1])
            hashed_password = hashlib.sha256(post_data['password'].encode()).hexdigest()
            success = update_user(user_id, post_data['username'], hashed_password, post_data['full_name'], post_data['dob'], post_data['gender'])
            self.send_response(200 if success else 404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': success} if success else {'error': 'Update failed'}).encode())

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]
        if len(path_parts) == 2 and path_parts[0] == 'users':
            user_id = int(path_parts[1])
            success = delete_user(user_id)
            self.send_response(200 if success else 404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': success} if success else {'error': 'Delete failed'}).encode())

def run(server_class=HTTPServer, handler_class=UserHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=8080)
