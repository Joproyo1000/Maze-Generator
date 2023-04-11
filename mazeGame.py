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
        if self.settings.SHADERON:
            self.screen = pygame.display.set_mode(self.settings.RESOLUTION, pygame.OPENGL | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode(self.settings.RESOLUTION)

        self.background = pygame.image.load('graphics/startscreen.png').convert()
        self.background = pygame.transform.scale(self.background, (self.screen.get_size()))

        # initialize maze
        self.maze = Maze(self.settings)

        # initialize the render menus
        self.buttons = []
        if self.settings.SHADERON:
            self.shader = Shader(self.screen.get_size(), self.settings)

        pygame.display.set_caption(self.settings.TEXTS[self.settings.LANGUAGE]['The Maze Of Shadows'])
        self.clock = pygame.time.Clock()

    def main_menu(self):
        """
        Main menu, runs at start
        """
        self.buttons = [Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.1), self.settings.TEXTS[self.settings.LANGUAGE]['START'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), self.settings.TEXTS[self.settings.LANGUAGE]['PARAMETERS'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.3), self.settings.TEXTS[self.settings.LANGUAGE]['QUIT GAME'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)]

        self.drawScreen()

        titleText = pygame.font.Font('font/Pixeltype.ttf', self.settings.HEIGHT // 8).render(self.settings.TEXTS[self.settings.LANGUAGE]['The Maze Of Shadows'].upper(), True, self.settings.TEXTCOLOR)
        titleTextRect = titleText.get_rect(center=(self.settings.WIDTH/2, self.settings.HEIGHT/3.5))
        self.screen.blit(titleText, titleTextRect)

        fadeTransitionEnd(self.screen, self.shader if self.settings.SHADERON else None)

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
                                if self.chooseType():
                                    fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                    self.maze.reset()
                                    self.game()
                                else:
                                    continue
                            if i == 1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.settings_menu(self.main_menu)
                            if i == 2:
                                pygame.quit()
                                exit()

            self.drawScreen()
            self.screen.blit(titleText, titleTextRect)

            if not self.settings.SHADERON:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def settings_menu(self, start: classmethod, dotransition: bool=True):
        """
        Settings menu to change game settings
        """

        sliderSize = self.settings.HEIGHT//230

        self.buttons = [Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 4), self.settings.TEXTS[self.settings.LANGUAGE]['DIFFICULTY'],
                               (0, 2), self.settings.FONT, self.settings.TEXTCOLOR, self.settings.SLIDEREXTCOLOR, self.settings.SLIDERINTCOLOR, self.settings.HOVERINGCOLOR, self.settings.TEXTCOLOR,
                               sliderSize, 0, custom={0: self.settings.TEXTS[self.settings.LANGUAGE]['EASY'], 1: self.settings.TEXTS[self.settings.LANGUAGE]['MEDIUM'], 2: self.settings.TEXTS[self.settings.LANGUAGE]['HARD']}),

                        CheckButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 3.0), self.settings.TEXTS[self.settings.LANGUAGE]['HEART BEAT EFFECT'],
                                    self.settings.SHOWHEARTBEATEFFECT, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),

                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 2.2), self.settings.TEXTS[self.settings.LANGUAGE]['GAMMA'],
                               (5, 20), self.settings.FONT, self.settings.TEXTCOLOR, self.settings.SLIDEREXTCOLOR, self.settings.SLIDERINTCOLOR, self.settings.HOVERINGCOLOR, self.settings.TEXTCOLOR,
                               sliderSize, self.settings.GAMMA),

                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), self.settings.TEXTS[self.settings.LANGUAGE]['VOLUME'],
                               (0, 100), self.settings.FONT, self.settings.TEXTCOLOR, self.settings.SLIDEREXTCOLOR, self.settings.SLIDERINTCOLOR, self.settings.HOVERINGCOLOR, self.settings.TEXTCOLOR,
                               sliderSize, startVal=self.settings.VOLUME),

                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 1.4), self.settings.TEXTS[self.settings.LANGUAGE]['FPS'],
                               (30, 120), self.settings.FONT, self.settings.TEXTCOLOR, self.settings.SLIDEREXTCOLOR, self.settings.SLIDERINTCOLOR, self.settings.HOVERINGCOLOR, self.settings.TEXTCOLOR,
                               sliderSize, 60),

                        Button(None, (self.settings.WIDTH // 1.3, self.settings.HEIGHT // 1.2), self.settings.TEXTS[self.settings.LANGUAGE]['CONTROLS'] + ' ->',
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),

                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.2), self.settings.TEXTS[self.settings.LANGUAGE]['QUIT'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)]

        self.drawScreen()

        if dotransition:
            fadeTransitionEnd(self.screen, self.shader if self.settings.SHADERON else None)
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
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.settings.DIFFICULTY = int(self.buttons[0].value)
                                self.maze.FPS = self.buttons[4].value
                                start()
                            if i == len(self.buttons)-2:
                                self.controls_menu(start)

            self.settings.SHOWHEARTBEATEFFECT = self.buttons[1].value
            self.settings.GAMMA = self.buttons[2].value
            self.settings.VOLUME = self.buttons[3].value
            self.settings.MUSIC.set_volume(self.settings.VOLUME / 100)

            self.drawScreen()

            if not self.settings.SHADERON:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def controls_menu(self, start: classmethod):
        """
        Settings menu to change game controls
        """

        self.buttons = [InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 4.5), self.settings.TEXTS[self.settings.LANGUAGE]['UP'] + ': ',
                                    self.settings.K_UP, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 3), self.settings.TEXTS[self.settings.LANGUAGE]['DOWN'] + ': ',
                                    self.settings.K_DOWN, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.2), self.settings.TEXTS[self.settings.LANGUAGE]['LEFT'] + ': ',
                                    self.settings.K_LEFT, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), self.settings.TEXTS[self.settings.LANGUAGE]['RIGHT'] + ': ',
                                    self.settings.K_RIGHT, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.4), self.settings.TEXTS[self.settings.LANGUAGE]['MAP'] + ': ',
                                    self.settings.K_MAP, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 4, self.settings.HEIGHT // 1.2), '<- ' + self.settings.TEXTS[self.settings.LANGUAGE]['PARAMETERS'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.2), self.settings.TEXTS[self.settings.LANGUAGE]['QUIT'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)]

        self.drawScreen()

        while True:
            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        # if an input button is pressed, show a 'waiting for input' screen
                        if isinstance(button, InputButton):
                            if button.isHovered():
                                self.screen.fill(self.settings.MENUBACKGROUNDCOLOR)
                                waitText = self.settings.FONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['Waiting for input...'], True, self.settings.HOVERINGCOLOR)
                                self.screen.blit(waitText, waitText.get_rect(center=(self.settings.WIDTH/2, self.settings.HEIGHT/2)))
                                button.exitInputButton.update(self.screen)
                                if self.settings.SHADERON:
                                    self.shader.render(self.screen)
                                pygame.display.update()
                        # check every button for input
                        if button.checkForInput():
                            if i == len(self.buttons) - 1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                start()
                            if i == len(self.buttons) - 2:
                                self.settings_menu(start, dotransition=False)


            self.updateKeys()
            self.drawScreen()

            if not self.settings.SHADERON:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def game(self, doTransition: bool=True):
        """
        Main game loop
        """

        if doTransition:
            self.maze.run(0)
            fadeTransitionEnd(self.screen, self.shader if self.settings.SHADERON else None)

        currentTime = time.time()

        while True:
            # calculate deltaTime to make the speed go at the same rate regardless of FPS
            deltaTime = time.time() - currentTime
            currentTime = time.time()

            # set background color
            self.screen.fill('black')

            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # inventory
                if event.type == pygame.MOUSEWHEEL:
                    self.maze.player.currentItemIndex = (self.maze.player.currentItemIndex + event.y) % len(self.maze.player.inventory)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.maze.playerUse()
                    if self.maze.status == 'finished':
                        if self.maze.retryButton.checkForInput():
                            self.maze.reset()
                            self.maze.status = 'running'
                        if self.maze.restartButtion.checkForInput():
                            self.maze.reset()
                            self.maze.status = 'running'
                        if self.maze.exitButton.checkForInput():
                            self.main_menu()
                            self.maze.status = 'running'

                # menus
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[self.settings.K_MAP]:
                        self.map()
                    if key[pygame.K_ESCAPE]:
                        self.pause_menu()

                # update all enemies
                dstsToPlayer = []
                # get player pos
                playerPos = self.maze.check_tile(self.maze.player.rect.centerx // self.settings.TILESIZE,
                                                 self.maze.player.rect.centery // self.settings.TILESIZE)
                for i, enemyEvent in enumerate(self.maze.enemyEvents):
                    if event.type == enemyEvent:
                        d = self.maze.enemyBehavior(i, playerPos)
                        if d is not None:
                            dstsToPlayer.append(d)
                # keep track of the closest enemy to player
                if len(dstsToPlayer) > 0:
                    closestEnemy = min(dstsToPlayer)
                    self.settings.dstToClosestEnemy = closestEnemy

            # run the level
            self.maze.run(deltaTime)

            if not self.settings.SHADERON:
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
        slideTransitionStart(self.screen, mapSurf, self.shader if self.settings.SHADERON else None)

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
                        slideTransitionEnd(self.screen, mapSurf, self.shader if self.settings.SHADERON else None)
                        self.game(doTransition=False)
                    if key[self.settings.K_MAP]:
                        self.maze.run(0, getInput=False)
                        slideTransitionEnd(self.screen, mapSurf, self.shader if self.settings.SHADERON else None)
                        self.game(doTransition=False)

            # run the level
            mazeScreen = self.maze.run(deltaTime, getInput=False)
            self.screen.blit(mazeScreen, mazeScreen.get_rect())
            self.screen.blit(mapSurf, (0, 0))

            if self.settings.SHADERON:
                self.shader.render(self.screen)
            else:
                pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)

    def pause_menu(self):
        """
        Pause menu, runs when escape is pressed
        """

        self.buttons = [Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.3), self.settings.TEXTS[self.settings.LANGUAGE]['CONTINUE'],
                                      self.settings.FONT, self.settings.TEXTCOLOR, self.settings.TEXTCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.8), self.settings.TEXTS[self.settings.LANGUAGE]['PARAMETERS'],
                                      self.settings.FONT, self.settings.TEXTCOLOR, self.settings.TEXTCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.3), self.settings.TEXTS[self.settings.LANGUAGE]['MAIN MENU'],
                                      self.settings.FONT, self.settings.TEXTCOLOR, self.settings.TEXTCOLOR)]

        self.drawScreen()

        fadeTransitionEnd(self.screen, self.shader if self.settings.SHADERON else None)

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
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.maze.transition = 200
                                self.game()
                            elif i == 1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.settings_menu(self.pause_menu)
                            elif i == 2:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.main_menu()

            self.drawScreen()

            if not self.settings.SHADERON:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def updateKeys(self):
        """
        Updates key in settings
        """
        self.settings.K_UP = self.buttons[0].key
        self.settings.K_DOWN = self.buttons[1].key
        self.settings.K_LEFT = self.buttons[2].key
        self.settings.K_RIGHT = self.buttons[3].key
        self.settings.K_MAP = self.buttons[4].key

    def chooseType(self):
        boyButton = Button(None, (self.settings.WIDTH // 1.6, self.settings.HEIGHT // 2), self.settings.TEXTS[self.settings.LANGUAGE]['BOY'],
                                  self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)
        girlButton = Button(None, (self.settings.WIDTH // 2.4, self.settings.HEIGHT // 2), self.settings.TEXTS[self.settings.LANGUAGE]['GIRL'] + '        /',
                                   self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)
        cancelButton = Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.3), self.settings.TEXTS[self.settings.LANGUAGE]['CANCEL'],
                                     self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)

        self.screen.blit(self.background, self.background.get_rect())

        boyButton.update(self.screen)
        girlButton.update(self.screen)
        cancelButton.update(self.screen)

        type = None
        while type is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boyButton.checkForInput():
                        type = 'boy'
                    if girlButton.checkForInput():
                        type = 'girl'
                    if cancelButton.checkForInput():
                        return False

            boyButton.update(self.screen)
            girlButton.update(self.screen)
            cancelButton.update(self.screen)

            if self.settings.SHADERON:
                self.shader.render(self.screen)
            else:
                pygame.display.update()

        self.settings.TYPE = type

        return True

    def drawScreen(self):
        """
        Draws background, buttons and additional debug info for menus
        """
        self.screen.blit(self.background, self.background.get_rect())

        # debug FPS count
        debug("FPS : " + str(round(self.clock.get_fps() * 10) / 10), x=20)

        for button in self.buttons:
            button.update(self.screen)


if __name__ == '__main__':
    mazeGen = MazeGame()
    mazeGen.main_menu()
