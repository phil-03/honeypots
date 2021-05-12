#Simple ftp honeypo:w
t
import socket
import smtplib
import atexit
from datetime import datetime



# Change to port you will logg data to
RHOST = '192.168.X.X'
RPORT = 8000

# FAKEBAN displayed needs to be vulnerable service
FAKEBAN = '220 vsftpd-2.3.4\nLogin: '

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
       
        (insock, addr) = listen.accept()        
        insock.settimeout(TIMEOUT)
        print('[*] Honeypot connected from ' + addr[0] + ':' + str(addr[1]) + ' on port ' + str(PORT))
       
        try:
            insock.send(FAKEBAN.encode())
            data = insock.recv(2048)
            send_email(addr[0])
        except socket.error as err:
            sendData(addr[0],'Error: ' + str(err))
        else:
            sendData(addr[0],data)
        finally:
            insock.close()
        

def send_email(src_addr):
    """ Send an email if we're scanned / probed on this port """

    sender = 'myself@domain.com'
    receivers = ['philipjb18@gmail.com']


    message = f"""From: FTP server
		To: philipjb18@gmail.com
		MIME-Version: 1.0
		Content-type: text/html
		Subject: Alert! Your honeypot has been triggered by IP: {src_addr}
		"""

    try:
	    smtpObj = smtplib.SMTP('localhost')
	    smtpObj.sendmail(sender, receivers, message)
	    print("Successfully sent email")
    except SMTPException:
	    print("Error: unable to send email")
    
   

def sendData(whos_ip, message):
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
