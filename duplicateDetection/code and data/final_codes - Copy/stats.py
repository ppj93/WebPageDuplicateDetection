import ast
def countduplicates():
    
    ft = open('D:\\textual.txt')
    fc = open('D:\\conceptual.txt')
    fe = open('D:\\exacts.txt')
    fsim = open('D:\\simhash.txt')

    t1 = ft.readlines()
    t2 = fc.readlines()
    t3 = fe.readlines()
    t4 = fsim.readlines()

    lt = ast.literal_eval(t1[0]) #converts strings to list
    lc = ast.literal_eval(t2[0])
    le = ast.literal_eval(t3[0])
    lsim = ast.literal_eval(t4[0])

    # print lt
    # print lc
    # print le
    temp = []

    for i in lc:
        for j in i:
            if j not in temp:
                temp.append(j)

    for i in lt:
        for j in i:
            if j not in temp:
                temp.append(j)

    for i in le:
        for j in i:
            if j not in temp:
                temp.append(j)            

            


    total = len(temp)


    ft.close()
    fsim.close()
    fc.close()
    fe.close()

    return total
   
import ast
ft = open('D:\\textual.txt')
fc = open('D:\\conceptual.txt')
fe = open('D:\\exacts.txt')
fsim = open('D:\\simhash.txt')

t1 = ft.readlines()
t2 = fc.readlines()
t3 = fe.readlines()
t4 = fsim.readlines()

lt = ast.literal_eval(t1[0]) #converts strings to list
lc = ast.literal_eval(t2[0])
le = ast.literal_eval(t3[0])
lsim = ast.literal_eval(t4[0])

# print lt
# print lc
# print le
temp = []

for i in lc:
    for j in i:
        if j not in temp:
            temp.append(j)

for i in lt:
    for j in i:
        if j not in temp:
            temp.append(j)

for i in le:
    for j in i:
        if j not in temp:
            temp.append(j)            

        


total = len(temp)


print "Ours: ",total
print "Simhash: ",len(lsim)


import matplotlib.pyplot as plt
import numpy as np

# x - shingle size #y - number of duplicates    
# Y = [total, len(lsim)]
# pos = np.arange(2)
# width = 1.0
# ax = plt.axes()
# ax.set_xticks(pos + (width / 2))
# ax.set_xticklabels(['Modified', 'Original'])
# ax.set_xlabel('Algorithm')
# ax.set_ylabel('Number of duplicates detected')
# plt.bar(pos, Y, width, color='r')
# plt.show()

ft.close()
fsim.close()
fc.close()
fe.close()
