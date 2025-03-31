import pygame as pg
import numpy as np

class Pseudo_edge:
    def __init__(self, n1, pos):
        self.n1 = n1
        self.start = n1.pos
        self.end = pos

    def update(self, pos):
        self.end = pos

    def render(self, color, screen):
        pg.draw.aaline(screen, color, self.start, self.end)

class Edge:
    def __init__(self, n1, n2, origin, node_radius, arrow_size, directed = True):
        self.n1 = n1
        self.n2 = n2
        self.start = n1.pos
        self.end = n2.pos

        self.directed = directed

        self.boundaries_size = 5
        self.arrow = None
        self.angle = None
        self.rect = None

        self.update(node_radius, arrow_size, origin)

    def calculate_angle(self, origin_direction):

        mine_direction =  self.n2.pos - self.n1.pos

        dot_product = np.dot(origin_direction, mine_direction)

        origin_norm = np.linalg.norm(origin_direction)
        mine_norm = np.linalg.norm(mine_direction)

        angle = np.arccos(dot_product / (origin_norm * mine_norm))

        cross = np.cross(origin_direction, mine_direction)

        if (cross > 0):
            angle = np.pi*2-angle

        return angle

    def update_edge_boundaries(self, origin_direction):
        self.angle = self.calculate_angle(origin_direction)

        p1_min_x, p1_max_x = self.start[0] - np.sin(self.angle) * self.boundaries_size, self.start[0] + np.sin(self.angle) * self.boundaries_size
        p1_min_y, p1_max_y = self.start[1] - np.cos(self.angle) * self.boundaries_size, self.start[1] + np.cos(self.angle) * self.boundaries_size
        p2_min_x, p2_max_x = self.end[0] - np.sin(self.angle) * self.boundaries_size, self.end[0] + np.sin(self.angle) * self.boundaries_size
        p2_min_y, p2_max_y = self.end[1] - np.cos(self.angle) * self.boundaries_size, self.end[1] + np.cos(self.angle) * self.boundaries_size

        self.rect = np.array([
            [p1_min_x, p1_min_y],
            [p1_max_x, p1_max_y],
            [p2_max_x, p2_max_y],
            [p2_min_x, p2_min_y],
        ])
    

    def update_position(self, radius, arrow_size):
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

    def update(self, radius, arrow_size, origin_direction):
        self.update_position(radius, arrow_size)
        self.update_edge_boundaries(origin_direction)

    def check(self, point):
        inside = False
        x, y = point
        # Store the first point in the polygon and initialize the second point
        p1 = self.rect[0]
    
        # Loop through each edge in the polygon
        for i in range(1, 5):
            # Get the next point in the polygon
            p2 = self.rect[i % 4]
    
            # Check if the point is above the minimum y coordinate of the edge
            if y > min(p1[1], p2[1]):
                # Check if the point is below the maximum y coordinate of the edge
                if y <= max(p1[1], p2[1]):
                    # Check if the point is to the left of the maximum x coordinate of the edge
                    if x <= max(p1[0], p2[0]):
                        # Calculate the x-intersection of the line connecting the point to the edge
                        x_intersection = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
    
                        # Check if the point is on the same line as the edge or to the left of the x-intersection
                        if p1[0] == p2[0] or x <= x_intersection:
                            # Flip the inside flag
                            inside = not inside
            p1 = p2

        return inside
    
    def render(self, color, screen):
        pg.draw.aaline(screen, color, self.start, self.end)
        pg.draw.polygon(screen, color, self.arrow)

    