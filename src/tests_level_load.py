from game import level_load
import unittest

class TestLoadLevel(unittest.TestCase):

        def test_non_existent_lv(self):
                """This test guarantees levels must exist in the layout folder."""
                with self.assertRaises(FileNotFoundError):
                        level_load.load_level(15, 64)

        def test_negative_tile_size(self):
                """This test makes sure that tile sizes <0 are rejected."""
                with self.assertRaises(ValueError):
                        level_load.load_level(1, -5)

        def test_zero_tile_size(self):
                """This test makes sure that a tile size of 0 is rejected."""
                with self.assertRaises(ValueError):
                        level_load.load_level(1, 0)


if __name__ == '__main__':
    unittest.main()
