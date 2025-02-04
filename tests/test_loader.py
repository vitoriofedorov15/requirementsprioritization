import unittest
from modules.loader import load_data

class TestLoader(unittest.TestCase):
    def test_load_data(self):
        data = load_data("data/input.csv")
        self.assertIsNotNone(data)

if __name__ == '__main__':
    unittest.main()
