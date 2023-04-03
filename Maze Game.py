import time
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

        # initialize pygame and mixer
        pygame.init()
        pygame.mixer.init()

        # start music playback
        self.settings.music.play(loops=-1)
        self.settings.music.set_volume(self.settings.volume)

        # changes screen mode to adapt if shaders are activated or not
        if self.settings.shadersOn:
            self.screen = pygame.display.set_mode(self.settings.RESOLUTION, pygame.OPENGL | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode(self.settings.RESOLUTION)

        # initialize maze
        self.maze = Maze(self.settings)

        # initialize the render menus
        self.buttons = []
        if self.settings.shadersOn:
            self.shader = Shader(self.screen.get_size(), self.settings)

        pygame.display.set_caption('Maze Game')
        self.clock = pygame.time.Clock()

    def main_menu(self):
        """
        Main menu, runs at start
        """

        self.buttons = [Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.1), 'START GAME',
                               self.settings.font, 'darkgray', 'white'),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), 'PARAMETERS',
                               self.settings.font, 'darkgray', 'white'),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.3), 'QUIT GAME',
                               self.settings.font, 'darkgray', 'white')]

        self.draw_screen()


        transitionEnd(self.screen, self.shader if self.settings.shadersOn else None)

        while True:
            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.checkForInput():
                            if i == 0:
                                transitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                self.maze.reset()
                                self.game()
                            if i == 1:
                                transitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                self.settings_menu(self.main_menu)
                            if i == 2:
                                pygame.quit()
                                exit()

            self.draw_screen()

            if not self.settings.shadersOn:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def settings_menu(self, start: classmethod):
        """
        Settings menu to change game settings
        """

        sliderSize = self.settings.HEIGHT//230

        self.buttons = [Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 4), 'DIFFICULTY',
                               (0, 2), self.settings.font, 'darkgray', 'gray28', 'black', 'black', 'darkgray',
                               sliderSize, 0, custom={0: 'EASY', 1: 'MEDIUM', 2: 'HARD'}),
                        CheckButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 3.0), 'HEART BEAT EFFECT',
                                    self.settings.font, 'darkgray', 'gray'),
                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 2.2), 'GAMMA',
                               (5, 20), self.settings.font, 'darkgray', 'gray28', 'black', 'black', 'darkgray',
                               sliderSize, self.settings.gamma),
                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), 'VOLUME',
                               (0, 100), self.settings.font, 'darkgray', 'gray28', 'black', 'black', 'darkgray',
                               sliderSize, self.settings.volume),
                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 1.4), 'FPS',
                               (30, 120), self.settings.font, 'darkgray', 'gray28', 'black', 'black', 'darkgray',
                               sliderSize, 60),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.2), 'EXIT',
                               self.settings.font, 'darkgray', 'gray')]

        self.draw_screen()

        transitionEnd(self.screen, self.shader if self.settings.shadersOn else None)

        while True:
            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.checkForInput():
                            if i == len(self.buttons)-1:
                                transitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                self.settings.DIFFICULTY = int(self.buttons[0].value)
                                self.maze.FPS = self.buttons[4].value
                                start()

            self.settings.showHeartBeatEffect = self.buttons[1].value
            self.settings.gamma = self.buttons[2].value
            self.settings.volume = self.buttons[3].value
            self.settings.music.set_volume(self.settings.volume/100)

            self.draw_screen()

            if not self.settings.shadersOn:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def game(self):
        """
        Main game loop
        """

        self.maze.run(0)
        transitionEnd(self.screen, self.shader if self.settings.shadersOn else None)

        currentTime = time.time()

        while True:
            # calculate deltaTime to make the speed go at the same rate regardless of the FPS
            deltaTime = time.time() - currentTime
            currentTime = time.time()

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
                        self.pause_menu()

                # update all enemies
                dstsToPlayer = []
                for i, enemyEvent in enumerate(self.maze.enemyEvents):
                    if event.type == enemyEvent:
                        d = self.maze.enemyBehavior(i)
                        if d is not None:
                            dstsToPlayer.append(d)
                # keep track of closest enemy to player
                if len(dstsToPlayer) > 0:
                    closestEnemy = sorted(dstsToPlayer)[0]
                    self.settings.dstToClosestEnemy = closestEnemy

            # run the level
            self.maze.run(deltaTime)

            if not self.settings.shadersOn:
                pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)

    def pause_menu(self):
        """
        Pause menu, runs when escape is pressed
        """

        self.buttons = [Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.9),
                               'CONTINUE', self.settings.font, 'darkgray', 'white'),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.3),
                               'SETTINGS', self.settings.font, 'darkgray', 'white'),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7),
                               'EXIT TO MAIN MENU', self.settings.font, 'darkgray', 'white')]

        self.draw_screen()

        transitionEnd(self.screen, self.shader if self.settings.shadersOn else None)

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
                    for i, button in enumerate(self.buttons):
                        if button.checkForInput():
                            if i == 0:
                                transitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                self.maze.transition = 200
                                self.game()
                            elif i == 1:
                                transitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                self.settings_menu(self.pause_menu)
                            elif i == 2:
                                transitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                self.main_menu()

            self.draw_screen()

            if not self.settings.shadersOn:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def draw_screen(self):
        """
        Draws background, buttons and additional debug info for menus
        """
        # self.screen.fill(pygame.Color(46, 60, 87))
        self.screen.fill('white')

        # debug FPS count
        debug("FPS : " + str(round(self.clock.get_fps() * 10) / 10))

        for button in self.buttons:
            button.update(self.screen)


if __name__ == '__main__':
    mazeGen = MazeGame()
    mazeGen.game()
