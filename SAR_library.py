#!/usr/bin/env python
#! -*- encoding: utf-8 -*-
# Diego Ros , Aitana Villaplana y Pau Sanchez

from operator import itemgetter
import re
import sys
import random
import pickle
import json
import os
import numpy as np

def save_object(object, file_name): #guardar en disco
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)

def load_object(file_name): #cargar de disco
    with open(file_name, 'rb') as fh:
        obj = pickle.load(fh)
    return obj

#clean_re = re.compile(';|\.|!|\?|\,|"|\'') #eliminar simbolos
#def clean_text(text):
#    return clean_re.split(text)


clean_f = re.compile('\W+')
def clean_frase(text):
    return clean_f.sub(' ', text)


def sort_dic(d): #ordenar diccionario
    for key, value in sorted(d.items(), key=lambda a: (-a[1], a[0])):
        yield key, value

def load_json(f): #cargar json
    with open(f) as fh:
        obj = json.load(fh)
    return obj

def ini_distancia(p1,p2):
    #matriz de ceros
    matrix = np.zeros((len(p1)+1, len(p2)+1), dtype=int)
    coste = 0
    #inicializo fila 0
    matrix[0][0]=0
    for cont in range(1, len(p2)+1):
        
        coste += 1
        matrix[0][cont] = coste
    coste = 0

    #inicilizo columna 0
    for cont in range(1, len(p1)+1):
        coste += 1
        matrix[cont][0] = coste

    return matrix


def distanciaDamLev(p1,p2):
    matrix=ini_distancia(p1,p2)
    #relleno la columna
    p1=" "+p1
    p2=" "+p2
    ini2_DamLev(matrix,p1,p2,1)
    ini2_DamLev(matrix,p2,p1,2)
    for cont in range(2, len(p1)):
        for cont2 in range(2, len(p2)):
            if p1[cont] != p2[cont2]:
                coste = 1
            else:
                coste = 0
    #corta matrix original en matrices 2x2 para sacar el minimo de los 3 casos
            mat = matrix[cont-1:cont+1,cont2-1:cont2+1]
            mat = mat.flatten()
    
    #Sumas coste Sus,Borr, Ins
            mat[0]=mat[0]+coste
            mat[1]=mat[1]+1
            mat[2]=mat[2]+1
    #Anyadir Intercambio
            if p1[cont]==p2[cont2-1] and p1[cont-1]==p2[cont2]:
                mat[3]= matrix[cont-2, cont2-2]+1
            else:
                #me quedo con los 3 primero 3 casos
                mat = mat[:-1]

    #me quedo con el minimo de los 3 casos
            minimun = min(mat)
    #relleno con el resultado
            matrix[cont,cont2] = minimun 
    #devolvemos el ultimo elemento, la distancia minima
    print(matrix)
    return matrix[len(p1)-1,len(p2)-1]
    

def ini2_DamLev(matrix,p1,p2,op):
    for cont in range(1, len(p1)):
        if p1[cont] != p2[1]:
          coste = 1
        else:
            coste = 0
            #corta matrix original en matrices 2x2 para sacar el minimo de los 3 casos
        if op==1:
            mat = matrix[cont-1:cont+1,:2]
        else:
            mat = matrix[:2,cont-1:cont+1]
        
        mat = mat.flatten()
    #me quedo con los 3 primero 3 casos
        mat = mat[:-1]
    #Sumas coste Sus,Borr, Ins
        mat[0]=mat[0]+coste
        mat[1]=mat[1]+1
        mat[2]=mat[2]+1
    #me quedo con el minimo de los 3 casos
        minimun = min(mat)
    #relleno con el resultado
        if op==1:
            matrix[cont,1] = minimun 
        else:
            matrix[1,cont] = minimun    
        
    #devolvemos el ultimo elemento, la distancia minima    

    return matrix

def distanciaLev(p1,p2):
    
    matrix=ini_distancia(p1,p2)
    #relleno la columna
    p1=" "+p1
    p2=" "+p2
    for cont in range(1, len(p1)):
        for cont2 in range(1, len(p2)):
            if p1[cont] != p2[cont2]:
                coste = 1
            else:
                coste = 0
    #corta matrix original en matrices 2x2 para sacar el minimo de los 3 casos
            mat = matrix[cont-1:cont+1,cont2-1:cont2+1]
            mat = mat.flatten()
    #me quedo con los 3 primero 3 casos
            mat = mat[:-1]
    #Sumas coste Sus,Borr, Ins
            mat[0]=mat[0]+coste
            mat[1]=mat[1]+1
            mat[2]=mat[2]+1
    #me quedo con el minimo de los 3 casos
            minimun = min(mat)
    #relleno con el resultado
            matrix[cont,cont2] = minimun 
    #devolvemos el ultimo elemento, la distancia minima
    return matrix[len(p1)-1,len(p2)-1]
    

def levesteinTree_Word_PD(p,trie,tolerancia):
    sol=list()
    p=" "+p
    matrix = np.zeros((len(p), len(trie.nodes)), dtype=int)
    coste = 0
    #inicializo fila 0
    matrix[0][0]=0
    for cont in range(1,len(trie.nodes)):
        
        matrix[0][cont] = trie.getNode(cont).getDepth()

    #inicilizo columna 0
    for cont in range(1, len(p)):
        coste += 1
        matrix[cont][0] = coste
    #relleno la columna
    for cont in range(1, len(p)):
        for cont2 in range(1, len(trie.nodes)): 

            nodo=trie.getNode(cont2) 

            if p[cont] != nodo.getChr() :
                coste = 1
            else:
                coste = 0
    #corta matrix original en matrices 2x2 para sacar el minimo de los 3 casos
            M = np.zeros((1,3), dtype=int)

    #Sumas coste Sus,Borr, Ins
            M[0][0]=matrix[cont-1,cont2]+1
            x = nodo.getParent()
            #no tienen padre 
            M[0][1]=matrix[cont,x.getIndice()]+1
            M[0][2]=matrix[cont-1,x.getIndice()]+coste
    #me quedo con el minimo de los 3 casos
            
            matrix[cont,cont2] = np.amin(M) 
    #devolvemos los elementos con distancia menor a la tolerancia
    for c in trie.finalList:
        dis= matrix[cont,c]
        if dis<=tolerancia:
            sol.append((trie.getNode(c).getPalabra(),dis,c))

    return sol


def dam_levesteinTree_Word_PD(p,trie,tolerancia):
    sol=list()
    p=" "+p
    matrix = np.zeros((len(p), len(trie.nodes)), dtype=int)
    coste = 0
    #inicializo fila 0
    matrix[0][0]=0
    for cont in range(1,len(trie.nodes)):
        matrix[0][cont] = trie.getNode(cont).getDepth()
    #inicilizo columna 0
    for cont in range(1, len(p)):
        coste += 1
        matrix[cont][0] = coste
    #relleno la columna
    for cont in range(1, len(p)):
        for cont2 in range(1, len(trie.nodes)):
            nodo=trie.getNode(cont2)
            if p[cont] != nodo.getChr():
                coste = 1
            else:
                coste = 0
    #corta matrix original en matrices 2x2 para sacar el minimo de los 3 casos
            M = np.zeros((1,4), dtype=int)

    #Sumas coste Sus,Borr, Ins
            M[0][0]=matrix[cont-1,cont2]+1
            x = nodo.getParent()
            #no tienen padre 
            M[0][1]=matrix[cont,x.getIndice()]+1
            M[0][2]=matrix[cont-1,x.getIndice()]+coste
            #Anyadir Intercambio ---------------------------------------------------------------
            if nodo.getDepth() >= 2 and cont >= 2:
                if p[cont]==trie.getNode(cont2).getParent().getChr() and p[cont-1]==trie.getNode(cont2).getChr():
                    M[0][3]= matrix[cont-2, nodo.getParent().getParent().getIndice()]+1
                else:
                    #me quedo con los 3 primero 3 casos --------------------------------------------
                    M = M[0][:-1]
            else:
                M = M[0][:-1]
            #-----------------------------------------------------------------------------------

    #me quedo con el minimo de los 3 casos
            matrix[cont,cont2] = np.amin(M) 
    #devolvemos los elementos con distancia menor a la tolerancia
    for c in trie.finalList:
        dis= matrix[cont,c]
        if dis<=tolerancia:
            sol.append((trie.getNode(c).getPalabra(),dis,c))

    return sol




def levesteinTrie_Word_Ramificacion(p,trie,tolerancia):
    sol = list()
    fifo=list()
    fifo.append((0,0,0))
    coste = 0
    palabra = len(p)-1
    while(len(fifo)>0):
        IndLetra,IndNodo,dis = fifo[0]
        nodo = trie.getNode(IndNodo)
        letra = nodo.getChr()
        fifo.pop(0)
 
        if (dis <= tolerancia):
            if letra == p[IndLetra]:
                coste = 1
            else:
                coste = 0  
            #add solutions 
            if(IndLetra == palabra and nodo.esFinal):
                sol.append((nodo.getPalabra(),dis + coste))
            
            childs = nodo.getSons()
            #Insercion
            if (IndLetra<palabra):
               fifo.append((IndLetra+1,IndNodo,dis+1))
            for c in childs.keys():
                #borrado
                fifo.append((IndLetra,childs[c].getIndice(),dis+1))
                #sustitucion
                if (IndLetra<palabra):
                    fifo.append((IndLetra+1,childs[c].getIndice(),dis+coste))
    return sol


