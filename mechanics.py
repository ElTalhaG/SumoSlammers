import pygame

# Start Pygame
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

# Spilleregenskaber
player1 = pygame.Rect(200, 400, 50, 50)  # Spiller 1 (rød)
player2 = pygame.Rect(550, 400, 50, 50)  # Spiller 2 (blå)

vel_y1 = 0  # Vertikal hastighed for spiller 1
vel_y2 = 0  # Vertikal hastighed for spiller 2

ground = pygame.Rect(100, 500, 600, 20)  # Platform (grøn)

clock = pygame.time.Clock()
run = True

while run:
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, ground)  # Tegn platformen
    pygame.draw.ellipse(screen, RED, player1)  # Tegn spiller 1
    pygame.draw.ellipse(screen, BLUE, player2)  # Tegn spiller 2
    
    keys = pygame.key.get_pressed()
    
    # Bevægelse spiller 1 (AWD)
    if keys[pygame.K_a]:
        player1.x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player1.x += PLAYER_SPEED
    if keys[pygame.K_w] and player1.bottom >= ground.top:
        vel_y1 = JUMP_STRENGTH
    
    # Bevægelse spiller 2 (piletasterne)
    if keys[pygame.K_LEFT]:
        player2.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player2.x += PLAYER_SPEED
    if keys[pygame.K_UP] and player2.bottom >= ground.top:
        vel_y2 = JUMP_STRENGTH
    
    # Anvend tyngdekraft
    vel_y1 += GRAVITY
    vel_y2 += GRAVITY
    
    player1.y += vel_y1
    player2.y += vel_y2
    
    # Hold spillerne på platformen
    if player1.bottom >= ground.top:
        player1.bottom = ground.top
        vel_y1 = 0
    if player2.bottom >= ground.top:
        player2.bottom = ground.top
        vel_y2 = 0
    
    pygame.display.update()
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()