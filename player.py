import pygame
import time

class Player():
    def __init__(self, screen, max_health):
        # Variable d'affichage du Joueur
        self.screen = screen
        self.image = pygame.image.load('img/lom1.png').convert_alpha()
        new_size = (self.image.get_width() // 4, self.image.get_height() // 4)  # Diviser la taille par 2
        self.image = pygame.transform.scale(self.image, new_size)

        #Variable de gestion de la position / Mouvement
        self.rect = self.image.get_rect(x=0, y=0)
        self.speed = 5
        self.velocity = [0, 0]

        self.hp = max_health

    def move(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            self.velocity[0] = -1
        elif pressed[pygame.K_RIGHT]:
            self.velocity[0] = 1
        else:
            self.velocity[0] = 0

        if pressed[pygame.K_UP]:
            self.velocity[1] = -1
        elif pressed[pygame.K_DOWN]:
            self.velocity[1] = 1
        else:
            self.velocity[1] = 0

        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)

    def draw(self):
        self.screen.blit(self.image, self.rect)