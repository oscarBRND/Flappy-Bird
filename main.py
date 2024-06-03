import random
import pygame
import os
from game import Game

def load_high_score(filename="high_score.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return int(file.read())
    return 0

def save_high_score(high_score, filename="high_score.txt"):
    with open(filename, "w") as file:
        file.write(str(high_score))


def draw_floor():
    #appliquer le sol 
    screen.blit(floor_surface,(floor_x_pos,650))
    screen.blit(floor_surface,(floor_x_pos + 1680,650))

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe.image, pipe.rectbottom )
        screen.blit(pipe.imagetop, pipe.recttop)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.move_pipes() 

def check_collision(pipes, bird):
    for pipe in pipes:
        if bird.rect.colliderect(pipe.recttop) or bird.rect.colliderect(pipe.rectbottom):
            game.font.toggle_display()
            if game.font.score > game.font.highscore:
                save_high_score(game.font.score, filename="high_score.txt")
                game.font.increase_highscore(game.font.score)
            return False
    
    if bird.rect.top <= -100 : 
        game.font.toggle_display()
        if game.font.score > game.font.highscore:
            save_high_score(game.font.score, filename="high_score.txt")
            game.font.increase_highscore(game.font.score)
        return False
    return True

pygame.init()

#Frame per second
clock = pygame.time.Clock()


#générer la fenetre du jeu
pygame.display.set_caption("flappyoiseau")
screen = pygame.display.set_mode((1280,720))


# Game variable
height_pipes = [350, 400, 450, 500, 550, 600]
#background
background_surface = pygame.image.load('assets/background.jpg').convert()
background_surface = pygame.transform.scale_by(background_surface, 1)
#floor
floor_surface = pygame.image.load('assets/Sprites/base (1).png').convert()
floor_x_pos = 0
floor_speed = 1
#Clock
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

BIRDFLAP = pygame.USEREVENT + 1 
pygame.time.set_timer(BIRDFLAP, 200)

game_active = False
#charger le jeu 
game = Game()

running = True

game.font.increase_highscore(load_high_score(filename="high_score.txt"))

while running:

    for event in pygame.event.get():
        #si le joueur ferme la fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            if event.key == pygame.K_SPACE:
                game.player.fly() 
            if event.key == pygame.K_SPACE and not game_active:
                game.player.rect.centery = 325
                game_active = True
                floor_speed = 1
                game.font.reinit_score()
                game.font.toggle_display()
                game.font.increase_highscore(load_high_score(filename="high_score.txt"))
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        elif event.type == SPAWNPIPE and game_active:
            game.add_pipe(random.choice(height_pipes))
        elif event.type == BIRDFLAP:
            game.player.flapp()


    #appliquer le bg
    screen.blit(background_surface, (0, 0))

    #Ground
    floor_x_pos -= floor_speed
    draw_floor()
    if floor_x_pos <= -1680:
        floor_x_pos = 0

    if game_active:
        #Bird
        game.player.rotate_bird()
        screen.blit(game.player.imgused, game.player.rect)
        if game.player.rect.midbottom[1] < 650:
            game.player.fall()
        else:
            game.player.vitesse = 0

        #pipes
        draw_pipes(game.pipes)
        move_pipes(game.pipes)

        game_active = check_collision(game.pipes, game.player)

        #Score
    for tube in game.pipes:
        if tube.recttop.right < game.player.rect.left and not hasattr(tube, 'scored'):
            game.font.increase_score()
            tube.scored = True

    if not game_active:
        floor_speed = 0
        screen.blit(game.font.high_score_surface,game.font.high_score_rect)
        game.pipes.empty()

    screen.blit(game.font.score_surface,game.font.score_rect)
   

    #mettre à jour l'écran
    pygame.display.update()
      
    #120 frame par second max
    clock.tick(120) 