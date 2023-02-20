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


class Slider:
    def __init__(self, pos, text_input, range, font, base_color, interior_color, hovering_color, ball_color):
        self.base_color, self.interior_color, self.hovering_color, self.ball_color = base_color, interior_color, hovering_color, ball_color

        self.slider = pygame.Surface((600, 100))
        self.slider.fill(self.base_color)
        self.rect = self.slider.get_rect(center=(pos[0], pos[1]))

        self.slider_small_rect = self.rect.inflate(-80, -80)
        self.slider_small = pygame.Surface((self.slider_small_rect.width, self.slider_small_rect.height))
        self.slider_small.fill(self.interior_color)

        self.slider_ball = pygame.Rect(self.slider_small_rect.left, self.slider_small_rect.top - 12.5, 50, 50)

        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.range = range

        self.font = font

        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos - 80))

        self.value = 0

    def update(self, screen):
        self.checkForInput()
        if self.slider is not None:
            screen.blit(self.slider, self.rect)
            screen.blit(self.slider_small, self.slider_small_rect)
        pygame.draw.circle(screen, self.ball_color, self.slider_ball.center, self.slider_ball.width / 1.5)
        self.text = self.font.render(self.text_input + ":" + str(round(self.value)), True, self.base_color)
        screen.blit(self.text, self.text_rect)

        self.value = self.valueFromBallPos()

    def checkForInput(self):
        mPos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mPos) and pygame.mouse.get_pressed()[0]:
            if self.slider_small_rect.left - 0.1 < mPos[0] < self.slider_small_rect.right + 0.1:
                self.slider_ball.centerx = mPos[0]

    def changeColor(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def getValue(self):
        return self.value

    def valueFromBallPos(self):
        value = ((self.slider_small_rect.right - self.slider_ball.centerx) / (self.slider_small_rect.left - self.slider_small_rect.right) + 1) * 100
        value = value * ((self.range[1] - self.range[0]) / 100) + self.range[0]

        return value

    def ballPosFromValue(self):
        value = (self.value - self.range[0]) / ((self.range[1] - self.range[0]) / 100)
        pos = (self.slider_small_rect.right - self.slider_small_rect.left) * value / 100 + self.slider_small_rect.left
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
        self.TURNFACTOR = 6

        # colors
        self.WALLCOLOR = 'darkgreen'
        self.PATHCOLOR = 'green'
        self.CURRENTCOLOR = 'red'

        # set FPS
        self.GAMEFPS = 60

        """ ================================================== """
        """ ONLY FOR DEBUGGING, MAKES THE MAZE GENERATE SLOWER """
        self.RUNSLOW = False
        self.RUNSLOWFPS = 10
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

        self.tilesize_slider = Slider((self.WIDTH * 3 / 4, 300), 'Tile Size', (20, min(self.MAZERESOLUTION)//2), self.font, 'white', 'gray', 'gray', 'black')
        self.tilesize_slider.value = self.TILESIZE
        self.tilesize_slider.slider_ball.centerx = self.tilesize_slider.ballPosFromValue()

        self.mazewidth_slider = Slider((self.WIDTH * 3 / 4, 500), 'Maze Width', (100, 2000), self.font, 'white', 'gray', 'gray', 'black')
        self.mazewidth_slider.value = self.MAZEWIDTH
        self.mazewidth_slider.slider_ball.centerx = self.mazewidth_slider.ballPosFromValue()

        self.mazeheight_slider = Slider((self.WIDTH * 3 / 4, 700), 'Maze Height', (100, 2000), self.font, 'white', 'gray', 'gray', 'black')
        self.mazeheight_slider.value = self.MAZEHEIGHT
        self.mazeheight_slider.slider_ball.centerx = self.mazeheight_slider.ballPosFromValue()


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

            self.TILESIZE = int(self.tilesize_slider.getValue())
            self.MAZEWIDTH = int(self.mazewidth_slider.getValue())
            self.MAZEHEIGHT = int(self.mazeheight_slider.getValue())

    def run(self):
        self.blit()
