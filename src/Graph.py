import numpy as np
import time
from src.Edge import Edge
from src.Node import Node
from collections import deque


class Graph:
    def __init__(self):
        self.objects = []
        self.nodes:dict[Node] = {}
        self.edges:list[Edge] = []
        self.selected_obj = None
        self.radius = 30
        self.count = 0
        self.visited = None
        self.nodes_stored = None

    def add_node(self, pos, text_generator):
        node = Node(pos, self.count, text_generator)
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
            self.objects.remove(self.nodes[self.selected_obj.id])
            del self.nodes[self.selected_obj.id]
            
        elif(isinstance(self.selected_obj, Edge)):
            self.edges.remove(self.selected_obj)
            self.objects.remove(self.selected_obj)
        del self.selected_obj
        self.selected_obj = None

    def update_edges(self, radius, arrow_size):
        for edge in self.edges:
            edge.update(radius = radius, arrow_size=arrow_size)

    
    def update_selected_obj(self, radius, pos, arrow_size):
        if(self.select_object):
            if(isinstance(self.selected_obj, Node)):
                self.selected_obj.update(pos=pos)
            elif(isinstance(self.selected_obj, Edge)):
                self.selected_obj.update(radius, arrow_size, pos)

    def dfs(self, sleep_time):
        self.visited = {i : False for i in [x.id for x in self.nodes.values()]}
        
        for node in self.nodes.values():
            node.dfs(self.visited, sleep_time)
        
        self.visited = None

    def bfs(self, sleep_time):
        visited = {i : False for i in [x.id for x in self.nodes.values()]}
        for node in self.nodes.values():
            self.visited = visited.copy()
            self.nodes_stored = deque()
            node.bfs(self.visited, self.nodes_stored, sleep_time)
        
        self.visited = None
        self.nodes_stored = None


    def update(self, radius, pos, arrow_size):
        self.update_selected_obj(radius, pos, arrow_size)
        self.update_edges(radius, arrow_size=arrow_size)

    
            

    