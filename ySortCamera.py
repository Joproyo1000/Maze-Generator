import pygame


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        # get the display surface
        self.screen = pygame.display.get_surface()

        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2

        self.offsetToCenterX, self.offsetToCenterY = (self.settings.WIDTH - self.settings.MAZEWIDTH) // 2, (self.settings.HEIGHT - self.settings.MAZEHEIGHT) // 2

        self.offset = pygame.math.Vector2()
        self.correctionX = 2.1
        self.correctionY = 2.3

    def blit(self, sprite, isWall):
        self.screen.blit(sprite.image, (sprite.rect.centerx / self.correctionX - sprite.rect.centery / self.correctionX - self.offset.x,
                                        sprite.rect.centerx / self.correctionY + sprite.rect.centery / self.correctionY - self.offset.y + 10 * isWall))

    def custom_draw(self, player):
        # calculate offset of player to center of screen
        self.offset.x = player.rect.centerx / self.correctionX - player.rect.centery / self.correctionX - self.half_width
        self.offset.y = player.rect.centerx / self.correctionY + player.rect.centery / self.correctionY - self.half_height

        mazeSprites = [sprite for sprite in self.sprites() if not str(type(sprite)) == "<class 'player.Player'>"]

        for sprite in mazeSprites:
            if not sprite.isWall:
                self.blit(sprite, False)

        #for sprite in sorted(self.sprites(), key=lambda sprite: (round(sprite.rect.centerx * TILESIZE) / TILESIZE)):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            # separate the player from the tiles
            if not str(type(sprite)) == "<class 'player.Player'>":
                if sprite.isWall:
                    self.blit(sprite, False)
            else:
                self.blit(player, True)

    def debug_draw(self, size):
        for sprite in self.sprites():
            offset = (sprite.rect.topleft[0] + self.offsetToCenterX) / size + 20, (sprite.rect.topleft[1] + self.offsetToCenterY) / size + 50
            img = pygame.transform.smoothscale(sprite.image, (sprite.image.get_width() / size, sprite.image.get_height() / size))
            img.fill(sprite.color)
            self.screen.blit(img, offset)
