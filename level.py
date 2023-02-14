import pygame
from settings import *
from cell import Cell
from player import Player


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # get the display surface
        self.screen = pygame.display.get_surface()

        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2

        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
        for sprite in self.sprites():
            if str(type(sprite)) == "<class 'player.Player'>":
                offset_pos = sprite.rect.topleft - self.offset
                self.screen.blit(sprite.image, offset_pos)
            else:
                offset_pos = (sprite.rect.x * TILESIZE) * 2 + 1, (sprite.rect.y * TILESIZE) * 2 + 1
                offset_pos -= self.offset
                self.screen.blit(sprite.image, offset_pos)

    def debug_draw(self):
        for sprite in self.sprites():
            if not (str(type(sprite)) == "<class 'player.Player'>"):
                sprite.debug_draw()
                #self.screen.blit(sprite.image, sprite.rect)


class Level:
    def __init__(self):
        # get the display surface
        self.screen = pygame.display.get_surface()

        self.FPS = GAMEFPS

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.cols, self.rows = MAZEWIDTH // TILESIZE, MAZEHEIGHT // TILESIZE

        # calculate offset to center the maze on the screen
        self.offsetToCenterX, self.offsetToCenterY = (WIDTH - MAZEWIDTH) // 2, (HEIGHT - MAZEHEIGHT) // 2

        # initializes the grid of cells
        self.grid_cells = [Cell(col, row, self.cols, self.rows, self.offsetToCenterX, self.offsetToCenterY, self.check_cell, [self.visible_sprites, self.obstacle_sprites]) for row in range(self.rows) for col in range(self.cols)]
        #self.grid_cells = [Cell(col, row, self.cols, self.rows, self.offsetToCenterX, self.offsetToCenterY, self.check_cell, [self.obstacle_sprites]) for row in range(self.rows) for col in range(self.cols)]

        # set first cell to the cell in the grid of index 0
        self.current_cell = self.grid_cells[0]

        # stack keeps track how which path as been taken, can get to a size of (rows * cols)
        self.stack = []

        # True if maze is done generating
        self.mazeGenerated = False

        # generate maze fast
        if not RUNSLOW:
            while self.stack or not self.grid_cells[0].visited:
                self.generate_maze()
            self.mazeGenerated = True

            for cell in self.grid_cells:
                cell.update_images()

    def generate_maze(self):
        """
        generates maze either slow or fast way
        """

        # runs while maze not finished
        self.current_cell.visited = True
        self.current_cell.draw_current_cell()

        # sets next cell to a random neighbor of the current cell
        next_cell = self.current_cell.check_neighbors(self.grid_cells)

        # if a neighboring cell is available, set it as current
        if next_cell:
            next_cell.visited = True
            self.stack.append(self.current_cell)
            self.remove_walls(next_cell)
            self.current_cell = next_cell
        # else go back in the stack until a new cell is available again
        elif self.stack:
            self.current_cell = self.stack.pop()

        self.player = Player((TILESIZE + TILESIZE / 2, TILESIZE + TILESIZE / 2), [self.visible_sprites], self.obstacle_sprites)

    def gradientRect(self, screen, left_colour, right_colour, target_rect):
        """ Draw a horizontal-gradient filled rectangle covering target_rect """
        colour_rect = pygame.Surface((2, 2))
        pygame.draw.line(colour_rect, left_colour, (0, 0), (1, 0))
        pygame.draw.line(colour_rect, right_colour, (0, 1), (1, 1))
        colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
        screen.blit(colour_rect, target_rect)

    def remove_walls(self, next: object):
        """
        Removes walls between current and next cell
        :param current: current cell whose walls are changed
        :param next: next cell being checked
        """
        dx = self.current_cell.rect.x - next.rect.x
        dy = self.current_cell.rect.y - next.rect.y

        if dx == 1:
            self.current_cell.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            self.current_cell.walls['right'] = False
            next.walls['left'] = False
        elif dy == 1:
            self.current_cell.walls['top'] = False
            next.walls['bot'] = False
        elif dy == -1:
            self.current_cell.walls['bot'] = False
            next.walls['top'] = False

    def check_cell(self, x: int, y: int) -> object:
        """
        Converts cell from x, y position to a 1D position on the cell grid
        :param x: x position on the 2D grid
        :param y: y position on the 2D grid
        :return: corresponding cell on the 1D grid
        """
        find_index = lambda x, y: x + y * self.cols

        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return False

        return self.grid_cells[find_index(x, y)]

    def run(self):
        # update and draw the game
        if RUNSLOW:
            # if maze is finished set mazeGenerated to True
            if not (self.stack or not self.grid_cells[0].visited):
                self.mazeGenerated = True

            if not self.mazeGenerated:
                self.FPS = RUNSLOWFPS
                self.generate_maze()
            else:
                for cell in self.grid_cells:
                    cell.update_images()
                self.FPS = GAMEFPS

        # self.visible_sprites.draw(self.screen)
        if RUNSLOW and not self.mazeGenerated:
            self.visible_sprites.debug_draw()
        else:
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update()
