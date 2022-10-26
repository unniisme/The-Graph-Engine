import graph as gr
from math_utils import Vector2
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from search import Search

class GraphVisualizer:
    """
    Generates a 2D representation of a graph
    """
    
    #Definitions
    def __init__ (self, graph : gr.Graph):
        self.graph = graph
        self.graphNodes = {}
        for node in self.graph.nodes:
            self.graphNodes[node] = (0,0)

        self.specialEdges = []

    
    def CopyGraphNodes(self, other):
        self.graphNodes = other.graphNodes.copy()
        dellist = []
        for v in self.graphNodes:
            if v not in self.graph.nodes:
                dellist.append(v)
        
        for v in dellist:
            del self.graphNodes[v]
    
    def Cluster(self):
        """
        Clusters the nodes based on their closeness
        """
        def eval(edge):
            return self.graph.getNeighbourCount(edge[1])

        rearrangement = []
        for node in self.graph.nodes:
            if node in rearrangement:
                continue
            rearrangement += Search.arbitrarySearch(self.graph, node, evaluator=eval)

        self.graph.nodes = {key:self.graph.nodes[key] for key in rearrangement}

    def ClusterBipartition(self, leftNodes, rightNodes):
        """
        Clusters nodes as a bipartition
        """
        if len(leftNodes)+len(rightNodes) != len(self.graphNodes):
            raise ValueError()
        self.graph.nodes = {key:self.graph.nodes[key] for key in leftNodes+rightNodes}

    def Circle(self, radius = 1, uniform=False):
        """
        Distribute graph nodes in a circle around the origin. Radius defines the radius of the circle.
        If uniform is false, the nodes which have more neighbours will be closer to the centre.
        """
        n = len(self.graphNodes)
        for i, node in enumerate(self.graph.nodes):
            if uniform:
                dist = radius
            else:
                dist = radius/max(len(self.graph.nodes[node]),1)
            angle = i*360/n 
            self.graphNodes[node] = Vector2.PolarConstructorDeg(dist, angle).asTuple()

    def Bipartition(self, leftNodes, rightNodes):
        """
        Distribute the graph nodes into 2 lines on either side of the origin based on given bipartition
        the input lists should be names of nodes.
        """
        l = len(leftNodes)
        r = len(rightNodes)
        if l+r != len(self.graphNodes):
            raise ValueError()
        
        l_offset = Vector2(-l/2, -l/2)

        for i,node in enumerate(leftNodes):
            if node not in self.graphNodes:
                raise ValueError()

            self.graphNodes[node] = (l_offset + Vector2.UP()*i).asTuple()

        r_offset = Vector2(r/2, -r/2)

        for i,node in enumerate(rightNodes):
            if node not in self.graphNodes:
                raise ValueError()

            self.graphNodes[node] = (r_offset + Vector2.UP()*i).asTuple()

    def Tree(self, root, head = (0,0), spread=5):
        """
        Distribute the graphnodes into a tree or tree-like rooted at root
        """
        head = Vector2(head) #starts from origin

        # Uhh this isn't exactly BFS, come back later
        BFSdepth = {}

        def rec_call(node, depth, head):
            try:
                BFSdepth[node]
                return
            except:
                self.graphNodes[node] = head.asTuple()
                span = 1#spread/self.graph.getNeighbourCount(node)
                left = head + Vector2.DOWN() + (self.graph.getNeighbourCount(node)/2)*Vector2.LEFT()
                BFSdepth[node] = depth
                for i, neig in enumerate(self.graph.getNeighboursList(node)):
                    rec_call(neig, depth+1, left+span*i*Vector2.RIGHT())

        rec_call(root, 0, head)

        return BFSdepth


        #Better run a BFS and make tree accordingly
        depths = Search.BFStree(self.graph, root)
        maxdepth = max(depths.values())
        head = Vector2(0, maxdepth/2)

        for d in range(maxdepth+1):
            layer = [v for v in depths if depths[v] == d]
            left = Vector2(-len(layer)/2,0) + head+(d*Vector2.DOWN())
            for i, node in enumerate(layer):
                self.graphNodes[node] = (left+i*Vector2.RIGHT()).asTuple()


        

    def Transform(self, scale=1, rotate=0, offset=(0,0)):
        """
        Call assumes graph with no external manipulations
        rotate is angle in degrees
        """
        for node in self.graphNodes:
            self.graphNodes[node] = (((scale*Vector2(self.graphNodes[node])).RotateDeg(rotate)) + Vector2(offset)).asTuple()


    def Plot(self, vertexColor = 'b', edgeColor = 'b', directed = False, weighted = False):
        """
        Draw matplotlib graphs of the graphs
        keep any color = None to not draw
        """
        lines = []
        if not directed:
            for u in self.graph.nodes:
                for v in self.graph.nodes[u]:
                    lines.append([self.graphNodes[u], self.graphNodes[v]])

        if not hasattr(GraphVisualizer, 'ax'):
            fig, GraphVisualizer.ax = plt.subplots()
        ax = GraphVisualizer.ax

        if vertexColor != None:
            ax.scatter(*list(zip(*self.graphNodes.values())), color=vertexColor)
        for key in self.graphNodes:
            ax.annotate(key, self.graphNodes[key])
        
        if not directed:
            if edgeColor != None:
                ax.add_collection(LineCollection(lines, colors=edgeColor))

        else:
            for u in self.graph.nodes:
                for v in self.graph.nodes[u]:
                    ax.arrow(*self.graphNodes[u], *((Vector2(self.graphNodes[v]) - Vector2(self.graphNodes[u])).asTuple()), head_width=0.03, length_includes_head = True, color=edgeColor)

        if weighted:
            for u in self.graph.nodes:
                for v in self.graph.nodes[u]:
                    if self.graph.getWeight(u, v) != 0:
                        dirV = (Vector2(self.graphNodes[v]) - Vector2(self.graphNodes[u]))
                        if dirV.magnitude == 0:
                            continue
                        pos = (Vector2(self.graphNodes[u]) + dirV/2 + dirV.RotateDeg(90).Normalized()*dirV.magnitude/50).asTuple()
                        ax.annotate(str(self.graph.getWeight(u, v)), xy=pos)

    def PlotReset():
        del GraphVisualizer.ax

    def Show():
        plt.show()

    
    def deleteNode(self, node):
        del self.graphNodes[node]

    #Overrides
    def __setitem__(self, node, position : tuple):
        self.graphNodes[node] = position

    def __getitem__(self, node):
        return self.graphNodes[node]


