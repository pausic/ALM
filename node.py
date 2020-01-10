# Diego Ros y Aitana Villaplana, Pau Sanchez y Javier Garrido
class Node:

    def __init__(self, ind, chr="",depth = 0, pre=None, final = False,palabra = None):
        self.ind = ind
        self.chr = chr
        self.pre = pre
        self.sons = {}
        self.final = final
        self.depth = depth
        self.palabra = palabra

    def getPalabra(self):
        return self.palabra

    def esFinal(self):
        return self.final

    def getSons(self):
        return self.sons

    def getChr(self): 
        return self.chr  

    def getDepth(self):
        return self.depth

    def getParent(self):
        return self.pre

    def getIndice(self):
        return self.ind
        

"""
    def getString(self, ind, chr, pre):
        result = ""
        
        for pre in pre.chr 
        Node aux = pre

        result = self.chr + result

        return result
        """