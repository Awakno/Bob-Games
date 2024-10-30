import sys
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
        """Vérifie la couleur des pixels aux coins du sprite en avant de la direction de mouvement."""
        corners = [
            (self.rect.topleft[0] + x_offset, self.rect.topleft[1] + y_offset),     # Coin supérieur gauche
            (self.rect.topright[0] + x_offset, self.rect.topright[1] + y_offset),   # Coin supérieur droit
            (self.rect.bottomleft[0] + x_offset, self.rect.bottomleft[1] + y_offset), # Coin inférieur gauche
            (self.rect.bottomright[0] + x_offset, self.rect.bottomright[1] + y_offset) # Coin inférieur droit
        ]
        # Vérifier si un des coins rencontre une couleur d'obstacle
        for corner in corners:
            if 0 <= corner[0] < screen_width and 0 <= corner[1] < screen_height:
                pixel_color = background.get_at(corner)
                if pixel_color == OBSTACLE_COLOR:
                    return "WALL"
                if pixel_color == WIN_COLOR:
                    return "WIN"
                if pixel_color == SPAWN_COLOR:
                    return "SPAWN"
        return False

    def go_left(self):
        if self.rect.x >= 0 and not self.check_collision(-self.velocity, 0) == "WALL":
            self.rect.x -= self.velocity

    def go_right(self):
        if self.rect.right < screen_width and not self.check_collision(self.velocity, 0) == "WALL":
            self.rect.x += self.velocity

    def go_up(self):
        if self.rect.y >= 0 and not self.check_collision(0, -self.velocity) == "WALL":
            self.rect.y -= self.velocity

    def go_down(self):
        if self.rect.bottom < screen_height and not self.check_collision(0, self.velocity) == "WALL":
            self.rect.y += self.velocity

# Création du joueur
sprite = Bob("assets/player.png", (screen_width // 2, screen_height // 2), (30, 530))
sprites_group = pygame.sprite.Group()
sprites_group.add(sprite)

# Création du point d'arrivée (en haut à droite, juste un rectangle de couleur)
end_rect = pygame.Rect(screen_width - 50, 50, 50, 50)  # Point de fin
end_group = pygame.sprite.Group()  # Nous n'en avons pas besoin pour l'affichage, mais juste pour gérer les collisions

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

    # Vérification de collision avec le point de fin
    if sprite.check_collision() == "WIN":
        print("Félicitations ! Vous avez atteint la fin.")
        running = False

    # Affichage de fond avec la carte
    screen.blit(background, (0, 0))
    
    # Dessiner tous les sprites (joueur)
    sprites_group.draw(screen)

    # Dessiner le point d'arrivée (invisible pour le joueur)
    pygame.draw.rect(screen, WIN_COLOR, end_rect)  # Cela sert à la détection de collision seulement

    print(sprite.rect.x, "  |  ", sprite.rect.y)
    
    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
