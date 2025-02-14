import pygame
from pygame.locals import *
from game_objects.bird import Bird
from game_objects.pipe import Pipe
from game_objects.button import Button
from utils.image_text import draw_text
import random
from configparser import ConfigParser
from utils import camera_manager

class Game:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config/settings.cfg")

        pygame.init()
        self.clock = pygame.time.Clock()

        self.fps = int(self.config["Player"]["fps"])
        self.WIDTH = int(self.config["Screen"]["width"])
        self.HEIGHT = int(self.config["Screen"]["height"])
        self.PIPE_GAP = int(self.config["LVL3"]["pipe_gap"])
        self.PIPE_FRECUENCY = int(self.config["LVL3"]["pipe_frecuency"])
        self.SCROLL_SPEED = int(self.config["LVL3"]["scroll_speed"])

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Slappy Bird')

        # Define font
        self.font = pygame.font.SysFont(str(self.config["Game"]["font"]), int(self.config["Game"]["font_size"]))

        # Define colors
        self.font_color = (255,255,255)
        # self.font_color = tuple(map(int, self.config["Game"]["font_color"].split(',')))

        # Define game variables
        self.ground_scroll = 0
        self.flying = False
        self.game_over = False
        self.last_pipe = pygame.time.get_ticks() - self.PIPE_FRECUENCY
        self.score = 0
        self.pass_pipe = False

        # Initialize camera manager
        self.camera = camera_manager.CameraManager()

        # Load images
        self.bg = pygame.image.load(self.config["Game"]["bg"])
        self.ground_img = pygame.image.load(self.config["Game"]["ground"])
        self.button_img = pygame.image.load(self.config["Game"]["button"])

        # Reduce images size to fit the screen
        self.bg = pygame.transform.scale(self.bg, (self.WIDTH, 384))
        self.ground_img = pygame.transform.scale(self.ground_img, (self.WIDTH + 35, 84))
        self.button_img = pygame.transform.scale(self.button_img, (100,30))

        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()

        self.flappy = Bird(70, int(self.HEIGHT/2), self.camera)
        self.bird_group.add(self.flappy)

        # Create restart button instance
        self.button = Button(self.WIDTH // 2 - 50, self.HEIGHT // 2 - 50, self.button_img)

    def run(self):
        run = True
        while run:
            self.clock.tick(self.fps)

            # Draw background
            self.screen.blit(self.bg, (0,0))

            self.bird_group.draw(self.screen)
            self.bird_group.update(self.flying, self.game_over)

            self.pipe_group.draw(self.screen)

            # Draw the ground
            self.screen.blit(self.ground_img, (self.ground_scroll, 384)) 

            # Check the score
            if len(self.pipe_group) > 0:
                if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.left\
                    and self.bird_group.sprites()[0].rect.right < self.pipe_group.sprites()[0].rect.right\
                    and not self.pass_pipe:
                    self.pass_pipe = True

                if self.pass_pipe:
                    if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.right:
                        self.score += 1
                        self.pass_pipe = False

            draw_text(str(self.score), self.font, self.font_color, int(self.WIDTH/2), 20, self.screen)

            # Look for collision
            if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.flappy.rect.top < 0:
                self.game_over = True

            # Check if bird has hit the ground
            if self.flappy.rect.bottom >= 384:

                self.game_over = True
                self.flying = False

            if not self.game_over and self.flying:
                # Generate new pipes
                current_time = pygame.time.get_ticks()
                if current_time - self.last_pipe > self.PIPE_FRECUENCY:
                    pipe_height = random.randint(-100,100)
                    btm_pipe = Pipe(self.WIDTH, int(self.HEIGHT/2) + pipe_height, self.PIPE_GAP)
                    top_pipe = Pipe(self.WIDTH, int(self.HEIGHT/2) + pipe_height, self.PIPE_GAP, 1)
                    self.pipe_group.add(btm_pipe)
                    self.pipe_group.add(top_pipe)
                    self.last_pipe = current_time

                # Scroll ground
                self.ground_scroll -= self.SCROLL_SPEED

                if abs(self.ground_scroll) > 35 :
                    self.ground_scroll = 0

                self.pipe_group.update(self.SCROLL_SPEED)

            # Check for game over and reset
            if self.game_over:
                if self.button.draw(self.screen):
                    self.game_over = False
                    self.score = self.reset_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if self.camera.pulse_detected and not self.flying and not self.game_over:
                self.flying = True

            pygame.display.update()

        pygame.quit()


    def reset_game(self):
        self.pipe_group.empty()
        self.flappy.rect.x = 70
        self.flappy.rect.y = int(self.HEIGHT/2)
        self.score = 0
        return self.score

