#!/usr/bin/env python
#! -*- encoding: utf-8 -*-
# Diego Ros y Aitana Villaplana y Pau Sanchez

import re
import sys
import os
import json
from SAR_library import *
from nltk.stem import SnowballStemmer
#import pdb; pdb.set_trace()
from time import time

#Herramienta para stemming
stemmer = SnowballStemmer('spanish')


def syntax():
    print ("\n%s index_directory [-q=query] [-s]" % sys.argv[0])
    sys.exit()

def processArgs():
    if len(sys.argv) > 0:
        index = sys.argv[1]
        ix = load_object(index)
        stem = False
        if len(sys.argv) == 2:
            searchCmd(ix, stem)

        if len(sys.argv) >= 3:
            #Editado para aceptar el parametro -s
            param = sys.argv
            for p in param:
                if p.find("-s") >= 0:                        
                    stem = True
                    break
            if param[2].find("-q=") >= 0:
                query = param[2].split("=")
                query = query[1]

                
                resolver_consultas(ix, query, stem )
            else:
                searchCmd(ix, stem)

            
        else:
            syntax()
    else:
        syntax()

def Dict_to_tupla(dic):
    tuplas = []
    for i in dic.keys():
        valor = dic.get(i,0)
        tuplas.append((i, valor))
    return tuplas

def searchCmd(ix, stem):  
    while True:
        text = input("Dime:")
        if len(text) == 0:
            sys.exit()
        #Editado para aceptar el parametro -s
        else:
            resolver_consultas(ix, text, stem)

#Stemming es un parametro booleano para determinar si esta consulta es con stemming
def resolver_consultas(indice, consulta, stemming):
 
    consulta = consulta.lower()
    consulta = " ( ".join(consulta.split("("))
    consulta = " ) ".join(consulta.split(")"))
    consulta = consulta.split(" ")
    doc_ids = indice[1]
    resultado = []
    aux=[]

    parentesis =False


    #Juntar palabras en array que deberian estar juntas dado un ''
    i = 0
    while i<len(consulta):
        if consulta[i] is not "":
            aux.append(consulta[i])
        if consulta[i].count('"')==1:
            auxi = i
            while i < len(consulta)-1:
                i += 1
                if consulta[i].find('"') >= 0:
                    auxc = consulta[auxi:i+1]
                    aux[auxi] = " ".join(auxc)
                    break
                if i==len(consulta):
                    print ('No puedes escribir un unico " para hacer busqueda posicional')
                    sys.exit()
        i+=1       

    i=0
    while i < len(aux):
        temp = bucle(aux,resultado,i,parentesis,indice,doc_ids,stemming)
        resultado=temp[0]
        i=temp[1]
    
    resultado = list(set(resultado))
    #(resultado, pesos) = ordenar_relevancia(indice[9], resultado, consulta)
    
    mostrar_consultas(doc_ids,resultado,aux,indice,stemming)#,pesos)
    return 0

def busca_adicional(indice,consulta,steaming):
    if consulta.find("%") >= 0:
        consulta = consulta.split("%")
        num =int (consulta[1])
        consulta = consulta[0]
        print(num)
        time1 = time()
        sol = levesteinTree_Word_PD(consulta,indice[10],num)
        time2 = time() - time1
        print(time2)
            
    elif consulta.find("@") >= 0:
        consulta = consulta.split("@")
        num =int( consulta[1])
        consulta = consulta[0]
        
        time1 = time()
        sol = Dict_to_tupla(dam_levesteinTrie_Word_Ramificacion(consulta,indice[10],num))
        time2 = time() - time1
        print(time2)    
    else:
        return busca_adicional1(indice,consulta,steaming)                                                                 
    res=[]
    for i in sol:
        print(i[0])
        res=or_op( busca_adicional1(indice,i[0],steaming) , res)
    return res
    

def busca_adicional1(indice, consulta,steaming):
    resultado = []
    
    if not steaming or '"' in consulta:
        if not":" in consulta:
            if not '"' in consulta:
                resultado= indice[0].get(consulta,[])
                if  len(resultado)>0 :
                    resultado=resultado.keys()
            else:
                resultado = busca_posicional(indice[0], consulta)
        else:
            consult = consulta.split(":")
            busqueda = consult[0]
            consulta = consult[1]
            if busqueda == "title":
                if not '"' in consulta:
                    resultado= indice[3].get(consulta,[])
                    if  len(resultado)>0 :
                        resultado=resultado.keys()
                else:
                    resultado=busca_posicional(indice[3],consulta)
            elif busqueda == "summary":                
                if not '"' in consulta:
                    resultado= indice[4].get(consulta,[])
                    if  len(resultado)>0 :
                        resultado=resultado.keys()
                else:
                    resultado=busca_posicional(indice[4],consulta)
            elif busqueda == "keywords":
                resultado = indice[5].get(consulta, [])
            elif busqueda == "date":
                resultado = indice[6].get(consulta, [])
            elif busqueda == "article":
                if not '"' in consulta:
                    resultado= indice[3].get(consulta,[])
                    if  len(resultado)>0 :
                        resultado=resultado.keys()
                else:
                    resultado=busca_posicional(indice[3],consulta)
            else:
                print("Sólo se permiten búsquedas con: title, summary, keywords, date, article")
                sys.exit()
    else:
        if not":" in consulta:
            resultado = get_stems(consulta, indice[2], indice[0])
        else:
            consult = consulta.split(":")
            busqueda = consult[0]
            consulta = consult[1]
            if busqueda == "title":
                resultado = get_stems(consulta, indice[7], indice[3])
            elif busqueda == "summary":
                resultado = get_stems(consulta, indice[8], indice[4])
            elif busqueda == "keywords":
                resultado = indice[5].get(consulta, [])
            elif busqueda == "date":
                resultado = indice[6].get(consulta, [])
            elif busqueda == "article":
                resultado = get_stems(consulta, indice[2], indice[0])
            else:
                print("Sólo se permiten búsquedas con: title, summary, keywords, date, article")
                sys.exit()

    if len(resultado)>0:
        resultado= sorted(resultado) 
    #print(resultado)   
    return resultado

#busquedas posicionales

def busca_posicional(indice,consulta):
    consulta = consulta.split(" ")
    consulta[0] = consulta[0][1:]
    lc = len(consulta)
    lp = len(consulta[lc-1])
    consulta[lc-1] = consulta[lc-1][:lp-1]
    resultado=[]
    dic=dict()
    i = 1
    dic[consulta[0]]= indice.get(consulta[0], {})
    docs = dic.get(consulta[0], {})
    if len(docs.items()) != 0:
        docs = sorted(docs.keys())
    else: 
        docs = []

    while i<len(consulta):
        dic[consulta[i]]= indice.get(consulta[i], {})
        doc = dic.get(consulta[i], {})
        if len(doc.items()) != 0:
            doc = sorted(doc.keys())
        else: 
            doc = []
        docs= and_op(docs,doc)
        i+=1

    for elem in docs:
        for pos_ini in sorted(dic[consulta[0]].get(elem, [])):
            i=1
            cont=True
            while i<len(consulta) and cont:
                cont=False
                for pos in sorted(dic[consulta[i]].get(elem, [])):
                    if pos == pos_ini + i:
                        i+=1
                        cont=True
                        break
                    elif pos_ini < pos:
                        break
            if cont:
                resultado.append(elem)
                break
    return resultado

def bucle(consulta,resultado,i,parentesis,indice,doc_ids,stemming_c):
    while True:
        temp=[]
        while consulta[i]=="(" :
            i+=1
        term = consulta[i]

        if term == "not":
            if consulta[i+1]=="(" :
                aux=bucle(consulta,[],i+2,True,indice,doc_ids,stemming_c)
                i=aux[1]
                resultado = not_op(aux[0], doc_ids)
            else:
                aux=busca_adicional(indice,consulta[i + 1],stemming_c)
                resultado = not_op(aux, doc_ids)
                i+=2
        elif term == "and":
            if consulta[i+1]=="not":
                if consulta[i+2]=="(" :
                    aux=bucle(consulta,[],i+3,True,indice,doc_ids,stemming_c)
                    i=aux[1]
                    resultado = and_op(resultado, not_op(aux[0], doc_ids))
                else:
                    aux=busca_adicional(indice,consulta[i+2],stemming_c)
                    temp = not_op(aux, doc_ids)
                    resultado = and_op(resultado, temp)
                    i+=3
            elif consulta[i+1]=="(" :
                aux=bucle(consulta,[],i+2,True,indice,doc_ids,stemming_c)
                i=aux[1]
                resultado = and_op(resultado, aux[0])
            else:
                aux=busca_adicional(indice,consulta[i + 1],stemming_c)
                resultado = and_op(resultado, aux)
                i+=2
        elif  term == "or":
            if consulta[i+1]=="not":
                if consulta[i+2]=="(" :
                    aux=bucle(consulta,[],i+3,True,indice,doc_ids,stemming_c)
                    i=aux[1]
                    resultado = or_op(resultado, not_op(aux[0], doc_ids))
                else:
                    aux=busca_adicional(indice,consulta[i+2],stemming_c)
                    temp= not_op(aux, doc_ids)
                    resultado = or_op(resultado, temp)
                    i+=3
            elif consulta[i+1]=="(" :
                aux=bucle(consulta,[],i+2,True,indice,doc_ids,stemming_c)
                i=aux[1]
                resultado = or_op(resultado, aux[0])
            else:
                aux=busca_adicional(indice,consulta[i + 1],stemming_c)
                resultado = or_op(resultado, aux)
                i+=2   
        elif consulta[i]!=")":
            resultado=busca_adicional(indice,consulta[i],stemming_c)
            i+=1
        if len(consulta)== i:
            break
        if consulta[i]==")":
            i+=1
            break
        if not parentesis :
            break
    return (resultado,i)

def get_stems(word, stems, dic_terminos):
    resultado = []
    for w in stems.get(stemmer.stem(word), []):
        aux=dic_terminos.get(w,{})
        if(len(aux.keys())>0):
            resultado += aux
    if len(resultado)>0:
        return sorted(list(set(resultado)))
    return resultado

def and_op(lista1, lista2):
    resultado = []
    i=j=0
    while i<len(lista1) and j < len(lista2):
        if(lista1[i]==lista2[j]):
            resultado.append(lista1[i])
            i+=1
            j+=1
            continue
        if(lista1[i]<lista2[j]):
            i+=1
        else:
            j+=1 
    return resultado

def or_op(lista1, lista2):
    resultado = []
    i=j=0
    while i<len(lista1) and j < len(lista2):
        if(lista1[i]==lista2[j]):
            resultado.append(lista1[i])
            i+=1
            j+=1
            continue
        if(lista1[i]<lista2[j]):
            resultado.append(lista1[i])
            i+=1
            continue
        else:
            resultado.append(lista2[j])
            j+=1
            continue
    resultado.extend(lista1[i:])
    resultado.extend(lista2[j:])
    resultado = list(set(resultado))
    if len(resultado)>0:
        resultado= sorted(resultado)
    return resultado

def not_op(lista, dic):
    resultado = list(dic.keys())
    for elem in lista:
        resultado.remove(elem)
    return resultado

#NO SE USA
"""
def ordenar_relevancia(pesos, resultado, consulta):
    aux = []
    res = []
    peso = 0.0
    for doc in resultado:
        for term in consulta:tolerancia
            if term not in "and, or, not":
                floatt = float(pesos[term].get(doc, 0))
                peso += floatt
        j = 0
        aux.append((peso, doc))
    aux.sort(reverse=True) #Ordena al reves de forma que los primeros son los mas grandes
    res = [i[1] for i in aux] #Coge el segundo elemento de la lista de tuplas
    return (res, aux)
"""

def mostrar_consultas(docs, lista, consulta,index,stemming):#, pesos):
    cont = 0
    print("")
    print("==================================================================")
    print("Resultados para la consulta:", " ".join(consulta))
    print("==================================================================")
    print("")

    for id in lista:
        item = docs.get(id, 0)
        path = item[2]
        pos = item[1]
        noticia = load_json(path)

        fecha = noticia[pos].get("date")
        titular = noticia[pos].get("title")
        key = noticia[pos].get("keywords")
        art = noticia[pos].get("article")

        #relevancia = 0
        #for p,d in pesos:
        #    if d == id:
        #        relevancia = p

        if(len(lista) <= 2):
            print("Title: ",titular)
            print("Date: ",fecha)
            print("Keywords: ",key)
            print("")
            print(art)
            print("")
            print("")

        if(len(lista) >= 3 and len(lista) <= 5):
            print("Title: ",titular)
            print("Date: ",fecha)
            print("Keywords: ",key)
            print("Relevancia: ", relevancia)
            print("Contexto: ", snippet(art, consulta,id,index,stemming))
            print("")

        if(len(lista) > 5):
            print("Title: ",titular,"Date: ",fecha,"Keywords: ",key)
            cont+=1
            if(cont == 10): break

    print("===========")
    print(len(lista)," results")

    return 0

def snippet(art, query,idArt,index,stemming):
    aux=[]
    steam=[]
    pos=[]
    for j in query:
        if j is not "(" and j is not ")":
            if not ":" in j or "article:" in j:
                if idArt in busca_adicional(index,j,stemming):
                    if '"' in j:
                        pos.append(j)
                    elif stemming:
                        for w in index[2].get(stemmer.stem(j), []):    
                            steam.append(w)
                    else:
                        aux.append(j)
    if len(steam) > 0:
        aux=steam

    snippet = ""
    art = clean_frase(art)
    art = art.split(" ")
    for p in pos:
        consulta = p.split(" ")
        consulta[0] = consulta[0][1:]
        lc = len(consulta)
        lp = len(consulta[lc-1])
        consulta[lc-1] = consulta[lc-1][:lp-1]
        for i in range(0, len(art)):
            c=1
            if art[i]==consulta[0] and i + len(consulta)<=len(art):
                a=True
                for j in range(i+1, i + len(consulta)):
                    if art[j]!= consulta[c]:
                        a=False
                        break
                    c+=1  
                if a:
                    snippet += "..." + " ".join(art[max(0, i - 3):min(len(art), i + c + 3)]) + "...\n"

    if len(aux)>0:
        for i in range(0, len(art)):
            if art[i] in aux:
                snippet += "..." + " ".join(art[max(0, i - 3):min(len(art), i + 4)]) + "...\n"
    elif len(pos) ==0 :
        art=art[0:min(len(art),100)]
        snippet= " ".join(art) + " ...\n"
    return snippet



if __name__ == "__main__":
    if len(sys.argv) < 2:
        syntax()
    processArgs()