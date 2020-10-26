import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, color, special=0):
        super().__init__()
        self.special = special
        self.width = 50
        self.height = 50
        self.image = pygame.Surface([self.width, self.height])

        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
