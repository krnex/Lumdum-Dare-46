import pygame

class menu:
    def __init__(self, height, width, surface, player):

        self.uiScale = 0.2

        self.player = player

        self.height = height
        self.width = width

        self.spriteGroup = pygame.sprite.Group()
        self.buttonGroup = pygame.sprite.Group()
        self.mmGroup = pygame.sprite.Group()

        #mm
        self.title = text(int(width * 2/3), int(height * 1/3), (0,0,0), 100, 0, 0)
        self.titlecont = text(int(width * 2/3), int(height * 1/3), (0,0,0), 20, 0, 125)

        #bottom bar
        self.bottomBar = bar(height, width, self.uiScale)
        self.spriteGroup.add(self.bottomBar)

        #score
        self.scoreText = text(width, 0, (0,0,0), 40, -10, 10)

        #pellet button
        self.baitButton = button(0, 0, 100, ((height*self.uiScale)-50)/2, height*(1-self.uiScale), "food.png", 0, 3)
        self.buttonGroup.add(self.baitButton)
        self.spriteGroup.add(self.baitButton)

        #goldfish Button
        self.goldfishButton = button(0, 1, 100, ((height*self.uiScale)-50)/2, height*(1-self.uiScale), "goldfish.png", 1, 5)
        self.goldfishButton.isSelected = True
        self.spriteGroup.add(self.goldfishButton)
        self.buttonGroup.add(self.goldfishButton)

        #flake button
        self.fishButton = button(1, 0, 100, ((height*self.uiScale)-50)/2, height*(1-self.uiScale), "flakes.png", 2, 25)
        self.spriteGroup.add(self.fishButton)
        self.buttonGroup.add(self.fishButton)

        #tetra Button
        self.tetraButton = button(1, 1, 100, ((height*self.uiScale)-50)/2, height*(1-self.uiScale), "tetra.png", 3, 30)
        self.spriteGroup.add(self.tetraButton)
        self.buttonGroup.add(self.tetraButton)

        #gold Button
        self.goldButton = button(2, 0, 100, ((height*self.uiScale)-50)/2, height*(1-self.uiScale), "gold.png", 4, 100)
        self.spriteGroup.add(self.goldButton)
        self.buttonGroup.add(self.goldButton)

        #betta
        self.bettaButton = button(2, 1, 100, ((height*self.uiScale)-50)/2, height*(1-self.uiScale), "betta.png", 5, 75)
        self.spriteGroup.add(self.bettaButton)
        self.buttonGroup.add(self.bettaButton)

        #betta
        self.turtlebutton = button(3, 1, 100, ((height*self.uiScale)-50)/2, height*(1-self.uiScale), "turtlr.png", 7, 1000)
        self.spriteGroup.add(self.turtlebutton)
        self.buttonGroup.add(self.turtlebutton)

    def update(self):
        self.spriteGroup.update()
        self.scoreText.update(str(self.player.money))

    def draw(self, surface):
        self.spriteGroup.draw(surface)
        self.scoreText.draw(surface)

        for button in self.buttonGroup:
            button.draw(surface)

    def updateMM(self):
        self.title.update("Fishing Frenzy!")
        self.titlecont.update("Press any button to continue.")
        
    def drawMM(self, surface):
        self.title.draw(surface)
        self.titlecont.draw(surface)

    def updateGO(self):
        self.title.update("Game Over.")
        self.titlecont.update("Press any button to close.")
        
    def drawGO(self, surface):
        self.title.draw(surface)
        self.titlecont.draw(surface)


    def click(self, mousePos):
        for sprite in self.buttonGroup.sprites():
            if(sprite.rect.collidepoint(mousePos)):
                for otherSprite in self.buttonGroup.sprites():
                    if otherSprite != sprite:
                        otherSprite.isSelected = False
                sprite.isSelected = True
                return sprite.itemNumber

class bar(pygame.sprite.Sprite):
    def __init__(self, height, width, uiscale):
        pygame.sprite.Sprite.__init__(self)

        self.size = uiscale

        self.height = height * self.size
        self.width = width
        self.pos = (0, height * (1-self.size))
        self.color = pygame.Color(44, 130, 255, 200)
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

class button(pygame.sprite.Sprite):
    def __init__(self, xNum, yNum, width, height, yOffset, image, itemNumber, cost):
        pygame.sprite.Sprite.__init__(self)

        self.height = height
        self.width = width

        self.xNum = xNum
        self.yNum = yNum

        self.padding = 20

        self.pos = ((self.xNum)*self.width + self.padding*(self.xNum+1), yOffset + (self.yNum)*self.height + self.padding*(self.yNum+1))
        self.colorInactive = pygame.Color(200, 200, 200)
        self.colorActive = pygame.Color(0,255,0)
        self.color = self.colorInactive
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)

        self.fishImage = pygame.image.load('images/'+ image).convert_alpha()
        self.imgRect = self.fishImage.get_rect()

        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.cost = str(cost)

        self.text = text(self.rect.topright[0], self.rect.topright[1], (0,0,0), 12, -2, 0)

        self.isSelected = False
        self.itemNumber = itemNumber

    def update(self):
        if self.isSelected == True:
            self.color = self.colorActive
        else:
            self.color = self.colorInactive

        self.image.fill(self.color)
        self.text.update(self.cost)

    def draw(self, surface):
        surface.blit(self.fishImage, (self.rect.center[0] - self.imgRect.width/2, self.rect.center[1] - self.imgRect.height/2))
        self.text.draw(surface)

class text(pygame.sprite.Sprite):

    def __init__(self, x, y, color, size, xOffset, yOffset):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        self.color = color
        self.size = size
        self.font = pygame.font.Font('font/Brightly Crush Shine.otf', self.size)
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.x = x
        self.y = y
        self.text = self.font.render("money", True, self.color)
        self.rect = self.text.get_rect()

    def update(self, words):
        self.text = self.font.render(words, True, self.color)
        self.rect = self.text.get_rect()
        self.rect.topright = (self.x + self.xOffset, self.y + self.yOffset)

    def draw(self, surface):
        surface.blit(self.text, self.rect)
