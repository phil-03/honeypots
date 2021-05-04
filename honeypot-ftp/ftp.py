#Simple ftp honeypot
import socket
import atexit

# Local IP/Port for the honeypot to listen on (TCP)
LHOST = '0.0.0.0'
LPORT = 21

# Remote IP/Port to send the log data to (TCP)
RHOST = '192.168.X.X'
RPORT = 7000

# Banner displayed needs to be vulnerable service
BANNER = 'Server\nName: '

# Socket timeout in seconds
TIMEOUT = 10


