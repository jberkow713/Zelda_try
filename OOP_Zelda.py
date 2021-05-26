import pygame
import random
import sys
from pygame.locals import(
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_ESCAPE, KEYDOWN, QUIT
)
WIDTH = 1500 #1800
HEIGHT = 1000 #1400
FPS = 60
LINK_WIDTH = 100
LINK_HEIGHT = 100

#defining colors
GROUND_COLOR = (255, 222, 179)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)

player_speed = 10

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Legend of Zelda")
link = pygame.image.load("link.jpg").convert_alpha()
link = pygame.transform.scale(link, (LINK_WIDTH, LINK_HEIGHT))

class Link:
    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.image = link
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.down = True #link faces down by default
        self.up = False
        self.left = False
        self.right = False
        
        
        

    def update(self):
        
        #MOVEMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.y += player_speed
            self.x += 0
            self.down = True
            self.up = False
            self.left = False
            self.right = False
            self.rect.center = (self.x, self.y)
            print(self.rect.center)
            

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.y -= player_speed
            self.x += 0
            self.down = False
            self.up = True 
            self.left = False
            self.right = False
            self.rect.center = (self.x, self.y)
            print(self.rect.center)

        if keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
            self.y += 0
            self.x += player_speed
            self.down = False
            self.up = False
            self.left = False
            self.right = True
            self.rect.center = (self.x, self.y)
            print(self.rect.center)

        if keys[pygame.K_LEFT] and not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT]:
            self.y += 0
            self.x -= player_speed
            self.down = False
            self.up = False
            self.left = True 
            self.right = False
            self.rect.center = (self.x, self.y)
            print(self.rect.center) 


player = Link()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if event.type == pygame.KEYDOWN:
        
        player.update()
        

    
    
    screen.fill(WHITE)
    screen.blit(player.image, player.rect)
    
    
    pygame.display.flip()

