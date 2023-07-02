
class Graph:
    #Base class, directed weighted graph
    
    # Privates---------------
    def __init__(self):
        self.nodes = {}

    def __str__(self):
        return self.string()

    def __repr__(self):
        return self.string()  

    #------------------------  
    def copy(self):
        copyGraph = Graph()
        copyGraph.nodes = self.nodes
        return copyGraph

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
        """
        Returns adjacency list of each vertex
        """
        string = ""
        for key in self.nodes:
            string += str(key)
            string += "\t"
            string += str(self.nodes[key])
            string += "\n"

        return string        


    #Some query functions

    def getNodes(self) -> list:
        """
        Returns list of nodes
        """
        return list(self.nodes.keys())

    def getWeight(self, u, v) -> float:
        """
        Returns weight of the given edge. Weight is 0 if edge doesn't exit
        """
        if v in self.nodes[u]:
            return self.nodes[u][v]
        return 0
    
    def isEdge(self, u, v) -> bool:
        if not self.isNode(u):
            return False
        return v in self.nodes[u]

    def isNode(self, node) -> bool:
        try:
            self.nodes[node]
            return True
        except:
            return False

    def getNeighbourCount(self, u) -> int:
        """
        Returns number of neighbors for a vertex
        """
        return len(self.nodes[u])

    def getNeighbours(self, u) -> dict:
        """
        Returns {neighbour: weight} dictionary
        """
        return self.nodes[u]

    def getNeighboursList(self, u) -> list:
        """
        Returns list of neighbors
        """
        return list(self.nodes[u].keys())

    def getEdges(self) -> list:
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
