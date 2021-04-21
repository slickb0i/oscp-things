#!/bin/python3

# A simple python server that will store files sent through a POST request. Ideal
# for quickly sending files stored in a place in that is somewhat unaccessible. Should
# work for both binary and text files (as long as you POST the file correctly).
#
# From client machine:
#
# curl -XPOST -F "file=@file-to-copy.txt" http://server-ip:port

import argparse
import http.server
import socketserver
import cgi

# Use command line to specify options
options = {}

def parse_args():
    parser = argparse.ArgumentParser(description='Simple server to recieve files')
    parser.add_argument('--addr', default='0.0.0.0', help='Address to listen on')
    parser.add_argument('--port', default=8000, help='Port to listen on')
    parser.add_argument('--file', default='output.txt', help='File to write to')
    global options
    options = vars(parser.parse_args())

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.close_connection = True
        self.end_headers()
        self.flush_headers()

        if self.path == "/data":
            print("[+] Receieved data from {0}".format(self.client_address[0]))
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
            if "file" in form:
                print("[+] Writing to file {0}".format(options['file']))
                with open(options['file'], 'wb') as fh:
                    fh.write(form['file'].value)
                print("[+] Data successfully stored")

parse_args()
print("[+] Serving on {0} port {1}".format(options['addr'],options['port']))
server_addr = (options['addr'],int(options['port']))
httpd = http.server.HTTPServer(server_addr, Handler)
httpd.handle_request()
httpd.server_close()
