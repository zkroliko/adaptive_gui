from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from cameraSource import CameraSource

PORT_NUMBER = 8080


class myHandler(BaseHTTPRequestHandler):

    source = CameraSource()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(str(self.source.get_ratio()))
        return

try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
