#!/usr/bin/python3

#Simple Python http honeypot
#Functions
#->Logging, alerting, banning via firewall iptables
#
#
#Usage: ./honeypot-http
#       ./honeypot-http 0.0.0.0:8000
#
#Kill Python process cmd: kill -9 $(ps -A | grep python | awk '{print $1}')


from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv
from socketserver import ThreadingMixIn
import os
import sys
import logging
import threading


USE_HTTPS = True
BIND_HOST = '0.0.0.0'
PORT = 8000

web_dir = os.path.join(os.path.dirname(__file__), 'data')
os.chdir(web_dir)

#Start out with simple http webserver

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        #if self.path == '/':
         #   self.path = '/index.html'
        self.write_response(b'')
        logging.error(self.headers)
        #self.wfile.write(b'Hello Bro\t' +threading.currentThread().getName().encode() + b'\t')
        self.wfile.write(bytes("<html><head><p>Parse error: syntax error, unexpected end of file in /home/pbutts/public_html/wp-content/themes/mycommerce/pro_framework/local.php on line 812</p></head></html>","utf-8")) 
       
    
    def do_POST(self): #Listen for POST req
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        body = self.rfile.read(content_length) #echo body
    
        logging.error(self.headers)
        self.wfile.write(bytes("<html><head><p>Parse error: syntax error, unexpected end of file in /home/pbutts/public_html/wp-content/themes/mycommerce/pro_framework/local.php on line 812</p></head></html>","utf-8"))
        
        self.write_response(body)
    

    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)

        print(self.headers)
        print(content.decode('utf-8')) #Print info back to console
    


#For continuous streaming it is better to use sockets via BaseHTTPServer
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass




def runServer():
    print(f'Listening on http://{BIND_HOST}:{PORT}\n')
    buffer=1
    sys.stderr = open('http.log', 'w', buffer)
    server = ThreadingSimpleServer((BIND_HOST, PORT), GetHandler)
    #if USE_HTTPS:
     #   import ssl
      #  server.socket = ssl.wrap_socket(server.socket, keyfile='./key.pem', certfile='./cert.pem', server_side=True)
    server.serve_forever()

#Establish self-signed cert: openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 


if __name__ == '__main__':

    #Parse cmdline args
    if len(argv) > 1:
        arg = argv[1].split(':')
        BIND_HOST = arg[0]
        PORT = int(arg[1])
        runServer()

    else:
        runServer()

