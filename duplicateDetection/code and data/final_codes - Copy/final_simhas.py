from gensim import corpora, models, similarities
import os
import simhash
texts = []
count = 0
def getfiles(directory):
    list = []
    for dirpath,dirnames,files in os.walk(directory):
        for file in files:
            #if file.endswith("*"):
                temp = os.path.join(dirpath,file)
                list.append(temp)
    return list
    #u might want to change the way 'texts' are generated...
def getdocs(fileaddresses):   
    global texts
    stoplist = '. , ( ) : / \ ~ @ the so and or to for in a is on from of as that ? ; - < > { } ! = # $ % ^ & * [ ] + - * ^ " " ' ' ` '.split()
    for i, address in enumerate(fileaddresses):
        tempDoc = ''
        with open(address) as f:
            for line in f:
                tempDoc+=line
        texts.insert(i, [])
        doc = ''
        for word in tempDoc.lower().split():
            if word not in stoplist:
               doc+=word+' ' 
        texts[i].append(doc)
  
#pass this function a sorted array of fingerprints, the cur list of docs and the dictionary object. It returns the updated list  
finallist = []

def process():
    global count
    global finallist
    i = 0
    j = 0
    while i<len(texts):
        j = i + 1
        while j<len(texts):
            count+=1
            s1 = simhash.Simhash(texts[i])
            s2 = simhash.Simhash(texts[j])
            if s1.distance(s2) < 3:
                if i not in finallist:
                    finallist.append(i)
                if j not in finallist:
                    finallist.append(j)
            j+=1
        i+=1
    
    print finallist
        
        
def top(threshold):
    directory = "D:\\users\\pravin\\Downloads\\20_newsgroups\\My dataset"
    filelist = getfiles(directory)
    
    f = open('D:\\filelist.txt','w')
    
    for i, file in enumerate(filelist):
        f.write(str(i)+' '+file[len(directory):len(file)]+'\n')
    f.close()
    
    getdocs(filelist)
   
    process()
    
    print len(finallist)
    #print count
    f = open('D:\\simhash.txt','w')
    f.write((str)(finallist))
    f.close()
    
    
def main():
    top(46)
if __name__=="__main__": main()
