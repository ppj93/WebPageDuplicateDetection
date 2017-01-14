import numpy as np
    
def termDocMat(corp, diclen, nfiles):
    matrix = np.zeros((diclen, nfiles),"int")
    for i, doc in enumerate(corp):
        j = 0
        for pair in doc:
            if j==pair[0]:
                matrix[j][i] = pair[1]
            else:
                while j<pair[0]:
                    matrix[j][i] = 0
                    j+=1
                matrix[j][i] = pair[1]
            j+=1
        while j<diclen:
            matrix[j][i] = 0
            j+=1
    
    l = matrix.tolist()
    f = open('D:\\svd.txt','w')
    for i in l:
        for j in i:
            f.write(str(j)+'  ')
        f.write('\n')
    f.close()
    return matrix
