import pygame
from random import randint
import json

pygame.init()
clock = pygame.time.Clock()


def display_score():
    if game_active:
        score_surf = game_font.render(f'{speed_count}', False, 'black')
        score_rect = score_surf.get_rect(center=(250, 100))
        screen.blit(score_surf, score_rect)
    else:
        score_surf = game_font.render(f'Score: {speed_count}', False, 'black')
        score_rect = score_surf.get_rect(center=(250, 100))
        screen.blit(score_surf, score_rect)


def get_high_score():
    with open('Files/high_score.json', 'r') as openfile:
        high_score_dict = json.load(openfile)

    return high_score_dict['Score']


def update_high_score(score):
    update = False
    with open('Files/high_score.json', 'r') as openfile:
        high_score_dict = json.load(openfile)
    if high_score_dict["Score"] <= score:
        high_score_dict["Score"] = score
        update = True
    else:
        high_score_dict = high_score_dict
    with open('Files/high_score.json', 'w') as outfile:
        json.dump(high_score_dict, outfile)
    return update


def display_high_score(new_high_score):
    if new_high_score:
        high_score_surf = game_font.render(f' NEW High Score: {get_high_score()}', False, 'black')
        high_score_rect = high_score_surf.get_rect(center=(250, 600))
        screen.blit(high_score_surf, high_score_rect)
    else:
        high_score_surf = game_font.render(f'High Score: {get_high_score()}', False, 'black')
        high_score_rect = high_score_surf.get_rect(center=(250, 600))
        screen.blit(high_score_surf, high_score_rect)


game_font = pygame.font.Font('Files/Pixeltype.ttf', 50)

color_list = ['lightcoral', 'tan1', 'lightgoldenrod', 'palegreen', ' lightskyblue', 'lightpink', 'mediumpurple1']

screen = pygame.display.set_mode((500, 750))
pygame.display.set_caption('FLAPPY SQUARE: RAINBOW EDITION')
bg = pygame.Surface((500, 750))
bg.fill('gray')

# Bird
bird_surf = pygame.Surface((50, 50))
bird_surf.fill('yellow')
bird_rect = bird_surf.get_rect(center=(100, 375))
bird_gravity = 0

# Pipes
size = randint(100, 601)
top_pipe_surf = pygame.Surface((100, 200))
top_pipe_surf.fill('dark green')
top_pipe_rect = top_pipe_surf.get_rect(midtop=(500, 0))

bot_pipe_surf = pygame.Surface((100, 200))
bot_pipe_surf.fill('dark green')
bot_pipe_rect = bot_pipe_surf.get_rect(midbottom=(500, 750))

intro_surf = game_font.render('PRESS SPACE TO FLAP', False, 'black')
intro_rect = intro_surf.get_rect(center=(250, 200))

pipe_speed = 3
speed_count = 0
color_rotation = 0
bird_rotation = 1
first_run = True

game_active = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_gravity = -15
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird_gravity = -15
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                speed_count = 0

    if game_active:
        # Background
        screen.blit(bg, (0, 0))
        intro_rect.x -= 3
        if intro_rect.x == -100:
            intro_rect.x = -100
        screen.blit(intro_surf, intro_rect)

        # Bird Actions
        bird_gravity += 1
        bird_rect.y += bird_gravity
        if bird_rect.bottom >= 750:
            game_active = False
        screen.blit(bird_surf, bird_rect)

        # Pipes
        top_pipe_rect.x -= pipe_speed
        if top_pipe_rect.x <= -100:
            size = randint(100, 500)
            top_pipe_surf = pygame.transform.scale(top_pipe_surf, (100, size))
            top_pipe_rect = top_pipe_surf.get_rect(midtop=(550, 0))
        screen.blit(top_pipe_surf, top_pipe_rect)

        bot_pipe_rect.x -= pipe_speed
        if bot_pipe_rect.x <= -100:
            speed_count += 1
            bot_height = 500 - size
            bot_pipe_surf = pygame.transform.scale(bot_pipe_surf, (100, bot_height))
            bot_pipe_rect = bot_pipe_surf.get_rect(midbottom=(550, 750))
            bg.fill(color_list[color_rotation])
            bird_surf.fill(color_list[bird_rotation])
            color_rotation += 1
            bird_rotation += 1
            if not speed_count % 3:
                pipe_speed += 1
            if pipe_speed >= 9:
                pipe_speed = 9
            print(pipe_speed, speed_count)
        screen.blit(bot_pipe_surf, bot_pipe_rect)

        # Collison
        if bird_rect.colliderect(bot_pipe_rect) or bird_rect.colliderect(top_pipe_rect):
            game_active = False
        if bird_rect.collidepoint(100, 750) or bird_rect.collidepoint(100, 0):
            game_active = False
        display_score()
        first_run = False
        if color_rotation >= len(color_list):
            color_rotation = 0
        if bird_rotation >= len(color_list):
            bird_rotation = 0

    else:

        new = update_high_score(speed_count)
        pipe_speed = 3
        screen.fill('sky blue')
        bird_gravity = 0

        # Reset variables
        bird_rect = bird_surf.get_rect(center=(100, 375))

        top_pipe_surf = pygame.Surface((100, 200))
        top_pipe_surf.fill('dark green')
        top_pipe_rect = top_pipe_surf.get_rect(midtop=(800, 0))

        bot_pipe_surf = pygame.Surface((100, 200))
        bot_pipe_surf.fill('dark green')
        bot_pipe_rect = bot_pipe_surf.get_rect(midbottom=(800, 750))

        title_surf = game_font.render(f'Flappy Square', False, 'black')
        title_rect = title_surf.get_rect(center=(250, 250))

        play_surf = game_font.render(f'Press space to play', False, 'black')
        play_rect = title_surf.get_rect(center=(210, 350))

        intro_rect = intro_surf.get_rect(center=(250, 200))

        screen.blit(title_surf, title_rect)
        screen.blit(play_surf, play_rect)
        if not first_run:
            display_score()
        display_high_score(new)
    pygame.display.update()
    clock.tick(60)
pygame.quit()
