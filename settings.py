import pygame

""" PARAMETERS """

# set the resolution for the screen
RESOLUTION = WIDTH, HEIGHT = 1402, 802
MAZERESOLUTION = MAZEWIDTH, MAZEHEIGHT = 502, 502

# set the tilesize (larger ones means smaller maze)
TILESIZE = 50

# set the linewidth (best set to 2)
LINEWIDTH = 2

# amount of 3D offset
OFFSET3D = 20

# colors
WALLCOLOR = pygame.Color('darkorange')
PATHCOLOR = pygame.Color(50, 50, 50)
MIDPATHCOLOR = pygame.Color(40, 40, 40)

# set FPS
GAMEFPS = 60

""" ================================================== """
""" ONLY FOR DEBUGGING, MAKES THE MAZE GENERATE SLOWER """
RUNSLOW = True
RUNSLOWFPS = 20
""" ================================================== """
