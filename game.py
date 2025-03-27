import pygame
from monster import Monster

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
        self.power_ups = None # Liste des power-ups

        self.all_monsters = pygame.sprite.Group()

    def spawn_monster(self):
        monster = Monster()
        self.all_monsters.add(monster)
    def setup(self):
        """
        self.player = ...
        self.platforms = ...
        self.enemies = ...
        self.power_ups = ...
        """


    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            self.screen.fill("black")

            # Mise à jour et rendu des entités

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()


