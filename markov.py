## http://code.activestate.com/recipes/194364/ (r3)
import random;
import sys;

nonword = "\n" # Since we split on whitespace, this can never be a word
sentenceend = (".","?","!")
w1 = nonword
w2 = nonword

# GENERATE TABLE
table = {}

def load(filepath):
  w1 = w2 = nonword
  for line in open(filepath):
    for word in line.split():
      table.setdefault( (w1, w2), [] ).append(word)
      w1, w2 = w2, word
  table.setdefault( (w1, w2), [] ).append(nonword) # Mark the end of the file

def generate(files, number):                    
  for file in files:
    load(file)
  # GENERATE OUTPUT
  w1 = nonword
  w2 = nonword

  sentence = []
  sentences = []
  #for i in xrange(maxwords):
  while len(sentences) < number:
    newword = random.choice(table[(w1, w2)])
    if newword == nonword: sys.exit()
    if newword[-1] in sentenceend:
      joined = " ".join(sentence)
      if len(joined) > 1:
        sentences.append(joined+" "+newword)
        sentence = []
    else:
      sentence.append(newword)    
    w1, w2 = w2, newword
  return sentences
