from graph import *
from queue import PriorityQueue

class Search:

    globalData = {}

    def arbitrarySearch(graph : Graph, start, end=None, evaluator=lambda x:1):
        """
        Runs a search algorithm that keeps a priority queue.
        Can effectively be used as BFS, best first search, A* search and Dijkstra's 

        evaluator has to be a function that takes an edge tuple as argument and returns it's priority
        evaluator : u,v -> number

        start is a node in graph
        end is the final node, or the set of final nodes
        
        Search.searchPath gives the resulting found path.
        """
        try:
            end[0]
        except:
            end = [end] 

        frontier = PriorityQueue()
        searchPaths = PriorityQueue()

        frontier.put((0,start))
        searchPaths.put((0, [start]))
        expanded = []

        while not frontier.empty():
            curr = frontier.get()[1]
            Search.searchPath = searchPaths.get()[1]

            if curr in end:
                expanded.append(curr)
                return expanded

            for neigh in graph.getNeighbours(curr):
                if neigh in expanded:
                    continue
                
                frontier.put((evaluator((curr, neigh)), neigh))
                searchPaths.put((evaluator((curr, neigh)), Search.searchPath + [neigh]))

            expanded.append(curr)
        Search.searchPath = None    # No solution path
        return expanded

    def BFS(graph : Graph, start, end=None, getSearchEdges = False):

        return Search.arbitrarySearch(graph, start, end)

    def BFStree(graph : Graph, start):
        """
        Recursive BFS that returns a dictionary of node depth from start
        """
        # Better run a BFS and divide accordingly

        BFSdepth = {}

        def rec_call(node, depth):
            try:
                BFSdepth[node]
                return
            except:
                BFSdepth[node] = depth
                for neig in graph.getNeighbours(node):
                    rec_call(neig, depth+1)

        rec_call(start, 0)

        return BFSdepth



    def DFS(graph : Graph, start, end=None, getSearchEdges=False):
        Search.globalData["DFScounter"] = 0
        def dfsEval(edge):
            Search.globalData["DFScounter"] -= 1
            return Search.globalData["DFScounter"]

        searchRes = Search.arbitrarySearch(graph, start, end, evaluator=dfsEval)
        Search.globalData.pop("DFScounter")
        return searchRes
    
    def Bipartition(graph: Graph):
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

    