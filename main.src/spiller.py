import pygame
from config import *
import random

class Spiller:
    def __init__(self, x, y, color, name):
        # Basic player properties
        self.body = pygame.Rect(x, y, PLAYER_SIZE*2, PLAYER_SIZE*2)
        self.color = color
        self.name = name
        
        # Movement variables
        self.speed_x = 0
        self.speed_y = 0
        self.facing_right = True
        self.on_ground = False
        self.air_dash = MAX_AIR_DASH
        
        # Combat stats
        self.damage = 0
        self.points = 0
        self.combo = 0
        self.last_hit_time = 0
        
        # Status effects
        self.stunned = False
        self.stun_time = 0
        self.is_dead = False
        self.death_timer = 0
        self.recovery_frames = 0
        self.invincible = False
        self.invincible_timer = 0
        
        # Dash mechanics
        self.can_dash = True
        self.dash_timer = 0
        self.is_dashing = False
        self.dash_direction = 1
        self.is_attacking = False
        
        # Combo system
        self.combo_timer = 0
        self.combo_count = 0
        self.last_attacker = None
        
        # Particle system
        self.particles = []
    
    def move(self, left, right, jump, dash):
        if self.is_dead:
            return
            
        if self.stunned:
            self.stun_time -= 1
            if self.stun_time <= 0:
                self.stunned = False
            return
            
        keys = pygame.key.get_pressed()
        
        # Normal movement
        if not self.is_dashing:
            if keys[left]:
                self.speed_x = -MOVEMENT_SPEED
                self.facing_right = False
                self.dash_direction = -1
            if keys[right]:
                self.speed_x = MOVEMENT_SPEED
                self.facing_right = True
                self.dash_direction = 1
                
            # Jump mechanics
            if keys[jump]:
                if self.on_ground:
                    self.speed_y = JUMP_FORCE
                    self.on_ground = False
                    self.add_jump_effect()
        
        # Update dash cooldown
        if not self.can_dash:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.can_dash = True
                self.dash_timer = 0
        
        # Dash system
        if keys[dash] and self.can_dash and not self.is_dashing:
            if self.on_ground or self.air_dash > 0:
                self.start_dash()
                if not self.on_ground:
                    self.air_dash -= 1
        
        # Dash movement
        if self.is_dashing:
            self.speed_x = DASH_FORCE * self.dash_direction
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.stop_dash()
        
        # Air control
        if not self.on_ground:
            self.speed_x *= AIR_RESISTANCE
    
    def start_dash(self):
        """Start a new dash"""
        self.is_dashing = True
        self.dash_timer = DASH_LENGTH
        self.can_dash = False
        self.is_attacking = True
    
    def stop_dash(self):
        """Stop the current dash"""
        self.is_dashing = False
        self.is_attacking = False
        # Start cooldown timer when dash stops
        self.dash_timer = DASH_COOLDOWN
        self.can_dash = False
    
    def update(self):
        if self.is_dead:
            self.speed_y += GRAVITY * 0.5
            self.body.y += self.speed_y
            if self.body.top > HEIGHT + 100:
                self.death_timer += 1
                if self.death_timer > 60:
                    return True
            return False
        
        # Physics update
        self.speed_y += GRAVITY
        self.body.x += self.speed_x
        self.body.y += self.speed_y
        
        if self.on_ground:
            self.speed_x *= FRICTION
        
        # Screen boundaries
        if self.body.left < 0:
            self.body.left = 0
            self.speed_x = 0
        if self.body.right > WIDTH:
            self.body.right = WIDTH
            self.speed_x = 0
        
        # Platform collision
        self.on_ground = False
        if (self.body.bottom >= PLATFORM_Y and 
            self.body.left < PLATFORM_X + PLATFORM_WIDTH and 
            self.body.right > PLATFORM_X and 
            self.speed_y >= 0):
            self.body.bottom = PLATFORM_Y
            self.speed_y = 0
            self.on_ground = True
            self.air_dash = MAX_AIR_DASH
        
        # Update timers
        if self.recovery_frames > 0:
            self.recovery_frames -= 1
        
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Update combo system
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0
        
        # Update particles
        self.update_particles()
        
        return False
    
    def apply_knockback(self, direction, force):
        if self.invincible:
            return
            
        # Calculate knockback with damage scaling
        knockback_bonus = 1 + (self.damage / 75)  # Faster scaling
        total_force = min(force * knockback_bonus, MAX_KNOCKBACK)
        
        # Apply knockback with focus on horizontal movement
        self.speed_x = direction[0] * total_force * 2.0
        self.speed_y = direction[1] * total_force - 3
        
        # Stun based on damage
        self.stunned = True
        self.stun_time = int(8 * knockback_bonus)
        
        # Give recovery frames
        self.recovery_frames = RECOVERY_FRAMES
        
        # Add hit effect
        self.add_hit_effect()
    
    def add_hit_effect(self):
        # Add particles on hit
        for _ in range(5):
            self.particles.append({
                'pos': [self.body.centerx, self.body.centery],
                'vel': [random.uniform(-5, 5), random.uniform(-5, 5)],
                'timer': 10,
                'color': self.color
            })
    
    def add_jump_effect(self):
        # Add jump effect
        for _ in range(3):
            self.particles.append({
                'pos': [self.body.centerx, self.body.bottom],
                'vel': [random.uniform(-2, 2), random.uniform(0, 2)],
                'timer': 5,
                'color': GRAY
            })
    
    def update_particles(self):
        # Update all particles
        for particle in self.particles[:]:
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['timer'] -= 1
            if particle['timer'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, window):
        # Draw particles
        for particle in self.particles:
            alpha = int(255 * (particle['timer'] / 10))
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(window, color, 
                             [int(particle['pos'][0]), int(particle['pos'][1])], 3)
        
        # Draw player
        pygame.draw.ellipse(window, self.color, self.body)
        
        # Draw direction indicator
        direction_x = self.body.centerx + (10 if self.facing_right else -10)
        pygame.draw.circle(window, BLACK, (direction_x, self.body.centery), 5)
        
        # Draw damage and combo
        damage_text = f"{int(self.damage)}%"
        if self.combo_count > 1:
            damage_text += f" [{self.combo_count}x]"
        
        text = pygame.font.Font(None, MEDIUM_FONT).render(damage_text, True, BLACK)
        window.blit(text, (self.body.centerx - text.get_width()//2, 
                          self.body.top - 30))
    
    def get_center(self):
        return [self.body.centerx, self.body.centery]
    
    def has_fallen(self):
        return self.body.top > HEIGHT + 50
    
    def start_position(self):
        self.is_dead = False
        self.death_timer = 0
        self.damage = 0
        self.combo_count = 0
        self.combo_timer = 0
        self.last_attacker = None
        self.speed_x = 0
        self.speed_y = 0
        self.stunned = False
        self.stun_time = 0
        self.is_dashing = False
        self.can_dash = True
        self.dash_timer = 0
        self.air_dash = MAX_AIR_DASH
        self.particles = [] 