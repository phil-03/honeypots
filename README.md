# Honeypots
### Just another honeypot repository...

## About this project
This project is an attempt at emulating protocols FTP and HTTP. You can utilize 
fail2ban for logging and iptables to set your packet filtering rules.
Installation and setup for those tools will not be included in this setup.
The http program only receives GET and POST request. The ftp honeypot is intended to
be a one and done pot. Meaning that a user will try to connect and the client is alerted
only after one attempt. Remember to set your email with the ftp.py to the correct address
and install your MTA.


## Prerequisites
* Python3
* MTA - mail or postfix(if you prefer- additional changes necessary)
* iptables-persistent (optional)
* fail2ban (optional)

## Configuration
Simply clone the repository to you intended directory:
`git clone https://github.com/phil-03/honeypots.git`

## Running the honeypots
You can run these programs locally via two terminals, for remote configuration you may need to make additional
changes. Keep in mind if you use iptables, you need to set your restrictions to all tcp input 
and make sure you whitelist your ip address.

# Protocol USAGE:
## FTP 
`python3 ftp.py`

## HTTP
`Usage: ./honeypot-http
       ./honeypot-http 0.0.0.0:8000`

Two HTTP methods are currently recognized: `GET` and `POST`

### TODO:
* Add multithreading for ftp
* Add honeypot
* Add keylogger functionality
