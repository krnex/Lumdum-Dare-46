import pygame
from pygame.locals import *

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/"+image_file)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0