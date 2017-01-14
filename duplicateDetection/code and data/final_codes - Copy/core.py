import pygraph 
import preproc as pp
from gensim import corpora, models, similarities
import hashlib
import numpy as np
import os
import math
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search

grc = graph()
grt = graph()
exacts = graph()
bitdict = dict()

def tobedeleted(id1, id2):
    return id1
    
def create_bitdict(l):
    global bitdict
    for i in range(0,l):
        bitdict[i] = 1
    
def cosinesim(x,y):
    magx = 0
    magy = 0
    for i in range(0,len(x)):
        magx+= x[i]**2
    for i in range(0,len(y)):
        magy+= y[i]**2

    denominator = math.sqrt(magy*magx)
    sum = 0
    for i  in range(0,len(x)):
        sum+= x[i]*y[i]
        
    return sum/denominator
    
def ham_dist(fing1, fing2):
    sim = 0
    for i, bit1 in enumerate(fing1):
        if bit1==fing2[i]:sim+=1
    return sim    

#pass this function a sorted array of fingers, the cur list of docs and the dictionary object. It returns the updated list
# def update(sorted_finger, dict, tht1, tht2, tht3, thc, lsi):
    # global gr, bitdict
    # for i, finger in enumerate(sorted_finger):
        # if i==len(sorted_finger)-1:break
        # if(ham_dist(sorted_finger[i], sorted_finger[i+1])>tht1):
            # l1 = dict[sorted_finger[i]]
            # l2 = dict[sorted_finger[i+1]]

            # if ham_dist(sorted_finger[i], sorted_finger[i+1]) < tht2:#conceptual duplicates
                # for id1 in l1:
                    # for id2 in l2:
                        # #print "cosine",cosinesim(lsi[id1], lsi[id2])
                        # if cosinesim(lsi[id1], lsi[id2])>thc:
                            # #print "Cosine similar:",l1,l2
                            # bitdict[id1] = 0
                            # bitdict[id2] = 0 #no more uniques
                            # if not grc.has_node(id1):
                                # grc.add_node(id1)
                                
                            # if not grc.has_node(id2):
                                # grc.add_node(id2) 
                                
                            # if not(grc.has_edge((id1,id2))):
                                # grc.add_edge((id1,id2))
                        
            # elif ham_dist(sorted_finger[i], sorted_finger[i+1])>tht3:#exact duplicates
                # for id1 in l1:
                    # for id2 in l2:
                        # if not exacts.has_node(id1):
                            # exacts.add_node(id1)
                            
                        # if not exacts.has_node(id2):
                            # exacts.add_node(id2) 
                            
                        # if not(exacts.has_edge((id1,id2))):
                            # exacts.add_edge((id1,id2))
                # i = 0
                # cur1 = l1[0]
                # while i<len(l1)-1:
                    # tbd = tobedeleted(cur1, l1[i+1])
                    # if tbd==cur1:
                        # cur1 = l1[i+1]
                    # if(bitdict.has_key(tbd)):
                        # bitdict.pop(tbd)
                    # i+=1
                    
                # i = 0
                # cur2 = l2[0]
                # while i<len(l2)-1:
                    # tbd = tobedeleted(cur2, l2[i+1])
                    # if tbd==cur2:
                        # cur2 = l2[i+1]
                    # if(bitdict.has_key(tbd)):
                        # bitdict.pop(tbd)
                    # i+=1    
                
                # if l1!=l2:    
                    # tbd = tobedeleted(cur1, cur2)
                    # if(bitdict.has_key(tbd)):
                        # bitdict.pop(tbd)
            
            # else:#near duplicates
                # #print "Similarity ", ham_dist(sorted_finger[i], sorted_finger[i+1])
                # for id1 in l1:
                    # for id2 in l2:
                        # #print id1, id2,'->', ham_dist(sorted_finger[i], sorted_finger[i+1]),
                        # bitdict[id1] = 0
                        # bitdict[id2] = 0 #no more uniques
                        # if not grt.has_node(id1):
                            # grt.add_node(id1)
                            
                        # if not grt.has_node(id2):
                            # grt.add_node(id2) 
                            
                        # if not(grt.has_edge((id1,id2))):
                            # grt.add_edge((id1,id2))             

def update(sorted_finger, dict, tht1, tht2, tht3, thc, lsi):
    global gr, bitdict
    for i, finger in enumerate(sorted_finger):
        if i==len(sorted_finger)-1:break
        l1 = dict[sorted_finger[i]]
        l2 = dict[sorted_finger[i+1]]
        if((ham_dist(sorted_finger[i], sorted_finger[i+1])>tht2) and (ham_dist(sorted_finger[i], sorted_finger[i+1])<=tht3)):    
            for id1 in l1:
                    for id2 in l2:
                        #print id1, id2,'->', ham_dist(sorted_finger[i], sorted_finger[i+1]),
                        bitdict[id1] = 0
                        bitdict[id2] = 0 #no more uniques
                        if not grt.has_node(id1):
                            grt.add_node(id1)
                            
                        if not grt.has_node(id2):
                            grt.add_node(id2) 
                            
                        if not(grt.has_edge((id1,id2))):
                            grt.add_edge((id1,id2))             
            
                
                        
        elif ham_dist(sorted_finger[i], sorted_finger[i+1])>tht3:#exact duplicates
                for id1 in l1:
                    for id2 in l2:
                        if not exacts.has_node(id1):
                            exacts.add_node(id1)
                            
                        if not exacts.has_node(id2):
                            exacts.add_node(id2) 
                            
                        if not(exacts.has_edge((id1,id2))):
                            exacts.add_edge((id1,id2))
                i = 0
                cur1 = l1[0]
                while i<len(l1)-1:
                    tbd = tobedeleted(cur1, l1[i+1])
                    if tbd==cur1:
                        cur1 = l1[i+1]
                    if(bitdict.has_key(tbd)):
                        bitdict.pop(tbd)
                    i+=1
                    
                i = 0
                cur2 = l2[0]
                while i<len(l2)-1:
                    tbd = tobedeleted(cur2, l2[i+1])
                    if tbd==cur2:
                        cur2 = l2[i+1]
                    if(bitdict.has_key(tbd)):
                        bitdict.pop(tbd)
                    i+=1    
                
                if l1!=l2:    
                    tbd = tobedeleted(cur1, cur2)
                    if(bitdict.has_key(tbd)):
                        bitdict.pop(tbd)
            
        else:
            for id1 in l1:
                for id2 in l2:
                    #print "cosine",cosinesim(lsi[id1], lsi[id2])
                    if cosinesim(lsi[id1], lsi[id2])>thc:
                        #print "Cosine similar:",l1,l2
                        bitdict[id1] = 0
                        bitdict[id2] = 0 #no more uniques
                        if not grc.has_node(id1):
                            grc.add_node(id1)
                            
                        if not grc.has_node(id2):
                            grc.add_node(id2) 
                            
                        if not(grc.has_edge((id1,id2))):
                            grc.add_edge((id1,id2))
                            
#following method to be called for each doc - return fingerprint 
def get_fingerprint(shingles, binhash_value, dictionary, tfidf, shingleSize):#tfidf, binhash_value of a particular document to be sent while iterating in a for loop just as they did
   
    fingerprint = initialize()
    for i in range(len(binhash_value)): #for each shingle
        temp_id = []
        tfidf_arr = []
        for j in range(shingleSize):
            temp_id.insert(j, dictionary.token2id[shingles[i][j].lower()])
    
        for j in range(shingleSize):
            temp_tfidf = pp.get_tfidf(temp_id[j], tfidf)
            if temp_tfidf==None:
                temp_tfidf = 0
            tfidf_arr.insert(j, temp_tfidf)
        
        wt = sum(tfidf_arr)/len(tfidf) #reducing impact of length of the document
        for j in range(64):
            if binhash_value[i][j]=='1':
                fingerprint[j]+=wt 
            else:
                fingerprint[j]-=wt
    return fingerprint

#method to initialize... :(
def initialize():
    temp = []
    for i in range(64):
        temp.append(0)
    return temp    

def convert2bin(x):
    for docn in range(len(x)):
        for shinglen in range(len(x[docn])):
            if x[docn][shinglen]>0:
                x[docn][shinglen]=1
            else:
                x[docn][shinglen]=0
    return x

def dec(x):
    sum = 0
    for i in range(len(x)):
        sum+=(2**(len(x)-i-1))*x[i]
    return sum

def convert2dec(x):
    for i in range(len(x)):
        x[i] = dec(x[i])
    return x

def compact(x):
    y = []
    for i, doc in enumerate(x):
        temp = ""
        for bit in doc:
            temp+=str(bit)
        y.insert(i, temp)
    return y    

def create_dict(x):    
    d = {}
    for i, ele in enumerate(x):
        d.setdefault(ele,[]).append(i)  
    return d

def rotate(fingList, dict, tht1, tht2, tht3, thc, lsi):
    create_bitdict(len(lsi))
    temp = []
    for times in range(64):
        for i, doc in enumerate(fingList):
            strin = doc[1:len(doc)] #rotation!
            strin+=doc[0]
            fingList[i] = strin
        dict = create_dict(fingList)
        update(sorted(fingList), dict, tht1, tht2, tht3, thc, lsi)
    

def fine_preprocessor(doc):
    stoplist = '. , ( ) : / \ ~ @ the so and or to for in is on from of as that ? 0 1 2 3 4 5 6 7 8 9 ; - < > { } ! = # $ % ^ & * [ ] + - * ^ " " ' ' ` '.split()
    tempDoc = ''
    for char in doc:
        if char not in stoplist:
            tempDoc+=char
    return tempDoc;
    
def getShingles(docAdd, shingle_len):
    shingles = [] 
    for i in range(len(docAdd)):
        tempDoc = ''
        with open(docAdd[i]) as f:
            for line in f:
                tempDoc+=line
        the_string = tempDoc #extracting ith document
        the_string = fine_preprocessor(the_string)
        temp = the_string.split() #removing spaces from doc
        
        stoplist = '. , ~ ( ) : / \ ~ @ the so and or to for in a is on from of as that ? ; - < > { } ! = # $ % ^ & * [ ] + - * ^ " " ' ' ` '.split()
        
        tokens = []
        for z in temp:    
            if z.lower() not in stoplist:
                tokens.append(z)
              
        shingles.insert(i, []) #another initialization
        for j in range(len(tokens) - shingle_len + 1): #actual shingling
            #if(len(tokens[j])<3): #allowing shingles to start with stop words who
            shingles[i].append(tokens[j:j + shingle_len])
      
    #print shingles[0]
    return shingles

def getHash(shingles, shingleSize):
    hashValues = []
    for docn in range(len(shingles)):
        temp = []
        for shinglen in range(len(shingles[docn])): #how many shingles
            string = ''
            for i in range(shingleSize):
                string+= (shingles[docn][shinglen][i] + ' ')
            string = string[0:len(string)-1] #removing last extra space
            temp.append(hashlib.sha1(string).hexdigest()[0:16])
        hashValues.insert(docn, temp)     
    return hashValues    
    
def getBin(hashValues):
    binhash = []
    scale = 16
    num = 64
    for docn in range(len(hashValues)):#over all the d
        temp = []
        for shinglen in range(len(hashValues[docn])):#number of shingles in a doc
            temp_bin = bin(int(hashValues[docn][shinglen], scale))[2:].zfill(num) #Considering first 64 bits...
            temp.append(temp_bin)
        binhash.append(temp)
    return binhash    
  
