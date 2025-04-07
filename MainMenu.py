import math
import os
import pygame
from button import Button
from pygame import mixer
import sys

###################
# Ressources
#
# Moving Background : https://youtu.be/ARt6DLP38-Y?si=MGtFLBf3tNWc1MkS
# Animation boutons volumes : ChatGPT
###################

# Pour le moving background
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

class MainMenu:
    def __init__(self, screen, clock):

        # Pour la musique
        mixer.init()
        mixer.music.load('audio/MainMenu_music.mp3')
        mixer.music.set_volume(0.5)

        # Pour le background
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

        self.vol_on = pygame.image.load("img/MainMenu/volume/Volume_On.png").convert_alpha()
        self.vol_on_pressed = pygame.image.load("img/MainMenu/volume/Volume_On_Pressed.png").convert_alpha()
        self.vol_off = pygame.image.load("img/MainMenu/volume/Volume_Off.png").convert_alpha()
        self.vol_off_pressed = pygame.image.load("img/MainMenu/volume/Volume_Off_Pressed.png").convert_alpha()

        self.start_button = Button(650, 400, start_button_img, "start",self.screen, True)
        self.exit_button = Button(650, 525, exit_button_img, "exit", self.screen, True, 0.30, 0.35)

        self.volume_button = Button(1225, 50, self.vol_on, "vol_on", self.screen, False, 1.5)
        self.volume_button.type_button = "vol_on"

        # Pour l'animation des boutons volume pressés (ChatGPT pour cette partie)
        self.volume_button_pressed = False
        self.volume_button_press_time = 0
        self.volume_button_press_delay = 200  # en ms

        # Lancement de la musique (en mode infini : -1)
        mixer.music.play(-1)

        self.isRunning = True

    def run(self):

        while self.isRunning:

            if self.start_button.is_clicked:
                mixer.music.stop()
                return True

            self.clock.tick(FPS)

            self.display()

            self.handle_event()

            if self.volume_button_pressed:
                if pygame.time.get_ticks() - self.volume_button_press_time >= self.volume_button_press_delay:
                    if self.volume_button.type_button == "vol_off":
                        self.volume_button.set_image(self.vol_off)
                    elif self.volume_button.type_button == "vol_on":
                        self.volume_button.set_image(self.vol_on)
                    self.volume_button_pressed = False

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

        self.volume_button.update()
        self.volume_button.draw()

        self.screen.blit(self.logo, self.rect_logo)

        pygame.display.flip()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                pygame.display.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.volume_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.volume_button_pressed = True
                    self.volume_button_press_time = pygame.time.get_ticks()

                    if self.volume_button.type_button == "vol_on":
                        self.volume_button.set_image(self.vol_on_pressed)
                        mixer.music.set_volume(0)
                        self.volume_button.type_button = "vol_off"

                    elif self.volume_button.type_button == "vol_off":
                        self.volume_button.set_image(self.vol_off_pressed)
                        mixer.music.set_volume(0.5)
                        self.volume_button.type_button = "vol_on"




