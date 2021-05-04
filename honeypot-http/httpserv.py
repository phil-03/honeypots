#!/usr/bin/python3

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

import time, threading, socket, SocketServer, BaseHTTPServer

BIND_HOST = 'localhost'
PORT = 8000

web_directory = os.path.join(os.path.dirname(__file__), 'data')
os.chdir(web_directory)
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

'''class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path != '/':
            self.send_error(404, "Object not found")
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # serve up an infinite stream
        i = 0
        while True:
            self.wfile.write("%i " % i)
            time.sleep(0.1)
            i += 1

# Create ONE socket.
addr = ('', 8000)
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(addr)
sock.listen(5)

# Launch 100 listener threads.
class Thread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.i = i
        self.daemon = True
        self.start()
    def run(self):
        httpd = BaseHTTPServer.HTTPServer(addr, Handler, False)

        # Prevent the HTTP server from re-binding every handler.
        # https://stackoverflow.com/questions/46210672/
        httpd.socket = sock
        httpd.server_bind = self.server_close = lambda self: None

        httpd.serve_forever()
[Thread(i) for i in range(100)]
time.sleep(9e9) '''


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


