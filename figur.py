import pygame


class Figur():
    def __init__(self, bildesti: str, scalenr: float):
        self.og_bilde = pygame.image.load(bildesti).convert_alpha()
        self.scale_bilde = pygame.transform.scale(self.og_bilde, (int(self.og_bilde.get_width() * scalenr), int(self.og_bilde.get_height() * scalenr)))
        self.ramme = self.scale_bilde.get_rect()
    
    def tegn(self, vindu: pygame.Surface):
        vindu.blit(self.scale_bilde, self.ramme)