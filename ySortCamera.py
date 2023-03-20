import pygame.sprite

import settings
from Pygame_Lights import *
from shaders import Shader


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, settings: settings.Settings):
        super().__init__()

        # copy settings to self to access them in the whole class
        self.settings = settings

        # get the display surface
        self.screen = pygame.surface.Surface((self.settings.WIDTH, self.settings.HEIGHT))

        # initialize OpenGL shader
        if self.settings.shadersOn:
            self.shader = Shader(self.settings.RESOLUTION)

        # precalculate half the width and half the height of the screen
        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2

        # initialize offset which is used to offset the display to center the view on the player
        self.offset = pygame.math.Vector2()

        # perspectiveOffset is used to offset each tile by a percentage (1 being no offset) to create fake perspective
        self.perspectiveOffset = 1.3

    def initLight(self):
        """
        Sets the light object of the player
        """
        lightColor = self.settings.LIGHTCOLOR
        lightSize = self.settings.LIGHTRADIUS
        self.light = LIGHT(lightSize, pixel_shader(lightSize, lightColor, 1, False))
        # create shadow objects (walls, etc...)
        # the rect's y parameter must be adjusted to the TILESIZE
        self.shadow_objects = [pygame.Rect(tile.rect.topleft[0], tile.rect.topleft[1] / self.perspectiveOffset - self.settings.TILESIZE/12, self.settings.TILESIZE, self.settings.TILESIZE).inflate(0, -14) for tile in self.sprites() if not (str(type(tile)) == "<class 'player.Player'>" or str(type(tile)) == "<class 'enemy.Enemy'>") and tile.isWall]

    def renderLight(self):
        """
        Blits the light on the screen with shadows cast from the shadow_objects
        """
        # reset screen
        lights_display = pygame.Surface((self.screen.get_size()))

        # global light darkens the background
        lights_display.blit(global_light(self.screen.get_size(), self.settings.LIGHTINTENSITY), (0, 0))
        # main light
        self.light.main(self.shadow_objects, self.offset, lights_display, self.half_width, self.half_height)

        # show the light on the screen
        self.screen.blit(lights_display, (0, 0), special_flags=BLEND_RGBA_MULT)

    def blit(self, sprite: pygame.sprite.Sprite, customImage=None):
        """
        :param sprite: sprite to blit on the screen
        :return: blits the sprite on the screen after applying the perspective offset
        """
        if customImage is not None:
            self.screen.blit(customImage, (sprite.rect.topleft[0] - self.offset.x,
                                           sprite.rect.topleft[1] / self.perspectiveOffset - self.offset.y))
        else:
            self.screen.blit(sprite.image, (sprite.rect.topleft[0] - self.offset.x,
                                            sprite.rect.topleft[1] / self.perspectiveOffset - self.offset.y))

    def custom_draw(self, player: pygame.sprite.Sprite):
        """
        :param player: player sprite (used to calculate the offset to center the screen)
        :return: draws with perspective all the sprites in the visible_sprites group
        """
        # reset screen
        self.screen.fill('black')

        # calculate offset of player to center of screen
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery / self.perspectiveOffset - self.half_height

        mazeSprites = [sprite for sprite in self.sprites() if not (str(type(sprite)) == "<class 'player.Player'>" or str(type(sprite)) == "<class 'enemy.Enemy'>")]

        for sprite in mazeSprites:
            if not sprite.isWall:
                self.blit(sprite)

        # we create a copy of the player sprite that we are going to cut to prevent overlap with the walls
        # we do that so that the player sprite isn't affected by lighting since it would cause some bugs
        cutPlayerSprite = player.image.copy()

        # draw every sprite sorted by y coordinate
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # separate the player from the tiles
            if not (str(type(sprite)) == "<class 'player.Player'>" or str(type(sprite)) == "<class 'enemy.Enemy'>"):
                if sprite.isWall:
                    self.blit(sprite)

                    # remove wall sprite from player,
                    if sprite.rect.centery > player.rect.centery:
                        pygame.draw.rect(cutPlayerSprite, (0, 0, 0, 0),
                                         pygame.Rect(sprite.rect.centerx - player.rect.centerx - 9,
                                                    (sprite.rect.centery - player.rect.centery - 13) / self.perspectiveOffset,
                                                     self.settings.TILESIZE, self.settings.TILESIZE))
            elif str(type(sprite)) == "<class 'enemy.Enemy'>":
                self.blit(sprite)

        # lighting
        self.renderLight()

        # draw player after lighting so that it is not affected
        self.blit(player, customImage=cutPlayerSprite)

        # and finally render screen
        if self.settings.shadersOn:
            self.shader.render(self.screen)
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