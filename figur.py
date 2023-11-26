import pygame


class Figur():
    def __init__(self, bildesti: str, scalenr: float):
        self.og_bilde = pygame.image.load(bildesti).convert_alpha()
        self.scale_bilde = pygame.transform.scale(self.og_bilde, (int(self.og_bilde.get_width() * scalenr), int(self.og_bilde.get_height() * scalenr)))
        self.rect = self.scale_bilde.get_rect()
        self.kollider = False
    
    def tegn(self, vindu: pygame.Surface):
        vindu.blit(self.scale_bilde, self.rect)

    def fjern(self):
        self.rect.topleft = (-100, -100) 