import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, settings, pos, isWall, groups):
        super().__init__(groups)
        self.settings = settings

        self.image = pygame.image.load('graphics/maze/Bush - Copie.png').convert_alpha()
        scale = self.settings.TILESIZE/27
        self.image = pygame.transform.scale(self.image, (27 * scale, 37 * scale))
        self.path = pygame.image.load('graphics/maze/Grass.png').convert_alpha()
        self.path = pygame.transform.scale(self.path, (27 * scale, 37 * scale))

        self.rect = pygame.rect.Rect(pos[0], pos[1], min(self.image.get_width(), self.image.get_height()), min(self.image.get_width(), self.image.get_height()))

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.hitbox = self.rect.inflate(-10, -10)

        self.pos = pygame.Vector2(pos)

        self.color = self.settings.WALLCOLOR

        self.isWall = isWall

        # pathfinding variables
        self.gCost = 0
        self.hCost = 0

        self.parent = None

    def __lt__(self, other):
        compare = False if self.fCost() == other.fCost() else self.fCost() < other.fCost()
        if compare == False:
            compare = self.hCost < other.hCost
        return compare

    def fCost(self):
        return self.gCost + self.hCost

    def reset(self):
        self.gCost = 0
        self.hCost = 0

    def draw_current(self):
        self.color = self.settings.CURRENTCOLOR

    def update_color(self):
        if self.isWall:
            self.color = self.settings.WALLCOLOR
        else:
            self.color = self.settings.PATHCOLOR
            self.image = self.path
