import pygame as pg
from src.Graph import Graph
from src.StoppableThread import StoppableThread
from collections import deque
import numpy as np
import time
from src.Logic import Logic


class App:
    def __init__(self, screen_width = 1280, screen_height= 720):
        pg.init()
        self.width, self.height = screen_width, screen_height
        self.size = [self.width, self.height]
        self.screen_size = [self.width, self.height]

        self.node_radius = 30

        self.node_color = [0,0,0]
        self.visited_node_color = [239, 239, 38]
        self.edge_color = [0,0,0]

        self.node_width = 2
        self.visited_node_width = 2
        self.edge_width = 2

        self.arrow_size = 10

        self.screen = pg.display.set_mode(self.screen_size, pg.HWSURFACE | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.mouse_pos = pg.mouse.get_pos()
        self.font = pg.font.Font(None, 30)
        self.running = True

    def poll_event(self):
        self.mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                    self.running = False

            elif(pg.key.get_pressed()[pg.K_LSHIFT] and pg.mouse.get_pressed()[0]):
                with self.logic.lock:
                    self.logic.input_list.append('LSHIT+LEFT_MOUSE')

            else:
                with self.logic.lock:
                    self.logic.input_list.append(event)

    def render_graph(self):
        nodes = self.logic.graph.nodes
        edges = self.logic.graph.edges
        visited = self.logic.graph.visited

        if(visited):
            for i in visited:
                node = nodes[i]
                if(visited[i]):
                    node.rect = pg.draw.circle(self.screen, self.visited_node_color, node.pos, self.node_radius, self.visited_node_width)
                    self.screen.blit(node.label, node.label.get_rect(center=node.pos))
                else:
                    node.rect = pg.draw.circle(self.screen, self.node_color, node.pos, self.node_radius, self.node_width)
                    self.screen.blit(node.label, node.label.get_rect(center=node.pos))

        else:
            for node in nodes.values():
                node.rect = pg.draw.circle(self.screen, self.node_color, node.pos, self.node_radius, self.node_width)
                self.screen.blit(node.label, node.label.get_rect(center=node.pos))

        for edge in edges:
            if(edge.arrow):
                edge.rect = pg.draw.line(self.screen, self.edge_color, edge.start, edge.end, width=self.edge_width)
                pg.draw.polygon(self.screen, self.edge_color, edge.arrow)
            else:
                edge.rect = pg.draw.line(self.screen, self.edge_color, edge.start, edge.end, width=self.edge_width)

    def render(self):
        self.screen.fill((255, 255, 255))

        self.render_graph()
        
        pg.display.update()
        self.clock.tick(60)
    
    def start(self):
        self.logic = Logic(self)
        self.logic.start_loop()
        while (self.running):
            self.poll_event()
            self.render()
        pg.quit()
    
