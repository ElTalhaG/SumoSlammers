import pygame
import math  # For distance calculation

# Initialiser Pygame
pygame.init()

# Skærmstørrelse
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sumo Fighter Prototype")

# Farver
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Spilkonstanter
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLAYER_SPEED = 5
KNOCKBACK_FORCE = 10
FRICTION = 0.85
PLAYER_RADIUS = 25  # Juster radius til ellipse-formen (halv bredde og højde)

class Player:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 50)  # Spillerens rektangulære form og startposition
        self.color = color  # Farven på spilleren
        self.vel_x = 0  # Vandret hastighed
        self.vel_y = 0  # Lodret hastighed

    def move(self, left, right, jump):
        keys = pygame.key.get_pressed()  # Tjekker hvilke taster der er trykket ned
        if keys[left]:
            self.vel_x = -PLAYER_SPEED  # Bevæg til venstre
        if keys[right]:
            self.vel_x = PLAYER_SPEED  # Bevæg til højre
        if keys[jump] and self.rect.bottom >= ground.top:  # Hvis spilleren står på platformen og hopper
            self.vel_y = JUMP_STRENGTH  # Hop, hvis spilleren står på en platform

    def apply_physics(self):
        self.vel_y += GRAVITY  # Anvend tyngdekraft
        self.rect.x += self.vel_x  # Opdater spillerens position i x-retningen
        self.rect.y += self.vel_y  # Opdater spillerens position i y-retningen
        self.vel_x *= FRICTION  # Anvend friktion, så spilleren ikke glider uendeligt

        # Hold spilleren på platformen
        if self.rect.bottom >= ground.top:  # Hvis spilleren er på platformen
            self.rect.bottom = ground.top  # Sørg for at spilleren lander på platformen
            self.vel_y = 0  # Nulstil lodret hastighed

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)  # Tegn spilleren som en ellipse (bruger rektangel til beregning, men visualiserer som ellipse)

    def get_center(self):
        """Returnerer spillerens centerkoordinater (bruges til afstandskontrol)"""
        return self.rect.center  # Returnerer centrum af spillerens rektangel

# Opret spillere
player1 = Player(200, 400, RED)  # Spiller 1 (rød)
player2 = Player(550, 400, BLUE)  # Spiller 2 (blå)

ground = pygame.Rect(100, 500, 600, 20)  # Platform (grøn)
clock = pygame.time.Clock()
run = True

while run:
    screen.fill(WHITE)  # Fyld skærmen med hvid baggrund
    pygame.draw.rect(screen, GREEN, ground)  # Tegn platformen
    player1.draw(screen)  # Tegn spiller 1
    player2.draw(screen)  # Tegn spiller 2
    
    player1.move(pygame.K_a, pygame.K_d, pygame.K_w)  # Spiller 1 bevægelse (AWD)
    player2.move(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)  # Spiller 2 bevægelse (piletaster)
    
    player1.apply_physics()  # Opdater spiller 1s fysik
    player2.apply_physics()  # Opdater spiller 2s fysik
    
    # Kollision mellem spillerne
    center1 = player1.get_center()  # Få centrum af spiller 1
    center2 = player2.get_center()  # Få centrum af spiller 2

    # Beregn afstanden mellem spillerne
    distance = math.dist(center1, center2)  # Brug math.dist til at beregne den faktiske afstand mellem spillernes midtpunkter

    # Hvis afstanden er mindre end summen af radierne (det vil sige de overlapper)
    if distance < PLAYER_RADIUS * 2:  # 2 gange radiusen fordi vi sammenligner hele diameteren
        overlap = PLAYER_RADIUS * 2 - distance  # Hvor meget de overlapper
        
        # Beregn retningen for knockback
        direction = (center1[0] - center2[0], center1[1] - center2[1])  # Find retning fra spiller 2 til spiller 1
        norm = math.sqrt(direction[0]**2 + direction[1]**2)  # Beregn længden af retningen (normalisering)
        direction = (direction[0] / norm, direction[1] / norm)  # Normaliser retningen, så den bliver en enhedsvektor
        
        # Skub spillerne væk baseret på overlap og retning
        player1.rect.x += direction[0] * overlap / 2  # Flyt spiller 1 væk fra spiller 2
        player1.rect.y += direction[1] * overlap / 2  # Flyt spiller 1 væk fra spiller 2
        player2.rect.x -= direction[0] * overlap / 2  # Flyt spiller 2 væk fra spiller 1
        player2.rect.y -= direction[1] * overlap / 2  # Flyt spiller 2 væk fra spiller 1

        # Anvend knockback
        knockback_direction = 1 if player1.rect.x < player2.rect.x else -1  # Bestem knockback-retning
        player1.vel_x = -KNOCKBACK_FORCE * knockback_direction  # Anvend knockback på spiller 1
        player2.vel_x = KNOCKBACK_FORCE * knockback_direction  # Anvend knockback på spiller 2
    
    pygame.display.update()  # Opdater skærmen
    clock.tick(60)  # Sætter spillet til at køre ved 60 FPS
    
    for event in pygame.event.get():  # Gennemgå alle hændelser
        if event.type == pygame.QUIT:  # Hvis spilleren lukker vinduet
            run = False  # Afslut spilløkken

pygame.quit()  # Afslut Pygame
