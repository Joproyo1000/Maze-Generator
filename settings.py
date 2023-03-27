import pygame
from support import Button, CheckButton, Slider


class Settings:
    def __init__(self):
        # get screen
        self.screen = pygame.display.get_surface()

        # set size of screen
        self.WIDTH, self.HEIGHT = 1400, 800

        # set size of maze for each level
        self.numLevels = 3
        self.MAZEWIDTHS, self.MAZEHEIGHTS = [0] * self.numLevels, [0] * self.numLevels
        for i in range(self.numLevels):
            self.MAZEWIDTHS[i], self.MAZEHEIGHTS[i] = (i+1) * 2000, (i+1) * 2000

        self.currentLevel = 0

        # set the resolution for the screen
        self.RESOLUTION = self.WIDTH, self.HEIGHT
        self.MAZERESOLUTION = self.MAZEWIDTHS[self.currentLevel], self.MAZEHEIGHTS[self.currentLevel]

        # set the tilesize (larger ones means smaller maze)
        self.TILESIZE = 120

        # randomness of the maze
        self.TURNFACTOR = 10

        # colors
        self.WALLCOLOR = 'darkgreen'
        self.PATHCOLOR = 'green'

        # lighting
        self.LIGHTCOLOR = (255, 255, 200)
        self.LIGHTRADIUS = 250 * self.TILESIZE//60
        self.LIGHTINTENSITY = 40

        # shaders
        self.shadersOn = True

        # set FPS
        self.GAMEFPS = 60
