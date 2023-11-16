import pygame

class Spiller():
    def __init__(self, x, y, flip, data, sheet, animasjon_steg ) -> None:
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animasjon_list = self.load_images(sheet, animasjon_steg)
        self.action = 0 #0.: idle 1: løp, 2: hopp, 3: angrep1, 4: angrep2, 5: truffet, 6:dø
        self.frame_index = 0
        self.image = self.animasjon_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.hopp = False 
        self.angrip = False
        self.angreptype = 0
        self.liv = 100


    def load_images(self, sheet, animasjon_steg):
        y = 0
        animasjon_list = []
        for animasjon in animasjon_steg:
            temp_img_list =[]
            for x in range(animasjon):
                temp_img = sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img,(self.size *self.image_scale, self.size * self.image_scale)))
            y += 1
            animasjon_list.append(temp_img_list)
        return animasjon_list

    
    def flytt(self, bredde, hoyde, surface, fiende):
        FART = 10
        TYNGDE = 2
        dx = 0
        dy = 0
        #taster
        key = pygame.key.get_pressed()
        
        #spiller kan ikke gjøre andre ting imens den angriper
        if self.angrip == False:

            #flytting
            if key[pygame.K_a]:
                dx = -FART
            if key[pygame.K_d]:
                dx = FART

            #hopp
            if key[pygame.K_w] and self.hopp == False:
                self.vel_y = -30
                self.hopp = True

            #angrep
            if key[pygame.K_r] or key[pygame.K_t]:
                self.angrep(surface, fiende)

                #hvilken angepstype
                if key[pygame.K_r]:
                    self.angreptype = 1
                if key[pygame.K_t]:
                    self.angreptype = 2
            
        
        #tyngdekraft
        self.vel_y += TYNGDE
        dy += self.vel_y

        #spiller i vindu
        if self.rect.left + dx <0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > bredde:
            dx = bredde - self.rect.right
        if self.rect.bottom + dy > hoyde - 110:
            self.vel_y = 0
            self.hopp = False
            dy = hoyde - 110 - self.rect.bottom


        #pass på at spiller er vendt mot hverandre
        if fiende.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True


        #oppdatere posisjon
        self.rect.x += dx
        self.rect.y += dy

    def angrep(self, surface, fiende):
        self.angrip = True
        angrip_rect = pygame.Rect(self.rect.centerx - ( 2* self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if angrip_rect.colliderect(fiende.rect):
            fiende.liv -= 10

        pygame.draw.rect(surface, (0, 255, 0), angrip_rect)




    def tegn(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))