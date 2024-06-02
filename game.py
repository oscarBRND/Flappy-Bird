import pygame
from player import Bird
from entities import Pipe, Font

#classe qui represente le jeu ?
class Game:

    def __init__(self):
        #charger le joueur
        self.player = Bird()
        self.pressed = {}
        self.pipes = pygame.sprite.Group()
        self.font = Font()
        
    def add_pipe(self, y):
        pipe = Pipe(y)
        self.pipes.add(pipe)




        
