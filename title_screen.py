import pygame
import pygame_gui
from pygame.locals import QUIT
import sys
import time

def get_player_name_input(screen, screen_width, screen_height):
    gui_manager = pygame_gui.UIManager((screen_width, screen_height))

    label_rect = pygame.Rect(screen_width // 2 - 200, screen_height // 2 - 70, 400, 30)
    label = pygame_gui.elements.UILabel(relative_rect=label_rect, text='ENTER PLAYER NAME', manager=gui_manager)

    text_input_rect = pygame.Rect(screen_width // 2 - 200, screen_height // 2 - 20, 400, 40)
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=text_input_rect, manager=gui_manager)

    getting_name = True
    enter_pressed = False

    while getting_name:
        for event in pygame.event.get():
            if (event.type == QUIT or \
            (event.type in (pygame.KEYDOWN,pygame.KEYUP) and event.key == pygame.K_ESCAPE)):
                pygame.quit()
                sys.exit()

            gui_manager.process_events(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                enter_pressed = True

        screen.fill((0, 0, 0))

        gui_manager.update(time.time())
        gui_manager.draw_ui(screen)

        pygame.display.flip()

        if text_input.get_text() != "" and enter_pressed:
            player_name = text_input.get_text()
            getting_name = False

    return player_name
