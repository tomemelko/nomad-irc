#Loosely modeled from: http://www.osix.net/modules/article/?id=780
import sys
import socket 
from functools import partial
import threading
import time

#Config
host = 'localhost'
port = 6667
nick = 'nomad'
ident = 'nomadbot'
realname = 'nomadbot'
owner = 'tom'
channel = '\#nomad'
readbuffer = ''

def listen(socketInUse):
  while True:
    line = socketInUse.recv(4096)
    if line != "":
      if line != "\r\n":
        if "PING" in line:
          socketInUse.send("PONG\r\n")
        if "PRIVMSG" in line:
          sender = line[1:line.find('!')]
          message = line[line.rfind(':')+1:-2]
          if sender == owner and message == "quit":
            exit()
          print sender,"says",message
          s.send('PRIVMSG #nomad Hello everybody!\r\n')

#Connect to server and listen
s = socket.socket()
listener = threading.Thread(target=partial(listen, s))
listener.start()
s.connect((host, port))
time.sleep(2)
print "Sending USER",ident,host,"bla :",realname
s.send('USER '+ident+' '+host+' bla :'+realname+'\r\n') #Identify to server 
print "Sending NICK",nick
s.send('NICK ' + nick + "\r\n")
time.sleep(5)
print "Joining channel"
s.send('JOIN #nomad \r\n')

while listener.isAlive():
  time.sleep(5)
