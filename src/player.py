import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, position, size, screen_width, screen_height):
        """
        This function initializes the player object using assets
        and sound effects, and also scales it to proportion with the
        rest of the level.
        It also initializes the player's hit box.
        """

        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.start_position = position
        
        #LOAD PLAYER ASSETS
        self.image_front = pygame.image.load('../Assets/Gertrude.png')
        self.arrow_image = pygame.image.load('../Assets/Arrow.png')

        #SCALE PLAYER ASSETS
        self.image_front = pygame.transform.scale(self.image_front, (size, size))
        self.arrow_image = pygame.transform.scale(self.arrow_image, (30, 30))

        #SOUND EFFECTS
        self.jump_sound = pygame.mixer.Sound('../Assets/Sound/jump.mp3')
        self.jump_sound.set_volume(0.3)

        self.goal_sound = pygame.mixer.Sound('../Assets/Sound/draw_sword.mp3')
        self.goal_sound.set_volume(0.1)

        # Initialise
        self.image = self.image_front
        self.rect = self.image.get_rect(center=position)

        # Adjust hitbox
        self.hitbox = self.rect.inflate(-30, -30)
        self.hitbox.center = self.rect.center

        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 5 # Left/Right movement speed of player
        self.jump_strength = -22  # Jump strength (negative because it's going upwards)
        self.gravity = 1  # Gravity strength
        self.on_ground = False  # Track whether player is on ground or in air
        self.is_active = False # Track whether player should be able to move

    def apply_gravity(self):
        """Applies gravity to player"""
        # Apply gravity to the player
        if self.is_active:
            self.velocity.y += self.gravity

            # Ensure player doesn't accelerate indefinitely
            if self.velocity.y > 10:
                self.velocity.y = 10

            self.rect.y += self.velocity.y    
            self.hitbox.y += self.velocity.y

    def move(self, keys_pressed):
        """Movement"""
        if self.is_active:
            self.velocity.x = 0 # Reset the velocity
        
            # Move left/right
            if keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_RIGHT]:
                self.velocity.x = -self.speed
            elif keys_pressed[pygame.K_RIGHT] and not keys_pressed[pygame.K_LEFT]:
                self.velocity.x = self.speed
            else:
                self.velocity.x = 0
            
            self.rect.x += self.velocity.x-1
            self.hitbox.x += self.velocity.x-1

            # Jump
            if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_UP] and self.on_ground:
                self.jump()

            # Check for screen edges
            if self.hitbox.left < 0:  
                self.rect.left = -15
                self.hitbox.left = 0
            elif self.rect.right > self.screen_width/2:
                self.rect.right = self.screen_width/2
                self.hitbox.right = self.screen_width/2 - 10

    def jump(self):
        """Jump"""
        if self.is_active:
            if self.on_ground:
                self.jump_sound.play()
                self.velocity.y = self.jump_strength    

    def deactivate(self):
        """Disables player movement"""
        # Call this method when the player reaches the goal or touches a spike
        self.is_active = False

    def collide_with_tiles_horizontal(self, tiles_group):
        """Detect collision with walls"""
        for tile in tiles_group:
            if self.rect.colliderect(tile.rect):
                if self.velocity.x > 0:  # Moving right
                    self.rect.right = tile.rect.left
                    self.velocity.x = 0
                    self.hitbox.right = tile.rect.left - 15
                if self.velocity.x < 0:  # Moving left
                    self.rect.left = tile.rect.right
                    self.velocity.x = 0
                    self.hitbox.left = tile.rect.right + 15
                return True

    def collide_with_tiles_vertical(self, tiles_group):
        """Detect collision with ground"""
        self.on_ground = False
        for tile in tiles_group:
            if self.rect.colliderect(tile.rect):
                if self.velocity.y > 0:  # Falling
                    self.rect.bottom = tile.rect.top
                    self.hitbox.bottom = tile.rect.top - 10
                    self.on_ground = True
                    self.velocity.y = 0
                elif self.velocity.y < 0:  # Jumping/Moving up
                    self.rect.top = tile.rect.bottom
                    self.hitbox.top = tile.rect.bottom + 10
                    self.velocity.y = 0          
                return True

    def collide_with_goal(self, goals_group):
        """Detect collision with goals"""
        for goal in goals_group:
            if self.hitbox.colliderect(goal.hitbox):
                return True

    def collide_with_spike(self, spikes_group):
        """Detect collision with spikes"""
        for spike in spikes_group:
            if self.hitbox.colliderect(spike.hitbox):
                return True     

    def reset_position(self):
        """Resets player position"""
        self.rect.center = self.start_position
        self.hitbox.center = self.start_position
        self.velocity = pygame.math.Vector2(0, 0)  # Reset velocity
        self.is_active = True  # Enable player movement

    def has_fallen_off_screen(self):
        """Detect if player falls off the level"""
        return self.hitbox.top > self.screen_height
