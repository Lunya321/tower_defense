import sys
import os
import pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.spatial_hash import SpatialHash


class MockEntity:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)


def test_spatial_hash_insert_and_clear():
    spatial_hash = SpatialHash(cell_size=40)
    entity = MockEntity(50, 50)
    
    spatial_hash.insert(entity)
    assert len(spatial_hash.grid) > 0
    
    spatial_hash.clear()
    assert len(spatial_hash.grid) == 0


def test_spatial_hash_get_nearby():
    spatial_hash = SpatialHash(cell_size=40)
    
    entity1 = MockEntity(50, 50)
    entity2 = MockEntity(60, 60)
    entity3 = MockEntity(200, 200)
    
    spatial_hash.insert(entity1)
    spatial_hash.insert(entity2)
    spatial_hash.insert(entity3)
    
    nearby = spatial_hash.get_nearby(55, 55, 30)
    
    assert entity1 in nearby
    assert entity2 in nearby
    assert entity3 not in nearby


def test_spatial_hash_empty_query():
    spatial_hash = SpatialHash(cell_size=40)
    
    nearby = spatial_hash.get_nearby(100, 100, 50)
    
    assert len(nearby) == 0


def test_spatial_hash_cell_distribution():
    spatial_hash = SpatialHash(cell_size=50)
    
    for i in range(10):
        entity = MockEntity(i * 60, i * 60)
        spatial_hash.insert(entity)
    
    assert len(spatial_hash.grid) >= 5