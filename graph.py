
class Graph:
    #Base class, directed weighted graph
    
    def __init__(self):
        self.nodes = {}

    def addNode(self, node):
        if  node not in self.nodes:
            self.nodes[node] = {}

    def addNodes(self, nodes):
        for node in nodes:
            self.addNode(node)

    def addEdge(self, u, v, weight = 1):
        self.nodes[u][v] = weight

    def deleteNode(self, node):
        for v in self.nodes:
            self.deleteEdge(node, v)
            self.deleteEdge(v, node)

        del self.nodes[node]

    def deleteEdge(self, u, v):
        if v in self.nodes[u]:
            del self.nodes[u][v]

    def addEdges(self, edgeTuples):
        for edgeTuple in edgeTuples:
            self.addEdge(*edgeTuple)

    def AdjMat(self):
        """
        Returns the adjacency matrix as a string.
        """
        string = "\t"
        for key in self.nodes:
            string+=(str(key)+"\t")
        string+="\n"
        for u in self.nodes:
            string+=str(u)+"\t"
            for v in self.nodes:
                string += str(self.getWeight(u, v)) + "\t"
            string+="\n"

        return string

    def string(self):
        string = ""
        for key in self.nodes:
            string += str(key)
            string += "\t"
            string += str(self.nodes[key])
            string += "\n"

        return string        


    def __str__(self):
        return self.string()

    def __repr__(self):
        return self.string()    


    #Some query functions

    def getWeight(self, u, v):
        if v in self.nodes[u]:
            return self.nodes[u][v]
        return 0

    def getNeighbourCount(self, u):
        """
        Returns number of neighbors for a vertex
        """
        return len(self.nodes[u])

    def getNeighbours(self, u):
        """
        Returns {neighbour: weight} dictionary
        """
        return self.nodes[u]

    def getEdges(self):
        """
        Returns a list of edges in order of added nodes
        """
        edges = []
        for u in self.nodes:
            for v in self.nodes:
                if self.getWeight(u, v) != 0:
                    edges.append((u,v))
        return edges



class UndirectedGraph(Graph):

    def addEdge(self, u, v, weight=1):
        Graph.addEdge(self, u, v, weight)
        Graph.addEdge(self, v, u, weight)

    def deleteEdge(self, u, v):
        Graph.deleteEdge(self, u, v)
        Graph.deleteEdge(self, v, u)

class UnweightedGraph(Graph):

    def addEdge(self, u, v):
        Graph.addEdge(self, u, v)

class SimpleGraph(UndirectedGraph, UnweightedGraph):
    
    def addEdge(self, u, v):
        UndirectedGraph.addEdge(self, u, v)

    def Construct(self, edges):
        xnodes = [x for x,y in edges]
        ynodes = [y for x,y in edges]
        self.addNodes(xnodes+ynodes)
        self.addEdges(edges)
