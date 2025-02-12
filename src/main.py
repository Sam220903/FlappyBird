import pygame
from pygame.locals import *
from game_objects.bird import Bird
from game_objects.pipe import Pipe
from game_objects.button import Button
from utils.image_text import draw_text
import random
from configparser import ConfigParser
from utils import camera_manager

config = ConfigParser()
config.read("config/settings.cfg")

pygame.init()

clock = pygame.time.Clock()
fps = int(config["Player"]["fps"])

WIDTH = int(config["Screen"]["width"])
HEIGHT = int(config["Screen"]["height"])
PIPE_GAP = int(config["Game"]["pipe_gap"])
PIPE_FRECUENCY = int(config["Game"]["pipe_frecuency"])

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Flappy Bird')

# Define font
font = pygame.font.SysFont('Bauhaus 93', 40)

# Define colors
white = (255, 255, 255)

# Define game variables
ground_scroll = 0
scroll_speed = 3
flying = False
game_over = False
last_pipe = pygame.time.get_ticks() - PIPE_FRECUENCY
score = 0
pass_pipe = False


# Initialize camera manager
camera = camera_manager.CameraManager()

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 70
    flappy.rect.y = int(HEIGHT/2)
    score = 0
    return score

# Load images
bg = pygame.image.load('assets/images/campus_upaep.png')
ground_img = pygame.image.load('assets/images/ground1.png')
button_img = pygame.image.load('assets/images/restart.png')

# Reduce images size to fit the screen
bg = pygame.transform.scale(bg, (WIDTH, 384))
ground_img = pygame.transform.scale(ground_img, (WIDTH + 35, 84))
button_img = pygame.transform.scale(button_img, (100,30))

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(70, int(HEIGHT/2), camera)

bird_group.add(flappy)

# Create restart button instance
button = Button(WIDTH // 2 - 50, HEIGHT // 2 - 50, button_img)

run = True 

while run:

    clock.tick(fps)

    # Draw background
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update(flying, game_over)

    pipe_group.draw(screen)

    # Draw the ground
    screen.blit(ground_img, (ground_scroll, 384)) 

    # Check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and not pass_pipe:
            pass_pipe = True

        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(WIDTH/2), 20, screen)

    # Look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # Check if bird has hit the ground
    if flappy.rect.bottom >= 384:
        game_over = True
        flying = False

    if not game_over and flying:
        # Generate new pipes
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > PIPE_FRECUENCY:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(WIDTH, int(HEIGHT/2) + pipe_height, PIPE_GAP)
            top_pipe = Pipe(WIDTH, int(HEIGHT/2) + pipe_height, PIPE_GAP, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = current_time

        # Scroll ground
        ground_scroll -= scroll_speed

        if abs(ground_scroll) > 35 :
            ground_scroll = 0

        pipe_group.update(scroll_speed)

    # Check for game over and reset
    if game_over:
        if button.draw(screen):
            game_over = False
            score = reset_game()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if camera.pulse_detected and not flying and not game_over:
        flying = True

    pygame.display.update()


pygame.quit()