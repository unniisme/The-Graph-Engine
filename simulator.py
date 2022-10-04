from math_utils import Vector2
import pygame
import graph as gr
import visualizer
from search import *

class Simulator:
    """
    Simulates the graph using Pygame
    """

    nodeRadius = 10
    def CheckInNode(graph_vis, node, position):
        return (Vector2(graph_vis[node]) - Vector2(position)).magnitude < Simulator.nodeRadius
    def CheckInAllNodes(graph_vis, position):
        if len(graph_vis.graphNodes) == 0:
            return None

        for node in graph_vis.graphNodes:
            if Simulator.CheckInNode(graph_vis, node, position):
                return node
        return None

    def __init__ (self, screenSize = [800, 600]):
        self.graph = gr.SimpleGraph()
        self.graph_vis = visualizer.GraphVisualizer(self.graph)
        self.screen = pygame.display.set_mode(screenSize)
        self.screenSize = screenSize
        self.clock = pygame.time.Clock()
        self.running = True

    def Start(self):

        # MenuStates
        state = 0
        s_base = 0
        s_matching = 0

        dragging = None
        edgeStart = None
        #matching = Matching(self.graph, [])

        while self.running:
            self.screen.fill((255,255,255))

            mouse_pos = pygame.mouse.get_pos()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    return 0
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
                    return 0
                if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                    del self.graph
                    del self.graph_vis
                    self.graph = gr.SimpleGraph()
                    self.graph_vis = visualizer.GraphVisualizer(self.graph)
                
                if e.type == pygame.KEYDOWN and e.key == pygame.K_b:
                    partition = Search.Bipartition(self.graph)
                    if partition!=None:
                        self.graph_vis.Bipartition(*partition)
                        self.graph_vis.Transform(self.screenSize[1]/(2*len(self.graph.nodes)), 0, Vector2(self.screenSize)/2)

                #state change to matching
                if e.type == pygame.KEYDOWN and e.key == pygame.K_m:
                    if state == s_base:
                        state = s_matching
                    if state == s_matching:
                        state = s_base
                

                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        onNode = Simulator.CheckInAllNodes(self.graph_vis, mouse_pos)
                        if onNode == None:
                            node = len(self.graph.nodes)
                            self.graph.addNode(node)
                            self.graph_vis[node] = mouse_pos
                        else:
                            dragging = onNode
                    elif e.button == 3:
                        if edgeStart == None:
                            edgeStart = Simulator.CheckInAllNodes(self.graph_vis, mouse_pos)
                        else:
                            edgeEnd = Simulator.CheckInAllNodes(self.graph_vis, mouse_pos)
                            if edgeEnd == None:
                                edgeStart = None
                            else:
                                if state == s_base:
                                    if not self.graph.getWeight(edgeStart, edgeEnd):
                                        self.graph.addEdge(edgeStart, edgeEnd)
                                    else:
                                        self.graph.deleteEdge(edgeStart, edgeEnd)
                                    edgeStart = None
                                elif state == s_matching:
                                    pass

                        

                if e.type == pygame.MOUSEBUTTONUP:
                    if e.button == 1:
                        dragging = None

            #condition handlers
            if dragging != None:
                self.graph_vis[dragging] = mouse_pos

            if edgeStart != None:
                pygame.draw.line(self.screen, (50,50,50), self.graph_vis[edgeStart], mouse_pos)

            edges = self.graph.getEdges()
            if edges!=None:
                for edge in edges:
                    pygame.draw.line(self.screen, (50,50,50), self.graph_vis[edge[0]], self.graph_vis[edge[1]])

            for node in self.graph.nodes:
                colour = (0,0,250) if Simulator.CheckInNode(self.graph_vis, node, mouse_pos) else (255,0,0)
                pygame.draw.circle(self.screen, colour, self.graph_vis[node], self.nodeRadius)

            pygame.display.flip()
            self.clock.tick(60)


a = Simulator()
a.Start()

    