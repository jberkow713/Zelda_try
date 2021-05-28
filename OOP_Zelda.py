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
#list for enemy collision checking
Coord_List = []
#list for enemy movement
enemy_list = []

class Enemy:
    def __init__(self,x,y, image):
        self.starting_x = x
        self.starting_y = y
        self.x = x
        self.y = y
        self.width = 100
        self.image = image 
        self.size = self.width
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.direction = None 
        self.movement = ['up', 'down', 'left', 'right']
        self.speed = 10
        self.aggressiveness = 3
        self.invisible = False
        enemy_list.append(self)
        Coord_List.append((self.x, self.y))
        
        
    def coords_to_avoid(self, coord):
        #Start with a list of all other enemies, and eventually objects,  that exist on the map
        if self.invisible == True:
            return False
        #coord will represent the coordinate we want to check, a tuple of an x and y value
        COORD_List = []
        curr = (self.x, self.y, self.size/2)
        
        for x in Coord_List:
            if x != curr:
                COORD_List.append(x)
               
        for x in COORD_List:
            x_range = []
            y_range = []
            left_x = x[0] - x[2]
            right_x = x[0] + x[2]
            high_y = x[1] - x[2]
            low_y = x[1] + x[2]
            x_range.append(left_x)
            x_range.append(right_x)
            y_range.append(high_y)
            y_range.append(low_y)
            

            if coord[0] >=x_range[0]-(.25*self.size) and coord[0] <= x_range[1]+(.25*self.size):
                if coord[1] >= y_range[0]-(.25*self.size) and coord[1] <= y_range[1]+(.25*self.size):
                    return True 
        
        return False
               
        
    def update(self):
        #TODO, we need to take the list of current enemy positions found in To_Avoid, and make sure that the movement does not 
        #overlap ANY of these positions, while attacking, or while not attacking
        
        Links_Position = Links_Pos[-1]

        distance_to_link = math.sqrt((Links_Position[0]-self.rect.center[0])**2 + (Links_Position[1]-self.rect.center[1])**2)
        #Want the enemy at this point, to calculate which direction will bring it closer to Link by the greatest amount
        
        if distance_to_link <((WIDTH+HEIGHT) * .5) /self.aggressiveness:
            Attacking = True
        else:
            Attacking = False    
        
        
        if Attacking == True:
            distances = []    
            
            
            for x in self.movement:
                           
                if x == 'up':

                    current_x = self.x
                    current_y = self.y                    
                    

                    current_y -= self.speed
                    current_x += 0
                    if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                        if self.coords_to_avoid((current_x, current_y)) == False:

                            
                     
                            distances.append((current_x , current_y))
                    else:
                        distances.append((10000,10000))    
                
                if x == 'down':
                    current_x = self.x
                    current_y = self.y 

                    current_y += self.speed
                    current_x +=0

                    if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                        if self.coords_to_avoid((current_x, current_y)) == False:

                                                       
                        
                            distances.append((current_x , current_y))
                        
                        
                    else:
                        distances.append((10000,10000))

                if x == 'left':
                    current_x = self.x
                    current_y = self.y 

                    current_y +=0
                    current_x-= self.speed
                    if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                        if self.coords_to_avoid((current_x, current_y)) == False:

                                                       
                        
                            distances.append((current_x , current_y))

                        
                    else:
                        distances.append((10000,10000))
                
                if x == 'right':
                    current_x = self.x
                    current_y = self.y 

                    current_y +=0
                    current_x += self.speed
                    
                    if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                        if self.coords_to_avoid((current_x, current_y)) == False:

                                                        
                        
                            distances.append((current_x , current_y))
                        
                    else:
                        distances.append((10000,10000))
                    
            distance_to_link = []
            
            for x in distances: 
            
                distance = math.sqrt((Links_Position[0]-x[0])**2 + (Links_Position[1]-x[1])**2)
                distance_to_link.append(distance)

            closest_dict = dict(zip(distances, distance_to_link))
            if len(closest_dict)>0:

                closest = min(closest_dict, key=closest_dict.get)

                self.x = closest[0]
                self.y = closest[1]
                self.rect.center = (self.x, self.y)
            if len(closest_dict)==0:
                self.rect.center = (self.x, self.y)


        
        if Attacking == False:
                
            self.direction = self.movement[random.randint(0, len(self.movement)-1)]

            if self.direction == 'up':
                current_x = self.x
                current_y = self.y
                current_y -= self.speed
                current_x +=0

                
                if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                    if self.coords_to_avoid((current_x, current_y)) == False:

                        self.x = current_x
                        self.y = current_y 
                                            
                        self.rect.center = (self.x, self.y)
                
                else:

                    self.y += self.speed
                    self.x +=0
                    self.rect.center = (self.x, self.y) 
                    
                    

            if self.direction == 'down':
                current_x = self.x
                current_y = self.y
                current_y += self.speed
                current_x +=0

                if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                    if self.coords_to_avoid((current_x, current_y)) == False:

                        self.x = current_x
                        self.y = current_y 

                        self.rect.center = (self.x, self.y)
                else:

                    self.y -= self.speed
                    self.x +=0
                    self.rect.center = (self.x, self.y) 
                    

            if self.direction == 'left':
                current_x = self.x
                current_y = self.y
                current_y +=0
                current_x -= self.speed
                
                if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                    if self.coords_to_avoid((current_x, current_y)) == False:

                        self.x = current_x
                        self.y = current_y 

                        self.rect.center = (self.x, self.y)
                else:
                    self.y += 0
                    self.x += self.speed 
                    self.rect.center = (self.x, self.y) 
                        
            if self.direction == 'right':
                current_x = self.x
                current_y = self.y
                current_y +=0
                current_x += self.speed
                
                if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                    if self.coords_to_avoid((current_x, current_y)) == False:

                        self.x = current_x
                        self.y = current_y 
                                                
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

enemy1 = Enemy(250,250, ghost)
enemy2 = Enemy(1250,250,ghost)
enemy3 = Enemy(250,750,ghost)
enemy4 = Enemy(1250,750,ghost)
enemy5 = Enemy(1000, 250,ghost)
enemy6 = Enemy(1000, 500,ghost)

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
    
    

    length = len(enemy_list)
    index = 0
    while length >0:
        curr = enemy_list[index]
        
        Coord_List[index] =  (curr.x, curr.y, curr.size/2)     
        
        
        index +=1
        length -=1    
    
    for x in enemy_list:
                
        if randomize() == True:
            
            x.update()

        screen.blit(x.image, x.rect)
    

    pygame.display.flip()

