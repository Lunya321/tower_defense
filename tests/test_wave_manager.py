import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.wave_manager import WaveManager


class MockPath:
    def __init__(self):
        self.path = [(0, 1), (1, 1), (2, 1), (3, 1)]


def test_wave_manager_initial_state():
    path = MockPath().path
    manager = WaveManager(path, 40)
    
    assert manager.current_wave == 1
    assert manager.is_active is False
    assert len(manager.enemies_queue) == 0


def test_wave_manager_starts_wave():
    path = MockPath().path
    manager = WaveManager(path, 40)
    
    manager.update(6.0, 0)
    
    assert manager.is_active is True


def test_wave_manager_spawns_enemies():
    path = MockPath().path
    manager = WaveManager(path, 40)
    
    manager.update(6.0, 0)
    
    enemy = manager.update(1.5, 0)
    
    assert enemy is not None
    assert enemy.is_alive is True


def test_wave_manager_increments_wave():
    path = MockPath().path
    manager = WaveManager(path, 40)
    
    manager.update(6.0, 0)
    
    while True:
        enemy = manager.update(1.5, 0)
        if enemy is None:
            break
    
    manager.update(0.1, 0)
    
    assert manager.current_wave == 2