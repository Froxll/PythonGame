import pygame
import math

class Powerup:
    def __init__(self, screen, player, type):
        self.screen = screen
        self.player = player
        if type == "boots":
            self.scale_change = 0.1
        else:
            self.scale_change = 0.2

        # Gestion de l'animation (haut/bas)
        self.counter = 0
        self.animation_speed = 0.05
        self.animation_amplitude = 15
        if type == "boots":
            self.original_y = 100
        else:
            self.original_y = 1488

        if type == "boots": # Flemme de faire de l'héritage
            self.image = pygame.image.load("img/powerup/boots_powerup.png")
            self.rescale_images()
            self.display_rect = self.image.get_rect(x=150, y=self.original_y)
        elif type == "heart":
            self.image = pygame.image.load("img/Lifebar/Full_Heart.png")
            self.rescale_images()
            self.display_rect = self.image.get_rect(x=2343, y=self.original_y)


    def draw(self, camera_x, camera_y):
        self.counter += 1
        self.display_rect.y = self.original_y + math.sin(self.counter * self.animation_speed) * self.animation_amplitude

        display_x = self.display_rect.x - camera_x
        display_y = self.display_rect.y - camera_y

        self.screen.blit(self.image, (display_x, display_y))

    def get_scaled_image(self, image, scale):
        width, height = image.get_rect().width, image.get_rect().height
        return pygame.transform.smoothscale(image, (int(width * scale), int(height * scale)))

    def rescale_images(self):
        self.image = self.get_scaled_image(self.image, self.scale_change)

