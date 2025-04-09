import pygame
import random


class Monster(pygame.sprite.Sprite):

    def __init__(self, x, y, left_limit, right_limit, player):
        super().__init__()

        self.player = player
        self.hp = 4

        self.images_walking_normal = []
        self.images_walking_flipped = []
        self.images_attack_normal = []
        self.images_attack_flipped = []

        for i in range(18):
            img_path = f'img/Golem/Walking/Golem_01_Walking_{i:03d}.png'
            img = pygame.image.load(img_path)
            self.images_walking_normal.append(pygame.transform.scale(img, (150, 150)))
            flipped_img = pygame.transform.flip(img, True, False)
            self.images_walking_flipped.append(pygame.transform.scale(flipped_img, (150, 150)))

        for i in range(12):
            img_path = f'img/Golem/Attacking/Golem_01_Attacking_{i:03d}.png'
            img = pygame.image.load(img_path)
            scaled_img = pygame.transform.scale(img, (150, 150))

            self.images_attack_normal.append(scaled_img)
            flipped = pygame.transform.flip(img, True, False)
            self.images_attack_flipped.append(pygame.transform.scale(flipped, (150, 150)))

        self.image = self.images_walking_normal[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hitbox = pygame.Rect(
            self.rect.x + 40,
            self.rect.y + 30,
            self.rect.width - 80,
            self.rect.height - 35,
        )

        self.left_limit = left_limit
        self.right_limit = right_limit

        self.facing_right = True
        self.speed = 1

        self.current_image = 0
        self.time_since_last_update = 0
        self.animation_speed = 0.1

        self.state = "walk"
        self.attack_timer = 0

    def update_walking(self):
        if self.time_since_last_update >= self.animation_speed:
            self.time_since_last_update = 0
            self.current_image += 1
            if self.current_image >= len(self.images_walking_normal):
                self.current_image = 0

            if self.facing_right:
                self.image = self.images_walking_normal[self.current_image]
            else:
                self.image = self.images_walking_flipped[self.current_image]

    def update_attack(self, player_position):
        if self.time_since_last_update >= self.animation_speed:
            self.time_since_last_update = 0
            self.current_image += 1

            if self.current_image == 11 and self.rect.colliderect(self.player.hit_box):
                self.player.hp -= 1


            if player_position < self.rect.centerx:
                self.facing_right = False
            else:
                self.facing_right = True

            if self.current_image >= len(self.images_attack_normal):
                self.state = "walk"
                self.current_image = 0
            else:
                if self.facing_right:
                    self.image = self.images_attack_normal[self.current_image]
                else:
                    self.image = self.images_attack_flipped[self.current_image]

    def update(self, dt, player_position):
        self.time_since_last_update += dt

        if self.state == "attack":
            self.update_attack(player_position)
        elif self.state == "walk":
            self.update_walking()

        # Mise à jour de la position
        if self.state == "walk":
            if self.facing_right:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

            if self.rect.x >= self.right_limit:
                self.facing_right = False
            elif self.rect.x <= self.left_limit:
                self.facing_right = True

        self.hitbox.x = self.rect.x + 40
        self.hitbox.y = self.rect.y + 30
        self.hitbox.width = self.rect.width - 80
        self.hitbox.height = self.rect.height - 35
