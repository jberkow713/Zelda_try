import pygame
import random
import sys
from pygame.locals import(
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_ESCAPE, KEYDOWN, QUIT
)
size = width, height = 800, 800
centerx = size[0] *.5
centery = size[1] *.5
center = (centerx, centery)
speed = [1.5, 2.25]
black = (0,0,0)
blue = (0,0,255)
turquoise= (0,255,255)

pygame.init()

screen = pygame.display.set_mode(size)
ball = pygame.image.load("BEACH_BALL.jpg")
ball = pygame.transform.scale(ball, (50, 50))
#Setting player's position in center of map
player = ball.get_rect(topleft=center)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #in the event where a key is pressed
              
              
            
            if event.key == pygame.K_DOWN:
                centerx += 50
                centery +=50
                player.center = (centerx, centery)
                if player.left <0:
                    player.left = 0
                    centerx = player.left
                if player.right >width:
                    player.right = width
                    centerx = player.right    
                if player.top <0:
                    player.top = 0
                    centery = player.top
                if player.bottom > height:
                    player.bottom = height
                    centery = player.bottom  
            if event.key == pygame.K_UP:
                centerx -=50
                centery -=50
                player.center = (centerx, centery)

                if player.left <0:
                    player.left = 0
                    centerx = player.left
                if player.right >width:
                    player.right = width
                    centerx = player.right    
                if player.top <0:
                    player.top = 0
                    centery = player.top
                if player.bottom > height:
                    player.bottom = height
                    centery = player.bottom     
    
    screen.fill(blue)
    #blit takes an object, and puts it on a surface
    #player in this case creates a rectangle object
    #the ball is then put onto this surface
    screen.blit(ball, player)
    
    pygame.display.flip()
