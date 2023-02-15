import pygame
from settings import TILESIZE, WALLCOLOR, PATHCOLOR


class Tile(pygame.sprite.Sprite):
    def __init__(self, color, pos, isWall, groups):
        super().__init__(groups)

        self.image = pygame.surface.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.hitbox = self.rect.inflate(0, -10)

        self.pos = pygame.Vector2(pos)

        self.isWall = isWall

    def draw_current(self):
        self.image.fill('saddlebrown')
        # offsetRect = self.rect.x + offsetX, self.rect.y + offsetY
        # screen.blit(self.image, offsetRect)

    def update_color(self):
        if self.isWall:
            self.image.fill(WALLCOLOR)
        else:
            self.image.fill(PATHCOLOR)

