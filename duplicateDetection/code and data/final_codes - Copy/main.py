import preproc as pp
import core as ts
import graphplotter
from gensim import corpora, models, similarities
import lsi
import numpy as np
from pygraph.algorithms.accessibility import *
corpus = []
import stats
def connected_comp(gr):
    temp_dic =  mutual_accessibility(gr)
    conn_comp = []
    for i in temp_dic:
        if conn_comp.count(temp_dic[i])==0:
            conn_comp.append(temp_dic[i])
    return conn_comp
    
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
    return corpora.Dictionary(texts) 
    
def top(shingleSize, tht1, tht2, tht3, thc):
    directory = "D:\\users\\pravin\\Downloads\\20_newsgroups\\My dataset"
    filelist = pp.getfiles(directory)
    print filelist
    dictionary = pp.getDict(filelist)
    dictionary1 = getDict(filelist)
    f = open('D:\\files.txt','w')
    
    for i, file in enumerate(filelist):
        f.write(str(i)+' '+file[len(directory):len(file)]+'\n')
    f.close()
    print "now you may open the file"
    matrix = lsi.termDocMat(corpus, len(dictionary1), len(filelist))
    U, s, V = np.linalg.svd(matrix, full_matrices=False)
    corpus_lsi = s*(V.transpose()).tolist()   
    
    tfidf = models.TfidfModel(pp.corpus)
    corpus_tfidf = tfidf[pp.corpus]
    list_shingles = ts.getShingles(filelist, shingleSize)
    #print list_shingles
    hash_values = ts.getHash(list_shingles, shingleSize)
    binhash_values = ts.getBin(hash_values)
    fingerprints = []
    
    for i, doc in enumerate(corpus_tfidf): #term wise ordering
        temp = ts.get_fingerprint(list_shingles[i], binhash_values[i], dictionary, doc, shingleSize)
        fingerprints.append(temp)
        
    
    fingerprints = ts.convert2bin(fingerprints)
    temp_cip = fingerprints #temp cluster input
    comp_fings = ts.compact(fingerprints)
    fing_dict = ts.create_dict(comp_fings)
    ts.rotate(comp_fings, fing_dict, tht1, tht2, tht3, thc, corpus_lsi)

    f = open('D:\\textual.txt','w')
    f.write(str(connected_comp(ts.grt)))
    f.close()
    f = open('D:\\conceptual.txt','w')
    f.write(str(connected_comp(ts.grc)))
    f.close()
    f = open('D:\\exacts.txt','w')
    f.write(str(connected_comp(ts.exacts)))
    f.close()
    #print "connected - componentsn conceptual", connected_comp(ts.grc)
    #print "connected - componentsn textual", connected_comp(ts.grt)

def main():
    #top(2, 16, 44, 57, 0.85)
    #top(2, 16, 46, 57, 0.85) #50 by 7
    #top(2, 16, 46, 57, 0.80) #53 false positives: arnd 11
    #top(2, 16, 46, 57, 0.80)#recall decreases drastically if u change 46 to some lower value
    # top(4, 16, 40, 57, 0.80)
    # top(4, 16, 42, 57, 0.80)
    # top(4, 16, 44, 57, 0.80)
    top(3, 16, 46, 57, 0.80)
    # top(3, 16, 46, 57, 0.80)
    # top(4, 16, 50, 57, 0.80)
    
if __name__=="__main__": main()
