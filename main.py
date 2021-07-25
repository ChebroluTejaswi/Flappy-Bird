import random # for creating randomness(to create pipes)
import sys #sys.exit() is uesd to exit from game
import pygame # basic pygame imports
from pygame.locals import *

#Global variables for game
FPS= 32 #frames per second
SCREENWIDTH = 1000
SCREENHEIGHT = 667
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT)) #Initialize a window or screen for display
GROUNDY = SCREENHEIGHT*0.81
GAME_SPRITES = {}  # creating empty dictionaries --collection of  images
GAME_SOUNDS = {}   # --collection of audios 
PLAYER = 'gallery/sprites/bird.png' #full path for player image
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
sco=[]
sco.append(0)
# welcome screen --shows the welcome images on screen
def welcomeScreen():
    playerx = int((SCREENWIDTH - GAME_SPRITES['player'].get_width())/2) # to display bird at position width/5
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    message2x = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    message2y = int(SCREENHEIGHT*0.7)
    basex = 0
    while True:
        for event in pygame.event.get():
            #if user clicks cross or clicks on escape, then close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if user clicks space or up key, then start the game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):  # keydown states some key is being pressed
                return # then we move to mainGame() function
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey )) 
                SCREEN.blit(GAME_SPRITES['message2'], (message2x,message2y ))     
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()   # until and unlesss we execute this, screen won't change
                FPSCLOCK.tick(FPS) # fixing maximum number of FPS

# Main game
def mainGame():
    score = 0 # intial score
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0
    # creating 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe() # upper pipe
    newPipe2 = getRandomPipe() # lower pipe
     # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]
     
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # when bird is flapping it is true, in all other situations it is false

    while True:
        for event in pygame.event.get():
            #if user clicks cross or clicks on escape, then close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if user clicks space or up key, bird moves up ----game continues(birds moves)
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv # y direction velocity = velocity during flapping
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        #this function will return true if player is crashed
        if crashTest:
            crash(playerx,playery,GROUNDY)
            return

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                sco.append(score)
                print(f"Your score is {score}") 
                print(f"Highest Score is {max(sco)}")
                GAME_SOUNDS['point'].play()

        
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes): # a=[1,2] b=[3,4] zip(a,b)=[(1,3),(2,4)]
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
            

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe() 
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
   

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
       
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0 # total width to blit our number
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY-56  or playery <0:  #55 is the bird's height
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

# function to display GAMEOVER
def crash(playerx,playery,GROUNDY):
    gameoverx = int((SCREENWIDTH - GAME_SPRITES['gameover'].get_width())/2)
    gameovery = int(SCREENHEIGHT*0.40)
    SCREEN.blit(GAME_SPRITES['background'], (0,0))
    SCREEN.blit(GAME_SPRITES['gameover'], (gameoverx,gameovery))
    SCREEN.blit(GAME_SPRITES['outplayer'], (playerx,playery))
    SCREEN.blit(GAME_SPRITES['base'],(0,GROUNDY))
    if max(sco)==0:
        myDigits = [int(x) for x in list(str('0'))]
    else:
        myDigits = [int(x) for x in list(str(max(sco)))]
    width = 0 # total width to blit our number
    for digit in myDigits:
        width += GAME_SPRITES['numbers'][digit].get_width()
    Xoffset = (SCREENWIDTH - width)*0.6
    SCREEN.blit(GAME_SPRITES['highscore'], (Xoffset-GAME_SPRITES['highscore'].get_width()+30, SCREENHEIGHT*0.12))
    for digit in myDigits:
        SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset+30, SCREENHEIGHT*0.12))
        Xoffset += GAME_SPRITES['numbers'][digit].get_width()
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    return

#random pipe generation function
def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3 # difference between two pipes
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX = SCREENWIDTH +10
    y1 = pipeHeight -y2 + offset
    pipe =[
        {'x': pipeX,'y': -y1}, # for upper pipe
        {'x': pipeX,'y': y2}  # for lower pipe
    ]
    return pipe

if __name__ == "__main__":
    # This is point where game starts
    pygame.init() #intializes all pygame modules
    FPSCLOCK = pygame.time.Clock()  # clock is used to control FPS of game
    pygame.display.set_caption('Flappy Bird by Tejaswi')
    #loading images
    #convert alpha tries to optimize our image for the game
    GAME_SPRITES['numbers'] =( # creating a tuple of images
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['message'] =  pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['message2'] =  pygame.image.load('gallery/sprites/message2.png').convert_alpha()
    GAME_SPRITES['base'] =  pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =  (
        pygame.transform.rotate(pygame.image.load('gallery/sprites/pipe.png').convert_alpha(), 180),
        pygame.image.load('gallery/sprites/pipe.png').convert_alpha()
    )
    GAME_SPRITES['gameover'] = pygame.image.load('gallery/sprites/gameover1.png').convert_alpha()
    GAME_SPRITES['outplayer'] = pygame.image.load('gallery/sprites/bird1.png').convert_alpha()
    GAME_SPRITES['highscore'] = pygame.image.load('gallery/sprites/highscore.png').convert_alpha()
    #game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() #shows welcome screen to the user until he clicks on a button
        mainGame() # this is main game of function


# Bliting image:
# measured from top left corner of screen and the top-left point of image gets placed at that point(x,y)