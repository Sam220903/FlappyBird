from pygame.sprite import Sprite
from pygame import image, transform, key, K_SPACE

class Bird(Sprite):

    def __init__(self, x : int, y : int):
        Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.initial_x = x
        self.intial_y = y
        for num in range(1,4):
            img = image.load(f'assets/images/bird{num}.png')
            img = transform.scale(img, (32, 25))
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.pressed = False

    def update(self, flying : bool, game_over : bool):

        if flying:
            # Gravity (just to explain what's going on)
            self.vel += 0.4

            if self.vel > 10: 
                self.vel = 10
            
            if self.rect.bottom <= 384:
                self.rect.y += int(self.vel)

        if not game_over:
            # Jump
            keys = key.get_pressed()
            if keys[K_SPACE] and self.pressed == False:
                self.pressed = True
                self.vel = -7
            
            if not keys[K_SPACE]:
                self.pressed = False

            # Handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1

                if self.index >= len(self.images): 
                    self.index = 0

            self.image = self.images[self.index]

            # Rotate the bird
            self.image = transform.rotate(self.images[self.index], self.vel * -2)

        else:
            self.image = transform.rotate(self.images[self.index], -90)

        if not game_over and not flying:
            self.image = transform.rotate(self.images[self.index], 0)
            self.rect.center = [self.initial_x, self.intial_y]






