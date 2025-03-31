import pygame


class Monster(pygame.sprite.Sprite):

    def __init__(self, x, y, left_limit, right_limit):
        super().__init__()

        self.health = 100
        self.max_health = 100
        self.attack = 5

        # On créé les tableaux pour stocker les images du golem
        self.images_normal = []
        self.images_flipped = []

        for i in range(18):  # On stock les images d'animations du golem en version normale et en mirror
            img_path = f'img/Golem/Walking/Golem_01_Walking_{i:03d}.png'
            img = pygame.image.load(img_path)
            self.images_normal.append(pygame.transform.scale(img, (150, 150)))
            flipped_img = pygame.transform.flip(img, True, False)
            self.images_flipped.append(pygame.transform.scale(flipped_img, (150, 150)))

        self.image = self.images_normal[0]  # On prend la première image pour initialiser notre golem
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Limites du mouvement
        self.left_limit = left_limit
        self.right_limit = right_limit

        # Direction et vitesse
        self.facing_right = True
        self.speed = 2

        # Animation
        self.current_image = 0
        self.time_since_last_update = 0
        self.animation_speed = 0.1

    def update(self, dt):
        # Mise à jour de l'animation
        self.time_since_last_update += dt
        if self.time_since_last_update >= self.animation_speed:
            self.time_since_last_update = 0
            self.current_image = (self.current_image + 1) % len(self.images_normal)
            if self.facing_right:
                self.image = self.images_normal[self.current_image]
            else:
                self.image = self.images_flipped[self.current_image]

        # Déplacement du monstre à droite ou à gauche
        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        # Changer de direction aux limites imposées
        if self.rect.x >= self.right_limit:
            self.facing_right = False
        elif self.rect.x <= self.left_limit:
            self.facing_right = True
