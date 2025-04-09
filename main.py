from asyncio import current_task

import pygame
import os
from game import Game
from MainMenu import MainMenu


def main_loop():
    window_size = (1280, 720)

    pygame.init()
    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()

    menu = MainMenu(screen, clock)
    current_scene = "menu"
    is_launched = False

    while True:
        if current_scene == "menu":
            state = menu.run()
            is_launched = True
            if state:
                current_scene = "game"
        elif current_scene == "game":
            game = Game((1280, 720))
            game.setup()
            state = game.run()
            if state == "EXIT":
                break
            elif state == "RESTART":
                continue
            elif state == "HOME":
                current_scene = "menu"
                if is_launched:
                    is_launched = False
                    new_clock = pygame.time.Clock()
                    menu = MainMenu(screen, new_clock)
                continue


    pygame.quit()


if __name__ == "__main__":
    main_loop()