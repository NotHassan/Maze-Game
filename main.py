import os
import pygame
import time
import glob
import re
from random import randint
from settings import TITLE, BACKGROUND_COLOR, WALL_COLOR, PLAYER_WIDTH, PLAYER_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, MENU_FONT_COLOR, MENU_BACKGROUND_COLOR
from player import Player
from map import Map

# Initialization
pygame.init()
pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Get list of all maps
maps = [re.sub(r'\./maps\\+(.*)\.bmp', r'\g<1>', file) for file in glob.glob('./maps/*')]

# Players Sprite List Group
player_list = pygame.sprite.Group()


def build_player(x=0, y=0):
    # The parameters the Player class takes are tile locations.
    # You are always spawned in the middle of a tile
    # (0, 0) will spawn you at the top left tile.
    player = Player(x, y)
    player_list.add(player)
    return player


# This builds the map based on the pixel colours within the .bmp file of the map
# Black pixels become the pathway
# Green pixels become the starting tiles
# Red pixels become the finishing tiles
# Every other colour becomes regular walls
def build_map(map_name='map1'):
    return Map(map_name)


# Starting menu splash screen
def game_intro():
    start_screen = True

    while start_screen:
        title_text = text(TITLE, y=(SCREEN_HEIGHT / 4))
        play_btn = text('Play', y=(SCREEN_HEIGHT / 4) + 70, font_size=40)
        quit_btn = text('Exit', y=(SCREEN_HEIGHT / 4) + 125, font_size=40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()

                if mouse[0] in range(play_btn['rect'].x, play_btn['rect'].x + play_btn['rect'].width) and mouse[1] in range(play_btn['rect'].y, play_btn['rect'].y + play_btn['rect'].height):
                    game_loop()

                if mouse[0] in range(quit_btn['rect'].x, quit_btn['rect'].x + quit_btn['rect'].width) and mouse[1] in range(quit_btn['rect'].y, quit_btn['rect'].y + quit_btn['rect'].height):
                    game_quit()

        screen.fill(MENU_BACKGROUND_COLOR)

        screen.blit(title_text['surface'], title_text['rect'])
        screen.blit(play_btn['surface'], play_btn['rect'])
        screen.blit(quit_btn['surface'], quit_btn['rect'])

        pygame.display.update()
        clock.tick(30)


# Main game loop used for when the game is actually being played
def game_loop():
    game_screen = True
    map = build_map(maps[randint(0, (len(maps) - 1))])
    player = build_player(map.start_pos['x'], map.start_pos['y'])
    start_time = time.perf_counter()

    while game_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        screen.fill(BACKGROUND_COLOR)

        player_list.update()
        map.update_list()

        map.draw(screen)
        player_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        space_top = 0
        space_bottom = 0
        space_left = 0
        space_right = 0

        # Get distance between player and walls for AI
        while True:
            # Calculate distance between player and closest top wall
            if (player.rect.y - space_top <= 0 or screen.get_at((player.rect.x + int(PLAYER_WIDTH / 2), player.rect.y - space_top)) == WALL_COLOR) and space_top is not -1:
                player.distance_top = space_top
                space_top = -1
            elif space_top is not -1:
                space_top += 1

            # Calculate distance between player and closest bottom wall
            if (player.rect.y + PLAYER_HEIGHT + space_bottom >= SCREEN_HEIGHT or screen.get_at((player.rect.x + int(PLAYER_WIDTH / 2), player.rect.y + PLAYER_HEIGHT + space_bottom)) == WALL_COLOR) and space_bottom is not -1:
                player.distance_bottom = space_bottom
                space_bottom = -1
            elif space_bottom is not -1:
                space_bottom += 1

            # Calculate distance between player and closest left wall
            if (player.rect.x - space_left <= 0 or screen.get_at((player.rect.x - space_left, player.rect.y + int(PLAYER_HEIGHT / 2))) == WALL_COLOR) and space_left is not -1:
                player.distance_left = space_left
                space_left = -1
            elif space_left is not -1:
                space_left += 1

            # Calculate distance between player and closest right wall
            if (player.rect.x + PLAYER_WIDTH + space_right >= SCREEN_WIDTH or screen.get_at((player.rect.x + PLAYER_WIDTH + space_right, player.rect.y + int(PLAYER_HEIGHT / 2))) == WALL_COLOR) and space_right is not -1:
                player.distance_right = space_right
                space_right = -1
            elif space_right is not -1:
                space_right += 1

            if space_top is -1 and space_bottom is -1 and space_left is -1 and space_right is -1:
                break

        player.controls()

        winner = pygame.sprite.spritecollide(player, map.finish_tiles_list, True)
        loser = pygame.sprite.spritecollide(player, map.wall_list, True)

        if winner:
            end_time = time.perf_counter()
            player.win = True
            game_screen = False
            winner.clear()
            game_win(end_time - start_time)

        if loser:
            player.lose = True
            game_screen = False
            loser.clear()
            game_over()


# Splash screen if the player beats the level
def game_win(speed):
    win_screen = True

    while win_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            win_screen = False
            game_reset()

        screen.fill(MENU_BACKGROUND_COLOR)

        message = text('Winner!')
        score = text('Time: {} seconds'.format(round(speed, 2)), y=(SCREEN_HEIGHT / 2 + 40), font_size=17)

        screen.blit(message['surface'], message['rect'])
        screen.blit(score['surface'], score['rect'])

        pygame.display.update()
        clock.tick(30)


# Splash screen if the player loses
def game_over():
    end_screen = True

    while end_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            end_screen = False
            game_reset()

        screen.fill(MENU_BACKGROUND_COLOR)

        gameover = text('Game Over')
        tryagain = text('Press Enter to try again...', y=(SCREEN_HEIGHT / 2 + 40), font_size=17)

        screen.blit(gameover['surface'], gameover['rect'])
        screen.blit(tryagain['surface'], tryagain['rect'])

        pygame.display.update()
        clock.tick(30)


# This empties the sprite group lists and runs the main game loop again
def game_reset():
    player_list.empty()
    player_list.update()

    game_loop()


def game_quit():
    pygame.quit()
    quit()


def text(text_str, x=(SCREEN_WIDTH / 2), y=(SCREEN_HEIGHT / 2), font='calibri', font_size=60, font_color=MENU_FONT_COLOR):
    font = pygame.font.SysFont(font, font_size)
    text_surf = font.render(text_str, True, font_color)
    text_rect = text_surf.get_rect()
    text_rect.center = (x, y)
    return {'surface': text_surf, 'rect': text_rect}


game_intro()
game_quit()
