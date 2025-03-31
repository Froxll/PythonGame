import pygame
import pytmx


##from player import Player

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



        self.background = pygame.image.load("img/Map.png").convert()
        tmx_data = pytmx.load_pygame("data/MapTMX.tmx")

        self.rect_list = []
        self.ladder_list = []

        for obj in tmx_data.objects:
            if obj.name == "plateforme":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.rect_list.append(rect)
            if obj.name == "echelle":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.ladder_list.append(rect)

        # Caméra temporaire Et1
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 900

    def setup(self):

        #self.player = Player(self.screen, 50)
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            self.camera_x -= self.camera_speed * self.dt
        if keys[pygame.K_h]:
            self.camera_x += self.camera_speed * self.dt
        if keys[pygame.K_t]:
            self.camera_y -= self.camera_speed * self.dt
        if keys[pygame.K_g]:
            self.camera_y += self.camera_speed * self.dt

    def display(self):
        # self.player.draw()

        self.screen.blit(self.background, (-self.camera_x, -self.camera_y))

        for rect in self.rect_list:
            shifted_rect = rect.move(-self.camera_x, -self.camera_y)
            pygame.draw.rect(self.screen, (255, 0, 0), shifted_rect, width=4)
        
        for rect in self.ladder_list:
            shifted_rect = rect.move(-self.camera_x, -self.camera_y)
            pygame.draw.rect(self.screen, (255, 0, 0), shifted_rect, width=4)




        pygame.display.flip()


