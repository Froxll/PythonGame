import math
import pygame
from button import Button

###################
# Ressources
#
# Moving Background : https://youtu.be/ARt6DLP38-Y?si=MGtFLBf3tNWc1MkS
###################

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

class MainMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        # Initialisation du Logo
        self.logo = pygame.image.load('img/MainMenu/Logo.png').convert_alpha()
        self.logo = pygame.transform.smoothscale(self.logo, (int(self.logo.get_width() * 0.3), int(self.logo.get_height() * 0.3)))
        self.rect_logo = self.logo.get_rect()
        self.rect_logo.topleft = (530, 90)

        # Initialisation pour le background qui bouge
        self.background = pygame.image.load("img/MainMenu/Main_menu.png").convert()
        self.scroll = 0
        self.tiles = math.ceil(SCREEN_WIDTH / self.background.get_width()) + 1

        # Initialisation pour les boutons
        start_button_img = pygame.image.load("img/MainMenu/Start_Button.png").convert_alpha()
        exit_button_img = pygame.image.load("img/MainMenu/Exit_Button.png").convert_alpha()

        vol_on = pygame.image.load("img/MainMenu/volume/Volume_On.png").convert_alpha()
        vol_on_pressed = pygame.image.load("img/MainMenu/volume/Volume_On_Pressed.png").convert_alpha()
        vol_off = pygame.image.load("img/MainMenu/volume/Volume_Off.png").convert_alpha()
        vol_off_pressed = pygame.image.load("img/MainMenu/volume/Volume_Off_Pressed.png").convert_alpha()

        self.start_button = Button(650, 400, start_button_img, "start",self.screen, True)
        self.exit_button = Button(650, 525, exit_button_img, "exit", self.screen, True, 0.30, 0.35)

        self.volume_button = Button(1250, 50, vol_on, "vol_on", self.screen, False)


        self.isRunning = True

    def run(self):

        while self.isRunning:

            if self.start_button.is_clicked:
                return True


            self.clock.tick(FPS)

            self.display()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
        pygame.quit()

    def display(self):

        # Boucle qui gère le background qui bouge
        for i in range(0, self.tiles):
            self.screen.blit(self.background, (i*self.background.get_width() + self.scroll, 0))
        self.scroll -= 1
        if abs(self.scroll) > self.background.get_width():
            self.scroll = 0

        self.start_button.update()
        self.start_button.draw()

        self.exit_button.update()
        self.exit_button.draw()

        self.screen.blit(self.logo, self.rect_logo)

        pygame.display.flip()
