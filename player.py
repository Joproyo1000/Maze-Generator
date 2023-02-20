import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, type, TILESIZE, groups, obstacle_sprites):
        super().__init__(groups)
        # get the display surface
        self.screen = pygame.display.get_surface()

        if type == 'girl':
            self.player_back_walk = [pygame.transform.scale(pygame.image.load(f'graphics/player/girl_sprite_back{i}.png').convert_alpha(), (TILESIZE, TILESIZE)) for i in range(1, 5)]

        self.player_back_walk_way = 0.1
        self.player_index = 0
        self.image = self.player_back_walk[self.player_index]

        self.color = 'gold'

        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-TILESIZE//2, -TILESIZE//2)

        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.speed *= TILESIZE/10

        self.obstacle_sprites = obstacle_sprites
        self.obstacle = pygame.sprite.Group()

        self.TILESIZE = TILESIZE

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_q]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center
        self.depth = self.rect.x + self.rect.y

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.isWall:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.isWall:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom

    def animation_state(self):
        self.player_index += self.player_back_walk_way
        if self.player_index >= len(self.player_back_walk)-0.1 or self.player_index <= 0: self.player_back_walk_way = -self.player_back_walk_way
        self.image = self.player_back_walk[int(self.player_index)]

    def update(self):
        self.input()
        self.move(self.speed)
        self.animation_state()
