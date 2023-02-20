import pygame

""" PARAMETERS """

# set the resolution for the screen
RESOLUTION = WIDTH, HEIGHT = 1402, 802
MAZERESOLUTION = MAZEWIDTH, MAZEHEIGHT = 802, 802

# set the tilesize (larger ones means smaller maze)
TILESIZE = 50

# colors
# WALLCOLOR = pygame.Color('darkorange')
# PATHCOLOR = pygame.Color(50, 50, 50)
WALLCOLOR = pygame.Color('black')
PATHCOLOR = pygame.Color(10, 10, 10)

# set FPS
GAMEFPS = 60

""" ================================================== """
""" ONLY FOR DEBUGGING, MAKES THE MAZE GENERATE SLOWER """
RUNSLOW = False
RUNSLOWFPS = 30
""" ================================================== """
