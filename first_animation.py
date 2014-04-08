__author__ = 'McGuiT1'
import sys
import time
import pygame
import os
from pygame.locals import *
import random

BLOCKSIZE=15
x = 100
y = 20
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
soundFile = "snare.wav"
pygame.mixer.init()
sound = pygame.mixer.Sound(soundFile)
#window:
WINWIDTH = 1200
WINHEIGHT = 700
winSurf = pygame.display.set_mode((WINWIDTH,WINHEIGHT),0,32)
pygame.display.set_caption('Animation!!!!!!')

DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9
NONE=0
UP = 2
DOWN = 8
MOVESPEED = 2

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,128,20)
PINK = (255,10,255)
p1color = PINK
p2color = ORANGE
def crash(x,y):
    particles = []
    # send 10 - 20 particles at random directions
    for b in range (0,10):
        particle = {'rect':pygame.Rect(x,y,2,2), 'color':RED, 'dir':UP }
        particles.append(particle)
    return particles

def isPointInsideRect(x,y,rect):
    if (x >= rect.left) and (x <= rect.right) and (y > rect.top) and (y < rect.bottom):
        return True

def collision(player,sb):
    for block in sb:
        for a,b in [(player, block), (block, player)]:
            if ((isPointInsideRect (a['rect'].left, a['rect'].top, b['rect'])) or
                (isPointInsideRect (a['rect'].left, a['rect'].bottom, b['rect'])) or
                (isPointInsideRect(a['rect'].right, a['rect'].top, b['rect'])) or (isPointInsideRect(a['rect'].right, a['rect'].bottom, b['rect']))):
                return True

def moveBlock(b):

    if b['dir'] == DOWNLEFT:
        b['rect'].left -= MOVESPEED
        b['rect'].top += MOVESPEED
    if b['dir'] == UP:
        b['rect'].top -= MOVESPEED
    if b['dir'] == DOWNRIGHT:
        b['rect'].left += MOVESPEED
        b['rect'].top += MOVESPEED
    if b['dir'] == UPRIGHT:
        b['rect'].left += MOVESPEED
        b['rect'].top -= MOVESPEED
    if b['dir'] == UPLEFT:
        b['rect'].left -= MOVESPEED
        b['rect'].top -= MOVESPEED

    if b['rect'].bottom < 0:
        #past the top
        b['rect'].top = WINHEIGHT
        # if b['dir'] == UPLEFT:
        #     b['dir'] = DOWNLEFT
        # if b['dir'] == UPRIGHT:
        #     b['rect'].top = WINHEIGHT
        #     #b['dir'] = DOWNRIGHT
        # if b['dir'] == UP:
        #     b['rect'].top = WINHEIGHT

    if b['rect'].bottom > WINHEIGHT:
        #past the bottom
        if b['dir'] == DOWNLEFT:
            b['dir'] = UPLEFT
        if b['dir'] == DOWNRIGHT:
            b['dir'] = UPRIGHT

    if b['rect'].left < 0:
        b['rect'].left = WINWIDTH -BLOCKSIZE
        #past the left
        # if b['dir'] == UPLEFT:
        #     b['dir'] = UPRIGHT
        # if b['dir'] == DOWNLEFT:
        #     b['dir'] = DOWNRIGHT

    if b['rect'].right > WINWIDTH:
        #past the right
        # if b['dir'] == UPRIGHT:
        #     b['dir'] = UPLEFT
        # if b['dir'] == DOWNRIGHT:
        #     b['dir'] = DOWNLEFT
        b['rect'].left =0

def restart(player1points, player2points):
    time.sleep(0.3)
    player1 = {'rect':pygame.Rect(300,80,BLOCKSIZE,BLOCKSIZE), 'color':GREEN, 'bcolor':PINK, 'dir':UP, 'points':player1points}
    player2 = {'rect':pygame.Rect(WINWIDTH/2 + 100,100,BLOCKSIZE,BLOCKSIZE), 'color':BLUE, 'bcolor':ORANGE, 'dir':UP, 'points':player2points}
    return player1, player2

def doStaticBlocks():
    static_blocks = []
    blocks_to_skip = random.randint(5,10)
    start = random.randint(0,WINHEIGHT - blocks_to_skip * BLOCKSIZE)
    end = start + blocks_to_skip * BLOCKSIZE

    for x in range(0,WINHEIGHT,BLOCKSIZE):
        # skip blocks in a row at random:
        if x < start or x > end:
            static_blocks.append({'rect':pygame.Rect(WINWIDTH/2,x,BLOCKSIZE,BLOCKSIZE),'color':WHITE, 'dir':NONE})
    return static_blocks

def makeStaticBlock(static_blocks,player):
    h = 0
    v = 0
    playerColor = player['bcolor']
    # put a static block down and advance player past it so it doesn't register as a collision
    # if player direction is up, put it BLOCKSIZE to the rear  # if upleft, put it down and right  if upright, put it down and right
    if player['dir'] == UP:
        h = 0
        v = BLOCKSIZE
    if player['dir'] == UPLEFT:
        h = BLOCKSIZE
        v = BLOCKSIZE
    if player['dir'] == UPRIGHT:
        h = -BLOCKSIZE
        v = BLOCKSIZE
    print (str(h) + " is h and " + str(v) + " is v")
    print ("player dir: " + str(player['dir']))
    newBlock = {'rect':pygame.Rect(player['rect'].left + h,player['rect'].top + v,BLOCKSIZE,BLOCKSIZE),'color':playerColor, 'dir':NONE}
    static_blocks.append(newBlock)
    return static_blocks

player1 = {'rect':pygame.Rect(300,80,BLOCKSIZE,BLOCKSIZE), 'color':RED,'bcolor':PINK, 'dir':UP, 'points':0}
player2 = {'rect':pygame.Rect(WINWIDTH/2 + 100,100,BLOCKSIZE,BLOCKSIZE), 'color':BLUE, 'bcolor':ORANGE, 'dir':UP, 'points':0}
static_blocks = doStaticBlocks()
p1addblock = False
p2addblock = False

#gameloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            print ("player1: " + str(player1['points']))
            print ("player2: " + str(player2['points']))
            pygame.quit()
            sys.exit()


        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_LEFT:
                player2['dir'] = UPLEFT
            if event.key == pygame.locals.K_RIGHT:
                player2['dir'] = UPRIGHT
            if event.key == pygame.locals.K_UP:
                player2['dir'] = UP
            if event.key == pygame.locals.K_DOWN:
                p2addblock = True

            if event.key == ord('a'):
                player1['dir'] = UPLEFT
            if event.key == ord('d'):
                player1['dir'] = UPRIGHT
            if event.key == ord('w'):
                player1['dir'] = UP
            if event.key == ord('s'):
                p1addblock = True
        if event.type == pygame.locals.KEYUP:
            print("hey keyup")
            if event.key == pygame.locals.K_DOWN:
                p2addblock = False
            if event.key == ord('s'):
                print("hey S")
                p1addblock = False

    winSurf.fill(BLACK)

    if p2addblock:
        makeStaticBlock(static_blocks,player2)
#        newBlock = {'rect':pygame.Rect(player2['rect'].left-20,player2['rect'].top-20,20,20),'color':PINK, 'dir':NONE}
#        static_blocks.append(newBlock)

    if p1addblock:
 #       newBlock = {'rect':pygame.Rect(player1['rect'].left-20,player1['rect'].top -20,20,20),'color':ORANGE, 'dir':NONE}
 #       static_blocks.append(newBlock)
        makeStaticBlock(static_blocks,player1)
    moveBlock(player1)
    moveBlock(player2)



    hasCollision = False
    if(collision(player1, static_blocks)):
        player2['points'] += 1
        hasCollision = True
    if(collision(player2,static_blocks)):
        player1['points'] += 1
        hasCollision = True
    if hasCollision:
        sound.play()
        MOVESPEED = 3
        static_blocks = doStaticBlocks()
        player1,player2 = restart(player1['points'], player2['points'])
    if MOVESPEED < 10:
        MOVESPEED = MOVESPEED + 0.1

    pygame.draw.rect(winSurf,player1['color'],player1['rect'])
    pygame.draw.rect(winSurf,player2['color'],player2['rect'])
    for sb in static_blocks:
        pygame.draw.rect(winSurf,sb['color'],sb['rect'])
    pygame.display.update()
    time.sleep(0.02)

