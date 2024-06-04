import pygame
from player import Bird
from entities import Pipe, Score, Gameover

#classe qui represente le jeu ?
class Game:

    def __init__(self):
        self.game_state = 'Menu'
        #charger le joueur
        self.player = Bird(self)
        self.gameover = Gameover()
        self.pressed = {}
        self.pipes = pygame.sprite.Group()
        self.score = Score(self)
        
    def add_pipe(self, y):
        pipe = Pipe(y)
        self.pipes.add(pipe)

    def move_pipes(self):
        for pipe in self.pipes:
            pipe.move_pipes() 

    def mode_play(self):
        self.game_state = 'Play'
        self.score.update_score_surface()

    def mode_menu(self):
        self.game_state = 'Menu'
        self.score.update_score_surface()


    def check_collision(self):
        for pipe in self.pipes:
            if self.player.rect.colliderect(pipe.recttop) or self.player.rect.colliderect(pipe.rectbottom):
                if self.score.score > self.score.highscore:
                    self.score.save_high_score(filename="high_score.txt")
                    self.score.increase_highscore(self.score.score)
                self.game_state = 'Gameover'
                self.score.update_score_surface()
        if self.player.rect.top <= -100 : 
            if self.score.score > self.score.highscore:
                self.score.save_high_score(filename="high_score.txt")
                self.score.increase_highscore(self.score.score)
            self.game_state = 'Gameover'
            self.score.update_score_surface()


        
