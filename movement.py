import pygame
import random
import sys
from pygame.locals import(
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_ESCAPE, KEYDOWN, QUIT
)
size = width, height = 800, 800
positionx = size[0] *.5
positiony = size[1] *.5
position = (positionx, positiony)
speed = [1.5, 2.25]
black = (0,0,0)
blue = (0,0,255)
turquoise= (0,255,255)


RESCALE_WIDTH = 100
RESCALE_HEIGHT = 100

pygame.init()

screen = pygame.display.set_mode(size)
ball = pygame.image.load("BEACH_BALL.jpg")
ball = pygame.transform.scale(ball, (RESCALE_WIDTH, RESCALE_HEIGHT))
#Setting player's position in center of map
player = ball.get_rect(topleft=position)


def check_coordinates(positionx, positiony, board_width, board_height, obj_width, obj_height):
    
    position = (positionx, positiony)
        
    max_width = board_width-obj_width
    max_height = board_height-obj_height

    if position[0]<0:
        positionx = 0
        return positionx, positiony 
    if position[0]>max_width:
        positionx = max_width
        return positionx, positiony
    if position[1]<0:
        positiony = 0
        return positionx, positiony
    if position[1]>max_height:
        positiony = max_height
        return positionx, positiony

    return positionx, positiony                   







running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #in the event where a key is pressed
              
              
            
            if event.key == pygame.K_DOWN:
                positiony +=50
                
                coords = check_coordinates(positionx, positiony, width, height, RESCALE_WIDTH, RESCALE_HEIGHT)
                print(coords)
                positiony = coords[1]
                position = (coords[0], coords[1])
                
                player = ball.get_rect(topleft=position)
                
                
            
            if event.key == pygame.K_LEFT:
                positionx -=50
                
                coords = check_coordinates(positionx, positiony, width, height, RESCALE_WIDTH, RESCALE_HEIGHT)
                print(coords)
                positionx = coords[0]
                position = (coords[0], coords[1])
                player = ball.get_rect(topleft=position)
                            
            if event.key == pygame.K_RIGHT:
                positionx +=50
                
                coords = check_coordinates(positionx, positiony, width, height, RESCALE_WIDTH, RESCALE_HEIGHT)
                print(coords)
                positionx = coords[0]
                position = (coords[0], coords[1])
                player = ball.get_rect(topleft=position)
                

            if event.key == pygame.K_UP:
                positiony -=50
                
                coords = check_coordinates(positionx, positiony, width, height, RESCALE_WIDTH, RESCALE_HEIGHT)
                print(coords)
                positiony = coords[1]
                position = (coords[0], coords[1])
                player = ball.get_rect(topleft=position)
                                 
    
    screen.fill(blue)
    #blit takes an object, and puts it on a surface
    #player in this case creates a rectangle object
    #the ball is then put onto this surface
    screen.blit(ball, player)
    
    pygame.display.flip()
