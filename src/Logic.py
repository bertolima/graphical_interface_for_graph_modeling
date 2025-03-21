import threading
import time
import pygame as pg
from src.Graph import Graph

DOUBLE_CLICK_TIME = 0.2

EVENTS = ['DOUBLE_CLICK', 'MOUSE_UP', 'CLICK']


class Logic:
    # This will run in another thread
    def __init__(self, game):
        self._last_click_time = 0
        self.creating_edge = False

        # Threaded fields -> Those accessible from other threads
        self.game = game
        self.graph = Graph()
        self.input_list = []  # A list of commands to queue up for execution
        self.mouse_status = 'FREE'
        self.keyboard_status = 'FREE'
        self.algorithm_sleep = 0.5
        self.algorithm = None


        # A lock ensures that nothing else can edit the variable while we're changing it
        self.lock = threading.Lock()

    def _loop(self):
        time.sleep(0.5)  # Wait a bit to let things load
        # We're just going to kill this thread with the main one so it's fine to just loop forever
        while True:
            # Check for commands
            time.sleep(0.005)  # Limit the logic loop running to every 10ms

            if len(self.input_list) > 0:

                with self.lock:  # The lock is released when we're done
                    # If there is a command we pop it off the list
                    ev:pg.event.Event = self.input_list.pop(0)
                if (ev == 'LSHIT+LEFT_MOUSE'):
                    self.keyboard_status = 'NEW_EDGE'
                elif (ev.type == pg.KEYDOWN):
                    self.keyboard_status = ev.key
                elif(ev.type == pg.MOUSEBUTTONDOWN):
                    self.mouse_click_event()
                elif(ev.type == pg.MOUSEBUTTONUP):
                    self.mouse_release_event()

            with self.lock:  # Again we call the lock because we're editing
                self.update()
            self.run_algorithm()


    def start_loop(self):
        # We spawn a new thread using our _loop method, the loop has no additional arguments,
        # We call daemon=True so that the thread dies when main dies
        threading.Thread(target=self._loop,
                         args=(),
                         daemon=True).start()
        
    def mouse_click_event(self):
        current_time = time.time()
        if (current_time - self._last_click_time <= DOUBLE_CLICK_TIME):
            self.mouse_status = 'DOUBLE_CLICK'
            self._last_click_time = current_time
        else:
            self.mouse_status = 'CLICK'
        self._last_click_time = current_time

    def mouse_release_event(self):
        if(self.creating_edge):
            self.check_created_edge()
            self.creating_edge = False
            self.keyboard_status = 'FREE'
        self.mouse_status = 'FREE'

    def events_by_key(self):
        key = self.keyboard_status
        if(key == 'NEW_EDGE' and self.creating_edge == False):
            self.create_edge_event()
            self.creating_edge = True
        elif(key == pg.K_DELETE):
            self.delete_selected_obj_event()
            self.keyboard_status = 'FREE'
        elif(key == pg.K_d):
            self.algorithm = 'DFS'
            self.keyboard_status = 'FREE'
        elif(key == pg.K_b):
            self.algorithm = 'BFS'
            self.keyboard_status = 'FREE'

    def events_by_mouse(self):
        if (self.mouse_status == 'CLICK'):
            self.select_movable_obj_event()
            self.mouse_status = 'HELD'
        elif(self.mouse_status == 'DOUBLE_CLICK'):
            self.create_node_event()
            self.mouse_status = 'FREE'
        elif(self.mouse_status == 'HELD'):
            pass
        elif(self.mouse_status == 'FREE'):
            self.graph.selected_obj = None

    def run_algorithm(self):
        if(self.algorithm == 'DFS'):
            threading.Thread(target=self.graph.dfs,
                         args=[self.algorithm_sleep],
                         daemon=True).start()
            
        if(self.algorithm == 'BFS'):
            threading.Thread(target=self.graph.bfs,
                         args=[self.algorithm_sleep],
                         daemon=True).start()
            

        self.algorithm = None


    def update(self):
        self.events_by_key()
        self.events_by_mouse()
        self.graph.update(self.game.node_radius, self.game.mouse_pos, self.game.arrow_size)
        
    def create_node_event(self):
        self.graph.add_node(self.game.mouse_pos, self.game.font)

    def create_edge_event(self):
        self.graph.add_edge(self.game.mouse_pos)
        self.mouse_status = 'HELD'

    def select_movable_obj_event(self):
        self.graph.select_object(self.game.mouse_pos)

    def delete_selected_obj_event(self):
        self.graph.delete_selected_obj()
    
    def check_created_edge(self):
        self.graph.check_created_edge(self.game.mouse_pos)

    def update_app_variables(self):
        self.game.mouse_pos = pg.mouse.get_pos()