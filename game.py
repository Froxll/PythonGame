import pygame
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

        self.all_monsters = pygame.sprite.Group()
        self.spawn_monster()

    def spawn_monster(self):
        monster = Monster()
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

    def update(self):
        self.player.move()

    def display(self):
        self.screen.fill("black")
        self.player.draw()
        pygame.display.flip()
