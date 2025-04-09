import pygame
import sys

###################
# Ressources
#
# ChatGPT pour faire l'animation du hover de manière fluide
###################

class Button:
    def __init__(self, x, y, image, type_button, screen, state_hover,base_scale=0.35, hover_scale=0.4, scale_speed=0.1):
        self.original_image = image
        self.base_size = image.get_size()
        self.x = x
        self.y = y
        self.screen = screen
        self.type_button = type_button
        self.state_hover = state_hover

        # Paramètres de gestion du clic
        self.pressed = False
        self.is_clicked = False
        self.press_time = 0

        # Paramètres pour la gestion du Hover des boutons
        self.base_scale = base_scale
        self.hover_scale = hover_scale
        self.current_scale = base_scale
        self.target_scale = base_scale
        self.scale_speed = scale_speed

        # Initialisation de l'image et du rect pour le bouton
        self.image = self.get_scaled_image(self.current_scale)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    # Fonction qui permet d'augmenter la taille d'une image à partir d'un coefficient sans déformer l'image
    def get_scaled_image(self, scale):
        width, height = self.base_size
        return pygame.transform.smoothscale(self.original_image, (int(width * scale), int(height * scale)))

    # Fonction qui gère le clic des boutons (c'est une manière de faire, non-reproduite dans les autres pages car non-ergonomique)
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.target_scale = self.hover_scale
            if pygame.mouse.get_pressed()[0] == 1:
                if self.type_button == "exit":
                    self.is_clicked = True
                    pygame.display.quit()
                    sys.exit()
                if self.type_button == "start":
                    self.is_clicked = True

        else:
            self.target_scale = self.base_scale

        # Gestion du Hover du bouton
        if abs(self.current_scale - self.target_scale) > 0.01 and self.state_hover:
            self.current_scale += (self.target_scale - self.current_scale) * self.scale_speed
            self.image = self.get_scaled_image(self.current_scale)
            self.rect = self.image.get_rect(center=(self.x, self.y))

    # Fonction qui permet de dessiner l'image dans l'écran de la fenêtre
    def draw(self):
        self.screen.blit(self.image, self.rect)

    # Fonction qui permet de changer l'image d'un bouton
    def set_image(self, new_image):
        self.original_image = new_image
        self.base_size = new_image.get_size()
        self.image = self.get_scaled_image(self.current_scale)
        self.rect = self.image.get_rect(center=(self.x, self.y))
