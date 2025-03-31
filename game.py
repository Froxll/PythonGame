import pygame
import pytmx
from player import Player
from monster import Monster


class Game():
    def __init__(self, window_size):
        # Pygame initialization
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True

        self.player = None  # Joueur
        self.platforms = None  # Liste des plateformes
        self.power_ups = None  # Liste des power-ups

        self.background = pygame.image.load("img/Map.png").convert()
        tmx_data = pytmx.load_pygame("data/MapTMX.tmx")

        self.rect_list = []
        self.ladder_list = []
        self.spades_list = []

        for obj in tmx_data.objects:
            if obj.name == "plateforme":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.rect_list.append(rect)
            if obj.name == "echelle":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.ladder_list.append(rect)
            if obj.name == "piques":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.spades_list.append(rect)

        # Caméra temporaire Et1
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 900
        self.all_monsters = pygame.sprite.Group()
        self.spawn_monsters()

    def spawn_monsters(self):
        golem_positions = [
            (1260, 1735, 1260, 1620),  # Spawn en x:1260 y:1735 et va de 1260 à 1620 en x
            (3988, 1737, 3988, 4372),
            (184, 84, 184, 568),
            (2700, 1929, 2700, 2910),
        ]

        for pos in golem_positions:
            monster = Monster(*pos)
            self.all_monsters.add(monster)

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


        # Caméra temporaire

        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            self.camera_x -= self.camera_speed * self.dt
        if keys[pygame.K_h]:
            self.camera_x += self.camera_speed * self.dt
        if keys[pygame.K_t]:
            self.camera_y -= self.camera_speed * self.dt
        if keys[pygame.K_g]:
            self.camera_y += self.camera_speed * self.dt

        self.all_monsters.update(self.dt)

    def display(self):
        self.screen.blit(self.background, (-self.camera_x, -self.camera_y))

        for rect in self.rect_list:
            shifted_rect = rect.move(-self.camera_x, -self.camera_y)
            pygame.draw.rect(self.screen, (255, 0, 0), shifted_rect, width=2)

        for rect in self.ladder_list:
            shifted_rect = rect.move(-self.camera_x, -self.camera_y)
            pygame.draw.rect(self.screen, (0, 255, 0), shifted_rect, width=2)

        for rect in self.spades_list:
            shifted_rect = rect.move(-self.camera_x, -self.camera_y)
            pygame.draw.rect(self.screen, (0, 0, 255), shifted_rect, width=2)

        for monster in self.all_monsters:
            # Décaler la position du monstre selon la position de la caméra
            display_x = monster.rect.x - self.camera_x
            display_y = monster.rect.y - self.camera_y
            self.screen.blit(monster.image, (display_x, display_y))
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