import pygame
from config import *

class Spiller:
    def __init__(self, x, y, farve, navn):
        # Grundlæggende spiller egenskaber
        self.krop = pygame.Rect(x, y, 50, 50)  # Spillerens hitbox
        self.farve = farve                     # Spillerens farve (rød eller blå)
        self.navn = navn                       # Spillerens navn
        
        # Bevægelse variabler
        self.fart_x = 0                        # Vandret hastighed
        self.fart_y = 0                        # Lodret hastighed
        
        # Kamp statistikker
        self.skade = 0                         # Nuværende skade procent
        self.point = 0                         # Antal point/sejre

        # Status flags
        self.lammet = False                    # Om spilleren er lammet efter et hit
        self.lammelse_tid = 0                  # Hvor længe spilleren er lammet
        self.er_død = False                    # Om spilleren er faldet ned
        self.død_timer = 0                     # Timer for genoplivning
        
        # Dash mekanik
        self.kan_dashe = True                  # Om spilleren kan bruge dash
        self.dash_timer = 0                    # Timer for dash cooldown
        self.dasher = False                    # Om spilleren er i gang med et dash
        self.dash_retning = 1                  # Hvilken retning dashet går (1 eller -1)
        self.angriber = False                  # Om spilleren er den aktive angriber
    
    def bevæg(self, venstre, højre, hop, dash):
        # Hvis spilleren er død, gør ingenting
        if self.er_død:
            return
        
        # Hvis spilleren er lammet, opdater lammelse timer
        if self.lammet:
            self.lammelse_tid -= 1
            if self.lammelse_tid <= 0:
                self.lammet = False
            return
        
        # Læs tastatur input
        taster = pygame.key.get_pressed()
        
        # Normal bevægelse (kun hvis vi ikke dasher)
        if not self.dasher:
            if taster[venstre]:
                self.fart_x = -BEVÆGELSE_FART
                self.dash_retning = -1         # Gem retning til næste dash
            if taster[højre]:
                self.fart_x = BEVÆGELSE_FART
                self.dash_retning = 1          # Gem retning til næste dash
            if taster[hop] and self.krop.bottom >= PLATFORM_Y:
                self.fart_y = HOPPE_KRAFT
        
        # Håndter dash input og cooldown
        if taster[dash] and self.kan_dashe and not self.dasher:
            self.start_dash()
        
        if not self.kan_dashe:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.kan_dashe = True
        
        # Opdater dash bevægelse
        if self.dasher:
            self.fart_x = DASH_KRAFT * self.dash_retning
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.stop_dash()
    
    def start_dash(self):
        """Start et nyt dash"""
        self.dasher = True
        self.dash_timer = DASH_LÆNGDE
        self.kan_dashe = False
        self.angriber = True
    
    def stop_dash(self):
        """Stop det nuværende dash"""
        self.dasher = False
        self.dash_timer = DASH_VENTETID
        self.angriber = False
    
    def opdater(self):
        # Håndter død spiller
        if self.er_død:
            self.fart_y += TYNGDEKRAFT * 0.5   # Langsom fald animation
            self.krop.y += self.fart_y
            if self.krop.top > HØJDE + 100:    # Når spilleren er faldet ud af skærmen
                self.død_timer += 1
                if self.død_timer > 60:         # Vent 1 sekund
                    return True                 # Klar til genstart
            return False
        
        # Normal fysik opdatering
        self.fart_y += TYNGDEKRAFT             # Anvend tyngdekraft
        self.krop.x += self.fart_x             # Opdater x position
        self.krop.y += self.fart_y             # Opdater y position
        self.fart_x *= BREMSE                  # Anvend friktion
        
        # Hold spilleren inden for skærmen
        if self.krop.left < 0:
            self.krop.left = 0
            self.fart_x = 0
        if self.krop.right > BREDDE:
            self.krop.right = BREDDE
            self.fart_x = 0
        
        # Platform kollision
        if (self.krop.bottom >= PLATFORM_Y and 
            self.krop.left < PLATFORM_X + PLATFORM_BREDDE and 
            self.krop.right > PLATFORM_X):
            self.krop.bottom = PLATFORM_Y
            self.fart_y = 0
        
        return False
    
    def bliv_skubbet(self, retning, kraft):
        """Anvendt når spilleren bliver ramt"""
        # Beregn knockback baseret på skade
        skub_bonus = 1 + (self.skade / 100)
        samlet_kraft = min(kraft * skub_bonus, MAX_SKUB)
        
        # Anvend knockback med mere vandret kraft
        self.fart_x = retning[0] * samlet_kraft * 1.5  # Øget vandret kraft
        self.fart_y = retning[1] * samlet_kraft - 2    # Reduceret lodret kraft
        
        # Lam spilleren kortvarigt
        self.lammet = True
        self.lammelse_tid = int(10 * skub_bonus)  # Lammelse skalerer med skade
    
    def er_faldet_ned(self):
        """Tjek om spilleren er faldet af platformen"""
        if not self.er_død and (
            self.krop.bottom > HØJDE or 
            (self.krop.bottom > PLATFORM_Y and 
             (self.krop.right < PLATFORM_X or 
              self.krop.left > PLATFORM_X + PLATFORM_BREDDE))):
            self.er_død = True
            return True
        return False
    
    def start_position(self):
        """Nulstil spilleren til start position"""
        # Sæt position baseret på spiller nummer
        if self.navn == "Spiller 1":
            self.krop.x, self.krop.y = 200, 400
        else:
            self.krop.x, self.krop.y = 550, 400
        
        # Nulstil alle værdier
        self.fart_x = 0
        self.fart_y = 0
        self.skade = 0
        self.lammet = False
        self.lammelse_tid = 0
        self.er_død = False
        self.død_timer = 0
        self.kan_dashe = True
        self.dash_timer = 0
        self.dasher = False
        self.angriber = False
    
    def tegn(self, vindue):
        """Tegn spilleren og UI elementer"""
        # Tegn spilleren
        pygame.draw.ellipse(vindue, self.farve, self.krop)
        
        # Tegn skade procent
        skade_tekst = pygame.font.Font(None, 36).render(
            f"{int(self.skade)}%", True, SORT)
        vindue.blit(skade_tekst, 
                   (self.krop.centerx - 20, self.krop.top - 25))
        
        # Tegn dash cooldown bar
        if not self.kan_dashe:
            cooldown = self.dash_timer / DASH_VENTETID
            pygame.draw.rect(vindue, SORT, 
                           (self.krop.centerx - 15, 
                            self.krop.bottom + 5, 
                            30 * cooldown, 5))
    
    def få_centrum(self):
        """Returner spillerens centrum koordinater"""
        return self.krop.center 