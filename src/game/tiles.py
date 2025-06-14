import pygame

class Block(pygame.sprite.Sprite):
	"""
	This class represents the block tile in the game.
	"""

	def __init__(self,position,size):
		super().__init__()

		#BLOCKS
		self.image = pygame.image.load('../Assets/Block.PNG')
		self.image = pygame.transform.scale(self.image, (size, size))
		self.rect = self.image.get_rect(topleft=position)

	def update(self, x_shift):
		self.rect.x += x_shift

class Goal(pygame.sprite.Sprite):
	"""
	This class represents the goal tile in the game.
	"""

	def __init__(self,position,size):
		super().__init__()

		#GOAL
		self.image = pygame.Surface((size, size))
		self.image = pygame.image.load('../Assets/Goal.png')
		self.image = pygame.transform.scale(self.image, (size + 20, size + 20))
		self.rect = self.image.get_rect(topleft=position)
		self.hitbox = self.rect.inflate(-30, -40)
		self.hitbox.center = self.rect.center

	def update(self, x_shift):
		self.rect.x += x_shift
		self.hitbox.x += x_shift

class Spike(pygame.sprite.Sprite):
	"""
	This class represents the spike tile in the game.
	"""

	def __init__(self,position,size):
		super().__init__()

		#SPIKES
		self.image = pygame.Surface((size, size))
		self.image = pygame.image.load('../Assets/Spikes.png')
		self.image = pygame.transform.scale(self.image, (size + 20, size + 20))
		self.rect = self.image.get_rect(topleft=position)
		self.hitbox = self.rect.inflate(-40, -30)
		self.hitbox.center = self.rect.center

	def update(self, x_shift):
		self.rect.x += x_shift
		self.hitbox.x += x_shift
