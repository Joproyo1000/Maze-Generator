from random import choice, randint
import pygame

from tile import Tile
from random import choice
from ySortCamera import YSortCameraGroup
from player import Player


class Maze(pygame.sprite.Group):
    def __init__(self, settings):
        super().__init__()

        # get the settings
        self.settings = settings

        # get the screen
        self.screen = pygame.display.get_surface()

        # create two groups, one for sprites that need to be drawn on th screen, the other for the ones with collisions
        self.visible_sprites = YSortCameraGroup(self.settings)
        self.obstacle_sprites = pygame.sprite.Group()

        # calculate number of columns and rows
        self.cols, self.rows = int(self.settings.MAZEWIDTH // self.settings.TILESIZE / 2) * 2, int(self.settings.MAZEHEIGHT // self.settings.TILESIZE / 2) * 2
        # initialize the grid of cells
        self.grid_cells = [Tile(self.settings, (col * self.settings.TILESIZE, row * self.settings.TILESIZE), True, [self.visible_sprites, self.obstacle_sprites]) for row in range(self.rows + 1) for col in range(self.cols + 1)]

        # first tile to start the maze from
        self.start_tile = self.grid_cells[self.cols + 2]
        self.current_tile = self.start_tile
        # initialize the stack (used to generate the maze)
        self.stack = []

        # initialize the player and put it on the first tile
        self.player = Player(self.start_tile.rect.center, 'girl', self.settings.TILESIZE, [self.visible_sprites], self.obstacle_sprites)

        # True if maze is done generating
        self.mazeGenerated = False

        # set FPS for the game
        self.FPS = self.settings.GAMEFPS

        # generate maze fast if RUNSLOW isn't checked
        if not self.settings.RUNSLOW:
            while self.stack or self.grid_cells[self.cols + 2].isWall:
                self.generate_maze()
            self.update_tile_colors()
            self.mazeGenerated = True

    def get_tile_pos_in_grid(self, x: int, y: int) -> int:
        """
        :param x: x position in the grid
        :param y: y position in the grid
        :return: the 1D position of the cell in the grid list
        """
        return x + y * (self.cols+1)

    def check_tile(self, x: int, y: int) -> object:
        """
        Converts tile from x, y position to a 1D position on the tile grid
        :param x: x position on the 2D grid
        :param y: y position on the 2D grid
        :return: corresponding tile on the 1D grid
        """
        # if tile is outside maze return false
        if x < 0 or x > self.cols or y < 0 or y > self.rows:
            return False

        # else return the tile in the grid corresponding to the coordinates
        return self.grid_cells[self.get_tile_pos_in_grid(x, y)]

    def check_neighbors(self, x: int, y: int) -> object:
        """
        Checks for neighbors in the tiles surrounding the current tile
        :return: returns any possible neighbors to the current tile
        """
        neighbors = []
        top = self.check_tile(x, y - 2)
        left = self.check_tile(x - 2, y)
        bot = self.check_tile(x, y + 2)
        right = self.check_tile(x + 2, y)

        if randint(1, self.settings.TURNFACTOR) == 1:
            if top:
                neighbors.append(top)
            if left:
                neighbors.append(left)
            if bot:
                neighbors.append(bot)
            if right:
                neighbors.append(right)
            if self.start_tile not in neighbors:
                return choice(neighbors) if neighbors else False

        else:
            if top and top.isWall:
                neighbors.append(top)
            if left and left.isWall:
                neighbors.append(left)
            if bot and bot.isWall:
                neighbors.append(bot)
            if right and right.isWall:
                neighbors.append(right)

        return choice(neighbors) if neighbors else False

    def remove_walls(self, next_tile: object):
        """
        Removes walls between current and next tile
        :param next_tile: next tile being checked
        """
        dx = (self.current_tile.rect.x - next_tile.rect.x) // self.settings.TILESIZE
        dy = (self.current_tile.rect.y - next_tile.rect.y) // self.settings.TILESIZE
        current_pos = self.get_tile_pos_in_grid(self.current_tile.rect.x // self.settings.TILESIZE, self.current_tile.rect.y // self.settings.TILESIZE)

        # moving left
        if dx == 2:
            leftTile = self.grid_cells[current_pos - 1]
            leftTile.isWall = False

        # moving right
        elif dx == -2:
            rightTile = self.grid_cells[current_pos + 1]
            rightTile.isWall = False

        # moving up
        if dy == 2:
            upTile = self.grid_cells[current_pos - (self.cols + 1)]
            upTile.isWall = False

        # moving down
        elif dy == -2:
            downTile = self.grid_cells[current_pos + (self.cols + 1)]
            downTile.isWall = False

    def update_tile_colors(self):
        """
        updates the color of the tile based on it being a wall or not
        """
        for tile in self.grid_cells:
            tile.update_color()

    def generate_maze(self):
        """
        generate maze using the Depth First Search (DFS) algorithm
        """
        # runs while maze not finished
        self.current_tile.isWall = False
        # self.obstacle_sprites.remove(self.current_tile)

        self.update_tile_colors()
        self.current_tile.draw_current()

        # sets next cell to a random neighbor of the current cell
        next_tile = self.check_neighbors(self.current_tile.rect.x // self.settings.TILESIZE, self.current_tile.rect.y // self.settings.TILESIZE)

        # if a neighboring cell is available, set it as current
        if next_tile:
            next_tile.isWall = False
            self.stack.append(self.current_tile)
            self.remove_walls(next_tile)
            self.current_tile = next_tile
        # else go back in the stack until a new cell is available again
        elif self.stack:
            self.current_tile = self.stack.pop()

    def run(self):
        if self.settings.RUNSLOW and not self.mazeGenerated:
            self.visible_sprites.debug_draw(1)

            # if maze is finished generate border and set mazeGenerated to True
            if not (self.stack or self.grid_cells[self.cols + 2].isWall):
                self.update_tile_colors()
                self.mazeGenerated = True

            if not self.mazeGenerated:
                self.FPS = self.settings.RUNSLOWFPS
                self.generate_maze()
            else:
                self.FPS = self.settings.GAMEFPS

        if self.mazeGenerated:
            self.visible_sprites.update()
            self.visible_sprites.custom_draw(self.player)
            #self.visible_sprites.debug_draw(10)
