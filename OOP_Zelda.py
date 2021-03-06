import pygame
import random
import sys
import math
from pygame.locals import(
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_ESCAPE, KEYDOWN, QUIT, K_RETURN
)
WIDTH = 1500 #1800
HEIGHT = 1000 #1400
FPS = 60
LINK_WIDTH = 100
LINK_HEIGHT = 100
SWORD_WIDTH = 100
SWORD_HEIGHT = 100 
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

sword_pos = (0,0) 

player_speed = 10

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Legend of Zelda")
link = pygame.image.load("link.jpg").convert_alpha()

link = pygame.transform.scale(link, (LINK_WIDTH, LINK_HEIGHT))
#Link Directions
link_up = pygame.image.load("Link_Up_Advanced.jpg")
link_up = pygame.transform.scale(link_up, (LINK_WIDTH, LINK_HEIGHT))

link_down = pygame.image.load("Link_Down_Advanced.png")
link_down = pygame.transform.scale(link_down, (LINK_WIDTH, LINK_HEIGHT))

link_left = pygame.image.load("Link_Left_advanced.png").convert_alpha()
link_left = pygame.transform.scale(link_left, (LINK_WIDTH, LINK_HEIGHT))

link_right = pygame.image.load("Link_Right_Advanced.png").convert_alpha()
link_right = pygame.transform.scale(link_right, (LINK_WIDTH, LINK_HEIGHT))
#Sword

sword_up = pygame.image.load("Link_Sword_Up.jpg")
sword_up = pygame.transform.scale(sword_up, (SWORD_WIDTH, SWORD_HEIGHT))

sword_down = pygame.image.load("Link_Sword_Down.png")

sword_down = pygame.transform.scale(sword_down, (SWORD_WIDTH, SWORD_HEIGHT))

sword_left = pygame.image.load("Link_Sword_Left.jpg")
sword_left = pygame.transform.scale(sword_left, (SWORD_WIDTH, SWORD_HEIGHT))

sword_right = pygame.image.load("Link_Sword_Right.png")
sword_right = pygame.transform.scale(sword_right, (SWORD_WIDTH, SWORD_HEIGHT))

Enemy_Weapon = pygame.image.load("Enemy_Weapon.jpg")
Enemy_Weapon = pygame.transform.scale(Enemy_Weapon, (50, 50))

WALL= pygame.image.load("Zelda_Wall.jpg")
WALL = pygame.transform.scale(WALL, (100, 100))

DOOR = pygame.image.load("black_square.png").convert_alpha()
DOOR = pygame.transform.scale(DOOR, (100, 100))

LOCKED_DOOR = pygame.image.load("Locked_Door.jpg")
LOCKED_DOOR = pygame.transform.scale(LOCKED_DOOR, (100, 100))

ghost = pygame.image.load("ghost.png").convert_alpha()
ghost = pygame.transform.scale(ghost, (GHOST_WIDTH, GHOST_HEIGHT))

dragon = pygame.image.load("DRAGON_ZELDA.jpg")
dragon  = pygame.transform.scale(dragon , (250, 250))

Tree = pygame.image.load('TREE_PNG.png')
Mountain = pygame.image.load('MOUNTAIN_PNG.png')
#list for enemy collision checking
Coord_List = []
Object_Coords = []
#list for enemy movement
enemy_list = []
object_list = []
Door_Coords = []
Door_List = []
enemy_length = 0
enemy_index = 0
room_edges = [0]*2


def randomize(number):
    num = random.randint(0,10)
    if num >=number:
        return True
    else:
        return False  
  
def Collide(x, y, size, buffer, starting_position, list):
    #Check collisions for enemies, objects, Link, etc...
    left_x = x - 4 * size 
    right_x = x + 4 * size 
    upper = y - 5.5*size 
    lower = y + 5.5*size 
        
    possible_vals = list[starting_position:]
        
    usable_list = [x for x in possible_vals if x[0]-x[2]>=left_x and x[0]+x[2] <= right_x and x[1]-x[2]> upper and x[1]+x[2]< lower ]
    
    for A in usable_list:
        x_range = []
        y_range = []
        left_x = A[0] - A[2]
        right_x = A[0] + A[2]
        high_y = A[1] - A[2]
        low_y = A[1] + A[2]
        x_range.append(left_x)
        x_range.append(right_x)
        y_range.append(high_y)
        y_range.append(low_y)

        if x >=x_range[0]-(buffer*size) and x <= x_range[1]+(buffer*size):
            if y >= y_range[0]-(buffer*size) and y <= y_range[1]+(buffer*size):
                
                return True    


class OBJECT:
    def __init__(self, x, y, image, size, door=None):
        self.x = x
        self.y = y
        self.size = size 
        self.image = image
        self.door = door
        
        # We set image so it ignores background of white
        self.image.set_colorkey(WHITE) 
        self.rescale()
        if door != None:
            Door_Coords.append((self.x, self.y, self.size/2))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        Object_Coords.append((self.x, self.y, self.size/2))
        object_list.append(self)
    
class Projectile:
    def __init__(self, x, y, image, direction, index):
        #For enemy firing
        self.x = x
        self.y = y
        self.image = image
        self.image.set_colorkey(WHITE)
        self.direction = direction 
        self.index = index
        self.size = 50
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def move_projectile(self):
        if self.direction == 'UP':
            self.y -= self.speed 
        elif self.direction == 'DOWN':
            self.y += self.speed
        elif self.direction == 'RIGHT':
            self.x += self.speed
        elif self.direction == 'LEFT':
            self.x -= self.speed

        return self.x, self.y

class Enemy:
    def __init__(self,x,y, image, type,size):
        
        self.x = x
        self.y = y
        self.invisible = False
        self.invis_count = 0
        self.type = type 
        self.create_stats()
        self.size = size
        self.image = image
        self.rescale()
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.direction = None
        self.path = None  
        self.movement = ['up', 'down', 'left', 'right']
        enemy_list.append(self)
        Coord_List.append((self.x, self.y))
        self.health = self.get_health()
        self.hit = False
        self.down = True #enemy faces down by default
        self.up = False
        self.left = False
        self.right = False
        self.shooting = False
        self.index = None
        global enemy_length
        enemy_length+=1
        global enemy_index
        self.index = enemy_index 
        enemy_index +=1
                
               
    
    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
    def get_health(self):
        health_dict = {'ghost': 4, 'dragon':20, 'centaur':6}
        for k,v in health_dict.items():
            if self.type == k:
                return v

    def create_stats(self):
        
        invis_dict = {'ghost':True, 'dragon':False, 'centaur':False}
        for k,v in invis_dict.items():
            if self.type == k:
                # if randomize(6)==True:
                self.invisible = v 

        self.speed = random.randint(2,5)
        self.aggressiveness = random.randint(2,5)
                
        
    def shooting_check(self, other):
        #checking if enemy in range to shoot
        if abs(self.x - other.x) <15:
            if abs(self.y - other.y) >self.size*1.5:
                if self.y > other.y:

                    if self.get_direction() =='UP':
                        
                        return True, 'UP'
                if self.y < other.y:
                    if self.get_direction() =='DOWN':
                        
                        return True, 'DOWN'

        if abs(self.y - other.y) <15:
            if abs(self.x-other.x) > self.size*1.5:
                if self.x > other.x:

                    if self.get_direction() == 'LEFT':
                        
                        return  True, 'LEFT'
                if self.x < other.x:
                    if self.get_direction() == 'RIGHT':

                        return  True, 'RIGHT'

    def get_coords_projectile(self, other):
        if self.shooting_check(other):
            
            coords =  (self.x, self.y, self.shooting_check(other)[1])
            coord_x = self.x
            coord_y = self.y  
            if coords[2] == 'UP':
                coord_y -= self.size/2
            elif coords[2] == 'DOWN':
                coord_y += self.size/2
            elif coords[2] == 'RIGHT':
                coord_x += self.size/2
            elif coords[2] == 'LEFT':
                coord_x -= self.size/2

            return coord_x, coord_y, coords[2]

    def coords_to_avoid(self, coord):
        #Start with a list of all other enemies, and eventually objects,  that exist on the map              
        
        curr = (self.x, self.y, self.size/2)
        Big_List = Coord_List + Object_Coords
        COORD_List = [x for x in Big_List if x!= curr]
        
        if Collide(coord[0], coord[1], self.size, .3, 0,COORD_List)==True:
            return True                    
                
        return False
    def get_direction(self):

        if self.up == True:
            return 'UP'
        if self.down == True:
            return 'DOWN'
        if self.left == True:
            return 'LEFT'
        if self.right == True:
            return 'RIGHT'     
           
    def update(self):
        #Update enemy position
        
        Links_Position = Links_Pos[-1]

        distance_to_link = math.sqrt((Links_Position[0]-self.rect.center[0])**2 +\
            (Links_Position[1]-self.rect.center[1])**2)
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
                
                            distances.append((current_x , current_y, 'up'))
                        else:                        
                            distances.append((10000,10000))    
                
                if x == 'down':

                    current_x = self.x
                    current_y = self.y 
                    current_y += self.speed
                    current_x +=0

                    if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                        if self.coords_to_avoid((current_x, current_y)) == False:
                            distances.append((current_x , current_y, 'down'))
                        else:
                            distances.append((10000,10000))

                if x == 'left':

                    current_x = self.x
                    current_y = self.y 
                    current_y +=0
                    current_x-= self.speed
                    
                    if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                        if self.coords_to_avoid((current_x, current_y)) == False:
                            distances.append((current_x , current_y, 'left'))
                            
                        else:                        
                            distances.append((10000,10000))
                
                if x == 'right':

                    current_x = self.x
                    current_y = self.y 
                    current_y +=0
                    current_x += self.speed
                    
                    if current_y < HEIGHT-self.size and current_y >0+self.size and current_x < WIDTH - self.size and current_x >0 + self.size:
                        if self.coords_to_avoid((current_x, current_y)) == False:                
                            distances.append((current_x , current_y, 'right'))
                            
                        else:
                            distances.append((10000,10000))
                    
            distance_to_link = []
            
            for x in distances: 
            
                distance = math.sqrt((Links_Position[0]-x[0])**2 + (Links_Position[1]-x[1])**2)
                distance_to_link.append(distance)
            #Dictionary with possible directions and their corresponding distances
            closest_dict = dict(zip(distances, distance_to_link))
            
            #no movement if trapped
            if len(closest_dict)==0:
                self.rect.center = (self.x, self.y)
            
            if len(closest_dict)>0:
                #choose direction with closest distance to Link
                closest = min(closest_dict, key=closest_dict.get)
                #puts enemy back in original spot if all moves give this default of (10,000, 10,000)
                if closest[0] == 10000:
                    self.rect.center = (self.x, self.y)

                else:
                    #set coordinates to best possible directions coordinates    
                    self.x = closest[0]
                    self.y = closest[1]

                    self.rect.center = (self.x, self.y)
                    
                    direction = closest[2]
                    if direction == 'up':
                        self.down = False  
                        self.up = True
                        self.left = False
                        self.right = False
                    elif direction == 'down':
                        self.down = True   
                        self.up = False 
                        self.left = False
                        self.right = False
                    elif direction == 'right':
                        self.down = False    
                        self.up = False 
                        self.left = False  
                        self.right = True
                    elif direction == 'left':
                        self.down = False    
                        self.up = False 
                        self.left = True 
                        self.right = False                      

        
        if Attacking == False:
            
            if self.path == None:
                
                self.direction = self.movement[random.randint(0, len(self.movement)-1)]                
            
            if self.path == 'up':
                self.direction = 'up'
            if self.path == 'down':
                self.direction = 'down'
            if self.path == 'right':
                self.direction = 'right'
            if self.path == 'left':
                self.direction = 'left'

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
                        self.path = 'up'
                        self.down = False  
                        self.up = True
                        self.left = False
                        self.right = False 
                    
                    else:
                        self.rect.center = (self.x, self.y)
                        self.path = None
                        
                else:
                    self.rect.center = (self.x, self.y)
                    self.path = None                   

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
                        self.path = 'down'
                        self.down = True   
                        self.up = False 
                        self.left = False
                        self.right = False
                    else:
                        self.rect.center = (self.x, self.y)
                        self.path = None
                else:
                    self.rect.center = (self.x, self.y)
                    self.path = None                         

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
                        self.down = False    
                        self.up = False 
                        self.left = True 
                        self.right = False
                        self.path = 'left' 
                    else:                            
                        self.rect.center = (self.x, self.y)
                        self.path = None
                else:
                    self.rect.center = (self.x, self.y)
                    self.path = None                                
                        
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
                        self.down = False    
                        self.up = False 
                        self.left = False  
                        self.right = True
                        self.path = 'right' 
                    else:                        
                        self.rect.center = (self.x, self.y)
                        self.path = None
                else:

                    self.rect.center = (self.x, self.y)
                    self.path = None             
                                            

class Sword:
    
    def __init__(self, owner):
        self.owner = owner
        self.image = self.load_sword() 
        self.x = -1000
        self.y = -1000
        self.size = SWORD_WIDTH
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)        

    def load_sword(self):
        if self.owner.direction()=='UP':
            self.image = sword_up
            self.image.set_colorkey(WHITE)
            return self.image
        if self.owner.direction()=='DOWN':
            self.image = sword_down
            self.image.set_colorkey(WHITE)
            return self.image    
        if self.owner.direction()=='RIGHT':
            self.image = sword_right
            self.image.set_colorkey(WHITE)
            return self.image    
        if self.owner.direction()=='LEFT':
            self.image = sword_left
            self.image.set_colorkey(WHITE)
            return self.image

class Link:
    def __init__(self):
        self.sword = None 
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.image = link
        self.image.set_colorkey(WHITE)
        self.invincible = False
        self.invincible_animation_count = 0
        self.stunned_animation_count = 0 
        self.stunned = False 
        self.width = 100
        self.size = self.width
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.health = 10
        self.down = True #link faces down by default
        self.up = False
        self.left = False
        self.right = False
        self.ring = None 
        Links_Pos.append(self.rect.center)
        Object_Coords.append((self.x, self.y))
    
    def direction(self):
        if self.up == True:
            return 'UP'
        if self.down == True:
            return 'DOWN'
        if self.left == True:
            return 'LEFT'
        if self.right == True:
            return 'RIGHT'            
    
    def coords_to_avoid(self, coord):
        #When Link is not invincible, makes sure he does not move over objects, or enemies
        # Return 99 if runs into an enemy
                
        curr = (self.x, self.y, self.size/2)      
        Enemy_COORD_List = [x for x in Coord_List]
        Object_Coord_List = [x for x in Object_Coords if x != curr]
        if Collide(coord[0], coord[1], self.size, .3, 0, Object_Coord_List)== True:           
            return True          

        if Collide(coord[0], coord[1], self.size, .3, 0, Enemy_COORD_List) == True:
        
            if self.invincible == False:
                return 99
        
        return False
    
    def non_moving_check(self):
        #When Link is not invincible and not moving, checks if he is inside a monster, or near a monster...
        
        if Collide(self.x, self.y, self.size, .35, 0, Coord_List) == True:
       
            if self.invincible == False:

                self.health -=.01
                self.health = round(self.health,2)
                if self.health <=0:
                    print('Game Over')

                    return sys.exit() 
        return
    
    def player_enemy_collision(self):
        #Checks only player against enemy units
        
        curr = (self.new_x, self.new_y, self.size/2)    
        Obj_Coords = [x for x in Object_Coords if x != curr]                       
        
        if Collide(self.new_x, self.new_y, self.size, .3, 0, Obj_Coords)== True:
            return True 
                       
        if self.new_y > HEIGHT-self.size or self.new_y <0+self.size or self.new_x > WIDTH - self.size or self.new_x <0 + self.size:
            return True
        
        return         

    def configure_direction(self):
        if self.up == True:
            self.image = link_up
            self.image.set_colorkey(WHITE)
        if self.down == True:
            self.image = link_down
            self.image.set_colorkey(WHITE)            
        if self.right == True:
            self.image = link_right
            self.image.set_colorkey(WHITE)            
        if self.left == True:
            self.image = link_left
        
        return self.image        

    def set_player_direction(self,direction):
        #Set's player directional attributes
        if direction == 'UP':
            self.rect.center = (self.x, self.y)
            Links_Pos.append(self.rect.center)
            self.up = True
            self.down = False
            self.right = False
            self.left = False
            return
        elif direction == 'DOWN':
            self.rect.center = (self.x, self.y)
            Links_Pos.append(self.rect.center)
            self.up = False
            self.down = True 
            self.right = False
            self.left = False
            return
        elif direction == 'RIGHT':
            self.rect.center = (self.x, self.y)
            Links_Pos.append(self.rect.center)
            self.up = False
            self.down = False 
            self.right = True 
            self.left = False
            return
        elif direction == 'LEFT':
            self.rect.center = (self.x, self.y)
            Links_Pos.append(self.rect.center)
            self.up = False
            self.down = False 
            self.right = False 
            self.left = True
            return              

    def update(self):                              
                
        #checking stunned condition, shortly paralyzed while stunned
        if self.stunned == True:
            self.stunned_animation_count +=1
        if self.stunned_animation_count >=25:
            self.stunned_animation_count = 0
            self.stunned = False   
        #Can move again once not stunned, checks key commands
        if self.stunned == False:

            keys = pygame.key.get_pressed()
              
            self.new_y = self.y
            self.new_x = self.x           
                    
            if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                self.new_y -= player_speed
                self.new_x +=0
                
                #Checks to see that pre-collision move is not into wall, this must always be checked first
                if self.new_y < HEIGHT-self.size and self.new_y >0+self.size and self.new_x < WIDTH - self.size and self.new_x >0 + self.size:
                    #If he has avoided an object, but run into an enemy
                    if self.coords_to_avoid((self.new_x, self.new_y)) == 99:
                        #Collision created
                        self.health -=.5
                        self.invincible = True
                        self.invincible_animation_count = 0                        
                        self.new_y += player_speed *20
                        self.new_x +=0
                        self.stunned = True 
                        self.x = self.new_x
                        #This is checking objects and walls ONLY off the bounceback
                        # If true, that means overlapped object, returns original coords, and exits function                                               
                        if self.player_enemy_collision() == True:
                            self.set_player_direction('UP')                             
                            return                                                       
                        
                        #Otherwise, bounceback can occur, sets player coords equal to bounceback coords
                        self.x = self.new_x
                        self.y = self.new_y  
                        
                    #If wall has been avoided, enemy has been avoided, and objects have been avoided
                    if self.coords_to_avoid((self.new_x, self.new_y)) == False:

                        self.x = self.new_x
                        self.y = self.new_y  
                self.set_player_direction('UP')     
                            
            if keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:

                self.new_y += player_speed
                self.new_x +=0
                   
                if self.new_y < HEIGHT-self.size and self.new_y >0+self.size and self.new_x < WIDTH - self.size and self.new_x >0 + self.size:
                    if self.coords_to_avoid((self.new_x, self.new_y)) == 99:
                        self.health -=.5
                        self.invincible = True
                        self.invincible_animation_count = 0
                        
                        self.new_y -= player_speed *20
                        self.new_x +=0
                        self.stunned = True
                       
                        if self.player_enemy_collision() == True:
                            self.set_player_direction('DOWN') 
                            return                       
                        
                        self.x = self.new_x
                        self.y = self.new_y                          
                    
                    if self.coords_to_avoid((self.new_x, self.new_y)) == False:

                        self.x = self.new_x
                        self.y = self.new_y                                     
                self.set_player_direction('DOWN')

            if keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
                    
                self.new_x += player_speed
                self.new_y +=0
                #if youre not off screen
                if self.new_y < HEIGHT-self.size and self.new_y >0+self.size and self.new_x < WIDTH - self.size and self.new_x >0 + self.size:
                     
                    if self.coords_to_avoid((self.new_x, self.new_y)) == 99:
                        self.health -=.5
                        self.invincible = True
                        self.invincible_animation_count = 0
                        self.new_x -= player_speed *20
                        self.new_y +=0
                        self.stunned = True

                        if self.player_enemy_collision() == True:
                            self.set_player_direction('RIGHT')                            
                            return                                            
                                                    
                        self.x = self.new_x
                        self.y = self.new_y                       
                    
                    if self.coords_to_avoid((self.new_x, self.new_y)) == False:

                        self.x = self.new_x
                        self.y = self.new_y                               
                self.set_player_direction('RIGHT')

            if keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:

                self.new_x -= player_speed
                self.new_y +=0
                
                if self.new_y < HEIGHT-self.size and self.new_y >0+self.size and self.new_x < WIDTH - self.size and self.new_x >0 + self.size:
                    if self.coords_to_avoid((self.new_x, self.new_y)) == 99:
                        self.health -=.5
                        self.invincible = True
                        self.invincible_animation_count = 0
                        self.new_x += player_speed *20
                        self.new_y +=0
                        self.stunned = True
                        
                        if self.player_enemy_collision() == True:
                            self.set_player_direction('LEFT')                            
                            return

                        self.x = self.new_x
                        self.y = self.new_y                          
                    
                    if self.coords_to_avoid((self.new_x, self.new_y)) == False:

                        self.x = self.new_x
                        self.y = self.new_y                         
                self.set_player_direction('LEFT')

            if keys[pygame.K_RETURN]:
                global sword_pos

                if self.up:

                    self.sword.x = self.x 
                    self.sword.y = self.y -.5*self.size
                    sword_pos = self.x, (self.y -SWORD_WIDTH)
                     
                if self.down:
                    self.sword.x = self.x
                    self.sword.y = self.y + .5*self.size
                    sword_pos = self.x, (self.y +SWORD_WIDTH)
                    
                if self.right:
                    self.sword.x = self.x + .5*self.size
                    self.sword.y = self.y 
                    sword_pos = (self.x+SWORD_WIDTH), self.y
                    
                if self.left:
                    self.sword.x = self.x -.5*self.size
                    self.sword.y = self.y             
                    sword_pos = (self.x - SWORD_WIDTH), self.y                

#TODO Create Board Mapping function                 

player = Link()
sword = Sword(player)
player.sword = sword

def room_1():
    global LOCKED
    LOCKED = False 
    door = DOOR    
    locked = random.randint(0,10)
    if locked > 8:
        LOCKED = True
        door = LOCKED_DOOR  

    open_coords = []
    wall_roll = random.randint(0,10)
    if wall_roll >5:
        walltype = Tree
    if wall_roll <=5:
        walltype = Mountain

    wallsize = 50
    #wall size customization
    wall_thickness = random.randint(1,10)
    for j in range(wall_thickness):

        for i in range (2*int(WIDTH/wallsize)):
            OBJECT(i*wallsize/2, j*wallsize/2+wallsize/2, walltype, wallsize)
        
            
        for i in range (2*int(WIDTH/wallsize)):
            OBJECT(i*wallsize/2, HEIGHT- j*wallsize/2-wallsize/2, walltype, wallsize)
            
        #only create outer side walls if thickness is small, otherwise, exits on sides
        if wall_thickness <2:
        
            for i in range (2*int(HEIGHT/wallsize)):
                OBJECT(j*wallsize/2+wallsize/2, HEIGHT - i*wallsize/2, walltype, wallsize)    
                OBJECT(WIDTH-wallsize/2-j*wallsize/2, HEIGHT - i*wallsize/2, walltype, wallsize)
       
    #Doors...only top and bottom doors if thickness is under certain size
    
    if wall_thickness <4:

        OBJECT (WIDTH/2, wall_thickness*wallsize/2, door, 100, door=True)
        
        OBJECT (WIDTH/2, HEIGHT-wall_thickness*wallsize/2, door, 100, door=True)    
    
    OBJECT (0, HEIGHT/2, door, 100, door=True)
    
    OBJECT (WIDTH, HEIGHT/2 , door, 100, door=True)

    #TODO set up enemies with remaining space
    ##############################################
    upper_horiz_bound = 25+(wall_thickness-1)*.5*wallsize
    lower_horiz_bound = HEIGHT-25 - (wall_thickness-1)*.5*wallsize
    left_x = 75
    right_x = WIDTH-75
    room_edges[0]= upper_horiz_bound
    room_edges[1] = lower_horiz_bound

    

    #Enemy placement
    enemies = random.randint(3,5)
    rows = random.randint(1,2)
    for i in range(enemies):
        
        Enemy(left_x+100+i*(WIDTH/enemies),upper_horiz_bound+100, ghost, 'ghost',100)
    if rows >1:
        for i in range(enemies):
        
            Enemy(left_x+100+i*(WIDTH/enemies),lower_horiz_bound-100, ghost, 'ghost',100)
    object_roll = random.randint(0,10)
    if object_roll >5:
        objecttype = Tree
    if object_roll <=5:
        objecttype = Mountain
    #tree/mountain placement
    Objects = [3,5]
    a = random.randint(0,1)
    Objects = Objects[a]
    Rows = 3
    for j in range(Rows):
        for i in range(Objects):
            if upper_horiz_bound+200*(j+1) < lower_horiz_bound:
                if left_x+188+i*WIDTH/Objects < right_x - 188:

                
                    OBJECT(left_x+226+i*WIDTH/Objects, upper_horiz_bound+165*(j+1), objecttype, 50)
                      
    
    #resetting projectile list
    global projectile_list
    projectile_list = [0]*enemy_length
    
    
    return 

#TODO room2, or room function in general to randomly create rooms 
# def create_room():


room_1()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()    
    
    if event.type == pygame.KEYDOWN:
        
        player.update()    
    #Check Link's position to see if he enters new room
    if LOCKED == False:

        if Collide(player.x, player.y, player.size, .7, 0, Door_Coords):
            
            Coord_List.clear()
            Object_Coords.clear()
            enemy_list.clear()
            object_list.clear()
            Door_Coords.clear()
            
            
            
            if player.y <2*player.size:
                player.x = WIDTH/2
                player.y = room_edges[1]-2.9*player.size 
            elif player.y > HEIGHT - 2*player.size:
                player.x = WIDTH/2
                player.y = room_edges[0]+2.9*player.size 
            elif player.x < 2*player.size:
                player.x = WIDTH - 2.1*player.size
                player.y = HEIGHT/2
            else:
                player.x = 2.1*player.size
                player.y = HEIGHT/2

            Object_Coords.append((player.x, player.y))            
            enemy_length = 0
            enemy_index = 0
            
            room_1()                         
    
    
    #this is the invincible check after player moves or is hit    
    if player.invincible:
        player.invincible_animation_count += 1
        if player.invincible_animation_count >= 100:
            player.invincible_animation_count = 0
            player.invincible = False

    #Placeholder for now, when he dies
    if player.health <= 0:
        sys.exit()
        
    screen.fill(GROUND_COLOR)

    Object_Coords[0] = (player.x, player.y, player.size/2)

    length = len(enemy_list)
    index = 0
    while length >0:
        curr = enemy_list[index]
        
        Coord_List[index] =  (curr.x, curr.y, curr.size/2)     
       
        index +=1
        length -=1  
    
    #implement function to create correct player image based on direction
    player.configure_direction()
    screen.blit(player.image, player.rect)

    #Sword Graphics
    sword.rect = sword.image.get_rect()
    sword.rect.center = (sword.x, sword.y)
    sword.load_sword()
    screen.blit(sword.image, sword.rect)
    sword.x = -1000
    sword.y = -1000

    #This is the invincible check when a player is not moving, to prevent
    # Staying inside the enemy object without taking damage
    player.non_moving_check()
    
    #Create projectile objects and update all enemy movement
    counter = 0
    for enemy in enemy_list:
                    
        if enemy.shooting == False:

            if enemy.get_coords_projectile(player):

                coords = enemy.get_coords_projectile(player)
                
                if randomize(7)==True:
                    

                    weapon = Projectile(coords[0], coords[1], Enemy_Weapon, coords[2], enemy.index)
                    projectile_list[enemy.index]= weapon
                    enemy.shooting= True 
          

        Collision = False 
        enemy_hit = False
        
        pos_1 = []        
        pos = (enemy.x, enemy.y, enemy.size/2)
        pos_1.append(pos)

        if Collide(sword_pos[0], sword_pos[1], 75,0,0, pos_1)==True:
                        

            enemy_new_x = enemy.x
            enemy_new_y = enemy.y

            if player.up == True:
                enemy_new_y -= enemy.speed *30
            if player.down == True:
                enemy_new_y += enemy.speed *30
            if player.right == True:
                enemy_new_x += enemy.speed *30
            if player.left == True:
                enemy_new_x -= enemy.speed *30
                
                #if projected coordinates from sword bounceback do not hit walls
            if enemy_new_y < HEIGHT-enemy.size and enemy_new_y >0+enemy.size \
                and enemy_new_x < WIDTH - enemy.size and enemy_new_x >0 + enemy.size:
                
                #Compare knockback all objects except Link
                if Collide(enemy_new_x, enemy_new_y, enemy.size, .3, 1, Object_Coords)==True:
                
                    Collision = True 

                    #Compare knockback to other enemies
                if Collide(enemy_new_x, enemy_new_y, enemy.size, .3, 0, Coord_List)== True:
                
                    Collision = True 

                if Collision == False:
                    enemy.x = enemy_new_x
                    enemy.y = enemy_new_y
                    # print(enemy.x, enemy.y)
                    screen.blit(enemy.image, enemy.rect)
                
            enemy_hit = True 

        if enemy_hit == True:
            if enemy.health >0:
                
                enemy.health -=1
                                     
                    
        enemy.update()
        #invisibility loop
        if enemy.invis_count == 0:

            if enemy.health >0:
                if enemy.invisible == True:
                    a = randomize(9)
                    b = randomize(9)
                    c = randomize(9)
                    if a ==True and b == True and c ==True :
                            #initiate invisibility
                            enemy.invis_count +=1                        
                    else:
                        screen.blit(enemy.image, enemy.rect)
                else:
                    screen.blit(enemy.image, enemy.rect)
        
        if enemy.invis_count >0:
            enemy.invis_count +=1
            if enemy.invis_count ==40:
                enemy.invis_count = 0             

        
        
        if enemy.health <=0:
           
            #take off board if health goes to 0
            enemy.x = -1000
            enemy.y = -1000            
        
        #Check to see if locked doors can open once all enemies are dead        
        
        if LOCKED ==True:

            if enemy.x==-1000:
                if enemy.y == -1000:
                    counter +=1       
        
            door_convert = 0 
            if counter == len(enemy_list):
                LOCKED = False
                for x in Door_Coords:
                    
                    OBJECT(x[0], x[1], DOOR, 100, door=True)
                    door_convert+=1
                    if door_convert >10:
                        break
                break              

    sword_pos = sword.x, sword.y 
    
    for x in object_list:
        screen.blit(x.image, x.rect)
    
    #Projectile update and Projectile Collision check 
    for x in projectile_list:
        if isinstance(x, Projectile):
            screen.blit(x.image, x.rect)
            
            pos_1 = []        
            pos = (player.x, player.y, player.size/2)
            pos_1.append(pos)
            if Collide(x.x, x.y, x.size, .3, 0, pos_1)==True:
                player.health -=.01

            x.x, x.y = x.move_projectile()

            weapon = Projectile(x.x, x.y, Enemy_Weapon, x.direction, x.index)
            if weapon.x < WIDTH -weapon.size and weapon.x > 0+weapon.size and weapon.y >0+weapon.size and weapon.y < HEIGHT-weapon.size:
                
                projectile_list[x.index]= weapon
            else:
                projectile_list[x.index]= 0
                enemy_list[x.index].shooting = False 
           

    font = pygame.font.SysFont("comicsans", 40, True)    
    text = font.render(f'Health Remaining: {round(player.health,2)}', 1, RED) # Arguments are: text, anti-aliasing, color
    screen.blit(text, (10, 10))    

    pygame.display.flip()

