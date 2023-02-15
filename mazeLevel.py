from tile import Tile
from settings import *
from random import choice
from ySortCamera import YSortCameraGroup
from player import Player


class Maze(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.screen = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.cols, self.rows = MAZEWIDTH // TILESIZE, MAZEHEIGHT // TILESIZE
        self.grid_cells = [Tile(WALLCOLOR, (col * TILESIZE, row * TILESIZE), True, [self.visible_sprites, self.obstacle_sprites]) for row in range(self.rows + 1) for col in range(self.cols + 1)]

        self.current_tile = self.grid_cells[self.cols + 2]
        self.stack = []

        self.player = Player(self.grid_cells[self.cols + 2].rect.center, [self.visible_sprites], self.obstacle_sprites)

        # True if maze is done generating
        self.mazeGenerated = False

        self.FPS = GAMEFPS

        if not RUNSLOW:
            while self.stack or self.grid_cells[self.cols + 2].isWall:
                self.generate_maze()
            self.mazeGenerated = True

    def get_tile_pos_in_grid(self, x, y):
        return x + y * (self.cols+1)

    def check_cell(self, x: int, y: int) -> object:
        """
        Converts cell from x, y position to a 1D position on the cell grid
        :param x: x position on the 2D grid
        :param y: y position on the 2D grid
        :return: corresponding cell on the 1D grid
        """
        if x < 0 or x > self.cols or y < 0 or y > self.rows:
            return False

        return self.grid_cells[self.get_tile_pos_in_grid(x, y)]

    def check_neighbors(self, x, y):
        """
        Checks for neighbors in the cells surrounding the current cell
        :return: returns any possible neighbors to the current cell
        """
        neighbors = []
        top = self.check_cell(x, y - 2)
        left = self.check_cell(x - 2, y)
        bot = self.check_cell(x, y + 2)
        right = self.check_cell(x + 2, y)

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
        Removes walls between current and next cell
        :param next_tile: next cell being checked
        """
        dx = (self.current_tile.rect.x - next_tile.rect.x) // TILESIZE
        dy = (self.current_tile.rect.y - next_tile.rect.y) // TILESIZE
        current_pos = self.get_tile_pos_in_grid(self.current_tile.rect.x // TILESIZE, self.current_tile.rect.y // TILESIZE)

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
        for tile in self.grid_cells:
            tile.update_color()

    def generate_maze(self):
        # runs while maze not finished
        self.current_tile.isWall = False

        self.update_tile_colors()
        self.current_tile.draw_current()

        # sets next cell to a random neighbor of the current cell
        next_tile = self.check_neighbors(self.current_tile.rect.x // TILESIZE, self.current_tile.rect.y // TILESIZE)

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
        if RUNSLOW and not self.mazeGenerated:
            self.visible_sprites.debug_draw()

            # if maze is finished generate border and set mazeGenerated to True
            if not (self.stack or self.grid_cells[self.cols + 2].isWall):
                self.update_tile_colors()
                self.mazeGenerated = True

            if not self.mazeGenerated:
                self.FPS = RUNSLOWFPS
                self.generate_maze()
            else:
                self.FPS = GAMEFPS

        if self.mazeGenerated:
            self.visible_sprites.update()
            self.visible_sprites.custom_draw(self.player)
