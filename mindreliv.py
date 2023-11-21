import random
import pygame
from figur import Figur



class Mindreliv(Figur):
    def __init__(self, vindu_bredde: int):
        super().__init__("bilder/mindre.webp", 0.3)

        self.ventetid = 6000
        self.siste_fall_tid = pygame.time.get_ticks()
        self.ny_plassering(vindu_bredde)
    
    def ny_plassering(self, vindu_bredde: int):
        self.ramme.centerx = random.randint(0, vindu_bredde)
        self.ramme.top = 0
        self.siste_fall_tid = pygame.time.get_ticks()

    def fall(self, vindu_høyde: int):
        tid = pygame.time.get_ticks()

        # Sjekk om nok tid har gått siden forrige fall
        if tid - self.siste_fall_tid > self.ventetid:
            if self.ramme.top > vindu_høyde:
                self.ny_plassering(vindu_høyde)
            self.ramme.y += 1
