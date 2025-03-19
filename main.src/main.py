import pygame
import math
import time
from config import *
from spiller import Spiller

class GameState:
    MENU = 0
    BATTLE = 1
    PAUSE = 2
    ROUND_END = 3

def display_points(window, spiller1, spiller2, time_left):
    # Top bar background
    pygame.draw.rect(window, GRAY, (0, 0, WIDTH, 50))
    
    # Players' points and names
    p1_text = f"{spiller1.name}: {spiller1.points}"
    p2_text = f"{spiller2.name}: {spiller2.points}"
    
    font = pygame.font.Font(None, MEDIUM_FONT)
    p1_render = font.render(p1_text, True, RED)
    p2_render = font.render(p2_text, True, BLUE)
    
    window.blit(p1_render, (20, 10))
    window.blit(p2_render, (WIDTH - 20 - p2_render.get_width(), 10))
    
    # Timer in the middle
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    time_text = f"{minutes}:{seconds:02d}"
    time_render = font.render(time_text, True, BLACK)
    window.blit(time_render, (WIDTH//2 - time_render.get_width()//2, 10))

def display_round_start(window, round_num):
    # Create a transparent surface for the text
    text_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    font = pygame.font.Font(None, MEDIUM_FONT)
    text = font.render(f"Round {round_num}", True, (*BLACK[:3], 180))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    text_surface.blit(text, text_rect)
    
    window.blit(text_surface, (0, 0))

def display_winner(window, winner):
    # Background overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    window.blit(overlay, (0, 0))
    
    # Winner text
    font = pygame.font.Font(None, LARGE_FONT)
    text = font.render(f"{winner.name} Wins!", True, GOLD)
    window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
    
    # Instructions
    font = pygame.font.Font(None, SMALL_FONT)
    text = font.render("Press SPACE to start a new match", True, WHITE)
    window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 50))

def handle_collision(spiller1, spiller2):
    """Handle collision between two players"""
    # Find distance between players
    center1 = spiller1.get_center()
    center2 = spiller2.get_center()
    distance = math.dist(center1, center2)
    
    # If players are touching
    if distance < PLAYER_SIZE * 2 and not (spiller1.is_dead or spiller2.is_dead):
        # Determine direction based on players' position and direction
        direction = 1 if center1[0] < center2[0] else -1
        
        # Calculate force based on speed and dash
        spiller1_force = abs(spiller1.speed_x) * (1.5 if spiller1.is_dashing else 1)
        spiller2_force = abs(spiller2.speed_x) * (1.5 if spiller2.is_dashing else 1)
        
        # Apply damage and knockback based on who is most active
        if (spiller1.is_dashing or spiller1_force > 2) and spiller2.recovery_frames == 0:
            force = BASE_KNOCKBACK * (1.8 if spiller1.is_dashing else 1)
            force *= (1 + spiller2.damage / 100)
            
            # Update combo system
            if spiller1 == spiller2.last_attacker:
                spiller2.combo_count += 1
            else:
                spiller2.combo_count = 1
            spiller2.last_attacker = spiller1
            spiller2.combo_timer = 120
            
            # Less damage on dash
            damage = DAMAGE_AMOUNT * (DASH_DAMAGE_BONUS if spiller1.is_dashing else 1)
            spiller2.damage = min(spiller2.damage + damage, MAX_DAMAGE)
            spiller2.apply_knockback((direction, -0.15), force)
            
        if (spiller2.is_dashing or spiller2_force > 2) and spiller1.recovery_frames == 0:
            force = BASE_KNOCKBACK * (1.8 if spiller2.is_dashing else 1)
            force *= (1 + spiller1.damage / 100)
            
            # Update combo system
            if spiller2 == spiller1.last_attacker:
                spiller1.combo_count += 1
            else:
                spiller1.combo_count = 1
            spiller1.last_attacker = spiller2
            spiller1.combo_timer = 120
            
            # Less damage on dash
            damage = DAMAGE_AMOUNT * (DASH_DAMAGE_BONUS if spiller2.is_dashing else 1)
            spiller1.damage = min(spiller1.damage + damage, MAX_DAMAGE)
            spiller1.apply_knockback((-direction, -0.15), force)
        
        # Push players apart to avoid overlap
        overlap = PLAYER_SIZE * 2 - distance
        if center1[0] < center2[0]:
            spiller1.body.x -= overlap / 2
            spiller2.body.x += overlap / 2
        else:
            spiller1.body.x += overlap / 2
            spiller2.body.x -= overlap / 2

def main():
    """Main game loop"""
    pygame.init()
    pygame.font.init()
    
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sumo Battle!")
    
    # Create players with fixed spawn positions
    spiller1 = Spiller(PLATFORM_X + SPAWN_DISTANCE, 
                      PLATFORM_Y - SPAWN_HEIGHT, RED, "Spiller 1")
    spiller2 = Spiller(PLATFORM_X + PLATFORM_WIDTH - SPAWN_DISTANCE, 
                      PLATFORM_Y - SPAWN_HEIGHT, BLUE, "Spiller 2")
    
    platform = pygame.Rect(PLATFORM_X, PLATFORM_Y, 
                         PLATFORM_WIDTH, PLATFORM_HEIGHT)
    
    clock = pygame.time.Clock()
    running = True
    
    # Game state
    state = GameState.BATTLE
    round_num = 1
    round_start_time = time.time()
    
    while running:
        now = time.time()
        time_left = max(0, ROUND_TIME - (now - round_start_time))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == GameState.BATTLE:
                        state = GameState.PAUSE
                    else:
                        state = GameState.BATTLE
                elif event.key == pygame.K_SPACE:
                    # Allow space to work in both ROUND_END and PAUSE states
                    if state in [GameState.ROUND_END, GameState.PAUSE]:
                        # Reset both players
                        spiller1.points = 0
                        spiller2.points = 0
                        spiller1.start_position()
                        spiller2.start_position()
                        state = GameState.BATTLE
                        round_num = 1
                        round_start_time = now
        
        if state == GameState.BATTLE:
            # Update players
            spiller1.move(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
            spiller2.move(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
            
            spiller1_ready = spiller1.update()
            spiller2_ready = spiller2.update()
            
            # Check for falls and points
            if spiller1.has_fallen():
                spiller2.points += 1
                spiller1_ready = True
            elif spiller2.has_fallen():
                spiller1.points += 1
                spiller2_ready = True
            
            # Restart round if a player has fallen
            if spiller1_ready or spiller2_ready:
                spiller1.start_position()
                spiller2.start_position()
                round_num += 1
                round_start_time = now + 1.5
            
            # Handle collisions
            handle_collision(spiller1, spiller2)
            
            # Check for winner
            if spiller1.points >= MAX_POINTS or spiller2.points >= MAX_POINTS:
                state = GameState.ROUND_END
                print("Game ended! Press SPACE to start a new match") # Debug info
        
        # Draw game
        window.fill(WHITE)
        pygame.draw.rect(window, GREEN, platform)
        
        # Draw players and UI
        spiller1.draw(window)
        spiller2.draw(window)
        display_points(window, spiller1, spiller2, time_left)
        
        # Show round start countdown
        if now < round_start_time:
            display_round_start(window, round_num)
        
        # Show winner screen
        if state == GameState.ROUND_END:
            winner = spiller1 if spiller1.points > spiller2.points else spiller2
            display_winner(window, winner)
        elif state == GameState.PAUSE:
            # Show pause screen
            font = pygame.font.Font(None, LARGE_FONT)
            text = font.render("PAUSED", True, BLACK)
            window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
            
            font = pygame.font.Font(None, SMALL_FONT)
            text = font.render("Press SPACE to restart or ESC to resume", True, BLACK)
            window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 50))
        
        pygame.display.update()
        clock.tick(FRAME_RATE)
    
    pygame.quit()

if __name__ == "__main__":
    main() 