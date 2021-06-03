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




ghost = pygame.image.load("ghost.png").convert_alpha()
ghost = pygame.transform.scale(ghost, (GHOST_WIDTH, GHOST_HEIGHT))

Tree = pygame.image.load('TREE_PNG.png')
Mountain = pygame.image.load('MOUNTAIN_PNG.png')
#list for enemy collision checking
Coord_List = []
Object_Coords = []
#list for enemy movement
enemy_list = []
object_list = []

#TODO IMPLEMENT ATTACKING, need 4 photos of link and sword, trigger certain photos baed on if self is up, down , left, right

class OBJECT:
    def __init__(self, x, y, image, size):
        self.x = x
        self.y = y
        self.size = size 
        self.image = image
        # We set image so it ignores background of white
        self.image.set_colorkey(WHITE) 
        self.rescale()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        Object_Coords.append((self.x, self.y, self.size/2))
        object_list.append(self)

class Enemy:
    def __init__(self,x,y, image, type):
        
        self.x = x
        self.y = y
        self.invisible = False
        self.create_stats()
        self.size = 100
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.direction = None 
        self.movement = ['up', 'down', 'left', 'right']
        enemy_list.append(self)
        Coord_List.append((self.x, self.y))
        self.type = type 
        self.health = self.get_health()
        self.hit = False  

    def get_health(self):
        health_dict = {'ghost': 120, 'dragon':1000, 'centaur':300}
        for k,v in health_dict.items():
            if self.type == k:
                return v


    def create_stats(self):
        
        self.speed = random.randint(5,7)
        self.aggressiveness = random.randint(2,5)
        invis_roll = random.randint(0,10)
        if invis_roll > 7:
            self.invisible = True 
        
    def coords_to_avoid(self, coord):
        #Start with a list of all other enemies, and eventually objects,  that exist on the map
                
        COORD_List = []
        curr = (self.x, self.y, self.size/2)
        Big_List = Coord_List + Object_Coords
        COORD_List = [x for x in Big_List if x!= curr]
                       
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
            

            if coord[0] >=x_range[0]-(.3*self.size) and coord[0] <= x_range[1]+(.3*self.size):
                if coord[1] >= y_range[0]-(.3*self.size) and coord[1] <= y_range[1]+(.3*self.size):
                    return True 
        
        return False
               
        
    def update(self):
        #Update enemy position
        
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
        #True if run into object, 
        #99 if not run into object but run into enemy
        #False if not run into any of them
        
        curr = (self.x, self.y, self.size/2)      
        Enemy_COORD_List = [x for x in Coord_List]
        Object_Coord_List = [x for x in Object_Coords if x != curr]
        
        for x in Object_Coord_List:
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
            
            if coord[0] >=x_range[0]-(.3*self.size) and coord[0] <= x_range[1]+(.3*self.size):
                if coord[1] >= y_range[0]-(.3*self.size) and coord[1] <= y_range[1]+(.3*self.size):
                    return True 
        
        for x in Enemy_COORD_List:
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

            if coord[0] >=x_range[0]-(.3*self.size) and coord[0] <= x_range[1]+(.3*self.size):
                if coord[1] >= y_range[0]-(.3*self.size) and coord[1] <= y_range[1]+(.3*self.size):
                    if self.invincible == False:
                        return 99
        return False
    
    def non_moving_check(self):
        #When Link is not invincible and not moving, checks if he is inside a monster, or near a monster...
        #Sensitive range

        for x in Coord_List:
                        
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
            
            if self.x >=x_range[0]-(.35*self.size) and self.x <= x_range[1]+(.35*self.size):
                if self.y >= y_range[0]-(.35*self.size) and self.y <= y_range[1]+(.35*self.size):
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
                
        for x in Obj_Coords:
              
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
            
            if self.new_x >=x_range[0]-(.3*self.size) and self.new_x <= x_range[1]+(.3*self.size):
                if self.new_y >= y_range[0]-(.3*self.size) and self.new_y <= y_range[1]+(.3*self.size):                                                           
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
                
                
                
player = Link()
sword = Sword(player)
player.sword = sword

enemy1 = Enemy(250,250, ghost, 'ghost')
enemy2 = Enemy(1250,250,ghost, 'ghost')
enemy3 = Enemy(250,750,ghost, 'ghost')
enemy4 = Enemy(1250,750,ghost, 'ghost')
enemy5 = Enemy(1000, 250,ghost, 'ghost')
enemy6 = Enemy(1000, 500,ghost, 'ghost')
Tree1 = OBJECT(500,500, Tree, 50)
Tree2 = OBJECT(550,500, Tree, 50)
Tree3 = OBJECT(605,555, Tree, 50)
Tree4 = OBJECT(625,355, Mountain, 50)
# Tree5 = OBJECT(50,50, Mountain, 150)
Tree6 = OBJECT(900,900, Mountain, 150)


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    

    if event.type == pygame.KEYDOWN:
        
        player.update()
        
    #this is the invincible check after player moves or is hit
    
    if player.invincible:
        player.invincible_animation_count += 1
        if player.invincible_animation_count >= 100:
            player.invincible_animation_count = 0
            player.invincible = False

          
    #Placeholder for now, when he dies
    if player.health == 0:
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
    

    #implement function to create correct image based on direction

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
    # Staying inside the enemy object
    player.non_moving_check()

        
    for enemy in enemy_list:
                        
        enemy_hit = False
                
        pos = (enemy.x, enemy.y, enemy.size/2)
        x_range = []
        y_range = []
        left_x = pos[0] - pos[2]
        right_x = pos[0] + pos[2]
        high_y = pos[1] - pos[2]
        low_y = pos[1] + pos[2]
        x_range.append(left_x)
        x_range.append(right_x)
        y_range.append(high_y)
        y_range.append(low_y)
        
        if sword_pos[0] >=x_range[0] and sword_pos[0] <= x_range[1]:
            if sword_pos[1] >= y_range[0] and sword_pos[1] <= y_range[1]:
                enemy_hit = True 

            if enemy_hit == True:
                
                enemy.health -=1
                #TODO implement enemy knockback from weapons, etc        
                

        if randomize() == True:
            
            enemy.update()

        #Sword/Weapon Interaction with enemies

        if enemy.health >0:
           
            screen.blit(enemy.image, enemy.rect)

        if enemy.health <=0:
            #take off board if health goes to 0
            enemy.x = -1000
            enemy.y = -1000

    for x in object_list:
        screen.blit(x.image, x.rect)
    font = pygame.font.SysFont("comicsans", 40, True)
    
    text = font.render(f'Health Remaining: {round(player.health,2)}', 1, RED) # Arguments are: text, anti-aliasing, color
    screen.blit(text, (10, 10))
    

    pygame.display.flip()

