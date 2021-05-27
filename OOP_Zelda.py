import pygame
import random
import sys
import math
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
Links_Pos = []

player_speed = 11

def randomize():
    num = random.randint(0,10)
    if num >=7:
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
ghost_list = []

class Ghost:
    def __init__(self,x,y):
        self.starting_x = x
        self.starting_y = y
        self.x = x
        self.y = y
        self.width = 100
        self.image = ghost
        self.size = self.width
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.direction = None 
        self.movement = ['up', 'down', 'left', 'right']
        self.speed = 10
        self.aggressiveness = 3
        
        
    def update(self):
        if Links_Pos[-1] != None:
            Links_Position = Links_Pos[-1]

        distance_to_link = math.sqrt((Links_Position[0]-self.rect.center[0])**2 + (Links_Position[1]-self.rect.center[1])**2)
        #Want the enemy at this point, to calculate which direction will bring it closer to Link by the greatest amount
        
        if distance_to_link <((WIDTH+HEIGHT) * .5) /self.aggressiveness:
            Attacking = True
        else:
            Attacking = False    
        
        
        if Attacking == True:
            distances = []    
            current = (self.x, self.y)
            
            for x in self.movement:
                           
                if x == 'up':
                    self.x = current[0]
                    self.y = current[1]

                    self.y -= self.speed
                    self.x += 0
                    if self.y < HEIGHT-self.size and self.y >0+self.size and self.x < WIDTH - self.size and self.x >0 + self.size:
                        
                        distances.append((self.x, self.y))
                    else:
                        distances.append((10000,10000))    
                
                if x == 'down':
                    self.x = current[0]
                    self.y = current[1]

                    self.y += self.speed
                    self.x +=0

                    if self.y < HEIGHT-self.size and self.y >0+self.size and self.x < WIDTH - self.size and self.x >0 + self.size:
                        
                        distances.append((self.x, self.y))
                    else:
                        distances.append((10000,10000))

                if x == 'left':
                    self.x = current[0]
                    self.y = current[1]

                    self.y +=0
                    self.x -= self.speed
                    if self.y < HEIGHT-self.size and self.y >0+self.size and self.x < WIDTH - self.size and self.x >0 + self.size:

                        distances.append((self.x, self.y))
                    else:
                        distances.append((10000,10000))
                
                if x == 'right':
                    self.x = current[0]
                    self.y = current[1]

                    self.y +=0
                    self.x += self.speed
                    
                    if self.y < HEIGHT-self.size and self.y >0+self.size and self.x < WIDTH - self.size and self.x >0 + self.size:

                        distances.append((self.x, self.y))
                    else:
                        distances.append((10000,10000))
                    
            distance_to_link = []
            
            for x in distances: 
            
                distance = math.sqrt((Links_Position[0]-x[0])**2 + (Links_Position[1]-x[1])**2)
                distance_to_link.append(distance)

            closest_dict = dict(zip(distances, distance_to_link))
            closest = min(closest_dict, key=closest_dict.get)

            self.x = closest[0]
            self.y = closest[1]
            self.rect.center = (self.x, self.y)
        
        if Attacking == False:
                
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
        Links_Pos.append(self.rect.center)
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
            Links_Pos.append(self.rect.center)

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.y -= player_speed
            self.x += 0
            self.down = False
            self.up = True 
            self.left = False
            self.right = False
            self.rect.center = (self.x, self.y)
            Links_Pos.append(self.rect.center)

        if keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
            self.y += 0
            self.x += player_speed
            self.down = False
            self.up = False
            self.left = False
            self.right = True
            self.rect.center = (self.x, self.y)
            Links_Pos.append(self.rect.center)

        if keys[pygame.K_LEFT] and not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT]:
            self.y += 0
            self.x -= player_speed
            self.down = False
            self.up = False
            self.left = True 
            self.right = False
            self.rect.center = (self.x, self.y)
            Links_Pos.append(self.rect.center)

player = Link()

enemy1 = Ghost(250,250)
enemy2 = Ghost(1250,250)
enemy3 = Ghost(250,750)
enemy4 = Ghost(1250,750)
ghost_list.append(enemy1)
ghost_list.append(enemy2)
ghost_list.append(enemy3)
ghost_list.append(enemy4)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if event.type == pygame.KEYDOWN:
        
        player.update()
        
    for x in ghost_list:
        if randomize() == True:
   
            x.update()
    
    screen.fill(WHITE)
    screen.blit(player.image, player.rect)
    for x in ghost_list:

        screen.blit(x.image, x.rect)
   
    pygame.display.flip()

