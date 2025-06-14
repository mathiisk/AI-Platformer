import pygame

class LevelSelectMenu:
    def __init__(self, screen):
        """
        This function is responsible for initializing the
        visual elements of the level select menu.
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()

        #FONTS
        self.text_font = pygame.font.Font('../Fonts/Norse.otf', 40)

        #COLORS
        self.button_normal_color = (0, 123, 204)  # Normal blue
        self.button_hover_color = (0, 95, 158)  # Slightly darker blue
        self.text_color = (255, 255, 255)  # White

        # Button dimensions and layout
        self.button_width = 150
        self.button_height = 50
        self.button_gap = 20
        self.buttons = self.create_level_buttons(10)

        # Return button
        self.return_text = self.text_font.render('Return', True, (255, 255, 255))
        self.return_button = pygame.Rect(self.screen_rect.width - 170, self.screen_rect.height - 70, 150, 50)  # Positioned at the bottom
        self.return_button_normal_color = (120, 120, 120) # Grey
        self.return_button_hover_color = (100, 100, 100)  # Slightly darker grey

    def create_level_buttons(self, num_levels):
        """
        This function creates the interactive elements of
        the level select menu, such as the buttons.
        """

        buttons = []
        num_rows = 2
        num_columns = num_levels // num_rows
        column_gap = 60  # Gap between buttons horizontally

        # Calculate starting positions
        start_x = self.screen_rect.centerx - (num_columns * self.button_width + (num_columns - 1) * column_gap) // 2
        start_y = 100

        """Arrange the buttons in a table"""
        for i in range(num_levels):
            row = i // num_columns
            col = i % num_columns

            button_x = start_x + col * (self.button_width + column_gap)
            button_y = start_y + row * (self.button_height + self.button_gap)

            button = pygame.Rect(button_x, button_y, self.button_width, self.button_height)
            buttons.append((button, f"Level {i+1}"))

        return buttons

    def display(self):
        """
        This function is responsible for rendering the select level
        menu on screen for the player.
        """

        self.screen.fill((43, 28, 89))
        mouse_pos = pygame.mouse.get_pos()

        # Level buttons (1-10)
        for button, text in self.buttons:
            if button.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.button_hover_color, button)
            else:
                pygame.draw.rect(self.screen, self.button_normal_color, button)

            text_surface = self.text_font.render(text, True, self.text_color)
            text_rect = text_surface.get_rect(center=button.center)
            text_rect.y += 4
            self.screen.blit(text_surface, text_rect)

        # Return button
        if self.return_button.collidepoint(mouse_pos):
            return_button_color = self.return_button_hover_color
        else:
            return_button_color = self.return_button_normal_color


        pygame.draw.rect(self.screen, return_button_color, self.return_button)
        return_text_rect = self.return_text.get_rect(center=self.return_button.center)
        return_text_rect.y +=3
        self.screen.blit(self.return_text, return_text_rect)

    def handle_click(self, mouse_pos):
        for i, (button, _) in enumerate(self.buttons):
            if button.collidepoint(mouse_pos):
                print(f"Selected Level: {i+1}")
                return i + 1  # Return level number
        return None
