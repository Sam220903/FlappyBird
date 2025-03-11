from pygame import Surface
from pygame.font import SysFont

def draw_text(text : str, font : SysFont, color : tuple, outline_color : tuple , x :int, y : int, screen : Surface):
    """Dibuja texto con contorno en Pygame usando pygame.freetype"""
    border_size = 2  # Grosor del contorno

    # Dibuja el contorno en 4 direcciones
    font.render_to(screen, (x - border_size, y), text, outline_color)
    font.render_to(screen, (x + border_size, y), text, outline_color)
    font.render_to(screen, (x, y - border_size), text, outline_color)
    font.render_to(screen, (x, y + border_size), text, outline_color)

    # Dibuja el texto principal encima
    font.render_to(screen, (x, y), text, color)

