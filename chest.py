import pygame
from player import load_images_folder

class Chest:
    def __init__(self, screen):
        self.screen = screen
        self.images = []
        # Appel de la fonction de chargement des images
        load_images_folder(self.images, "Chests")

        # Variable de gestion de la position / Mouvement
        self.scale_change = 0.85
        self.rescale_images()
        self.display_rect = self.images[0].get_rect(x=5550, y=292)
        print(self.display_rect.width, self.display_rect.height)
        # Gestion de l'animation
        self.is_closed = True
        self.is_opening = False
        self.is_open = False
        self.animation_count = 0
        self.frame_count = 0
        self.frame_per_animation = 8

    def draw(self, camera_x, camera_y):
        self.handle_animation()
        display_x = self.display_rect.x - camera_x
        display_y = self.display_rect.y - camera_y

        self.screen.blit(self.images[self.animation_count], (display_x, display_y))

    def get_scaled_image(self, image, scale):
        width, height = image.get_rect().width, image.get_rect().height
        return pygame.transform.smoothscale(image, (int(width * scale), int(height * scale)))

    def rescale_images(self):
        for i in range(len(self.images)):
            self.images[i] = self.get_scaled_image(self.images[i], self.scale_change)

    def handle_animation(self):
        self.frame_count += 1
        if self.frame_count % self.frame_per_animation == 0 and self.is_opening:
            self.animation_count = (self.animation_count + 1) % len(self.images)

        if self.animation_count == len(self.images) - 1:
            self.is_opening = False
            self.is_open = True
    def open(self):
        self.is_opening = True
        self.is_closed = False