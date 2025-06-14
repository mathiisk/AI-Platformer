from player import Player
import unittest
import pygame
from tiles import Block
from tiles import Goal
from tiles import Spike

"""We initialise in order for the sound mixer to work with the player class"""
pygame.init()
class TestPlayer(unittest.TestCase):

	def test_gravity_if_active(self):
		'''Checks that our player cannot move if it is not active.The velocity.y should not change'''
		p=Player((10,10),10,500,550)
		p.velocity.y=5
		p.is_active=False
		p.apply_gravity()
		self.assertEqual(p.velocity.y,5)

	def test_gravity_ensure_max_speed(self):
		'''This test ensures that the maximum speed achieved by falling is set to 10 '''
		p=Player((10,10),10,500,550)
		p.velocity.y=10
		p.is_active=False
		p.apply_gravity()
		self.assertEqual(p.velocity.y,10)

	def test_gravity_into_bottom_of_screen(self):
		''' Checks if the character falls of from the bottom of the screen '''
		p=Player((0,500),10,500,550)
		p.apply_gravity()
		self.assertEqual(p.velocity.y,0)

	def test_jump_off_ground(self):
		"""Test wether the player can jump while off the ground"""
		p=Player((0,500),10,500,550)
		p.on_ground=False
		p.is_active=True
		p.jump()
		self.assertEqual(p.velocity.y,0)

	def test_jump_on_ground(self):
		"""Test wether the player can jump while on the ground"""
		p=Player((0,500),10,500,550)
		p.on_ground=True
		p.is_active=True
		p.jump()
		self.assertEqual(p.velocity.y,p.jump_strength)

	def test_collide_with_tiles_agent_to_obstacle(self):
		"""A simple testcase to check if the horizontal collide check works - part 1"""
		tile=Block((10,10),1)
		tile_group=[tile]
		p=Player((10,10),1,500,550)
		p.velocity.x=100
		p.collide_with_tiles_horizontal(tile_group)
		self.assertEqual(p.velocity.x,0)

	def test_collide_with_tiles_h_nothing_to_collide_to(self):
		"""A simple testcase to check if the horizontal collide check works - part 2"""
		tile=Block((20,20),1)
		tile_group=[tile]
		p=Player((10,10),1,500,550)
		p.velocity.x=100
		p.collide_with_tiles_horizontal(tile_group)
		self.assertEqual(p.velocity.x,100)

	def test_collide_with_tiles_v_agent_to_obstacle(self):
		"""A simple testcase to check if the vertical collide check works - part 1"""
		tile=Block((10,10),1)
		tile_group=[tile]
		p=Player((10,10),1,500,550)
		p.velocity.y=100
		p.collide_with_tiles_vertical(tile_group)
		self.assertEqual(p.velocity.y,0)

	def test_collide_with_tiles_v_nothing_to_collide_to(self):
		"""A simple testcase to check if the vertical collide check works - part 2"""
		tile=Block((20,20),1)
		tile_group=[tile]
		p=Player((10,10),1,500,550)
		p.velocity.y=100
		p.collide_with_tiles_vertical(tile_group)
		self.assertEqual(p.velocity.y,100)

	def test_collide_with_tile_diag(self):
		'''Here we check collision with the corner of a box(diagonal speed vector at the frame that player enters the box)'''
		tile=Block((10,10),1)
		tile_group=[tile]
		p=Player((10,10),1,500,550)
		p.velocity.y=100
		p.velocity.x=100
		p.collide_with_tiles_horizontal(tile_group)
		p.collide_with_tiles_vertical(tile_group)
		self.assertEqual(0,p.velocity.x,p.velocity.y)

	def test_colide_with_goal(self):
		"""Simple test to check the proper work of the goal collision function"""
		goal=Goal((10,10),1)
		goal_group=[goal]
		p=Player((10,10),1,500,550)
		self.assertIs(True,p.collide_with_goal(goal_group))

	def test_colide_with_spike(self):
		"""Simple test to check the proper work of the spike collision function"""
		spike=Spike((10,10),1)
		spike_group=[spike]
		p=Player((10,10),1,500,550)
		self.assertIs(True,p.collide_with_spike(spike_group))

if __name__ == '__main__':
    unittest.main()
