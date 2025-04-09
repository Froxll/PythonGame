import math
import sys
import pygame
import pytmx
import time
from pygame import mixer
from player import Player
from monster import Monster
from button import Button
from chest import Chest
from powerup import Powerup
from EndScreensManager import EndScreensManager

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

class Game:
    def __init__(self, window_size):

        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.isRunning = True
        self.is_game_over = False

        self.window_size_w = window_size[0]
        self.window_size_h = window_size[1]

        self.player = None  # Joueur
        self.chest = None  # Coffre
        self.powerup_boots = None

        # Initialisation pour le background qui bouge
        self.background = pygame.image.load("img/Background.png").convert()
        self.scroll = 0
        self.tiles = math.ceil(SCREEN_WIDTH / self.background.get_width()) + 1
        self.map = pygame.image.load("img/Map.png").convert_alpha()


        self.heart_full = pygame.image.load("img/Lifebar/Full_Heart.png")
        self.heart_mid = pygame.image.load("img/Lifebar/Mid_Heart.png")
        self.heart_empty = pygame.image.load("img/Lifebar/Empty_Heart.png")

        heart_size = (50, 44)
        self.heart_full = pygame.transform.scale(self.heart_full, heart_size)
        self.heart_mid = pygame.transform.scale(self.heart_mid, heart_size)
        self.heart_empty = pygame.transform.scale(self.heart_empty, heart_size)

        tmx_data = pytmx.load_pygame("data/MapTMX.tmx")

        self.rect_list = []
        self.ladder_list = []
        self.spades_list = []

        # Placement des rect de collision
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

        # Caméra
        self.camera_x = 0
        self.camera_y = 0

        self.all_monsters = pygame.sprite.Group()
        self.monsters_rect_list = []
        self.hitbox_last_time = 0
        self.hitbox_delay = 2
        self.time_since_last_player_attack = 0

        self.end_screens_manager = None



    def spawn_monsters(self):
        golem_positions = [
            (1260, 1735, 1260, 1620),  # Spawn en x:1260 y:1735 et va de 1260 à 1620 en x
            (3988, 1737, 3988, 4372),
            (184, 84, 184, 568),
            (2700, 1929, 2700, 2910),
        ]

        for pos in golem_positions:
            monster = Monster(*pos, self.player)
            self.all_monsters.add(monster)

    def setup(self):

        self.player = Player(self.screen)
        self.chest = Chest(self.screen)

        self.end_screens_manager = EndScreensManager(self.screen, self.player)

        self.spawn_monsters()
        for monster in self.all_monsters:
            self.monsters_rect_list.append(monster.rect)
        self.powerup_boots = Powerup(self.screen, self.player, "boots")


    def run(self):
        while self.isRunning:
            # Structure du code : https://www.youtube.com/watch?v=N56R1V5XZBw&list=PLKeQQTikvsqkeJlhiE8mXwskOhXLKdl8m&index=3
            # Gestion de l'évenement "Quit
            state = self.handling_events()
            if state == "EXIT":
                return state
            elif state == "RESTART":
                return state
            elif state == "HOME":
                return state
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
                return "EXIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.jump_count < 1 and self.player.hp > 0:
                    self.player.jump()
                elif event.key == pygame.K_e and self.time_since_last_player_attack > self.player.frame_per_animation * len(self.player.images["attack"]) and 0 <= self.player.y_vel < 1 and self.player.hp > 0:
                    self.handle_player_attack()
                    self.handle_chest_opening()
                # TEST
                elif event.key == pygame.K_o:
                    self.is_game_over = True
                    self.player.hp = 0

            state_end = self.end_screens_manager.handle_event(event)
            if state_end == "EXIT":
                return "EXIT"
            elif state_end == "RESTART":
                return "RESTART"
            elif state_end == "HOME":
                return "HOME"





    def update(self):
        current_time = time.time()

        self.player.move()
        self.check_rect_collisions()
        self.check_ladder_collisions()
        self.handle_camera_movements()
        if self.powerup_boots is not None:
            self.check_boots_powerup_collision()

        self.all_monsters.update(self.dt, self.player.hit_box.centerx)
        self.time_since_last_player_attack += 1

        if self.player.hp <= 0:
            self.is_game_over = True

        self.all_monsters.update(self.dt, self.player.hit_box.centerx)

        for monster in self.all_monsters:
            if self.player.hit_box.colliderect(monster.rect):
                if monster.state != "attack":
                    monster.state = "attack"
                    monster.current_image = 0
                    monster.time_since_last_update = 0

            if self.player.hit_box.colliderect(monster.hitbox) and monster.hp > 0:
                if current_time - self.hitbox_last_time >= self.hitbox_delay:
                    self.player.hp -= 0.5
                    if self.player.hp == 0:
                        self.player.is_dead_by_golem = True
                    self.hitbox_last_time = current_time

    def display_lifebar(self):
        full_hearts = math.floor(self.player.hp)
        half_hearts = 0

        if self.player.hp % 1 >= 0.5:
            half_hearts = 1

        total_hearts = full_hearts + half_hearts

        empty_hearts = 5 - total_hearts

        for i in range(full_hearts):
            self.screen.blit(self.heart_full, (10 + i * 60, 10))

        if half_hearts > 0:
            self.screen.blit(self.heart_mid, (10 + full_hearts * 60, 10))

        for i in range(empty_hearts):
            self.screen.blit(self.heart_empty, (10 + (full_hearts + half_hearts + i) * 60, 10))

    def display(self):

        # Boucle qui gère le background qui bouge
        for i in range(0, self.tiles):
            self.screen.blit(self.background, (i * self.background.get_width() + self.scroll, 0))
        self.scroll -= 0.5
        if abs(self.scroll) > self.background.get_width():
            self.scroll = 0


        self.screen.blit(self.map, (-self.camera_x, -self.camera_y))



        for monster in self.all_monsters:
            # Décaler la position du monstre selon la position de la caméra
            if monster.hp > 0:
                display_x = monster.rect.x - self.camera_x
                display_y = monster.rect.y - self.camera_y
                self.screen.blit(monster.image, (display_x, display_y))

        self.chest.draw(self.camera_x, self.camera_y)

        self.player.draw(self.camera_x, self.camera_y)

        self.display_lifebar()
        if self.powerup_boots is not None:
            self.powerup_boots.draw(self.camera_x, self.camera_y)
            display_x = self.powerup_boots.display_rect.x - self.camera_x
            display_y = self.powerup_boots.display_rect.y - self.camera_y
            shifted_rect = pygame.Rect(display_x, display_y, self.powerup_boots.display_rect.width,self.powerup_boots.display_rect.height)
            pygame.draw.rect(self.screen, (0, 0, 255), shifted_rect, width=2)


        display_x = self.player.display_rect.x - self.camera_x
        display_y = self.player.display_rect.y - self.camera_y
        shifted_rect = pygame.Rect(display_x, display_y, self.player.display_rect.width, self.player.display_rect.height)
        #pygame.draw.rect(self.screen, (0, 0, 255), shifted_rect, width=2)

        """
        display_x = self.player.hit_box.x - self.camera_x
        display_y = self.player.hit_box.y - self.camera_y
        shifted_rect = pygame.Rect(display_x, display_y, self.player.hit_box.width,self.player.hit_box.height)
        #pygame.draw.rect(self.screen, (255, 0, 255), shifted_rect, width=2)
        """

        # Ecran GameOver
        if self.is_game_over:
            self.end_screens_manager.display_game_over()
        elif self.chest.is_open:
            self.end_screens_manager.display_win()


        pygame.display.flip()

    def check_rect_collisions(self):
        collision_index = self.player.hit_box.collidelist(self.rect_list)
        if  collision_index > -1:
            # J'ai essayé d'implémenter quelque chose mais ChatGPT a corrigé en me donnant cette version
            # Calculer les distances entre les bords du joueur et du rectangle touché
            dx_left = abs(self.player.hit_box.right - self.rect_list[collision_index].left)  # Distance au bord gauche de l'obstacle
            dx_right = abs(self.player.hit_box.left - self.rect_list[collision_index].right)  # Distance au bord droit de l'obstacle
            dy_top = abs(self.player.hit_box.bottom - self.rect_list[collision_index].top)  # Distance au bord supérieur de l'obstacle
            dy_bottom = abs(self.player.hit_box.top - self.rect_list[collision_index].bottom)  # Distance au bord inférieur de l'obstacle

            # Trouver le côté où la collision est la plus "profonde" (le plus petit décalage)
            min_dist = min(dx_left, dx_right, dy_top, dy_bottom)

            if min_dist == dx_left:
                self.player.hit_box.right = self.rect_list[collision_index].left  # Bloquer à gauche
                self.player.hit_side()
            elif min_dist == dx_right:
                self.player.hit_box.left = self.rect_list[collision_index].right  # Bloquer à droite
                self.player.hit_side()
            elif min_dist == dy_top:
                self.player.hit_box.bottom = self.rect_list[collision_index].top  # Bloquer au sol
                self.player.landed()
            elif min_dist == dy_bottom:
                self.player.hit_box.top = self.rect_list[collision_index].bottom  # Bloquer en haut (tête du joueur)
                self.player.y_vel *= -1

    def check_ladder_collisions(self):
        collision_index = self.player.hit_box.collidelist(self.ladder_list)
        if collision_index > -1:
            pressed = pygame.key.get_pressed()
            self.player.x_vel = 0
            if pressed[pygame.K_UP] or pressed[pygame.K_z]:
                self.player.climb("up")
            elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                self.player.climb("down")
            else:
                dx_left = abs(self.player.hit_box.right - self.ladder_list[collision_index].left)  # Distance au bord gauche de l'obstacle
                dx_right = abs(self.player.hit_box.left - self.ladder_list[collision_index].right)  # Distance au bord droit de l'obstacle
                dy_top = abs(self.player.hit_box.bottom - self.ladder_list[collision_index].top)  # Distance au bord supérieur de l'obstacle
                dy_bottom = abs(self.player.hit_box.top - self.ladder_list[collision_index].bottom)  # Distance au bord inférieur de l'obstacle

                # Trouver le côté où la collision est la plus "profonde" (le plus petit décalage)
                min_dist = min(dx_left, dx_right, dy_top, dy_bottom)
                if min_dist == dy_top:
                    self.player.hit_box.bottom = self.ladder_list[collision_index].top  # Bloquer au sol
                    self.player.landed()

    def handle_camera_movements(self):
        env_width = 5755
        env_height = 2160

        self.camera_x = self.player.display_rect.x - self.window_size_w / 2 + self.player.display_rect.width / 2
        self.camera_y = self.player.display_rect.y - self.window_size_h / 2 + self.player.display_rect.height / 2
        if self.camera_x < 0:
            self.camera_x = 0

        if self.camera_y < 0:
            self.camera_y = 0

        if self.camera_x + self.window_size_w >= env_width:
            self.camera_x = env_width - self.window_size_w

        if self.camera_y + self.window_size_h >= env_height:
            self.camera_y = env_height - self.window_size_h

    def handle_player_attack(self):
        self.player.handle_move_type("attack")
        self.time_since_last_player_attack = 0
        collision_index = self.player.display_rect.collidelist(self.monsters_rect_list)
        if collision_index > -1:
            if self.all_monsters.sprites()[collision_index].hp > 0:
                self.all_monsters.sprites()[collision_index].hp -= self.player.damage

            if self.all_monsters.sprites()[collision_index].hp  <= 0:
                self.all_monsters.sprites()[collision_index].hp  = 0

    def handle_chest_opening(self):
        collision_index = self.player.display_rect.colliderect(self.chest.display_rect)
        print(collision_index)
        if collision_index:
            self.chest.open()

    def check_boots_powerup_collision(self):
        collision = self.player.hit_box.colliderect(self.powerup_boots.display_rect)
        if collision:
            self.player.obtain_powerup("boots")
            self.powerup_boots = None