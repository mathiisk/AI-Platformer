import level_load
import unittest

class TestLoadLevel(unittest.TestCase):

	def test_non_existent_lv(self):
		"""This test gurantes if we can only read levels that are currently in our levels_layout folder"""
		with self.assertRaises(FileNotFoundError):
			level_load.load_level(15, 64)
		"""This test makes sures that tile sizes which are <0 are not accepted"""
	def test_negative_tile_size(self):
		with self.assertRaises(ValueError):
			level_load.load_level(1, -5)
		"""This test makes sures that the tile size which is exactly 0 is not accepted"""
	def test_zero_tile_size(self):
		with self.assertRaises(ValueError):
			level_load.load_level(1, 0)


if __name__ == '__main__':
    unittest.main()
