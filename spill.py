import pygame
from spiller import Spiller
from merliv import Merliv
from mindreliv import Mindreliv




# 1 oppsett
pygame.init()
BREDDE = 1000
HOYDE = 600
vindu = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("spill")

FPS = 60
klokke = pygame.time.Clock()

YELLOW = (255,255,0)
RED = (120, 29, 22)
WHITE = (255, 255, 255)
GREEN = (15, 145, 91)
BLACK = (0, 0, 0)
DARK = (71, 74, 64)



merliv = Merliv(BREDDE)
mindreliv = Mindreliv(BREDDE)
#definer spill variabler
start_nedtelling = 3
nedtelling_update = pygame.time.get_ticks()
poeng = [0, 0] # poeng til spillere [spiller1, spiller2]
runde_slutt = False

RUNDE_SLUTT_COOLDOWN = 3000


#definer spiller variabler

SVERD_SIZE = 180
SVERD_SCALE = 4
SVERD_OFFSET = [88, 58]
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

# definer fonter
font_nedtelling = pygame.font.SysFont("impact", 80)
font_poeng = pygame.font.SysFont("impact", 20)
font_vinn = pygame.font.SysFont("impact", 60)

# funksjon for tegning av teksten
def tegn_tekst( tekst, font, tekst_farge, x, y):
    img = font.render(tekst, True, tekst_farge)
    vindu.blit(img, (x, y))



#bakgrunn
bg_bilde = pygame.image.load("bilder/bakr.gif").convert_alpha()
def tegn_bg():
    scale_bg = pygame.transform.scale(bg_bilde, (BREDDE, HOYDE))
    vindu.blit(scale_bg, (0,0))

#tegne liv 
def tegn_liv(liv, x, y):
    forhold = liv / 100
    pygame.draw.rect(vindu, YELLOW, (x - 2, y- 2, 404, 34))
    pygame.draw.rect(vindu, RED, (x, y, 400, 30))
    pygame.draw.rect(vindu, GREEN, (x, y, 400 * forhold, 30))

#spillere
spiller_1 = Spiller(1, 200, 310, False, SVERD_DATA, sverd, SVERD_STEG)
spiller_2 = Spiller(2, 700,310, True, ANDRE_DATA, andre, ANDRE_STEG)

while True:

    #tegne bakgrunn
    tegn_bg()

    #vis poeng

    pygame.draw.rect(vindu, DARK, (18, 60, 94, 30))
    pygame.draw.rect(vindu, DARK, (878, 60, 94, 30))
    tegn_tekst("Spiller 1 : " + str(poeng[0]), font_poeng, WHITE, 20, 60)
    tegn_tekst("Spiller 2 : " + str(poeng[1]), font_poeng, WHITE, 880, 60)


    #vis liv
    tegn_liv(spiller_1.liv, 20, 20)
    tegn_liv(spiller_2.liv, 580, 20)

    #oppdatere nedtelling
    if start_nedtelling <= 0: 

        #flytt spillere
        spiller_1.flytt(BREDDE, HOYDE, vindu, spiller_2)
        spiller_2.flytt(BREDDE, HOYDE, vindu, spiller_1)
    else:
        #vis nedtelling
        tegn_tekst(str(start_nedtelling), font_nedtelling, WHITE, 479, 300)
        #oppdater nedtelling
        if (pygame.time.get_ticks() - nedtelling_update) >= 1000:
            start_nedtelling -= 1
            nedtelling_update = pygame.time.get_ticks()
    


    #kollisjon mellom xliv og spillere

    if spiller_1.kollisjon(merliv):
        merliv.fjern()
        spiller_1.liv += 10
        #spillere får +10 liv hvis de kolliderer med merliv

    if spiller_2.kollisjon(merliv):
        merliv.fjern()
        spiller_2.liv += 10

    if spiller_1.kollisjon(mindreliv):
        mindreliv.fjern()
        spiller_1.liv -= 10
        #spillere får -10 liv hvis de kolliderer med mindreliv

    if spiller_2.kollisjon(mindreliv):
        mindreliv.fjern()
        spiller_2.liv -= 10
    
    

    #sjekke hvem som har vunnet
    if runde_slutt == False:
        if spiller_1.ilive == False:
            poeng[1] += 1
            runde_slutt = True
            runde_slutt_tid = pygame.time.get_ticks()
            vinner = "spiller 2"
            print(poeng)
        elif spiller_2.ilive == False:
            poeng[0] += 1
            runde_slutt = True
            vinner = "spiller 1"
            runde_slutt_tid = pygame.time.get_ticks()

            
    else:
    #print vinneren
        tegn_tekst(f"{vinner} har vunnet", font_vinn, WHITE, 270, 300)
        if pygame.time.get_ticks() - runde_slutt_tid > RUNDE_SLUTT_COOLDOWN:
            runde_slutt = False
            start_nedtelling = 3
            spiller_1 = Spiller(1, 200, 310, False, SVERD_DATA, sverd, SVERD_STEG) # gir fulle liv
            spiller_2 = Spiller(2, 700,310, True, ANDRE_DATA, andre, ANDRE_STEG)




            

            

    #oppdatere spillere
    spiller_1.update()
    spiller_2.update()



    mindreliv.fall(HOYDE)
    merliv.vis(BREDDE)



    # tegne spiller
    spiller_1.tegn(vindu)
    spiller_2.tegn(vindu)


    merliv.tegn(vindu)
    mindreliv.tegn(vindu)
    # 2. håndterer spillet
    for hendelse in pygame.event.get():
        if hendelse.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    # 3. oppdater spill
    pygame.display.update()
    # 4. tegn
    
    klokke.tick(FPS)