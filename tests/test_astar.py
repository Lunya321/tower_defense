import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.astar import a_star_search, manhattan_distance


class MockGridModel:
    def __init__(self, grid):
        self.grid = grid

    def get_tile(self, x, y):
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x]
        return -1


def test_manhattan_distance():
    assert manhattan_distance((0, 0), (3, 4)) == 7
    assert manhattan_distance((1, 1), (1, 1)) == 0
    assert manhattan_distance((5, 2), (2, 5)) == 6


def test_astar_straight_path():
    grid = [
        [0, 0, 0, 0, 0],
        [3, 1, 1, 1, 4],
        [0, 0, 0, 0, 0],
    ]
    model = MockGridModel(grid)
    path = a_star_search(model, (0, 1), (4, 1))
    
    assert path is not None
    assert len(path) > 0
    assert path[0] == (0, 1)
    assert path[-1] == (4, 1)
    assert len(path) == 5


def test_astar_no_path():
    grid = [
        [0, 0, 0, 0, 0],
        [3, 1, 2, 1, 4],
        [0, 0, 0, 0, 0],
    ]
    model = MockGridModel(grid)
    path = a_star_search(model, (0, 1), (4, 1))
    
    assert path is None or len(path) == 0


def test_astar_diagonal_avoidance():
    grid = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 2, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    model = MockGridModel(grid)
    path = a_star_search(model, (0, 0), (4, 4))
    
    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)