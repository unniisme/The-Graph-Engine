from graph import *
from visualizer import GraphVisualizer
from search import Search

c = SimpleGraph()
c.Construct([(1,2),(1,4),(2,5),(1,3),(2,6),(6,3),(3,7),(4,7),(7,8),(8,9),(6,10),(6,11),(10,12)])
d = SimpleGraph()
d.Construct([(1,2),(2,6),(7,8),(6,10)])
#print(c.AdjMat())

#print(Search.searchedEdges)

c_vis = GraphVisualizer(c)
d_vis = GraphVisualizer(d)
c_vis.Bipartition(*Search.Bipartition(c, 1))

d_vis.CopyGraphNodes(c_vis)

c_vis.Plot()
d_vis.Plot(None, 'r')

GraphVisualizer.Show()


#exec(open("./test.py").read())