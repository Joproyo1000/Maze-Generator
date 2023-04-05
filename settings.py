import pygame
from screeninfo import get_monitors


class Settings:
    def __init__(self):
        # get screen
        self.screen = pygame.display.get_surface()

        # set size of screen
        self.WIDTH, self.HEIGHT = get_monitors()[0].width, get_monitors()[0].height

        # set size of maze for each level
        self.numLevels = 3
        self.MAZEWIDTHS, self.MAZEHEIGHTS = [0] * self.numLevels, [0] * self.numLevels
        for i in range(self.numLevels):
            self.MAZEWIDTHS[i], self.MAZEHEIGHTS[i] = (i+1) * 2000, (i+1) * 2000

        self.currentLevel = 0

        # set the resolution for the screen and the maze
        self.RESOLUTION = self.WIDTH, self.HEIGHT
        self.MAZERESOLUTION = self.MAZEWIDTHS[self.currentLevel], self.MAZEHEIGHTS[self.currentLevel]

        # set the tilesize in the maze (larger ones means smaller maze)
        self.TILESIZE = 120

        # randomness of the maze
        self.TURNFACTOR = 5

        # difficulty of the maze 0=easy 1=medium 2=hard
        self.DIFFICULTY = 0

        # proportion of enemies for a 1000*1000 maze
        self.WOLFPROPORTION = 0.5
        self.SPIDERPROPORTION = 1.5
        self.SLIMEPROPORTION = 3

        # initialize font
        self.font = pygame.font.Font('font/Pixeltype.ttf', self.HEIGHT//10)

        # colors
        self.WALLCOLOR = 'darkgreen'  # color of the wall on the map
        self.PATHCOLOR = 'green'  # color of the path on the map

        # lighting
        self.LIGHTCOLOR = (255, 255, 200)  # color of the light
        self.LIGHTRADIUS = 250 * self.TILESIZE//60  # size of the light
        self.LIGHTINTENSITY = 10  # intensity of the light

        # shaders
        self.shadersOn = False  # activate shader
        self.gamma = 20  # default gamma value

        # set FPS
        self.GAMEFPS = 60

        # initialize music
        self.music = pygame.mixer.Sound('sound/Horror3.1.mp3')
        self.volume = 0  # default volume

        # toggle heart beat effect in shaders
        self.showHeartBeatEffect = False

        # keep track of distance to the closest enemy
        self.dstToClosestEnemy = 1000000
