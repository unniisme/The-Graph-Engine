# Reparent dir
import sys
sys.path.append("../The-Graph-Engine")

#Import
from graph import *
from visualizer import GraphVisualizer
from search import Search
from matching import Matching
from matching import BipartiteMaximumMatching

# Construct a simple graph and bipartition it
c = SimpleGraph()
c.Construct([(1,2),(1,4),(2,5),(6,3),(3,7),(7,8),(8,9),(6,10),(6,11),(10,12),(1,9)])
bipartition = Search.Bipartition(c)

# Initialize matching and max matching
m = Matching(c, [(1,2),(7,8),(6,10)])
maxMat = BipartiteMaximumMatching(m, bipartition)

## Bipartition representation
c_vis = GraphVisualizer(c)                  # Initialize visualizer for base graph
d_vis = GraphVisualizer(m.matchingGraph)    # and for matching graph, this one in red
c_vis.Bipartition(*bipartition)   # Bipartition the graph
d_vis.CopyGraphNodes(c_vis)                 # Copy positions of graph node onto the matching graph
c_vis.Plot()                                # Plot base graph
d_vis.Plot(None, 'r')                       # Plot matching in red
GraphVisualizer.Show()                      # Show graph

# Find and augment an augmenting path
augPath = maxMat.getAugmentingPath()
print("Augmenting path :", augPath)
maxMat.Augment(augPath)

# Revisualize matching
d_vis = GraphVisualizer(m.matchingGraph)    # Reload matching graph now that it's been modified
d_vis.CopyGraphNodes(c_vis)                 # Copy positions of graph node onto the matching graph
GraphVisualizer.PlotReset()
c_vis.Plot()
d_vis.Plot(None, 'r')
GraphVisualizer.Show()

# Find maximum matching
maxMat.FindMaximum()
print("Augmenting to maximum")

# Revisualize matching
d_vis = GraphVisualizer(m.matchingGraph)    # Reload matching graph now that it's been modified
d_vis.CopyGraphNodes(c_vis)                 # Copy positions of graph node onto the matching graph
GraphVisualizer.PlotReset()
c_vis.Plot()
d_vis.Plot(None, 'r')
GraphVisualizer.Show()
