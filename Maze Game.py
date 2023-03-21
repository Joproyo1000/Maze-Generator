from sys import exit
import pygame

from mazeLevel import Maze
from settings import Settings
from debug import debug


class MazeGame:
    def __init__(self):

        # initialize settings
        self.settings = Settings()

        # general setup for pygame and display
        pygame.init()
        # changes screen mode to adapt if shaders are activated or not
        if self.settings.shadersOn:
            self.screen = pygame.display.set_mode(self.settings.RESOLUTION, pygame.OPENGL | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode(self.settings.RESOLUTION)

        # initialize maze
        self.maze = Maze(self.settings)

        pygame.display.set_caption('Maze Game')
        self.clock = pygame.time.Clock()

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

                for enemyEvent in self.maze.enemyEvents:
                    if event.type == enemyEvent:
                        self.maze.enemyBehavior()

            # run the level
            self.maze.run()

            debug("FPS : " + str(round(self.clock.get_fps() * 10) / 10))

            if not self.settings.shadersOn:
                pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)


if __name__ == '__main__':
    mazeGen = MazeGame()
    mazeGen.run()
