import sys 
import socket 
import string 

#Config
host = '127.0.0.1'
port = '6667'
nick = 'NOMAD'
ident = 'nomadbot'
realname = 'nomadbot'
owner = 'tom'
channel = '\#nomad'
readbuffer = ''

#Connect to server and identify
s = socket.socket()
s.connect(host, port)
s.send('NICK ' + nick + 'n')
s.send('USER ' + ident + ' ' + host + ' bla :' + realname + 'n')
