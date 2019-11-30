#!/usr/bin/env python
#! -*- encoding: utf-8 -*-
# Diego Ros, Aitana Villaplana, Pau Sanchez

import sys
import os
import json
import pickle
from SAR_library import *
from nltk.stem import SnowballStemmer
import math
from operator import itemgetter
import glob
from trie import *

#Herramienta para stemming
stemmer = SnowballStemmer('spanish')


def fun(doc,index):

    terminos= dict()
    documentos = dict()
    #Declaro diccionario de stems
    stems = dict()

    titles = dict()
    summary = dict()
    keywords = dict()
    dates = dict()

    title_stems = dict()
    summary_stems = dict()

    peso_terminos = dict()

    trie = Trie()

    docid=0
    newid=0
    dats = []
    N = 0

    for dirname,_,files in os.walk(doc):
        N += len(files)                     #sacar el num de noticias (N)

    for dirname,_,files in os.walk(doc):
        for filename in files:
            name = os.path.join(dirname,filename)
            lista = load_json(name)
            pos=0
            for dic in lista:
                art = dic["article"]
                palabras = clean_frase(art).lower().split(" ")
                for i in range(0, len(palabras)):
                    p = palabras[i]
                    trie.add_son(p)
                    if p is not "":
                    #Stemming 0.1
                        stword = stemmer.stem(p)
                        stset = stems.get(stword, [])
                        stset.append(p)
                        stems[stword] = stset
                    #Stemming End                                    

                    #posing posicional
                        terminos[p] = terminos.get(p, {})
                        if newid not in terminos[p].keys():
                            terminos[p][newid] = terminos[p].get(newid,[i]) 
                        else:
                            terminos[p][newid].append(i)
            
                
                for p in palabras:
                    if p is not "":
                        tf = 1 + math.log10(len(terminos[p][newid]))   #frec del termino en el doc
                        idf = math.log10(N/len(terminos[p].keys()))   #N/num de docs que contienen el termino (N = numero de noticias)
                        w = tf + idf   
                        w = "{0:.4f}".format(w)                                     #pesado tfxidf, truncado a 4 decimales

                        peso_terminos[p] = peso_terminos.get(p, {})
                        peso_terminos[p][newid] = w                     #diccionario donde el término tiene un peso en cada doc en el que aparece
                        
                        
                suma = dic["summary"]
                summarys = clean_frase(suma).lower().split(" ")
                for i in  range(0,len(summarys)):
                    s = summarys[i]
                    trie.add_son(s)
                    if s is not "":
                    #Stemming 0.1
                        stword = stemmer.stem(s)
                        stset = summary_stems.get(stword, [])
                        stset.append(s)
                        summary_stems[stword] = stset
                    #Stemming End

                    #posing posicional
                        summary[s] = summary.get(s, {})
                        if newid not in summary[s].keys():
                            summary[s][newid] = summary[s].get(newid,[i]) 
                        else:
                            summary[s][newid].append(i)

                key = dic["keywords"]
                keys = clean_frase(key).lower().split(",")
                keys = " ".join(keys)
                keys = keys.split(" ")
                for t in keys:
                    trie.add_son(t)
                    keywords[t] = keywords.get(t, [])
                    if(newid  not in keywords[t]):
                        keywords[t].append(newid)

                tit = dic["title"]
                titulos = clean_frase(tit).lower().split(" ")
                for i in range(0, len(titulos)):
                    t=titulos[i]
                    trie.add_son(t)
                    if t is not "":
                    #Stemming 0.1
                        stword = stemmer.stem(t)
                        stset = title_stems.get(stword, [])
                        stset.append(t)
                        title_stems[stword] = stset
                    #Stemming End

                    #posing posicional
                        titles[t] = titles.get(t, {})
                        if newid not in titles[t].keys():
                            titles[t][newid] = titles[t].get(newid,[i]) 
                        else:
                            titles[t][newid].append(i)
                
                dat = dic["date"]
                dats.append(dat)
                for t in dats:
                    dates[t] = dates.get(t, [])
                    if(newid  not in dates[t]):
                        dates[t].append(newid)
                        
                
                documentos[newid]= documentos.get(newid, (docid,pos,name))
                pos+=1
                newid+=1
                dats = []
            docid+=1
    print(newid,len(terminos.keys()))
    #Guarda también stems
    save_object((terminos,documentos,stems,titles,summary,keywords,dates,title_stems,summary_stems,peso_terminos,trie),index)



clean_f = re.compile('\W+')
def clean_frase(text):
    return clean_f.sub(' ', text)

def syntax():
    print ("\n%s doc_directory index_directory" % sys.argv[0])
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        syntax()
    fun(sys.argv[1],sys.argv[2])