import pygame

class Pipe(pygame.sprite.Sprite):

    def __init__(self,ybottom):
        super().__init__()
        self.image = pygame.transform.scale2x(pygame.image.load('assets/Sprites/pipe-green.png').convert())
        self.imagetop = pygame.transform.flip(self.image,False,True)
        self.rectbottom = self.image.get_rect()
        self.recttop = self.imagetop.get_rect()
        self.recttop.bottomleft = (1280,ybottom -300)
        self.rectbottom.topleft = (1280, ybottom)
        
    def move_pipes(self):
        self.rectbottom.x -=5
        self.recttop.x-= 5
        if self.recttop.x < -self.recttop.width:
            self.kill() 


class Font(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.highscore = 0
        self.game_font = pygame.font.Font('04B_19__.TTF', 40)
        self.game_state = True
        self.update_score_surface()
        

    def update_score_surface(self):
        if self.game_state:
            self.score_surface = self.game_font.render(str(self.score), True, (255, 255, 255))
            self.score_rect = self.score_surface.get_rect(center=(640, 50))
            self.high_score_surface = None
            self.high_score_rect = None
        else : 
            self.score_surface = self.game_font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.score_rect = self.score_surface.get_rect(center=(640, 50))
            self.high_score_surface = self.game_font.render(f"High score: {self.highscore}", True, (255, 255, 255))
            self.high_score_rect = self.high_score_surface.get_rect(center=(640, 600))

    def increase_score(self):
        self.score += 1
        self.update_score_surface()
        
    def reinit_score(self):
        self.score = 0
        self.update_score_surface()
        
    def toggle_display(self):
        self.game_state = not self.game_state
        self.update_score_surface()
    
    def increase_highscore(self, score):
        self.highscore = score
        self.update_score_surface()

