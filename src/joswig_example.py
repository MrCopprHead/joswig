#Jacob Cleveland Summer 2022

import t_joswig as tj
import math

Vertex = tj.Vertex
dfs3 = tj.dfs3
genWeights = tj.genWeights
reduce = tj.reduce
printPaths = tj.printPaths

vert = Vertex.vertices #create label for list of vertices

up = 6 #total number of vertices
for i in range(0,up):
    Vertex("v"+str(i))

vert[0].add(vert[1],'x2')  #adding in edges
vert[0].add(vert[2],'x1')
vert[0].add(vert[3],4)
vert[2].add(vert[1],2)
vert[2].add(vert[3],5)
vert[3].add(vert[1],1)
vert[1].add(vert[3],3)
vert[1].add(vert[4],7)
vert[3].add(vert[4],'x3')
vert[1].add(vert[5],2)
vert[3].add(vert[5],2)

cpath = []
paths = dfs3(vert[0],cpath) #generate paths

weights = genWeights(paths) #generate corresponding list of lists of weights

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
    grok = reduce(line[1][0])
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
    printPaths(line[0])
    print(line[1])
    
length_pairs = []
target_number = len(reducedTotal)
for count in range(0,target_number):
    top = len(reducedTotal[count][1])
    for i in range(0,top):
        for j in range(i+1,top):
            pair = [reducedTotal[count][1][i],reducedTotal[count][1][j]]
            length_pairs.append(pair)

print(len(length_pairs))
