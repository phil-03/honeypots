#!/usr/bin/env python3

#Simple Python http honeypot
#Functions
#->Logging, alerting, banning via firewall api
#
#
#Usage: ./honeypot-http
#       ./honeypot-http 0.0.0.0:8000


from http.server import SimpleHTTPServer, BaseHTTPRequestHandler
from sys import argv
import SocketServer
import os
import logging

BIND_HOST = 'localhost'
PORT = 8000

web_dir = os.path.join(os.path.dirname(__file__), 'web')
os.chdir(web_dir)
#Start out with simple http webserver


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):#Listen for GET req
        self.write_response(b'')

    def do_POST(self): #Listen for POST req
        content_length = int(self.header.get('content-length', 0)) #echo out header
        body = self.rfile.read(content_length) #echo body

        self.write_response(body)

    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)

        print(self.headers)
        print(content.decode('utf-8')) #Print info back to console


class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        logging.error(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self): #Listen for POST req
        logging.error(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_POST(self)

Handler = GetHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

#Parse cmdline args
if len(argv) > 1:
    arg = argv[1].split(':')
    BIND_HOST = arg[0]
    PORT = int(arg[1])


printf(f'Listening on http://{BIND_HOST}:{PORT}\n')
buffer=1
sys.stderr = open('http.log', 'w', buffer)
httpd = HTTPServer((BIND_HOST, PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()


