import sys
import time
from random import randint
import pygame
from math import floor

from tile import Tile
from random import choice
from cameras import YSortCameraGroup
from player import Player
from enemy import Enemy
from spatial_hashmap import HashMap
from pathFinding import PathFinder
from support import distance


class Maze(pygame.sprite.Group):
    def __init__(self, settings):
        super().__init__()

        # get the settings
        self.settings = settings

        # get the screen
        self.screen = pygame.display.get_surface()

        # value to control fade in transition
        self.transition = 300

        # surface for the fade in transition
        self.blackGradient = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.blackGradient.fill('black')

        # calculate number of columns and rows
        self.cols = int(self.settings.MAZEWIDTHS[self.settings.currentLevel] // self.settings.TILESIZE / 2) * 2 + 1
        self.rows = int(self.settings.MAZEHEIGHTS[self.settings.currentLevel] // self.settings.TILESIZE / 2) * 2 + 1

        # create two groups, one for sprites that need to be drawn on th screen, the other for the ones with collisions
        self.visible_sprites = YSortCameraGroup(self.settings, self.get_neighbors, self.check_tile)
        self.obstacle_sprites = HashMap(self.settings.TILESIZE, self.cols)

        # initialize the grid of cells
        self.grid_cells = [Tile(self.settings, (col * self.settings.TILESIZE, row * self.settings.TILESIZE), True, [self.visible_sprites, self.obstacle_sprites]) for row in range(self.rows) for col in range(self.cols)]

        # initialize map
        self.map = None
        self.map_size = 5

        # first tile to start the maze from
        self.start_tile = self.grid_cells[self.cols + 1]
        self.current_tile = self.start_tile
        self.goal = self.grid_cells[self.cols * self.rows - self.cols - 2]

        # initialize the stack (used to generate the maze)
        self.stack = []

        # initialize the player and put it on the first tile
        self.player = Player(self.start_tile.rect.center, 'girl', self.settings, [self.visible_sprites], self.obstacle_sprites)

        # initialize enemies
        self.enemies = pygame.sprite.Group()

        #region variables
        # True if maze is done generating
        self.mazeGenerated = False

        # set FPS for the game
        self.FPS = self.settings.GAMEFPS

        # time
        self.currentTime = time.time()
        #endregion

        # generate maze
        while self.stack or self.grid_cells[self.cols + 1].isWall:
            self.init_maze()

        self.update_tile_colors()
        self.obstacle_sprites.generate_hashmap()
        self.map = self.bake_maze(self.map_size)

        self.mazeGenerated = True

        # initialize main things in maze
        self.init_enemies()
        print(list(e.rect.center for e in self.enemies.sprites()))
        self.visible_sprites.init_background()
        self.visible_sprites.init_light()

        # initialize pathfinder
        self.pathFinder = PathFinder(self)

    def init_maze(self):
        """
        generate maze using the Depth First Search (DFS) algorithm
        """
        # runs while maze not finished
        self.current_tile.isWall = False

        self.update_tile_colors()

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

    def init_enemies(self):
        numberOfWolfs = floor(self.settings.MAZEWIDTHS[self.settings.currentLevel] / 2000 * (self.settings.WOLFPROPORTION + self.settings.DIFFICULTY))
        numberOfSpiders = floor(self.settings.MAZEWIDTHS[self.settings.currentLevel] / 2000 * (self.settings.SPIDERPROPORTION + self.settings.DIFFICULTY))
        numberOfSlimes = floor(self.settings.MAZEWIDTHS[self.settings.currentLevel] / 2000 * (self.settings.SLIMEPROPORTION + self.settings.DIFFICULTY))

        self.enemyEvents = [0] * (numberOfWolfs + numberOfSpiders + numberOfSlimes)

        # initializes all enemies
        # enemy class initializes like this Enemy(pos, type, speed, FOV, AI, settings, groups, obstacle_sprites)
        for i in range(numberOfWolfs):
            self.enemyEvents[i] = pygame.USEREVENT + (i + 1)
            pygame.time.set_timer(self.enemyEvents[i], 1000 + i * 200)

            wolf = Enemy(self.get_random_tile_in_maze(3).rect.center,
                         'wolf',
                         1,
                         700,
                         True,
                         self.settings,
                         [self.visible_sprites],
                         self.obstacle_sprites)
            self.enemies.add(wolf)

        for i in range(numberOfSpiders):
            self.enemyEvents[i + numberOfWolfs] = pygame.USEREVENT + (i + 1)
            pygame.time.set_timer(self.enemyEvents[i + numberOfWolfs], 1000 + i * 200)

            spider = Enemy(self.get_random_tile_in_maze(2).rect.center,
                           'spider',
                           0.7,
                           400,
                           True,
                           self.settings,
                           [self.visible_sprites],
                           self.obstacle_sprites)
            self.enemies.add(spider)

        for i in range(numberOfSlimes):
            self.enemyEvents[i + numberOfWolfs + numberOfSpiders] = pygame.USEREVENT + (i + 1)
            pygame.time.set_timer(self.enemyEvents[i + numberOfWolfs + numberOfSpiders], 5000 + i*1000)

            slime = Enemy(self.get_random_tile_in_maze(2).rect.center,
                          'slime',
                          0.4,
                          200,
                          False,
                          self.settings,
                          [self.visible_sprites],
                          self.obstacle_sprites)
            self.enemies.add(slime)

    def get_tile_pos_in_grid(self, x: int, y: int) -> int:
        """
        :param x: x position in the grid
        :param y: y position in the grid
        :return: the 1D position of the cell in the grid list
        """
        return x + y * self.cols

    def check_tile(self, x: int, y: int) -> pygame.sprite.Sprite:
        """
        Converts tile from x, y position to a 1D position on the tile grid
        :param x: x position on the 2D grid
        :param y: y position on the 2D grid
        :return: corresponding tile on the 1D grid
        """
        # if tile is outside maze return false
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return False

        # else return the tile in the grid corresponding to the coordinates
        return self.grid_cells[self.get_tile_pos_in_grid(x, y)]

    def check_neighbors(self, x: int, y: int) -> pygame.sprite.Sprite:
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

    def get_neighbors(self, tile):
        neighbors = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue

                if not isinstance(tile, bool):
                    checkX = tile.rect.x // self.settings.TILESIZE + x
                    checkY = tile.rect.y // self.settings.TILESIZE + y

                    neighbor = self.check_tile(checkX, checkY)
                    if neighbor:
                        neighbors.append(neighbor)

        return neighbors

    def get_random_tile_in_maze(self, distanceFromPlayer):
        """
        :param distanceFromPlayer: 1 is close, 2 is middle, 3 is far
        :return: a random pos that is not a wall in the grid and that is at least further away than the given distance
        """
        if distanceFromPlayer < 1 or distanceFromPlayer > 3:
            raise ValueError(f'distanceFromPlayer cannot be {distanceFromPlayer}. It must be either 1, 2 or 3')

        xRange = self.cols // 2 - 1
        yRange = self.rows // 2 - 1
        if randint(0, 1):
            return self.check_tile(randint(int(xRange * distanceFromPlayer/3 - 1), xRange) * 2 + 1,
                                   randint(0, yRange) * 2 + 1)
        else:
            return self.check_tile(randint(0, xRange) * 2 + 1,
                                   randint(int(yRange * distanceFromPlayer / 3 - 1), yRange) * 2 + 1)

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
            upTile = self.grid_cells[current_pos - self.cols]
            upTile.isWall = False

        # moving down
        elif dy == -2:
            downTile = self.grid_cells[current_pos + self.cols]
            downTile.isWall = False

    def update_tile_colors(self):
        """
        updates the color of the tile based on it being a wall or not
        """
        for tile in self.grid_cells:
            tile.update_color()

    def bake_maze(self, size: int) -> (pygame.Surface, pygame.Rect):
        """
        :param size: size of the baked map
        :return: a baked version of the map onto a Surface
        """
        baked_map = pygame.Surface((self.settings.TILESIZE * self.cols, self.settings.TILESIZE * self.rows))
        for tile in self.grid_cells:
            tile_image = pygame.Surface((self.settings.TILESIZE, self.settings.TILESIZE))
            tile_image.fill(tile.color)
            baked_map.blit(tile_image, tile.rect)

        baked_map = pygame.transform.scale(baked_map, (self.settings.TILESIZE * self.cols / size, self.settings.TILESIZE * self.rows / size))
        return baked_map, baked_map.get_rect()

    def enemyBehavior(self, i):
        """
        :param i: index of the current enemy being updated
        Enemy behavior method, basically just pathfinding
        """
        if self.mazeGenerated:
            enemy = self.enemies.sprites()[i]

            # get the tile where the enemy and the player are
            enemyPos = self.check_tile(enemy.rect.centerx // self.settings.TILESIZE,
                                       enemy.rect.centery // self.settings.TILESIZE)

            playerPos = self.check_tile(self.player.rect.centerx // self.settings.TILESIZE,
                                        self.player.rect.centery // self.settings.TILESIZE)

            enemyDst = distance(enemyPos, playerPos)

            # the wolf is blind, so he won't go towards the player unless it moves
            if enemy.type == 'wolf' and self.player.direction.magnitude() == 0:
                randomPos = self.get_random_tile_in_maze(1)

                path = self.pathFinder.findPath(enemyPos, randomPos)
                enemy.followPath(path=path, replace=True)
            # activate enemy pathfinding
            elif enemy.AI:

                # if both exists (failsafe) pathfind to player
                if enemyPos and playerPos:

                    # optimization : update enemy more frequently if close to player
                    pygame.time.set_timer(self.enemyEvents[i], int((enemyDst + 1000)))
                    if len(enemy.path) != 0:
                        enemy.followPath()

                    # if close enough to player, follow him
                    if enemyDst < enemy.range:
                        path = self.pathFinder.findPath(enemyPos, playerPos)
                        enemy.followPath(path=path, replace=True)

                    # else chose random location and pathfind there
                    else:
                        randomPos = self.get_random_tile_in_maze(3)

                        path = self.pathFinder.findPath(enemyPos, randomPos)
                        enemy.followPath(path=path, replace=True)
            else:
                randomPos = self.get_random_tile_in_maze(1)
                # print(enemyPos)
                path = self.pathFinder.findPath(enemyPos, randomPos)
                enemy.followPath(path=path, replace=True)

            return enemyDst

    def check_victory(self):
        """
        Check if player reaches goal
        """
        if pygame.sprite.collide_rect(self.player, self.goal):
            return True
        return False

    def check_death(self):
        """
        Check if player hits enemy
        """
        # if self.player.hitbox.collidelistall(list(enemy.hitbox for enemy in self.enemies)):
        #     return True
        # return False
        return False

    def check_game_state(self):
        """
        Check if game is supposed to end
        """
        if self.check_victory():
            self.settings.currentLevel += 1
            # check if player as reached exit of last level
            if self.settings.currentLevel >= self.settings.numLevels:
                print('YOU WON !')
                pygame.quit()
                sys.exit()
            else:
                self.reset()

        if self.check_death():
            print('YOU DIED !')
            self.reset()

    def reset(self):
        """
        Resets maze with same settings
        """
        self.__init__(self.settings)

    def run(self, deltaTime):
        if self.mazeGenerated:

            # fade in transition
            if self.transition >= 0:
                self.transition -= 2
                self.blackGradient.set_alpha(self.transition)

            self.visible_sprites.custom_draw(self.player, self.blackGradient)

            self.visible_sprites.update(deltaTime)

            self.check_game_state()
