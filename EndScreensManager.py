import pygame
from pygame import mixer
from button import Button

# Classe qui gère les écrans de fins (Game Over ou Win)
class EndScreensManager:
    def __init__(self, screen, player):
        mixer.init()

        # Récupération des arguments nécessaires pour le fonctionnement de la classe
        self.screen = screen
        self.player = player

        # Initialisation des images et bouton "Retour vers le menu prinicipal"/"Home"
        self.home_1 = pygame.image.load("img/Game/MainMenu_Btn/Home_1.png").convert_alpha()
        self.home_2 = pygame.image.load("img/Game/MainMenu_Btn/Home_2.png").convert_alpha()
        self.home_button = Button(1225, 50, self.home_1, "home_1", self.screen, False, 1.5)

        # Gestion de l'animation du bouton "Home"
        self.home_button_pressed = False
        self.home_button_press_time = 0
        self.home_button_press_delay = 200  # en ms

        # Booléen qui gère l'envoi vers le menu principal
        self.go_home = False

        # Initialisation pour l'écran de Game Over
        game_over_img = pygame.image.load("img/Game/Game_Over.png").convert_alpha()
        self.game_over = None
        self.rect_game_over = None
        restart_img = pygame.image.load("img/Game/Restart_Button.png").convert_alpha()
        exit_img = pygame.image.load("img/Game/Exit_Button.png").convert_alpha()
        self.restart_button_go = Button(645, 400,restart_img, "restart", self.screen, True, 0.30, 0.35)
        self.exit_button_go = Button(645, 550, exit_img, "exit", self.screen, True, 0.28, 0.33)
        self.music_game_over = False

        self.game_over_logo = pygame.transform.smoothscale(game_over_img, (int(game_over_img.get_width() * 0.5), int(game_over_img.get_height() * 0.5)))
        self.rect_game_over = self.game_over_logo.get_rect()
        self.rect_game_over.topleft = (460, 40)
        self.is_game_over = False


        # Initialisation pour l'écran de Win
        win_img = pygame.image.load("img/Game/Win.png").convert_alpha()
        self.win = None
        self.rect_win = None
        self.restart_button_win = Button(660, 400, restart_img, "restart", self.screen, True, 0.30, 0.35)
        self.exit_button_win = Button(660, 550, exit_img, "exit", self.screen, True, 0.28, 0.33)
        self.music_win = False

        self.win_logo = pygame.transform.smoothscale(win_img, (int(win_img.get_width() * 0.5), int(win_img.get_height() * 0.5)))
        self.rect_win = self.win_logo.get_rect()
        self.rect_win.topleft = (460, 50)
        self.is_win = False


    # Fonction qui affiche l'écran "Game Over" qui se positionne au-dessus de l'écran
    def display_game_over(self):
        # Affichage de la surface foncé de l'écran
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        self.is_game_over = True
        # Affichage du logo
        self.screen.blit(self.game_over_logo, self.rect_game_over)

        # Affichage et lancement des boutons du menu "Game Over"
        self.restart_button_go.update()
        self.restart_button_go.draw()
        self.exit_button_go.update()
        self.exit_button_go.draw()
        self.home_button.update()
        self.home_button.draw()

        # Gestion de la musique (en fonction de la mort)
        if not self.music_game_over:
            self.music_game_over = True
            if self.player.is_dead_by_golem:
                mixer.music.load('audio/tk78_55milliards.mp3')
                mixer.music.set_volume(0.5)
            else:
                mixer.music.load('audio/tk78_maisNAN.mp3')
                mixer.music.set_volume(1)

            mixer.music.play()

        # Gestion de l'animation du bouton "Home"
        if self.home_button_pressed:
            if pygame.time.get_ticks() - self.home_button_press_time > self.home_button_press_delay:
                if self.home_button.type_button == "home_1":
                    self.home_button.set_image(self.home_2)
                self.home_button_pressed = False
                self.go_home = True

    # Affichage de l'écran "Win" qui se positionne au-dessus de l'écran
    def display_win(self):
        # Affichage de la surface foncé de l'écran
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0,0))
        self.is_win = True
        # Affichage du logo
        self.screen.blit(self.win_logo, self.rect_win)

        # Affichage et lancement des boutons du menu "Win"
        self.restart_button_win.update()
        self.restart_button_win.draw()
        self.exit_button_win.update()
        self.exit_button_win.draw()
        self.home_button.update()
        self.home_button.draw()

        # Gestion de la musique
        if not self.music_win:
            self.music_win = True
            mixer.music.load('audio/EndMusic.mp3')
            mixer.music.set_volume(0.25)
            mixer.music.play()

        # Gestion de l'animation du bouton "Home"
        if self.home_button_pressed:
            if pygame.time.get_ticks() - self.home_button_press_time > self.home_button_press_delay:
                if self.home_button.type_button == "home_1":
                    self.home_button.set_image(self.home_2)
                self.home_button_pressed = False
                self.go_home = True


    def handle_event(self, event):
        if self.go_home:
            return "HOME"

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Gestion du clic sur le bouton "Home"
            if self.home_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.home_button_pressed = True
                self.home_button_press_time = pygame.time.get_ticks()

                if self.home_button.type_button == "home_1":
                    self.home_button.set_image(self.home_2)
                    mixer.music.stop()
                    self.home_button.type_button = "home_2"
                elif self.home_button.type_button == "home_2":
                    self.home_button.set_image(self.home_1)
                    mixer.music.stop()
                    self.home_button.type_button = "home_1"

            # Événements des boutons du Game Over
            if self.restart_button_go is not None and self.is_game_over:
                if self.restart_button_go.rect.collidepoint(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    mixer.music.load('audio/MainMenu_music.mp3')
                    mixer.music.set_volume(0.2)
                    mixer.music.play()
                    return "RESTART"
            if self.exit_button_go is not None and self.is_game_over:
                if self.exit_button_go.rect.collidepoint(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    return "EXIT"

            # Événements des boutons du Win
            if self.restart_button_win is not None and self.is_win:
                if self.restart_button_win.rect.collidepoint(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    mixer.music.load('audio/MainMenu_music.mp3')
                    mixer.music.set_volume(0.2)
                    mixer.music.play()
                    return "RESTART"
            if self.exit_button_win is not None and self.is_win:
                if self.exit_button_win.rect.collidepoint(pygame.mouse.get_pos()):
                    mixer.music.stop()
                    return "EXIT"