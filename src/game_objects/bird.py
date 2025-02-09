from pygame.sprite import Sprite
from pygame import image, transform
from utils import camera_manager as cm

class Bird(Sprite):

    def __init__(self, x: int, y: int, camera_manager: cm.CameraManager):
        super().__init__()
        self.images = []
        self.index = 0
        self.counter = 0
        self.initial_x = x
        self.initial_y = y  
        self.camera = camera_manager
        
        for num in range(1, 4):
            img = image.load(f'assets/images/bird{num}.png')
            img = transform.scale(img, (32, 25))
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.pressed = False

    def update(self, flying: bool, game_over: bool):
        if flying:
            self.vel += 0.4  # Simulación de gravedad
            self.vel = min(self.vel, 10)  # Límite de velocidad

            if self.rect.bottom <= 384:
                self.rect.y += int(self.vel)

        if not game_over:
            # Usar el detector de pulsos en un hilo separado
            if self.camera.pulse_detected and not self.pressed:
                self.vel = -7
                self.pressed = True

            if not self.camera.pulse_detected:
                self.pressed = False

            # Manejo de animación
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)

            self.image = self.images[self.index]

            # Rotar el pájaro
            self.image = transform.rotate(self.images[self.index], self.vel * -2)

        else:
            self.image = transform.rotate(self.images[self.index], -90)

        if not game_over and not flying:
            self.image = transform.rotate(self.images[self.index], 0)
            self.rect.center = [self.initial_x, self.initial_y]
