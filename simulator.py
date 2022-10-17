from math_utils import Vector2
import pygame
import graph as gr
import visualizer
from search import *

#Not working for now

class ColourPalette:
    Red = (255,0,0),

class SimulatorColours(ColourPalette):
    Vertex_normal = (255,0,0)
    Vertex_Hover = (0,0,250)
    Edge_normal = (50,50,50)
    Edge_drag_normal = (50,50,50)
    Edge_drag_Matching = (100,100,100)
    Edge_Matched = (200,10,10)
    Edge_NonMatched = (10,10,100)

class AnimationHolder:

    def __init__(self, info : dict = {}):
        self.info = info

    def __setitem__(self, index, item):
        self.info[index] = item

    def __getitem__(self, index):
        return self.info[index]

class Simulator:
    """
    Simulates the graph using Pygame
    """
    uNum = 0
    def GetUnum():
        Simulator.uNum = Simulator.uNum+1
        return Simulator.uNum-1

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
        s_uninteractive = -1
        s_base = 0
        s_matching = 1

        dragging = None
        edgeStart = None

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

                # Unresponsive
                if state == s_uninteractive:
                    break

                if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                    del self.graph
                    del self.graph_vis
                    self.graph = gr.SimpleGraph()
                    self.graph_vis = visualizer.GraphVisualizer(self.graph)
                
                if e.type == pygame.KEYDOWN and e.key == pygame.K_b:
                    partition = Search.Bipartition(self.graph)
                    if partition!=None:
                        self.TransitionAnimator = AnimationHolder()
                        self.TransitionAnimator["graph_vis_init"] = visualizer.GraphVisualizer(self.graph)
                        self.TransitionAnimator["graph_vis_init"].CopyGraphNodes(self.graph_vis)
                        self.TransitionAnimator["graph_vis_fin"] = visualizer.GraphVisualizer(self.graph)
                        self.TransitionAnimator["graph_vis_fin"].CopyGraphNodes(self.graph_vis)
                        self.TransitionAnimator["graph_vis_fin"].Bipartition(*partition)
                        self.TransitionAnimator["graph_vis_fin"].Transform(self.screenSize[1]/(2*len(self.graph.nodes)), 0, Vector2(self.screenSize)/2)
                        self.TransitionAnimator["t"] = 0
                        state = s_uninteractive

                #state change to matching
                if e.type == pygame.KEYDOWN and e.key == pygame.K_m:
                    if state == s_base:
                        state = s_matching
                    elif state == s_matching:
                        state = s_base
                

                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        onNode = Simulator.CheckInAllNodes(self.graph_vis, mouse_pos)
                        if onNode == None:
                            node = Simulator.GetUnum()
                            self.graph.addNode(node)
                            self.graph_vis[node] = mouse_pos
                        else:
                            dragging = onNode
                    elif e.button == 2:
                        onNode = Simulator.CheckInAllNodes(self.graph_vis, mouse_pos)
                        if onNode != None:
                            self.graph.deleteNode(onNode)
                            self.graph_vis.deleteNode(onNode)

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

                        

                if e.type == pygame.MOUSEBUTTONUP:
                    if e.button == 1:
                        dragging = None

            #Animation

            if state==s_uninteractive:
                if hasattr(self, "TransitionAnimator"):
                    if self.TransitionAnimator["t"] >= 1:
                        self.TransitionAnimator["t"] = 1

                    for node in self.graph_vis.graphNodes:
                        self.graph_vis[node] = Vector2.lerp(Vector2(self.TransitionAnimator["graph_vis_init"][node]), Vector2(self.TransitionAnimator["graph_vis_fin"][node]), self.TransitionAnimator["t"]).asTuple()
                        self.TransitionAnimator["t"] += 1/(self.clock.get_fps()*2)

                    if self.TransitionAnimator["t"] >= 1:
                        state = s_base
                        del self.TransitionAnimator
                    

            #condition handlers
            if dragging != None:
                self.graph_vis[dragging] = mouse_pos

            if edgeStart != None:
                if state==s_base:
                    pygame.draw.line(self.screen, SimulatorColours.Edge_drag_normal, self.graph_vis[edgeStart], mouse_pos)
                if state==s_matching:
                    pygame.draw.line(self.screen, SimulatorColours.Edge_drag_Matching, self.graph_vis[edgeStart], mouse_pos, 2)

            edges = self.graph.getEdges()
            if edges!=None:
                for edge in edges:
                    pygame.draw.line(self.screen, SimulatorColours.Edge_normal, self.graph_vis[edge[0]], self.graph_vis[edge[1]])
            

            for node in self.graph.nodes:
                colour = SimulatorColours.Vertex_Hover if Simulator.CheckInNode(self.graph_vis, node, mouse_pos) else SimulatorColours.Vertex_normal
                pygame.draw.circle(self.screen, colour, self.graph_vis[node], self.nodeRadius)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    a = Simulator()
    a.Start()

    