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
        mixer.music.set_volume(0.2)

        # Pour le background
        self.screen = screen
        self.clock = clock

        # Initialisation du Logo
        self.logo = pygame.image.load('img/MainMenu/Logo.png').convert_alpha()
        self.logo = pygame.transform.smoothscale(self.logo, (int(self.logo.get_width() * 0.3), int(self.logo.get_height() * 0.3)))
        self.rect_logo = self.logo.get_rect()
        self.rect_logo.topleft = (530, 90)

        # Initialisation du titre "Contrôles"
        self.controles_logo = pygame.image.load('img/MainMenu/Controles.png').convert_alpha()
        self.controles_logo = pygame.transform.smoothscale(self.controles_logo, (int(self.controles_logo.get_width() * 0.2), int(self.controles_logo.get_height() * 0.2)))
        self.rect_controles = self.controles_logo.get_rect()
        self.rect_controles.topleft = (80,475)

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

        # Pour l'animation des boutons volume pressés (ChatGPT pour cette partie)
        self.volume_button_pressed = False
        self.volume_button_press_time = 0
        self.volume_button_press_delay = 200  # en ms

        self.d_1_img = pygame.image.load("img/MainMenu/Keyboard/D_1.png").convert_alpha()
        self.d_2_img = pygame.image.load("img/MainMenu/Keyboard/D_2.png").convert_alpha()
        self.d_button = Button(213, 585, self.d_1_img, "d_1", self.screen, False, 2)

        self.z_1_img = pygame.image.load("img/MainMenu/Keyboard/Z_1.png").convert_alpha()
        self.z_2_img = pygame.image.load("img/MainMenu/Keyboard/Z_2.png").convert_alpha()
        self.z_button = Button(170, 550, self.z_1_img, "z_1", self.screen, False, 2)

        self.s_1_img = pygame.image.load("img/MainMenu/Keyboard/S_1.png").convert_alpha()
        self.s_2_img = pygame.image.load("img/MainMenu/Keyboard/S_2.png").convert_alpha()
        self.s_button = Button(175, 585, self.s_1_img, "s_1", self.screen, False, 2)

        self.q_1_img = pygame.image.load("img/MainMenu/Keyboard/Q_1.png").convert_alpha()
        self.q_2_img = pygame.image.load("img/MainMenu/Keyboard/Q_2.png").convert_alpha()
        self.q_button = Button(137, 585, self.q_1_img, "q_1", self.screen, False, 2)

        self.space_1_img = pygame.image.load("img/MainMenu/Keyboard/SPACE_1.png").convert_alpha()
        self.space_2_img = pygame.image.load("img/MainMenu/Keyboard/SPACE_2.png").convert_alpha()
        self.space_button = Button(175, 620, self.space_1_img, "space_1", self.screen, False, 1.5)


        # Lancement de la musique
        mixer.music.play(-1)

        self.isRunning = True

    def run(self):

        while self.isRunning:

            if self.start_button.is_clicked:
                mixer.music.set_volume(0.1)
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

        self.z_button.update()
        self.z_button.draw()
        self.d_button.update()
        self.d_button.draw()
        self.q_button.update()
        self.q_button.draw()
        self.s_button.update()
        self.s_button.draw()
        self.space_button.update()
        self.space_button.draw()

        self.screen.blit(self.logo, self.rect_logo)
        self.screen.blit(self.controles_logo, self.rect_controles)

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
                        mixer.music.set_volume(0.2)
                        self.volume_button.type_button = "vol_on"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.d_button.set_image(self.d_2_img)
                if event.key == pygame.K_q:
                    self.q_button.set_image(self.q_2_img)
                if event.key == pygame.K_s:
                    self.s_button.set_image(self.s_2_img)
                if event.key == pygame.K_z:
                    self.z_button.set_image(self.z_2_img)
                if event.key == pygame.K_SPACE:
                    self.space_button.set_image(self.space_2_img)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.d_button.set_image(self.d_1_img)
                if event.key == pygame.K_q:
                    self.q_button.set_image(self.q_1_img)
                if event.key == pygame.K_s:
                    self.s_button.set_image(self.s_1_img)
                if event.key == pygame.K_z:
                    self.z_button.set_image(self.z_1_img)
                if event.key == pygame.K_SPACE:
                    self.space_button.set_image(self.space_1_img)



