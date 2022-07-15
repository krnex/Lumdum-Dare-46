import pygame
from pygame.locals import *

class player:

    def __init__(self):
        self.selectedButton = 1
        self.mouseButtons = [0,0]
        self.money = 9