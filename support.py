import math
from os import walk
import pygame
import tile


def import_folder(path, size):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale_by(image_surf, size)
            surface_list.append(image_surf)

    return surface_list


def distance(a: tile, b: tile):
    if isinstance(a, bool):
        raise TypeError(f'A should be of type Tile and not {a}')
    if isinstance(b, bool):
        raise TypeError(f'B should be of type Tile and not {b}')

    return math.sqrt(sum((a.pos[i] - b.pos[i]) ** 2 for i in range(2)))


def fadeTransitionStart(screen: pygame.Surface, shader=None):
    blackGradient = pygame.Surface((screen.get_width(), screen.get_height()))
    blackGradient.fill('black')
    for a in range(150):
        blackGradient.set_alpha(a)
        screen.blit(blackGradient, (0, 0))
        if shader is None:
            pygame.display.update()
        else:
            shader.render(screen)
        pygame.time.delay(5)


def fadeTransitionEnd(screen: pygame.Surface, shader=None):
    background = screen.copy()
    blackGradient = pygame.Surface((screen.get_width(), screen.get_height()))
    blackGradient.fill('black')
    for a in range(180, -1, -3):
        blackGradient.set_alpha(a)
        screen.blit(background, (0, 0))
        screen.blit(blackGradient, (0, 0))

        if shader is None:
            pygame.display.update()
        else:
            shader.render(screen)
        pygame.time.delay(5)


def slideTransitionStart(screen: pygame.Surface, surface: pygame.Surface):
    background = screen.copy()
    rect = screen.get_rect(topleft=screen.get_rect().bottomleft)

    screen.blit(surface, rect)
    j = screen.get_height() // 6
    while rect.y > 0:
        screen.blit(background, (0, 0))
        screen.blit(surface, rect)

        pygame.display.flip()

        rect.y -= j
        j -= j // 6

        pygame.time.delay(5)


def slideTransitionEnd(screen: pygame.Surface, surface: pygame.Surface):
    background = screen.copy()
    rect = screen.get_rect()

    screen.blit(surface, rect)
    j = screen.get_height() // 6
    while rect.y < screen.get_height():
        screen.blit(background, (0, 0))
        screen.blit(surface, rect)

        pygame.display.flip()

        rect.y += j
        j += j // 6

        pygame.time.delay(5)


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
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
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
        pygame.draw.rect(screen, self.base_color, self.box, 8)

        if self.value:
            pygame.draw.line(screen, self.base_color, (self.cross_rect.left + 4, self.cross_rect.top + 4),
                             (self.cross_rect.right - 4, self.cross_rect.bottom - 4), 8)
            pygame.draw.line(screen, self.base_color, (self.cross_rect.left + 4, self.cross_rect.bottom - 4),
                             (self.cross_rect.right - 4, self.cross_rect.top + 4), 8)

        self.changeColor()

    def checkForInput(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.value = not self.value
            return self.value

    def changeColor(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Slider:
    def __init__(self, pos, text_input, range, font, base_color, exterior_color, interior_color, hovering_color,
                 ball_color, size, startVal, custom=None):
        self.base_color, self.exterior_color, self.interior_color, self.hovering_color, self.ball_color = base_color, exterior_color, interior_color, hovering_color, ball_color

        # main rectangle of the slider (the biggest one)
        self.slider = pygame.Surface((100 * size, 16.666 * size))
        self.slider.fill(self.exterior_color)
        self.rect = self.slider.get_rect(center=(pos[0], pos[1]))

        # second rectangle of the slider (smaller one in which the ball is)
        self.slider_small_rect = self.rect.inflate(-13.333 * size, -13.333 * size)
        self.slider_small = pygame.Surface((self.slider_small_rect.width, self.slider_small_rect.height))
        self.slider_small.fill(self.interior_color)

        # slider ball that you can drag around
        self.slider_ball = pygame.Rect(self.slider_small_rect.left, self.slider_small_rect.top - 2.08333 * size,
                                       8.333 * size, 8.333 * size)

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
        self.value = startVal
        self.slider_ball.x = self.ballPosFromValue()

        # custom text/value dictionnary
        self.custom = custom

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
        pygame.draw.rect(screen, self.exterior_color, self.rect, border_radius=50)  # exterior rect
        screen.blit(self.slider_small, self.slider_small_rect)  # interior rect
        pygame.draw.circle(screen, self.ball_color, self.slider_ball.center, self.slider_ball.width / 1.5)  # ball
        if self.custom is None:
            self.text = self.font.render(self.text_input + ": " + str(round(self.value)), True, self.base_color)  # text
            self.text_rect.centerx = self.x_pos - (len(": " + str(round(self.value))) * 20) / 2
        else:
            self.text = self.font.render(self.text_input + ": " + self.custom[round(self.value)], True,
                                         self.base_color)  # text
            self.text_rect.centerx = self.x_pos - (len(": " + self.custom[round(self.value)]) * 20) / 2
        screen.blit(self.text, self.text_rect)  # show text

        self.value = self.valueFromBallPos()  # update value

    def changeColor(self, position):
        """
        Makes the color of the text change if the mouse is over it
        :param position: position of the thing you want to test is over the text
        """
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top,
                                                                                                    self.text_rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def valueFromBallPos(self):
        # value from pos = ((distance between right of the small slider and ball / - width of the slider) + 1) * 100
        #                   * (range of values / 100) + minimum value
        value = ((self.slider_small_rect.right - self.slider_ball.centerx) / (
                self.slider_small_rect.left - self.slider_small_rect.right) + 1) * 100
        value = value * ((self.range[1] - self.range[0]) / 100) + self.range[0]

        return value

    def ballPosFromValue(self):
        # value converted to percentage = (value - minimum value) / (value range / 100)
        value = (self.value - self.range[0]) / ((self.range[1] - self.range[0]) / 100)
        # pos from value = width of the slider * value / 100 + left of the small slider
        pos = self.slider_small_rect.width * value / 100 + self.slider_small_rect.left

        return pos
