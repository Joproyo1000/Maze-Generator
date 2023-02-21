import pygame


class YSortIsoCameraGroup(pygame.sprite.Group):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        # get the display surface
        self.screen = pygame.display.get_surface()

        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2

        self.offsetToCenterX, self.offsetToCenterY = (self.settings.WIDTH - self.settings.MAZEWIDTH) // 2, (self.settings.HEIGHT - self.settings.MAZEHEIGHT) // 2

        self.offset = pygame.math.Vector2()
        self.isoOffset = pygame.math.Vector2(0.47, 0.45)

    def blit(self, sprite):
        self.screen.blit(sprite.image, (sprite.rect.centerx * self.isoOffset.x + sprite.rect.centery * -self.isoOffset.x - self.offset.x,
                                        sprite.rect.centerx * self.isoOffset.y + sprite.rect.centery * self.isoOffset.y - self.offset.y))

    def custom_draw(self, player):
        # calculate offset of player to center of screen
        self.offset.x = player.rect.x * self.isoOffset.x - player.rect.y * self.isoOffset.x - self.half_width + self.settings.TILESIZE/2
        self.offset.y = player.rect.x * self.isoOffset.y + player.rect.y * self.isoOffset.y - self.half_height + self.settings.TILESIZE

        mazeSprites = [sprite for sprite in self.sprites() if not (str(type(sprite)) == "<class 'player.Player'>" or str(type(sprite)) == "<class 'enemy.Enemy'>")]

        for sprite in mazeSprites:
            if not sprite.isWall:
                self.blit(sprite)

        for sprite in sorted(self.sprites(), key=lambda sprite: (sprite.rect.centerx * self.isoOffset.x + sprite.rect.centery * self.isoOffset.x,
                                                                 sprite.rect.centerx * self.isoOffset.y + sprite.rect.centery * self.isoOffset.y)):
            # separate the player from the tiles
            if not (str(type(sprite)) == "<class 'player.Player'>" or str(type(sprite)) == "<class 'enemy.Enemy'>"):
                if sprite.isWall:
                    self.blit(sprite)
            else:
                self.blit(sprite)

        # overlay = pygame.surface.Surface((self.settings.WIDTH, self.settings.HEIGHT)).convert_alpha()
        # overlay.fill(pygame.Color(2, 2, 10, 150))
        # self.screen.blit(overlay, overlay.get_rect())

    def draw_map(self, pos, map, player, size):
        rect = map[1].x + pos[0], map[1].y + pos[0]
        self.screen.blit(map[0], rect)
        player_image = pygame.Surface((self.settings.TILESIZE, self.settings.TILESIZE))
        player_image.fill(player.color)
        player_image = pygame.transform.scale(player_image, (self.settings.TILESIZE / size, self.settings.TILESIZE / size))
        player_rect = player_image.get_rect(center=(player.rect.centerx / size + pos[0], player.rect.centery / size + pos[1]))
        self.screen.blit(player_image, player_rect)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        # get the display surface
        self.screen = pygame.display.get_surface()

        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2

        self.offset = pygame.math.Vector2()

    def blit(self, sprite):
        self.screen.blit(sprite.image, (sprite.rect.topleft[0] - self.offset.x,
                                        sprite.rect.topleft[1]/1.3 - self.offset.y))

    def custom_draw(self, player):
        # calculate offset of player to center of screen
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery/1.3 - self.half_height

        mazeSprites = [sprite for sprite in self.sprites() if not (str(type(sprite)) == "<class 'player.Player'>" or str(type(sprite)) == "<class 'enemy.Enemy'>")]

        for sprite in mazeSprites:
            if not sprite.isWall:
                self.blit(sprite)

        for sprite in sorted(self.sprites(), key=lambda sprite: (sprite.rect.centery)):
            # separate the player from the tiles
            if not (str(type(sprite)) == "<class 'player.Player'>" or str(type(sprite)) == "<class 'enemy.Enemy'>"):
                if sprite.isWall:
                    self.blit(sprite)
            else:
                self.blit(sprite)

        # overlay = pygame.surface.Surface((self.settings.WIDTH, self.settings.HEIGHT)).convert_alpha()
        # overlay.fill(pygame.Color(2, 2, 10, 150))
        # self.screen.blit(overlay, overlay.get_rect())

    def draw_map(self, pos, map, player, enemies, size):
        # get the rect of the map with the offset and show it
        rect = map[1].x + pos[0], map[1].y + pos[0]
        self.screen.blit(map[0], rect)

        # get player image and scale it to fit the map, then show it
        player_image = pygame.Surface((self.settings.TILESIZE, self.settings.TILESIZE))
        player_image.fill(player.color)
        player_image = pygame.transform.scale(player_image, (self.settings.TILESIZE / size, self.settings.TILESIZE / size))

        player_rect = player_image.get_rect(center=(player.rect.centerx / size + pos[0], player.rect.centery / size + pos[1]))

        self.screen.blit(player_image, player_rect)

        # show every enemy on the minimap
        for enemy in enemies:
            # get enemy image and scale it to fit the map, then show it
            enemy_image = pygame.Surface((self.settings.TILESIZE, self.settings.TILESIZE))
            enemy_image.fill(enemy.color)
            enemy_image = pygame.transform.scale(enemy_image, (self.settings.TILESIZE / size, self.settings.TILESIZE / size))

            enemy_rect = player_image.get_rect(center=(enemy.rect.centerx / size + pos[0], enemy.rect.centery / size + pos[1]))

            self.screen.blit(enemy_image, enemy_rect)

    def debug_draw(self):
        for sprite in self.sprites():
            img = pygame.Surface((self.settings.TILESIZE, self.settings.TILESIZE))
            img.fill(sprite.color)
            rect = img.get_rect(topleft=(sprite.rect.topleft[0], sprite.rect.topleft[1]))
            self.screen.blit(img, rect)