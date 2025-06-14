import pygame
from tiles import Block
from tiles import Goal
from tiles import Spike
import unittest

class TestTiles(unittest.TestCase):

	def test_update_block(self):
		'''Check wether the update method work on blocks'''
		block=Block((20,20),1)
		block.update(x_shift=10)
		self.assertEqual(30,block.rect.x)

	def test_update_spike(self):
		'''Check wether the update method work on spikes'''
		spike=Spike((20,20),1)
		spike.update(x_shift=10)
		self.assertEqual(30,spike.rect.x)

	def test_update_goal(self):
		'''Check wether the update method work on the goal'''
		goal=Goal((20,20),1)
		goal.update(x_shift=10)
		self.assertEqual(30,goal.rect.x)
