#Loosely modeled from: http://www.osix.net/modules/article/?id=780
import sys
import socket 
import thread 
import time

def listen(socketInUse):
  while True:
    line = socketInUse.recv(4096)
    if line != "":
      if line != "\r\n":
        print line
        line = line[line.rfind(':')+1:-2]
        print line
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
thread.start_new_thread(listen, (s,))
s.connect((host, port))
time.sleep(2)
print "Sending USER",ident,host,"bla :",realname
s.send('USER '+ident+' '+host+' bla :'+realname+'\r\n') #Identify to server 
time.sleep(5)
print "Sending NICK",nick
s.send('NICK ' + nick + "\r\n")
time.sleep(5)
print "Joining channel"
s.send('JOIN #nomad \r\n')

while True:
  pass
