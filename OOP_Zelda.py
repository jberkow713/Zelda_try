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
    def __init__(self,x,y, image):
        
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
        for x in Big_List:
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

class Link:
    def __init__(self):
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
        self.health = 6
        self.down = True #link faces down by default
        self.up = False
        self.left = False
        self.right = False
        self.ring = None 
        Links_Pos.append(self.rect.center)
        Object_Coords.append((self.x, self.y))
    
    def coords_to_avoid(self, coord):
        #When Link is not invincible, makes sure he does not move over objects, or enemies
        #True if run into object, 
        #99 if not run into object but run into enemy
        #False if not run into any of them
              
        Enemy_COORD_List = []
        Object_Coord_List = []

        curr = (self.x, self.y, self.size/2)
     
        for x in Coord_List:
            Enemy_COORD_List.append(x)
        
        for x in Object_Coords:
            if x != curr:
                Object_Coord_List.append(x)

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
            
            if self.x >=x_range[0]-(.6*self.size) and self.x <= x_range[1]+(.6*self.size):
                if self.y >= y_range[0]-(.6*self.size) and self.y <= y_range[1]+(.6*self.size):
                    if self.invincible == False:

                        self.health -=.01
                        self.health = round(self.health,2)
                        if self.health <=0:
                            print('Game Over')

                            return sys.exit() 
        return
    
    def player_enemy_collision(self):
        #Checks only player against enemy units
        Obj_Coords = []
        curr = (self.new_x, self.new_y, self.size/2)    
                                
        for x in Object_Coords:
            if x != curr:
                Obj_Coords.append(x)
        
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
                        self.set_player_direction('UP')
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
                        self.set_player_direction('DOWN')  
                    
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
                        self.set_player_direction('RIGHT')
                    
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
                        self.set_player_direction('LEFT')
                    
                    if self.coords_to_avoid((self.new_x, self.new_y)) == False:

                        self.x = self.new_x
                        self.y = self.new_y  
                        self.set_player_direction('LEFT')  
                            
player = Link()

enemy1 = Enemy(250,250, ghost)
enemy2 = Enemy(1250,250,ghost)
enemy3 = Enemy(250,750,ghost)
enemy4 = Enemy(1250,750,ghost)
enemy5 = Enemy(1000, 250,ghost)
enemy6 = Enemy(1000, 500,ghost)
Tree1 = OBJECT(500,500, Tree, 50)
Tree2 = OBJECT(550,500, Tree, 50)
Tree3 = OBJECT(605,555, Tree, 50)
Tree4 = OBJECT(625,355, Mountain, 50)
Tree5 = OBJECT(50,50, Mountain, 150)
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
    
    screen.blit(player.image, player.rect)
    #This is the invincible check when a player is not moving, to prevent
    # Staying inside the enemy object
    player.non_moving_check()
        
    for x in enemy_list:
                
        if randomize() == True:
            
            x.update()

        screen.blit(x.image, x.rect)

    for x in object_list:
        screen.blit(x.image, x.rect)
    
    
    pygame.display.flip()

