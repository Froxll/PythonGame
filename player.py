import pygame
import time

# Utilisation de la vidéo : https://youtu.be/B6DrRN5z_uU?si=vNqB4-23R81IHm74
# Création du personnage / gestion des déplacements

class Player():
    def __init__(self, screen, max_health):
        # Variable d'affichage du Joueur
        self.screen = screen
        self.image = pygame.image.load('img/lom1.png').convert_alpha()
        new_size = (self.image.get_width() // 4, self.image.get_height() // 4)  # Diviser la taille par 2
        self.image = pygame.transform.scale(self.image, new_size)

        #Variable de gestion de la position / Mouvement
        self.rect = self.image.get_rect(x=100, y=0)

        self.velocity = 5
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.fall_count = 0

        self.jump_count = 0
        self.jump_speed = 12
        self.side_hit_count = 0

        self.climb_speed = 5

        self.hp = max_health

    def move(self):
        self.y_vel += min(1, self.fall_count / 60)
        if self.y_vel > 18:
            self.y_vel = 18
        pressed = pygame.key.get_pressed()
        self.x_vel = 0
        if pressed[pygame.K_LEFT]:
            self.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.move_right()

        self.rect.move_ip(self.x_vel, self.y_vel)
        self.fall_count += 1

    def draw(self, camera_x, camera_y):
        display_x = self.rect.x - camera_x
        display_y = self.rect.y - camera_y
        if self.direction == "left":
            # On retourne l'image en mirroir
            image_flipped = pygame.transform.flip(self.image, True, False)
            self.screen.blit(image_flipped, (display_x, display_y))
        elif self.direction == "right":
            self.screen.blit(self.image, (display_x, display_y))

    def move_left(self):
        self.x_vel = -self.velocity
        if self.direction != "left":
            self.direction = "left"
            #self.animation_count = 0

    def move_right(self):
        self.x_vel = self.velocity
        if self.direction != "right":
            self.direction = "right"
            # self.animation_count = 0

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.side_hit_count = 0

    def jump(self):
        self.y_vel = -1 * self.jump_speed
        self.jump_count += 1
        if self.jump_count == 2:
            self.fall_count = 0

    def hit_side(self):
        self.fall_count = 0
        self.y_vel = 0
        self.side_hit_count += 1
        if self.side_hit_count == 1:
            self.jump_count = 0

    def climb(self, climb_type):
        self.fall_count = 0
        if climb_type == "up":
            self.y_vel = -1 * self.climb_speed
        elif climb_type == "down":
            self.y_vel = self.climb_speed
