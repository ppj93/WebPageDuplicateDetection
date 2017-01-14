from gensim import corpora, models, similarities
import hashlib
import re
import numpy as np
import os
corpus = []

def getfiles(directory):
    list = []
    i=0
    
    for dirpath,dirnames,files in os.walk(directory):
        for file in files:
            #if file.endswith(".txt"):
                temp = os.path.join(dirpath,file)
                list.append(temp)
    return list
   
def fine_preprocessor(doc):
    stoplist = '. , ( ) : / \ ~ @ the so and or to for in is on from of as that ? 0 1 2 3 4 5 6 7 8 9 ; - < > { } ! = # $ % ^ & * [ ] + - * ^ " " ' ' ` '.split()
    tempDoc = ''
    for char in doc:
        if char not in stoplist:
            tempDoc+=char
    return tempDoc;

def filter(tempdoc):
    out = ''
    for i in tempdoc:
	match = re.match(r'[a-zA-Z]', i)
	if match or i==' ' or i=='\n':
		out+=i
    
    return out
    
def getDict(fileaddresses):
    texts = []
    stoplist = '. , ( ) : / \ ~ @ the so and or to for in a is on from of as that ? ; - < > { } ! = # $ % ^ & * [ ] + - * ^ " " ' ' ` '.split()
    #stoplist = set(''.split())
    for i, address in enumerate(fileaddresses):
        tempDoc = ''
        with open(address) as f:
            for line in f:
                tempDoc+=line
        #tempDoc = filter(tempDoc)
        tempDoc = fine_preprocessor(tempDoc)
        texts.insert(i, [])
        for word in tempDoc.lower().split():
            if word not in stoplist:
                texts[i].append(word)
     
    global corpus
    corpus = [(corpora.Dictionary(texts)).doc2bow(doc) for doc in texts]   
    return corpora.Dictionary(texts)            
    
def get_tfidf(id, tfidf): #tfidf here represents the doc
    for i in tfidf:
        if i[0]==id:
            return i[1]