__author__ = 'mcgyver5'
import sys
import time
import datetime
import pygame
import os
import globals
pygame.init()
import surround_menu
from pygame.locals import *
import random
fade = 100
BLOCKSIZE=15
x = 100
y = 20
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

soundFile = "snare.wav"
pygame.mixer.init()
sound = pygame.mixer.Sound(soundFile)
print(globals.WINWIDTH)
print("______________________________")
winSurf = pygame.display.set_mode((globals.WINWIDTH,globals.WINHEIGHT),0,32)
pygame.display.set_caption('Animation!!!!!!')

MOVESPEED = 2

p1color = globals.PINK
p2color = globals.ORANGE
def crash(x,y):
    particles = []
    # send 10 - 20 particles at random directions
    for b in range (0,10):
        particle = {'rect':pygame.Rect(x,y,2,2), 'color':globals.RED, 'dir':globals.UP }
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
    if b['dir'] == globals.DOWNLEFT:
        b['rect'].left -= MOVESPEED
        b['rect'].top += MOVESPEED
    if b['dir'] == globals.UP:
        b['rect'].top -= MOVESPEED
    if b['dir'] == globals.DOWNRIGHT:
        b['rect'].left += MOVESPEED
        b['rect'].top += MOVESPEED
    if b['dir'] == globals.UPRIGHT:
        b['rect'].left += MOVESPEED
        b['rect'].top -= MOVESPEED
    if b['dir'] == globals.UPLEFT:
        b['rect'].left -= MOVESPEED
        b['rect'].top -= MOVESPEED

    if b['rect'].bottom < 0:
        #past the top
        b['rect'].top = globals.WINHEIGHT

    if b['rect'].bottom > globals.WINHEIGHT:
        #past the bottom
        if b['dir'] == globals.DOWNLEFT:
            b['dir'] = globals.UPLEFT
        if b['dir'] == globals.DOWNRIGHT:
            b['dir'] = globals.UPRIGHT

    if b['rect'].left < 0:
        b['rect'].left = globals.WINWIDTH -BLOCKSIZE

    if b['rect'].right > globals.WINWIDTH:
        b['rect'].left =0

def restart(player1points, player2points):
    time.sleep(0.3)
    player1 = {'rect':pygame.Rect(300,80,BLOCKSIZE,BLOCKSIZE), 'color':globals.GREEN, 'bcolor':globals.PINK, 'dir':globals.UP, 'points':player1points}
    player2 = {'rect':pygame.Rect(globals.WINWIDTH/2 + 100,100,BLOCKSIZE,BLOCKSIZE), 'color':globals.BLUE, 'bcolor':globals.ORANGE, 'dir':globals.UP, 'points':player2points}
    return player1, player2

def doInitialStaticBlocks():
    static_blocks = []
    blocks_to_skip = random.randint(5,10)
    start = random.randint(0,globals.WINHEIGHT - blocks_to_skip * BLOCKSIZE)
    end = start + blocks_to_skip * BLOCKSIZE

    for x in range(0,globals.WINHEIGHT,BLOCKSIZE):
        # skip blocks in a row at random:
        if x < start or x > end:
            static_blocks.append({'rect':pygame.Rect(globals.WINWIDTH/2,x,BLOCKSIZE,BLOCKSIZE),'color':globals.WHITE, 'dir':globals.NONE,'lifespan':2000})
    return static_blocks

def makeStaticBlock(static_blocks,player):
    h = 0
    v = 0
    playerColor = player['bcolor']
    # put a static block down and advance player past it so it doesn't register as a collision
    # if player direction is up, put it BLOCKSIZE to the rear  # if upleft, put it down and right  if upright, put it down and right
    if player['dir'] == globals.UP:
        h = 0
        v = BLOCKSIZE
    if player['dir'] == globals.UPLEFT:
        h = BLOCKSIZE
        v = BLOCKSIZE
    if player['dir'] == globals.UPRIGHT:
        h = -BLOCKSIZE
        v = BLOCKSIZE

    newBlock = {'rect':pygame.Rect(player['rect'].left + h,player['rect'].top + v,BLOCKSIZE,BLOCKSIZE),'color':playerColor, 'dir':globals.NONE, 'lifespan':fade,'delete':False}
    static_blocks.append(newBlock)
    return static_blocks

# start players at a random y value:
randy1 = random.randint(0,globals.WINHEIGHT)
randy2 = random.randint(0,globals.WINHEIGHT)

player1 = {'rect':pygame.Rect(300,randy1,BLOCKSIZE,BLOCKSIZE), 'color':globals.RED,'bcolor':globals.PINK, 'dir':globals.UP, 'points':0}
player2 = {'rect':pygame.Rect(globals.WINWIDTH/2 + 100,randy2,BLOCKSIZE,BLOCKSIZE), 'color':globals.BLUE, 'bcolor':globals.ORANGE, 'dir':globals.DOWN, 'points':0}
static_blocks = doInitialStaticBlocks()
p1addblock = False
p2addblock = False


def checkStaticBlocks(static_blocks):
    for block in static_blocks:
        block['lifespan'] = block['lifespan'] -1
        if block['lifespan'] <=0:
            # flag for deletion
            static_blocks.remove(block)
startTime = datetime.datetime.now()
#gameloop
while True:
    for event in pygame.event.get():

        if event.type == pygame.locals.QUIT:
            print ("player1: " + str(player1['points']))
            print ("player2: " + str(player2['points']))
            pygame.quit()
            sys.exit()


        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.locals.K_LEFT:
                player2['dir'] = globals.UPLEFT
            if event.key == pygame.locals.K_RIGHT:
                player2['dir'] = globals.UPRIGHT
            if event.key == pygame.locals.K_UP:
                player2['dir'] = globals.UP
            if event.key == pygame.locals.K_DOWN:
                p2addblock = True

            if event.key == ord('a'):
                player1['dir'] = globals.UPLEFT
            if event.key == ord('d'):
                player1['dir'] = globals.UPRIGHT
            if event.key == ord('w'):
                player1['dir'] = globals.UP
            if event.key == ord('s'):
                p1addblock = True
        if event.type == pygame.locals.KEYUP:

            if event.key == pygame.locals.K_DOWN:
                p2addblock = False
            if event.key == ord('s'):
                p1addblock = False

    winSurf.fill(globals.BLACK)

    checkStaticBlocks(static_blocks)
    if p2addblock:
        makeStaticBlock(static_blocks,player2)

    if p1addblock:
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
        static_blocks = doInitialStaticBlocks()
        player1,player2 = restart(player1['points'], player2['points'])
    # MOVESPEED 3, 6, 9, 12
    # When to step?
    now = datetime.datetime.now()
    elapsed = now - startTime
    secondsPassed = elapsed.total_seconds()
    if secondsPassed > 2 and MOVESPEED <=12:
        MOVESPEED = MOVESPEED + 1
        startTime = now
    #if MOVESPEED < 10:
    #    MOVESPEED = MOVESPEED + 0.1

    pygame.draw.rect(winSurf,player1['color'],player1['rect'])
    pygame.draw.rect(winSurf,player2['color'],player2['rect'])
    for sb in static_blocks:
        pygame.draw.rect(winSurf,sb['color'],sb['rect'])
    pygame.display.update()
    time.sleep(0.02)

