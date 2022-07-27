#Module defining vertex and path length classes
#with some functions on vertices and path lengths
#Jacob Cleveland Summer 2022

class Vertex:
    num_vert = 0
    vertices = []
    source = 0

    def __init__(self, lab):
        self.label = lab
        self.adj = []
        self.visited = False
        Vertex.num_vert += 1
        Vertex.vertices.append(self)

    def add(self, other, weight): #add weighted adjacency
        self.adj.append([other,weight])

    def source(self): #determine which vertex is single source
        Vertex.source = self

class pLen:
    def __init__(self, length, seq):
        self.length = length #list of constant, parameters
        self.seq    = seq    #sequence of vertices taken by path
        self.adj    = []     #list of pLen that self points to in poset

    #links self to pLen other in adj list
    def link(self,other):
        if(compare(self.length,other.length)):
            if(len(self.length) <= len(other.length)): #shorter comparable list is shorter
                self.adj.append(other)
            else:
                other.adj.append(self)
       
'''
***************
Function dirContained
***************
returns if the parameters of plen1
are contained in the parameters of plen2
'''
def dirContained(plen1,plen2):
    result = True
    for i in range(1,len(plen1)): #are all params of plen1 in plen2?
        if(not(plen1[i] in plen2)):
            result = False
    return result

'''
***************
Function compare
***************
Given two arrays of path lengths to a vertex in a graph,
return whether the paths are equal, comparable, or incomparable

comparable = True
incomparable = False
If they are comparable, return the smaller one?
'''
def compare(plen1,plen2):
    result = False #assume incomparable
    result = (dirContained(plen1,plen2) | dirContained(plen2,plen1))
    return result

'''
***************
Function dfs3
***************

'''
def dfs3(src,cpath):
    path_list = [[src]]
    for next_vertex in src.adj:
        if next_vertex[0] in cpath:
            continue
        partial_paths = dfs3(next_vertex[0],cpath + [src])
        for path in partial_paths:
            path_list.append([src]+path)
    return path_list

'''
***************
Function tot_weight
***************
Returns a list of the edge weights along path
according to the current graph in the Vertex class
'''
def tot_weight(path):
    result = []
    src = path[0]
    for v in src.adj:
        if v[0] == path[1]:
            result.append(v[1])
            break
    if(len(path)>2):
        result += tot_weight(path[1:])
    return result

'''
***************
Function collapse
***************
Returns a simplified list of edge weights along
the path where all the constants are summed up and
in the first entry
'''
def collapse(pathLength):
    result = [0]
    for weight in pathLength:
        if(type(weight) == int):
            result[0] += weight #add constant weight
        else:
            result += [weight] #append parametric weight
    return result

'''
***************
Function printPaths
***************
'''
def printPaths(paths):
    for path in paths:
        result = ""
        for vertex in path:
            result += vertex.label
        print(result)

'''
***************
Function printPathsArray
***************
'''
def printPathsArray(paths):
    result = []
    for path in paths:
        temp = []
        for vertex in path:
            temp += [vertex.label]
        result += [temp]
    print(result)

'''
***************
Function genWeights
***************
'''
def genWeights(paths):
    result = []
    for p in paths[1:]:
        h = tot_weight(p)
        l = collapse(h)
        result += [l]
    return result

'''
helper function pequal
checks if par1 and par2 have the same list of parameters xi
don't need to match order

e.g. pequal([1,"x1","x2"],[3,"x2"]) = False
and pequal([1,"x1","x2"],[3,"x2","x1"]) = True
'''
def pequal(par1,par2):
    result = True
    for i in range(1,len(par1)):
        if(not(par1[i] in par2)):
            result = False
    return result

'''
helper function min_param

Given a list of parametric path lengths 
with the same parameters, returns the
parametric path length with smallest 
constant weight.
'''
def min_param(part):
    result = -1
    if(len(part)>0):
        result = part[0]
        for cost in part:
            value1 = cost[0]
            value2 = result[0]
            if((type(value1) == int) and (type(value2) == int)):
                if(cost[0] < result[0]):
                    result = cost
    return result

'''
***************
Function reduce
***************
Given an array of path lengths to a vertex in a graph,
gives the reduced array of path lengths s.t.
the minimum of both arrays is the same.

for example, reduce([1,2,3+x]) yields [2,3+x]
more likely
reduce([1,2,[3,'x1']]) yields [1,[3,'x1']]
reduce([1,[1,'x1']]) yields [1]
reduce([[1,'x1','x2'],[2,'x1','x2']) yields [[1,x1,x2]]
reduce([[1,'x1','x2'],[2,'x1','x2'],[1,'x3']) yields [[1,x1,x2],[1,x3]]
reduce([10,2,[1,'x1'],[1,'x1','x2']]) yields [2,[1,'x1']]
reduce([10,2,[1,'x1','x2','x3'],[1,'x1','x2']]) yields [2,[1,'x1','x2']]
'''
def reduce(pLen):
    result = []
    const = []
    param = []
    for val in pLen:
        if(len(val) == 1):
            const.append(val)
        else:
            param.append(val) #partition pLen into parametric and const. path weights
    cMin = -1
    if(len(const) > 0):
       cMin = min(const)[0] #minimum of constants
       result.append([cMin])
    i = 0
    while(i < len(param)): #iterate through path lengths containing a parameter
        first = param[i]
        part = [first]
        grok = []
        for j in range(i+1,len(param)):
            second = param[j]
            if(pequal(first,second)):
                part.append(second) #iterate through and add all parametric weights with same list of variables
            else:
                grok.append(second)
        i+=1
        pMin = min_param(part)
        if((pMin[0] < cMin) | (cMin == -1)):
            result.append(pMin)
        if(len(grok) >0):
            param = grok
            i = 0
        else:
            break
    return result