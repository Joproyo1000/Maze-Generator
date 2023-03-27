from sys import exit
import pygame

from mazeLevel import Maze
from settings import Settings
from shaders import Shader
from debug import debug
from support import Button, CheckButton, Slider, transitionStart, transitionEnd


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

        # initialize to render menus
        self.shader = Shader(self.screen.get_size())

        pygame.display.set_caption('Maze Game')
        self.clock = pygame.time.Clock()

    def game(self):
        """
        Main game loop
        """

        while True:
            # set background color
            self.screen.fill(pygame.Color(46, 60, 87))

            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # update all enemies
                for enemyEvent in self.maze.enemyEvents:
                    if event.type == pygame.KEYDOWN:
                        key = pygame.key.get_pressed()
                        if key[pygame.K_ESCAPE]:
                            self.settings_menu()

                    if event.type == enemyEvent:
                        self.maze.enemyBehavior()

            # run the level
            self.maze.run()

            # debug FPS count
            debug("FPS : " + str(round(self.clock.get_fps() * 10) / 10))

            if not self.settings.shadersOn:
                pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)

    def main_menu(self):
        """
        Main menu, runs at start
        """

        startButton = Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2), 'START GAME', self.settings.font, 'gray', 'white')

        while True:
            # set background color
            self.screen.fill(pygame.Color(46, 60, 87))

            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if startButton.checkForInput():
                        transitionStart(self.screen, self.shader)
                        self.maze.reset()
                        self.game()

            startButton.update(self.screen)

            # debug FPS count
            debug("FPS : " + str(round(self.clock.get_fps() * 10) / 10))

            if not self.settings.shadersOn:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def settings_menu(self):
        """
        Settings menu, runs when escape is pressed
        """

        continueButton = Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.3), 'CONTINUE', self.settings.font, 'gray', 'white')
        exitButton = Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), 'EXIT TO MAIN MENU', self.settings.font, 'gray', 'white')

        while True:
            # set background color
            self.screen.fill(pygame.Color(46, 60, 87))

            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_ESCAPE]:
                        self.game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exitButton.checkForInput():
                        transitionStart(self.screen, self.shader)
                        self.main_menu()
                    if continueButton.checkForInput():
                        self.game()

            exitButton.update(self.screen)
            continueButton.update(self.screen)

            # debug FPS count
            debug("FPS : " + str(round(self.clock.get_fps() * 10) / 10))

            if not self.settings.shadersOn:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)


if __name__ == '__main__':
    mazeGen = MazeGame()
    mazeGen.main_menu()
