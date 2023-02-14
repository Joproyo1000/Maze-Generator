import pygame
from random import choice
from settings import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, cols, rows, offsetToCenterX, offsetToCenterY, check_cell, groups):
        super().__init__(groups)

        # get the display surface
        self.screen = pygame.display.get_surface()

        self.image = pygame.Surface((TILESIZE * 3, TILESIZE * 3))
        self.rect = pygame.rect.Rect(x, y, TILESIZE, TILESIZE)

        self.x, self.y = x, y
        self.walls = {'top': True, 'left': True, 'bot': True, 'right': True}
        self.visited = False

        self.cols, self.rows = cols, rows
        self.offsetToCenterX, self.offsetToCenterY = offsetToCenterX, offsetToCenterY

        self.check_cell = check_cell

    def draw_current_cell(self):
        """
        draws the current cell as different color
        """
        x, y = self.x * TILESIZE + self.offsetToCenterX, self.y * TILESIZE + self.offsetToCenterY
        pygame.draw.rect(self.screen, 'saddlebrown',
                         (x + LINEWIDTH, y + LINEWIDTH, TILESIZE - LINEWIDTH, TILESIZE - LINEWIDTH))

    def debug_draw(self):
        """
        draws cell with only walls on the screen
        """
        x, y = self.x * TILESIZE + self.offsetToCenterX, self.y * TILESIZE + self.offsetToCenterY

        if self.visited:
            pygame.draw.rect(self.screen, pygame.Color(50, 50, 50), (x, y, TILESIZE, TILESIZE))

        if self.walls['top']:
            pygame.draw.line(self.screen, pygame.Color('darkorange'), (x, y), (x + TILESIZE, y), LINEWIDTH)
        if self.walls['left']:
            pygame.draw.line(self.screen, pygame.Color('darkorange'), (x, y), (x, y + TILESIZE), LINEWIDTH)
        if self.walls['bot']:
            pygame.draw.line(self.screen, pygame.Color('darkorange'), (x, y + TILESIZE), (x + TILESIZE, y + TILESIZE),
                             LINEWIDTH)
        if self.walls['right']:
            pygame.draw.line(self.screen, pygame.Color('darkorange'), (x + TILESIZE - 1, y),
                             (x + TILESIZE - 1, y + TILESIZE), LINEWIDTH)


    def draw(self):
        x, y = ((2 * self.x + 1) * TILESIZE) + self.offsetToCenterX, ((2 * self.y + 1) * TILESIZE) + self.offsetToCenterY

        if self.visited:
            pygame.draw.rect(self.screen, PATHCOLOR, (x, y, TILESIZE, TILESIZE))

        if self.walls['top']:
            pygame.draw.rect(self.screen, WALLCOLOR, (x, y - TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        if self.walls['left']:
            pygame.draw.rect(self.screen, WALLCOLOR, (x - TILESIZE, y, TILESIZE, TILESIZE), TILESIZE)
        if self.walls['bot']:
            pygame.draw.rect(self.screen, WALLCOLOR, (x, y + TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        if self.walls['right']:
            pygame.draw.rect(self.screen, WALLCOLOR, (x + TILESIZE, y, TILESIZE, TILESIZE), TILESIZE)

        if not self.walls['top']:
            pygame.draw.rect(self.screen, MIDPATHCOLOR, (x, y - TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        if not self.walls['left']:
            pygame.draw.rect(self.screen, MIDPATHCOLOR, (x - TILESIZE, y, TILESIZE, TILESIZE), TILESIZE)
        if not self.walls['bot']:
            pygame.draw.rect(self.screen, MIDPATHCOLOR, (x, y + TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        if not self.walls['right']:
            pygame.draw.rect(self.screen, MIDPATHCOLOR, (x + TILESIZE, y, TILESIZE, TILESIZE), TILESIZE)

        pygame.draw.rect(self.screen, WALLCOLOR, (x - TILESIZE, y - TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        pygame.draw.rect(self.screen, WALLCOLOR, (x + TILESIZE, y - TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        pygame.draw.rect(self.screen, WALLCOLOR, (x - TILESIZE, y + TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        pygame.draw.rect(self.screen, WALLCOLOR, (x + TILESIZE, y + TILESIZE, TILESIZE, TILESIZE), TILESIZE)


    def update_images(self):
        if self.visited:
            pygame.draw.rect(self.image, PATHCOLOR, (TILESIZE, TILESIZE, TILESIZE, TILESIZE))

        if self.walls['top']:
            pygame.draw.rect(self.image, WALLCOLOR, (TILESIZE, 0, TILESIZE, TILESIZE), TILESIZE)
        if self.walls['left']:
            pygame.draw.rect(self.image, WALLCOLOR, (0, TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        if self.walls['bot']:
            pygame.draw.rect(self.image, WALLCOLOR, (TILESIZE, 2 * TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        if self.walls['right']:
            pygame.draw.rect(self.image, WALLCOLOR, (2 * TILESIZE, TILESIZE, TILESIZE, TILESIZE), TILESIZE)

        if not self.walls['top']:
            pygame.draw.rect(self.image, MIDPATHCOLOR, (TILESIZE, 0, TILESIZE, TILESIZE), TILESIZE)
        if not self.walls['left']:
            pygame.draw.rect(self.image, MIDPATHCOLOR, (0, TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        if not self.walls['bot']:
            pygame.draw.rect(self.image, MIDPATHCOLOR, (0, 2 * TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        if not self.walls['right']:
            pygame.draw.rect(self.image, MIDPATHCOLOR, (2 * TILESIZE, 0, TILESIZE, TILESIZE), TILESIZE)

        pygame.draw.rect(self.image, WALLCOLOR, (0, 0, TILESIZE, TILESIZE), TILESIZE)
        pygame.draw.rect(self.image, WALLCOLOR, (2 * TILESIZE, 0, TILESIZE, TILESIZE), TILESIZE)
        pygame.draw.rect(self.image, WALLCOLOR, (0, 2 * TILESIZE, TILESIZE, TILESIZE), TILESIZE)
        pygame.draw.rect(self.image, WALLCOLOR, (2 * TILESIZE, 2 * TILESIZE, TILESIZE, TILESIZE), TILESIZE)

    def check_neighbors(self, grid_cells):
        """
        Checks for neighbors in the cells surrounding the current cell
        :return: returns any possible neighbors to the current cell
        """
        neighbors = []

        top = self.check_cell(self.x, self.y - 1)
        left = self.check_cell(self.x - 1, self.y)
        bot = self.check_cell(self.x, self.y + 1)
        right = self.check_cell(self.x + 1, self.y)

        if top and not top.visited:
            neighbors.append(top)
        if left and not left.visited:
            neighbors.append(left)
        if bot and not bot.visited:
            neighbors.append(bot)
        if right and not right.visited:
            neighbors.append(right)

        return choice(neighbors) if neighbors else False
