from gensim import corpora, models, similarities
import hashlib
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy.cluster.vq import kmeans,vq
corpus = []
final = []
def getfiles(directory):
    list = []
    for dirpath,dirnames,files in os.walk(directory):
        for file in files:
            #if file.endswith("*"):
                temp = os.path.join(dirpath,file)
                list.append(temp)
    return list
    #u might want to change the way 'texts' are generated...
def getDict(fileaddresses):
    texts = []
    
    stoplist = '. , ( ) : / \ ~ @ the so and or to for in a is on from of as that ? ; - < > { } ! = # $ % ^ & * [ ] + - * ^ " " ' ' ` '.split()
    for i, address in enumerate(fileaddresses):
        tempDoc = ''
        with open(address) as f:
            for line in f:
                tempDoc+=line
        texts.insert(i, [])
        for word in tempDoc.lower().split():
            if word not in stoplist:
                texts[i].append(word)
     
    global corpus
    corpus = [(corpora.Dictionary(texts)).doc2bow(doc) for doc in texts]
    
    # for i in corpus:
        # print i
        
    return corpora.Dictionary(texts)            
    
  
#pass this function a sorted array of fingerprints, the cur list of docs and the dictionary object. It returns the updated list

temp_out = []
def update(sorted_finger, list, dict, threshold):
    for i, finger in enumerate(sorted_finger):
        if i==len(sorted_finger)-1:break
        if(ham_dist(sorted_finger[i], sorted_finger[i+1])>threshold):
            l1 = dict[sorted_finger[i]]
            l2 = dict[sorted_finger[i+1]]
            if [l1, l2] not in temp_out:
                temp_out.append([l1,l2])
            for id in l1:
                if id not in list:
                    list.append(id)
            for id in l2:
                if id not in list:
                    list.append(id)   
                
    return list  
    
def getShingles(docAdd, shingle_len):
    shingles = [] 
    for i in range(len(docAdd)):
        tempDoc = ''
        with open(docAdd[i]) as f:
            for line in f:
                tempDoc+=line 
        shingles.insert(i, []) #another initialization
        tokens = tempDoc.split() #removing spaces from doc
        stoplist = '. , ( ) : / \ ~ @ the so and or to for in a is on from of as that ? ; - < > { } ! = # $ % ^ & * [ ] + - * ^ " " ' ' ` '.split()
        
        temp = []
        for z in tokens:    
            if z.lower() not in stoplist:
                temp.append(z)
         
              
        for j in range(len(temp) - shingle_len + 1): 
			shingles[i].append(temp[j:j + shingle_len])
    return shingles
    
#following method to be called for each doc - return fingerprint 
def get_fingerprint(shingles, binhash_value, dictionary, tfidf, shingleSize):#tfidf, binhash_value of a particular document to be sent while iterating in a for loop just as they did
    
    fingerprint = initialize()
    for i in range(len(binhash_value)): #for each shingle
        temp_id = []
        tfidf_arr = []
        for j in range(shingleSize):
            temp_id.insert(j, dictionary.token2id[shingles[i][j].lower()])
    
        for j in range(shingleSize):
            temp_tfidf = get_tfidf(temp_id[j], tfidf)
            if temp_tfidf==None:
                temp_tfidf = 0
            tfidf_arr.insert(j, temp_tfidf)
        
        wt = sum(tfidf_arr)
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

def get_tfidf(id, tfidf): #tfidf here represents the doc
    for i in tfidf:
        if i[0]==id:
            return i[1]

def ham_dist(fing1, fing2):
    sim = 0
    for i, bit1 in enumerate(fing1):
        if bit1==fing2[i]:sim+=1
    return sim  
    
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

def rotate(fingList, dict, threshold):
    temp = []
    for times in range(64):
        for i, doc in enumerate(fingList):
            strin = doc[1:len(doc)]
            strin+=doc[0]
            fingList[i] = strin
        dict = create_dict(fingList)
        temp = update(sorted(fingList), temp, dict, threshold)
    
    return temp
    


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

def lsi(l):
    return 0;
    
    
def top(shingleSize, threshold):
    directory = "D:\\users\\pravin\\Downloads\\20_newsgroups\\My dataset"
    filelist = getfiles(directory)
    print filelist
    dictionary = getDict(filelist)
    f = open('D:\\fileList.txt','w')
    
    for i, file in enumerate(filelist):
        f.write(str(i)+' '+file[len(directory):len(file)]+'\n')
    f.close()
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    list_shingles = getShingles(filelist, shingleSize)
   
    hash_values = getHash(list_shingles, shingleSize)
    binhash_values = getBin(hash_values)
    
    fingerprints = []
    
    for i, doc in enumerate(corpus_tfidf): #term wise ordering
        temp = get_fingerprint(list_shingles[i], binhash_values[i], dictionary, doc, shingleSize)
        fingerprints.append(temp)
       
    fingerprints = convert2bin(fingerprints)
    temp_cip = fingerprints #temp cluster input
    comp_fings = compact(fingerprints)
    
    fing_dict = create_dict(comp_fings)
 
    final_list = rotate(comp_fings, fing_dict, threshold)
    final_list.sort()
    f = open('D:\\simhash.txt','w')
    f.write(str(final))
    f.close()
    print temp_out
    print len(final_list)

def main():
    top(1, 46)
if __name__=="__main__": main()
