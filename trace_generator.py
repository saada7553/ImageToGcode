import numpy as np

class TraceGenerator: 

    def __init__(self, binary_image, width: int, height: int): 
        self.neighbors_4 = [(0, 1), (1, 0), (-1, 0), (0, -1)] # up, down, right, left
        self.neighbors_8 = [(0, 1), (1, 0), (1, 1), (0, -1),  
                          (-1, 0), (-1, -1), (-1, 1), (1, -1)] # neighbors_4 + diagonals
        self.binary_image = binary_image
        self.width = width
        self.height = height

    def is_boundary_pixel(self, x: int, y: int) -> bool: 
        """
        A boundary pixel is an ON (1) pixel which is either: 
            1) At the edge of an image.
            OR
            2) 4 directionally adjacent to at least one OFF (0) pixel. 
        """
        if not self.binary_image[y][x]: 
            return False

        for dx, dy in self.neighbors_4: 
            nx, ny = x + dx, y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height): 
                return True
            if not self.binary_image[ny][nx]: 
                return True
        
        return False

    def find_single_moore_trace(self, start_point, visited): 
        """
        A moore trace is a sequence of pixels where: 
            1) each pixel is turned ON (1). 
            2) pixel i and pixel i + 1 are 8-directionally connected
            in the original image. 
        
        This specific trace finder is a modified version of BFS where
        the previously used direction is always preferred. 
        """
        result_trace = [start_point]
        x_start, y_start = start_point
        visited[y_start][x_start] = True

        prev_direction_index = 0
        current_point = start_point
        while True: 
            found_next = False
            
            for i in range(8): 
                new_direction_index = (prev_direction_index + i) % 8
                dx, dy = self.neighbors_8[new_direction_index]
                nx, ny = current_point[0] + dx, current_point[1] + dy

                if (0 <= nx < self.width and 
                    0 <= ny < self.height and
                    self.binary_image[ny][nx] and
                    not visited[ny][nx] and 
                    self.is_boundary_pixel(nx, ny)): 

                    result_trace.append((nx, ny))
                    visited[ny][nx] = True
                    prev_direction_index = new_direction_index
                    current_point = (nx, ny)
                    found_next = True
                    break
                                    
            if not found_next or current_point == start_point: 
                break
                        
        return result_trace
    
    def find_all_moore_traces(self):
        visited = np.zeros((self.height, self.width), dtype=bool)
        result_traces = []

        for y in range(self.height): 
            for x in range(self.width): 
                if not self.binary_image[y][x] or visited[y][x]: 
                    continue

                boundary = self.find_single_moore_trace((x, y), visited)
                if len(boundary) > 2: 
                    result_traces.append(boundary)
        
        return result_traces