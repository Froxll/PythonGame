import pygame
# from player import Player
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

        self.background = pygame.image.load("img/Map.png")
        self.background = pygame.transform.scale(self.background, self.screen.get_size())  # Ajuste à la taille de l'écran

        self.full_map = pygame.image.load("img/Map.png")

        self.camera_x = 0
        self.camera_y = 0

        # Taille de la fenêtre
        self.window_width, self.window_height = window_size

        self.all_monsters = pygame.sprite.Group()
        self.spawn_monsters()

    def spawn_monsters(self):
        golem_positions = [
            (1260, 1735, 1260, 1620),   # Spawn en x:1260 y:1735 et va de 1260 à 1620 en x
            (3988, 1737, 3988, 4372),
            (184, 84, 184, 568),
            (2700, 1929, 2700, 2910),
        ]

        for pos in golem_positions:
            monster = Monster(*pos)
            self.all_monsters.add(monster)

    def setup(self):

        # self.player = Player(self.screen, 50)
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

        # Vérifier les touches pressées
        keys = pygame.key.get_pressed()
        speed = 10  # Vitesse de déplacement de la caméra

        # Déplacer la caméra selon les touches fléchées
        if keys[pygame.K_LEFT]:
            self.camera_x = max(0, self.camera_x - speed)  # Empêcher d'aller en dehors de la map
        if keys[pygame.K_RIGHT]:
            self.camera_x = min(5755 - self.window_width, self.camera_x + speed)  # Empêcher d'aller trop loin
        if keys[pygame.K_UP]:
            self.camera_y = max(0, self.camera_y - speed)
        if keys[pygame.K_DOWN]:
            self.camera_y = min(2164 - self.window_height, self.camera_y + speed)

    def update(self):
        # Mettre à jour tous les monstres avec le delta time (dt)
        self.all_monsters.update(self.dt)

    def display(self):
        # Découper la portion de la map visible selon la position de la caméra
        map_view = self.full_map.subsurface((self.camera_x, self.camera_y, self.window_width, self.window_height))

        # Dessiner la portion de la map
        self.screen.blit(map_view, (0, 0))
        
        # Dessiner les monstres
        for monster in self.all_monsters:
            # Décaler la position du monstre selon la position de la caméra
            display_x = monster.rect.x - self.camera_x
            display_y = monster.rect.y - self.camera_y
            self.screen.blit(monster.image, (display_x, display_y))

        pygame.display.flip()