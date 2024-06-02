import pygame

#creaton de classe (joueur)
class Bird(pygame.sprite.Sprite):
    
    gravity = 0.25

    def __init__(self):
        super().__init__()
        self.alive = True
        self.frame =[pygame.transform.scale2x(pygame.image.load('assets/Sprites/redbird-downflap.png').convert()), pygame.transform.scale2x(pygame.image.load('assets/Sprites/redbird-midflap.png').convert()),pygame.transform.scale2x(pygame.image.load('assets/Sprites/redbird-upflap.png').convert())]
        self.imgused = pygame.transform.scale2x(self.frame[0])
        self.rect = self.imgused.get_rect(center = (150,325))
        self.vitesse = 0
        self.index = 0
        self.img = self.frame[self.index]
    

    
    def fly(self):
        self.vitesse = 0
        self.vitesse -= 12
        self.rect.centery += self.vitesse
    
    def fall(self):
        self.vitesse += Bird.gravity
        self.rect.centery += self.vitesse

    def rotate_bird(self):
        self.imgused = pygame.transform.rotate(self.img, -self.vitesse*3)

    def flapp(self):
        self.index = (self.index + 1) % 3
        self.img = self.frame[self.index]
        self.rect = self.img.get_rect(center = (100,self.rect.centery))