import pygame
from sys import exit
from random import choice
from player import Player


def gradientRect(screen, left_colour, right_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering target_rect """
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour, (0, 0), (1, 0))
    pygame.draw.line(colour_rect, right_colour, (0, 1), (1, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    screen.blit(colour_rect, target_rect)


def check_cell(x: int, y: int) -> object:
    """
    Converts cell from x, y position to a 1D position on the cell grid
    :param x: x position on the 2D grid
    :param y: y position on the 2D grid
    :return: corresponding cell on the 1D grid
    """
    find_index = lambda x, y: x + y * cols

    if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
        return False

    return obstacles.sprites()[find_index(x, y)]


def remove_walls(current: object, next: object):
    """
    Removes walls between current and next cell
    :param current: current cell whose walls are changed
    :param next: next cell being checked
    """
    dx = current.rect.x - next.rect.x
    dy = current.rect.y - next.rect.y

    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    elif dy == 1:
        current.walls['top'] = False
        next.walls['bot'] = False
    elif dy == -1:
        current.walls['bot'] = False
        next.walls['top'] = False


def add_3D_walls(current: object):
    cell3D = check_cell(current.rect.x - 1, current.rect.y)
    x, y = current.rect.x * TILESIZE + offsetToCenterX, current.rect.y * TILESIZE + offsetToCenterY

    if cell3D:
        if cell3D.walls['top']:
            if not cell3D.rect.x == 0:
                wall3D = pygame.rect.Rect(x - TILESIZE - LINEWIDTH + 1, y, TILESIZE + LINEWIDTH + 1, OFFSET3D)
                gradientRect(screen, pygame.Color('darkorange'), pygame.Color(139, 64, 0), wall3D)

    if current.walls['top']:
        if current.walls['right']:
            wall3D = pygame.rect.Rect(x, y, TILESIZE - LINEWIDTH, OFFSET3D)
            gradientRect(screen, pygame.Color('darkorange'), pygame.Color(139, 64, 0), wall3D)
        if current.walls['left']:
            wall3D = pygame.rect.Rect(x + LINEWIDTH, y, TILESIZE, OFFSET3D)
            gradientRect(screen, pygame.Color('darkorange'), pygame.Color(139, 64, 0), wall3D)

    if current.walls['bot']:
        wall3D = pygame.rect.Rect(x, y + TILESIZE, TILESIZE + LINEWIDTH - 1, OFFSET3D)
        gradientRect(screen, pygame.Color('darkorange'), pygame.Color(139, 64, 0), wall3D)


def add_3D_shadows(current: object):
    x, y = current.rect.x * TILESIZE + offsetToCenterX, current.rect.y * TILESIZE + offsetToCenterY

    # check if cell as top
    if current.walls['top']:
        # draw shadow
        darkGradient = pygame.rect.Rect(x, y + OFFSET3D, TILESIZE, OFFSET3D)

        # if cell as right
        leftCell = check_cell(current.rect.x - 1, current.rect.y)
        if leftCell:
            if leftCell.walls['right']:
                darkGradient = pygame.rect.Rect(x + LINEWIDTH, y + OFFSET3D, TILESIZE, OFFSET3D)

        # if cell as left
        rightCell = check_cell(current.rect.x + 1, current.rect.y)
        if rightCell:
            if rightCell.walls['left']:
                darkGradient = pygame.rect.Rect(x, y + OFFSET3D, TILESIZE - LINEWIDTH, OFFSET3D)

        # if cell as both left and right
        if leftCell and rightCell:
            if leftCell.walls['right'] and rightCell.walls['left']:
                darkGradient = pygame.rect.Rect(x + LINEWIDTH, y + OFFSET3D, TILESIZE - 2 * LINEWIDTH, OFFSET3D)

        # if cell is on border
        if not leftCell:
            darkGradient = pygame.rect.Rect(x + 2 * LINEWIDTH, y + OFFSET3D, TILESIZE, OFFSET3D)
        if not rightCell:
            darkGradient = pygame.rect.Rect(x, y + OFFSET3D, TILESIZE - LINEWIDTH, OFFSET3D)

        # if cell is on border and as right
        if not leftCell and rightCell:
            if rightCell.walls['left']:
                darkGradient = pygame.rect.Rect(x + LINEWIDTH, y + OFFSET3D, TILESIZE - 2 * LINEWIDTH, OFFSET3D)

        # if cell is on border and as left
        if not rightCell and leftCell:
            if leftCell.walls['right']:
                darkGradient = pygame.rect.Rect(x + LINEWIDTH, y + OFFSET3D, TILESIZE - 2 * LINEWIDTH, OFFSET3D)

        gradientRect(screen, pygame.Color(30, 30, 30), pygame.Color(50, 50, 50), darkGradient)


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('graphics/maze/baseCell.png').convert_alpha()
        self.rect = pygame.rect.Rect(x, y, TILESIZE, TILESIZE)
        self.mask = pygame.mask.from_surface(self.image)

        self.walls = {'top': True, 'left': True, 'bot': True, 'right': True}
        self.visited = False

    def draw_png(self):
        """
        draws the cell on the self.image
        """
        if self.walls['top']:
            pygame.draw.line(self.image, 'white', (0, 0), (TILESIZE, 0), LINEWIDTH)
        if self.walls['left']:
            pygame.draw.line(self.image, 'white', (0, 0), (0, TILESIZE), LINEWIDTH)
        if self.walls['bot']:
            pygame.draw.line(self.image, 'white', (0, TILESIZE - LINEWIDTH), (TILESIZE, TILESIZE - LINEWIDTH), LINEWIDTH)
        if self.walls['right']:
            pygame.draw.line(self.image, 'white', (TILESIZE - LINEWIDTH, 0), (TILESIZE - LINEWIDTH, TILESIZE), LINEWIDTH)

    def draw_current_cell(self):
        """
        draws the current cell as different color
        """
        x, y = self.rect.x * TILESIZE + offsetToCenterX, self.rect.y * TILESIZE + offsetToCenterY
        pygame.draw.rect(screen, 'saddlebrown',
                         (x + LINEWIDTH, y + LINEWIDTH, TILESIZE - LINEWIDTH, TILESIZE - LINEWIDTH))

    def draw(self):
        """
        draws cell on the screen
        """
        x, y = self.rect.x * TILESIZE + offsetToCenterX, self.rect.y * TILESIZE + offsetToCenterY

        if self.visited:
            pygame.draw.rect(screen, pygame.Color(50, 50, 50), (x, y, TILESIZE, TILESIZE))

        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y), (x + TILESIZE, y), LINEWIDTH)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y), (x, y + TILESIZE), LINEWIDTH)
        if self.walls['bot']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y + TILESIZE), (x + TILESIZE, y + TILESIZE), LINEWIDTH)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILESIZE - 1, y), (x + TILESIZE - 1, y + TILESIZE), LINEWIDTH)

    def check_neighbors(self):
        """
        Checks for neighbors in the cells surrounding the current cell
        :return: returns any possible neighbors to the current cell
        """
        neighbors = []

        top = check_cell(self.rect.x, self.rect.y - 1)
        left = check_cell(self.rect.x - 1, self.rect.y)
        bot = check_cell(self.rect.x, self.rect.y + 1)
        right = check_cell(self.rect.x + 1, self.rect.y)

        if top and not top.visited:
            neighbors.append(top)
        if left and not left.visited:
            neighbors.append(left)
        if bot and not bot.visited:
            neighbors.append(bot)
        if right and not right.visited:
            neighbors.append(right)

        return choice(neighbors) if neighbors else False

    def update_masks(self):
        self.mask = pygame.mask.from_surface(self.image)


""" PARAMETERS """

# set the resolution for the screen
RESOLUTION = WIDTH, HEIGHT = 1402, 802
MAZERESOLUTION = MAZEWIDTH, MAZEHEIGHT = 802, 602

# set the tilesize (larger ones means smaller maze)
TILESIZE = 70

# set the linewidth (best set to 2)
LINEWIDTH = 2

# amount of 3D offset
OFFSET3D = 20

# calculate how many columns and rows there are
cols, rows = MAZEWIDTH // TILESIZE, MAZEHEIGHT // TILESIZE

""" ================================================== """
""" ONLY FOR DEBUGGING, MAKES THE MAZE GENERATE SLOWER """
runSlow = False
runSlowFPS = 30
""" ================================================== """

""" VARIABLES """

# initialize pygame
pygame.init()

# set FPS
gameFPS = 60

# create the screen
screen = pygame.display.set_mode(RESOLUTION)

# create clock object
clock = pygame.time.Clock()

# calculates offset to center maze
offsetToCenterX, offsetToCenterY = (WIDTH - MAZEWIDTH) // 2, (HEIGHT - MAZEHEIGHT) // 2

# True if maze is done generating
mazeGenerated = False

# Groups
obstacles = pygame.sprite.Group([Cell(col, row) for row in range(rows) for col in range(cols)])
player = pygame.sprite.GroupSingle(Player((10, 10), obstacles, TILESIZE))

obstacleTest = pygame.sprite.Group()

# set first cell to the cell in the grid of index 0
current_cell = obstacles.sprites()[0]

# stack keeps track how which path as been taken
# can get to a size of (rows * cols)
stack = []


# generate maze fast
if not runSlow:
    # runs while maze not finished
    while stack or not obstacles.sprites()[0].visited:
        current_cell.visited = True
        current_cell.draw_current_cell()

        next_cell = current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()

    # when maze is generated, set FPS and mazeGenerated
    FPS = gameFPS
    mazeGenerated = True

    # saves every cell as a transparent PNG for collisions
    for index, cell in enumerate(obstacles.sprites()):
        cell.draw_png()
        cell.update_masks()

# main loop
while True:
    # set background color
    screen.fill(pygame.Color("darkslategray"))

    # used for taking inputs
    for event in pygame.event.get():
        # closes the game if the red cross button is pressed
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # shows tile index when clicked on
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttons = pygame.mouse.get_pressed(3)
            x, y = (pygame.mouse.get_pos()[0] - offsetToCenterX) // TILESIZE, (pygame.mouse.get_pos()[1] - offsetToCenterY) // TILESIZE
            cell = check_cell(x, y)
            if cell:
                if buttons[1]:
                    print(" x position :", cell.rect.x, "\n", "y position :", cell.rect.y)
                    #print(cell.walls)
                if buttons[0]:
                    cell.walls['left'] = not cell.walls['left']
                if buttons[2]:
                    cell.walls['right'] = not cell.walls['right']

    # draws every cell
    for i, cell in enumerate(obstacles.sprites()):
        cell.draw()
        #add_3D_shadows(cell)
        #add_3D_walls(cell)

    # === ONLY FOR DEBUGGING, GENERATES MAZE SLOWLY===
    if runSlow:

        # if maze is finished set mazeGenerated to True
        if not (stack or not obstacles.sprites()[0].visited):
            mazeGenerated = True

        if not mazeGenerated:
            current_cell.visited = True
            current_cell.draw_current_cell()

            FPS = runSlowFPS
            next_cell = current_cell.check_neighbors()
            if next_cell:
                next_cell.visited = True
                stack.append(current_cell)
                remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()

        else:
            FPS = gameFPS

    # handles player when maze is generated
    if mazeGenerated:
        player.sprite.custom_draw(offsetToCenterX, offsetToCenterY)
        player.update()

    # collision
    #print(obstacleTest.sprites()[0].rect.x)
    # for i in range(len(obstacles.sprites())):
    #     obstacleTest.add(obstacles.sprites()[i])
    #
    #     player.sprite.rect.x -= obstacleTest.sprites()[0].rect.x * TILESIZE
    #     player.sprite.rect.y -= obstacleTest.sprites()[0].rect.y * TILESIZE
    #
    #     if pygame.sprite.spritecollide(player.sprite, obstacleTest, False, pygame.sprite.collide_mask):
    #         print('collision')
    #         pass
    #
    #     player.sprite.rect.x += obstacleTest.sprites()[0].rect.x * TILESIZE
    #     player.sprite.rect.y += obstacleTest.sprites()[0].rect.y * TILESIZE
    #
    #     obstacleTest.remove(obstacles.sprites()[i])

    # draw display
    pygame.display.update()

    # set FPS
    clock.tick(FPS)
