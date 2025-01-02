import numpy as np

class ContourGenerator: 

    def __init__(self, binary_image, width, height): 
        self.neighbors = [(-1, -1), (0, -1), (1, -1),
                          (-1,  0), (1,  0), (-1,  1), 
                          (0,  1), (1,  1)]
        self.binary_image = binary_image
        self.width = width
        self.height = height

    def is_boundary_pixel(self, x, y): 
        if not self.binary_image[y][x]: 
            return False

        for dx, dy in self.neighbors: 
            nx, ny = x + dx, y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height): 
                return True
            if not self.binary_image[ny][nx]: 
                return True
        
        return False

    def find_contours(self): 
        visited = np.zeros((self.height, self.width), dtype=bool)
        result_contours = []

        for y in range(self.height): 
            for x in range(self.width): 
                if not self.binary_image[y][x] or visited[y][x]: 
                    continue
                if not self.is_boundary_pixel(x, y): 
                    continue

                boundary = self.find_moore_trace((x, y), visited)
                if len(boundary) > 2: 
                    result_contours.append(boundary)
        
        return result_contours

    def find_moore_trace(self, start_point, visited): 
        result_boundary = [start_point]
        x_start, y_start = start_point
        visited[y_start][x_start] = True

        prev_direction = 7
        current_point = start_point
        while True: 
            search_direction = (prev_direction + 1) % 8
            found_next = False

            for i in range(8): 
                dir_idx = (search_direction + i) % 8
                dx, dy = self.neighbors[dir_idx]
                nx, ny = current_point[0] + dx, current_point[1] + dy

                if (0 <= nx < self.width and 
                    0 <= ny < self.height and
                    self.binary_image[ny][nx] and
                    not visited[ny][nx]): 
                    result_boundary.append((nx, ny))
                    visited[ny][nx] = True
                    prev_direction = (dir_idx + 5) % 8
                    current_point = (nx, ny)
                    found_next = True
                    break
                                    
            if not found_next or current_point == start_point: 
                break
                        
        return result_boundary