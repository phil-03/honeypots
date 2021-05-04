#!/usr/bin/python3

#Simple Python http honeypot
#Functions
#->Logging, alerting, banning via firewall api
#
#
#Usage: ./honeypot-http
#       ./honeypot-http 0.0.0.0:8000


#Handle Python2/3 import error
try:
   
    import http.server as SimpleHTTPServer
    import http.server as BaseHTTPServer
    import http.server as BaseHTTPRequestHandler
    import socketserver as SocketServer
    import socketserver as ThreadingMixIn
    import threading
except ImportError:
    
    import SimpleHTTPServer
    import BaseHTTPServer
    import SocketServer

#from http.server import SimpleHTTPServer, BaseHTTPRequestHandler
from sys import argv
#import SocketServer
import os
import logging


USE_HTTPS = True
BIND_HOST = 'localhost'
PORT = 8000

web_directory = os.path.join(os.path.dirname(__file__), 'data')#find html page?
os.chdir(web_directory)

#Start out with simple http webserver

class GetHandler(http.server.SimpleHTTPRequestHandler):#SimpleHTTPServer

    def do_GET(self):
        self.write_response(b'')
        #if self.path == '/':
            #self.path = 'mywebpage.html'
        logging.error(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self): #Listen for POST req
        content_length = int(self.header.get('content-length', 0)) #echo out header
        body = self.rfile.read(content_length) #echo body
        self.write_response(body)
        logging.error(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_POST(self)

    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)

        print(self.headers)
        print(content.decode('utf-8')) #Print info back to console



#For continuous streaming it is better to use sockets via BaseHTTPServer
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


#Handler = GetHandler
#httpd = SocketServer.TCPServer(("", PORT), Handler)



#Parse cmdline args
if len(argv) > 1:
    arg = argv[1].split(':')
    BIND_HOST = arg[0]
    PORT = int(arg[1])


#Start Server
#printf(f'Listening on http://{BIND_HOST}:{PORT}\n')
#buffer=1
#sys.stderr = open('http.log', 'w', buffer)
#httpd = HTTPServer((BIND_HOST, PORT), SimpleHTTPRequestHandler)
#httpd.serve_forever()

def runServer():
    #printf(f'Listening on http://{BIND_HOST}:{PORT}\n')
    buffer=1
    sys.stderr = open('http.log', 'w', buffer)
    server = ThreadingSimpleServer(('0.0.0.0', 4444), GetHandler)
    if USE_HTTPS:
        import ssl
        server.socket = ssl.wrap_socket(server.socket, keyfile='./key.pem', certfile='./cert.pem', server_side=True)
    server.serve_forever()

#Establish self-signed cert: openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 


if __name__ == '__main__':
    runServer()

