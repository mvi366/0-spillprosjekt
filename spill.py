import pygame
from spiller import Spiller




# 1 oppsett
pygame.init()
BREDDE = 1000
HOYDE = 600
vindu = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("spill")

FPS = 60
klokke = pygame.time.Clock()

YELLOW = (255,255,0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (46, 139, 87)


#definer variabler

SVERD_SIZE = 180
SVERD_SCALE = 4
SVERD_OFFSET = [80, 58]
SVERD_DATA = [SVERD_SIZE, SVERD_SCALE, SVERD_OFFSET]
ANDRE_SIZE = 200
ANDRE_SCALE = 4.5
ANDRE_OFFSET = [87, 75]
ANDRE_DATA = [ANDRE_SIZE, ANDRE_SCALE, ANDRE_OFFSET]



#spritesheets
sverd = pygame.image.load("bilder/sverd/sverdsheet.png").convert_alpha()
andre = pygame.image.load("bilder/sverd/sverd2.png").convert_alpha()
#antall steg i animasjon

SVERD_STEG = [9, 8, 6, 7, 7, 4, 11]
ANDRE_STEG = [4, 8, 4, 4, 4, 3, 7]


#bakgrunn
bg_bilde = pygame.image.load("bilder/bakr.gif").convert_alpha()
def tegn_bg():
    scale_bg = pygame.transform.scale(bg_bilde, (BREDDE, HOYDE))
    vindu.blit(scale_bg, (0,0))

#tegne liv 
def tegn_liv(liv, x, y):
    forhold = liv / 100
    pygame.draw.rect(vindu, WHITE, (x - 2, y- 2, 405, 35))
    pygame.draw.rect(vindu, RED, (x, y, 400, 30))
    pygame.draw.rect(vindu, GREEN, (x, y, 400 * forhold, 30))

#spillere
spiller_1 = Spiller(1, 200, 310, False, SVERD_DATA, sverd, SVERD_STEG)
spiller_2 = Spiller(2, 700,310, True, ANDRE_DATA, andre, ANDRE_STEG)

while True:
    #tegne bakgrunn
    tegn_bg()

    #vis liv
    tegn_liv(spiller_1.liv, 20, 20)
    tegn_liv(spiller_2.liv, 580, 20)

    #flytt spilelr
    spiller_1.flytt(BREDDE, HOYDE, vindu, spiller_2)
    spiller_2.flytt(BREDDE, HOYDE, vindu, spiller_1)

    #oppdatere spillere
    spiller_1.update()
    spiller_2.update()


    # tegne spiller
    spiller_1.tegn(vindu)
    spiller_2.tegn(vindu)
    # 2. håndterer spillet
    for hendelse in pygame.event.get():
        if hendelse.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    # 3. oppdater spill
    pygame.display.update()
    # 4. tegn
    
    klokke.tick(FPS)