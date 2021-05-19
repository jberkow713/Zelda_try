
import pygame
import random
import sys
from pygame.locals import(
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_ESCAPE, KEYDOWN, QUIT
)
size = width, height = 1500, 1050
positionx = size[0] *.5
positiony = size[1] *.5
position = (positionx, positiony)

black = (0,0,0)
blue = (0,0,255)
turquoise= (0,255,255)
white = (255,255,255)


RESCALE_WIDTH = 100
RESCALE_HEIGHT = 100

pygame.init()

def random_position(number, screen_width, screen_height, obj_width, obj_height, Links_position, Links_size):
    '''
    Creates random x,y coordinate positioning for enemies, using board size and link's coordinates
    so as not to overlap Link...can overlap other creatures possibly
    '''
    list_of_dragons = []
    for i in range(number):
        possible_width = screen_width - obj_width
        possible_height = screen_height - obj_height


        link_x_left_bound = Links_position[0]- .5*Links_size
        link_x_right_bound = Links_position[0] +.5*Links_size
        link_y_low_bound = Links_position[1]- .5*Links_size
        link_y_upper_bound = Links_position[1] +.5*Links_size
        
        outside_link_x = False

        while outside_link_x == False:
            rand_x = random.randint(0, possible_width)
            
            if rand_x <link_x_left_bound or rand_x > link_x_right_bound:
                slightly_rand_x = rand_x
            
                outside_link_x = True

        outside_link_y = False
        while outside_link_y == False:
            rand_y = random.randint(0, possible_height)

            if rand_y < link_y_low_bound or rand_y> link_y_upper_bound:
                slightly_rand_y = rand_y
                
                outside_link_y = True
        list_of_dragons.append((slightly_rand_x, slightly_rand_y))        
    
    #[(184, 378), (903, 102), (394, 132), (531, 215), (694, 871)]
    #[(0, (184, 378)), (1, (903, 102)), (2, (394, 132)), (3, (531, 215)), (4, (694, 871))]

    updated_list_of_dragons = []
    
    length = len(list_of_dragons)
    index = 0
    while length >0:
        enumerated = list(enumerate(list_of_dragons))
        x_indices = []
        y_indices =[]
        x_val = list_of_dragons[index][0]
        y_val = list_of_dragons[index][1]

        for x in enumerated:
            if x[0] != index:
                x_indices.append(x[1][0])
                y_indices.append(x[1][1])
        
        x_distance = False 
        y_distance = False
        x_count = 0

        for x in x_indices:
            if abs(x_val-x)> obj_width:
                x_count +=1
        if x_count == len(x_indices):
            x_distance = True
        
        if x_distance == True:


            y_count = 0

            for x in y_indices:
                if abs(y_val-x)> obj_height:
                    y_count +=1
            if y_count == len(y_indices):
                y_distance = True

        if x_distance == True and y_distance == True:
            new_coord = (x_val, y_val)
            updated_list_of_dragons.append(new_coord)

        if x_distance == False or y_distance == False:
            updated_dist = 10000*index 
            list_of_dragons[index] = (updated_dist,updated_dist)
        

        index +=1
        length -=1    
    

    return updated_list_of_dragons


def check_coordinates(positionx, positiony, board_width, board_height, obj_width, obj_height):
    '''
    Takes in given object and makes sure it's position is not off edge of board
    '''
    
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

screen = pygame.display.set_mode(size)
link = pygame.image.load("link.jpg").convert_alpha()
link = pygame.transform.scale(link, (RESCALE_WIDTH, RESCALE_HEIGHT))
player = link.get_rect(topleft=position)
#Setting player's position in center of map
link_pos = []
link_pos.append(position)


dragon = pygame.image.load('Dragon.jpg').convert_alpha()
dragon = pygame.transform.scale(dragon, (75, 75))

at_least_5 = False
while at_least_5 == False:

    dragon_positions = random_position(20,width, height, 75,75, position, RESCALE_WIDTH)
    
    if len(dragon_positions)>=5:
        at_least_5 = True

dragon_list = []
for x in dragon_positions:
    dragon_list.append(x)
#TODO create the movement of the dragons or creatures, each needs to be separate, need 
#hitboxes so they bounce off each other

SPEED = 1
secondary_list = []
horizontal = [[SPEED,0], [-SPEED,0],[1]]
vertical = [[0,SPEED],[0,-SPEED],[1]]

length =len(dragon_list)
index = 0
while length >0:

    if index %2 == 0:
        secondary_list.append(horizontal)
    if index %2 ==1:
        secondary_list.append(vertical)

    index +=1
    length -=1



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
                
                positiony = coords[1]
                position = (coords[0], coords[1])
                link_pos.append(position)
                
                player = link.get_rect(topleft=position)

                
                
                
            
            if event.key == pygame.K_LEFT:
                positionx -=50
                
                coords = check_coordinates(positionx, positiony, width, height, RESCALE_WIDTH, RESCALE_HEIGHT)
                
                positionx = coords[0]
                position = (coords[0], coords[1])
                player = link.get_rect(topleft=position)
                link_pos.append(position)

                
                            
            if event.key == pygame.K_RIGHT:
                positionx +=50
                
                coords = check_coordinates(positionx, positiony, width, height, RESCALE_WIDTH, RESCALE_HEIGHT)
                
                positionx = coords[0]
                position = (coords[0], coords[1])
                player = link.get_rect(topleft=position)
                link_pos.append(position)

                
                

            if event.key == pygame.K_UP:
                positiony -=50
                
                coords = check_coordinates(positionx, positiony, width, height, RESCALE_WIDTH, RESCALE_HEIGHT)
                
                positiony = coords[1]
                position = (coords[0], coords[1])
                player = link.get_rect(topleft=position)
                link_pos.append(position)

          
                                 
    
    screen.fill(white)
    #blit takes an object, and puts it on a surface
    #player in this case creates a rectangle object
    #the ball is then put onto this surface
    
    screen.blit(link, player)
    
    #Creating dictionary of dragons and their possible movement patterns as coordinates are updated
    #We use the secondary list of speeds, and triggers, to determine the movement of a dragon in the list
    DRAGON_dict = dict(zip(dragon_list,secondary_list))
    
    to_avoid_x = []
    for x in dragon_list:
        to_avoid_x.append(x[0])
    to_avoid_x.append(link_pos[-1][0])

    to_avoid_y = []
    for x in dragon_list:
        to_avoid_y.append(x[1])
    to_avoid_y.append(link_pos[-1][1])        
       
    checked_x = []
    checked_y = []   
    
    
    length = len(dragon_list)
    index = 0
    

    while length >0:
        horizontal = [[SPEED,0], [-SPEED,0],[1]]
        vertical = [[0,SPEED],[0,-SPEED],[1]]
        horizontal_reversed = [[SPEED,0], [-SPEED,0],[-1]]
        vertical_reversed = [[0,SPEED],[0,-SPEED],[-1]] 

        secondary_position = secondary_list[index]
        #creating additional coordinates to avoid based on other enemies and player objects
        avoided_x_enumerated = list(enumerate(to_avoid_x))
        avoided_y_enumerated = list(enumerate(to_avoid_y))
        
        for x in avoided_x_enumerated:
            if x[0]!= index:
                checked_x.append(x[1])
        for x in avoided_y_enumerated:
            if x[0]!= index:
                checked_y.append(x[1])        
        
        to_check_dict = dict(zip(checked_x, checked_y))
        # print(to_check_dict)

        position = dragon_list[index]

        

        for k,v in DRAGON_dict.items():
            if position == k:
                
                if v[2][0]== 1:
                            
                    new_x = position[0]+v[0][0]
                    new_y = position[1] + v[0][1]
                
                elif v[2][0]== -1:
                    
                    new_x = position[0]+ v[1][0]
                    new_y = position[1] + v[1][1]

                coords = check_coordinates(new_x, new_y, width, height, 75,75)

        Coords_Checked = False 
        #Begin Collision Checking, wall checking, etc...                   
                
        if Coords_Checked == False:
            #Wall Check

            if coords[0]==0 or coords[0]==(width-75) \
                or coords[1]==0 or coords[1]==(height-75):
                    
                if secondary_position == horizontal:
                    secondary_list[index] = horizontal_reversed
                elif secondary_position == horizontal_reversed:
                    secondary_list[index] = horizontal
                elif secondary_position == vertical:
                    secondary_list[index] = vertical_reversed
                elif secondary_position == vertical_reversed:
                    secondary_list[index] = vertical        
                
                
                Coords_Checked = True 
        
        
        if Coords_Checked == False:
            #Check to see if two enemies are overlapping or started overlapping
            for k,v in to_check_dict.items():
                
                Close = False 
                if abs(coords[0]-k) <76:
                    if abs(coords[1]-v) <76:
                        Close = True 
                if abs(coords[1]-v) <76:
                    if abs(coords[0]-k) <76:
                        Close = True 

                if Close == True:
                        


                    possible = [horizontal, horizontal_reversed, vertical, vertical_reversed]    
                    rand = random.randint(0,3)
                    
                    secondary_list[index] = possible[rand]  
                                            
                    Coords_Checked = True
               

        if Coords_Checked == False:
            for k,v in to_check_dict.items():
                if k != 0 and v !=0:
                    #you need to create variables there that represent the size of the creature, versus
                    # the size of the map...
                    # in this case, the x size of the map, or width, is 1500, and the dragon is 75
                    # so this represents .05 of the map, hence, k >.95, means that the dragon will change
                    # direction on the x axis, right before it overlaps another dragon
                    # 
                    # Same can be said about the y axis, and you can air on the side of caution in that
                    # you have them split maybe a bit early, to avoid overlap
                    # 
                    # This mapping will ensure that basically there is no overlap, if there is no starting
                    # overlap        
                    Close = False 
                    
                    if coords[0]/k >.88 and coords[0]/k < 1:
                        if coords[1]/v >.88 and coords[1]/v <1:
                            Close = True

                    if coords[1]/v >.88 and coords[1]/v <1:
                        if coords[0]/k >.88 and coords[0]/k < 1:
                            Close = True 

                    if Close == True:

                        
                        possible = [horizontal, horizontal_reversed, vertical, vertical_reversed]    
                        rand = random.randint(0,3)
                        
                        secondary_list[index] = possible[rand]  
                                                
                        Coords_Checked = True

                               
        
        if Coords_Checked == False:

            # if coords[0]>0 and coords[0]< width-75 and coords[1]>0 and coords[1]< height-75:
            secondary_list[index]= secondary_position
                  




               
        
        x = (coords[0], coords[1])
        
        dragon_list[index] = x
        dragon_rect = dragon.get_rect(topleft=x) 
        screen.blit(dragon, dragon_rect)
        index +=1
        length -=1
        #clear lists so next value has empty list to append to
        checked_x.clear()
        checked_y.clear()

        
    
    
    pygame.display.flip()
