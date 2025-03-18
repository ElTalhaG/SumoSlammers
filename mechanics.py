# BETA VERSION
# import pygame
# import math

# # Start pygame
# pygame.init()

# # Vindue størrelse
# BREDDE = 800
# HØJDE = 600
# vindue = pygame.display.set_mode((BREDDE, HØJDE))
# pygame.display.set_caption("Sumo Kamp!")

# # Mine farver
# HVID = (255, 255, 255)
# RØD = (255, 0, 0)
# BLÅ = (0, 0, 255)
# GRØN = (0, 255, 0)
# SORT = (0, 0, 0)

# # Spil indstillinger
# TYNGDEKRAFT = 0.5
# HOPPE_KRAFT = -10
# BEVÆGELSE_FART = 5
# GRUND_SKUB = 5
# MAX_SKUB = 25
# BREMSE = 0.85
# SPILLER_STØRRELSE = 25
# SKADE_MÆNGDE = 5
# MAX_SKADE = 300

# # Tekst
# pygame.font.init()
# FONT = pygame.font.Font(None, 36)

# class Spiller:
#     def __init__(self, x, y, farve, navn):
#         self.krop = pygame.Rect(x, y, 50, 50)
#         self.farve = farve
#         self.fart_x = 0
#         self.fart_y = 0
#         self.skade = 0
#         self.point = 0
#         self.navn = navn
#         self.lammet = False
#         self.lammelse_tid = 0
    
#     def bevæg(self, venstre, højre, hop):
#         # Hvis spilleren er lammet, vent til det er ovre
#         if self.lammet:
#             self.lammelse_tid -= 1
#             if self.lammelse_tid <= 0:
#                 self.lammet = False
#             return

#         taster = pygame.key.get_pressed()
#         if taster[venstre]:
#             self.fart_x = -BEVÆGELSE_FART
#         if taster[højre]:
#             self.fart_x = BEVÆGELSE_FART
#         if taster[hop] and self.krop.bottom >= platform.top:
#             self.fart_y = HOPPE_KRAFT
    
#     def opdater(self):
#         # Fysik
#         self.fart_y += TYNGDEKRAFT
#         self.krop.x += self.fart_x
#         self.krop.y += self.fart_y
#         self.fart_x *= BREMSE

#         # Hold spilleren inden for skærmen
#         if self.krop.left < 0:
#             self.krop.left = 0
#             self.fart_x = 0
#         if self.krop.right > BREDDE:
#             self.krop.right = BREDDE
#             self.fart_x = 0

#         # Platform kollision
#         if self.krop.bottom >= platform.top and self.krop.left < platform.right and self.krop.right > platform.left:
#             self.krop.bottom = platform.top
#             self.fart_y = 0
    
#     def bliv_skubbet(self, retning, kraft):
#         # Jo mere skade, jo længere væk bliver man skubbet
#         skub_bonus = 1 + (self.skade / 100)
#         samlet_kraft = min(kraft * skub_bonus, MAX_SKUB)
        
#         self.fart_x = retning[0] * samlet_kraft
#         self.fart_y = retning[1] * samlet_kraft - 5
        
#         # Spilleren er lammet et øjeblik
#         self.lammet = True
#         self.lammelse_tid = int(10 * skub_bonus)
    
#     def er_faldet_ned(self):
#         return (self.krop.bottom > HØJDE or 
#                 (self.krop.bottom > platform.top and 
#                  (self.krop.right < platform.left or self.krop.left > platform.right)))
    
#     def start_position(self):
#         if self.navn == "Spiller 1":
#             self.krop.x, self.krop.y = 200, 400
#         else:
#             self.krop.x, self.krop.y = 550, 400
#         self.fart_x = 0
#         self.fart_y = 0
#         self.skade = 0
#         self.lammet = False
#         self.lammelse_tid = 0
    
#     def tegn(self, vindue):
#         pygame.draw.ellipse(vindue, self.farve, self.krop)
#         skade_tekst = FONT.render(f"{int(self.skade)}%", True, SORT)
#         vindue.blit(skade_tekst, (self.krop.centerx - 20, self.krop.top - 25))
    
#     def få_centrum(self):
#         return self.krop.center

# def vis_point(vindue, spiller1, spiller2):
#     point_tekst = FONT.render(f"{spiller1.navn}: {spiller1.point}  {spiller2.navn}: {spiller2.point}", True, SORT)
#     vindue.blit(point_tekst, (10, 10))

# def nyt_spil(spiller1, spiller2):
#     spiller1.start_position()
#     spiller2.start_position()

# # Lav spillerne
# spiller1 = Spiller(200, 400, RØD, "Spiller 1")
# spiller2 = Spiller(550, 400, BLÅ, "Spiller 2")

# # Lav platformen
# platform = pygame.Rect(100, 500, 600, 20)

# ur = pygame.time.Clock()
# kør = True

# while kør:
#     vindue.fill(HVID)
#     pygame.draw.rect(vindue, GRØN, platform)
#     spiller1.tegn(vindue)
#     spiller2.tegn(vindue)
#     vis_point(vindue, spiller1, spiller2)
    
#     # Styr spillerne
#     spiller1.bevæg(pygame.K_a, pygame.K_d, pygame.K_w)
#     spiller2.bevæg(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
    
#     spiller1.opdater()
#     spiller2.opdater()
    
#     # Se om nogen er faldet ned
#     if spiller1.er_faldet_ned():
#         spiller2.point += 1
#         nyt_spil(spiller1, spiller2)
#     elif spiller2.er_faldet_ned():
#         spiller1.point += 1
#         nyt_spil(spiller1, spiller2)
    
#     # Tjek for sammenstød
#     centrum1 = spiller1.få_centrum()
#     centrum2 = spiller2.få_centrum()
#     afstand = math.dist(centrum1, centrum2)

#     if afstand < SPILLER_STØRRELSE * 2:
#         # Find retningen mellem spillerne
#         retning = (centrum1[0] - centrum2[0], centrum1[1] - centrum2[1])
#         længde = math.sqrt(retning[0]**2 + retning[1]**2)
#         retning = (retning[0] / længde, retning[1] / længde)
        
#         # Skub spillerne væk fra hinanden
#         overlap = SPILLER_STØRRELSE * 2 - afstand
#         spiller1.krop.x += retning[0] * overlap / 2
#         spiller1.krop.y += retning[1] * overlap / 2
#         spiller2.krop.x -= retning[0] * overlap / 2
#         spiller2.krop.y -= retning[1] * overlap / 2

#         # Giv skade og skub spillerne
#         spiller1.skade = min(spiller1.skade + SKADE_MÆNGDE, MAX_SKADE)
#         spiller2.skade = min(spiller2.skade + SKADE_MÆNGDE, MAX_SKADE)
        
#         # Beregn hvor hårdt de ramte hinanden
#         sammenstøds_fart = (spiller1.fart_x - spiller2.fart_x, spiller1.fart_y - spiller2.fart_y)
#         kraft = math.sqrt(sammenstøds_fart[0]**2 + sammenstøds_fart[1]**2)
#         skub_kraft = max(GRUND_SKUB, min(kraft * 0.5, MAX_SKUB))
        
#         spiller1.bliv_skubbet(retning, skub_kraft)
#         spiller2.bliv_skubbet((-retning[0], -retning[1]), skub_kraft)
    
#     pygame.display.update()
#     ur.tick(60)
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             kør = False

# pygame.quit()
