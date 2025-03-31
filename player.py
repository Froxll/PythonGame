import pygame
import os


# Utilisation de la vidéo : https://youtu.be/B6DrRN5z_uU?si=vNqB4-23R81IHm74
# Création du personnage / gestion des déplacements

class Player:
    def __init__(self, screen, max_health):
        # Variable d'affichage du Joueur
        self.screen = screen

        self.images = {}
        # Appel de la fonction de chargement des images
        self.load_sprites()

        self.image = self.images["run"][0]
        new_size = (self.image.get_width() * 3, self.image.get_height() * 3)  # Diviser la taille par 2
        self.image = pygame.transform.scale(self.image, new_size)

        #Variable de gestion de la position / Mouvement
        self.rect = self.image.get_rect(x=200, y=1995)

        self.velocity = 5
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.fall_count = 0

        self.jump_count = 0
        self.jump_speed = 12
        self.side_hit_count = 0

        self.climb_speed = 5

        self.hp = max_health



    def move(self):
        self.y_vel += min(1, self.fall_count / 60)
        if self.y_vel > 18:
            self.y_vel = 18
        pressed = pygame.key.get_pressed()
        self.x_vel = 0
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.move_left()
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.move_right()

        self.rect.move_ip(self.x_vel, self.y_vel)
        self.fall_count += 1

    def draw(self, camera_x, camera_y):
        display_x = self.rect.x - camera_x
        display_y = self.rect.y - camera_y
        if self.direction == "left":
            # On retourne l'image en mirroir
            image_flipped = pygame.transform.flip(self.image, True, False)
            self.screen.blit(image_flipped, (display_x, display_y))
        elif self.direction == "right":
            self.screen.blit(self.image, (display_x, display_y))

    def move_left(self):
        self.x_vel = -self.velocity
        if self.direction != "left":
            self.direction = "left"
            #self.animation_count = 0

    def move_right(self):
        self.x_vel = self.velocity
        if self.direction != "right":
            self.direction = "right"
            # self.animation_count = 0

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.side_hit_count = 0

    def jump(self):
        self.y_vel = -1 * self.jump_speed
        self.jump_count += 1

    def hit_side(self):
        self.fall_count = 0
        if self.side_hit_count == 0:
            self.jump_count = 0
        self.side_hit_count += 1
        self.y_vel = self.side_hit_count / 10


    def climb(self, climb_type):
        self.fall_count = 0
        if climb_type == "up":
            self.y_vel = -1 * self.climb_speed
        elif climb_type == "down":
            self.y_vel = self.climb_speed

    def load_sprites(self):
        # Création du dict par clés
        self.images = {
            "attack": [[], [], []],
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
        load_images_folder(self.images["attack"][0], "attack/1")
        load_images_folder(self.images["attack"][1], "attack/2")
        load_images_folder(self.images["attack"][2], "attack/3")
        load_images_folder(self.images["climb"], "climb")
        load_images_folder(self.images["die"], "die")
        load_images_folder(self.images["fall"], "fall")
        load_images_folder(self.images["grab"], "grab")
        load_images_folder(self.images["hurt"], "hurt")
        load_images_folder(self.images["idle"], "idle")
        load_images_folder(self.images["jump"], "jump")
        load_images_folder(self.images["run"], "run")

def load_images_folder(images_list, path):
    folder_path = os.path.join("img/player/", path)
    for img_name in sorted(os.listdir(folder_path)):
        img_path = os.path.join(folder_path, img_name)
        image = pygame.image.load(img_path).convert_alpha()
        images_list.append(image)