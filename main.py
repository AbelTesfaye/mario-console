import msvcrt
import os
from time import sleep



MAX_WORLD_WIDTH=80
MAX_WORLD_HEIGHT=25


MARIO_LOCATION_X=0
MARIO_LOCATION_Y=0

LAST_PRESSED_KEY=b''

CHARACTER_MARIO_REPLACED=''


WORLD_MAP=[
"                                                                               ",
"                                                                               ",
"                                                                               ",
"                                                                               ",
"                                                                               ",
"                                                                               ",
"                                                                               ",
"                                                                               ",
"                                                                               ",
"                                               |||                             ",
"                                           __||||||||||||                      ",  
"              ||||||||                     ||       ||                         ",
"|||||||||||||||      |||||||||||||||||||||||||||||||||||||||_______________    "
]

MARIO_SPRITE=[
" ▄████▄▄",
"▄▀█▀▐└─┐",
"█▄▐▌▄█▄┘",
"└▄▄▄▄▄┘ ",
"██▒█▒██ ",
]

MARIO_SPRITE_X=len(MARIO_SPRITE[0])
MARIO_SPRITE_Y=len(MARIO_SPRITE)

AREA_MARIO_REPLACED=list()
def print_world(world):
    for line in world:
        print(line)


def check_the_world(world):
    for i in range(1,len(WORLD_MAP)):
        #check if all lines are the same size
        
        if(len(world[i]) != len(world[i-1])):
            print("Line size not equal at line:",i,"and",i-1)




def create_2d_mario(x,y):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global AREA_MARIO_REPLACED

    

    for i in range(MARIO_SPRITE_Y):
        AREA_MARIO_REPLACED.append(WORLD_MAP[y-i][x-MARIO_SPRITE_X:x])

        WORLD_MAP[y-i]=WORLD_MAP[y-i][:x-MARIO_SPRITE_X]+ MARIO_SPRITE[MARIO_SPRITE_Y-i-1] +WORLD_MAP[y-i][x:]

    
    MARIO_LOCATION_X=x
    MARIO_LOCATION_Y=y




def delete_2d_mario(x,y):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global CHARACTER_MARIO_REPLACED

    for i in range(MARIO_SPRITE_Y):
        WORLD_MAP[y-i]=WORLD_MAP[y-i][:x-MARIO_SPRITE_X]+ AREA_MARIO_REPLACED[i] +WORLD_MAP[y-i][x:]

    AREA_MARIO_REPLACED.clear()
    MARIO_LOCATION_X=-1
    MARIO_LOCATION_Y=-1


def move_2d_mario(to_x,to_y):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y

    delete_2d_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y)

    #create a new mario
    create_2d_mario(to_x,to_y)
    
    MARIO_LOCATION_X=to_x
    MARIO_LOCATION_Y=to_y

def get_char_at(x,y):
    global WORLD_MAP
    return WORLD_MAP[y][x]
    
def process_key(key):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global LAST_PRESSED_KEY

    #print(LAST_PRESSED_KEY)
    #print(key)

    #left arrow
    if key == b'K':
        if not is_collided(get_characters_around_mario()[1]):
            move_2d_mario(MARIO_LOCATION_X-1,MARIO_LOCATION_Y)
        pass

    #down arrow
    elif key == b'P':
        if not is_collided(get_characters_around_mario()[0]):
            move_2d_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y+1)
        pass
    
    #up arrow
    elif key == b'H':
        if not is_collided(get_characters_around_mario()[2]):
            move_2d_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y-1)

        pass
    
    #right arrow
    elif key == b'M':
        if not is_collided(get_characters_around_mario()[3]):
            move_2d_mario(MARIO_LOCATION_X+1,MARIO_LOCATION_Y)

        pass
    
    LAST_PRESSED_KEY=key

def get_characters_around_mario():
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global MARIO_SPRITE_X
    global MARIO_SPRITE_Y

    characters_below_mario=list()
    for i in range(MARIO_LOCATION_X-MARIO_SPRITE_X,MARIO_LOCATION_X):
        characters_below_mario.append(get_char_at(MARIO_LOCATION_X-MARIO_SPRITE_X+(i-(MARIO_LOCATION_X-MARIO_SPRITE_X)),MARIO_LOCATION_Y+1))

    characters_above_mario=list()
    for i in range(MARIO_LOCATION_X-MARIO_SPRITE_X,MARIO_LOCATION_X):
        characters_above_mario.append(get_char_at(MARIO_LOCATION_X-MARIO_SPRITE_X+(i-(MARIO_LOCATION_X-MARIO_SPRITE_X)),MARIO_LOCATION_Y-MARIO_SPRITE_Y))

    characters_left_of_mario=list()
    for i in range(MARIO_SPRITE_Y):
        characters_left_of_mario.append(get_char_at(MARIO_LOCATION_X-MARIO_SPRITE_X-1,MARIO_LOCATION_Y-i))

    characters_right_of_mario=list()
    for i in range(MARIO_SPRITE_Y):
        characters_right_of_mario.append(get_char_at(MARIO_LOCATION_X,MARIO_LOCATION_Y-i))

    return [characters_below_mario,characters_left_of_mario,characters_above_mario,characters_right_of_mario]

def is_collided(char_list):
    for i in range(len(char_list)):
        print(char_list,char_list[i],len(char_list))
        if char_list[i] != ' ':
            return True
    return False
    


check_the_world(WORLD_MAP)    
#create_mario(0,0)

create_2d_mario(15,5)

while True:
    get_characters_around_mario()
    sleep(0.1)
    os.system('cls')
    
    print ("running")
    print_world(WORLD_MAP)

    move_2d_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y+1)
    
    if msvcrt.kbhit():
        process_key(msvcrt.getch())
        
