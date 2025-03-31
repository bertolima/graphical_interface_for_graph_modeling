import numpy as np
import time
from src.Edge import Edge, Pseudo_edge
from src.Node import Node
from collections import deque
from random import randint
import pygame as pg


class Graph:
    def __init__(self, app):
        self.objects = []
        self.nodes:dict[Node] = {}
        self.edges:list[Edge] = []

        self.selected_obj = None

        self.radius = 30
        self.count = 0
        self.app = app

        self.visited = None
        self.nodes_stored = None

        self.node_radius = 30

        self.node_color = [0,0,0]
        self.visited_node_color = [239, 239, 38]
        self.edge_color = [0,0,0]

        self.node_width = 2
        self.visited_node_width = 2
        self.edge_width = 2

        self.arrow_size = 10

    def add_node(self):
        node = Node(self.app.mouse_pos, self.count, self.app.font)
        self.nodes[self.count] = node
        self.objects.append(node)
        self.count+=1

    def add_edge(self):
        for node in self.nodes.values():
            if (node.check(self.app.mouse_pos, self.node_radius)):
                edge = Pseudo_edge(node, self.app.mouse_pos)
                self.selected_obj = edge
                return
            
    def from_adjacency_list(self, adjacency_list):
        for u, v in adjacency_list:
            node_u = None
            node_v = None
            if(u not in self.nodes):
                node_u = Node([randint(0, self.app.screen_size[0]), randint(0,self.app.screen_size[1])], u, self.app.font)
                self.nodes[u] = node_u
                self.objects.append(node_u)
            else:
                node_u = self.nodes[u]
            
            if(v not in self.nodes):
                node_v = Node([randint(0, self.app.screen_size[0]), randint(0,self.app.screen_size[1])], v, self.app.font)
                self.nodes[v] = node_v
                self.objects.append(node_v)
            else:
                node_v = self.nodes[v]

            edge = Edge(n1=node_u, n2=node_v, origin=self.app.origin, node_radius=self.node_radius, arrow_size=self.arrow_size)
            self.edges.append(edge)
            self.objects.append(edge)
            node_u.adjacency_list.append(node_v)
            node_v.predecessors.append(node_u)

            
    def check_created_edge(self):
        if(isinstance(self.selected_obj, Pseudo_edge)):
            for node in self.nodes.values():
                if (node != self.selected_obj.n1 and node.check(self.app.mouse_pos, self.node_radius)):
                    u = self.selected_obj.n1
                    v = node

                    u.adjacency_list.append(v)
                    edge = Edge(u, v, self.app.origin, self.node_radius, self.arrow_size)
                    self.edges.append(edge)
                    self.objects.append(edge)
                    del self.selected_obj
                    self.selected_obj = None
                    return
            del self.selected_obj
            self.selected_obj = None

    def select_object(self):
        for edge in self.edges:
            if (edge.check(self.app.mouse_pos)):
                self.selected_obj = edge
                return
        for node in self.nodes.values():
            if (node.check(self.app.mouse_pos, self.radius)):
                self.selected_obj = node
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

    def update_edges(self):
        nodes_outdated = {}
        for edge in self.edges:
            if(not edge.n1.updated or not edge.n2.updated):
                nodes_outdated[edge.n1.id] = edge.n1
                nodes_outdated[edge.n2.id] = edge.n2
                edge.update(radius = self.node_radius, arrow_size=self.arrow_size, origin_direction=self.app.origin)

        for node in nodes_outdated.values():
            node.updated = True
    
    def update_selected_obj(self):
        if(self.select_object):
            if(isinstance(self.selected_obj, Node)):
                self.selected_obj.update(pos=self.app.mouse_pos)
            elif(isinstance(self.selected_obj, Edge)):
                edge = Pseudo_edge(self.selected_obj.n1, self.selected_obj.n2.pos)
                self.objects.remove(self.selected_obj)
                self.edges.remove(self.selected_obj)

                del self.selected_obj
                self.selected_obj = None
                self.selected_obj = edge

                return 'creating_edge'
            elif(isinstance(self.selected_obj, Pseudo_edge)):
                self.selected_obj.update(self.app.mouse_pos)

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

    def topoSort(self):
        nodes = [node.id for node in self.nodes.values()]
        n = len(nodes)
        q = deque()
        deg = [0] * n
        sorted_graph = []

        for i in nodes:
            for it in self.nodes[i].adjacency_list:
                deg[it.id]+=1

        for i in nodes:
            if(deg[i] == 0):
                q.append(i)

        while(len(q) > 0):
            v = q[0]
            q.popleft()
            sorted_graph.append(self.nodes[v])
            for to in self.nodes[v].adjacency_list:
                deg[to.id]-=1
                if(deg[to.id] == 0):
                    q.append(to.id)

        if (len(sorted_graph) != len (nodes)):
            print("Contem ciclo")
        return sorted_graph
    
    def assign_levels(self):
        level = {}
        topoSorted = self.topoSort()
        for node in topoSorted:
            if(len(node.predecessors) > 0):
                level[node.id] = max(level[p.id] for p in node.predecessors) + 1
            else:
                level[node.id] = 1
        return level

    def group_by_level(self):
        nodes_with_level = self.assign_levels()
        nodes_per_level = {}

        for node, lv in nodes_with_level.items():
            if (lv not in nodes_per_level):
                nodes_per_level[lv] = []
            nodes_per_level[lv].append(self.nodes[node])

        nodes_per_height = self.app.screen_size[1]//len(nodes_per_level)
        nodes_per_width = self.app.screen_size[0]//(self.node_radius+2)

        bound = 5
        y = 10 + self.node_radius
        for level in nodes_per_level:
            qtd = self.app.screen_size[0]//(len(nodes_per_level[level])+1)

            x = qtd
            for node in nodes_per_level[level]:
                node.update([x,y])
                x += qtd
            y += nodes_per_height




    def update(self):
        self.update_edges()

    def render(self, screen):
        if (isinstance(self.selected_obj, Pseudo_edge)):
            self.selected_obj.render(self.edge_color, screen)
        if(self.visited):
            for i in self.visited:
                node = self.nodes[i]
                if(self.visited[i]):
                    node.render(self.node_radius, self.visited_node_width, self.visited_node_color, screen)
                else:
                    node.render(self.node_radius, self.node_width, self.node_color, screen)

        else:
            for node in self.nodes.values():
                node.render(self.node_radius, self.node_width, self.node_color, screen)

        for edge in self.edges:
            edge.render(self.edge_color, screen)

    
            

    