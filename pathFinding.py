import heapq
import pygame
from tile import Tile


def distance(a, b):
    dstX = abs(a.rect.x - b.rect.x)
    dstY = abs(a.rect.y - b.rect.y)

    y = min(dstX, dstY)
    x = max(dstX, dstY)

    return 14 * y + 10 * (x - y)


class PathFinder:
    def __init__(self, level):
        # get grid and fCost of each tile
        self.screen = pygame.display.get_surface()

        self.grid = [tile for tile in level.grid_cells if not tile.isWall]

        self.get_neighbors = level.get_neighbors
        self.open = []
        self.closed = []
        heapq.heapify(self.open)

    def findPath(self, start, end):
        self.open.clear()
        self.closed.clear()
        for tile in self.grid:
            tile.reset()

        heapq.heappush(self.open, (start.fCost(), start))

        while len(self.open) > 0:
            current = heapq.heappop(self.open)[1]
            self.closed.append(current)

            # if path as been found
            if current == end:
                return self.getPath(start, end)

            for neighbor in self.get_neighbors(current):
                neighbor.isVisited = True

                if neighbor.isWall or neighbor in self.closed:
                    continue

                movementCost = current.gCost + distance(current, neighbor)
                if movementCost < neighbor.gCost or neighbor not in [d[1] for d in self.open]:
                    neighbor.gCost = movementCost
                    neighbor.hCost = distance(neighbor, end)
                    neighbor.parent = current
                    if neighbor not in [d[0] for d in self.open]:
                        heapq.heappush(self.open, (neighbor.fCost(), neighbor))

    def getPath(self, start, end):
        path = []
        current = end
        while current != start:
            path.append(current)
            current = current.parent

        # since path is from end to start we need to reverse it
        path.reverse()
        return path
