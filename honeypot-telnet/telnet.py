#simple telnet honeypot

import socket
import atexit

# Local IP/Port for the honeypot to listen on (TCP)
LHOST = '0.0.0.0'
LPORT = 23

# Remote IP/Port to send the log data to (TCP)
RHOST = '192.168.X.X'
RPORT = 7000

# Banner displayed needs to be vulnerable service
BANNER = 'Server\nName: '

# Socket timeout in seconds
TIMEOUT = 10

def main():
    print '[*] Honeypot starting on ' + LHOST + ':' + str(LPORT)
    atexit.register(exit_handler)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((LHOST, LPORT))
    listener.listen(5)
    while True:
        (insock, address) = listener.accept()
        insock.settimeout(TIMEOUT)
        print '[*] Honeypot connection from ' + address[0] + ':' + str(address[1]) + ' on port ' + str(LPORT)
        try:
            insock.send(BANNER)
            data = insock.recv(1024)
        except socket.error, e:
            sendLog(address[0],'Error: ' + str(e))
        else:
            sendLog(address[0],data)
        finally:
            insock.close()

def sendLog(fromip, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((RHOST, RPORT))
    s.send('IP:' + fromip + ' Port:' + str(LPORT) + ' | ' + message.replace('\r\n', ' '))
    s.close()

def exit_handler():
    print '\n[*] Honeypot is shutting down!'
    listener.close()

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass