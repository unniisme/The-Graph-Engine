# Reparent dir
import sys
sys.path.append("../The-Graph-Engine")

#Import
from graph import *
from visualizer import GraphVisualizer
from search import Search
from matching import Matching

# Construct a simple graph and define a matching over it
c = SimpleGraph()
c.Construct([(1,2),(1,4),(2,5),(6,3),(3,7),(7,8),(8,9),(6,10),(6,11),(10,12),(1,9)])
m = Matching(c, [(1,2),(7,8),(6,10)])

## Bipartition representation
c_vis = GraphVisualizer(c)                  # Initialize visualizer for base graph
d_vis = GraphVisualizer(m.matchingGraph)    # and for matching graph, this one in red
c_vis.Bipartition(*Search.Bipartition(c))   # Bipartition the graph
d_vis.CopyGraphNodes(c_vis)                 # Copy positions of graph node onto the matching graph
c_vis.Plot()                                # Plot base graph
d_vis.Plot(None, 'r')                       # Plot matching in red
GraphVisualizer.Title("Bipartite")
GraphVisualizer.Show()                      # Show graph

GraphVisualizer.PlotReset()
c_vis.ClusterBipartition(*Search.Bipartition(c))    # Order nodes as a bipartition
c_vis.Circle(uniform=True)                  # Arrange nodes in a circle with uniform radius
d_vis.CopyGraphNodes(c_vis)                 # Copy positions of graph node onto the matching graph
c_vis.Plot()                                # Plot base graph
d_vis.Plot(None, 'r')                       # Plot matching in red
GraphVisualizer.Title("Bipartite circular")
GraphVisualizer.Show()                      # Show graph

## Circular cluster
GraphVisualizer.PlotReset()
c_vis.Cluster()                             # Order nodes in degree order
c_vis.Circle()                              # Arrange nodes in a circle with radius inversly proportional to degree
d_vis.CopyGraphNodes(c_vis)                 # Copy positions of graph node onto the matching graph
c_vis.Plot()                                # Plot base graph
d_vis.Plot(None, 'r')                       # Plot matching in red
GraphVisualizer.Title("Clusterd circular")
GraphVisualizer.Show()                      # Show graph






"""maxMat.Augment(maxMat.getAugmentingPath())

GraphVisualizer.PlotReset()
c_vis.Plot()
d_vis.Plot(None, 'r')
GraphVisualizer.Show()

maxMat.FindMaximum()

print(maxMat.getAugmentingPath())

GraphVisualizer.PlotReset()
c_vis.Plot()
d_vis.Plot(None, 'r')
GraphVisualizer.Show()"""
