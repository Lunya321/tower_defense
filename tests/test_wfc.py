import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.wfc import WaveFunctionCollapse


def test_wfc_generates_valid_grid():
    wfc = WaveFunctionCollapse(width=20, height=15)
    grid = None
    for _ in range(20):
        grid = wfc.generate()
        if grid is not None:
            break
    
    assert grid is not None
    assert len(grid) == 15
    assert all(len(row) == 20 for row in grid)


def test_wfc_has_spawn_and_base():
    wfc = WaveFunctionCollapse(width=20, height=15)
    grid = None
    for _ in range(20):
        grid = wfc.generate()
        if grid is not None:
            break
    
    assert grid is not None
    spawn_count = sum(row.count(3) for row in grid)
    base_count = sum(row.count(4) for row in grid)
    
    assert spawn_count == 1
    assert base_count == 1


def test_wfc_spawn_on_left_edge():
    wfc = WaveFunctionCollapse(width=20, height=15)
    grid = None
    for _ in range(20):
        grid = wfc.generate()
        if grid is not None:
            break
    
    assert grid is not None
    for y, row in enumerate(grid):
        if 3 in row:
            spawn_x = row.index(3)
            assert spawn_x == 0


def test_wfc_base_on_right_edge():
    wfc = WaveFunctionCollapse(width=20, height=15)
    grid = None
    for _ in range(20):
        grid = wfc.generate()
        if grid is not None:
            break
    
    assert grid is not None
    for y, row in enumerate(grid):
        if 4 in row:
            base_x = row.index(4)
            assert base_x == 19


def test_wfc_only_valid_tiles():
    wfc = WaveFunctionCollapse(width=20, height=15)
    grid = None
    for _ in range(20):
        grid = wfc.generate()
        if grid is not None:
            break
    
    assert grid is not None
    valid_tiles = {0, 1, 2, 3, 4}
    for row in grid:
        for tile in row:
            assert tile in valid_tiles