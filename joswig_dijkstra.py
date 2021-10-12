#Attempt to route using the Joswig Algorithm described here: https://arxiv.org/pdf/1904.01082.pdf
#using object oriented programming.
class Vertex:
    num_vert = 0
    vertices = []

    def __init__(self, lab=""):
        self.label  = lab
        self.adj    = []    #adjacency list
        self.weight = []    #weights associated to adjacency list edges
        self.known  = False #shortest path to self is known
        self.pv     = None  #previous node in shortest path tree
        self.dv     = 0     #current distance on best known path
        self.help   = False #helper boolean denoting if a vertex has had dv changed from 0.
        Vertex.num_vert += 1
        Vertex.vertices.append(self)

    #links self to vert with weight cost
    def link(self,vert,cost):
        if((vert in self.adj) == False):
            self.adj.append(vert)
            self.weight.append(cost)

    def editlink(self,vert,cost):
        if((vert in self.adj) == True):
            self.weight[self.adj.index(vert)] = cost

    def clear(self):
        Vertex.num_vert = 0
        Vertex.vertices = []

    def printadj(self,lab):
        for v in self.adj:
            result = v.label,v.dv
            if(lab == True):
                result = v.label,v.pv.label,v.dv
            print(result)

    #reset vertex boolean values
    #must be called before
    def vert_false(self):
        for v in Vertex.vertices:
            v.known = False
            v.dv = 0
            v.pv = None
            v.help = False

    def shortestpath(self):
        num_edge = 0
        if(self.adj != []):
            num_edge = len(self.adj)
        self.known = True
        if(num_edge > 0):
            for i in range(0,num_edge):
                weight = self.weight[i]
                if(weight == -1):
                    weight = 0
                if((self.adj[i].help == False) | (self.adj[i].dv > weight + self.dv)):
                    self.adj[i].dv = weight + self.dv
                    self.adj[i].pv = self
                    self.adj[i].help = True
        min = -1
        next = None
        done = True
        for v in Vertex.vertices:
            if(v.known == False):
                done = False
                if(v.help == True):
                    if((min == -1) | (min > v.dv)):
                        min = v.dv
                        next = v
        if(done == False):
            if(next != None):
                next.shortestpath()

class Tree:
    num_trees = 0
    trees = []

    def __init__(self,numvert):
        self.vertices = []
        for i in range(0,numvert):
            self.vertices.append(Vertex("v"+str(i+1)))
        Tree.num_trees += 1
        Tree.trees.append(self)

    def link(self,init,final,weight):
        numvert = len(self.vertices)
        init = init-1
        final = final-1
        if((init < numvert) & (final < numvert)):
            self.vertices[init].link(self.vertices[final],weight)

    def editlink(self,init,final,newweight):
        numvert = len(self.vertices)
        init = init - 1
        final = final - 1
        if ((init < numvert) & (final < numvert)):
            self.vertices[init].editlink(self.vertices[final],newweight)

    def shortestpath(self,vert):
        self.vertices[vert-1].shortestpath()
        result = []
        for x in self.vertices[vert-1].adj:
            result.append([x.label,x.pv.label,x.dv])
        return result

    def add_vertex(self,vert):
        self.vertices.append(vert)

    def vert_false(self):
        self.vertices[0].vert_false()

    def printadj(self,vert,lab):
        self.vertices[vert-1].printadj(lab)
