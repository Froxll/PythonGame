import pygame
import os

from numpy.ma.core import true_divide


# Utilisation de la vidéo : https://youtu.be/B6DrRN5z_uU?si=vNqB4-23R81IHm74
# Création du personnage / gestion des déplacements

class Player:
    def __init__(self, screen):
        # Variable d'affichage du Joueur
        self.screen = screen

        self.images = {}
        # Appel de la fonction de chargement des images
        self.load_sprites()

        #Variable de gestion de la position / Mouvement
        # self.display_rect = self.images["idle"][0].get_rect(x=5470, y=228) # Position du perso à coté du coffre de fin
        self.display_rect = self.images["idle"][0].get_rect(x=200, y=180) # Position à côté du powerup boots
        # self.display_rect = self.images["idle"][0].get_rect(x=200, y=1970)
        self.hit_box = self.display_rect.copy()
        self.hit_box_reduction = 94
        self.hit_box_offset = 18
        self.hit_box.width -= self.hit_box_reduction
        self.hit_box.x = self.display_rect.x + self.hit_box.width / 2
        self.hit_box.y = self.display_rect.y

        # Gestion des déplacements
        self.velocity = 7
        self.x_vel = 0
        self.y_vel = 0
        self.fall_count = 0
        self.jump_count = 0
        self.jump_speed = 11
        self.side_hit_count = 0
        self.climb_speed = 5

        # Stats de jeu
        self.hp = 5
        self.damage = 1

        # Gestion des animations
        self.direction = "right"
        self.move_type = "run" # Prend la valeur d'une clé du dict des images
        self.animation_count = 0
        self.frame_count = 0 # Compteur de frame pour changer l'image seulement toute les 5 frame
        self.frame_per_animation = 6
        self.is_jumping = False



    def move(self):
        if self.hp > 0:
            self.y_vel += min(1, self.fall_count / 60)
            if self.y_vel > 18:
                self.y_vel = 18
            pressed = pygame.key.get_pressed()
            self.x_vel = 0
            if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
                self.move_left()
            elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                self.move_right()

            self.hit_box.move_ip(self.x_vel, self.y_vel)
            self.fall_count += 1


    def draw(self, camera_x, camera_y):
        display_x = self.display_rect.x - camera_x
        display_y = self.display_rect.y - camera_y

        self.check_idle()
        self.handle_animation()
        self.display_rect.x = self.hit_box.x - self.hit_box.width / 2 - self.hit_box_offset
        self.display_rect.y = self.hit_box.y
        if self.hp <= 0:
            self.handle_move_type("die")

        if self.is_jumping and self.animation_count < len(self.images["jump"]) and self.y_vel < 0:
            if self.direction == "left":
                image_flipped = pygame.transform.flip(self.images["jump"][self.animation_count], True, False)
                self.screen.blit(image_flipped, (display_x, display_y))
            elif self.direction == "right":
                self.screen.blit(self.images["jump"][self.animation_count], (display_x, display_y))
        elif self.y_vel > 1:
            self.handle_move_type("fall")
            if self.direction == "left":
                image_flipped = pygame.transform.flip(self.images[self.move_type][self.animation_count], True, False)
                self.screen.blit(image_flipped, (display_x, display_y))
            elif self.direction == "right":
                self.screen.blit(self.images[self.move_type][self.animation_count], (display_x, display_y))
        else:
            if self.direction == "left":
                # On retourne l'image en mirroir
                image_flipped = pygame.transform.flip(self.images[self.move_type][self.animation_count], True, False)
                self.screen.blit(image_flipped, (display_x, display_y))
            elif self.direction == "right":
                self.screen.blit(self.images[self.move_type][self.animation_count], (display_x, display_y))


    def move_left(self):
        self.x_vel = -self.velocity
        if self.direction != "left":
            self.direction = "left"

        self.handle_move_type("run")

    def move_right(self):
        self.x_vel = self.velocity
        if self.direction != "right":
            self.direction = "right"

        self.handle_move_type("run")

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.side_hit_count = 0
        self.is_jumping = False

    def jump(self):
        self.y_vel = -1 * self.jump_speed
        self.jump_count += 1

        self.handle_move_type("jump")
        self.is_jumping = True

    def hit_side(self):
        self.fall_count = 0
        self.y_vel = 0
        if self.side_hit_count == 0:
            self.jump_count = 0
        self.side_hit_count += 1

        self.handle_move_type("grab")


    def climb(self, climb_type):

        if climb_type == "up":
            self.y_vel = -1 * self.climb_speed
            self.handle_move_type("climb")
            self.fall_count = 150
        elif climb_type == "down":
            self.y_vel = self.climb_speed
            self.handle_move_type("climb")
            self.fall_count = 0
        self.is_jumping = False


    def handle_animation(self):
        self.frame_count += 1
        if self.move_type == "attack" and self.animation_count == len(self.images["attack"]) - 1:
            self.handle_move_type("idle")
        elif self.is_jumping and self.animation_count == len(self.images["jump"]) - 1:
            self.animation_count = len(self.images["jump"]) - 1
        elif self.hp <= 0 and self.animation_count == len(self.images["die"]) - 1:
            self.animation_count = len(self.images["die"]) - 1
        elif self.frame_count % self.frame_per_animation == 0:
            self.animation_count = (self.animation_count + 1) % len(self.images[self.move_type])


    def check_idle(self):
        if self.x_vel == 0 and self.y_vel < 1 and self.move_type != "climb" and self.move_type != "attack" and self.hp > 0 and self.move_type != "jump" and self.move_type != "die":
            if self.move_type != "idle":
                self.move_type = "idle"
                self.animation_count = 0

    def handle_move_type(self, new_move_type):
        if new_move_type != self.move_type:
            self.move_type = new_move_type
            self.animation_count = 0

    def load_sprites(self):
        # Création du dict par clés
        self.images = {
            "attack": [],
            "climb": [],
            "die": [],
            "fall": [],
            "grab": [],
            "hurt": [],
            "idle": [],
            "jump": [],
            "run": [],
        }
        # Création des images dossiers par dossiers
        load_images_folder(self.images["attack"], "player/attack")
        load_images_folder(self.images["climb"], "player/climb")
        load_images_folder(self.images["die"], "player/die")
        load_images_folder(self.images["fall"], "player/fall")
        load_images_folder(self.images["grab"], "player/grab")
        load_images_folder(self.images["hurt"], "player/hurt")
        load_images_folder(self.images["idle"], "player/idle")
        load_images_folder(self.images["jump"], "player/jump")
        load_images_folder(self.images["run"], "player/run")

def load_images_folder(images_list, path):
    folder_path = os.path.join("img/", path)
    for img_name in sorted(os.listdir(folder_path)):
        img_path = os.path.join(folder_path, img_name)
        image = pygame.image.load(img_path).convert_alpha()
        new_size = (image.get_width() * 3, image.get_height() * 3)  # Augmenter la taille de l'image du personnage (très petite)
        image = pygame.transform.scale(image, new_size)
        images_list.append(image)