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

        self.pressed = False
        self.is_clicked = False
        self.press_time = 0

        self.base_scale = base_scale
        self.hover_scale = hover_scale
        self.current_scale = base_scale
        self.target_scale = base_scale
        self.scale_speed = scale_speed

        self.image = self.get_scaled_image(self.current_scale)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def get_scaled_image(self, scale):
        width, height = self.base_size
        return pygame.transform.smoothscale(self.original_image, (int(width * scale), int(height * scale)))

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

        if abs(self.current_scale - self.target_scale) > 0.01 and self.state_hover:
            self.current_scale += (self.target_scale - self.current_scale) * self.scale_speed
            self.image = self.get_scaled_image(self.current_scale)
            self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def set_image(self, new_image):
        self.original_image = new_image
        self.base_size = new_image.get_size()
        self.image = self.get_scaled_image(self.current_scale)
        self.rect = self.image.get_rect(center=(self.x, self.y))
