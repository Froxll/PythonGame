import pygame


class Monster(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 5

        # Charger les 18 images du golem
        self.images_normal = []
        self.images_flipped = []  # Liste pour les images inversées

        for i in range(18):  # Tes images vont de 0 à 17
            img_path = f'img/Golem/Walking/Golem_01_Walking_{i:03d}.png'
            img = pygame.image.load(img_path)

            # Ajouter l'image normale à la liste
            self.images_normal.append(pygame.transform.scale(img, (100, 100)))

            # Créer l'image miroir et l'ajouter à la liste des images inversées
            flipped_img = pygame.transform.flip(img, True, False)  # Inverser horizontalement
            self.images_flipped.append(pygame.transform.scale(flipped_img, (100, 100)))

        # Initialiser l'image actuelle
        self.image = self.images_normal[0]
        self.rect = self.image.get_rect()

        # Position initiale du golem
        self.rect.x = 100
        self.rect.y = 500

        # Variables pour alterner les images
        self.current_image = 0  # L'indice de l'image actuelle
        self.time_since_last_update = 0  # Temps depuis la dernière mise à jour de l'image
        self.animation_speed = 0.1  # Intervalle de temps entre chaque changement d'image (en secondes)

        # Direction du monstre (True = droite, False = gauche)
        self.facing_right = True
        self.speed = 2  # Vitesse du déplacement

    def update(self, dt):
        # Mise à jour du temps écoulé
        self.time_since_last_update += dt

        # Si le temps écoulé depuis la dernière mise à jour est supérieur à l'intervalle défini
        if self.time_since_last_update >= self.animation_speed:
            # Réinitialiser le temps
            self.time_since_last_update = 0

            # Passer à l'image suivante
            self.current_image = (self.current_image + 1) % len(self.images_normal)

            # Mettre à jour l'image du golem en fonction de la direction
            if self.facing_right:
                self.image = self.images_normal[self.current_image]
            else:
                self.image = self.images_flipped[self.current_image]

        # Déplacer le monstre
        self.rect.x += self.speed if self.facing_right else -self.speed  # Déplacement dans le bon sens

        # Si le monstre atteint la droite de l'écran, il fait demi-tour
        if self.rect.x > 1280 - self.rect.width:  # La largeur de l'écran - largeur du monstre
            self.facing_right = False  # Inverser la direction

        # Si le monstre atteint la gauche de l'écran, il fait demi-tour
        elif self.rect.x < 0:
            self.facing_right = True  # Inverser la direction