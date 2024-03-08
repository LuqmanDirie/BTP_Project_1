from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from db import (
    create_test_result,
    get_test_result_by_id,
    get_all_test_results_for_user,
    update_test_result,
    delete_test_result
)

class TestResultsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]
        
        if len(path_parts) == 3 and path_parts[0] == 'users' and path_parts[2] == 'test_results':
            user_id = int(path_parts[1])
            test_results = get_all_test_results_for_user(user_id)
            if test_results is not None:
                self._set_headers(200)
                self.wfile.write(json.dumps(test_results).encode())
            else:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': 'Failed to retrieve test results.'}).encode())
        elif len(path_parts) == 2 and path_parts[0] == 'test_results':
            result_id = int(path_parts[1])
            test_result = get_test_result_by_id(result_id)
            if test_result:
                self._set_headers(200)
                self.wfile.write(json.dumps(test_result).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Test result not found'}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))

        user_id = post_data.get('user_id')
        test_type = post_data.get('test_type')
        result_date = post_data.get('result_date')
        result = post_data.get('result')
        notes = post_data.get('notes')
        
        result_id = create_test_result(user_id, test_type, result_date, result, notes)
        if result_id:
            self._set_headers(201)
            self.wfile.write(json.dumps({'result_id': result_id}).encode())
        else:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': 'Failed to create test result.'}).encode())


    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]

        if len(path_parts) == 2 and path_parts[0] == 'test_results':
            result_id = int(path_parts[1])
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            
            updated = update_test_result(
                result_id,
                post_data.get('user_id'),
                post_data.get('test_type'),
                post_data.get('result_date'),
                post_data.get('result'),
                post_data.get('notes')
            )
            
            if updated:
                self._set_headers(200)
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Test result not found or not updated'}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())



    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]

        if len(path_parts) == 2 and path_parts[0] == 'test_results':
            result_id = int(path_parts[1])
            deleted = delete_test_result(result_id)
            if deleted:
                self._set_headers(200)
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Test result not found or not deleted'}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())


def run(server_class=HTTPServer, handler_class=TestResultsHandler, port=8085):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting test results service on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
