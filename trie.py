#import numpy as np
# Diego Ros y Aitana Villaplana, Pau Sanchez y Javier Garrido
from node import *

class Trie:

    def __init__(self):
        self.nodes = list()
        self.nodes.append(Node(0))
        self.size = 0
        self.finalList = list()

    def getNodes(self):
        return self.nodes

    def getNode(self, ind):
        return self.nodes[ind]

    def add_son(self, chr): #0 se ha anyadido, 1 se ha encontrado, 2 se ha encontrado pero previamente no era final
        letras = list(chr)
        i = 0
        aux = self.nodes[0]
        for i in range(len(letras)):
            if aux.sons.get(letras[i], 0) == 0:        
                
                
                break                                                       #Mientras existan ramas con la letra, se seguiran recorriendo y no se detendra el metodo.
            else:
                aux = aux.sons[letras[i]]                                            #Se continua explorando el trie en busca de un nodo con todas las letras y final.
            if i == (len(letras) - 1) and aux.final and aux.chr == letras[i]:                                 #Si se encuentra un nodo con todas las letras, este es final y 
                    return 1                                                                          #la letra del nodo es la ultima, no se modifica el trie, pues existe ya en este                                    
            elif i == (len(letras) - 1) and not aux.final and aux.chr == letras[i]:
                aux.final = True
                aux.palabra = chr
                self.finalList.append(aux.ind)
                return 2

        for j in range(i, len(letras)):     
            self.size += 1                                                                    #Se anyaden todos los nodos necesarios si no se encuentra uno que tenga la palabra
            if j != len(letras)-1:
                d = aux.getDepth()
                aux.sons[letras[j]] = Node(self.size, letras[j], d+1, aux, False, None)
            else:
                d = aux.getDepth()
                aux.sons[letras[j]] = Node(self.size, letras[j], d+1, aux, True,chr)
                self.finalList.append(aux.sons[letras[j]].ind)                #Si es la ultima letra, sera nodo final y su chr sera la palabra.
            
            self.nodes.append(aux.sons[letras[j]])
            aux = aux.sons[letras[j]]

        return 0

    def toString(self):
        #print(self.size, self.finalList)
        print(self.size)

    










