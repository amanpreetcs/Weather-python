from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from urllib.parse import urlparse, parse_qs
import os

class server_handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle preflight request
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        api_key = os.environ['API_KEY']
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        city = query_params.get('city', ['Delhi'])[0]
        print(query_params,city)

        data = []
        response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}')

        if response.status_code==200:
            res = response.json()
            data = {
                'location':res['location']['name'],
                'tempc':res['current']['temp_c'],
                'tempf':res['current']['temp_f'],
                'condition':res['current']['condition']['text']
            }
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'data': data}).encode())


def run(handler):
    port = 3004
    server_address = ("",port)
    server = HTTPServer(server_address,handler)
    print(f'Starting server on PORT: {port}')
    server.serve_forever()


# Run the server only when this file is called, not imported
if __name__ == "__main__":
    run(server_handler)