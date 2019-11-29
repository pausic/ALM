
##################################################
##                                              ##
##            INDEXADOR DE NOTICIAS             ##
##                   Version -1                 ##
##                                              ##
##              NO OPTIMIZADO !!                ##
## NO se puede utilizar PARA el proyecto de SAR ##
##                                              ##
##################################################

import json
import os
import pickle
import re
import sys
import time

from node import *
from trie import *


def tokenize(text):
    return re.sub("\W+", ' ', text.lower()).split()

def save_object(object, filename):
    with open(filename, 'wb') as fh:
        pickle.dump(object, fh)

def readTXT(filename):
    f = open(filename)
    f = f.read()
    return f

def appendTrie(f):
    files = readTXT(f)
    words = tokenize(files)
    trie = Trie()
    for word in words:
        trie.add_son(word)
    return trie

if __name__ == "__main__": 
    trie = appendTrie("quijote.txt")
    save_object(trie, "resultado")
