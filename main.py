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
"                                               |||                             ",
"                                           __|||||||||||||||||||||||||||||     ",
"              ||||||||                     ||       ||                         ",
"|||||||||||||||      |||||||||||||||||||||||||||||||||||||||_______________    "
]
def print_world(world):
    for line in world:
        print(line)


def check_the_world(world):
    for i in range(1,len(WORLD_MAP)):
        #check if all lines are the same size
        
        if(len(world[i]) != len(world[i-1])):
            print("Line size not equal at line:",i,"and",i-1)



#Dear Mario,
#keep going down, until you hit the ground,
def create_mario(x,y):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global CHARACTER_MARIO_REPLACED

    CHARACTER_MARIO_REPLACED=WORLD_MAP[y][x]

    temp_map_line=WORLD_MAP[y][:x]+'M'+WORLD_MAP[y][x+1:]

    WORLD_MAP[y]=temp_map_line
    MARIO_LOCATION_X=x
    MARIO_LOCATION_Y=y
    
def delete_mario(x,y):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global CHARACTER_MARIO_REPLACED

    temp_map_line=WORLD_MAP[y][:x]+CHARACTER_MARIO_REPLACED+WORLD_MAP[y][x+1:]
    
    WORLD_MAP[y]=temp_map_line
    MARIO_LOCATION_X=-1
    MARIO_LOCATION_Y=-1

def move_mario(to_x,to_y):
    #Delete (replace by ' ') old mario
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y

    if in_game_world(to_y) and (not is_rigid(to_x,to_y)):
        delete_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y)

        #create a new mario
        create_mario(to_x,to_y)
        MARIO_LOCATION_X=to_x
        MARIO_LOCATION_Y=to_y


def is_rigid(x,y):
    char=get_char_at(x,y)

    if(char=='|'):
        return True
    else:
        return False


def get_char_at(x,y):
    global WORLD_MAP
    return WORLD_MAP[y][x]
    
def process_key(key):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global LAST_PRESSED_KEY

    print(LAST_PRESSED_KEY)
    print(key)

    #left arrow
    if key == b'K':
        move_mario(MARIO_LOCATION_X-2,MARIO_LOCATION_Y)
        pass

    #down arrow
    elif key == b'P':
        move_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y+2)
        pass
    
    #up arrow
    elif key == b'H':
        move_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y-6)

        pass
    
    #right arrow
    elif key == b'M':
        move_mario(MARIO_LOCATION_X+2,MARIO_LOCATION_Y)

        pass
    
    LAST_PRESSED_KEY=key




def in_game_world(y):
    global WORLD_MAP
    if(y<=(len(WORLD_MAP)-1) and y>=0):
        return True
    else:
        return False
    

check_the_world(WORLD_MAP)    
create_mario(0,0)
while True:
    sleep(0.1)
    os.system('cls')
    
    print ("running")
    
    print_world(WORLD_MAP)

    move_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y+1)
    
    if msvcrt.kbhit():
        process_key(msvcrt.getch())
        
