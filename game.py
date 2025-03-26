import pygame

class Game:
    def __init__(self):
        # Fenêtre du jeu

        pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Caleste")

    def run(self):
        # Boucle qui permet de laisser la fenêtre affiché

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
