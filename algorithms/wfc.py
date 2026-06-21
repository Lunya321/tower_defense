import random

class WaveFunctionCollapse:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.rules = {
            0: {
                0: {0, 1, 2, 3, 4},
                1: {0, 1, 2, 3, 4},
                2: {0, 1, 2, 3, 4},
                3: {0, 1, 2, 3, 4},
                4: {0, 1, 2, 3, 4},
            },
            1: {
                0: {0, 1, 3, 4},
                1: {0, 1, 3, 4},
                2: {0, 1, 3, 4},
                3: {0, 1, 3, 4},
                4: {0, 1, 3, 4},
            },
            2: {
                0: {0, 2},
                1: {0, 2},
                2: {0, 2},
                3: {0, 2},
                4: {0, 2},
            },
            3: {
                0: {0, 1, 2, 3, 4},
                1: {1},
                2: {0, 1, 2, 3, 4},
                3: {0, 1, 2, 3, 4},
            },
            4: {
                0: {0, 1, 2, 3, 4},
                1: {0, 1, 2, 3, 4},
                2: {0, 1, 2, 3, 4},
                3: {1},
            },
        }

    def generate(self):
        grid = [
            [{0, 2} for _ in range(self.width)] for _ in range(self.height)
        ]
        
        spawn_y = self.height // 2
        base_y = self.height // 2
        
        spawn_pos = (0, spawn_y)
        base_pos = (self.width - 1, base_y)

        path = self._generate_winding_path(spawn_pos, base_pos)
        
        for x, y in path:
            grid[y][x] = {1}

        grid[spawn_y][0] = {3}
        grid[base_y][self.width - 1] = {4}

        queue = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if len(grid[y][x]) == 1
        ]
        
        if not self._propagate(grid, queue):
            return None

        while True:
            min_entropy = 999
            choices = []
            for y in range(self.height):
                for x in range(self.width):
                    w = len(grid[y][x])
                    if w > 1:
                        if w < min_entropy:
                            min_entropy = w
                            choices = [(x, y)]
                        elif w == min_entropy:
                            choices.append((x, y))

            if not choices:
                break

            cx, cy = random.choice(choices)
            tile = random.choice(list(grid[cy][cx]))
            grid[cy][cx] = {tile}

            if not self._propagate(grid, [(cx, cy)]):
                return None

        return [[list(cell)[0] for cell in row] for row in grid]

    def _generate_winding_path(self, start, end):
        path = [start]
        cx, cy = start
        
        cx += 1
        path.append((cx, cy))
        
        x1 = self.width // 4
        x2 = self.width // 2
        x3 = (3 * self.width) // 4
        
        checkpoints = [
            (x1, random.randint(2, self.height - 3)),
            (x2, random.randint(2, self.height - 3)),
            (x3, random.randint(2, self.height - 3)),
            (end[0] - 1, end[1])
        ]
        
        for tx, ty in checkpoints:
            while cx < tx:
                cx += 1
                path.append((cx, cy))
            while cy < ty:
                cy += 1
                path.append((cx, cy))
            while cy > ty:
                cy -= 1
                path.append((cx, cy))
        
        while cx < end[0]:
            cx += 1
            path.append((cx, cy))
        
        return path

    def _propagate(self, grid, queue):
        dirs = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}
        while queue:
            cx, cy = queue.pop(0)
            for d, (dx, dy) in dirs.items():
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    current_allowed = grid[cy][cx]
                    possible_neighbors = set()
                    for t in current_allowed:
                        possible_neighbors.update(self.rules[t][d])

                    neighbor_set = grid[ny][nx]
                    constrained = neighbor_set.intersection(
                        possible_neighbors
                    )
                    if not constrained:
                        return False
                    if constrained != neighbor_set:
                        grid[ny][nx] = constrained
                        if (nx, ny) not in queue:
                            queue.append((nx, ny))
        return True