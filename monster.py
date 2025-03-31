import pygame
import random


class Monster(pygame.sprite.Sprite):

    def __init__(self, x, y, left_limit, right_limit):
        super().__init__()

        self.health = 100
        self.max_health = 100
        self.attack = 5

        # On créé les tableaux pour stocker les images du golem
        self.images_walking_normal = []
        self.images_walking_flipped = []
        self.images_idle_normal = []
        self.images_idle_flipped = []

        for i in range(18):  # On stock les images d'animations du golem en version normale et en mirror
            img_path = f'img/Golem/Walking/Golem_01_Walking_{i:03d}.png'
            img = pygame.image.load(img_path)
            self.images_walking_normal.append(pygame.transform.scale(img, (150, 150)))
            flipped_img = pygame.transform.flip(img, True, False)
            self.images_walking_flipped.append(pygame.transform.scale(flipped_img, (150, 150)))

        for i in range(8):
            img_path = f'img/Golem/Idle/Golem_01_Idle_{i:03d}.png'
            img = pygame.image.load(img_path)
            self.images_idle_normal.append(pygame.transform.scale(img, (150, 150)))
            flipped_img = pygame.transform.flip(img, True, False)
            self.images_idle_flipped.append(pygame.transform.scale(flipped_img, (150, 150)))

        self.image = self.images_walking_normal[0]  # On prend la première image pour initialiser notre golem
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Limites du mouvement
        self.left_limit = left_limit
        self.right_limit = right_limit

        # Direction et vitesse
        self.facing_right = True
        self.speed = 1

        # Animation
        self.current_image = 0
        self.time_since_last_update = 0
        self.animation_speed = 0.3

        # Pause
        self.is_stopped = False
        self.is_idle = False
        self.stop_timer = 0  # Temps restant d'arrêt
        self.next_stop_time = random.uniform(2, 5)  # Prochaine pause entre 2 à 5 sec

    def update(self, dt):
        self.time_since_last_update += dt
        self.next_stop_time -= dt

        # Gérer l'animation walking
        if not self.is_stopped and self.time_since_last_update >= self.animation_speed:
            self.time_since_last_update = 0
            self.current_image = (self.current_image + 1) % len(self.images_walking_normal)
            self.image = self.images_walking_normal[self.current_image] if self.facing_right else \
                self.images_walking_flipped[self.current_image]

        # Gérer la pause du golem
        if self.next_stop_time <= 0 and not self.is_stopped:
            self.is_stopped = True
            self.stop_timer = 2

        # Gérer l'animation idle quand le golem est arrêté
        if self.is_stopped:
            self.time_since_last_update += dt
            if self.time_since_last_update >= self.animation_speed:
                self.time_since_last_update = 0
                self.current_image = (self.current_image + 1) % len(self.images_idle_normal)
                self.image = self.images_idle_normal[self.current_image] if self.facing_right else \
                    self.images_idle_flipped[self.current_image]

            self.stop_timer -= dt
            if self.stop_timer <= 0:
                self.is_stopped = False
                self.next_stop_time = random.uniform(2, 5)
            return

        # Déplacement du golem à droite ou à gauche
        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        # Changer de direction aux limites imposées
        if self.rect.x >= self.right_limit:
            self.facing_right = False
        elif self.rect.x <= self.left_limit:
            self.facing_right = True
