import random
import pygame
from figur import Figur

class Merliv(Figur):
    def __init__(self, vindu_bredde: int):
        super().__init__("bilder/mer.webp", 0.3)
        self.ventetid_stå_stille = 5000
        self.ventetid_dukke_opp = 1000
        self.siste_tid = pygame.time.get_ticks()
        self.ny_plassering(vindu_bredde)
    
    def ny_plassering(self, vindu_bredde: int):
        self.rect.centerx = random.randint(0, vindu_bredde)
        self.rect.centery = 200 
        self.siste_tid = pygame.time.get_ticks()

    def vis(self, vindu_bredde: int):
        tid = pygame.time.get_ticks()

        if tid - self.siste_tid > self.ventetid_stå_stille + self.ventetid_dukke_opp:
            self.ny_plassering(vindu_bredde)
            self.siste_tid = tid