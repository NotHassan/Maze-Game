import pygame
from settings import PLAYER_COLOR, MOVE_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.win = False
        self.lose = False

        self.distance_top = 0
        self.distance_bottom = 0
        self.distance_left = 0
        self.distance_right = 0

        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.image = pygame.Surface([self.width, self.height])

        pygame.draw.rect(self.image, PLAYER_COLOR, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = (x * 50 + 20)
        self.rect.y = (y * 50 + 20)

    def move_up(self):
        if (self.rect.y - (self.height / 3)) > 0:
            self.rect.y -= MOVE_SPEED

    def move_down(self):
        if (self.rect.y + self.height + 2) < SCREEN_HEIGHT:
            self.rect.y += MOVE_SPEED

    def move_left(self):
        if (self.rect.x - (self.width / 3)) > 0:
            self.rect.x -= MOVE_SPEED

    def move_right(self):
        if (self.rect.x + self.width + 2) < SCREEN_WIDTH:
            self.rect.x += MOVE_SPEED

    def controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.move_up()

        if keys[pygame.K_DOWN]:
            self.move_down()

        if keys[pygame.K_LEFT]:
            self.move_left()

        if keys[pygame.K_RIGHT]:
            self.move_right()
