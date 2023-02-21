from sys import exit
import pygame
from mazeLevel import Maze
from mazeMenu import Menu
from debug import debug



class MazeGame:
    def __init__(self):

        # set the resolution for the screen
        self.RESOLUTION = 1402, 802
        self.MAZERESOLUTION = 802, 802

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.RESOLUTION))
        pygame.display.set_caption('Maze Game')
        self.clock = pygame.time.Clock()

        self.menu = Menu(self.RESOLUTION, self.MAZERESOLUTION)
        self.maze = Maze(self.menu)

    def run(self):

        while True:
            # set background color
            self.screen.fill(pygame.Color(10, 10, 10))

            # used for taking inputs
            for event in pygame.event.get():
                # closes the game if the red cross button is pressed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.switch()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if self.menu.generate_button.checkForInput():
                            self.maze.reset()
                        if self.menu.runslow_button.checkForInput():
                            self.menu.RUNSLOW = not self.menu.RUNSLOW

            # run the level
            self.maze.run()
            self.menu.run()

            debug("FPS : " + str(round(self.clock.get_fps() * 10) / 10))

            # draw display
            pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)


if __name__ == '__main__':
    mazeGen = MazeGame()
    mazeGen.run()