from graph import *
from search import Search

class Matching:
    def __init__(self, g : SimpleGraph, edges=[]):
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

    def addEdge(self, edge):
        self.matchingGraph.addEdge(*edge)

        # Consistency
        for v in edge:
            if self.matchingGraph.getNeighbourCount(v) > 1:
                self.isMatching = False
        return self.isMatching


    def deleteEdge(self, edge):
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


    # Queries:
    def isAlternating(self, path):
        if len(path) == 0:
            return True

        # Complete

class BipartiteMaximumMatching(MaximumMatching):
    """
    This class represents a maximum bipartite matching in a bipartite graph.

    Args:
        matching (Matching): An instance of the Matching class representing the initial matching.
        bipartition (tuple): A tuple containing two lists representing the bipartition of the graph.

    Attributes:
        matching (Matching): An instance of the Matching class representing the current matching.
        bipartition (tuple): A tuple containing two lists representing the bipartition of the graph.
        A0 (list): List of unsaturated vertices in the first partition (A) and in the bipartition.
        B0 (list): List of unsaturated vertices in the second partition (B) and in the bipartition.
        H (UnweightedGraph): A modified directed graph with edges directed from B to A if the edge is in the matching (M),
                             and from A to B otherwise.

    Methods:
        ModifiedGraph(matching, bipartition): Returns a modified graph with edges directed based on the matching (M).
        getAugmentingPath(): Runs DFS on the set of unsaturated vertices in A and returns an M-augmenting path if DFS
                             terminates in an unsaturated vertex in B. Otherwise, returns None.
        Augment(augPath): Augments the given path, updating the matching and the modified graph.
        FindMaximum(): Finds an augmenting path and augments it until no longer possible, updating the matching.

    """

    def __init__(self, matching : Matching, bipartition):
        self.matching = matching
        matching.AssertConsistency()
        self.bipartition = bipartition
        self.A0 = [v for v in matching.getUnsaturatedVertices() if v in bipartition[0]]
        self.B0 = [v for v in matching.getUnsaturatedVertices() if v in bipartition[1]]
        
        self.H = BipartiteMaximumMatching.ModifiedGraph(matching, bipartition)

    def ModifiedGraph(matching, bipartition):
        """
        Returns a modified graph with Edges directed from B to A if edge in M and A to B otherwise.
        """
        H = UnweightedGraph()
        H.addNodes(matching.graph.getNodes())       # Modified graph, with directions according to M
        for u in bipartition[1]:    # B -> A if in M
            if matching.matchingGraph.isNode(u):
                H.addEdge(u, matching.matchingGraph.getNeighboursList(u)[0])
        for u in bipartition[0]:    # A -> B if not in M
            for v in matching.graph.getNeighbours(u):
                if not matching.matchingGraph.isEdge(u, v):
                    H.addEdge(u, v)
        return H


    def getAugmentingPath(self):
        """
        Runs DFS on the set of unsaturated vertices in A, stops and returns M-Augmenting path if DFS terminates in an unsaturated vertex in B.
        Else returns None
        """
        A0 = self.A0.copy()
        while len(A0):
            a0 = A0.pop()
            Search.DFS(self.H, a0, self.B0)
            if Search.searchPath != None:
                return Search.searchPath

        return None

    def Augment(self, augPath : list) -> bool:
        """
        Augments the Given path.
        Returns if augmentation was successful.
        """
        #Check if augPath is M-Augmenting, or make it so that removing edges phases out independant vertices in matchingGraph

        for edge in zip(augPath, augPath[1:]):
            if self.matching.matchingGraph.isEdge(*edge):
                self.matching.deleteEdge(edge)
            else:
                self.matching.matchingGraph.addNodes(edge)
                self.matching.addEdge(edge)
            # Remove or add edges to matchingGraph
            # Consistency here is that matchingGraph only contains saturated nodes

            # Flip corresponding edge in H
            if self.H.isEdge(*edge):
                self.H.deleteEdge(*edge)
                self.H.addEdge(edge[1], edge[0])
            else:
                self.H.deleteEdge(edge[1], edge[0])
                self.H.addEdge(*edge)

        self.A0.remove(augPath[0])
        self.B0.remove(augPath[-1])

    def FindMaximum(self):
        """
        Finds augmenting path and augments it until no longer possible
        """

        path = self.getAugmentingPath()
        while path != None:

            self.Augment(path)
            path = self.getAugmentingPath()


        

        

     