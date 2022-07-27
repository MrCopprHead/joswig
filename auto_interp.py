#automatic interpolation of a soap scenario
#involving the Lunar Gateway
#using the temporal Joswig alg
#Jacob Cleveland Summer 2022

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate,optimize
import t_joswig as tj
import math

griddata = interpolate.griddata

'''
Function that takes in two alternative
path lengths and returns values on the hypersurface
'''
def hypersurface(len1, len2, xnew, interps):
    result = 0
    result += len1[0] - len2[0] #add on constants
    for param in len1[1:]:
        ind = int(param[1])
        result += interps[ind](xnew)
    for param in len2[1:]:
        ind = int(param[1])
        result -= interps[ind](xnew)
    return result

'''
Function that takes a list of path lengths
to a single destination vertex, evaluates
the polynomial for certain parameter values,
and checks if the point is within epsilon of
the tropical hypersurface
'''
def border(plens, param_vals, epsilon):
    result = False
    evaluated_poly = []
    for path_length in plens:
        tot = path_length[0]
        for term in path_length[1:]:
            index = int(term[1])
            tot += param_vals[index - 1] #x1 in 0, x2 in 1, etc
        evaluated_poly.append(tot)
    m = min(evaluated_poly)
    count = 0
    for l in evaluated_poly:
        if abs(m-l)<epsilon:
            count += 1
            if count == 2:
                result = True
                break
    return result

'''
Function that takes a list of path lengths
to a single destination vertex, evaluates
the polynomial for certain parameter values,
and returns the minimal path length
'''
def minPoly(plens, param_vals):
    result = plens[0]
    evaluated_poly = []
    for path_length in plens:
        tot = path_length[0]
        for term in path_length[1:]:
            index = int(term[1])
            tot += param_vals[index - 1] #x1 in 0, x2 in 1, etc
        evaluated_poly.append(tot)
    m = min(evaluated_poly)
    i = evaluated_poly.index(m)
    result = plens[i]
    return result

'''
************************
READING IN DATA FROM CSV
************************
'''
#open and read the file after the appending:
fil = open("gatewayDistances.csv", "r")
x = []
a = fil.readline()
while(a != ""):
    x.append(a)
    a = fil.readline()

times = []
params = []
numParams = 0
line = x[1]
vals = line.split('\n')[0]
other = vals.split(',')
numParams = len(other) - 1
for i in range(0,numParams):
    params.append([])
 
for line in x[1:]:
    vals = line.split('\n')[0]
    other = vals.split(',')
    times.append(int(other[0])) #column from csv corresponding to time stamps
    params[0].append(float(other[3])) #WSNM
    params[1].append(float(other[5])) #TDRS3
    params[2].append(float(other[1])) #GSFC
    params[3].append(float(other[4])) #TDRS13
    params[4].append(float(other[7])) #TDRS7
    params[5].append(float(other[2])) #GRGT
    params[6].append(float(other[6])) #TDRS5

fil.close()

'''
*******************************
PARAMETRIC GRAPH INITIALIZATION
*******************************
'''
vert = tj.Vertex.vertices

up = 8 #total number of vertices
for i in range(0,up):
    tj.Vertex("v"+str(i))

vert[0].add(vert[1],'x1')  #adding in edges
vert[0].add(vert[2],'x2')
vert[0].add(vert[3],'x3')
vert[0].add(vert[4],'x4')
vert[0].add(vert[5],'x5')
vert[0].add(vert[6],'x6')
vert[0].add(vert[7],'x7')
vert[1].add(vert[2],39719)
vert[1].add(vert[3],2773)
vert[1].add(vert[6],10878)
vert[1].add(vert[7],40018)
vert[2].add(vert[1],39719)
vert[2].add(vert[3],38116)
vert[2].add(vert[4],27631)
vert[2].add(vert[5],77513)
vert[2].add(vert[7],72626)
vert[3].add(vert[1],2773)
vert[3].add(vert[2],38116)
vert[3].add(vert[4],40544)
vert[3].add(vert[6],12756)
vert[4].add(vert[2],27631)
vert[4].add(vert[3],40544)
vert[4].add(vert[5],62654)
vert[4].add(vert[7],82377)
vert[5].add(vert[2],77513)
vert[5].add(vert[4],62654)
vert[5].add(vert[6],39523)
vert[5].add(vert[7],67977)
vert[6].add(vert[1],10878)
vert[6].add(vert[3],12756)
vert[6].add(vert[5],39523)
vert[6].add(vert[7],38344)
vert[7].add(vert[1],40018)
vert[7].add(vert[2],72626)
vert[7].add(vert[4],82377)
vert[7].add(vert[5],67977)
vert[7].add(vert[6],38344)

cpath = []
paths = tj.dfs3(vert[0],cpath) #generate paths
weights = tj.genWeights(paths) #generate corresponding list of lists of weights

tot = []
for path in paths[1:]:
    vertex = path[-1]
    vpath = []  #list of all paths ending with vertex
    vweight = [] #list of weights of those paths
    for otherPath in paths[1:]:
        if(otherPath[-1] == vertex):
            vpath += [otherPath]
            i = paths.index(otherPath)
            if(i!=-1):
                vweight += [weights[i-1]]
    tot.append([[vpath],[vweight]])

reducedTotal = []
for line in tot:
    grok = tj.reduce(line[1][0])
    temp = []
    for h in grok:
        i = line[1][0].index(h)
        temp += [line[0][0][i]]
    if(not([temp,grok] in reducedTotal)):
        reducedTotal += [[temp,grok]]
       
totCount = 0 #number of bits needed for trees
for line in reducedTotal:
    count = len(line[0])
    count = math.ceil(math.log(count,2))
    totCount += count

'''
***********************
PARAMETER INTERPOLATION
***********************
'''
beg = 0
end = len(x) - 2
f1 = interpolate.interp1d(times,params[0],'cubic')
f2 = interpolate.interp1d(times,params[1],'cubic')
f3 = interpolate.interp1d(times,params[2],'cubic')
f4 = interpolate.interp1d(times,params[3],'cubic')
f5 = interpolate.interp1d(times,params[4],'cubic')
f6 = interpolate.interp1d(times,params[5],'cubic')
f7 = interpolate.interp1d(times,params[6],'cubic')

xnew = np.arange(30*beg,30*end,15)

interps = [0,f1,f2,f3,f4,f5,f6,f7]

length_pairs = []
target_number = len(reducedTotal)
for count in range(0,target_number):
    top = len(reducedTotal[count][1])
    for i in range(0,top):
        for j in range(i+1,top):
            pair = [reducedTotal[count][1][i],reducedTotal[count][1][j]]
            length_pairs.append(pair)

#print(len(length_pairs))

'''
***********
ROOTFINDING
***********
'''
roots = []
samples = 2000
start = xnew[0]
end = xnew[-1]
diff = (end-start)/(1.*samples)
for lpair in length_pairs:
    t2 = start+diff
    val = hypersurface(lpair[0],lpair[1],t2,interps)
    pair = [val,val]
    for i in range(1,samples):
        t2 = start+i*diff
        t1 = t2-diff
        val = hypersurface(lpair[0],lpair[1],t2,interps)
        pair = [pair[1],val]
        if(np.sign(pair[0]) != np.sign(pair[1])):
            avg = int((t2+t1)/2)
            if(not(avg in roots)):
                for count in range(0,target_number):
                    path_lengths = reducedTotal[count][1]
                    vals = []
                    for interpolant in interps[1:]:
                        vals.append(interpolant(avg))
                    if border(path_lengths,vals,60):
                        roots.append(avg)

roots.sort()

'''
********************************
TREE LABELING AND ROOT REDUCTION
********************************
'''
time_table = []
roots = [0] + roots
for i in range(0,len(roots)-1):
    sample = int((roots[i]+roots[i+1])/2)
    treenumber = 0
    for count in range(0,target_number):
        path_lengths = reducedTotal[count][1]
        vals = []
        for interpolant in interps[1:]:
            vals.append(interpolant(sample))
        monomial = minPoly(path_lengths,vals)
        num = path_lengths.index(monomial)
        num=int(math.pow(16,count)*num)
        treenumber += num
    s = f"0x{treenumber:07x}"
    print(f"{roots[i]:05}",s)
    time_table.append([roots[i],treenumber])

reduced_table = [time_table[0]]
for i in range(0,len(time_table)-1):
    if(time_table[i][1] != time_table[i+1][1]):
        reduced_table.append(time_table[i+1])

print(len(time_table),len(reduced_table))
for entry in reduced_table:
    print(f"{entry[0]:05}",f"0x{entry[1]:07x}")
