import pygame.sprite
from math import floor


class HashMap(pygame.sprite.Group):
    """
    Optimized version of getting collisions sprites with a complexity of O(1)
    """
    def __init__(self, TILESIZE, cols):
        super().__init__()
        self.TILESIZE = TILESIZE
        self.cols = cols
        self.grid = {}

    def get_grid_pos(self, posX, posY):
        gridPosX = floor(posX / self.TILESIZE) * self.TILESIZE
        gridPosY = floor(posY / self.TILESIZE) * self.TILESIZE
        gridPos = gridPosX + gridPosY * self.cols
        return gridPos

    def get_neighbors(self, pos):
        neighborsIndex = [self.get_grid_pos(pos[0] - self.TILESIZE, pos[1] - self.TILESIZE),  # topleft
                          self.get_grid_pos(pos[0], pos[1] - self.TILESIZE),  # top
                          self.get_grid_pos(pos[0] + self.TILESIZE, pos[1] - self.TILESIZE),  # topright
                          self.get_grid_pos(pos[0] - self.TILESIZE, pos[1]),  # left
                          self.get_grid_pos(pos[0] + self.TILESIZE, pos[1]),  # right
                          self.get_grid_pos(pos[0] - self.TILESIZE, pos[1] + self.TILESIZE),  # bottomleft
                          self.get_grid_pos(pos[0], pos[1] + self.TILESIZE),  # bottom
                          self.get_grid_pos(pos[0] + self.TILESIZE, pos[1] + self.TILESIZE)]  # bottomright

        neighbors = []
        for key in neighborsIndex:
            neighbor = self.grid.get(key, False)
            if neighbor:
                neighbors.append(neighbor)

        return neighbors

    def set(self, key, value):
        self.grid[key] = value

    def generate_hashmap(self):
        for sprite in self.sprites():
            alignedSpriteCoords = floor(sprite.rect.x / self.TILESIZE) * self.TILESIZE + \
                                  floor(sprite.rect.y / self.TILESIZE) * self.TILESIZE * self.cols
            self.set(alignedSpriteCoords, sprite)
