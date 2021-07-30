import joswig_dijkstra as jd

'''
***************
Function equaltree
***************
Given two arrays, x and y,
representing the shortest path
trees one receives as a result
of running Dijkstras,
determines if they are equal
'''
def equaltree(x,y):
    result = True
    for i in range(0, len(x)):
        for j in range(0, len(x[0]) - 1): #minus 1 so that we ignore the weights
            if (x[i][j] != y[i][j]):
                result = False
    return result

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

'''
Returns a list of all edges in graph Tree
'''
def edges(Tree):
    result = []
    for v in Tree.vertices:
        if (v.adj != []):
            for vert in v.adj:
                result.append([v, vert])
    return result

'''
Returns a list of all edges represented by tree edgelist
with source node=source
'''
def treeedges(Tree,edgelist):
    result = []
    for e in edgelist:
        init = None
        term = None
        for v in Tree.vertices:
            if(e[0] == v.label):
                term = v
            elif(e[1] == v.label):
                init = v
            if((init != None) & (term != None)):
                result.append([init,term])
                break
    return result

'''
Prints all the paths in a given set of paths
'''
def printpaths(paths):
    for path in paths:
        result = ""
        for v in path:
            if(isinstance(v,jd.Vertex)):
                result += v.label
            else:
                result += str(v)
        print(result)

'''
Returns a list of all paths emanating from the source node.
'''
def edgepaths(edges, base):
    result = []
    for e1 in edges:
        if(e1[0] == base):
            if(not(e1 in result)):
                result.append(e1)
        for e2 in edges:
            if((e1[-1] == e2[0]) & (e1[0] == base)):
                p = e1+e2[1:]
                if(not(p in result)):
                    result.append(p)
    return result

def retrievecost(t,paths):
    result = 0
    variable = False
    for p in paths:
        if(t == p[0:-2]):
            result = p[-2]
            variable = p[-1]
            break
    return result,variable

def pathcost(Tree,paths,source,sink):
    #result = 0 #Change to be a list of weights since the same S/T mult. paths
    source = Tree.vertices[source]
    sink = Tree.vertices[sink]
    for p in paths:
        result = 0
        variable = False
        if((p[0] == source)&(p[-1] == sink)):
            for v in p:
                if(v != sink):
                    n = v.adj.index(p[p.index(v)+1])
                    w = v.weight[n]
                    print(w)
                    if(w == -1):
                        print('variable')
                        variable = True
                    else:
                        result += w
                # break
            p.append(result)
            p.append(variable)
    return paths

T0 = jd.Tree(4)
T0.link(4, 1, 5)
T0.link(4, 3, -1)  # -1 denotes a variable edge weight
T0.link(4, 2, 4)
T0.link(3, 1, 2)
T0.link(3, 2, 3)

totweight = totalweight(T0)

e = edges(T0)
print(e)
print(len(e))
p = edgepaths(e,T0.vertices[3])
print(p)
print(len(p))
printpaths(p)

p = pathcost(T0,p,3,2)

for y in p:
    print(y[-2:])

p = pathcost(T0,p,3,0)


for y in p:
    print(y[-2:])

p = pathcost(T0,p,3,1)

for y in p:
    print(y[-2:])

boundaries = []
interval = []
potentials = []
eps = 1./4

T0.editlink(4, 3, 0)
T0.vert_false()
x = T0.shortestpath(4)
print(x)
source = T0.vertices[3]
print(source.label)

Treeedges = treeedges(T0,x)
print(Treeedges)
printpaths(Treeedges)
treepath = edgepaths(Treeedges,T0.vertices[3])
print("Hello")
printpaths(treepath)
print(p[0][0:-2])
for path in p:
    if(not(path[0:-2] in treepath)):
        for t in treepath:
            if((path[0] == t[0]) & (path[-3] == t[-1])):
                cost,var = retrievecost(t,p)
                if(var):
                    boundaries.append(path[-2] - cost)

boundaries.sort()
print(boundaries)
for bound in boundaries:
    T0.editlink(4, 3, bound - eps)
    T0.vert_false()
    potentials.append([T0.shortestpath(4),bound - eps])
    T0.editlink(4, 3, bound + eps)
    T0.vert_false()
    potentials.append([T0.shortestpath(4),bound + eps])

for tree in potentials:
    print(tree)

print(equaltree(potentials[0][0],potentials[1][0]))


left = 0
j = 0
right = boundaries[j]
j+=1
for i in range(0,len(potentials)-1):
    if(not(equaltree(potentials[i][0],potentials[i+1][0]))):
        interval.append([potentials[i][0],[left,right]])
        left = right
        if (j == len(boundaries)):
            right = totweight
        else:
            right = boundaries[j]
            j += 1

interval.append([potentials[-1][0],[left,right]])

for tree in interval:
    print(tree)
