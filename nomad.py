#Loosely modeled from: http://www.osix.net/modules/article/?id=780
import sys
import socket 
from functools import partial
import threading
import time
import markov
import random
import os

#Config
host = 'localhost'
port = 6667
nick = 'nomad'
ident = 'nomadbot'
realname = 'nomadbot'
owner = 'tom'
channel = '\#nomad'
srcdir = "srctxt/"
files = os.listdir(srcdir)
table = {}
for file in files:
  print "Loading:",srcdir+file
  table.update(markov.load(srcdir+file))
  
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
          response = markov.generate(1000, table)
          while len(response) == 0:
            response = markov.generate(1000, table)
          s.send('PRIVMSG #nomad '+response[random.randint(0,1000)]+'\r\n')

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
