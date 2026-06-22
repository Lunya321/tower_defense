import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.bfs import find_path_bfs


def test_bfs_straight_line():
    grid = [
        [0, 0, 0],
        [3, 1, 4],
        [0, 0, 0],
    ]
    path = find_path_bfs(grid, (0, 1), (2, 1))
    
    assert path is not None
    assert path[0] == (0, 1)
    assert path[-1] == (2, 1)
    assert len(path) == 3


def test_bfs_winding_path():
    grid = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [3, 1, 1, 1, 4],
    ]
    path = find_path_bfs(grid, (0, 2), (4, 2))
    
    assert path is not None
    assert path[0] == (0, 2)
    assert path[-1] == (4, 2)


def test_bfs_no_path():
    grid = [
        [0, 2, 0],
        [3, 2, 4],
        [0, 2, 0],
    ]
    path = find_path_bfs(grid, (0, 1), (2, 1))
    
    assert path is None


def test_bfs_complex_maze():
    grid = [
        [3, 1, 2, 1, 1],
        [2, 1, 2, 1, 2],
        [1, 1, 1, 1, 4],
    ]
    path = find_path_bfs(grid, (0, 0), (4, 2))
    
    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (4, 2)