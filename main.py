import sys
import time
import pygame

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bob games")
clock = pygame.time.Clock()

# Charger l'image de fond pour la carte
background = pygame.image.load("assets/scene.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# Définir les couleurs de collision pour les obstacles, la fin et le spawn
OBSTACLE_COLOR = (0, 0, 0)  # Noir
WIN_COLOR = (118, 255, 68)  # Vert
SPAWN_COLOR = (255, 0, 0)  # Rouge

# Classe pour le sprite Bob
class Bob(pygame.sprite.Sprite):
    def __init__(self, path, position, start):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.velocity = 3
        # Position de départ
        self.rect.x = start[0]
        self.rect.y = start[1]

    def check_collision(self, x_offset=0, y_offset=0):
        """Vérifie les pixels aux bords pour détecter une collision avec un obstacle."""
        for x in range(self.rect.left + x_offset, self.rect.right + x_offset):
            if 0 <= x < screen_width:
                if 0 <= self.rect.top + y_offset < screen_height and \
                background.get_at((x, self.rect.top + y_offset)) == OBSTACLE_COLOR:
                    return True
                if 0 <= self.rect.bottom + y_offset < screen_height and \
                background.get_at((x, self.rect.bottom + y_offset)) == OBSTACLE_COLOR:
                    return True

        for y in range(self.rect.top + y_offset, self.rect.bottom + y_offset):
            if 0 <= y < screen_height:
                if 0 <= self.rect.left + x_offset < screen_width and \
                background.get_at((self.rect.left + x_offset, y)) == OBSTACLE_COLOR:
                    return True
                if 0 <= self.rect.right + x_offset < screen_width and \
                background.get_at((self.rect.right + x_offset, y)) == OBSTACLE_COLOR:
                    return True

        return False



    def go_left(self):
        if self.rect.x >= 0:
            # Vérifiez la collision à gauche avant de déplacer
            if not self.check_collision(-self.velocity, 0):
                self.rect.x -= self.velocity

    def go_right(self):
        if self.rect.right < screen_width:
            # Vérifiez la collision à droite avant de déplacer
            if not self.check_collision(self.velocity, 0):
                self.rect.x += self.velocity

    def go_up(self):
        if self.rect.y >= 0:
            # Vérifiez la collision en haut avant de déplacer
            if not self.check_collision(0, -self.velocity):
                self.rect.y -= self.velocity

    def go_down(self):
        if self.rect.bottom < screen_height:
            # Vérifiez la collision en bas avant de déplacer
            if not self.check_collision(0, self.velocity):
                self.rect.y += self.velocity

# Création du joueur
sprite = Bob("assets/player.png", (screen_width // 2, screen_height // 2), (30, 530))
sprites_group = pygame.sprite.Group()
sprites_group.add(sprite)

# Création du point d'arrivée (en haut à droite, juste un rectangle de couleur)
end_rect = pygame.Rect(screen_width - 100, 0, 220, 90)  # (x, y, largeur, hauteur)
end_group = pygame.sprite.Group()  # Nous n'en avons pas besoin pour l'affichage, mais juste pour gérer les collisions

HAS_MOVED = False
STARTED_MOVING = None

class Enemi(pygame.sprite.Sprite):
    def __init__(self, path, position, start, velocity):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.velocity = velocity
        # Position de départ
        self.rect.x = start[0]
        self.rect.y = start[1]
    
    def update(self):
        # if collision with player
        if self.rect.colliderect(sprite.rect):
            print("collision")
            sprite.rect.x = 30
            sprite.rect.y = 530
        self.rect.x += self.velocity
        if self.rect.x > screen_width:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = screen_width

enemy_coord = [(6, 404), (567, 275)]

enemi_group = pygame.sprite.Group()
for coord in enemy_coord:
    enemi = Enemi("assets/enemi.png", (screen_width // 2, screen_height // 2), coord, 5)
    enemi_group.add(enemi)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    # Gestion du mouvement du joueur
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        sprite.go_left()
    if keys[pygame.K_RIGHT]:
        sprite.go_right()
    if keys[pygame.K_UP]:
        sprite.go_up()
    if keys[pygame.K_DOWN]:
        sprite.go_down()

    # Vérification de la victoire dès que Bob touche la zone de victoire
    if sprite.rect.colliderect(end_rect):
        CHRONO_END = time.time() - STARTED_MOVING
        print("Félicitations ! Vous avez atteint la fin. Temps : {} secondes.".format(CHRONO_END))
        running = False  # Arrêter la boucle principale

    # Démarrage du chrono dès le premier mouvement
    if not HAS_MOVED and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
        print("Début du chrono")
        STARTED_MOVING = time.time()
        HAS_MOVED = True

    # Affichage de fond avec la carte
    screen.blit(background, (0, 0))
    
    # Dessiner tous les sprites (joueur et ennemis)
    sprites_group.draw(screen)
    sprites_group.update()
    enemi_group.draw(screen)
    enemi_group.update()
    sprites_group.draw(screen)
    sprites_group.update()
    # Dessiner le point d'arrivée (invisible pour le joueur)
    pygame.draw.rect(screen, WIN_COLOR, end_rect)  

    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(100)

pygame.quit()
