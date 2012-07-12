#Loosely modeled from: http://www.osix.net/modules/article/?id=780
import sys
import socket 
from functools import partial
import threading
import time

def listen(socketInUse):
  while True:
    line = socketInUse.recv(4096)
    if line != "":
      if line != "\r\n":
        print line
        if "PING" in line:
          print "PONG"
          socketInUse.send("PONG\r\n")
        if "PRIVMSG" in line:
          sender = line[1:line.find('!')]
          line = line[line.rfind(':')+1:-2]
          print sender,"says",line
        if "quit" in line:
          exit()

#Config
host = 'localhost'
port = 6667
nick = 'nomad'
ident = 'nomadbot'
realname = 'nomadbot'
owner = 'tom'
channel = '\#nomad'
readbuffer = ''

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
  pass
