import time

from sys import exit

import pygame

from mazeLevel import Maze
from settings import Settings
from shaders import Shader
from debug import debug
from support import *


class MazeGame:
    def __init__(self):

        # initialize settings
        self.settings = Settings()

        # initialize pygame and mixer
        pygame.init()
        pygame.mixer.init()

        # start music playback
        self.settings.MUSIC.play(loops=-1)
        self.settings.MUSIC.set_volume(self.settings.VOLUME)

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
                               self.settings.FONT, 'darkgray', 'white'),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), 'PARAMETERS',
                               self.settings.FONT, 'darkgray', 'white'),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.3), 'QUIT GAME',
                               self.settings.FONT, 'darkgray', 'white')]

        self.draw_screen()


        fadeTransitionEnd(self.screen, self.shader if self.settings.shadersOn else None)

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
                                fadeTransitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                self.maze.reset()
                                self.game()
                            if i == 1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.shadersOn else None)
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
                               (0, 2), self.settings.FONT, 'darkgray', 'gray28', 'black', 'black', 'darkgray',
                               sliderSize, 0, custom={0: 'EASY', 1: 'MEDIUM', 2: 'HARD'}),
                        CheckButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 3.0), 'HEART BEAT EFFECT',
                                    self.settings.SHOWHEARTBEATEFFECT, self.settings.FONT, 'darkgray', 'gray'),
                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 2.2), 'GAMMA',
                               (5, 20), self.settings.FONT, 'darkgray', 'gray28', 'black', 'black', 'darkgray',
                               sliderSize, self.settings.GAMMA),
                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), 'VOLUME',
                               (0, 100), self.settings.FONT, 'darkgray', 'gray28', 'black', 'black', 'darkgray',
                               sliderSize, self.settings.VOLUME),
                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 1.4), 'FPS',
                               (30, 120), self.settings.FONT, 'darkgray', 'gray28', 'black', 'black', 'darkgray',
                               sliderSize, 60),
                        Button(None, (self.settings.WIDTH // 1.4, self.settings.HEIGHT // 1.2), 'CONTROLS ->',
                               self.settings.FONT, 'darkgray', 'gray'),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.2), 'EXIT',
                               self.settings.FONT, 'darkgray', 'gray')]

        self.draw_screen()

        # fadeTransitionEnd(self.screen, self.shader if self.settings.shadersOn else None)

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
                                fadeTransitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                self.settings.DIFFICULTY = int(self.buttons[0].value)
                                self.maze.FPS = self.buttons[4].value
                                start()
                            if i == len(self.buttons)-2:
                                self.controls_menu(start)

            # self.settings.SHOWHEARTBEATEFFECT = self.buttons[1].value
            # self.settings.GAMMA = self.buttons[2].value
            # self.settings.VOLUME = self.buttons[3].value
            # self.settings.MUSIC.set_volume(self.settings.VOLUME / 100)
            self.settings.VOLUME = self.buttons[0].value

            self.draw_screen()

            if not self.settings.shadersOn:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def controls_menu(self, start: classmethod):
        """
        Settings menu to change game controls
        """

        self.buttons = [InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 4.5), 'UP : ',
                                    self.settings.K_UP, self.settings.FONT, 'darkgray', 'gray'),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 3), 'DOWN : ',
                                    self.settings.K_DOWN, self.settings.FONT, 'darkgray', 'gray'),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.2), 'LEFT : ',
                                    self.settings.K_LEFT, self.settings.FONT, 'darkgray', 'gray'),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), 'RIGHT : ',
                                    self.settings.K_RIGHT, self.settings.FONT, 'darkgray', 'gray'),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.4), 'MAP : ',
                                    self.settings.K_MAP, self.settings.FONT, 'darkgray', 'gray'),
                        Button(None, (self.settings.WIDTH // 3.5, self.settings.HEIGHT // 1.2), '<- PARAMETERS',
                               self.settings.FONT, 'darkgray', 'gray'),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.2), 'EXIT',
                               self.settings.FONT, 'darkgray', 'gray')]

        self.draw_screen()

        while True:
            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.checkForInput():
                            if i == len(self.buttons) - 1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                start()
                            if i == len(self.buttons) - 2:
                                self.settings_menu(start)

            self.settings.K_UP = self.buttons[0].key
            self.settings.K_DOWN = self.buttons[1].key
            self.settings.K_LEFT = self.buttons[2].key
            self.settings.K_RIGHT = self.buttons[3].key
            self.settings.K_MAP = self.buttons[4].key
            self.draw_screen()

            if not self.settings.shadersOn:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def game(self, doTransition=True):
        """
        Main game loop
        """

        if doTransition:
            self.maze.run(0)
            fadeTransitionEnd(self.screen, self.shader if self.settings.shadersOn else None)

        currentTime = time.time()

        while True:
            # calculate deltaTime to make the speed go at the same rate regardless of FPS
            deltaTime = time.time() - currentTime
            currentTime = time.time()

            # set background color
            self.screen.fill(pygame.Color(46, 60, 87))

            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # inventory
                if event.type == pygame.MOUSEWHEEL:
                    self.maze.player.currentItemIndex = (self.maze.player.currentItemIndex + event.y) % len(self.maze.player.inventory)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.maze.playerUse()

                # menus
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[self.settings.K_MAP]:
                        self.map()
                    if key[pygame.K_ESCAPE]:
                        self.pause_menu()

                # update all enemies
                dstsToPlayer = []
                for i, enemyEvent in enumerate(self.maze.enemyEvents):
                    if event.type == enemyEvent:
                        d = self.maze.enemyBehavior(i)
                        if d is not None:
                            dstsToPlayer.append(d)
            # keep track of the closest enemy to player
            if len(dstsToPlayer) > 0:
                closestEnemy = min(dstsToPlayer)
                self.settings.dstToClosestEnemy = closestEnemy

            # run the level
            self.maze.run(deltaTime)
            # print(self.clock.get_fps())

            if not self.settings.shadersOn:
                pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)

    def map(self):
        """
        Map display
        """
        currentTime = time.time()

        mapSurf = pygame.transform.scale(pygame.image.load('graphics/special/objects/bigMap.png').convert_alpha(),
                                              (self.screen.get_size()))
        self.maze.run(0, getInput=False)
        mapImg = self.maze.bake_map()
        mapSurf.blit(mapImg, mapImg.get_rect(center=(self.settings.WIDTH/2, self.settings.HEIGHT/2)))
        slideTransitionStart(self.screen, mapSurf, self.shader)

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
                        self.maze.run(0, getInput=False)
                        slideTransitionEnd(self.screen, mapSurf, self.shader)
                        self.game(doTransition=False)
                    if key[pygame.K_m]:
                        self.maze.run(0, getInput=False)
                        slideTransitionEnd(self.screen, mapSurf, self.shader)
                        self.game(doTransition=False)

            # run the level
            mazeScreen = self.maze.run(deltaTime, getInput=False)
            self.screen.blit(mazeScreen, mazeScreen.get_rect())
            self.screen.blit(mapSurf, (0, 0))

            self.shader.render(self.screen)
            if not self.settings.shadersOn:
                pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)

    def pause_menu(self):
        """
        Pause menu, runs when escape is pressed
        """

        self.buttons = [Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.9),
                               'CONTINUE', self.settings.FONT, 'darkgray', 'white'),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.3),
                               'SETTINGS', self.settings.FONT, 'darkgray', 'white'),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7),
                               'EXIT TO MAIN MENU', self.settings.FONT, 'darkgray', 'white')]

        self.draw_screen()

        fadeTransitionEnd(self.screen, self.shader if self.settings.shadersOn else None)

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
                                fadeTransitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                self.maze.transition = 200
                                self.game()
                            elif i == 1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.shadersOn else None)
                                self.settings_menu(self.pause_menu)
                            elif i == 2:
                                fadeTransitionStart(self.screen, self.shader if self.settings.shadersOn else None)
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
        self.screen.fill(pygame.Color(46, 60, 87))
        # self.screen.fill('white')

        # debug FPS count
        debug("FPS : " + str(round(self.clock.get_fps() * 10) / 10), x=20)

        for button in self.buttons:
            button.update(self.screen)


if __name__ == '__main__':
    mazeGen = MazeGame()
    mazeGen.settings_menu(mazeGen.main_menu)
