import pygame
from settings import TILESIZE


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        # get the display surface
        self.screen = pygame.display.get_surface()

        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.inflate(0, 0)

        self.direction = pygame.math.Vector2()
        self.speed = 5

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
        #self.collision('horizontal', speed)
        self.hitbox.y += self.direction.y * speed
        #self.collision('vertical', speed)

        self.rect.center = self.hitbox.center

    def collision(self, direction, speed):
        if direction == 'horizontal':
            #if pygame.sprite.spritecollide(self, self.obstacle_sprites, False):
            for i in range(len(self.obstacle_sprites.sprites())):
                self.obstacle.add(self.obstacle_sprites.sprites()[i])

                self.rect.x -= self.obstacle.sprites()[0].rect.x * self.TILESIZE
                self.rect.y -= self.obstacle.sprites()[0].rect.y * self.TILESIZE

                # if collision
                if pygame.sprite.spritecollide(self, self.obstacle, False, pygame.sprite.collide_mask):
                    if self.direction.x > 0:  # moving left
                        self.hitbox.right -= self.direction.x * speed - 10
                    if self.direction.x < 0:  # moving right
                        self.hitbox.left += self.direction.x * speed + 10

                self.rect.x += self.obstacle.sprites()[0].rect.x * self.TILESIZE
                self.rect.y += self.obstacle.sprites()[0].rect.y * self.TILESIZE

                self.obstacle.remove(self.obstacle_sprites.sprites()[i])


        if direction == 'vertical':
            #if pygame.sprite.spritecollide(self, self.obstacle_sprites, False):
            for i in range(len(self.obstacle_sprites.sprites())):
                self.obstacle.add(self.obstacle_sprites.sprites()[i])

                self.rect.x -= self.obstacle.sprites()[0].rect.x * self.TILESIZE
                self.rect.y -= self.obstacle.sprites()[0].rect.y * self.TILESIZE

                # if collision
                if pygame.sprite.spritecollide(self, self.obstacle, False, pygame.sprite.collide_mask):
                    self.direction = -self.direction
                    # if self.direction.y > 0:  # moving up
                    #     self.hitbox.top -= self.direction.y * self.speed
                    # if self.direction.y < 0:  # moving down
                    #     self.hitbox.bottom -= self.direction.y * self.speed

                self.rect.x += self.obstacle.sprites()[0].rect.x * self.TILESIZE
                self.rect.y += self.obstacle.sprites()[0].rect.y * self.TILESIZE

                self.obstacle.remove(self.obstacle_sprites.sprites()[i])

    def update(self):
        self.input()
        self.move(self.speed)
