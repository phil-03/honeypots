#Simple ftp honeypot
import socket
import atexit
from datetime import datetime



# Remote IP/Port 
RHOST = '192.168.80.131'
RPORT = 8000

# FAKE-BAN displayed needs to be vulnerable service
FAKE-BAN = '220 vsftpd-2.3.4\nLogin: '

# Socket timeout in seconds
TIMEOUT = 10

# Local IP/Port 
HOST = '0.0.0.0'
PORT = 21

def ftp_server():
    print('[*] Honeypot starting on ' + HOST + ':' + str(PORT))
    atexit.register(exit)
    listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen.bind((HOST, PORT))

    listen.listen(5)
    while True:
        (insock, address) = listen.accept()        
        insock.settimeout(TIMEOUT)
        print('[*] Honeypot connected from ' + address[0] + ':' + str(address[1]) + ' on port ' + str(PORT))
        try:
            insock.send(FAKE-BAN.encode())
            data = insock.recv(2048)
        except socket.error as err:
            sendLog(address[0],'Error: ' + str(err))
        else:
            sendLog(address[0],data)
        finally:
            insock.close()
        

def send_email(src_address):
    """ Todo: send an email if we're scanned / probed on this port """
    pass


def sendLog(whos_ip, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((RHOST, RPORT))
    s.send('IP:' + whos_ip + ' Port:' + str(PORT) + ' | ' + message.replace('\r\n', ' '))
    s.close()

         

def exit():
    print('\n[*] Honeypot is shutting down!')
    listen.close()


def getDandT():
	now = datetime.now()
	currentDateTime = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
	return currentDateTime


listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == '__main__':
	print('Starting logging, Date (DD/MM/YY): ' + getDandT() + "\n")
	try:
		ftp_server()
	except KeyboardInterrupt:
		pass