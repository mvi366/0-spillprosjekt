import pygame

class Spiller():
    def __init__(self, spiller, x, y, flip, data, sheet, animasjon_steg ) -> None:
        self.spiller = spiller
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animasjon_liste = self.load_images(sheet, animasjon_steg)
        self.action = 0 #0.: idle 1: løp, 2: hopp, 3: angrep1, 4: angrep2, 5: truffet, 6:dø
        self.frame_index = 0
        self.image = self.animasjon_liste[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180)) 
        self.vel_y = 0
        self.running = False
        self.hopp = False 
        self.angrip = False
        self.angreptype = 0
        self.angrep_cooldown = 0
        self.skade = False
        self.liv = 100
        self.ilive = True


    def load_images(self, sheet, animasjon_steg):
        y = 0
        animasjon_liste = []
        for animasjon in animasjon_steg:
            temp_img_list =[]
            for x in range(animasjon):
                temp_img = sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img,(self.size *self.image_scale, self.size * self.image_scale)))
            y += 1
            animasjon_liste.append(temp_img_list)
        return animasjon_liste

    
    def flytt(self, bredde, hoyde, surface, fiende):
        FART = 10
        TYNGDE = 2
        dx = 0
        dy = 0
        self.running = False
        self.angreptype = 0
        #taster
        key = pygame.key.get_pressed()
        
        #spiller kan ikke gjøre andre ting imens den angriper
        if self.angrip == False and self.ilive == True: #kan ikke bevege seg når spiller er død
            #sjekk spiller 1 kontroller
            if self.spiller == 1:
                #flytting
                if key[pygame.K_a]:
                    dx = -FART
                    self.running = True
                if key[pygame.K_d]:
                    dx = FART
                    self.running = True

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

            #sjekk spiller 2 kontroller
            if self.spiller == 2:
                #flytting
                if key[pygame.K_LEFT]:
                    dx = -FART
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = FART
                    self.running = True

                #hopp
                if key[pygame.K_UP] and self.hopp == False:
                    self.vel_y = -30
                    self.hopp = True

                #angrep
                if key[pygame.K_l] or key[pygame.K_k]:
                    self.angrep(surface, fiende)

                    #hvilken angepstype
                    if key[pygame.K_l]:
                        self.angreptype = 1
                    if key[pygame.K_k]:
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


        #sett på cooldown etter angrep
        if self.angrep_cooldown > 0:
            self.angrep_cooldown -= 1


        #oppdatere posisjon
        self.rect.x += dx
        self.rect.y += dy
    
    def update(self):
        #sjekke hvilken animasjon
        if self.liv <= 0:
            self.liv = 0
            self.ilive = False
            self.update_action(6)
        elif self.skade == True:
            self.update_action(5)
        elif self.angrip == True:
            if self.angreptype == 1:
                self.update_action(3)
            elif self.angreptype == 2:
                self.update_action(4)


        elif self.hopp == True:
            self.update_action(2)

        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)
        animasjon_cooldown = 80
        #oppdatere bilde
        self.image = self.animasjon_liste[self.action][self.frame_index]
        #sjekke om nok tid har gått
        if pygame.time.get_ticks() - self.update_time > animasjon_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #sjekke om animasjonen er ferdig
        if self.frame_index >= len(self.animasjon_liste[self.action]):
            #hvis spilleren er død, avslutt animasjonen
            if self.ilive == False:
                self.frame_index = len(self.animasjon_liste[self.action]) - 1 # blir på det siste bilde i listen til animasjonen
            else:

                self.frame_index = 0
                #sjekke om angrep har skjedd
                if self.action == 3 or self.action == 4:
                    self.angrip = False
                    self.angrep_cooldown = 25
                #sjekke om det ble skade
                if self.action ==5:
                    self.skade = False
                    #hvis spilleren var i midten av et angrep, vil angrepet bli stoppet
                    self.angrip = False
                    self.angrep_cooldown = 20




    def angrep(self, surface, fiende):
        if self.angrep_cooldown == 0:
            self.angrip = True
            angrip_rect = pygame.Rect(self.rect.centerx - ( 2* self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if angrip_rect.colliderect(fiende.rect):
                fiende.liv -= 10
                fiende.skade = True



    def update_action(self, ny_action):
        #sjekke om den nye handlingen er annerledes
        if ny_action != self.action:
            self.action = ny_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def tegn(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def kollisjon(self, xliv):
        return self.rect.colliderect(xliv.rect)
        
