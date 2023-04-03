import random

import pygame.sprite

import settings
from Pygame_Lights import *
from shaders import Shader


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, settings: settings.Settings, get_neighbors, check_tile):
        super().__init__()

        # copy settings to self to access them in the whole class
        self.settings = settings

        # get the display surface and initialize background surface
        self.screen = pygame.surface.Surface((self.settings.WIDTH, self.settings.HEIGHT))
        self.background = pygame.Surface((self.settings.MAZEWIDTHS[self.settings.currentLevel],
                                          self.settings.MAZEHEIGHTS[self.settings.currentLevel]))
        self.backgroundRect = self.background.get_rect()

        # initialize OpenGL shader
        if self.settings.shadersOn:
            self.shader = Shader(self.settings.RESOLUTION, self.settings)

        # precalculate half the width and half the height of the screen
        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2

        # initialize offset which is used to offset the display to center the view on the player
        self.offset = pygame.math.Vector2()

        # perspectiveOffset is used to offset each tile by a percentage (1 being no offset) to create fake perspective
        self.perspectiveOffset = 1.3

        self.get_neighbors = get_neighbors
        self.check_tile = check_tile

    def init_background(self):
        self.ySortSprites = []

        for sprite in self.sprites():
            if str(type(sprite)) == "<class 'tile.Tile'>":
                if not sprite.isWall:
                    self.blit(sprite, customScreen=self.background)
                else:
                    self.ySortSprites.append(sprite)
            else:
                self.ySortSprites.append(sprite)

    def init_light(self):
        """
        Sets the light object of the player
        """
        lightColor = self.settings.LIGHTCOLOR
        lightSize = self.settings.LIGHTRADIUS
        self.light = LIGHT(lightSize, pixel_shader(lightSize, lightColor, 1, False))


        # create shadow objects (walls, etc...)
        # the rect's y parameter must be adjusted to the TILESIZE
        self.shadow_objects = [pygame.Rect(tile.rect.topleft[0], tile.rect.topleft[1] / self.perspectiveOffset - self.settings.TILESIZE/12, self.settings.TILESIZE, self.settings.TILESIZE).inflate(0, -14) for tile in self.sprites() if str(type(tile)) == "<class 'tile.Tile'>" and tile.isWall]

        self.torches = []
        for sprite in self.sprites():
            if str(type(sprite)) == "<class 'objects.Torch'>":
                torch = LIGHT(lightSize, pixel_shader(lightSize, lightColor, 1, False))
                pos = (sprite.rect.centerx, sprite.rect.centery / self.perspectiveOffset)
                torch.baked_lighting(self.shadow_objects, pos[0], pos[1], pygame.Vector2(0, 0), False)

                self.torches.append([torch, pos])

    def render_light(self):
        """
        Blits the light on the screen with shadows cast from the shadow_objects
        """
        # reset screen
        lights_display = pygame.Surface((self.screen.get_size()))

        # global light darkens the background
        lights_display.blit(global_light(self.screen.get_size(), self.settings.LIGHTINTENSITY), (0, 0))

        # show lights
        self.light.main(self.shadow_objects, self.offset, lights_display, self.half_width, self.half_height)

        for torch, pos in self.torches:
            torch.main([], (0, 0), lights_display, pos[0] - self.offset.x, pos[1] - self.offset.y)

        # show the light on the screen
        self.screen.blit(lights_display, (0, 0), special_flags=BLEND_RGBA_MULT)

    def blit(self, sprite: pygame.sprite.Sprite, customScreen=None, customImage=None):
        """
        :param sprite: sprite to blit on the screen
        :param customScreen: custom screen onto which blit the image instead of the normal screen
        :param customImage: custom image to blit on the screen instead of the sprite's image
        Blits the sprite on the screen after applying the perspective offset
        """
        if customImage is not None:
            self.screen.blit(customImage, (sprite.rect.topleft[0] - self.offset.x,
                                           sprite.rect.topleft[1] / self.perspectiveOffset - self.offset.y))

        elif customScreen is not None:
            customScreen.blit(sprite.image, (sprite.rect.topleft[0] - self.offset.x,
                                             sprite.rect.topleft[1] / self.perspectiveOffset - self.offset.y))

        else:
            self.screen.blit(sprite.image, (sprite.rect.topleft[0] - self.offset.x,
                                            sprite.rect.topleft[1] / self.perspectiveOffset - self.offset.y))

    def custom_draw(self, player: pygame.sprite.Sprite, blackGradient):
        """
        :param player: player sprite (used to calculate the offset to center the screen)
        :return: draws with perspective all the sprites in the visible_sprites group
        """
        # reset screen
        self.screen.fill('black')

        # calculate offset of player to center of screen
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery / self.perspectiveOffset - self.half_height

        backgroundRect = pygame.Rect(self.backgroundRect.x - self.offset.x, self.backgroundRect.y - self.offset.y,
                                     self.backgroundRect.width, self.backgroundRect.height)
        self.screen.blit(self.background, backgroundRect)

        # we create a copy of the player sprite that we are going to cut to prevent overlap with the walls
        # we do that so that the player sprite isn't affected by lighting since it would cause some bugs
        cutPlayerSprite = player.image.copy()

        # draw every sprite sorted by y coordinate
        for sprite in sorted(self.ySortSprites, key=lambda sprite: sprite.rect.centery):
            # separate the player from the tiles
            if str(type(sprite)) == "<class 'tile.Tile'>":
                if sprite.isWall:
                    self.blit(sprite)

            elif str(type(sprite)) == "<class 'enemy.Enemy'>" or str(type(sprite)) == "<class 'objects.Torch'>":
                self.blit(sprite)

        # remove surrounding wall sprites from player image
        for sprite in self.get_neighbors(self.check_tile(player.rect.centerx // self.settings.TILESIZE,
                                                         player.rect.centery // self.settings.TILESIZE)):
            if sprite.isWall and sprite.rect.centery > player.rect.centery:
                pygame.draw.rect(cutPlayerSprite, (0, 0, 0, 0),
                                 pygame.Rect(sprite.rect.centerx - player.rect.centerx - 9,
                                            (sprite.rect.centery - player.rect.centery - 13) / self.perspectiveOffset,
                                             self.settings.TILESIZE, self.settings.TILESIZE))

        # lighting
        if self.settings.shadersOn:
            self.render_light()

        # draw player after lighting so that it is not affected
        self.blit(player, customImage=cutPlayerSprite)

        # fade in transition
        self.screen.blit(blackGradient, blackGradient.get_rect())

        # apply heart beat effect if activated
        scaledScreen = self.screen
        if self.settings.showHeartBeatEffect:
            if self.settings.dstToClosestEnemy <= 400:
                hearBeatEffectFactor = int((-self.settings.dstToClosestEnemy + 500)/100)

                scaledScreen = pygame.transform.scale(self.screen, (self.settings.WIDTH + hearBeatEffectFactor*10, self.settings.HEIGHT + hearBeatEffectFactor*10))
                scaledScreen.blit(scaledScreen, (random.randint(-hearBeatEffectFactor, hearBeatEffectFactor) - hearBeatEffectFactor*5,
                                                 random.randint(-hearBeatEffectFactor, hearBeatEffectFactor) - hearBeatEffectFactor*5))

        # and finally render screen
        if self.settings.shadersOn:
            self.shader.render(scaledScreen)
        else:
            pygame.display.get_surface().blit(self.screen, self.screen.get_rect())

    def draw_map(self, pos: (int, int), map, player: pygame.sprite.Sprite, enemies, size):
        display = pygame.display.get_surface()
        # get the rect of the map with the offset and show it
        rect = map[1].x + pos[0], map[1].y + pos[0]
        display.blit(map[0], rect)

        # get player image and scale it to fit the map, then show it
        player_image = pygame.Surface((self.settings.TILESIZE, self.settings.TILESIZE))
        player_image.fill(player.color)
        player_image = pygame.transform.scale(player_image, (self.settings.TILESIZE / size, self.settings.TILESIZE / size))

        player_rect = player_image.get_rect(center=(player.rect.centerx / size + pos[0], player.rect.centery / size + pos[1]))

        display.blit(player_image, player_rect)

        # show every enemy on the minimap
        for enemy in enemies:
            # get enemy image and scale it to fit the map, then show it
            enemy_image = pygame.Surface((self.settings.TILESIZE, self.settings.TILESIZE))
            enemy_image.fill(enemy.color)
            enemy_image = pygame.transform.scale(enemy_image, (self.settings.TILESIZE / size, self.settings.TILESIZE / size))

            enemy_rect = player_image.get_rect(center=(enemy.rect.centerx / size + pos[0], enemy.rect.centery / size + pos[1]))

            display.blit(enemy_image, enemy_rect)

    def debug_draw(self):
        for sprite in self.sprites():
            img = pygame.Surface((self.settings.TILESIZE, self.settings.TILESIZE))
            img.fill(sprite.color)
            rect = img.get_rect(topleft=(sprite.rect.topleft[0], sprite.rect.topleft[1]))
            self.screen.blit(img, rect)