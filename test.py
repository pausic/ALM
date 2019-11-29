#import numpy as np
from node import *
from trie import *

def start():
    trie = Trie()
    trie.add_son("cas")
    trie.add_son("casas")
    for n in trie.nodes:
        print(n.getIndice(), n.getDepth(), n.getChr())

if __name__ == "__main__":
    start()