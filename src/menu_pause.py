import pygame

class PauseMenu:
    def __init__(self, screen):
        """
        This function sets up the pause menu.
        It initializes the visual aspects of the menu.
        These include fonts, colors, background, and text.
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()

        #FONTS
        self.font = pygame.font.Font('../Fonts/NorseBold.otf', 100)
        self.button_font = pygame.font.Font('../Fonts/Norse.otf', 40)

        #COLORS
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent black
        self.text_color = (255, 255, 255)  # White
        self.text_color_inactive = (44, 44, 44)  # Dark Grey
        self.button_normal_color = (70, 70, 70)  # Grey
        self.button_hover_color = (100, 100, 100) # Light Grey
        
        #BACKGROUND
        self.menu_bg = pygame.Surface((self.screen_rect.width // 3 + 150, self.screen_rect.height // 2 + 50))
        self.menu_bg.set_alpha(self.bg_color[3])
        self.menu_bg.fill(self.bg_color)
        self.menu_rect = self.menu_bg.get_rect(center=self.screen_rect.center)

        # Initialize text and buttons
        self.initialize_menu('Paused')

    def initialize_menu(self, message):
        """
        This function initializes the pause menu itself
        based on the current state of the game.
        """

        # Text
        self.text = self.font.render(message, True, self.text_color)
        self.text_rect = self.text.get_rect(midtop=(self.menu_rect.centerx, self.menu_rect.top + 20))

        # Buttons
        self.button_height = 50
        self.button_width = self.menu_rect.width - 40
        self.button_gap = 20

        if message == 'Level Complete':
            self.next_level_button = pygame.Rect(self.menu_rect.left + 20, self.text_rect.bottom + 20, self.button_width, self.button_height)
            self.next_level_text = self.button_font.render('Next Level', True, self.text_color)
        elif message == 'You Died':
            self.resume_button = pygame.Rect(self.menu_rect.left + 20, self.text_rect.bottom + 20, self.button_width, self.button_height)
            self.resume_text = self.button_font.render('Resume', True, self.text_color_inactive)
        else:
            self.resume_button = pygame.Rect(self.menu_rect.left + 20, self.text_rect.bottom + 20, self.button_width, self.button_height)
            self.resume_text = self.button_font.render('Resume', True, self.text_color)

        self.restart_button = pygame.Rect(self.menu_rect.left + 20, self.resume_button.bottom + self.button_gap, self.button_width, self.button_height)
        self.main_menu_button = pygame.Rect(self.menu_rect.left + 20, self.restart_button.bottom + self.button_gap, self.button_width, self.button_height)

        # Button Texts
        self.main_menu_text = self.button_font.render('Main Menu', True, self.text_color)
        self.restart_text = self.button_font.render('Restart', True, self.text_color)

    def display(self, message):
        """
        The display function is responsible for actually rendering
        the menu on screen.
        """

        mouse_pos = pygame.mouse.get_pos()
        
        if self.resume_button.collidepoint(mouse_pos) and not message == 'You Died':
            self.resume_button_color = self.button_hover_color
        else:
            self.resume_button_color = self.button_normal_color
        
        if self.restart_button.collidepoint(mouse_pos):
            self.restart_button_color = self.button_hover_color
        else:
            self.restart_button_color = self.button_normal_color

        if self.main_menu_button.collidepoint(mouse_pos):
            self.main_menu_button_color = self.button_hover_color
        else:
            self.main_menu_button_color = self.button_normal_color 
         
        # Update the message and layout if needed
        self.initialize_menu(message)

        # Draw the semi-transparent background
        self.screen.blit(self.menu_bg, self.menu_rect)

        # Draw the text
        self.screen.blit(self.text, self.text_rect)

        # Draw buttons
        if message == 'Level Complete':

            if self.next_level_button.collidepoint(mouse_pos):
                self.next_level_button_color = self.button_hover_color
            else:
                self.next_level_button_color = self.button_normal_color

            pygame.draw.rect(self.screen, self.next_level_button_color, self.next_level_button)
            next_level_rect = self.next_level_text.get_rect(center=self.next_level_button.center)
            next_level_rect.y += 5
            self.screen.blit(self.next_level_text, next_level_rect)
        else:
            pygame.draw.rect(self.screen, self.resume_button_color, self.resume_button)
            resume_rect = self.resume_text.get_rect(center=self.resume_button.center)
            resume_rect.y += 5
            self.screen.blit(self.resume_text, resume_rect)

        pygame.draw.rect(self.screen, self.main_menu_button_color, self.main_menu_button)
        main_menu_rect = self.main_menu_text.get_rect(center=self.main_menu_button.center)
        main_menu_rect.y += 5
        self.screen.blit(self.main_menu_text, main_menu_rect)

        pygame.draw.rect(self.screen, self.restart_button_color, self.restart_button)
        restart_rect = self.restart_text.get_rect(center=self.restart_button.center)
        restart_rect.y += 5
        self.screen.blit(self.restart_text, restart_rect)
