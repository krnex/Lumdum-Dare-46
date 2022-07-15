import pygame
from pygame.locals import *

class hungerBar:

    def __init__(self, pos, width):
        self.pos = pos
        self.yoffset = -10
        self.color = pygame.Color(0,255,0,125)
        self.backgroundColor = pygame.Color(0,0,0,125)
        self.width = width
        self.height = 5
        self.rect = pygame.Rect(pos[0], pos[1] + self.yoffset, self.width, self.height-2)
        self.backgroundRect = pygame.Rect(pos[0], pos[1] + self.yoffset, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.backgroundColor, self.backgroundRect, 1)
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self, pos, hungerPercent):
        self.rect.x = pos[0] + 1
        self.rect.y = pos[1] + self.yoffset + 1
        self.rect.width = (self.width - 1) * (1 - hungerPercent) 
        self.backgroundRect.x = pos[0]
        self.backgroundRect.y = pos[1] + self.yoffset
