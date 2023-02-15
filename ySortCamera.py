import pygame
from settings import WIDTH, HEIGHT, MAZEWIDTH, MAZEHEIGHT


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # get the display surface
        self.screen = pygame.display.get_surface()

        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2

        self.offsetToCenterX, self.offsetToCenterY = (WIDTH - MAZEWIDTH) // 2, (HEIGHT - MAZEHEIGHT) // 2

        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # calculate offset of player to center of screen
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        sortedSprites = []

        for sprite in self.sprites():

            # separate the player from the tiles
            if str(type(sprite)) == "<class 'player.Player'>":
                sortedSprites.append(sprite)

            # if the sprite is a wall add it to the sortedSprites list
            elif sprite.isWall:
                sortedSprites.append(sprite)

            # else draw it now to not mess up the perspective
            else:
                offset_pos = sprite.rect.topleft - self.offset
                self.screen.blit(sprite.image, offset_pos)

        # for all other sprite we sort them and show them by y order to give an impression of depth
        for sprite in sorted(sortedSprites, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)

    def debug_draw(self):

        for sprite in self.sprites():
            if not (str(type(sprite)) == "<class 'player.Player'>"):
                offset = sprite.rect.topleft[0] + self.offsetToCenterX, sprite.rect.topleft[1] + self.offsetToCenterY
                self.screen.blit(sprite.image, offset)