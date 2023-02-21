import pygame


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

        self.changeColor()

    def checkForInput(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class CheckButton:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image

        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.font = font

        self.base_color, self.hovering_color = base_color, hovering_color

        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        self.box = pygame.Rect(0, 0, self.text_rect.height, self.text_rect.height)
        self.box.center = (self.x_pos + self.text_rect.width / 1.8, self.y_pos)
        self.cross_rect = self.box.inflate(-6, -6)

        self.value = False

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)
        pygame.draw.rect(screen, self.base_color, self.box, 4)

        if self.value:
            pygame.draw.line(screen, self.base_color, self.cross_rect.topleft, self.cross_rect.bottomright, 4)
            pygame.draw.line(screen, self.base_color, self.cross_rect.bottomleft, self.cross_rect.topright, 4)

        self.changeColor()

    def checkForInput(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.value = True
            return True
        self.value = False
        return False

    def changeColor(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Slider:
    def __init__(self, pos, text_input, range, font, base_color, interior_color, hovering_color, ball_color, size):
        self.base_color, self.interior_color, self.hovering_color, self.ball_color = base_color, interior_color, hovering_color, ball_color

        # main rectangle of the slider (biggest one)
        self.slider = pygame.Surface((100 * size, 16.666 * size))
        self.slider.fill(self.base_color)
        self.rect = self.slider.get_rect(center=(pos[0], pos[1]))

        # second rectangle of the slider (smaller one in which the ball is)
        self.slider_small_rect = self.rect.inflate(-13.333 * size, -13.333 * size)
        self.slider_small = pygame.Surface((self.slider_small_rect.width, self.slider_small_rect.height))
        self.slider_small.fill(self.interior_color)

        # slider ball that you can drag around
        self.slider_ball = pygame.Rect(self.slider_small_rect.left, self.slider_small_rect.top - 2.08333 * size, 8.333 * size, 8.333 * size)

        self.x_pos = pos[0]
        self.y_pos = pos[1]

        # range of value
        self.range = range

        self.font = font

        # text to be displayed above the slider
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos - 13.333 * size))

        # value of the slider
        self.value = 0

    def checkForInput(self):
        """
        Updates the position of the ball if the mouse drags it
        """
        mPos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mPos) and pygame.mouse.get_pressed()[0]:
            if self.slider_small_rect.left - 0.1 < mPos[0] < self.slider_small_rect.right + 0.1:
                self.slider_ball.centerx = mPos[0]

    def update(self, screen):
        # update ball
        self.checkForInput()

        # show slider
        screen.blit(self.slider, self.rect)  # show slider
        screen.blit(self.slider_small, self.slider_small_rect)  # small slider
        pygame.draw.circle(screen, self.ball_color, self.slider_ball.center, self.slider_ball.width / 1.5)  # ball
        self.text = self.font.render(self.text_input + ": " + str(round(self.value)), True, self.base_color)  # render text
        screen.blit(self.text, self.text_rect)  # show text

        self.value = self.valueFromBallPos()  # update value

    def changeColor(self, position):
        """
        Makes the color of the text change if the mouse is over it
        :param position: position of the thing you want to test is over the text
        """
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def getValue(self):
        return self.value

    def valueFromBallPos(self):
        # value from pos = ((distance between right of the small slider and ball / - width of the slider) + 1) * 100
        #                   * (range of values / 100) + minimum value
        value = ((self.slider_small_rect.right - self.slider_ball.centerx) / (self.slider_small_rect.left - self.slider_small_rect.right) + 1) * 100
        value = value * ((self.range[1] - self.range[0]) / 100) + self.range[0]

        return value

    def ballPosFromValue(self):
        # value converted to percentage = (value - minimum value) / (value range / 100)
        value = (self.value - self.range[0]) / ((self.range[1] - self.range[0]) / 100)
        # pos from value = width of the slider * value / 100 + left of the small slider
        pos = self.slider_small_rect.width * value / 100 + self.slider_small_rect.left

        return pos


class Menu:
    def __init__(self, RESOLUTION, MAZERESOLUTION):
        super().__init__()

        self.screen = pygame.display.get_surface()

        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)

        self.WIDTH, self.HEIGHT = RESOLUTION[0], RESOLUTION[1]
        self.MAZEWIDTH, self.MAZEHEIGHT = MAZERESOLUTION[0], MAZERESOLUTION[1]

        # set the resolution for the screen
        self.RESOLUTION = self.WIDTH, self.HEIGHT
        self.MAZERESOLUTION = self.MAZEWIDTH, self.MAZEHEIGHT

        # set the tilesize (larger ones means smaller maze)
        self.TILESIZE = 60

        # randomness of the maze
        self.TURNFACTOR = 15

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
