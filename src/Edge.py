import pygame as pg
import numpy as np

class Edge:
    def __init__(self, n1, n2=None, pos=[0,0], directed = True):
        self.n1 = n1
        self.n2 = None
        self.start = n1.pos
        self.end = pos
        self.arrow = None
        self.directed = directed

        self.rect = None

    def update(self, radius, arrow_size, pos=None):
        if(self.n2 == None):
            if(pos):
                self.end = pos
        else:
            start, end = self.n1.pos, self.n2.pos
            direction = end - start
            distance = np.linalg.norm(direction)
            if distance == 0:
                self.start, self.end = start, end
            else:
                # Normalize direction vector
                unit_direction = direction / distance

                # Calculate new points at the edge of each circle
                new_p1 = start + unit_direction * radius
                new_p2 = end - unit_direction * radius

                start, end = new_p1, new_p2
                direction = end - start
                distance = np.linalg.norm(direction)

                unit_direction = direction / distance

                perp = np.array([-unit_direction[1], unit_direction[0]])

                arrow_tip = end
                arrow_left = end - (unit_direction * arrow_size) + (perp * (arrow_size / 2))
                arrow_right = end - (unit_direction * arrow_size) - (perp * (arrow_size / 2))

                self.arrow = [arrow_tip, arrow_left, arrow_right]
                self.start, self.end = new_p1, new_p2 

    def check(self, point):
        if(self.rect):
            return self.rect.collidepoint(point)
        return False
    # def render(self, screen):
    #     if(self.arrow):
    #         self.rect = pg.draw.line(screen, (0,0,0), self.start, self.end, width=2)
    #         pg.draw.polygon(screen, (0,0,0), self.arrow)
    #     else:
    #         self.rect = pg.draw.line(screen, (0,0,0), self.start, self.end, width=2)