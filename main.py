import pygame
import time

pygame.init()

# How many digits do you want to calculate?
digits = 6
timestep = 10000

# Display
width, height = 1600, 900
WIN = pygame.display.set_mode((width, height))
BG = pygame.transform.scale(pygame.image.load('images/background.jpg'), (width,height))
pygame.display.set_caption("Calculate Pi by Collision")
font = pygame.font.SysFont("consolas", 40)
textColor = "white"
pi = font.render('0', True, "white")
nrCol = font.render('# Collisions: ', True, "white")
s = '1' + '0' * (2*(digits - 1)%3) + ',000' * int(2*(digits - 1)/3) + ' kg'

# Enviroment
wallWidth = 160
wallHeight = height
WALL = pygame.transform.scale(pygame.image.load('images/border.png'), (60,660))
wall = pygame.Rect(0,0,wallWidth, wallHeight)
LINE = pygame.transform.scale(pygame.image.load('images/borderdown.png'), (1600,70))
clack = pygame.mixer.Sound('clack.wav')

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


def draw():
    WIN.blit(BG,(0,0))
    WIN.blit(LINE,(wallWidth, wallHeight - 140))
    WIN.blit(WALL,(wallWidth - 60,100))
    pi = font.render(str(totalCollision), True, textColor)
    nrCol = font.render('# Collisions:', True, textColor)
    WIN.blit(nrCol,(600,20))
    WIN.blit(pi,(950,20))
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
run = True
totalCollision = 0
if digits >= 8 :
    timestep = timestep * 10
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
            run = False
            break
    for i in range(timestep) :
        move()
        collision()
    draw()
    pygame.display.update()  
pygame.quit()