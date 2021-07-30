import joswig_dijkstra as jd
import matplotlib.pyplot as plt
# import numpy as np

# Recursion depth
__depth__ = 10  # make sure the depth isn't too big, high enough accuracy will mess up the decimals

'''
******************
Function totalweight
******************
Given a weighted graph,
returns the sum of all constant
weights.
'''
def totalweight(tree):
    result = 0
    for v in tree.vertices:
        for weight in v.weight:
            if(weight != -1):
                result += weight
    return result

"""
***************
Function equaltree
***************
Given two arrays, x and y,
representing the shortest path
trees one receives as a result
of running Dijkstras,
determines if they are equal
"""
def equaltree(x,y):
    result = True
    for i in range(0, len(x)):
        for j in range(0, len(x[0]) - 1): #minus 1 so that we ignore the weights
            if (x[i][j] != y[i][j]):
                result = False
    return result

def mergeList(L1,L2):
    L1 += L2
    result = []
    for item in L1:
        if(not(item in result)):
            result.append(item)
    return result

'''

'''
def d2treebinary(left,right,slope,yint,interval):
    depth = 10
    buff1 = []
    buff2 = []
    T0.editlink(4,3,left)
    T0.editlink(4,1,slope*left+yint)
    T0.vert_false()
    y = T0.shortestpath(4)
    buff1.append([y,[[left,slope*left+yint]]])
    T0.editlink(4,3,right)
    T0.editlink(4,1,slope*right+yint)
    T0.vert_false()
    y = T0.shortestpath(4)
    buff2.append([y,[[right,slope*right+yint]]])
    buff1 = mergeForest(buff1,buff2)
    treebinary(T0,left,right,depth,buff1,slope,yint)
    result = mergeForest(interval,buff1)
    return result

'''
Assumes that there are only at most two matching trees between F1 and F2;
This can be guaranteed if after each run, it is merged properly.
'''
def mergeForest(F1,F2):
    F1 += F2
    ignore = []
    result = []
    for i in range(0,len(F1)):
        dup = False
        for j in range(0,len(F1)):
            if((i != j) & (not(i in ignore))):
                if(equaltree(F1[i][0],F1[j][0])):
                    dup = True
                    ignore.append(j)
                    # print(ignore)
                    result.append([F1[i][0],mergeList(F1[i][1],F1[j][1])])
        if((not(i in ignore)) & (not(dup))):
            result.append(F1[i])
    return result

"""
************
Function treebinary
************
Performs a recursive binary search on
the parameter space to approximate
the regions of validity for different
shortest path trees.
tree     = graph we wish to search on
left     = left bound of approximation
right    = right bound of approximation
count    = recursion depth
interval = array of trees and sample values
           they are valid on
"""
def treebinary(tree,left,right,count,interval,slope,yint):
    guess = 0.5*(left+right)
    tree.editlink(4,3,guess)
    tree.editlink(4,1,slope*guess+yint)
    tree.vert_false()
    fee = tree.shortestpath(4)
    equal = False
    for foo in interval:
        equal = equaltree(foo[0],fee)
        if(equal):
            # if(foo[1].count(guess) == 0):
            yval = slope*guess+yint
            if([guess,yval] not in foo[1]):
                foo[1].append([guess,yval])
                foo[1].sort()
                interval.sort()
            samples = foo[1]
            end = len(samples) - 1
            ind = interval.index(foo)
            if(guess == foo[1][end][0]): #guess was the biggest in the list
                left = guess
            elif(guess == foo[1][0][0]): #guess was the smallest in the list
                right = guess
            if(count > 0):
                treebinary(tree,left,right,count-1,interval,slope,yint)
            break
    if(not(equal)):
        interval.append([fee,[[guess,slope*guess+yint]]])
        interval.sort()
        treebinary(tree,left,guess,count,interval,slope,yint)
        treebinary(tree,guess,right,count,interval,slope,yint)

T0 = jd.Tree(4)
T0.link(4,1,5)
T0.link(4,3,-1) # -1 denotes a variable edge weight
T0.link(4,2,4)
T0.link(3,1,2)
T0.link(3,2,3)

T0.editlink(4,3,0)
T0.editlink(4,1,14)
T0.vert_false()
x = T0.shortestpath(4)
# print(x)

totw = totalweight(T0)

interval = []
left = 0
right = totalweight(T0)
# print(right)
# right = 10
slope = 1
yint = 0

T0.editlink(4,3,left)
T0.editlink(4,1,slope*left+yint)
T0.vert_false()
x = T0.shortestpath(4)
interval.append([x,[[left,slope*left+yint]]])

intalt = []

T0.editlink(4,3,right)
T0.editlink(4,1,slope*right+yint)
T0.vert_false()
x = T0.shortestpath(4)
intalt.append([x,[[right,slope*right+yint]]])

# print("interval:",interval)
# print("intalt:",intalt)

interval = mergeForest(interval,intalt)

# print("Merged:",interval)

treebinary(T0,left,right,__depth__,interval,slope,yint)

# print("Int:",interval)
# print(len(interval))

left = 0
right = totw
slope = -1
yint = totw
__depth__ = 10
altinterval = []

T0.editlink(4,3,left)
T0.editlink(4,1,slope*left+yint)
T0.vert_false()
x = T0.shortestpath(4)
altinterval.append([x,[[left,slope*left+yint]]])

T0.editlink(4,3,right)
T0.editlink(4,1,slope*right+yint)
T0.vert_false()
x = T0.shortestpath(4)
altinterval.append([x,[[right,slope*right+yint]]])

treebinary(T0,left,right,__depth__,altinterval,slope,yint)
interval = mergeForest(interval,altinterval)

samples = 10 #determines the number of points on each edge that a line is drawn to

for i in range(1,samples): #binary search along lines emanating from each corner
    left = 0
    right = i/float(samples)*totw
    slope = float(samples)/i
    yint = 0
    interval = d2treebinary(left,right,slope,yint,interval)
    right = 23
    slope = i/float(samples)
    yint = 0
    interval = d2treebinary(left,right,slope,yint,interval)

for i in range(1,samples):
    left = 0
    right = totw
    slope = (float(samples)-i)/samples
    yint = i*totw/float(samples)
    interval = d2treebinary(left,right,slope,yint,interval)
    left = i*totw/float(samples)
    right = totw
    slope = float(samples)/(samples-i)
    yint = -(totw*i)/(float(samples)-i)
    interval = d2treebinary(left,right,slope,yint,interval)

for i in range(1,samples):
    left = 0
    right = totw*i/float(samples)
    slope = -float(samples)/i
    yint = totw
    interval = d2treebinary(left,right,slope,yint,interval)
    left = 0
    right = totw
    slope = (i-float(samples))/samples
    yint = totw
    interval = d2treebinary(left,right,slope,yint,interval)

for i in range(1,5):
    left = 0
    right = totw
    slope = -i/float(samples)
    yint = totw*i/float(samples)
    interval = d2treebinary(left,right,slope,yint,interval)
    left = totw*i/float(samples)
    right = totw
    slope = float(samples)/(i-samples)
    yint = -totw*float(samples)/(i-samples)
    interval = d2treebinary(left,right,slope,yint,interval)

print(interval)

fig, ax = plt.subplots()
i = 0
for foo in interval:
    t = []
    s = []
    for vals in foo[1]:
        s.append(vals[0])
        t.append(vals[1])
    ax.scatter(s, t,label = "T"+str(i))
    i+=1

ax.set(
    xlabel='4-3 Edge weight parameter',
    ylabel = '4-1 Edge weight parameter',
    title='Tree regions of validity'
    )
ax.set_xlim(-1,25)
ax.legend()
ax.grid()

plt.tick_params(
    axis="y",
    which="both",
    left=False,
    right=False)

plt.figure(figsize=(20,20),dpi=250)
fig.savefig("test.png")
plt.show()