import pygame
import settings

from math import floor
from support import import_folder
from objects import CobWeb


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos: (int, int), type: str, speed: float, FOV: int, AI:bool, settings: settings.Settings, groups: [pygame.sprite.Group], obstacle_sprites: [pygame.sprite.Sprite]):
        """
        :param pos: spawn position of the enemy
        :param type: type of the enemy
        :param FOV: distance at which the player can be seen by the enemy in pixels
        :param AI: activates or no pathfinding for enemy
        :param settings: general settings (same as in the maze level)
        :param groups: groups in which the enemy should be
        :param obstacle_sprites: group of obstacles
        """
        super().__init__(groups)
        # get the display surface
        self.screen = pygame.display.get_surface()

        # get settings
        self.settings = settings

        # set type
        self.type = type

        # graphics setup
        self.import_ennemy_assets()
        self.status = 'left'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.color = 'darkred'

        self.rect = self.image.get_bounding_rect()
        self.rect.center = pos
        self.hitbox = self.rect

        # movement
        self.direction = pygame.math.Vector2()
        self.normalSpeed = speed + self.settings.DIFFICULTY/10
        self.slowedSpeed = self.normalSpeed / 2
        self.speed = self.normalSpeed

        # pathfinding
        self.path = []
        self.AI = AI
        self.range = FOV

        self.obstacle_sprites = obstacle_sprites
        self.obstacle = pygame.sprite.Group()

    def import_ennemy_assets(self):
        """
        :param type: type of the ennemy
        Loads the corresponding animation frames onto the ennemy
        """
        if self.type == 'wolf':
            character_path = 'graphics/enemies/wolf/'
            self.animations = {'left': [], 'right': [],
                               'left_idle': [], 'right_idle': []}

            for animation in self.animations:
                full_path = character_path + animation
                self.animations[animation] = import_folder(full_path, 1.6)

        if self.type == 'spider':
            character_path = 'graphics/enemies/spider/'
            self.animations = {'left': [], 'right': [],
                               'left_idle': [], 'right_idle': []}

            for animation in self.animations:
                full_path = character_path + animation
                self.animations[animation] = import_folder(full_path, 1.6)

        if self.type == 'slime':
            character_path = 'graphics/enemies/slime/'
            self.animations = {'up': [], 'left': [], 'down': [], 'right': [],
                               'up_idle': [], 'left_idle': [], 'down_idle': [], 'right_idle': []}

            for animation in self.animations:
                full_path = character_path + animation
                self.animations[animation] = import_folder(full_path, 1.6)

        self.image = self.animations['left_idle'][0]

    def set_status(self):
        """
        Set the current status of the enemy for animation
        """
        if self.type == 'slime':
            if self.direction.y < 0:
                self.status = 'up'

            elif self.direction.y > 0:
                self.status = 'down'

            if self.direction.y < 0 and 0 > self.direction.x > self.direction.y:
                self.status = 'up'

            if self.direction.y > 0 and 0 < self.direction.x < self.direction.y:
                self.status = 'down'

        if self.direction.x < 0:
            self.status = 'left'

        elif self.direction.x > 0:
            self.status = 'right'

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if '_idle' not in self.status:
                self.status = self.status + '_idle'

    def followPath(self, path=True, replace=False):
        if replace and path:
            self.path = path
        if len(self.path) != 0:
            target = self.path[0]

            self.direction = pygame.math.Vector2(target.rect.centerx - self.rect.centerx,
                                                 target.rect.centery - self.rect.centery)

            if self.direction.length() < self.settings.TILESIZE/2:
                self.path.pop(0)

    def move(self, speed: float, dt: float):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

            self.hitbox.x += self.direction.x * speed * dt * 250
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * speed * dt * 250
            self.collision('vertical')

            self.rect.center = self.hitbox.center

    def collision(self, direction):
        """
        :param direction: either 'horizontal' or 'vertical'. Checks collision with the walls on either directions
        If collision occurs, stop the enemy
        """
        inCobweb = False

        if direction == 'horizontal':
            for sprite in self.obstacle_sprites.get_neighbors(self.rect.center):
                if sprite.hitbox.colliderect(self.hitbox):
                    if str(type(sprite)) == "<class 'objects.CobWeb'>":
                        if self.type != 'spider':
                            inCobweb = True
                    else:
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites.get_neighbors(self.rect.center):
                if sprite.hitbox.colliderect(self.hitbox):
                    if str(type(sprite)) == "<class 'objects.CobWeb'>":
                        if self.type != 'spider':
                            inCobweb = True
                    else:
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom

        if inCobweb:
            self.speed = self.slowedSpeed
        else:
            self.speed = self.normalSpeed

    def spawnCobweb(self, visible_sprites):
        cobweb = CobWeb(self.rect.center, [visible_sprites], self.obstacle_sprites)
        visible_sprites.ySortSprites.append(cobweb)

        return cobweb

    def animate(self, dt):
        """
        Animates the ennemy based on the current status
        """
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed * dt * 50
        if self.frame_index >= len(animation) - self.animation_speed:
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self, dt):
        self.set_status()  # set status
        self.animate(dt)  # animate based on status
        self.move(self.speed, dt)  # move based on path
