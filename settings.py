import pygame
from screeninfo import get_monitors


class Settings:
    def __init__(self):
        """
        Settings of the maze
        """
        # get screen
        self.screen = pygame.display.get_surface()

        # activate shader
        self.SHADERON = False

        # set size of screen
        self.WIDTH, self.HEIGHT = get_monitors()[0].width, get_monitors()[0].height

        # set size of maze for each level
        self.NUMLEVELS = 3
        self.MAZEWIDTHS, self.MAZEHEIGHTS = [0] * self.NUMLEVELS, [0] * self.NUMLEVELS
        for i in range(self.NUMLEVELS):
            self.MAZEWIDTHS[i], self.MAZEHEIGHTS[i] = (i+1) * 3200, (i+1) * 2000

        self.CURRENTLEVEL = 0

        # set the resolution for the screen and the maze
        self.RESOLUTION = self.WIDTH, self.HEIGHT
        self.MAZERESOLUTION = self.MAZEWIDTHS[self.CURRENTLEVEL], self.MAZEHEIGHTS[self.CURRENTLEVEL]

        # set the tilesize in the maze (larger ones means smaller maze)
        self.TILESIZE = 120

        # randomness of the maze
        self.TURNFACTOR = 5

        # difficulty of the maze 0=easy 1=medium 2=hard
        self.DIFFICULTY = 0

        # proportion of enemies for a 1000*1000 maze
        self.WOLFPROPORTION = 0.125
        self.SPIDERPROPORTION = 0.375
        self.SLIMEPROPORTION = 0.5
        self.RABBITPROPORTION = 0.2

        # initialize font
        self.FONT = pygame.font.Font('font/Pixeltype.ttf', self.HEIGHT // 10)
        self.BIGCREEPYFONT = pygame.font.Font('font/HelpMe.ttf', 130)
        self.SMALLCREEPYFONT = pygame.font.Font('font/HelpMe.ttf', 100)

        # controls
        self.K_UP = pygame.K_z
        self.K_DOWN = pygame.K_s
        self.K_LEFT = pygame.K_q
        self.K_RIGHT = pygame.K_d
        self.K_MAP = pygame.K_m

        # colors
        self.MENUBACKGROUNDCOLOR = pygame.Color(46, 60, 87)
        self.TEXTCOLOR = 'darkgray'
        self.HOVERINGCOLOR = 'gray'
        self.SLIDEREXTCOLOR = 'gray28'
        self.SLIDERINTCOLOR = 'black'

        self.WALLCOLOR = 'gold4' if self.SHADERON else pygame.Color(163, 128, 83)  # color of the wall on the map
        self.PATHCOLOR = 'goldenrod4' if self.SHADERON else 'burlywood'  # color of the path on the map
        self.PLAYERCOLOR = 'blue'  # color of the player on the map
        self.ENDCOLOR = 'gold'  # color of the end on the map
        self.CHESTCOLOR = 'chocolate4' if self.SHADERON else pygame.Color(117, 79, 46)  # color of chests on the map

        # lighting
        self.LIGHTCOLOR = (255, 255, 200)  # color of the light
        self.LIGHTRADIUS = 250 * self.TILESIZE//60  # size of the light
        self.LIGHTINTENSITY = 10  # intensity of the light

        # toggle heart beat effect in shaders
        self.SHOWHEARTBEATEFFECT = True

        # shaders
        self.GAMMA = 10  # default gamma value

        # set FPS
        self.GAMEFPS = 60

        # initialize music
        self.MUSIC = pygame.mixer.Sound('sound/Horror3.1.mp3')
        self.VOLUME = 0  # default volume

        # type of the player, either boy or girl
        self.TYPE = 'girl'

        # translations of the texts
        self.LANGUAGE = 'FR'
        self.TEXTS = {
            'FR': {'The Maze Of Shadows': 'Le Labyrinthe Des Ombres',
                   'START': 'COMMENCER',
                   'PARAMETERS': 'PARAMETRES',
                   'QUIT GAME': 'QUITTER LE JEU',
                   'QUIT': 'QUITTER',
                   'DIFFICULTY': 'DIFFICULTEE',
                   'EASY': 'FACILE',
                   'MEDIUM': 'MOYEN',
                   'HARD': 'DIFFICILE',
                   'HEART BEAT EFFECT': 'EFFET BATTEMENTS DE COEUR',
                   'GAMMA': 'GAMMA',
                   'VOLUME': 'VOLUME',
                   'FPS': 'FPS',
                   'CONTROLS': 'CONTROLES',
                   'UP': 'HAUT',
                   'DOWN': 'BAS',
                   'LEFT': 'GAUCHE',
                   'RIGHT': 'DROITE',
                   'MAP': 'CARTE',
                   'Waiting for input...': 'Appuyez sur une touche...',
                   'CONTINUE': 'CONTINUER',
                   'MAIN MENU': 'MENU PRINCIPAL',
                   'BOY': 'GARCON',
                   'GIRL': 'FILLE',
                   'CANCEL': 'ANNULER',
                   'YOU HAVE FOUND': 'VOUS AVEZ TROUVE',
                   'YOU HAVE USED': 'VOUS AVEZ UTILISEZ',
                   'YOU HAVE REFOUND': 'VOUS AVEZ RETROUVE',
                   'YOUR BROTHER': 'VOTRE FRERE',
                   'YOUR SISTER': 'VOTRE SOEUR',
                   'YOU DIED': 'VOUS ETES MORT',
                   'LIVES': 'VIES',
                   'A PIECE OF MAP': 'UN BOUT DE CARTE',
                   'A FREEZE ITEM': 'UN GEL',
                   'AN EXTRA LIFE': 'UNE VIE EN PLUS'},
            'EN': {'The Maze Of Shadows': 'The Maze Of Shadows',
                   'START': 'START',
                   'PARAMETERS': 'PARAMETERS',
                   'QUIT GAME': 'QUIT GAME',
                   'QUIT': 'QUIT',
                   'DIFFICULTY': 'DIFFICULTY',
                   'EASY': 'EASY',
                   'MEDIUM': 'MEDIUM',
                   'HARD': 'HARD',
                   'HEART BEAT EFFECT': 'HEART BEAT EFFECT',
                   'GAMMA': 'GAMMA',
                   'VOLUME': 'VOLUME',
                   'FPS': 'FPS',
                   'CONTROLS': 'CONTROLS',
                   'UP': 'UP',
                   'DOWN': 'DOWN',
                   'LEFT': 'LEFT',
                   'RIGHT': 'RIGHT',
                   'MAP': 'MAP',
                   'Waiting for input...': 'Waiting for input...',
                   'CONTINUE': 'CONTINUE',
                   'MAIN MENU': 'MAIN MENU',
                   'BOY': 'BOY',
                   'GIRL': 'GIRL',
                   'CANCEL': 'CANCEL',
                   'YOU FOUND': 'YOU FOUND',
                   'YOU USED': 'YOU USED',
                   'YOU REFOUND': 'YOU FOUND',
                   'YOUR BROTHER': 'YOUR BROTHER',
                   'YOUR SISTER': 'YOUR SISTER',
                   'YOU DIED': 'YOU DIED',
                   'LIVES': 'LIVES',
                   'A PIECE OF MAP': 'A PIECE OF MAP',
                   'A FREEZE ITEM': 'A FREEZE ITEM',
                   'AN EXTRA LIFE': 'AN EXTRA LIFE'},
            'DE': {'The Maze Of Shadows': 'Le Labyrinthe Des Ombres',
                   'START': '',
                   'PARAMETERS': '',
                   'QUIT GAME': '',
                   'QUIT': '',
                   'DIFFICULTY': '',
                   'EASY': '',
                   'MEDIUM': '',
                   'HARD': '',
                   'HEART BEAT EFFECT': '',
                   'GAMMA': '',
                   'VOLUME': '',
                   'FPS': '',
                   'CONTROLS': '',
                   'UP': '',
                   'DOWN': '',
                   'LEFT': '',
                   'RIGHT': '',
                   'MAP': '',
                   'Waiting for input...': '',
                   'CONTINUE': '',
                   'MAIN MENU': '',
                   'BOY': '',
                   'GIRL': '',
                   'CANCEL': '',
                   'YOU FOUND': '',
                   'YOU USED': '',
                   'YOU REFOUND': '',
                   'YOUR BROTHER': '',
                   'YOUR SISTER': '',
                   'YOU DIED': '',
                   'LIVES': '',
                   'A PIECE OF MAP': '',
                   'A FREEZE ITEM': '',
                   'AN EXTRA LIFE': ''}
        }

        # keep track of distance to the closest enemy
        self.dstToClosestEnemy = 1000000
