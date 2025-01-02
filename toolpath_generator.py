import math
import numpy as np
from toolpaths import *

class ToolpathGenerator: 
    def __init__(self, contours, scale=0.1, arc_tolerance=1.0): 
        self.contours = contours
        self.scale = scale
        self.arc_tolerance = arc_tolerance
        self.toolpaths = []
    
    def generate_toolpaths(self): 
        for contour in self.contours: 
            scaled_contour = [(x * self.scale, y * self.scale) for (x, y) in contour]
            toolpath = self.integrate_arcs(scaled_contour)
            self.toolpaths.append(toolpath)
        
    def integrate_arcs(self, contour): 
        toolpath = []

        i = 0
        while i < len(contour): 
            curr_window_size = 3 
            max_window_size = min(10, len(contour) - i)

            biggest_fit = None
            biggest_window = curr_window_size

            for size in range(curr_window_size, max_window_size + 1): 
                window_points = contour[i : i + size]
                xc, yc, r = self.least_squares_circle_fit(window_points)

                if xc is None: 
                    break
            
                max_dist = self.calculate_max_distance(window_points, xc, yc, r)
                if max_dist > self.arc_tolerance: 
                    break

                biggest_fit = (xc, yc, r, window_points)
                biggest_window = size
            
            if not biggest_fit: 
                if i + 1 < len(contour): 
                    next_point = contour[i + 1]
                    linear_move = LinearMove(x=next_point[0], y=next_point[1])
                    toolpath.append(linear_move)
                i += 1
                continue
                
            xc, yc, r, window_points = biggest_fit
            start_point, end_point = window_points[0], window_points[-1]

            if len(window_points) >= 3: 
                cross_product = self.cross_product(
                    window_points[0], 
                    window_points[1], 
                    window_points[2])
                clockwise = cross_product < 0
            else: 
                clockwise = True
            
            i_offset = xc - start_point[0]
            j_offset = yc - start_point[1]

            circular_move = ArcMove(
                end_point[0], 
                end_point[1],
                i_offset, 
                j_offset, 
                clockwise
            )
            toolpath.append(circular_move)

            i += biggest_window - 1
        return toolpath
        
    @staticmethod
    def cross_product(point0, point1, point2): 
        return ((point1[0] - point0[0]) * (point2[1] - point0[1]) - 
                (point1[1] - point0[1]) * (point2[0] - point0[0]))

    @staticmethod
    def least_squares_circle_fit(points): 
        x_coordinates = np.array([point[0] for point in points])
        y_coordinates = np.array([point[1] for point in points])
        A = np.c_[2*x_coordinates, 2*y_coordinates, np.ones(len(points))]
        b = x_coordinates**2 + y_coordinates**2

        try: 
            c, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
            xc, yc, c0 = c
            r = math.sqrt(c0 + xc**2 + yc**2)
            return (xc, yc, r)
        except np.linalg.LinAlgError: 
            return (None, None, None)
    
    @staticmethod
    def calculate_max_distance(points, xc, yc, r): 
        distances = [abs(math.hypot(p[0]-xc, p[1]-yc) - r) for p in points]
        return max(distances)