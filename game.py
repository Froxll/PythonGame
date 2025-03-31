import pygame
from player import Player

class Game():
    def __init__(self, window_size):
        # Pygame initialization
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True

        self.player = None    # Joueur
        self.platforms = None # Liste des plateformes
        self.enemies = None   # Liste des ennemis
        self.power_ups = None # Liste des power-ups

        # Test collision
        self.rect_list = []
        self.ladder_list = []

    def setup(self):

        self.player = Player(self.screen, 50)
        """
        self.platforms = ...
        self.enemies = ...
        self.power_ups = ...
        """


    def run(self):
        while self.isRunning:
            # Structure du code : https://www.youtube.com/watch?v=N56R1V5XZBw&list=PLKeQQTikvsqkeJlhiE8mXwskOhXLKdl8m&index=3
            # Gestion de l'évenement "Quit
            self.handling_events()

            # Mise à jour des différents éléments
            self.update()

            # Rendu des entités
            self.display()

            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.jump_count < 2 :
                    self.player.jump()

                elif event.key == pygame.K_UP and self.check_ladder_collisions():
                    self.player.climb()

    def update(self):
        self.player.move()
        self.check_rect_collisions()
        self.check_ladder_collisions()

    def display(self):
        self.screen.fill("black")

        self.player.draw()

        pygame.display.flip()

    def check_rect_collisions(self):
        collision_index = self.player.rect.collidelist(self.rect_list)
        if  collision_index > -1:
            # J'ai essayé d'implémenter quelque chose mais ChatGPT a corrigé en me donnant cette version
            # Calculer les distances entre les bords du joueur et du rectangle touché
            dx_left = abs(self.player.rect.right - self.rect_list[collision_index].left)  # Distance au bord gauche de l'obstacle
            dx_right = abs(self.player.rect.left - self.rect_list[collision_index].right)  # Distance au bord droit de l'obstacle
            dy_top = abs(self.player.rect.bottom - self.rect_list[collision_index].top)  # Distance au bord supérieur de l'obstacle
            dy_bottom = abs(self.player.rect.top - self.rect_list[collision_index].bottom)  # Distance au bord inférieur de l'obstacle

            # Trouver le côté où la collision est la plus "profonde" (le plus petit décalage)
            min_dist = min(dx_left, dx_right, dy_top, dy_bottom)

            if min_dist == dx_left:
                self.player.rect.right = self.rect_list[collision_index].left  # Bloquer à gauche
                self.player.hit_side()
            elif min_dist == dx_right:
                self.player.rect.left = self.rect_list[collision_index].right  # Bloquer à droite
                self.player.hit_side()
            elif min_dist == dy_top:
                self.player.rect.bottom = self.rect_list[collision_index].top  # Bloquer au sol
                self.player.landed()
            elif min_dist == dy_bottom:
                self.player.rect.top = self.rect_list[collision_index].bottom  # Bloquer en haut (tête du joueur)
                self.player.y_vel *= -1

    def check_ladder_collisions(self):
        collision_index = self.player.rect.collidelist(self.ladder_list)
        if collision_index > -1:
            pressed = pygame.key.get_pressed()
            self.player.x_vel = 0
            if pressed[pygame.K_UP]:
                self.player.climb("up")
            elif pressed[pygame.K_DOWN]:
                self.player.climb("down")
            else:
                dx_left = abs(self.player.rect.right - self.ladder_list[collision_index].left)  # Distance au bord gauche de l'obstacle
                dx_right = abs(self.player.rect.left - self.ladder_list[collision_index].right)  # Distance au bord droit de l'obstacle
                dy_top = abs(self.player.rect.bottom - self.ladder_list[collision_index].top)  # Distance au bord supérieur de l'obstacle
                dy_bottom = abs(self.player.rect.top - self.ladder_list[collision_index].bottom)  # Distance au bord inférieur de l'obstacle

                # Trouver le côté où la collision est la plus "profonde" (le plus petit décalage)
                min_dist = min(dx_left, dx_right, dy_top, dy_bottom)
                if min_dist == dy_top:
                    self.player.rect.bottom = self.ladder_list[collision_index].top  # Bloquer au sol
                    self.player.landed()