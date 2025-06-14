import pygame
import numpy as np
from .tiles import *

class Level:
	def __init__(self,tile_size,surface):
		"""
		This function initializes a new Level object.
		It sets up the level using the given surface and tile size.
		"""

		self.display_surface = surface
		self.setup_lv(tile_size)
		self.world_shift=-1

	def wordshift_on(self,switch):
		"""
		This function controls the scrolling of the level.
		By changing the world_shift value, it either allows or prevents the
		scrolling of the level.
		"""

		if switch==1:
			self.world_shift=-1
		elif switch==0:
			self.world_shift=0

	def setup_lv(self,layout):
		"""
		This function is responsible for drawing the level.
		It reads the layout and places world elements
		such as blocks, goals, and spikes accordingly.
		"""

		tile_size = 64
		self.blocks = pygame.sprite.Group()
		self.goals = pygame.sprite.Group()
		self.spikes = pygame.sprite.Group()

		# Blocks
		list_of_cord1=list(zip(*np.where(layout == 1)))
		for block in list_of_cord1:
			x=block[1]*tile_size
			y=block[0]*tile_size
			block=Block((x,y),tile_size)
			self.blocks.add(block)

		# Goal
		list_of_cord9=list(zip(*np.where(layout == 9)))
		for block in list_of_cord9:
				x=block[1]*tile_size
				y=block[0]*tile_size
				goal=Goal((x,y),tile_size)
				self.goals.add(goal)

		# Spikes
		list_of_cord2=list(zip(*np.where(layout == 2)))
		for block in list_of_cord2:
				x=block[1]*tile_size
				y=block[0]*tile_size
				spike=Spike((x - 7,y),tile_size)
				self.spikes.add(spike)

	"""Draw the level"""
	def run(self):
		"""
		This function is responsible for actually drawing the level.
		It ensures that all blocks, spikes, and goals get drawn
		correctly on world shift.
		"""

		self.blocks.update(self.world_shift)
		self.goals.update(self.world_shift)
		self.spikes.update(self.world_shift)
		self.blocks.draw(self.display_surface)
		self.goals.draw(self.display_surface)
		self.spikes.draw(self.display_surface)
