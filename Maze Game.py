from sys import exit
from settings import *
from mazeLevel import Maze
from debug import debug


class MazeGame:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Maze Game')
        self.clock = pygame.time.Clock()

        self.maze = Maze()

    def run(self):

        while True:
            # set background color
            self.screen.fill(pygame.Color("darkslategray"))

            # used for taking inputs
            for event in pygame.event.get():
                # closes the game if the red cross button is pressed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # run the level
            self.maze.run()

            debug("FPS : " + str(round(self.clock.get_fps() * 10) / 10))

            # draw display
            pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)


if __name__ == '__main__':
    mazeGen = MazeGame()
    mazeGen.run()