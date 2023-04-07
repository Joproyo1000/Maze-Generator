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
from objects import Torch, Chest, Map
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
        # initialize enemies group
        self.enemies = pygame.sprite.Group()

        # initialize the grid of cells
        self.grid_cells = [Tile(self.settings, (col * self.settings.TILESIZE, row * self.settings.TILESIZE), True, [self.visible_sprites]) for row in range(self.rows) for col in range(self.cols)]

        # first tile to start the maze from
        self.start_tile = self.grid_cells[self.cols + 1]
        self.current_tile = self.start_tile
        self.goal = self.grid_cells[self.cols * self.rows - self.cols - 2]

        # region variables
        # True if maze is done generating
        self.mazeGenerated = False

        # set FPS for the game
        self.FPS = self.settings.GAMEFPS

        # time
        self.currentTime = time.time()
        # endregion

        # initialize the stack (used to generate the maze)
        self.stack = []

        # generate maze
        self.chests = []
        self.init_maze()
        self.init_rooms()

        # initialize the player and put it on the first tile
        self.player = Player(self.start_tile.rect.center, 'girl', self.settings, [self.visible_sprites], self.obstacle_sprites)

        self.update_tile_colors()
        self.obstacle_sprites.generate_hashmap()

        self.mazeGenerated = True

        # initialize lighting, objects and enemies in maze
        self.init_enemies()
        self.visible_sprites.init_background()
        self.visible_sprites.init_light()

        # initialize pathfinder
        self.pathFinder = PathFinder(self)

    def init_maze(self):
        """
        generate maze using the Depth First Search (DFS) algorithm
        """
        # keep track of furthest tile
        dst = 0
        furthestDst = 0
        while self.stack or self.grid_cells[self.cols + 1].isWall:
            # runs while maze not finished
            self.current_tile.isWall = False

            self.update_tile_colors()

            # sets next cell to a random neighbor of the current cell
            next_tile = self.random_neighbor(self.current_tile.rect.x // self.settings.TILESIZE, self.current_tile.rect.y // self.settings.TILESIZE)

            # if a neighboring cell is available, set it as current
            if next_tile:
                dst += 1
                next_tile.isWall = False
                self.stack.append(self.current_tile)
                self.remove_walls(next_tile)
                self.current_tile = next_tile

            # else go back in the stack until a new cell is available again
            elif self.stack:
                dst -= 1
                self.current_tile = self.stack.pop()

            if dst > furthestDst:
                furthestDst = dst
                furthestTile = next_tile
        # set the end goal to the furthest tile from the start
        self.goal = furthestTile

        for tile in self.grid_cells:
            if tile.isWall:
                self.obstacle_sprites.add(tile)

    def init_rooms(self):
        """
        Initialize all rooms with a chest in the middle and a torch on top
        """
        # repeat for every room
        for _ in range(self.settings.currentLevel * 2 + 1):
            # get center of the room
            center = self.get_random_tile_in_maze(1)

            # initialize torch and chest objects
            Torch((center.rect.centerx, center.rect.top), 'right', self.settings, [self.visible_sprites])
            chest = Chest(center.rect.center, self.settings, [self.visible_sprites, self.obstacle_sprites])
            self.chests.append(chest)

            # remove all tiles in a 3*3 square to form a room
            for neighbor in self.get_neighbors(center):
                if neighbor.rect.left != 0 and neighbor.rect.top != 0 and neighbor.rect.right != self.cols * self.settings.TILESIZE and neighbor.rect.bottom != self.rows * self.settings.TILESIZE:
                    neighbor.isWall = False
                    self.obstacle_sprites.remove(neighbor)

    def init_enemies(self):
        """
        Initialize all enemies (wolves, spiders and slimes) and spawns them in maze according to the difficulty
        """
        numberOfWolfs = floor(self.settings.MAZEWIDTHS[self.settings.currentLevel] / 2000 * (self.settings.WOLFPROPORTION + self.settings.DIFFICULTY))
        numberOfSpiders = floor(self.settings.MAZEWIDTHS[self.settings.currentLevel] / 2000 * (self.settings.SPIDERPROPORTION + self.settings.DIFFICULTY))
        numberOfSlimes = floor(self.settings.MAZEWIDTHS[self.settings.currentLevel] / 2000 * (self.settings.SLIMEPROPORTION + self.settings.DIFFICULTY))

        self.enemyEvents = [0] * (numberOfWolfs + numberOfSpiders + numberOfSlimes)

        # initializes all enemies
        # enemy class initializes like this Enemy(position, type, speed, FOV, AI, settings, groups, obstacle sprites)
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

    def random_neighbor(self, x: int, y: int) -> pygame.sprite.Sprite:
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
        """
        :param tile: target tile
        :return: all existing neighbors of the target tile
        """
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
        :return: a random pos tile is not a wall in the grid and that is at least further away than the given distance
        """
        if distanceFromPlayer < 1 or distanceFromPlayer > 3:
            raise ValueError(f'distanceFromPlayer cannot be {distanceFromPlayer}. It must be either 1, 2 or 3')

        xRange = self.cols // 2 - 1
        yRange = self.rows // 2 - 1
        if randint(0, 1):
            return self.check_tile(randint(int(xRange * distanceFromPlayer / 4 - 1), xRange) * 2 + 1,
                                   randint(0, yRange) * 2 + 1)
        else:
            return self.check_tile(randint(0, xRange) * 2 + 1,
                                   randint(int(yRange * distanceFromPlayer / 4 - 1), yRange) * 2 + 1)

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

    def bake_map(self) -> pygame.Surface:
        """
        :return: a baked version of the map onto a Surface
        """
        # initialize baked map surface
        baked_map = pygame.Surface((self.settings.TILESIZE * self.cols, self.settings.TILESIZE * self.rows))

        image = pygame.Surface((self.settings.TILESIZE, self.settings.TILESIZE))
        # draw every tile and chest onto it
        for tile in self.grid_cells:
            image.fill(tile.color)
            baked_map.blit(image, tile.rect)
        for chest in self.chests:
            image.fill(chest.color)
            baked_map.blit(image, self.check_tile(chest.rect.centerx // self.settings.TILESIZE,
                                                  chest.rect.centery // self.settings.TILESIZE).rect)
        # draw player
        image.fill(self.player.color)
        baked_map.blit(image, self.check_tile(self.player.rect.centerx // self.settings.TILESIZE,
                                              self.player.rect.centery // self.settings.TILESIZE).rect)
        # draw end
        image.fill(self.settings.ENDCOLOR)
        baked_map.blit(image, self.goal.rect)

        ratio = baked_map.get_width() / baked_map.get_height()

        scaledWidth = self.settings.WIDTH
        scaledHeight = scaledWidth * ratio
        if scaledHeight > self.settings.HEIGHT:
            scaledHeight = self.settings.HEIGHT
            scaledWidth = scaledHeight * ratio

        baked_map = pygame.transform.scale(baked_map, (scaledWidth * 0.75, scaledHeight * 0.75))

        # mask the baked map to show only areas where player as found map
        mask = pygame.Surface(self.screen.get_size()).convert_alpha()
        mask.fill('black')
        for map in [object for object in self.player.inventory if isinstance(object, Map)]:
            pygame.draw.circle(mask, (0, 0, 0, 0), (map.pos[0] * baked_map.get_width(), map.pos[1] * baked_map.get_height()), 400 - 50 * self.settings.currentLevel * self.settings.DIFFICULTY)

        baked_map.blit(mask, mask.get_rect())
        baked_map.set_colorkey('black')

        return baked_map

    def enemyBehavior(self, i):
        """
        :param i: index of the current enemy being updated
        Enemy behavior method, handles different enemies behavior
        """
        if self.mazeGenerated:
            enemy = self.enemies.sprites()[i]

            if enemy.type == 'spider':
                if randint(0, 20) == 0:
                    enemy.spawnCobweb(self.visible_sprites)

            # region pathfinding
            # get the tile where the enemy and the player are
            enemyPos = self.check_tile(enemy.rect.centerx // self.settings.TILESIZE,
                                       enemy.rect.centery // self.settings.TILESIZE)

            playerPos = self.check_tile(self.player.rect.centerx // self.settings.TILESIZE,
                                        self.player.rect.centery // self.settings.TILESIZE)

            # if both exists (failsafe) pathfind to player
            if enemyPos and playerPos:
                enemyDst = distance(enemyPos, playerPos)

                # the wolf is blind, so he won't go towards the player unless it moves
                if enemy.type == 'wolf' and self.player.direction.magnitude() == 0:
                    randomPos = self.get_random_tile_in_maze(1)
                    path = self.pathFinder.findPath(enemyPos, randomPos)
                    enemy.followPath(path=path, replace=True)
                # activate enemy pathfinding to player
                elif enemy.AI:
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
                # activate enemy pathfinding to random location
                else:
                    randomPos = self.get_random_tile_in_maze(1)
                    path = self.pathFinder.findPath(enemyPos, randomPos)
                    enemy.followPath(path=path, replace=True)

                return enemyDst
            # endregion

        return None

    def rayCast(self, origin: Tile, direction: str, size: float) -> [Tile]:
        """
        :param origin: center of the ray
        :param direction: direction in which the ray should be cast
        :param size: size of the ray (in tiles)
        :return: a list of tiles that has been touched by the ray
        """
        directions = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        res = []

        target = origin
        origin = pygame.Vector2(origin.rect.x // self.settings.TILESIZE, origin.rect.y // self.settings.TILESIZE)

        ray = pygame.Vector2(directions[direction])
        while ray.magnitude() < size and not target.isWall:
            target = self.check_tile(int((origin + ray).x), int((origin + ray).y))
            if target:
                res.append(target)

            ray.scale_to_length(ray.magnitude() + 1)

        return res

    def check_interactables(self):
        for chest in self.chests:
            if self.player.hitbox.colliderect(chest.hitbox):
                chest.open(self.player)

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
        return False

    def check_game_state(self):
        """
        Update game state and interactables
        """
        # self.check_interactables()

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

    def run(self, deltaTime, getInput=True):
        """
        :param deltaTime: time interval between two frames
        :param getInput: activate or no player input
        Updates all sprites in maze and takes care of the game state
        """
        if self.mazeGenerated:

            # fade in transition
            if self.transition >= 0:
                self.transition -= 2
                self.blackGradient.set_alpha(self.transition)

            self.visible_sprites.custom_draw(self.player, self.blackGradient)

            self.player.getInput = getInput
            self.visible_sprites.update(deltaTime)

            self.check_game_state()
