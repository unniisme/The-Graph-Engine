# Reparent dir
import sys
sys.path.append("../The-Graph-Engine")

#import
from graph import *

# Test case for Graph class
graph = Graph()
graph.addNode("A")
graph.addNode("B")
graph.addNode("C")
graph.addEdge("A", "B", 2)
graph.addEdge("B", "C", 3)
print()
print("Weighted, Directed Graph")
print(graph.getNodes())  # Output: ['A', 'B', 'C']
print(graph.getEdges())  # [('A', 'B'), ('B', 'C')]
print(graph.getWeight("A", "B"))  # Output: 2
print(graph.isEdge("B", "C"))  # Output: True
print(graph.getNeighbourCount("B"))  # Output: 1
print(graph.getNeighbours("B"))  # Output: {'C': 3}

# Test case for UndirectedGraph class
undirectedGraph = UndirectedGraph()
undirectedGraph.addNode("A")
undirectedGraph.addNode("B")
undirectedGraph.addNode("C")
undirectedGraph.addEdge("A", "B", 2)
undirectedGraph.addEdge("B", "C", 3)
print()
print("Weighted, Undirected Graph")
print(undirectedGraph.getNodes())  # Output: ['A', 'B', 'C']
print(graph.getEdges())  # [('A', 'B'), ('B', 'C')]
print(undirectedGraph.getWeight("A", "B"))  # Output: 2
print(undirectedGraph.isEdge("B", "C"))  # Output: True
print(undirectedGraph.getNeighbourCount("B"))  # Output: 2
print(undirectedGraph.getNeighbours("B"))  # Output: {'A': 2, 'C': 3}

# Test case for UnweightedGraph class
unweightedGraph = UnweightedGraph()
unweightedGraph.addNode("A")
unweightedGraph.addNode("B")
unweightedGraph.addNode("C")
unweightedGraph.addEdge("A", "B")
unweightedGraph.addEdge("B", "C")
print()
print("Unweighted, directed Graph")
print(unweightedGraph.getNodes())  # Output: ['A', 'B', 'C']
print(unweightedGraph.isEdge("A", "B"))  # Output: True
print(unweightedGraph.getNeighbourCount("B"))  # Output: 1
print(unweightedGraph.getNeighbours("B"))  # Output: {'A': 1, 'C': 1}

# Test case for SimpleGraph class
simpleGraph = SimpleGraph()
edges = [("A", "B"), ("B", "C"), ("C", "D")]
simpleGraph.Construct(edges)
print(simpleGraph.getNodes())  # Output: ['A', 'B', 'C', 'D']
print(simpleGraph.getEdges())  # Output: [('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'B'), ('C', 'D'), ('D', 'C')]