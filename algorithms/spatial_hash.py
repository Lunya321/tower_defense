class SpatialHash:

    def __init__(self, cell_size=80):
        self.cell_size = cell_size
        self.grid = {}

    def _get_cell(self, x, y):
        return int(x // self.cell_size), int(y // self.cell_size)

    def clear(self):
        self.grid.clear()

    def insert(self, entity):
        cx, cy = self._get_cell(entity.pos.x, entity.pos.y)
        cell_key = (cx, cy)
        if cell_key not in self.grid:
            self.grid[cell_key] = []
        self.grid[cell_key].append(entity)

    def get_nearby(self, x, y, radius):
        start_cx, start_cy = self._get_cell(x - radius, y - radius)
        end_cx, end_cy = self._get_cell(x + radius, y + radius)
        nearby_entities = []
        for cx in range(start_cx, end_cx + 1):
            for cy in range(start_cy, end_cy + 1):
                cell_key = (cx, cy)
                if cell_key in self.grid:
                    nearby_entities.extend(self.grid[cell_key])
        return nearby_entities