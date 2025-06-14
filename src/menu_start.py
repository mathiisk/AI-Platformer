import pygame

class MainMenu:
    def __init__(self, screen):
        """
        This function initializes the start menu of the game.
        It initializes fonts, text, and buttons.
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()  # Get the rect of the screen for centering

        #CUSTOM FONTS
        self.title_font = pygame.font.Font('../Fonts/NorseBold.otf', 128)
        self.button_font = pygame.font.Font('../Fonts/Norse.otf', 64)
        self.smaller_button_font = pygame.font.Font('../Fonts/Norse.otf', 32)

        #TITLE TEXT
        self.title_text = self.title_font.render('Project Valk', True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery // 2))

        #BUTTON TEXT
        self.start_text = self.button_font.render('START', True, (255, 255, 255))
        self.exit_text = self.button_font.render('EXIT', True, (255, 255, 255))
        self.level_select_text = self.button_font.render('LEVEL SELECT', True, (255, 255, 255))
        self.how_to_play_text = self.smaller_button_font.render('How to Play', True, (255, 255, 255))

        #BUTTON COLORS
        self.button_hover_color = (36, 129, 77)  # Normal green
        self.button_normal_color = (56, 149, 87)  # Slightly darker green
        self.exit_hover_color = (124, 7, 11)  # Normal red
        self.exit_normal_color = (154, 17, 21)  # Slightly darker red
        self.select_button_normal_color = (0, 123, 204)  # Normal blue
        self.select_button_hover_color = (0, 95, 158)  # Slightly darker blue

        self.how_to_play_button_normal_color = (120, 120, 120)  # Grey color
        self.how_to_play_button_hover_color = (100, 100, 100)  # Grey color

        #BUTTON PARAMETERS
        button_width = 400
        button_height = 100
        button_gap = 20

        # Start button position
        start_button_x = self.screen_rect.centerx - button_width // 2
        start_button_y = self.screen_rect.centery - button_height + button_gap
        self.start_button = pygame.Rect(start_button_x, start_button_y, button_width, button_height)

        # Level select button position
        level_select_button_x = self.screen_rect.centerx - button_width // 2
        level_select_button_y = self.start_button.bottom + button_gap
        self.level_select_button = pygame.Rect(level_select_button_x, level_select_button_y, button_width, button_height)

        # Exit button position
        exit_button_x = self.screen_rect.centerx - button_width // 2
        exit_button_y = self.level_select_button.bottom + button_gap
        self.exit_button = pygame.Rect(exit_button_x, exit_button_y, button_width, button_height)

        # How-To-Play button position
        self.how_to_play_button = pygame.Rect(20, self.screen_rect.height - 70, 200, 50)  # Positioned in the corner
        
    def display(self):
        """
        This function renders the start menu visually for
        the player to interact with.
        """

        mouse_pos = pygame.mouse.get_pos()

        if self.start_button.collidepoint(mouse_pos):
            start_button_color = self.button_hover_color
        else:
            start_button_color = self.button_normal_color

        if self.exit_button.collidepoint(mouse_pos):
            exit_button_color = self.exit_hover_color
        else:
            exit_button_color = self.exit_normal_color

        if self.level_select_button.collidepoint(mouse_pos):
            select_button_color = self.select_button_hover_color
        else:
            select_button_color = self.select_button_normal_color

        if self.how_to_play_button.collidepoint(mouse_pos):
            how_to_play_button_color = self.how_to_play_button_hover_color
        else:
            how_to_play_button_color = self.how_to_play_button_normal_color

        # Fill the screen with a background for the menu
        self.screen.fill((43, 28, 89))

        #Draw title
        self.screen.blit(self.title_text, self.title_rect)

        # Draw the buttons
        pygame.draw.rect(self.screen, start_button_color, self.start_button)
        pygame.draw.rect(self.screen, exit_button_color, self.exit_button)
        pygame.draw.rect(self.screen, select_button_color, self.level_select_button)
        pygame.draw.rect(self.screen, how_to_play_button_color, self.how_to_play_button)
        how_to_play_text_rect = self.how_to_play_text.get_rect(center=self.how_to_play_button.center)
        how_to_play_text_rect.y += 3
        start_text_rect = self.start_text.get_rect(center=self.start_button.center) # Determine text position
        start_text_rect.y += 7
        exit_text_rect = self.exit_text.get_rect(center=self.exit_button.center) # Determine text position
        exit_text_rect.y += 7
        level_select_text_rect = self.level_select_text.get_rect(center=self.level_select_button.center)
        level_select_text_rect.y += 7

        self.screen.blit(self.start_text, start_text_rect)
        self.screen.blit(self.exit_text, exit_text_rect)
        self.screen.blit(self.level_select_text, level_select_text_rect)
        self.screen.blit(self.how_to_play_text, how_to_play_text_rect)
