import math
import numpy as np
from toolpaths import *

class ToolpathGenerator: 
    def __init__(self, traces, scale=1.0, arc_tolerance=1.0): 
        self.traces = traces
        self.scale = scale
        self.arc_tolerance = arc_tolerance
        self.toolpaths = []
    
    def generate_toolpaths(self): 
        for trace in self.traces: 
            scaled_trace = [(x * self.scale, y * self.scale) for (x, y) in trace]
            toolpath = self.integrate_arcs(scaled_trace)
            self.toolpaths.append(toolpath)
        
    def integrate_arcs(self, trace): 
        """
        Parameters:
        - trace: list of (x: int, y: int) coordinares which represents
        a line or curve that we want to draw. 

        Splits traces into multiple toolpaths: 
            1) If a set of points can be represented as a curve, 
            try to 'fit a circle' to that curve. Each original point
            must be within a tolerance distance to the new circle which 
            connects the points. 

            2) If a circle can not be fit to a set of points, 
            fall back and just draw a straight line between the points. 
        """
        toolpath = []

        i = 0
        while i < len(trace): 
            curr_window_size = 3 
            max_window_size = min(10, len(trace) - i)

            biggest_fit = None
            biggest_window = curr_window_size

            # Keep adding points to the current window. 
            # If all the points & generated curve stay within tolerence, try making the circle bigger. 
            for size in range(curr_window_size, max_window_size + 1): 
                window_points = trace[i : i + size]
                x_center, y_center, radius = self.least_squares_circle_fit(window_points)

                if x_center is None: 
                    break
            
                max_dist = self.calculate_max_distance(window_points, x_center, y_center, radius)
                if max_dist > self.arc_tolerance: 
                    break

                biggest_fit = (x_center, y_center, radius, window_points)
                biggest_window = size
            
            # We couldn't fit a circle / curve to the current window of points. 
            # Fallback to using a straight line to connect the points. 
            if not biggest_fit: 
                if i + 1 < len(trace): 
                    next_point = trace[i + 1]
                    linear_move = LinearMove(x=next_point[0], y=next_point[1])
                    toolpath.append(linear_move)
                i += 1
                continue
            
            # We found a circle that fits current points decently well (within tolerance). 
            # Which way does the circle go? (clockwise or counter clockwise)? 
            #   - Use orientation test (theory linked below). 
            x_center, y_center, radius, window_points = biggest_fit
            start_point, end_point = window_points[0], window_points[-1]

            if len(window_points) >= 3: 
                cross_product = self.orientation_test(
                    window_points[0], 
                    window_points[1], 
                    window_points[2])
                clockwise = cross_product < 0
            else: 
                clockwise = True
            
            i_offset = x_center - start_point[0]
            j_offset = y_center - start_point[1]

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
    def orientation_test(point0, point1, point2): 
        """
        Find out if the points form a clockwise or a counter clockwise curve. 
        Theory: https://dccg.upc.edu/people/vera/wp-content/uploads/2012/10/DAG-OrientationTests.pdf
        """
        return ((point1[0] - point0[0]) * (point2[1] - point0[1]) - 
                (point1[1] - point0[1]) * (point2[0] - point0[0]))

    @staticmethod
    def least_squares_circle_fit(points): 
        """
        Try to find a circle whose curve is similar
        to the points within the list. 

        Theory & explained equations: http://www.juddzone.com/ALGORITHMS/least_squares_circle.html
        """
        x_coordinates = np.array([point[0] for point in points])
        y_coordinates = np.array([point[1] for point in points])
        A = np.column_stack((2*x_coordinates, 2*y_coordinates, np.ones(len(points))))
        b = x_coordinates**2 + y_coordinates**2

        try: 
            res, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
            x_center, y_center, c0 = res
            radius = math.sqrt(c0 + x_center**2 + y_center**2)
            return (x_center, y_center, radius)
        except np.linalg.LinAlgError: 
            return (None, None, None)
    
    @staticmethod
    def calculate_max_distance(points, xc, yc, r): 
        distances = [abs(math.hypot(p[0]-xc, p[1]-yc) - r) for p in points]
        return max(distances)
    