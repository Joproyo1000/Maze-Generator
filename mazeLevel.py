import sys
from random import randint
import pygame

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
        self.transition = 200

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
        self.player = Player(self.start_tile.rect.center, 'girl', self.settings.TILESIZE, [self.visible_sprites], self.obstacle_sprites)

        # initialize enemies
        self.enemies = pygame.sprite.Group()

        #region variables
        # True if maze is done generating
        self.mazeGenerated = False

        # set FPS for the game
        self.FPS = self.settings.GAMEFPS
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
        self.visible_sprites.init_background()
        self.visible_sprites.init_light()

        # initialize pathfinder
        self.pathFinder = PathFinder(self)

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

    def get_random_pos_in_maze(self, distanceFromPlayer):
        """
        :param distanceFromPlayer: 0 is close, 1 is middle, 2 is far
        :return: a random pos that is not a wall in the grid and that is at least further away than the given distance
        """
        if distanceFromPlayer < 0 or distanceFromPlayer > 2:
            raise ValueError(f'distanceFromPlayer cannot be {distanceFromPlayer}. It must be either 0, 1 or 2')

        return self.check_tile(randint(int(distanceFromPlayer / 3 * self.cols),
                                       (int((distanceFromPlayer + 1) / 3 * self.cols))) // 2 + 1,
                               randint(int(distanceFromPlayer / 3 * self.cols),
                                       (int((distanceFromPlayer + 1) / 3 * self.cols))) // 2 + 1
                               ).rect.center

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
        numberOfEnemies = self.settings.currentLevel * 2 + 1
        self.enemyEvents = [0] * numberOfEnemies

        for i in range(numberOfEnemies):
            self.enemyEvents[i] = pygame.USEREVENT + (i + 1)
            pygame.time.set_timer(self.enemyEvents[i], 1000 + i*200)

            # enemy class initializes like this Enemy(pos, type, speed, FOV, settings, groups, obstacle_sprites)
            enemy = Enemy(self.get_random_pos_in_maze(2),
                          'wolf',
                          0.5,
                          700,
                          self.settings,
                          [self.visible_sprites],
                          self.obstacle_sprites)
            self.enemies.add(enemy)

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
            closestEnemy = 100000

            enemy = self.enemies.sprites()[i]

            # get the tile where the enemy and the player are
            enemyPos = self.check_tile(enemy.rect.centerx // self.settings.TILESIZE,
                                       enemy.rect.centery // self.settings.TILESIZE)
            playerPos = self.check_tile(self.player.rect.centerx // self.settings.TILESIZE,
                                        self.player.rect.centery // self.settings.TILESIZE)

            # if both exists (failsafe) pathfind to player
            if enemyPos and playerPos:

                # activate pathfinding for enemy
                enemyDst = distance(enemyPos, playerPos)

                if enemyDst < closestEnemy:
                    closestEnemy = enemyDst

                pygame.time.set_timer(self.enemyEvents[i], int((enemyDst + 1)))
                if len(enemy.path) != 0:
                    enemy.followPath()

                # if close enough to player, follow him
                if enemyDst < enemy.range:
                    path = self.pathFinder.findPath(enemyPos, playerPos)
                    enemy.followPath(path=path, replace=True)
                # else chose random location and pathfind there
                else:
                    randomPos = self.grid_cells[self.get_tile_pos_in_grid(randint(0, self.rows//2) * 2 - 1, randint(0, self.cols//2) * 2 - 1)]

                    path = self.pathFinder.findPath(enemyPos, randomPos)
                    enemy.followPath(path=path, replace=True)
            self.settings.dstToClosestEnemy = closestEnemy

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
        # if pygame.sprite.spritecollideany(self.player, self.enemies):
        if self.player.hitbox.collidelistall(list(enemy.hitbox for enemy in self.enemies)):
            return True
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

    def run(self):
        if self.mazeGenerated:

            # fade in transition
            if self.transition >= 0:
                self.transition -= 2
                self.blackGradient.set_alpha(self.transition)

            self.visible_sprites.update()
            self.visible_sprites.custom_draw(self.player, self.blackGradient)

            self.check_game_state()
