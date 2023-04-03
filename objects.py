import pygame

import settings
from support import import_folder


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

        # set color on the minimap
        self.color = 'white'

        # initialize rect (bounding box of the image) and hitbox (bounding box of the collision detection)
        self.rect = self.image.get_rect(center=pos)

    def import_object_assets(self):
        """
        Loads the corresponding animation frames onto the object
        """
        if self.side == 'right':
            character_path = 'graphics/special/torch/'
            self.animations = {'right': []}

            for animation in self.animations:
                full_path = character_path + animation
                self.animations[animation] = import_folder(full_path, 5)

        self.image = self.animations['right'][0]

    def animate(self, dt):
        """
        Animates the player based on the current status
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
