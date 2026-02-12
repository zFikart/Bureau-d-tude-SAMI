import matplotlib.pyplot as plt
import numpy as np
import random as rd


def glouton(list) :
    n = len(list)
    newList = [list [0]]
    list.remove(list [0])
    point = (0, 0)
    for pos in range (0, n-1) :
        point = list[0]
        min = dist(newList[pos], list[0])
        for j in range (len(list)) :
            if dist(newList[pos], list[j]) < min :
                min = dist(newList[pos], list[j])
                point  = list[j]
        newList.append(point)
        list.remove(point)
    plt.clf()
    X = [newList[i][0] for i in range (len(newList))]+[newList[0][0]]
    Y = [newList[i][1] for i in range (len(newList))]+[newList[0][1]]
    plt.plot(X,Y)
    plt.grid()
    plt.show()
    return newList








def dist(A, B) :
    return ((A[0]-B[0])**2 + (A[1]-B[1])**2)**(1/2)




liste = []
for i in range (15) :
    liste.append((rd.randint(0,5),rd.randint(0,4) ))

print(glouton(liste))
