import threading
import time
import pygame as pg
from src.Graph import Graph
import os

DOUBLE_CLICK_TIME = 0.2
ALGORITHM_SLEEP = 0.5

class Logic:
    # This will run in another thread
    def __init__(self, app, graph):
        self._last_click_time = 0
        self.flags = {'creating_edge' : False, 'moving_obj' : False}

        # Threaded fields -> Those accessible from other threads
        self.app = app
        self.graph = graph
        self.input_list = []  # A list of commands to queue up for execution
        self.mouse_status = 'FREE'
        self.keyboard_status = 'FREE'
        self.event = None

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
                elif (ev.type == pg.KEYUP):
                    self.keyboard_status = 'FREE'
                elif(ev.type == pg.MOUSEBUTTONDOWN):
                    self.mouse_click_event()
                elif(ev.type == pg.MOUSEBUTTONUP):
                    self.mouse_release_event()

            with self.lock:  # Again we call the lock because we're editing
                self.event_handler()
            self.graph.update()


    def start_loop(self):
        # We spawn a new thread using our _loop method, the loop has no additional arguments,
        # We call daemon=True so that the thread dies when main dies
        threading.Thread(target=self._loop,
                         args=(),
                         daemon=True).start()
        
    def event_handler(self):
        self.update_events_by_key()
        self.update_events_by_mouse()
        
        if(self.event):
            event = getattr(self, self.event, None)
            if(event):   
                event()
        self.event = None

    def mouse_click_event(self):
        current_time = time.time()
        if (current_time - self._last_click_time <= DOUBLE_CLICK_TIME):
            self.mouse_status = 'DOUBLE_CLICK'
            self._last_click_time = current_time
        elif(self.mouse_status == 'FREE'):
            self.mouse_status = 'CLICK'
        self._last_click_time = current_time

    def mouse_release_event(self):
        if (self.flags['creating_edge']):
            with self.lock:
                self.check_created_edge()
                self.flags['creating_edge'] = False
                self.keyboard_status = 'FREE'
        self.mouse_status = 'FREE'
        self.event = 'release_object'

    def update_events_by_key(self):
        key = self.keyboard_status
        if(key == 'NEW_EDGE' and self.flags['creating_edge'] == False):
            self.event = 'create_edge'
        elif(key == pg.K_DELETE):
            self.event = 'delet_object'
        elif(key == pg.K_d):
            self.event = 'DFS'
        elif(key == pg.K_b):
            self.event = 'BFS'
        elif(key == pg.K_s):
            self.event = 'graph_from_adjacencys'
        self.keyboard_status = 'FREE'
        
    def update_events_by_mouse(self):
        if (self.mouse_status == 'CLICK'):
            self.event = 'select_object'
            self.mouse_status = 'HELD'
        elif(self.mouse_status == 'DOUBLE_CLICK'):
            self.event = 'create_node'
            self.mouse_status = 'HELD'
        elif(self.mouse_status == 'HELD'):
            self.event = 'update_object'
            self.flags['moving_obj'] = True

    def update(self):
        self.graph.update()
        
    def create_node(self):
        self.graph.add_node()

    def create_edge(self):
        self.flags['creating_edge'] = True
        self.graph.add_edge()
        self.mouse_status = 'HELD'

    def select_object(self):
        self.graph.select_object()

    def delet_object(self):
        self.graph.delete_selected_obj()

    def release_object(self):
        self.flags['moving_obj'] = False

    def update_object(self):
        if(self.flags['moving_obj']):
            f = self.graph.update_selected_obj()
            if (f == 'creating_edge'):
                self.flags['creating_edge'] = True
    
    def check_created_edge(self):
        self.graph.check_created_edge()

    def DFS(self):
        threading.Thread(target=self.graph.dfs,
                         args=[ALGORITHM_SLEEP],
                         daemon=True).start()
        
    def BFS(self):
        threading.Thread(target=self.graph.bfs,
                         args=[ALGORITHM_SLEEP],
                         daemon=True).start()

    def graph_from_adjacencys(self):
        adjancecys = []
        with open(os.path.join(self.app.dir, 'adjacency_list.txt'), 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    u, v = map(int, line.split())
                    adjancecys.append([u, v])

        self.graph.from_adjacency_list(adjancecys)