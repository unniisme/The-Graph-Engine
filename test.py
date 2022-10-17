from graph import *
from visualizer import GraphVisualizer
from search import Search
from matching import Matching
from matching import BipartiteMaximumMatching

c = SimpleGraph()
c.Construct([(1,2),(1,4),(2,5),(6,3),(3,7),(7,8),(8,9),(6,10),(6,11),(10,12),(1,9)])
m = Matching(c, [(1,2),(7,8),(6,10)])
#bi = Search.Bipartition(c)
#maxMat = BipartiteMaximumMatching(m, bi)



c_vis = GraphVisualizer(c)
d_vis = GraphVisualizer(m.matchingGraph)
print(Search.Bipartition(c))
#c_vis.Cluster()
c_vis.Bipartition(*Search.Bipartition(c))
#c_vis.ClusterBipartition(*Search.Bipartition(c))


d_vis.CopyGraphNodes(c_vis)

c_vis.Plot()
d_vis.Plot(None, 'r')
GraphVisualizer.Show()

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
