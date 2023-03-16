import pygame
from support import Button, CheckButton, Slider


class Settings:
    def __init__(self, RESOLUTION, MAZERESOLUTION):
        # get screen
        self.screen = pygame.display.get_surface()

        # intitialize font
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)

        # get size of screen and maze
        self.WIDTH, self.HEIGHT = RESOLUTION[0], RESOLUTION[1]
        self.MAZEWIDTH, self.MAZEHEIGHT = MAZERESOLUTION[0], MAZERESOLUTION[1]

        # set the resolution for the screen
        self.RESOLUTION = self.WIDTH, self.HEIGHT
        self.MAZERESOLUTION = self.MAZEWIDTH, self.MAZEHEIGHT

        # set the tilesize (larger ones means smaller maze)
        self.TILESIZE = 120

        # randomness of the maze
        self.TURNFACTOR = 13

        # colors
        self.WALLCOLOR = 'darkgreen'
        self.PATHCOLOR = 'green'
        self.CURRENTCOLOR = 'red'

        # set FPS
        self.GAMEFPS = 60

        """ ================================================== """
        """ ONLY FOR DEBUGGING, MAKES THE MAZE GENERATE SLOWER """
        self.RUNSLOW = False
        self.RUNSLOWFPS = 30
        """ ================================================== """

        self.overlay = pygame.surface.Surface((self.WIDTH / 2, self.HEIGHT)).convert_alpha()
        self.overlay.fill(pygame.Color(200, 200, 200, 50))
        self.overlay_rect = self.overlay.get_rect(left=self.WIDTH / 2)

        self.generate()
        self.show = False

    def generate(self):
        self.title = self.font.render('Menu', False, 'white')
        self.title_rect = self.title.get_rect(center=(self.WIDTH * 3 / 4, 50))

        self.generate_button = Button(None, (self.WIDTH * 3 / 4, 150), 'Generate Maze', self.font, 'white', 'gray')

        self.tilesize_slider = Slider((self.WIDTH * 3 / 4, 250), 'Tile Size', (20, min(self.MAZERESOLUTION)//2), self.font, 'white', 'gray', 'gray', 'black', 3)
        self.tilesize_slider.value = self.TILESIZE
        self.tilesize_slider.slider_ball.centerx = self.tilesize_slider.ballPosFromValue()

        self.mazewidth_slider = Slider((self.WIDTH * 3 / 4, 350), 'Maze Width', (100, 5000), self.font, 'white', 'gray', 'gray', 'black', 3)
        self.mazewidth_slider.value = self.MAZEWIDTH
        self.mazewidth_slider.slider_ball.centerx = self.mazewidth_slider.ballPosFromValue()

        self.mazeheight_slider = Slider((self.WIDTH * 3 / 4, 450), 'Maze Height', (100, 5000), self.font, 'white', 'gray', 'gray', 'black', 3)
        self.mazeheight_slider.value = self.MAZEHEIGHT
        self.mazeheight_slider.slider_ball.centerx = self.mazeheight_slider.ballPosFromValue()

        self.turnfactor_slider = Slider((self.WIDTH * 3 / 4, 550), 'Turn Factor', (4, 20), self.font, 'white', 'gray', 'gray', 'black', 3)
        self.turnfactor_slider.value = self.TURNFACTOR
        self.turnfactor_slider.slider_ball.centerx = self.turnfactor_slider.ballPosFromValue()

        self.runslow_button = CheckButton(None, (self.WIDTH * 3 / 4, 650), 'Maze generates slowly', self.font, 'white', 'gray')
        self.runslow_button.value = self.RUNSLOW

    def switch(self):
        self.show = not self.show

    def blit(self):
        if self.show:
            self.screen.blit(self.overlay, self.overlay_rect)
            self.screen.blit(self.title, self.title_rect)

            self.generate_button.update(self.screen)
            self.tilesize_slider.update(self.screen)
            self.mazewidth_slider.update(self.screen)
            self.mazeheight_slider.update(self.screen)
            self.turnfactor_slider.update(self.screen)
            self.runslow_button.update(self.screen)

            self.TILESIZE = int(self.tilesize_slider.getValue())
            self.MAZEWIDTH = int(self.mazewidth_slider.getValue())
            self.MAZEHEIGHT = int(self.mazeheight_slider.getValue())
            self.TURNFACTOR = int(self.turnfactor_slider.getValue())

            self.runslow_button.value = self.RUNSLOW

    def run(self):
        self.blit()
