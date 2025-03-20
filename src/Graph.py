import numpy as np
import time
from src.Edge import Edge
from src.Node import Node

def get_random_color():
    return list(np.random.choice(range(256), size=3))

class Graph:
    def __init__(self):
        self.objects = []
        self.nodes:dict[Node] = {}
        self.edges:list[Edge] = []
        self.selected_obj = None
        self.radius = 30
        self.count = 0

    def add_node(self, pos, text_generator):
        node = Node(pos, self.count, (0,0,0))
        node.create_label(text_generator, get_random_color())
        self.nodes[self.count] = node
        self.objects.append(node)
        self.count+=1

    def add_edge(self, pos):
        for node in self.nodes.values():
            if (node.check(pos)):
                edge = Edge(node, pos)
                self.edges.append(edge)
                self.objects.append(edge)
                self.selected_obj = edge
                return
            
    def check_created_edge(self, pos):
        if(self.selected_obj):
            for node in self.nodes.values():
                if (node != self.selected_obj.n1 and node.check(pos)):
                    self.selected_obj.n2 = node
                    self.selected_obj.n1.adjacency_list.append(node)
                    return
            self.edges.remove(self.selected_obj)
            self.objects.remove(self.selected_obj)
            del self.selected_obj
            self.selected_obj = None

    def select_object(self, pos):
        for obj in self.objects:
            if (obj.check(pos)):
                self.selected_obj = obj
                return
        self.selected_obj = None

    def delete_selected_obj(self):
        if(isinstance(self.selected_obj, Node)):
            edges = [edge for edge in self.edges if (edge.n1 == self.selected_obj or edge.n2 == self.selected_obj)]
            for edge in edges:
                self.edges.remove(edge)
                self.objects.remove(edge)
            self.objects.remove(self.nodes[self.selected_obj.name])
            del self.nodes[self.selected_obj.name]
            
        elif(isinstance(self.selected_obj, Edge)):
            self.edges.remove(self.selected_obj)
            self.objects.remove(self.selected_obj)
        del self.selected_obj
        self.selected_obj = None

    def update_edges(self, radius):
        for edge in self.edges:
            edge.update(radius = radius)

    def update_nodes(self, radius):
        for node in self.nodes.values():
            node.update(radius = radius)
    
    def update_selected_obj(self, radius, pos):
        if(isinstance(self.selected_obj, Node)):
            self.selected_obj.update(pos=pos)
        elif(isinstance(self.selected_obj, Edge)):
            self.selected_obj.update(radius, pos)

    def dfs(self):
        visited = np.zeros(len(self.nodes), dtype=bool)
        color = (239, 239, 38)
        width = 2
        for node in self.nodes.values():
            node.dfs(visited, color, width)


            
    def render(self, screen):
        for obj in self.objects:
            obj.render(screen)

    def update(self, radius):
        self.update_nodes(radius)
        self.update_edges(radius)

    
            

    