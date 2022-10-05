from graph import *
from search import Search

class Matching:
    def __init__(self, g : Graph, edges=[]):
        """
        Define a matching on graph g consisting of the edges in edges.
        Unweighted Matching.
        """
        self.isMatching = True
        self.graph = g
        self.matchingGraph = SimpleGraph()   #Matching is represented as an undirected unweighted graph
        self.matchingGraph.Construct(edges)

        self.CheckMatching()


    def CheckMatching(self):
        """
        Checks if current set of edges is a matching
        Avoid calling this function. Matching consistency is checked during each individual operation on the matching.
        """
        self.isMatching = True
        for node in self.matchingGraph.getNodes():
            if self.matchingGraph.getNeighbourCount(node) > 1:
                self.isMatching = False
                return False 
        return True

    def AssertConsistency(self):
        """
        If one wants to throw an error if the set of edges is not a matching
        """
        if not self.CheckMatching():
            raise MatchingError("Not a matching")

    def AddEdge(self, edge):
        self.matchingGraph.addEdge(*edge)

        # Consistency
        for v in edge:
            if self.matchingGraph.getNeighbourCount(v) > 1:
                self.isMatching = False
        return self.isMatching


    def RemoveEdge(self, edge):
        self.matchingGraph.deleteEdge(*edge)

        # Consistency
        if self.isMatching:
            return True
        else:
            return self.CheckMatching()

    
    #Query functions

    def getSize(self):
        return len(self.matchingGraph.getEdges())

    def isEmpty(self):
        return self.getSize() == 0 

    def getUnsaturatedVertices(self):
        vs= []
        for node in self.graph.getNodes():
            try:
                self.matchingGraph.getNeighbours(node)
            except:
                vs.append(node)
        return vs


class MatchingError(Exception):
    """
    Error for holding data about matchings
    """
    def __init__(self, message="", defaulter = None):
        self.message = message
        self.defaulter = defaulter



class MaximumMatching:

    def __init__(self, matching : Matching):
        self.matching = matching
    
    def getAugmentingPath(self):
        pass

    def Augment(self):
        pass

    def FindMaximum(self):
        pass

class BipartiteMaximumMatching(MaximumMatching):

    def __init__(self, matching : Matching, bipartition):
        self.matching = matching
        matching.AssertConsistency()
        self.bipartition = bipartition
        self.A0 = [v for v in matching.getUnsaturatedVertices() if v in bipartition[0]]
        self.B0 = [v for v in matching.getUnsaturatedVertices() if v in bipartition[1]]
        
        H = UnweightedGraph()
        for u in bipartition[0]:    # A -> B if in M
            if matching.matchingGraph.isNode(u):
                print(matching.matchingGraph.getNeighbours(u))
        #NOT FINISHED DO THIS HERE NOW DON"T PUSH OTHERWISE I KNOW YOU"RE A LAZY FICK
        for u in bipartition[1]:    # B -> A if in M
            for v in matching.graph.getNeighbours(u):
                if not matching.matchingGraph.isEdge(u, v):
                    H.isEdge(u, v)

        self.H = H


    def getAugmentingPath(self):
        A0 = self.A0.copy()
        while len(A0):
            a0 = A0.pop()
            Search.DFS(self.H, a0, self.B0)
            if Search.searchPath != None:
                return Search.searchPath

        return None

        

     