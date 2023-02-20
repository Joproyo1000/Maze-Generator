import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, settings, pos, isWall, groups):
        super().__init__(groups)
        self.settings = settings

        self.image = pygame.image.load('graphics/maze/IsoBushv2.png').convert_alpha()
        scale = self.settings.TILESIZE/20
        self.image = pygame.transform.scale(self.image, (20 * scale, 26 * scale))
        self.path = pygame.image.load('graphics/maze/IsoPathv2.png').convert_alpha()
        self.path = pygame.transform.scale(self.path, (20 * scale, 26 * scale))

        self.rect = pygame.rect.Rect(pos[0], pos[1], min(self.image.get_width(), self.image.get_height()), min(self.image.get_width(), self.image.get_height()))

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.hitbox = self.rect.inflate(0, 0)
        self.hitbox.y -= 10

        self.pos = pygame.Vector2(pos)

        self.color = self.settings.WALLCOLOR

        self.isWall = isWall

    def draw_current(self):
        self.color = self.settings.CURRENTCOLOR

    def update_color(self):
        if self.isWall:
            self.color = self.settings.WALLCOLOR
        else:
            self.color = self.settings.PATHCOLOR
            self.image = self.path
