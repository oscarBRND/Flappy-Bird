import random
import pygame
from game import Game

def draw_floor():
    #appliquer le sol 
    screen.blit(floor_surface,(floor_x_pos,650))
    screen.blit(floor_surface,(floor_x_pos + 1680,650))

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe.image, pipe.rectbottom )
        screen.blit(pipe.imagetop, pipe.recttop)


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

#charger le jeu 
game = Game()

running = True

game.score.read_high_score(filename="high_score.txt")

while running:

    for event in pygame.event.get():
        #si le joueur ferme la fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            #en jeu
            if event.key == pygame.K_SPACE and game.game_state == 'Play':
                game.player.fly() 
            #Gameover
            elif event.key == pygame.K_SPACE and game.game_state == 'Gameover':
                game.mode_menu()
            #Menu
            elif event.key == pygame.K_SPACE and game.game_state == 'Menu':
                game.player.rect.centery = 325
                floor_speed = 1
                game_active = True
                game.score.reinit_score()
                game.mode_play()
                game.score.read_high_score(filename="high_score.txt")
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        elif event.type == SPAWNPIPE and game.game_state == 'Play':
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

    if game.game_state == 'Play':
        #Bird
        game.player.rotate_bird()
        screen.blit(game.player.imgused, game.player.rect)
        if game.player.rect.midbottom[1] < 650:
            game.player.fall()
        else:
            game.player.vitesse = 0

        #pipes
        draw_pipes(game.pipes)
        game.move_pipes()

        #Collision
        game.check_collision()
 
        #Score
        for tube in game.pipes:
            if tube.recttop.right < game.player.rect.left and not hasattr(tube, 'scored'):
                game.score.increase_score()
                tube.scored = True


    if game.game_state == 'Gameover':
        screen.blit(game.gameover.image,game.gameover.rect)
        floor_speed = 0
        game.pipes.empty()
        screen.blit(game.player.imgused, game.player.rect)
        game.player.dead()
        if game.player.rect.midbottom[1] < 650:
            game.player.fall()
        else:
            game.player.vitesse = 0

    if game.game_state == 'Menu':
        floor_speed = 0
        screen.blit(game.score.high_score_surface,game.score.high_score_rect)
        game.pipes.empty()

    screen.blit(game.score.score_surface,game.score.score_rect)
   

    #mettre à jour l'écran
    pygame.display.update()
      
    #120 frame par second max
    clock.tick(120) 