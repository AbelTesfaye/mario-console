import msvcrt
import os
from time import sleep
import winsound
import pyglet
sound_stomp = pyglet.media.load('sounds/smb_stomp.wav',streaming=False)
sound_mariodie = pyglet.media.load('sounds/smb_mariodie.wav',streaming=False)
sound_jump = pyglet.media.load('sounds/smb_jump-small.wav',streaming=False)
sound_theme = pyglet.media.load('sounds/01-main-theme-overworld.wav',streaming=False)

ENEMIES_KILLED=0
LIVES_LEFT=3

WON=False
bg_player=pyglet.media.Player()
bg_player.queue(sound_theme)
bg_player.eos_action = pyglet.media.SourceGroup.loop

MAX_WORLD_WIDTH=80-1
MAX_WORLD_HEIGHT=25

MARIO_LOCATION_X=0
MARIO_LOCATION_Y=0
MARIO_ALIVE = True
MARIO_CAN_DOUBLE_JUMP = True
MARIO_JUMPED_ONCE = True

ENEMY_LOCATION_X=0
ENEMY_LOCATION_Y=0
ENEMY_SHOULD_MOVE_TO_RIGHT=False

LAST_PRESSED_KEY=b''

CHARACTER_MARIO_REPLACED=''


WORLD_MAP=list()
def prepare_world():
    global WORLD_MAP
    with open('1-1.txt') as f:
        WORLD_MAP = f.read().splitlines()
        
        
prepare_world()


WORLD_MAP_WIDTH=0
WORLD_MAP_HEIGHT=0

MARIO_SPRITE=[
" ▄████▄▄",
"▄▀█▀▐└─┐",
"█▄▐▌▄█▄┘",
"└▄▄▄▄▄┘ ",
"██▒█▒██ ",
]

MARIO_SPRITE_WIDTH=len(MARIO_SPRITE[0])
MARIO_SPRITE_HEIGHT=len(MARIO_SPRITE)

ENEMY_SPRITE=[
"  ▓▓▓   ",
" ▓▒▓▒▓  ",
"▓▓▓▓▓▓▓ ",
" █████  ",
"▒▒███▒▒▒"
]

ENEMY_SPRITE_WIDTH=len(ENEMY_SPRITE[0])
ENEMY_SPRITE_HEIGHT=len(ENEMY_SPRITE)

AREA_MARIO_REPLACED=list()
AREA_ENEMY_REPLACED=list()


#prints world into cmd
def print_world(world):
    for line in world:

        camera_trigger_index=20
        if MARIO_LOCATION_X >camera_trigger_index:
            print(line[MARIO_LOCATION_X-camera_trigger_index:MARIO_LOCATION_X + (MAX_WORLD_WIDTH-camera_trigger_index)])
        else:
            print(line[:MAX_WORLD_WIDTH])

            
#cleans screen and prints world           
def refresh_screen():
    global ENEMIES_KILLED
    global LIVES_LEFT
    
    print ((" "*3)+"Enemies killed: "+str(ENEMIES_KILLED)+(" "*15)+"[1;40;31mM[40;32mA[40;33mR[40;34mI[40;35mO [40;36mC[40;31mO[40;32mN[40;33mS[40;34mO[40;35mL[40;36mE[40;37m"+(" "*15)+"Lives left: "+str(LIVES_LEFT))
        
    print_world(WORLD_MAP)
    os.system('cls')

#checks if world is properly formated
def check_the_world():
    global WORLD_MAP_WIDTH
    global WORLD_MAP_HEIGHT

    
    for i in range(1,len(WORLD_MAP)):
        #check if all lines are the same size
        
        if(len(WORLD_MAP[i]) != len(WORLD_MAP[i-1])):
            print("Line size not equal at line:",i,"and",i-1)
            
    WORLD_MAP_WIDTH=len(WORLD_MAP[0])
    WORLD_MAP_HEIGHT=len(WORLD_MAP)


#creates mario in a world, using x and y coordinates
def create_2d_mario(x,y):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global AREA_MARIO_REPLACED

    

    for i in range(MARIO_SPRITE_HEIGHT):
        AREA_MARIO_REPLACED.append(WORLD_MAP[y-i][x-MARIO_SPRITE_WIDTH:x])

        WORLD_MAP[y-i]=WORLD_MAP[y-i][:x-MARIO_SPRITE_WIDTH]+ MARIO_SPRITE[MARIO_SPRITE_HEIGHT-i-1] +WORLD_MAP[y-i][x:]

    
    MARIO_LOCATION_X=x
    MARIO_LOCATION_Y=y

#creates enemy in a world, using x and y coordinates
def create_2d_enemy(x,y):
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global AREA_ENEMY_REPLACED

    

    for i in range(ENEMY_SPRITE_HEIGHT):
        AREA_ENEMY_REPLACED.append(WORLD_MAP[y-i][x-ENEMY_SPRITE_WIDTH:x])

        WORLD_MAP[y-i]=WORLD_MAP[y-i][:x-ENEMY_SPRITE_WIDTH]+ ENEMY_SPRITE[ENEMY_SPRITE_HEIGHT-i-1] +WORLD_MAP[y-i][x:]

    
    ENEMY_LOCATION_X=x
    ENEMY_LOCATION_Y=y

#deletes mario in a world, using x and y coordinates
def delete_2d_mario(x,y):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global CHARACTER_MARIO_REPLACED

    for i in range(MARIO_SPRITE_HEIGHT):
        WORLD_MAP[y-i]=WORLD_MAP[y-i][:x-MARIO_SPRITE_WIDTH]+ AREA_MARIO_REPLACED[i] +WORLD_MAP[y-i][x:]

    AREA_MARIO_REPLACED.clear()
    MARIO_LOCATION_X=-1
    MARIO_LOCATION_Y=-1

#deletes enemy in a world, using x and y coordinates
def delete_2d_enemy(x,y):
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global CHARACTER_ENEMY_REPLACED

    for i in range(ENEMY_SPRITE_HEIGHT):
        WORLD_MAP[y-i]=WORLD_MAP[y-i][:x-ENEMY_SPRITE_WIDTH]+ AREA_ENEMY_REPLACED[i] +WORLD_MAP[y-i][x:]

    AREA_ENEMY_REPLACED.clear()
    ENEMY_LOCATION_X=-1
    ENEMY_LOCATION_Y=-1

#checks if mario can be moved to an x,y coordinates
def can_be_moved_mario(x,y):
    if(((x-MARIO_SPRITE_WIDTH) >= 0) and (x < WORLD_MAP_WIDTH) and ((y-(MARIO_SPRITE_HEIGHT-2)) > 0) and (y<WORLD_MAP_HEIGHT-1) ) :
        return True
    return False

#checks if enemy can be moved to an x,y coordinates
def can_be_moved_enemy(x,y):
    if(((x-ENEMY_SPRITE_WIDTH) >= 0) and (x < WORLD_MAP_WIDTH) and ((y-(ENEMY_SPRITE_HEIGHT-2)) > 0) and (y<WORLD_MAP_HEIGHT-1) ) :
        return True
    return False

#moves mario in 2d dimensions
def move_2d_mario(to_x,to_y):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    if(can_be_moved_mario(to_x,to_y)):
        delete_2d_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y)

        #create a new mario
        create_2d_mario(to_x,to_y)
        
        MARIO_LOCATION_X=to_x
        MARIO_LOCATION_Y=to_y
        
#moves enemy in 2d dimensions
def move_2d_enemy(to_x,to_y):
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    if(can_be_moved_enemy(to_x,to_y)):
        delete_2d_enemy(ENEMY_LOCATION_X,ENEMY_LOCATION_Y)

        #create a new enemy
        create_2d_enemy(to_x,to_y)
        
        ENEMY_LOCATION_X=to_x
        ENEMY_LOCATION_Y=to_y

def get_char_at(x,y):
    global WORLD_MAP
    return WORLD_MAP[y][x]


    
def get_characters_around_mario():
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global MARIO_SPRITE_WIDTH
    global MARIO_SPRITE_HEIGHT
    
    characters_below_mario=list()
    for i in range(MARIO_LOCATION_X-MARIO_SPRITE_WIDTH,MARIO_LOCATION_X):
        characters_below_mario.append(get_char_at(MARIO_LOCATION_X-MARIO_SPRITE_WIDTH+(i-(MARIO_LOCATION_X-MARIO_SPRITE_WIDTH)),MARIO_LOCATION_Y+1))
    
    characters_above_mario=list()
    for i in range(MARIO_LOCATION_X-MARIO_SPRITE_WIDTH,MARIO_LOCATION_X):
        characters_above_mario.append(get_char_at(MARIO_LOCATION_X-MARIO_SPRITE_WIDTH+(i-(MARIO_LOCATION_X-MARIO_SPRITE_WIDTH)),MARIO_LOCATION_Y-MARIO_SPRITE_HEIGHT))
    
    characters_left_of_mario=list()
    for i in range(MARIO_SPRITE_HEIGHT):
        characters_left_of_mario.append(get_char_at(MARIO_LOCATION_X-MARIO_SPRITE_WIDTH-1,MARIO_LOCATION_Y-i))
    
    characters_right_of_mario=list()
    for i in range(MARIO_SPRITE_HEIGHT):
        characters_right_of_mario.append(get_char_at(MARIO_LOCATION_X,MARIO_LOCATION_Y-i))
    
    return [characters_below_mario,characters_left_of_mario,characters_above_mario,characters_right_of_mario]

	  

def get_characters_around_enemy():
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global ENEMY_SPRITE_WIDTH
    global ENEMY_SPRITE_HEIGHT

    characters_below_enemy=list()
    for i in range(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH,ENEMY_LOCATION_X):
        characters_below_enemy.append(get_char_at(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH+(i-(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH)),ENEMY_LOCATION_Y+1))

    characters_above_enemy=list()
    for i in range(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH,ENEMY_LOCATION_X):
        characters_above_enemy.append(get_char_at(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH+(i-(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH)),ENEMY_LOCATION_Y-ENEMY_SPRITE_HEIGHT))

    characters_left_of_enemy=list()
    for i in range(ENEMY_SPRITE_HEIGHT):
        characters_left_of_enemy.append(get_char_at(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH-1,ENEMY_LOCATION_Y-i))

    characters_right_of_enemy=list()
    for i in range(ENEMY_SPRITE_HEIGHT):
        characters_right_of_enemy.append(get_char_at(ENEMY_LOCATION_X,ENEMY_LOCATION_Y-i))

    return [characters_below_enemy,characters_left_of_enemy,characters_above_enemy,characters_right_of_enemy]

	
	
def is_collided_with_ridgid(char_list):
    for i in range(len(char_list)):
        if char_list[i] == '|':
            return True
    return False
    
	
	
def process_key(key):
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y
    global MARIO_JUMPED_ONCE
    global MARIO_CAN_DOUBLE_JUMP
    global LAST_PRESSED_KEY
	
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y

    #print(LAST_PRESSED_KEY)
    #print(key)

    #left arrow
    if key == b'K':
        for i in range(3):
            if not is_collided_with_ridgid(get_characters_around_mario()[1]):
                move_2d_mario(MARIO_LOCATION_X-1,MARIO_LOCATION_Y)
                refresh_screen()
        pass

    #down arrow
    elif key == b'P':
        if not is_collided_with_ridgid(get_characters_around_mario()[0]):
            move_2d_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y+1)
        pass
    
    #up arrow
    elif key == b'H':
        if not MARIO_JUMPED_ONCE or MARIO_CAN_DOUBLE_JUMP:
            MARIO_JUMPED_ONCE=True

            MARIO_CAN_DOUBLE_JUMP=not MARIO_CAN_DOUBLE_JUMP
                
            for i in range(10):
                if not is_collided_with_ridgid(get_characters_around_mario()[2]):
                    
                    move_2d_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y-1)
                refresh_screen()
            sound_jump.play()

        pass
    
    #right arrow
    elif key == b'M':
        
        for i in range(6):
            if not is_collided_with_ridgid(get_characters_around_mario()[3]):
                move_2d_mario(MARIO_LOCATION_X+1,MARIO_LOCATION_Y)
                refresh_screen()
        pass
    
    LAST_PRESSED_KEY=key

def move_enemy_left_and_right():
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global ENEMY_SHOULD_MOVE_TO_RIGHT
    
    if is_collided_with_ridgid(get_characters_around_enemy()[3]):
        ENEMY_SHOULD_MOVE_TO_RIGHT=False
    elif is_collided_with_ridgid(get_characters_around_enemy()[1]):
        ENEMY_SHOULD_MOVE_TO_RIGHT=True
    
    if ENEMY_SHOULD_MOVE_TO_RIGHT:
        move_2d_enemy(ENEMY_LOCATION_X+1,ENEMY_LOCATION_Y)
    else:
        move_2d_enemy(ENEMY_LOCATION_X-1,ENEMY_LOCATION_Y)
        
        
def deal_with_mario_and_enemy_collisions():
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global ENEMY_SPRITE_WIDTH
    global ENEMY_SPRITE_HEIGHT
    
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y 
    global MARIO_SPRITE_WIDTH
    global MARIO_SPRITE_HEIGHT
    
    
    #if mario hit the top of enemy
    if (MARIO_LOCATION_Y > (ENEMY_LOCATION_Y-ENEMY_SPRITE_HEIGHT)) and (MARIO_LOCATION_Y < (ENEMY_LOCATION_Y-ENEMY_SPRITE_HEIGHT+2)) and (MARIO_LOCATION_X >= (ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH)) and ((MARIO_LOCATION_X <= (ENEMY_LOCATION_X) or (MARIO_LOCATION_X-MARIO_SPRITE_WIDTH) <= ENEMY_LOCATION_X)):
        #print("TOP collision detected")
        kill_enemy()
        pass
        
        
    #if side collision is detected
    left_of_enemy_collided_with_mario=(MARIO_LOCATION_X >= (ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH)) and (MARIO_LOCATION_X <= (ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH+2)) and (MARIO_LOCATION_Y>(ENEMY_LOCATION_Y-ENEMY_SPRITE_HEIGHT))
    right_of_enemy_collided_with_mario=(ENEMY_LOCATION_X > (MARIO_LOCATION_X-MARIO_SPRITE_WIDTH)) and ENEMY_LOCATION_X < (MARIO_LOCATION_X-(MARIO_SPRITE_WIDTH-2)) and (MARIO_LOCATION_Y>(ENEMY_LOCATION_Y-ENEMY_SPRITE_HEIGHT))
    
    if left_of_enemy_collided_with_mario or right_of_enemy_collided_with_mario:
        kill_mario()
        #print("SIDE Collision detected")
        pass
    
def kill_mario():
    global MARIO_ALIVE
    global LIVES_LEFT
    
    MARIO_ALIVE = False
    LIVES_LEFT=LIVES_LEFT -1
    sound_mariodie.play()  
    bg_player.pause()
    make_screen()
    sleep(sound_mariodie.duration)

    pass
 
def kill_enemy():
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global AREA_ENEMY_REPLACED
    global ENEMY_SHOULD_MOVE_TO_RIGHT
    global ENEMIES_KILLED
    
    ENEMIES_KILLED=ENEMIES_KILLED+1
    ENEMY_SHOULD_MOVE_TO_RIGHT=False

    sound_stomp.play()
    if MARIO_LOCATION_X > 400 and MARIO_LOCATION_X < 650:
        move_2d_enemy(700,18)
        
    elif MARIO_LOCATION_X < 400:
        move_2d_enemy(440,18)

    else:
        pass
    
    prepare_world()
    pass
def make_screen():
    print ((" "*3)+"Enemies killed: "+str(ENEMIES_KILLED)+(" "*15)+"[1;40;31mM[40;32mA[40;33mR[40;34mI[40;35mO [40;36mC[40;31mO[40;32mN[40;33mS[40;34mO[40;35mL[40;36mE[40;37m"+(" "*15)+"Lives left: "+str(LIVES_LEFT))
    print_world(WORLD_MAP) 
    
def deal_with_out_of_bounds_collisions():
    global MARIO_LOCATION_X
    global MARIO_LOCATION_Y 
    
    if MARIO_LOCATION_Y > 18:
        kill_mario()
    
    
def colorize_world(world):
    NEW_WORLD=list()
    for line in world:
        NEW_WORLD.append(line.replace(" ","[44m [40m"))
        NEW_WORLD.append(line.replace("|","[43m [40m"))

    return NEW_WORLD
def display_score():
    global ENEMIES_KILLED
    global MAX_WORLD_WIDTH

    print(("Enemies killed: "+str(ENEMIES_KILLED)).center(MAX_WORLD_WIDTH))  
    print("")
    print(("SCORE: "+str(ENEMIES_KILLED*ENEMIES_KILLED)).center(MAX_WORLD_WIDTH))        
      
def main():
    global MARIO_ALIVE
    global MARIO_JUMPED_ONCE
    global MARIO_CAN_DOUBLE_JUMP
    global AREA_MARIO_REPLACED
    global AREA_ENEMY_REPLACED
    global WON
    
    bg_player.play()

    
    check_the_world()   
    #create_mario(0,0)
    
    create_2d_mario(15,11)
    create_2d_enemy(210,18)
    
    MARIO_KILLING_LIFTED=False
    
    while True:
        sleep(0.05)
        os.system('cls')
        
        
        if MARIO_ALIVE:
            move_enemy_left_and_right()
            deal_with_mario_and_enemy_collisions()
            deal_with_out_of_bounds_collisions()
            
            
            if MARIO_LOCATION_X > 1166 and not WON:
                bg_player.pause()
                print("**** CONGRATULATIONS, YOU HAVE SUCCESSFULLY COMPLETED THE LEVEL ****".center(MAX_WORLD_WIDTH))

                winsound.PlaySound("sounds/smb_stage_clear.wav",winsound.SND_ALIAS)
                WON=True
                
                display_score()
                exit()
                
                
        
            if not is_collided_with_ridgid(get_characters_around_mario()[0]):
                    move_2d_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y+1)
            else:
                MARIO_CAN_DOUBLE_JUMP=False
                MARIO_JUMPED_ONCE=False
                    
        
                    
            if msvcrt.kbhit():
                process_key(msvcrt.getch())
            
            
        else:
            

            if MARIO_LOCATION_Y > 10 and not MARIO_KILLING_LIFTED:
                move_2d_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y-1)
            elif MARIO_KILLING_LIFTED:
                
                move_2d_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y+1)
                if not can_be_moved_mario(MARIO_LOCATION_X,MARIO_LOCATION_Y+1):
                #restart game
                    AREA_MARIO_REPLACED=list()
                    AREA_ENEMY_REPLACED=list()
                    
                    prepare_world()
                    if LIVES_LEFT > 0:
                        MARIO_ALIVE=True
                        
                        main()
                    else:
                        
                        break
                
                
                
            elif MARIO_LOCATION_Y == 10:
                MARIO_KILLING_LIFTED=True
            

                
            
        
        
        #print(MARIO_LOCATION_X,MARIO_LOCATION_Y)
        
        
        make_screen()
        
    print("Game Over".center(MAX_WORLD_WIDTH))        
    winsound.PlaySound('sounds/smb_gameover.wav',winsound.SND_ALIAS)
    display_score()

main()  
