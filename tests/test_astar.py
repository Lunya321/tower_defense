import unittest
from models.map_model import MapModel
from algorithms.astar import a_star_search

class TestAStar(unittest.TestCase):
    def setUp(self):
        self.map = MapModel()
        self.start = (0, 1)
        self.goal = (1, 1)

    def test_path_validity(self):
        path = a_star_search(self.map, self.start, self.goal)
        
        self.assertNotEqual(len(path), 0)
        self.assertEqual(path[0], self.start)
        self.assertEqual(path[-1], self.goal)
        
        for point in path:
            self.assertEqual(self.map.get_tile(*point), 1)

if __name__ == '__main__':
    unittest.main()