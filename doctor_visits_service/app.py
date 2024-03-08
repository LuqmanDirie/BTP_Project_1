from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from db import (
    create_doctor_visit,
    get_doctor_visit_by_id,
    get_all_doctor_visits_for_user,
    update_doctor_visit,
    delete_doctor_visit
)

class DoctorVisitsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]
        
        try:
            if len(path_parts) == 3 and path_parts[0] == 'users' and path_parts[2] == 'doctor_visits':
                user_id = int(path_parts[1])
                visits = get_all_doctor_visits_for_user(user_id)
                self._set_headers()
                self.wfile.write(json.dumps(visits).encode())
            elif len(path_parts) == 2 and path_parts[0] == 'doctor_visits':
                visit_id = int(path_parts[1])
                visit = get_doctor_visit_by_id(visit_id)
                if visit:
                    self._set_headers()
                    self.wfile.write(json.dumps(visit).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({'error': 'Visit not found'}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Not found'}).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))

        visit_id = create_doctor_visit(
            post_data['user_id'],
            post_data['visit_date'],
            post_data.get('doctor_name', ''),
            post_data.get('purpose', ''),
            post_data.get('notes', '')
        )

        if visit_id:
            self._set_headers(201)
            self.wfile.write(json.dumps({'visit_id': visit_id}).encode())
        else:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': 'Failed to create doctor visit record'}).encode())

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]

        if len(path_parts) == 2 and path_parts[0] == 'doctor_visits':
            visit_id = int(path_parts[1])
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))

            success = update_doctor_visit(
                visit_id,
                post_data['user_id'],
                post_data['visit_date'],
                post_data.get('doctor_name', ''),
                post_data.get('purpose', ''),
                post_data.get('notes', '')
            )

            if success:
                self._set_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Visit not found or not updated'}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())


    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]

        if len(path_parts) == 2 and path_parts[0] == 'doctor_visits':
            visit_id = int(path_parts[1])
            success = delete_doctor_visit(visit_id)

            if success:
                self._set_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Visit not found or not deleted'}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())



def run(server_class=HTTPServer, handler_class=DoctorVisitsHandler, port=8085):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting doctor visits service on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
