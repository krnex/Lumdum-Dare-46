import pygame
from pygame.locals import *

class BaseFood(pygame.sprite.Sprite):

    def __init__(self, x, y, bounds, price):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.loadImage()

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.position = pygame.Vector2(self.rect.x,self.rect.y)
        self.velocity = pygame.Vector2(0,0)
        self.foodDriftSpeed = 0.00001
        self.satiation = 50
        self.foodValue = 1

        self.bounds = bounds

        self.price = price
    

    def loadImage(self):

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

class pelletfood(BaseFood):

    def __init__(self, x, y, bounds, price):
        self.fileName = "food.png"
        super().__init__(x, y, bounds, price)

        self.foodDriftSpeed = 0.00001
        self.satiation = 100
        self.foodValue = 1

class flakefood(BaseFood):

    def __init__(self, x, y, bounds, price):
        self.fileName = "flakes.png"
        super().__init__(x, y, bounds, price)

        self.foodDriftSpeed = 0.00002
        self.satiation = 200
        self.foodValue = 6

class goldfood(BaseFood):

    def __init__(self, x, y, bounds, price):
        self.fileName = "gold.png"
        super().__init__(x, y, bounds, price)

        self.foodDriftSpeed = 0.0001
        self.satiation = 1000
        self.foodValue = 30

