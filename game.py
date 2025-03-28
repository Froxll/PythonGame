import pygame

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

        self.image = pygame.image.load('img/Map.jpg').convert()


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

            self.screen.blit(self.image, (0,0))

            # Mise à jour et rendu des entités



            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()


