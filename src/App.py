import pygame as pg
from src.Graph import Graph
from src.StoppableThread import StoppableThread
from collections import deque
import numpy as np
import time
from src.Logic import Logic


class App:
    def __init__(self, screen_width = 1280, screen_height= 720, main_path=None):
        pg.init()
        self.screen_size = np.array([screen_width, screen_height])
        self.screen = pg.display.set_mode(self.screen_size, pg.HWSURFACE | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.mouse_pos = pg.mouse.get_pos()
        self.font = pg.font.Font(None, 30)
        self.running = True
        self.dir = main_path
        self.origin = np.array([self.screen_size[0], self.screen_size[1]/2])

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
        

    def render(self):
        self.screen.fill((255, 255, 255))

        self.graph.render(self.screen)
        
        pg.display.update()
        self.clock.tick(60)
    
    def start(self):
        self.graph = Graph(self)
        self.logic = Logic(self, self.graph)
        
        self.logic.start_loop()

        while (self.running):
            self.poll_event()
            self.render()

        pg.quit()
    
