import graph
from queue import PriorityQueue

class Search:

    globalData = {}

    def arbitrarySearch(graph : graph.Graph, start, end=None, evaluator=lambda x:1, getSearchEdges = False):
        """
        Runs a search algorithm that keeps a priority queue.
        Can effectively be used as BFS, best first search, A* search and Dijkstra's 

        evaluator has to be a function that takes an edge tuple as argument and returns it's priority
        evaluator : u,v -> number

        start is a node in graph
        
        if getSearchEdges, -Not implemented- all edges explored during the search is saved in the class
        """
        frontier = PriorityQueue()
        frontier.put((0,start))
        expanded = []

        if getSearchEdges:
            #unused for now
            Search.searchedEdges = []

        while not frontier.empty():
            curr = frontier.get()[1]

            if curr==end:
                break

            for neigh in graph.getNeighbours(curr):
                if neigh in expanded:
                    continue
                
                frontier.put((evaluator((curr, neigh)), neigh))

            expanded.append(curr)

        return expanded

    def BFS(graph : graph.Graph, start, end=None, getSearchEdges = False):

        return Search.arbitrarySearch(graph, start, end, getSearchEdges=getSearchEdges)

    def DFS(graph : graph.Graph, start, end=None, getSearchEdges=False):
        Search.globalData["DFScounter"] = 0
        def dfsEval(edge):
            Search.globalData["DFScounter"] += 1
            return Search.globalData["DFScounter"]

        searchRes = Search.arbitrarySearch(graph, start, end, evaluator=dfsEval, getSearchEdges=getSearchEdges)
        Search.globalData.pop("DFScounter")
    
    def Bipartition(graph: graph.Graph):
        """
        Returns a pair of sets of vertices representing left and right bipartitions is bipartite
        Else returns None
        """
        frontier = PriorityQueue()

        start = list(graph.nodes.keys())[0]

        partition = {}
        for node in graph.nodes:
            partition[node] = 0 #Unvisited
        partition[start] = 1
        frontier.put((0,start))

        while True:
            if frontier.empty():
                unvisitedVs = [v for v in partition if partition[v] == 0]
                if len(unvisitedVs)==0:
                    break
                partition[unvisitedVs[0]] = 1
                frontier.put((0, unvisitedVs[0]))

            curr = frontier.get()[1]

            for neigh in graph.getNeighbours(curr):
                if not partition[neigh] == 0:
                    if partition[neigh] == partition[curr]:
                        return None
                    continue

                partition[neigh] = -partition[curr]
                frontier.put((0, neigh))

        return ([v for v in partition if partition[v] == 1], [v for v in partition if partition[v] == -1])
        



class Matching:

    def __init__(self, graph : graph.Graph, edges):
        self.isMatching = True
        self.graph = graph
        self.edges = edges

        return self.CheckMatching()

    def CheckMatching(self):
        self.isMatching = True
        for edge in self.edges:
            for edge1 in self.edges:
                if edge[0] in edge1 or edge[1] in edge1:
                    self.isMatching = False
                    return False
        return True

    def AddEdge(self, edge):
        if edge in self.edges:
            return self.isMatching
        
        for edge1 in self.edges:
            if edge[0] in edge1 or edge[1] in edge1:
                self.isMatching = False

        self.edges.append(edge)
        return self.isMatching

    def RemoveEdge(self, edge):
        if edge not in self.edges:
            return self.isMatching

        # Complete

    