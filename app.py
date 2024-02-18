from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import mysql.connector
from db import create_connection  # Import database connection function

# Define a handler for our HTTP requests
class NoteHandler(BaseHTTPRequestHandler):
    # Helper method to set HTTP headers for response
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    # Handle GET requests
    def do_GET(self):
        # Connect to database
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        # Feth all notes
        cursor.execute("SELECT * FROM notes")
        notes = cursor.fetchall()  # Store the results
        cursor.close()
        connection.close()

        # Set response headers and write the notes data as JSON
        self._set_headers()
        self.wfile.write(json.dumps(notes).encode('utf-8'))

    # handle POST requests
    def do_POST(self):
        # determine size of the data for parsing
        content_length = int(self.headers['Content-Length'])
        # read the raw data
        post_data = self.rfile.read(content_length)
        # convert data to json
        note = json.loads(post_data)

        # Insert the new note data into the database
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (note['title'], note['content']))
        connection.commit()  # commit
        cursor.close()
        connection.close()

        # Send 201 Created response with confirmation message
        self._set_headers(201)
        self.wfile.write(json.dumps({'message': 'Note created'}).encode('utf-8'))

# Function to start the HTTP server
def run(server_class=HTTPServer, handler_class=NoteHandler, port=8080):
    server_address = ('', port)
    # Instantiate the server class
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd on port {port}...")  # Server start-up message
    httpd.serve_forever()  # Start the server to listen for requests

# Entry point of the script
if __name__ == '__main__':
    run()
