import pygame
from sys import exit
from settings import *
from level import Level


class MazeGen:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        self.level = Level()

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

                # shows tile index when clicked on
                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed(3)
                    x, y = (((pygame.mouse.get_pos()[0] - self.level.offsetToCenterX) // TILESIZE) - 1) / 2, \
                           (((pygame.mouse.get_pos()[1] - self.level.offsetToCenterY) // TILESIZE) - 1) / 2
                    x, y = int(x), int(y)
                    print(x, y)
                    cell = self.level.check_cell(x, y)
                    if cell:
                        if buttons[1]:
                            print(" x position :", cell.rect.x, "\n", "y position :", cell.rect.y)
                            # print(cell.walls)

            # run the level
            self.level.run()

            # draw display
            pygame.display.update()

            # set FPS
            self.clock.tick(self.level.FPS)


if __name__ == '__main__':
    mazeGen = MazeGen()
    mazeGen.run()