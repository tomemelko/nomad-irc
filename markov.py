#From: http://code.activestate.com/recipes/194364-the-markov-chain-algorithm/

import random;
import sys;

stopword = "\n" # Since we split on whitespace, this can never be a word
stopsentence = (".", "!", "?",) # Cause a "new sentence" if found at the end of a word
sentencesep  = "\n" #String used to seperate sentences


# GENERATE TABLE
w1 = stopword
w2 = stopword
table = {}

for line in open("/home/tom/nltk_data/corpora/webtext/overheard_modified.txt"):
  for word in line.split():
    if word[-1] in stopsentence:
      table.setdefault( (w1, w2), [] ).append(word[0:-1])
      w1, w2 = w2, word[0:-1]
      word = word[-1]
    table.setdefault( (w1, w2), [] ).append(word)
    w1, w2 = w2, word
    
# Mark the end of the file
table.setdefault( (w1, w2), [] ).append(stopword)
                                             
# GENERATE SENTENCE OUTPUT
maxsentences  = 10
print "Done Reading"                 
w1 = stopword
w2 = stopword
sentencecount = 0
sentence = []

while sentencecount < maxsentences:
  newword = random.choice(table[(w1,w2)])
  if newword == stopword: sys.exit()
  if newword in stopsentence:
    joined = " ".join(sentence)
    if joined != ".":
      if joined != "!":
        if joined != "?":
          print "%s%s%s" % (joined, newword, sentencesep)
          sentencecount += 1
    sentence = []
  else:
    sentence.append(newword)
    w1, w2 = w2, newword

