import pygame
import math
from config import *
from spiller import Spiller

def vis_point(vindue, spiller1, spiller2):
    """Vis spillernes point på skærmen"""
    point_tekst = pygame.font.Font(None, 36).render(
        f"{spiller1.navn}: {spiller1.point}  {spiller2.navn}: {spiller2.point}", 
        True, SORT)
    vindue.blit(point_tekst, (10, 10))

def håndter_kollision(spiller1, spiller2):
    """Håndter kollision mellem to spillere"""
    # Find afstanden mellem spillerne
    centrum1 = spiller1.få_centrum()
    centrum2 = spiller2.få_centrum()
    afstand = math.dist(centrum1, centrum2)
    
    # Hvis spillerne rører hinanden
    if afstand < SPILLER_STØRRELSE * 2 and not (spiller1.er_død or spiller2.er_død):
        # Find ud af hvem der er angriberen baseret på bevægelse
        spiller1_bevæger = abs(spiller1.fart_x) > 1
        spiller2_bevæger = abs(spiller2.fart_x) > 1
        
        # Hvis kun én spiller bevæger sig, er de angriberen
        if spiller1_bevæger and not spiller2_bevæger:
            # Spiller 1 er angriberen
            retning = 1 if spiller1.fart_x > 0 else -1
            kraft = GRUND_SKUB * (2 if spiller1.dasher else 1)
            spiller2.skade = min(spiller2.skade + SKADE_MÆNGDE, MAX_SKADE)
            spiller2.bliv_skubbet((retning, -0.5), kraft)
            
        elif spiller2_bevæger and not spiller1_bevæger:
            # Spiller 2 er angriberen
            retning = 1 if spiller2.fart_x > 0 else -1
            kraft = GRUND_SKUB * (2 if spiller2.dasher else 1)
            spiller1.skade = min(spiller1.skade + SKADE_MÆNGDE, MAX_SKADE)
            spiller1.bliv_skubbet((retning, -0.5), kraft)
            
        # Skub spillerne fra hinanden for at undgå overlap
        overlap = SPILLER_STØRRELSE * 2 - afstand
        if centrum1[0] < centrum2[0]:
            spiller1.krop.x -= overlap / 2
            spiller2.krop.x += overlap / 2
        else:
            spiller1.krop.x += overlap / 2
            spiller2.krop.x -= overlap / 2

def main():
    """Hovedspilsløjfe"""
    # Initialiser pygame
    pygame.init()
    pygame.font.init()
    
    # Opret vindue
    vindue = pygame.display.set_mode((BREDDE, HØJDE))
    pygame.display.set_caption("Sumo Kamp!")
    
    # Opret spillere
    spiller1 = Spiller(200, 400, RØD, "Spiller 1")
    spiller2 = Spiller(550, 400, BLÅ, "Spiller 2")
    
    # Opret platform
    platform = pygame.Rect(PLATFORM_X, PLATFORM_Y, 
                         PLATFORM_BREDDE, PLATFORM_HØJDE)
    
    # Spilvariabler
    ur = pygame.time.Clock()
    kør = True
    
    # Hovedløkke
    while kør:
        # Håndter input og vindues-events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kør = False
        
        # Opdater spillere
        spiller1.bevæg(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_LSHIFT)
        spiller2.bevæg(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RSHIFT)
        
        spiller1_klar = spiller1.opdater()
        spiller2_klar = spiller2.opdater()
        
        # Tjek for fald og point
        if spiller1.er_faldet_ned():
            spiller2.point += 1
        elif spiller2.er_faldet_ned():
            spiller1.point += 1
        
        # Genstart runde hvis en spiller er faldet helt ned
        if spiller1_klar or spiller2_klar:
            spiller1.start_position()
            spiller2.start_position()
        
        # Håndter kollisioner
        håndter_kollision(spiller1, spiller2)
        
        # Tegn spillet
        vindue.fill(HVID)
        pygame.draw.rect(vindue, GRØN, platform)
        spiller1.tegn(vindue)
        spiller2.tegn(vindue)
        vis_point(vindue, spiller1, spiller2)
        
        # Opdater skærmen
        pygame.display.update()
        ur.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 