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
GHOST_WIDTH = 100
GHOST_HEIGHT = 100
#defining colors
GROUND_COLOR = (255, 222, 179)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)

player_speed = 5

def randomize():
    num = random.randint(0,4)
    if num >=2:
        return True
    else:
        return False      


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Legend of Zelda")
link = pygame.image.load("link.jpg").convert_alpha()
link = pygame.transform.scale(link, (LINK_WIDTH, LINK_HEIGHT))
ghost = pygame.image.load("ghost.png").convert_alpha()
ghost = pygame.transform.scale(ghost, (GHOST_WIDTH, GHOST_HEIGHT))
enemy_list = []

class Enemy:
    def __init__(self,x,y):
        self.starting_x = x
        self.starting_y = y
        self.x = x
        self.y = y
        self.image = ghost
        self.size = GHOST_WIDTH
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.direction = None 
        self.movement = ['up', 'down', 'left', 'right']
        self.speed = 10
        
    def update(self):

        self.direction = self.movement[random.randint(0, len(self.movement)-1)]


        if self.direction == 'up':
            
            self.y -= self.speed
            self.x += 0
            if self.y < HEIGHT-self.size and self.y >0+self.size and self.x < WIDTH - self.size and self.x >0 + self.size:
                
                self.rect.center = (self.x, self.y)
            
            else:

                self.y += self.speed
                self.x +=0
                self.rect.center = (self.x, self.y) 
                
                

        if self.direction == 'down':
            self.y += self.speed
            self.x +=0

            if self.y < HEIGHT-self.size and self.y >0+self.size and self.x < WIDTH - self.size and self.x >0 + self.size:
                self.rect.center = (self.x, self.y)
            else:

                self.y -= self.speed
                self.x +=0
                self.rect.center = (self.x, self.y) 
                

        if self.direction == 'left':
            self.y +=0
            self.x -= self.speed
            if self.y < HEIGHT-self.size and self.y >0+self.size and self.x < WIDTH - self.size and self.x >0 + self.size:

                self.rect.center = (self.x, self.y)
            else:
                self.y += 0
                self.x += self.speed 
                self.rect.center = (self.x, self.y) 
                    
        if self.direction == 'right':
            self.y +=0
            self.x += self.speed
            if self.y < HEIGHT-self.size and self.y >0+self.size and self.x < WIDTH - self.size and self.x >0 + self.size:

                self.rect.center = (self.x, self.y)
            else:
                
                self.y += 0
                self.x -= self.speed 
                self.rect.center = (self.x, self.y) 
                   
        
                    


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
            
            

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.y -= player_speed
            self.x += 0
            self.down = False
            self.up = True 
            self.left = False
            self.right = False
            self.rect.center = (self.x, self.y)
            

        if keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
            self.y += 0
            self.x += player_speed
            self.down = False
            self.up = False
            self.left = False
            self.right = True
            self.rect.center = (self.x, self.y)
            

        if keys[pygame.K_LEFT] and not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT]:
            self.y += 0
            self.x -= player_speed
            self.down = False
            self.up = False
            self.left = True 
            self.right = False
            self.rect.center = (self.x, self.y)
             


player = Link()

enemy1 = Enemy(250,250)
enemy2 = Enemy(750,750)
enemy3 = Enemy(750,250)
enemy4 = Enemy(250,750)
enemy_list.append(enemy1)
enemy_list.append(enemy2)
enemy_list.append(enemy3)
enemy_list.append(enemy4)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if event.type == pygame.KEYDOWN:
        
        player.update()
        
    for x in enemy_list:
        if randomize() == True:
   
            x.update()
       

    screen.fill(WHITE)
    screen.blit(player.image, player.rect)
    screen.blit(enemy1.image, enemy1.rect)
    screen.blit(enemy2.image, enemy2.rect)
    screen.blit(enemy3.image, enemy3.rect)
    screen.blit(enemy4.image, enemy4.rect)
    
    pygame.display.flip()

