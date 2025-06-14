import pygame
import sys
from .level_load import *
from .level_draw import Level
from .player import Player
from .controls import Controls
from .menu_start import MainMenu
from .menu_pause import PauseMenu
from .menu_selectlevel import LevelSelectMenu
from .menu_howtoplay import HowToPlayMenu

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Project Valk")

# Set up the drawing window
current_level_number = 1
tile_size = 64
lev, screen_width, screen_height = load_level(current_level_number, tile_size)
screen = pygame.display.set_mode((screen_width/2, screen_height))
time = pygame.time.Clock()

states = {
    "MAIN_MENU": True,
    "IN_GAME": False,
    "GAME_OVER": False,
    "GAME_WON": False,
    "PAUSED": False,
    "LEVEL_SELECT": False,
    "HOW_TO_PLAY": False
}

main_menu = MainMenu(screen)
level_select_menu = LevelSelectMenu(screen)
pause_menu = PauseMenu(screen)
how_to_play_menu = HowToPlayMenu(screen)

# Create a player instance
player_start_pos = (128, 400)  # Starting position for the player
player_size = 64
player = Player(player_start_pos, player_size, screen_width, screen_height)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handling events in Main Menu
        if states["MAIN_MENU"]:
            main_menu.display()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu.start_button.collidepoint(event.pos):
                    states["MAIN_MENU"] = False
                    states["IN_GAME"] = True
                    lv = Level(lev, screen)
                    player.reset_position()
                    player.is_active = True
                elif main_menu.exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif main_menu.level_select_button.collidepoint(event.pos):
                    states["MAIN_MENU"] = False
                    states["LEVEL_SELECT"] = True
                elif main_menu.how_to_play_button.collidepoint(event.pos):
                    states["HOW_TO_PLAY"] = True
                    states["MAIN_MENU"] = False

        # Handling events in Game State
        elif states["IN_GAME"]:
            if not states["PAUSED"]:
                Controls(event, player, states, lev, screen, lv)
                new_lv, level_changed = Controls(event, player, states, lev, screen, lv)

            else:
                if event.type == pygame.MOUSEBUTTONDOWN: # Handling pause menu clicks
                    mouse_pos = event.pos

                    if pause_menu.resume_button.collidepoint(mouse_pos) and not states["GAME_OVER"] and not states["GAME_WON"]:
                        states["PAUSED"] = False
                        player.is_active = True
                    elif pause_menu.main_menu_button.collidepoint(mouse_pos):
                        states["MAIN_MENU"] = True
                        states["IN_GAME"] = False
                        states["PAUSED"] = False
                        states["GAME_OVER"] = False
                        states["GAME_WON"] = False
                    elif pause_menu.restart_button.collidepoint(mouse_pos):
                        lv = Level(lev, screen)
                        player.is_active = True
                        player.reset_position()
                        states["PAUSED"] = False
                        states["GAME_OVER"] = False
                        states["GAME_WON"] = False
                    elif states["GAME_WON"] and pause_menu.next_level_button.collidepoint(mouse_pos) and current_level_number <= 9:
                        current_level_number += 1
                        lev, screen_width, screen_height = load_level(current_level_number, tile_size)
                        lv = Level(lev, screen)
                        player.reset_position()
                        states["PAUSED"] = False
                        states["GAME_WON"] = False
                        states["GAME_OVER"] = False
                        player.is_active = True

            new_lv, level_changed = Controls(event, player, states, lev, screen, lv)

            if level_changed:
                lv = new_lv

    # Updating the screen based on game states
    if states["LEVEL_SELECT"]:
        level_select_menu.display()

        if event.type == pygame.MOUSEBUTTONDOWN:
            selected_level = level_select_menu.handle_click(event.pos)
            if selected_level is not None:
                # Logic to load the selected level
                current_level_number = selected_level
                lev, screen_width, screen_height = load_level(current_level_number, tile_size)
                lv = Level(lev, screen)
                player.reset_position()
                states["LEVEL_SELECT"] = False
                states["IN_GAME"] = True
                player.is_active = True
            elif level_select_menu.return_button.collidepoint(event.pos):
                states["LEVEL_SELECT"] = False
                states["MAIN_MENU"] = True
    elif states["HOW_TO_PLAY"]:
        how_to_play_menu.display()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if how_to_play_menu.return_button.collidepoint(event.pos):
                states["HOW_TO_PLAY"] = False
                states["MAIN_MENU"] = True

    elif states["IN_GAME"]:
        screen.fill((43, 28, 89))
        if lv is not None:
            lv.run()
            lv.wordshift_on(0)
            player.move(pygame.key.get_pressed())
            player.collide_with_tiles_horizontal(lv.blocks)
            player.apply_gravity()
            player.collide_with_tiles_vertical(lv.blocks)
            player.collide_with_goal(lv.goals)
            player.collide_with_spike(lv.spikes)
            if player.rect.bottom < 0:  # Player is out of the view on top, show the arrow
                arrow_x = player.rect.centerx - 15  # Center arrow above the player
                screen.blit(player.arrow_image, (arrow_x, 10))
            screen.blit(player.image, player.rect)

            if player.has_fallen_off_screen():
                player.deactivate()
                pause_menu.display('You Died')
                states["PAUSED"] = True
                states["GAME_OVER"] = True
                lv.wordshift_on(0)
            if player.collide_with_goal(lv.goals):
                player.deactivate()
                lv.wordshift_on(0)
                pause_menu.display('Level Complete')
                states["PAUSED"] = True
                states["GAME_WON"] = True
            if player.collide_with_spike(lv.spikes):
                player.deactivate()
                lv.wordshift_on(0)
                pause_menu.display('You Died')
                states["PAUSED"] = True
                states["GAME_OVER"] = True
            if player.collide_with_tiles_horizontal(lv.blocks) and player.collide_with_tiles_vertical(lv.blocks) and player.rect.left <= 3: # Getting squashed
                player.deactivate()
                lv.wordshift_on(0)
                pause_menu.display('You Died')
                states["PAUSED"] = True
                states["GAME_OVER"] = True
    if states["PAUSED"]:
        if not states["GAME_OVER"] and not states["GAME_WON"]:
            player.deactivate()
            lv.wordshift_on(0)
            screen.fill((43, 28, 89))
            lv.run()
            screen.blit(player.image, player.rect)
            pause_menu.display('Paused')

    pygame.display.update()
    time.tick(60)
