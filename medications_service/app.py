from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse
from db import (
    create_medication,
    get_medication_by_id,
    get_all_medications_for_user,
    update_medication,
    delete_medication
)


class MedicationsHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]

        try:
            if len(path_parts) == 3 and path_parts[0] == 'users' and path_parts[2] == 'medications':
                user_id = int(path_parts[1])
                medications = get_all_medications_for_user(user_id)
                self._set_headers()
                self.wfile.write(json.dumps(medications).encode())
            elif len(path_parts) == 2 and path_parts[0] == 'medications':
                medication_id = int(path_parts[1])
                medication = get_medication_by_id(medication_id)
                if medication:
                    self._set_headers()
                    self.wfile.write(json.dumps(medication).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({'error': 'Medication not found'}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Not found'}).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))

        medication_id = create_medication(
            post_data['user_id'],
            post_data['medication_name'],
            post_data.get('dosage', ''),
            post_data.get('start_date', None),
            post_data.get('end_date', None),
            post_data.get('reason', '')
        )

        if medication_id:
            self._set_headers(201)
            self.wfile.write(json.dumps({'medication_id': medication_id}).encode())
        else:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': 'Failed to create medication record'}).encode())

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]
        
        if len(path_parts) == 2 and path_parts[0] == 'medications':
            medication_id = int(path_parts[1])
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))

            success = update_medication(
                medication_id,
                post_data['user_id'],
                post_data['medication_name'],
                post_data.get('dosage', ''),
                post_data.get('start_date', None),
                post_data.get('end_date', None),
                post_data.get('reason', '')
            )

            if success:
                self._set_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Medication not found or not updated'}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]
        
        if len(path_parts) == 2 and path_parts[0] == 'medications':
            medication_id = int(path_parts[1])
            success = delete_medication(medication_id)

            if success:
                self._set_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Medication not found or not deleted'}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

def run(server_class=HTTPServer, handler_class=MedicationsHandler, port=8082):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting medications service on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
