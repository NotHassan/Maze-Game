import pygame
from PIL import Image

from settings import START_COLOR, END_COLOR, WALL_COLOR
from tile import Tile


class Map(pygame.sprite.Sprite):
    def __init__(self, mapFile='map'):
        super().__init__()

        self.wall_list = pygame.sprite.Group()
        self.start_tiles_list = pygame.sprite.Group()
        self.finish_tiles_list = pygame.sprite.Group()

        im = Image.open(f'maps/{mapFile}.bmp')
        arr = list(im.getdata())
        arr = [-1 if x is 6 else x for x in arr]
        arr = [-2 if x is 9 else x for x in arr]
        arr = [1 if x > 0 else x for x in arr]
        arr = [arr[i:i + 10] for i in range(0, len(arr), 10)]

        for x in range(len(arr)):
            for y in range(len(arr[x])):
                # Regular Wall
                if arr[y][x] is 1:
                    self.wall_list.add(Tile(x * 50, y * 50, WALL_COLOR))

                # Start Area
                if arr[y][x] is -1:
                    self.start_tiles_list.add(Tile(x * 50, y * 50, START_COLOR, 1))

                # Finish Area
                if arr[y][x] is -2:
                    self.finish_tiles_list.add(Tile(x * 50, y * 50, END_COLOR, 2))

        self.start_pos = {
            'x': (self.start_tiles_list.sprites()[0].rect.left / 50),
            'y': (self.start_tiles_list.sprites()[0].rect.top / 50)
        }

    def update_list(self):
        self.wall_list.update()
        self.start_tiles_list.update()
        self.finish_tiles_list.update()

    def draw(self, screen):
        self.wall_list.draw(screen)
        self.start_tiles_list.draw(screen)
        self.finish_tiles_list.draw(screen)
