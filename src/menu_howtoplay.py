import pygame

class HowToPlayMenu:
    def __init__(self, screen):
        """
        This function sets up the 'How to Play' menu interface.
        It initializes the menu with a given Pygame screen,
        defining the layout, fonts, text content,
        and visual elements like buttons.
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()

        #FONTS
        self.title_font = pygame.font.Font('../Fonts/NorseBold.otf', 64)
        self.text_font = pygame.font.Font('../Fonts/Norse.otf', 32)

        #TEXT
        self.title_text = self.title_font.render('How to Play', True, (255, 255, 255))
        self.instructions = [
            "CONTROLS:",
            "Arrow keys - move",
            "Space - jump",
            "R - restart the level",
            "ESC - pause",
            "                       ",
            "Avoid the icy spikes and reach the sword in time",
            # Add more instruction
        ]

        # Return button
        self.return_text = self.text_font.render('Return', True, (255, 255, 255))
        self.return_button = pygame.Rect(self.screen_rect.width - 170, self.screen_rect.height - 70, 150, 50)  # Positioned at the bottom
        self.return_button_normal_color = (120, 120, 120)
        self.return_button_hover_color = (100, 100, 100)  # Grey color


    def display(self):
        """
        This function is responsible for rendering the How to Play menu on the screen.
        """

        mouse_pos = pygame.mouse.get_pos()
        self.screen.fill((43, 28, 89))

        # Title
        title_rect = self.title_text.get_rect(center=(self.screen_rect.centerx, 100))
        self.screen.blit(self.title_text, title_rect)

        # Text
        y_offset = 150
        for line in self.instructions:
            line_surface = self.text_font.render(line, True, (255, 255, 255))
            line_rect = line_surface.get_rect(center=(self.screen_rect.centerx, y_offset))
            self.screen.blit(line_surface, line_rect)
            y_offset += 40


        # Return button
        if self.return_button.collidepoint(mouse_pos):
            return_button_color = self.return_button_hover_color
        else:
            return_button_color = self.return_button_normal_color

        pygame.draw.rect(self.screen, return_button_color, self.return_button)
        return_text_rect = self.return_text.get_rect(center=self.return_button.center)
        return_text_rect.y +=3
        self.screen.blit(self.return_text, return_text_rect)
