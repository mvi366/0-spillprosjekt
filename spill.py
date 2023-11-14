import pygame

# 1 oppsett
pygame.init()
BREDDE = 600
HOYDE = 600
vindu = pygame.display.set_mode((BREDDE, HOYDE))
FPS = 60
klokke = pygame.time.Clock()

while True:
    # 2. håndterer spillet
    for hendelse in pygame.event.get():
        if hendelse.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    # 3. oppdater spikk
    # 4. tegn
    pygame.display.flip()
    klokke.tick(FPS)