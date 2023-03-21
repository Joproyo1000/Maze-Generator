import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos: (int, int), type: str, range:int,  settings, groups: [pygame.sprite.Group], obstacle_sprites: pygame.sprite.Group):
        """
        :param pos: spawn position of the enemy
        :param type: type of the enemy
        :param range: distance at which the player can see the enemy in pixels
        :param settings: general settings (same as in the maze level)
        :param groups: groups in which the enemy should be
        :param obstacle_sprites: group of obstacles
        """
        super().__init__(groups)
        # get the display surface
        self.screen = pygame.display.get_surface()

        if type == 'wolf':
            self.frames = [pygame.transform.scale(pygame.image.load('graphics/enemies/test.png').convert_alpha(), (settings.TILESIZE, settings.TILESIZE))]

        self.enemy_walk_change = 0.1
        self.enemy_index = 0
        self.image = self.frames[self.enemy_index]

        self.color = 'darkred'

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hitbox = self.rect.inflate(-settings.TILESIZE//3, -settings.TILESIZE//3)

        self.direction = pygame.math.Vector2()
        self.speed = 0.5
        self.speed *= settings.TILESIZE/10
        self.path = []

        self.range = range

        self.obstacle_sprites = obstacle_sprites
        self.obstacle = pygame.sprite.Group()

        self.TILESIZE = settings.TILESIZE

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * speed
            self.collision('vertical')

            self.rect.center = self.hitbox.center

    def followPath(self, path=True, replace=False):
        if path:
            if replace:
                self.path = path
            target = self.path[0]

            self.direction = pygame.math.Vector2(target.rect.centerx - self.rect.centerx,
                                                 target.rect.centery - self.rect.centery)

            if pygame.math.Vector2(target.rect.centerx - self.rect.centerx,
                                   target.rect.centery - self.rect.centery).length() < self.TILESIZE/2:
                self.path.pop(0)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites.get_neighbors(self.rect.center):
                if sprite.isWall:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites.get_neighbors(self.rect.center):
                if sprite.isWall:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom

    def animation_state(self):
        self.enemy_index += self.enemy_walk_change
        if self.enemy_index >= len(self.frames)-0.1 or self.enemy_index <= 0:
            self.enemy_walk_change = -self.enemy_walk_change
        self.image = self.frames[int(self.enemy_index)]

    def update(self):
        self.move(self.speed)
        self.animation_state()
