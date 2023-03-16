import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: (int, int), type: str, TILESIZE: int, groups: [pygame.sprite.Group], obstacle_sprites: [pygame.sprite.Sprite]):
        super().__init__(groups)
        # get the display surface
        self.screen = pygame.display.get_surface()

        # graphics setup
        self.import_player_assets(type)
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # set color on the minimap
        self.color = 'gold'

        # initialize rect (bounding box of the image) and hitbox (bounding box of the collision detection)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-TILESIZE//3, -TILESIZE//10)  # the 3 and 10 must be adjusted to the TILESIZE

        # initialize direction vector and speed which is proportional to the tilesize
        self.direction = pygame.math.Vector2()
        self.speed = 0.3
        self.speed *= TILESIZE/10

        self.obstacle_sprites = obstacle_sprites
        self.obstacle = pygame.sprite.Group()

        self.TILESIZE = TILESIZE

    def import_player_assets(self, type: str):
        """
        :param type: type of the player either 'boy' or 'girl'
        Loads the corresponding animation frames onto the player
        """
        if type == 'boy':
            character_path = 'graphics/player/boy/'
            self.animations = {'up': [], 'left': [], 'down': [], 'right': [],
                               'up_idle': [], 'left_idle': [], 'down_idle': [], 'right_idle': []}

            for animation in self.animations:
                full_path = character_path + animation
                self.animations[animation] = import_folder(full_path, 1.6)

        if type == 'girl':
            character_path = 'graphics/player/girl/'
            self.animations = {'up': [], 'left': [], 'down': [], 'right': [],
                               'up_idle': [], 'left_idle': [], 'down_idle': [], 'right_idle': []}

            for animation in self.animations:
                full_path = character_path + animation
                self.animations[animation] = import_folder(full_path, 1.6)

        self.image = pygame.image.load('graphics/player/boy/down_idle/boy_sprite_front_idle1.png')

    def input(self):
        """
        Updates direction based on input
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.status = 'down'
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_q]:
            self.status = 'left'
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.status = 'right'
            self.direction.x = 1
        else:
            self.direction.x = 0

    def get_status(self):
        """
        Set the current status of the player for animation
        """
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not '_idle' in self.status:
                self.status = self.status + '_idle'

    def move(self, speed: int):
        """
        :param speed: speed of the player when moving
        Moves the player after applying collisions
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def collision(self, direction: str):
        """
        :param direction: either 'horizontal' or 'vertical'. Checks collision with the walls on either directions
        If collision occurs, stop the player
        """
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

    def animate(self):
        """
        Animates the player based on the current status
        """
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        """
        Main update method
        """
        self.input()  # get inputs
        self.get_status()  # get status
        self.animate()  # animate based on status
        self.move(self.speed)  # move based on inputs
