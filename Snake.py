import random
import pygame

pygame.init()



#Initializes Screen Size
Height = 300
Width = 600


#Initializes all colours that will be used
Black = (0, 0, 0)
White = (255, 255, 255)
Green = (0, 255, 0)
Red = (255, 0, 0)
Blue = (0, 0, 255)


#Sets the size of each block of the snake
Size = 10;
Gap = 2;
Block = Size + Gap

#Creates a display for the game
gameDisplay = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Snake')






#Initializes Global Variables
clock = pygame.time.Clock()
crashed = False
SnakeArr = [[0, 0] , [0, 0]]
SnakeLength = 2
ApplePos = []
MUp = False
MLeft = False
MRight = True
MDown = False
Lost = False
Won = False
Score = 0
AI = False
FPS = 20
AIFPS = 30000






#Initializes Boundaries
YMin = 2 * Block
YMax = 22 * Block
XMin = 2 * Block
XMax = 46 * Block
#The boundaries of the frame were found with trial and error.
#These are the boundaries of the white frame ascii such
#[xminimum, yminimum, xmaximum, ymaximum]
Frame = [ XMin - Gap + Block, YMin - Gap + Block, XMax - 2 * Block + 1, YMax - 2 * Block + 1]



#Reinitializes the game
def init():
    global SnakeArr
    global SnakeLength
    global ApplePos
    global MUp
    global MLeft
    global MRight
    global MDown
    global Lost
    global Score
    global AI
    global FPS
    global Won
    SnakeArr = [[(Size + Gap) * 10,  (Size + Gap) * 10] , [(Size + Gap) * 10 - Size - Gap,  (Size + Gap) * 10]]
    SnakeLength = 2
    ApplePos = [-1,-1]
    MUp = False
    MLeft = False
    MRight = True
    MDown = False
    Lost = False
    Won = False
    Score = 0
    AI = False
    FPS = 20








#Returns column i in a matrix
def column(matrix, i):
    return [row[i] for row in matrix]












#Shows the snake
def SnakeDisp(Arr):
    global SnakeLength
    global ApplePos
    
    #Draw the whole snake except the head
    for i in range(SnakeLength - 1):
        pygame.draw.rect( gameDisplay, Green, [ (int)(Arr[i + 1][0]), (int)(Arr[i + 1][1]), Size, Size])
        
    #Draw the head of the snake
    #Drawn after the body so the head is visible in case of game over.
    pygame.draw.rect( gameDisplay, Blue, [ (int)(Arr[0][0]), (int)(Arr[0][1]), Size, Size])
    #Draw the red apple
    pygame.draw.rect( gameDisplay, Red, [ ApplePos[0], ApplePos[1], Size, Size])












#Looks for inputs
def KeyPush():
    global MUp
    global MDown
    global MLeft
    global MRight

    global crashed
    global AI
    global FPS
    global AIFPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:

            #This only applies before beginning the game
            if (not MUp) and (not MDown) and (not MLeft) and (not MRight):
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    MUp = True
                    MLeft = False
                    MRight = False
                    MDown = False
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    MUp = False
                    MLeft = False
                    MRight = False
                    MDown = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    MUp = False
                    MLeft = True
                    MRight = False
                    MDown = False
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    MUp = False
                    MLeft = False
                    MRight = True
                    MDown = False
                elif event.key == pygame.K_1:
                    #Game goes in mode AI if 1 is pressed
                    #AI Mode starts with snake going up
                    AI = True
                    MUp = True
                    MLeft = False
                    MRight = False
                    MDown = False
                    FPS = AIFPS
                    return

            #If the snake goes up, it cannot go down right away.
            elif (not MUp) and (not MDown):
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    MUp = True
                    MLeft = False
                    MRight = False
                    MDown = False
                    return
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    MUp = False
                    MLeft = False
                    MRight = False
                    MDown = True
                    return
                elif event.key == pygame.K_1:
                    #Game goes in mode AI if 1 is pressed
                    #AI Mode starts with snake going up
                    AI = True
                    MUp = True
                    MLeft = False
                    MRight = False
                    MDown = False
                    FPS = AIFPS
                    return

                    
            #If the snake goes right, it cannot go left right away.
            #elif so that the snake needs to go up at least once before doing a u-turn
            elif (not MLeft) and (not MRight):
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    MUp = False
                    MLeft = True
                    MRight = False
                    MDown = False
                    return
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    MUp = False
                    MLeft = False
                    MRight = True
                    MDown = False
                    return
                elif event.key == pygame.K_1:
                    #Game goes in mode AI if 1 is pressed
                    #AI Mode starts with snake going up
                    AI = True
                    MUp = True
                    MLeft = False
                    MRight = False
                    MDown = False
                    FPS = AIFPS
                    return















#Moves the body and head of the snake at each frame.
def SnakeMov():
    global SnakeArr
    global SnakeLength

    global MUp
    global MDown
    global MLeft
    global MRight


    for i in range(SnakeLength - 1):
        SnakeArr[ ( SnakeLength - i - 1)][ 0 ] = SnakeArr[ (SnakeLength - i - 2)][ 0 ]
        SnakeArr[(  SnakeLength - i - 1)][ 1 ] = SnakeArr[ (SnakeLength - i - 2)][ 1 ]

    if MUp:
        SnakeArr[0][1] -= Size + Gap
    elif MDown:
        SnakeArr[0][1] += Size + Gap
    elif MLeft:
        SnakeArr[0][0] -= Size + Gap
    elif MRight:
        SnakeArr[0][0] += Size + Gap












#Checks if losing conditions for the game have been fulfilled.
def GameLost():
    global Lost
    global SnakeLength
    global YMin
    global YMax
    global XMin
    global XMax

    #Checks if Snake is out of bounds
    if SnakeArr[0][1] <= YMin or SnakeArr[0][1] > YMax or SnakeArr[0][0] <= XMin or SnakeArr[0][0] > XMax:
        Lost = True

        
    #Checks is Snake is eating itself
    for i in range(SnakeLength - 1):
        if (SnakeArr[0][1] == SnakeArr[i + 1][1]) and (SnakeArr[0][0] == SnakeArr[i + 1][0]):
            Lost = True
            break

    #Prints text on screen once the game if over.
    if Lost:
        largeText = pygame.font.Font('freesansbold.ttf',40)
        TextSurf, TextRect = text_objects('You Lost', largeText)
        TextRect.center = (int(Width/2), int(Height/2))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()






#Checks if winning conditions for the game have been fulfilled.
def GameWon():
    global Won
    global SnakeLength
    global AIFPS

    if SnakeLength == 882:
        Won = True

        #Congratulates the player if the game was won.
        largeText = pygame.font.Font('freesansbold.ttf',40)
        TextSurf, TextRect = text_objects('Congratulations You Won!', largeText)
        TextRect.center = (int(Width/2), int(Height/2))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
    elif SnakeLength >= 850:
        FPS = 20





#Checks if the apple has been initialized or eaten.
#Randomly places the apple if either is true
def Apple():
    global ApplePos
    global SnakeArr
    global gameDisplay
    global SnakeLength
    global Score
    global YMin
    global YMax
    global XMin
    global XMax
    global Won

    #Spawning range of the apples, determined experimentally
    XMinApp = XMin + Block
    XMaxApp = XMax + Block
    YMinApp = YMin + Block
    YMaxApp = YMax + Block

    #Initiates the position of the Apple
    if ApplePos[0] == -1:
        #Randomly Positions the Apple in range
        ApplePos[0] = random.randrange(XMinApp, XMaxApp, Block)
        ApplePos[1] = random.randrange(YMinApp, YMaxApp, Block)
    
    #moves the Apple once eaten
    if (SnakeArr[0][0] == ApplePos[0] and SnakeArr[0][1] == ApplePos[1]):

        #Randomly Positions the Apple in range
        ApplePos[0] = random.randrange(XMinApp, XMaxApp, Block)
        ApplePos[1] = random.randrange(YMinApp, YMaxApp, Block)

        #Elongates the snake
        SnakeLength += 1;
        SnakeArr.append([SnakeArr[SnakeLength - 2][0], SnakeArr[SnakeLength - 2][1]])

        #Increase the score
        Score += 1

    #Makes sure the apple does not spawn inside the snake.
    #Also checks if the rectangle is full in case the game has been won.
    GameWon()
    for i in range(SnakeLength - 1):
        if Won:
            return
        elif (ApplePos[0] == SnakeArr[i + 1][0]) and (ApplePos[1] == SnakeArr[i + 1][1]):
            ApplePos = [-1, -1]
            Apple()
            break








#From https://pythonprogramming.net/displaying-text-pygame-screen/?completed=/adding-boundaries-pygame-video-game/
#Places test on the screen
def text_objects(text, font):
    textSurface = font.render(text, True, White)
    return textSurface, textSurface.get_rect()
#From the same sources, creates a rectangle around the text to position it easily.    
def Disp_Score():
    largeText = pygame.font.Font('freesansbold.ttf',12)
    TextSurf, TextRect = text_objects('Score: ' + str(Score), largeText)
    TextRect.center = (40,15)
    gameDisplay.blit(TextSurf, TextRect)







def SnakeAI():
    global SnakeArr
    global MUp
    global MDown
    global MRight
    global MLeft
    
    if MUp and ((SnakeArr[0][1] - Block) <= YMin):
        MUp = False
        MDown = False
        MRight = True
        MLeft = False
    elif MRight and ((SnakeArr[0][1] - Block) <= YMin):
        MUp = False
        MDown = True
        MRight = False
        MLeft = False
    elif MDown and ((SnakeArr[0][1] + 2 * Block) > YMax) and not (SnakeArr[0][0] + 2 * Block > XMax):
        MUp = False
        MDown = False
        MRight = True
        MLeft = False
    elif MRight and ((SnakeArr[0][1] + 2 * Block) > YMax):
        MUp = True
        MDown = False
        MRight = False
        MLeft = False
    elif MDown and ((SnakeArr[0][1] + Block) > YMax):
        MUp = False
        MDown = False
        MRight = False
        MLeft = True
    elif MLeft and ((SnakeArr[0][0] - 2 * Block) < XMin):
        MUp = True
        MDown = False
        MRight = False
        MLeft = False
    







#Initializes the game.
#Comments for this can be found in the main loop
init()
gameDisplay.fill(Black)
pygame.draw.rect( gameDisplay, White, Frame, Gap)
Apple()
SnakeDisp(SnakeArr)
pygame.display.update()
Begin = False



#Waits for the player to push a key.
while(not Begin):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            KeyPush()
            Begin = True











#Main loop of the game.
while not crashed:


    #Checks for user input
    if not(AI):
        KeyPush()
    else:
        SnakeAI()




    #Moves the snake and checks if the apple needs to be moved.
    SnakeMov()
    Apple()


    #Fills the display with black and puts a white frame around the play area.
    #The boundaries of the frame where found with trial and error.
    gameDisplay.fill(Black)
    pygame.draw.rect( gameDisplay, White, Frame, Gap)
    

    SnakeDisp(SnakeArr)
    Disp_Score();
    
    pygame.display.update()
    clock.tick(FPS)


    GameLost()
    GameWon()

    if Lost or Won:
        while(Lost or Won):
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_SPACE):
                        Lost = False
                        break
        init()

pygame.quit()
quit()
