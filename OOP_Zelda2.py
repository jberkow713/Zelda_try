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

enemy_list = []

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
        enemy_list.append(self)
        
    def update(self):
        
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
        self.width = 100
        self.size = self.width
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.down = True #link faces down by default
        self.up = False
        self.left = False
        self.right = False
        Links_Pos.append(self.rect.center)

    def update(self):
        
        #MOVEMENT
        self.down = False
        self.up = False
        self.left = False
        self.right = False
        
        keys = pygame.key.get_pressed()
        
        self.down = keys[pygame.K_DOWN]
        self.up = keys[pygame.K_UP] 
        self.right = keys[pygame.K_RIGHT]
        self.left = keys[pygame.K_LEFT]
        
        #temp variables to test edge of screen
        self.new_y = self.y
        self.new_x = self.x

        self.new_y += -player_speed * keys[pygame.K_UP] + player_speed * keys[pygame.K_DOWN]
        self.new_x += -player_speed * keys[pygame.K_LEFT] + player_speed * keys[pygame.K_RIGHT]
        
        if self.new_y < HEIGHT-self.size and self.new_y >0+self.size and self.new_x < WIDTH - self.size and self.new_x >0 + self.size:

            self.x = self.new_x
            self.y = self.new_y  
            self.rect.center = (self.x, self.y)
            Links_Pos.append(self.rect.center)
        
        else:
            
            self.rect.center = (self.x, self.y)
            Links_Pos.append(self.rect.center)


player = Link()

enemy1 = Ghost(250,250)
enemy2 = Ghost(1250,250)
enemy3 = Ghost(250,750)
enemy4 = Ghost(1250,750)


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
    for x in enemy_list:

        screen.blit(x.image, x.rect)
   
    pygame.display.flip()