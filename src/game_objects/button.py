from pygame import mouse, Surface

class Button():
    def __init__(self, x : int, y : int, image : Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        action = False

        # Get mouse position
        pos = mouse.get_pos()

        # Check if mouse is over the button
        if self.rect.collidepoint(pos):
            if mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

    