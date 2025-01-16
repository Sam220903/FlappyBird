from pygame.sprite import Sprite
from pygame import image, transform

class Pipe(Sprite):
    def __init__(self, x : int ,y : int, pipe_gap : int, position=-1):
        Sprite.__init__(self)
        self.image = image.load('assets/images/pipe.png')
        self.image = transform.scale(self.image, (40, 300))
        self.rect = self.image.get_rect()

        # Position 1 is from the top, -1 is from the bottom
        match position:
            case 1:
                self.image = transform.flip(self.image, False, True)
                self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
            case -1:
                self.rect.topleft = [x,y + int(pipe_gap / 2)]

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed

        # Delete the pipe when it disappears from the screen
        if self.rect.right < 0:
            self.kill()


        