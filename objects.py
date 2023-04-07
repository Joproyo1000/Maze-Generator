import pygame
import settings
import spatial_hashmap

from math import floor
from support import import_folder
from random import randint


class Torch(pygame.sprite.Sprite):
    def __init__(self, pos: (int, int), side: str, settings: settings.Settings, groups: [pygame.sprite.Group]):
        super().__init__(groups)
        # get the display surface
        self.screen = pygame.display.get_surface()

        self.settings = settings

        self.side = side

        # graphics setup
        self.import_object_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        # initialize rect (bounding box of the image) and hitbox (bounding box of the collision detection)
        self.rect = self.image.get_bounding_rect()
        self.rect.center = pos
        self.hitbox = self.rect

        # set color on the minimap
        self.color = 'white'

    def import_object_assets(self):
        """
        Loads the corresponding animation frames onto the object
        """
        if self.side == 'right':
            object_path = 'graphics/special/torch/'
            self.animations = {'right': []}

            for animation in self.animations:
                full_path = object_path + animation
                self.animations[animation] = import_folder(full_path, 5)

        self.image = self.animations['right'][0]

    def animate(self, dt):
        """
        Animates the torch based on the current status
        """
        animation = self.animations['right']

        # loop over the frame index
        self.frame_index += self.animation_speed * dt * 50
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self, dt):
        """
        Main update method
        """
        self.animate(dt)  # animate based on status


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos: (int, int), settings: settings.Settings, groups: [pygame.sprite.Group]):
        super().__init__(groups)
        # get the display surface
        self.screen = pygame.display.get_surface()

        self.settings = settings

        # graphics setup
        self.import_object_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        # current state of the chest, either closed or opened
        self.state = 'closed'

        # initialize rect (bounding box of the image) and hitbox (bounding box of the collision detection)
        # self.rect = self.image.get_rect(center=pos)
        self.rect = self.image.get_bounding_rect()
        self.rect.center = pos
        self.hitbox = self.rect

        # set color on the minimap
        self.color = self.settings.CHESTCOLOR

        # chose random item to put in the chest 0=freeze, 1=map, 2=scissors, 3=heal
        items = {0: Freeze(),
                 1: Map((self.rect.centerx / self.settings.MAZEWIDTHS[self.settings.currentLevel],
                        self.rect.centery / self.settings.MAZEHEIGHTS[self.settings.currentLevel])),
                 2: Scissors(),
                 3: Heal()}
        # self.item = items[randint(0, 3)]
        self.item = items[1]

    def import_object_assets(self):
        """
        Loads the corresponding animation frames onto the object
        """
        character_path = 'graphics/special/chest/'
        self.animations = {'closed': [], 'opened': []}

        for animation in self.animations:
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path, 5)

        self.image = self.animations['closed'][0]

    def open(self, player):
        """
        Change image to open chest sprite
        """
        if self.state != 'opened':
            animation = self.animations['opened']

            self.image = animation[0]
            player.inventory.append(self.item)

        self.state = 'opened'

    def close(self):
        """
        Change image to closed chest sprite
        """
        self.state = 'closed'

        animation = self.animations['closed']
        self.image = animation[0]


class CobWeb(pygame.sprite.Sprite):
    def __init__(self, pos, groups: [pygame.sprite.Group], obstacle_sprites: spatial_hashmap):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/special/cobweb.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.pos = pos

        obstacle_sprites.set(self.pos, self)


class Useable(pygame.sprite.Sprite):
    def use(self, *args, **kwargs):
        self.kill()


class Map(Useable):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos

    def use(self):
        self.kill()


class Freeze(Useable):
    def __init__(self):
        super().__init__()

    def use(self):
        # TODO freeze if facing enemy
        self.kill()


class Heal(Useable):
    def __init__(self):
        super().__init__()

    def use(self):
        # TODO freeze if facing enemy
        self.kill()


class Scissors(Useable):
    def __init__(self):
        super().__init__()

    def use(self):
        # TODO cut facing wall
        self.kill()
