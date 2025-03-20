import pygame as pg
from src.Graph import Graph
from src.StoppableThread import StoppableThread
from collections import deque
import time

DOUBLE_CLICK_TIME = 0.2

class App:
    def __init__(self, screen_width = 1280, screen_height= 720):
        self.width, self.height = screen_width, screen_height
        self.screen = None
        self.running = None
        self.clock = None
        self.last_click_time = 0
        self.radius = 30
        self.mouse_pos = None
        self.graph = None
        self.events = {}
        self.font = None
        self.algorithm = None
        self.process = deque()

        self.init()
 
    def init(self):
        pg.init()
        self.init_variables()
        self.init_renderer_screen()
        self.init_event_handlers()
        self.init_variables()

    def init_variables(self):
        self.screen_size = [self.width, self.height]
        self.running = True
        self.clock = pg.time.Clock()
        self.mouse_pos = pg.mouse.get_pos()
        self.font = pg.font.Font(None, 30)
        self.graph = Graph()

    def init_renderer_screen(self):
        self.screen = pg.display.set_mode(self.screen_size, pg.HWSURFACE | pg.DOUBLEBUF)

    def init_event_handlers(self):
        self.events['CREATE_NODE'] = False
        self.events['BLOCK_CREATE_EDGE'] = False
        self.events['MOVING_OBJ'] = False

    def poll_event(self):
        self.mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():

            keys = pg.key.get_pressed()
            mouse = pg.mouse.get_pressed()

            if (event.type == pg.QUIT):
                self.running = False
    
            if(keys[pg.K_LSHIFT] and mouse[0]):
                    self.create_edge_event()
                    self.events['BLOCK_CREATE_EDGE'] = True
                    self.events['MOVING_OBJ'] = True

            elif (event.type == pg.MOUSEBUTTONDOWN):
                if (event.button == 1):  # 1 é o botão esquerdo do mouse
                    if (self.double_click_event()):
                        self.create_node_event()
                    else:
                        self.select_movable_obj_event()
                        self.events['MOVING_OBJ'] = True

            if(keys[pg.K_DELETE]):
                self.delete_selected_obj_event()

            if(keys[pg.K_d]):
                self.algorithm = True
                
            if (event.type == pg.MOUSEBUTTONUP):
                self.events['MOVING_OBJ'] = False
                if(self.events['BLOCK_CREATE_EDGE']):
                    self.events['BLOCK_CREATE_EDGE']= False
                    self.check_created_edge()
                
                self.shift_pressed = False
                self.target_node = None

    def double_click_event(self):
        current_time = time.time()
        if (current_time - self.last_click_time <= DOUBLE_CLICK_TIME):
            self.last_click_time = current_time
            return True
        self.last_click_time = current_time
        return False
    
    def create_node_event(self):
        self.graph.add_node(self.mouse_pos, self.font)

    def create_edge_event(self):
        if(self.events['BLOCK_CREATE_EDGE'] == False):
            self.graph.add_edge(self.mouse_pos)

    def select_movable_obj_event(self):
        self.graph.select_object(self.mouse_pos)

    def delete_selected_obj_event(self):
        self.graph.delete_selected_obj()
    
    def check_created_edge(self):
        self.graph.check_created_edge(self.mouse_pos)

    def update_selected_obj(self):
        if (self.events['MOVING_OBJ']):
            self.graph.update_selected_obj(self.radius, self.mouse_pos)

    def run_algorithm(self):
        if (self.algorithm):
            algorithm_thread = StoppableThread(target=self.graph.dfs)
            algorithm_thread.start()
            self.process.append(algorithm_thread)
            self.algorithm = None

    def update(self):
        self.poll_event()
        self.run_algorithm()
        self.update_selected_obj()
        self.graph.update(self.radius)

    def render(self):
        self.screen.fill((255, 255, 255))  # Fill screen with white

        self.graph.render(self.screen)
        
        pg.display.update()
        self.clock.tick(60)
    

    def close_app(self):
        for process in self.process:
            process.stop()
        for process in self.process:
            process.join()
        pg.quit()

    
