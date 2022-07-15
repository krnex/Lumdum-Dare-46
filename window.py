# PyGame template.
 
# Import standard modules.
import sys
 
# Import non-standard modules.
import pygame
from pygame.locals import *

import random

# User modules
from fish import *
from food import *
from ui import menu
from user import player
from background import Background

class window:

    def __init__(self):
        pygame.init()
        random.seed()
        
        # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
    
        # Set up the window.
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Feeding Frenzy!")
    
        # screen is the surface representing the window.
        # PyGame surfaces can be thought of as screen sections that you can draw onto.
        # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.
    
        # Main game loop.
        self.dt = 1/self.fps # dt is the time since last frame.


        # initalize sprite groups
        self.groupAllSprites = pygame.sprite.Group()
        self.groupFish = pygame.sprite.Group()
        self.groupFood = pygame.sprite.Group()
        self.groupBg = pygame.sprite.Group()
        self.groupMoney = pygame.sprite.Group()

        # Background
        bg = Background('background.png')
        self.groupBg.add(bg)
                
        #Initialzing Player
        self.player = player()

        #Initializing UI
        self.ui = menu(self.height, self.width, self.screen, self.player)

        #MM
        self.mm = True

        #running
        self.running = True

        #Game over
        self.gameover = True

    def run(self):
        """
        Main loop. All errors will be raised back to here.
        """
        # Main Menu
        while self.mm:
            self.updateMM()
            self.drawMM()

        # Game
        while self.running:
            try:
                self.update()
                self.draw()
                self.checkGameOver()
                self.dt = self.fpsClock.tick(self.fps)

            except Exception as e:
                print("{0}: {1}".format(type(e).__name__,str(e)))
        
        # Main Menu
        while self.gameover:
            self.updateGO()
            self.drawGO()

    def checkGameOver(self):
        if len(self.groupFish) == 0 and len(self.groupMoney) == 0 and self.player.money < 5:
            self.running = False

    def updateGO(self):
        for event in pygame.event.get():
            # We need to handle these events. Initially the only one you'll want to care
            # about is the QUIT event, because if you don't handle it, your game will crash
            # whenever someone tries to exit.
            if event.type == QUIT:
                self.close()
                # on other operating systems too, but I don't know for sure.
            if event.type == pygame.KEYDOWN:
                self.gameover = False
            # Handle other events as you wish.
        self.ui.updateGO()

    def drawGO(self):
        """
        Draw things to the window. Called once per frame.
        """
        self.groupBg.draw(self.screen)
        self.ui.drawGO(self.screen)

        pygame.display.flip()



    def updateMM(self):
        for event in pygame.event.get():
            # We need to handle these events. Initially the only one you'll want to care
            # about is the QUIT event, because if you don't handle it, your game will crash
            # whenever someone tries to exit.
            if event.type == QUIT:
                self.close()
                # on other operating systems too, but I don't know for sure.
            if event.type == pygame.KEYDOWN:
                self.mm = False
            # Handle other events as you wish.
        self.ui.updateMM()

    def drawMM(self):
        """
        Draw things to the window. Called once per frame.
        """
        self.groupBg.draw(self.screen)
        self.ui.drawMM(self.screen)

        pygame.display.flip()


 
    def update(self):
        """
        Update game. Called once per frame.
        dt is the amount of time passed since last frame.
        If you want to have constant apparent movement no matter your framerate,
        what you can do is something like
        
        x += v * dt
        
        and this will scale your velocity based on time. Extend as necessary."""
        
        # Go through events that are passed to the script by the window.
        for event in pygame.event.get():
            # We need to handle these events. Initially the only one you'll want to care
            # about is the QUIT event, because if you don't handle it, your game will crash
            # whenever someone tries to exit.
            if event.type == QUIT:
                self.close()
                # on other operating systems too, but I don't know for sure.
            # Handle other events as you wish.

            if event.type == pygame.MOUSEBUTTONDOWN:
                if(event.button == 3):
                    self.click()
                if(event.button == 1):
                    button = self.ui.click(pygame.mouse.get_pos())
                    if button != None:
                        self.player.selectedButton = self.ui.click(pygame.mouse.get_pos())
                    for money in self.groupMoney.sprites():
                        self.player.money += money.click(pygame.mouse.get_pos())

        self.groupMoney.update(self.dt)
        
        self.groupAllSprites.update(self.dt)

        for fish in self.groupFish.sprites():
            fish.findFood(self.groupFood)

        self.ui.update()
 
    def draw(self):
        """
        Draw things to the window. Called once per frame.
        """
        self.groupBg.draw(self.screen)
        # Flip the display so that the things we drew actually show up.
        self.groupAllSprites.draw(self.screen)

        for fish in self.groupFish:
            fish.draw(self.screen)

        self.groupMoney.draw(self.screen)
    
        self.ui.draw(self.screen)

        pygame.display.flip()


    def close(self):
        pygame.quit() # Opposite of pygame.init
        sys.exit() # Not including this line crashes the script on Windows. Possibly

    def createFood(self, pos):

        pricePellet = 3
        priceFlake = 25
        priceGold = 100

        if(self.player.selectedButton == 0 and self.player.money >= pricePellet):
            food = pelletfood(pos[0], pos[1], (self.width, self.height), pricePellet)
        elif(self.player.selectedButton == 2 and self.player.money >= priceFlake):
            food = flakefood(pos[0], pos[1], (self.width, self.height), priceFlake)
        elif(self.player.selectedButton == 4 and self.player.money >= priceGold):
            food = goldfood(pos[0], pos[1], (self.width, self.height), priceGold)
        else:
            return
        self.player.money = self.player.money - food.price
        self.groupFood.add(food)
        self.groupAllSprites.add(food)

    def createFish(self, pos): 

        priceGoldfish = 5
        priceTetra = 30
        priceBetta = 75
        priceTurtle = 1000

        if(self.player.selectedButton == 1 and self.player.money >= priceGoldfish):
            fish = goldfish(pos[0], pos[1], (self.width, self.height*(1-self.ui.uiScale)), self.groupMoney, priceGoldfish)
        elif(self.player.selectedButton == 5 and self.player.money >= priceBetta):
            fish = bettafish(pos[0], pos[1], (self.width, self.height*(1-self.ui.uiScale)), self.groupMoney, priceBetta)
        elif(self.player.selectedButton == 3 and self.player.money >= priceTetra):
            fish = tetrafish(pos[0], pos[1], (self.width, self.height*(1-self.ui.uiScale)), self.groupMoney, priceTetra)
        elif(self.player.selectedButton == 7 and self.player.money >= priceTurtle):
            fish = turtle(pos[0], pos[1], (self.width, self.height*(1-self.ui.uiScale)), self.groupMoney, priceTurtle)
        else: 
            return
        self.player.money = self.player.money - fish.price
        self.groupFish.add(fish)
        self.groupAllSprites.add(fish)


    def click(self):
        if(self.player.selectedButton % 2 == 0):
            self.createFood(pygame.mouse.get_pos())
        elif(self.player.selectedButton % 2 == 1):
            self.createFish(pygame.mouse.get_pos())