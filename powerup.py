import pygame

class Powerup:
    def __init__(self, screen, player, type):
        self.screen = screen
        self.player = player
        self.scale_change = 0.1
        if type == "boots":
            self.image = pygame.image.load("img/powerup/boots_powerup.png")
            self.rescale_images()
            self.display_rect = self.image.get_rect(x=200, y=1900)

        #elif type == "heart":

    def draw(self, camera_x, camera_y):
        display_x = self.display_rect.x - camera_x
        display_y = self.display_rect.y - camera_y

        self.screen.blit(self.image, (display_x, display_y))

    def get_scaled_image(self, image, scale):
        width, height = image.get_rect().width, image.get_rect().height
        return pygame.transform.smoothscale(image, (int(width * scale), int(height * scale)))

    def rescale_images(self):
        self.image = self.get_scaled_image(self.image, self.scale_change)