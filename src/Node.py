import pygame as pg
import numpy as np
from src.Utils import get_random_color
import time
from collections import deque

class Node:
    def __init__(self, pos, node_id, text_generator):
        self.pos = np.array(pos)
        self.id = node_id
        self.adjacency_list = []
        self.rect:pg.Rect = None
        self.label = text_generator.render(str(self.id), True, get_random_color())
    
    def update(self, pos=None):
        if (pos):
            self.pos = np.array(pos)
    
    def dfs(self, visited, sleep_time):
        visited[self.id] = True
        print(self.id)
        time.sleep(sleep_time)
        for node in self.adjacency_list:
            if(not visited[node.id]):
                node.dfs(visited, sleep_time)
            time.sleep(sleep_time)
        visited[self.id] = False

    def bfs(self, visited, nodes_stored:deque, sleep_time):
        time.sleep(sleep_time)
        visited[self.id] = True
        nodes_stored.append(self)
        time.sleep(sleep_time)
        

        while(len(nodes_stored) > 0):
            curr = nodes_stored.popleft()

            for x in curr.adjacency_list:
                time.sleep(sleep_time)
                if (not visited[x.id]):
                    visited[x.id] = True
                    nodes_stored.append(x)
                time.sleep(sleep_time)


    def check(self, point):
        if(self.rect):
            return self.rect.collidepoint(point)
        return False
