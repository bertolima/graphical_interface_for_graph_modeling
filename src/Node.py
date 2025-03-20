import pygame as pg
import numpy as np
import time

class Node:
    def __init__(self, pos, name, color):
        self.pos = np.array(pos)
        self.name = name
        self.color = color
        self.width = 2
        self.radius = None
        self.rect = None
        self.label = None
        self.adjacency_list = []

    def create_label(self, text_generator, text_color):
        self.label = text_generator.render(str(self.name), True, text_color)
    
    def update(self, radius=None, pos=None):
        if (pos):
            self.pos = np.array(pos)
        if (self.radius != radius):
            self.radius = radius

    def render(self, renderer_screen:pg.Surface):
        self.rect = pg.draw.circle(renderer_screen, self.color, self.pos, self.radius, width=self.width)
        text_rect = self.label.get_rect(center=self.pos)
        renderer_screen.blit(self.label, text_rect)
        
    def check(self, point):
        return self.rect.collidepoint(point)
    
    def dfs(self, visited, color, width):
        visited[self.name] = True
        c = list(self.color)
        w = int(self.width)
        self.color = color
        self.width = width
        time.sleep(0.5)
        for node in self.adjacency_list:
            if(not visited[node.name]):
                node.dfs(visited, color, width)
        self.color = c
        self.width = w
