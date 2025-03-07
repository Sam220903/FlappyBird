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
        self.config.read("src/config/settings.cfg")

        pygame.init()
        self.clock = pygame.time.Clock()

        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.music.load("assets/sounds/main_song.wav")
        pygame.mixer.music.set_volume(1)

        self.fall_sound = pygame.mixer.Sound("assets/sounds/fall.wav")
        self.fall_sound.set_volume(1)

        self.played_fall_sound = False

        self.select_sound = pygame.mixer.Sound("assets/sounds/select.wav")
        self.select_sound.set_volume(1)

        self.increase_score_sound = pygame.mixer.Sound("assets/sounds/point.wav")
        self.increase_score_sound.set_volume(1)

        self.flap_sound = pygame.mixer.Sound("assets/sounds/flap.wav")
        self.flap_sound.set_volume(1)

        self.fps = 60
        self.WIDTH = int(572 * 1.25)
        self.HEIGHT = int(468 * 1.25)

        # Establecer icono de la ventana
        icon = pygame.image.load("assets/images/golden_eagle4.png")  
        pygame.display.set_icon(icon)

        self.easy = {"scroll_speed": 2,
                     "pipe_frequency": 2200,
                     "pipe_gap": int(270 * 1.25),
                     "gravity": 0.4}
        
        self.medium = {"scroll_speed": 3,
                       "pipe_frequency": 1500,
                       "pipe_gap": int(200 * 1.25),
                       "gravity": 0.4}

        self.hard = {"scroll_speed": 4,
                     "pipe_frequency": 800,
                     "pipe_gap": int(130 * 1.25),
                     "gravity": 0.5}

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Slappy Bird')

        self.font = pygame.freetype.SysFont("Bauhaus 93", int(40 * 1.25))
        self.font_color = (255, 255, 255)

        self.ground_level = self.HEIGHT - 84

        self.ground_scroll = 0
        self.flying = False
        self.game_over = False
        self.score = 0
        self.pass_pipe = False

        self.camera = camera_manager.CameraManager()

        self.bg = pygame.image.load("assets/images/campus_upaep.png")
        self.ground_img = pygame.image.load("assets/images/ground1.png")
        self.logo = pygame.image.load("assets/images/slappy_logo.png")
        self.start_btn = pygame.image.load("assets/images/start.png")
        self.restart_btn = pygame.image.load("assets/images/restart.png")

        self.hand0 = pygame.image.load("assets/images/hand0.png")
        self.hand1 = pygame.image.load("assets/images/hand1.png")
        self.hand2 = pygame.image.load("assets/images/hand2.png")
        self.hand3 = pygame.image.load("assets/images/hand3.png")
        self.hand4 = pygame.image.load("assets/images/hand4.png")
        self.hand5 = pygame.image.load("assets/images/hand5.png")

        self.bg = pygame.transform.scale(self.bg, (self.WIDTH, self.ground_level))
        self.ground_img = pygame.transform.scale(self.ground_img, (self.WIDTH + int(35 * 1.25), int(self.HEIGHT-84)))
        self.logo = pygame.transform.scale(self.logo, (3 * self.WIDTH // 4, self.HEIGHT // 4))
        self.start_btn = pygame.transform.scale(self.start_btn, (int(100 * 1.25), int(35 * 1.25)))
        self.restart_btn = pygame.transform.scale(self.restart_btn, (int(100 * 1.25), int(30 * 1.25)))

        self.hand0 = pygame.transform.scale(self.hand0, (int(100 * 1.25), int(100 * 1.25)))
        self.hand1 = pygame.transform.scale(self.hand1, (int(100 * 1.25), int(100 * 1.25)))
        self.hand2 = pygame.transform.scale(self.hand2, (int(100 * 1.25), int(100 * 1.25)))
        self.hand3 = pygame.transform.scale(self.hand3, (int(100 * 1.25), int(100 * 1.25)))
        self.hand4 = pygame.transform.scale(self.hand4, (int(100 * 1.25), int(100 * 1.25)))
        self.hand5 = pygame.transform.scale(self.hand5, (int(100 * 1.25), int(100 * 1.25)))

        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()

        self.start = Button(self.WIDTH // 2 - int(50 * 1.25), self.HEIGHT // 2 - int(25 * 1.25), self.start_btn)
        self.restart = Button(self.WIDTH // 2 - int(50 * 1.25), self.HEIGHT // 2 - int(50 * 1.25), self.restart_btn)

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
            self.screen.blit(self.ground_img, (self.ground_scroll, self.ground_level))

            # Check the score
            if len(self.pipe_group) > 0:
                if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.left\
                    and self.bird_group.sprites()[0].rect.right < self.pipe_group.sprites()[0].rect.right\
                    and not self.pass_pipe:
                    self.pass_pipe = True

                if self.pass_pipe:
                    if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.right:
                        self.score += 1
                        self.increase_score_sound.play()
                        self.pass_pipe = False

            draw_text(str(self.score), self.font, self.font_color, (0,0,0), int(self.WIDTH/2), 20, self.screen)

            # Look for collision
            if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.flappy.rect.top < 0:
                self.game_over = True

            # Check if bird has hit the ground
            if self.flappy.rect.bottom >= self.ground_level:
                self.game_over = True
                self.flying = False

            if not self.game_over and self.flying:
                # Generate new pipes
                current_time = pygame.time.get_ticks()
                if current_time - self.last_pipe > self.PIPE_FREQUENCY:
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
                if not self.played_fall_sound:
                    self.fall_sound.play()
                    self.played_fall_sound = True

                pygame.mixer.music.stop()  # Solo detiene la música actual  

                if self.restart.draw(self.screen):
                    self.game_over = False
                    self.select_sound.play()
                    self.score = self.reset_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()

            if self.camera.pulse_detected:
                self.flap_sound.play()

            if self.camera.pulse_detected and not self.flying and not self.game_over:
                self.flying = True

            pygame.display.update()

        pygame.quit()


    def reset_game(self):
        pygame.mixer.music.play(-1)  # Reanuda la música en bucle
        self.played_fall_sound = False
        self.pipe_group.empty()
        self.flappy.rect.x = int(70 * 1.25)
        self.flappy.rect.y = self.HEIGHT // 2
        self.score = 0
        self.choose_difficulty()
        return self.score
    
    def start_game(self):
        starting = True
        pygame.mixer.music.play(-1)
        while starting:
            # Draw background
            self.screen.blit(self.bg, (0, 0))
            
            # Draw the ground
            self.screen.blit(self.ground_img, (self.ground_scroll, self.ground_level))

            # Draw the logo
            self.screen.blit(self.logo, (self.WIDTH // 8, self.HEIGHT // 8))

            # Draw the start button and check if clicked
            if self.start.draw(self.screen):  
                starting = False  # Salir del loop para iniciar el juego
                self.select_sound.play()
                self.choose_difficulty()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def set_difficulty(self, difficulty):
        self.SCROLL_SPEED = difficulty["scroll_speed"]
        self.PIPE_FREQUENCY = difficulty["pipe_frequency"]
        self.PIPE_GAP = difficulty["pipe_gap"]
        self.last_pipe = pygame.time.get_ticks() - self.PIPE_FREQUENCY
        self.flappy = Bird(int(70 * 1.25), self.HEIGHT // 2, self.camera, difficulty["gravity"], self.ground_level)
        self.bird_group.empty()
        self.bird_group.add(self.flappy)
        self.select_sound.play()


    def choose_difficulty(self):
        choosing = True

        while choosing:
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.ground_img, (self.ground_scroll, self.ground_level))

            draw_text("Elige la dificultad", self.font, self.font_color, (0, 0, 0), self.WIDTH // 2 - 180, self.HEIGHT // 2 - 220, self.screen)

            # Dibujar manos
            self.screen.blit(self.hand1, (self.WIDTH // 2 - 170, self.HEIGHT // 2 - 150))
            self.screen.blit(self.hand2, (self.WIDTH // 2 - 170, self.HEIGHT // 2 - 50))  
            self.screen.blit(self.hand3, (self.WIDTH // 2 - 170, self.HEIGHT // 2 + 50))

            # Dibujar botones con etiquetas
            draw_text("Fácil", self.font, self.font_color, (0, 0, 0), self.WIDTH // 2 - 20, self.HEIGHT // 2 - 120, self.screen)
            draw_text("Medio", self.font, self.font_color, (0, 0, 0), self.WIDTH // 2 - 20, self.HEIGHT // 2 - 20, self.screen)
            draw_text("Difícil", self.font, self.font_color, (0, 0, 0), self.WIDTH // 2 - 20, self.HEIGHT // 2 + 80, self.screen)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            difficulty = self.camera.difficulty()

            if difficulty == [0, 1, 0, 0, 0]:  # Fácil
                self.set_difficulty(self.easy)
                choosing = False
            elif difficulty == [0, 1, 1, 0, 0]:  # Medio
                self.set_difficulty(self.medium)
                choosing = False
            elif difficulty == [0, 1, 1, 1, 0]:  # Difícil
                self.set_difficulty(self.hard)
                choosing = False

        self.run()  # Corre el juego después de elegir la dificultad
