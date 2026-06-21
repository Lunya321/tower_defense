from algorithms.wfc import WaveFunctionCollapse
from algorithms.bfs import find_path_bfs

class MapModel:

    def __init__(self, width=20, height=15, tile_size=40):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.grid = []
        self.path = []
        self.spawn_pos = (0, height // 2)
        self.base_pos = (width - 1, height // 2)
        self._generate_valid_map()

    def _generate_valid_map(self):
        wfc = WaveFunctionCollapse(self.width, self.height)
        for _ in range(10):
            generated_grid = wfc.generate()
            if generated_grid:
                computed_path = find_path_bfs(
                    generated_grid, self.spawn_pos, self.base_pos
                )
                if computed_path:
                    self.grid = generated_grid
                    self.path = computed_path
                    return

        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.width):
            self.grid[self.spawn_pos[1]][x] = 1
        self.grid[self.spawn_pos[1]][self.spawn_pos[0]] = 3
        self.grid[self.base_pos[1]][self.base_pos[0]] = 4
        self.path = find_path_bfs(self.grid, self.spawn_pos, self.base_pos)

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return -1