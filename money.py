import pygame
from pygame.locals import *

class money(pygame.sprite.Sprite):

    def __init__(self, x, y, bounds, foodLevel):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.loadImage()
        self.yoffset = 30

        self.rect = self.image.get_rect()
        self.rect.center = (x,y+self.yoffset)

        self.position = pygame.Vector2(self.rect.x,self.rect.y)
        self.velocity = pygame.Vector2(0,0)
        self.foodDriftSpeed = 0.00001
        self.price = 5

        self.bounds = bounds

        self.foodLevel = foodLevel
    

    def loadImage(self):

        self.fileName = "coin.png"

        try:
            image = pygame.image.load('images/'+ self.fileName).convert_alpha()

        except:
            raise pygame.error("Failed to load Image.")

        return image

    def updateRectPosition(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def updatePostion(self,dt):
        self.position += self.velocity * dt

    def updateVelocity(self, dt):
        self.velocity.y += self.foodDriftSpeed * dt

    def update(self, dt):
        self.updateVelocity(dt)
        self.updatePostion(dt)
        self.checkBounds()
        self.updateRectPosition()

    def checkBounds(self):

        if self.position.y > self.bounds[1]:
            self.kill()

    def kill(self):
        pygame.sprite.Sprite.kill(self)

    
    def click(self, mousePos):
        if(self.rect.collidepoint(mousePos)):
            self.kill()
            return self.foodLevel * self.price
        return 0