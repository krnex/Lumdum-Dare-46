# Import non-standard modules.
import pygame
from pygame.locals import *
import random
from hungerbar import hungerBar
from money import money

import sys

class BaseFish(pygame.sprite.Sprite):

    def __init__(self, x, y, bounds, money, value):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.loadImage()
        self.originalImage = self.loadImage()

        self.position = pygame.Vector2(x,y)
        self.maxVelocity = 0.2
        self.idleVelocity = 0.05
        self.velocity = pygame.math.Vector2(-0.05, 0.05)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.radius = 300

        self.bounds = bounds

        self.hunger = [0, 500, 0.01, 0.7] #current, max, rate, WhenToFindFood
        self.hungery = False
        self.directionChangeRate = 200;

        self.closestFood = None

        self.hungerbar = hungerBar((x,y), self.rect.width)

        self.dir = 1
        self.dirValue = self.rect.width
        self.dirVel = 10

        self.moneyGroup = money
        self.poopchance = 1000
        self.lastFoodLevel = 0

        self.price = value


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

    def update(self, dt):
        self.updateHunger(dt)
        self.checkBounds()
        self.changeDirection()
        self.updateVelocity()
        self.updateDirection()

        self.updatePostion(dt)
        self.updateRectPosition()

        self.hungerbar.update((self.position.x, self.position.y), self.hunger[0]/self.hunger[1])

    def draw(self, surface):

        self.hungerbar.draw(surface)

    def changeDirection(self):
        if(self.closestFood == None):
            if(random.randrange(0,self.directionChangeRate) == 1):
                self.idle()

    def flipX(self):
        self.velocity.x = self.velocity.x * -1

    def flipY(self):
        self.velocity.y = self.velocity.y * -1

    def checkBounds(self):
        if self.position.x > self.bounds[0]-self.rect.width:
            self.flipX()
        elif self.position.x < 0:
            self.flipX()
        
        if self.position.y > self.bounds[1]-self.rect.height:
            self.flipY()
        elif self.position.y < 0:
            self.flipY()

    def updateHunger(self, dt):
        self.hunger[0] += self.hunger[2] * dt
        if self.hunger[0] >= self.hunger[1]:
            self.kill()
        if self.hunger[0] >= self.hunger[1]*(1-self.hunger[3]):
            self.hungery = True
        else:
            self.hungery = False

        self.poopMoney()

    def updateVelocity(self):
        if self.closestFood != None:
            self.velocity = pygame.math.Vector2.normalize(self.closestFood.position - self.position) * self.maxVelocity

    def updateImageDirection(self):
        self.image = pygame.transform.flip(self.image, 1, 0)

    def kill(self):
        pygame.sprite.Sprite.kill(self)

    def findFood(self, foodGroup):
    
        self.closestFood = None
        if self.hungery == True:
            try:
                for food in foodGroup.sprites():
                    if pygame.sprite.collide_circle(self, food):
                        if self.closestFood not in foodGroup:
                            self.closestFood = food
                        elif self.position.distance_to(food.position) < self.position.distance_to(self.closestFood.position):
                            self.closestFood = food

                    if pygame.sprite.collide_rect(self, food):
                        self.eatFood(food)
            except TypeError as e:
                raise e
            except:
                raise pygame.error("Cannot get distances between fish and food.")

        if self.closestFood not in foodGroup:
            if pygame.math.Vector2.magnitude(self.velocity) > self.idleVelocity:
                self.idle()


    def idle(self):
        try:
            self.velocity.x = random.randint(-1,1)
            self.velocity.y = random.randint(-1,1)
            self.velocity = pygame.math.Vector2.normalize(self.velocity)*self.idleVelocity
        except ValueError as e:
            pass
                    
    def eatFood(self, food):

        self.hunger[0] = self.hunger[0] - food.satiation

        if self.hunger[0] < 0:
            self.hunger[0] = 0

        self.closestFood = None
        self.lastFoodLevel = food.foodValue
        food.kill()

    def updateDirection(self):
        if self.velocity.x > 0 and self.dir == -1:
            self.dirVel = -5
            if self.dirValue <= 0:
                self.dirVel = 5
                self.dir = 1

        elif self.velocity.x < 0 and self.dir == 1:
            self.dirVel = -5
            if self.dirValue <= 0:
                self.dirVel = 5
                self.dir = -1

        else:
            self.dirVel = 5

        self.dirValue += self.dirVel

        if self.dirValue > self.rect.width:
            self.dirValue = self.rect.width

        if self.dirValue < 0:
            self.dirValue = 0

        self.image = pygame.transform.smoothscale(self.originalImage, (self.dirValue,self.rect.height))

        if self.dir == -1:
            self.flipImage()
    
    def flipImage(self):
        self.image = pygame.transform.flip(self.image, 1, 0)

    def poopMoney(self):
        if (random.randint(1, self.poopchance) == 1 and self.lastFoodLevel != 0):
            poopmoney = money(self.rect.x, self.rect.y, self.bounds, self.lastFoodLevel)
            self.moneyGroup.add(poopmoney)
            self.lastFoodLevel = 0


class goldfish(BaseFish):

    def __init__(self, x, y, bounds, money, value):
        self.fileName = "goldfish.png"
        super().__init__(x, y, bounds, money, value)

        self.radius = 300
        self.maxVelocity = 0.2
        self.idleVelocity = 0.05
        self.directionChangeRate = 200
        self.poopchance = 300

        self.hunger = [0, 500, 0.01, 0.7]


class bettafish(BaseFish):

    def __init__(self, x, y, bounds, money, value):
        self.fileName = "betta.png"
        super().__init__(x, y, bounds, money, value)

        self.radius = 400
        self.maxVelocity = 0.3
        self.idleVelocity = 0.1
        self.directionChangeRate = 250
        self.poopchance = 100

        self.hunger = [0, 500, 0.01, 0.5]


class tetrafish(BaseFish):

    def __init__(self, x, y, bounds, money, value):
        self.fileName = "tetra.png"
        super().__init__(x, y, bounds, money, value)

        self.radius = 300
        self.maxVelocity = 0.4
        self.idleVelocity = 0.15
        self.directionChangeRate = 300
        self.poopchance = 200

        self.hunger = [0, 300, 0.01, 0.6]

class turtle(BaseFish):

    def __init__(self, x, y, bounds, money, value):
        self.fileName = "turtlr.png"
        super().__init__(x, y, bounds, money, value)

        self.radius = 1000
        self.maxVelocity = 0.01
        self.idleVelocity = 0.001
        self.directionChangeRate = 1
        self.poopchance = 10

        self.hunger = [0, 1000, 0.01, 1]


