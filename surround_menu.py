__author__ = 'mcgyver5'
import sys
import time
import pygame
import os
from pygame.locals import *
import globals
def menu_render(winSurf,textList,startPos,sepDist,fontSize=40,h_offset=0):
    print("MENU RENDER")
    basicFont = pygame.font.SysFont(None, fontSize)
    for str in textList:
        tt = basicFont.render(str,True, globals.WHITE,globals.RED)
        ttRect = tt.get_rect()
        ttRect.centerx = winSurf.get_rect().centerx + h_offset
        ttRect.centery = winSurf.get_rect().centery + startPos
        startPos = startPos + sepDist
        winSurf.blit(tt,ttRect)

def number_render(winSurf,xpos,ypos,fontSize=40, h_offset=200):
    print("NUMBER RENDER")
    str = "100"
    basicFont = pygame.font.SysFont(None, fontSize)
    tt = basicFont.render(str,True, globals.WHITE,globals.RED)
    ttRect = tt.get_rect()
    ttRect.centerx = winSurf.get_rect().centerx + h_offset
    ttRect.centery = winSurf.get_rect().centery + ypos
    winSurf.blit(tt,ttRect)

def show_fade():
    print("SHOW FADE")
    fadeList = ["20","30","60","100","200","500","1000"]
    number_render(winSurf, 60,30,20,100)
    # def menu_render(textList,startPos,sepDist,fontSize=40,h_offset=0):

def display_settings():
    # settings has speed, blocksize, fade
    settingsList = ["Start Speed: s","Block Size: b","Fade: f"]
    menu_render(winSurf,settingsList,60,60,30)


def show_speed():
    pass

menuList = ["Start: a", "Settings: c"]

#Startup screen:
startup = True
settings = False
winSurf = pygame.display.set_mode((globals.WINWIDTH,globals.WINHEIGHT),0,32)
pygame.display.set_caption('Animation!!!!!!')
menu_render(winSurf,menuList,-200,100)
pygame.display.update()
settingShow = False

while startup:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.locals.KEYDOWN:
            if event.key == ord('a'):
                startup = False
            if event.key == ord('c'):
                settingShow = True
                display_settings()
                pygame.display.update()
            if event.key == pygame.locals.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if settingShow:
                if event.key == ord('f'):
                    show_fade()
                if event.key == ord('s'):
                    show_speed()
                pygame.display.update()