import pygame


class Monster(pygame.sprite.Sprite):

    def __init__(self, x, y, left_limit, right_limit):
        super().__init__()

        self.health = 100
        self.max_health = 100
        self.attack = 5

        # Charger les images du golem
        self.images_normal = []
        self.images_flipped = []  

        for i in range(18):
            img_path = f'img/Golem/Walking/Golem_01_Walking_{i:03d}.png'
            img = pygame.image.load(img_path)
            self.images_normal.append(pygame.transform.scale(img, (150, 150)))
            flipped_img = pygame.transform.flip(img, True, False)
            self.images_flipped.append(pygame.transform.scale(flipped_img, (150, 150)))

        # Initialiser l'image du golem
        self.image = self.images_normal[0]  # Prendre la première image pour initialiser
        self.rect = self.image.get_rect()
        self.rect.x = x  # Position en X
        self.rect.y = y  # Position en Y

        # Limites du mouvement
        self.left_limit = left_limit
        self.right_limit = right_limit

        # Direction et vitesse
        self.facing_right = True
        self.speed = 1

        # Animation
        self.current_image = 0
        self.time_since_last_update = 0
        self.animation_speed = 0.2

    def update(self, dt):
    # Mise à jour de l'animation
        self.time_since_last_update += dt
        if self.time_since_last_update >= self.animation_speed:
            self.time_since_last_update = 0
            self.current_image = (self.current_image + 1) % len(self.images_normal)
            self.image = self.images_normal[self.current_image] if self.facing_right else self.images_flipped[self.current_image]

        # Déplacement du monstre
        self.rect.x += self.speed if self.facing_right else -self.speed  

        # Changer de direction aux limites
        if self.rect.x >= self.right_limit:
            self.facing_right = False
        elif self.rect.x <= self.left_limit:
            self.facing_right = True