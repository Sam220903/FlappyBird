from pygame import Surface
from pygame.font import SysFont


def draw_text(text : str, font : SysFont, color : tuple, x : int, y : int, screen : Surface):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))