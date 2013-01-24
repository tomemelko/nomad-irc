#Loosely modeled from: http://www.osix.net/modules/article/?id=780
import sys
import socket 
from functools import partial
import threading
import time
import markov
import random
import os
import cPickle as pickle

#Config
host = 'localhost'
port = 6667
nick = 'nomad'
ident = 'nomadbot'
realname = 'nomadbot'
owner = 'tom'
channel = '\#nomad'
srcdir = "srctxt/"
pickledtablepath = "table.pkl"
pickledaddedfile = "loadedfiles.pkl"
filesimported = False
files = os.listdir(srcdir)
loadedfiles = []
table = {}
refreshinterval = 5
sentencecount = 1000

if os.path.isfile(pickledaddedfile):
  print "Found loaded file table"
  with open(pickledaddedfile, 'r') as fp:
    loadedfiles = pickle.load(fp)

if os.path.isfile(pickledtablepath):
  print "Found pickled table"
  with open(pickledtablepath, 'r') as fp:
    table = pickle.load(fp)
    
for file in files:
  if file not in loadedfiles:
    print "Importing:",srcdir+file
    table.update(markov.load(srcdir+file))
    loadedfiles.append(file)
    filesimported = True
  
if (filesimported):
  with open(pickledtablepath, 'w') as fp:
    print "Dumping table..."
    pickle.dump(table, fp, 2) 
  with open(pickledaddedfile, 'w') as fp:     
    print "Dumping loaded file list"
    pickle.dump(loadedfiles, fp, 2) 

  
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
          if "nomad" in message.lower() or "nomad:" in line:
            if sender == owner and "quit" in message:
              print "Recieved quit command"
              exit()
            print sender,"says",message
            response = markov.generate(sentencecount, table)
            while len(response) == 0:
              response = markov.generate(sentencecount, table)
            s.send('PRIVMSG #nomad '+response[random.randint(0,sentencecount)]+'\r\n')

#Connect to server and listen
s = socket.socket()
time.sleep(1)
listener = threading.Thread(target=partial(listen, s))
listener.start()
s.connect((host, port))
time.sleep(2)
print "Sending USER",ident,host,"bla :",realname
s.send('USER '+ident+' '+host+' bla :'+realname+'\r\n') #Identify to server 
print "Sending NICK",nick
s.send('NICK ' + nick + "\r\n")
time.sleep(2)
print "Joining channel"
s.send('JOIN #nomad \r\n')

while listener.isAlive():
  time.sleep(refreshinterval)
