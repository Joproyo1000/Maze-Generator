from sys import exit
import pygame

from mazeLevel import Maze
from settings import Settings
from debug import debug

class MazeGame:
    def __init__(self):

        # set the resolution for the screen
        self.RESOLUTION = 1400, 800
        self.MAZERESOLUTION = 800, 800

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode(self.RESOLUTION, pygame.OPENGL | pygame.DOUBLEBUF)
        # self.screen = pygame.display.set_mode(self.RESOLUTION)
        pygame.display.set_caption('Maze Game')
        self.clock = pygame.time.Clock()

        # initialize settings and maze objects
        self.settings = Settings(self.RESOLUTION, self.MAZERESOLUTION)
        self.maze = Maze(self.settings)

    def run(self):

        while True:
            # set background color
            self.screen.fill(pygame.Color(0, 0, 0))

            # used for taking inputs
            for event in pygame.event.get():
                # closes the game if the red cross button is pressed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.settings.switch()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if self.settings.generate_button.checkForInput():
                            self.maze.reset()
                        if self.settings.runslow_button.checkForInput():
                            self.settings.RUNSLOW = not self.settings.RUNSLOW

            # run the level
            self.maze.run()
            self.settings.run()

            debug("FPS : " + str(round(self.clock.get_fps() * 10) / 10))

            # pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)


if __name__ == '__main__':
    mazeGen = MazeGame()
    mazeGen.run()
