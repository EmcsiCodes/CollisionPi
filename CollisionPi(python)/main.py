import pygame
import time

pygame.init()

# Important
digits = 1
totalCollision = 0
timestep = 10000
gamePaused = True

# Display
width, height = 1600, 900
WIN = pygame.display.set_mode((width, height))
BG = pygame.transform.scale(pygame.image.load('background.jpg'), (width,height))
pygame.display.set_caption("Calculate Pi by Collision")
font = pygame.font.SysFont("consolas", 50)
textColor = "white"
s = '1' + '0' * (2*(digits - 1)%3) + ',000' * int(2*(digits - 1)/3) + ' kg'
restartButton = pygame.Rect(width - 120, height - 120, 100, 100)
stopButton = pygame.Rect(width - 240, height - 120, 100, 100)
startButton = pygame.Rect(width - 240, height - 120, 100, 100)
RESTARTBUTTON = pygame.transform.scale(pygame.image.load('images/restartButton.png'), (100,100))
STOPBUTTON = pygame.transform.scale(pygame.image.load('images/stopButton.png'), (100,100))
STARTBUTTON = pygame.transform.scale(pygame.image.load('images/startButton.png'), (100,100))
UPARROW = pygame.transform.scale(pygame.image.load('images/upArrow.png'), (30,40))
DOWNARROW = pygame.transform.scale(pygame.image.load('images/downArrow.png'), (30,40))
piButton = pygame.Rect(650,height - 110,80,80)
upArrow = pygame.Rect(750,height - 115,30,40)
downArrow = pygame.Rect(750, height - 65,30,40)
piImage = pygame.transform.scale(pygame.image.load('images/pi.png'),(50,50))
setDigits = font.render("Set # of    's digits: ", True, "white")
nrCol = font.render('# Collisions:', True, textColor)
usr_txt = "1"

# Enviroment
wallWidth = width / 10
wallHeight = height
WALL = pygame.transform.scale(pygame.image.load('images/border.png'), (60,660))
wall = pygame.Rect(0,0,wallWidth, wallHeight)
LINE = pygame.transform.scale(pygame.image.load('images/borderdown.png'), (1600,70))
clack = pygame.mixer.Sound('clack.mp3')

# Square 1
SQUARE1_DIM = 100.0
smallSquare = [550.0, 660.0, 550.0 + SQUARE1_DIM, 660.0 + SQUARE1_DIM]
smallSquare_Img = pygame.transform.scale(pygame.image.load('images/smallSquare.jpg'), (SQUARE1_DIM, SQUARE1_DIM))

# Square 2
SQUARE2_DIM = 200.0
bigSquare = [1100.0, 560.0, 1100.0 + SQUARE2_DIM, 560.0 + SQUARE2_DIM]
bigSquare_Img = pygame.transform.scale(pygame.image.load('images/bigSquare.jpeg'), (SQUARE2_DIM, SQUARE2_DIM))

# Physics
v1 = 0
m1 = 1
v2 = -1/timestep
m2 = 100 ** (digits - 1)
    
def reset():
    global v1, m1, v2, m2, totalCollision, smallSquare, bigSquare, s, gamePaused
    gamePaused = True
    timestep = 10000 
    v1 = 0
    m1 = 1
    v2 = -1/timestep
    m2 = 100 ** (digits - 1)
    if digits >= 8 and digits <= 9:
        timestep = 10000
    if digits >= 10:
        timestep = 100000
    smallSquare = [550.0, 660.0, 550.0 + SQUARE1_DIM, 660.0 + SQUARE1_DIM]
    bigSquare = [1100.0, 560.0, 1100.0 + SQUARE2_DIM, 560.0 + SQUARE2_DIM]
    totalCollision = 0
    s = '1' + '0' * (2*(digits - 1)%3) + ',000' * int(2*(digits - 1)/3) + ' kg'
    draw()

def draw():
    WIN.blit(BG,(0,0))
    WIN.blit(LINE,(wallWidth, wallHeight - 140))
    WIN.blit(WALL,(wallWidth - 60,100))
    WIN.blit(RESTARTBUTTON,(width - 120, height - 120))
    if gamePaused == False :
        WIN.blit(STOPBUTTON,(width - 240, height - 120))
    else :
        WIN.blit(STARTBUTTON,(width - 240, height - 120))
    pygame.draw.rect(WIN,(59,68,75),piButton, 40,15)
    WIN.blit(UPARROW,(750,height - 115))
    WIN.blit(DOWNARROW,(750, height - 65))
    pi = font.render(str(totalCollision), True, textColor)
    usrInput = font.render(usr_txt, True, textColor)
    WIN.blit(nrCol,(580,40))
    WIN.blit(pi,(970,40))
    WIN.blit(piImage,(300,height - 95))
    WIN.blit(setDigits,(40, height - 95))
    WIN.blit(usrInput,(678,height - 94))
    x = smallSquare[0]
    if smallSquare[0] < wallWidth and digits >= 7: 
        x = wallWidth
    WIN.blit(smallSquare_Img,(x,smallSquare[1],x + SQUARE1_DIM,smallSquare[3]))
    WIN.blit(pygame.font.SysFont("consolas", 30).render('1 kg', True, textColor), (x + 15,smallSquare[1] - 40))
    x = bigSquare[0]
    if bigSquare[0] < wallWidth + SQUARE1_DIM and digits >= 7: 
        x = wallWidth + SQUARE1_DIM
    WIN.blit(bigSquare_Img,(x,bigSquare[1],x + SQUARE2_DIM,bigSquare[3]))
    WIN.blit(pygame.font.SysFont("consolas", 30).render(s, True, textColor), (((x+x+SQUARE2_DIM)/2-8*len(s)),bigSquare[1] - 40))
    
def move():
    smallSquare[0] += v1
    bigSquare[0] += v2
    
def collision():
    global v1, m1, v2, m2, totalCollision
    u1 = v1
    u2 = v2
    sum = m1 + m2
    if smallSquare[0] + SQUARE1_DIM >= bigSquare[0]:
        totalCollision += 1
        clack.play()
        v1 = ((m1 - m2)*u1 + 2*u2*m2)/sum
        v2 = (2*m1*u1 + (m2 - m1)*u2)/sum
    if smallSquare[0] <= wallWidth:
        totalCollision += 1
        clack.play()
        v1 = -v1

# Main
def main():
    run = True
    global timestep, digits, usr_txt, gamePaused
    digits = 1
    reset()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE: 
                    run = False
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restartButton.collidepoint(pygame.mouse.get_pos()):  
                    reset()
                if upArrow.collidepoint(pygame.mouse.get_pos()):
                    digits += 1
                    usr_txt = str(digits)
                    reset()
                if downArrow.collidepoint(pygame.mouse.get_pos()) and digits >= 2:
                    digits -= 1
                    usr_txt = str(digits)
                    reset()
                if stopButton.collidepoint(pygame.mouse.get_pos()) and gamePaused == False:
                    gamePaused = True
                    draw()
                elif startButton.collidepoint(pygame.mouse.get_pos()) and gamePaused == True:
                    gamePaused = False
        if gamePaused == False:      
            for i in range(timestep) :
                move()
                collision()
            draw()
        pygame.display.update()  
    pygame.quit()

if __name__ == "__main__" :
    main()
