# Rect parameters:
    # x (int) – The x-coordinate of the top-left corner.
    # y (int) – The y-coordinate of the top-left corner.
    # width (int) – The width of the rectangle.
    # height (int) – The height of the rectangle.
    #ex. - (100, 60, 15, 100) - x=100, y=60, width=15, height=100
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Define a more complex labyrinth but with more openings
def create_labyrinth_walls():
    walls = []

    # Inner border
    border_offset = 40
    walls.extend([
        pygame.Rect(border_offset, border_offset, SCREEN_WIDTH - 2 * border_offset, 10),
        pygame.Rect(border_offset, border_offset, 10, SCREEN_HEIGHT - 2 * border_offset),
        pygame.Rect(border_offset, SCREEN_HEIGHT - border_offset - 10, SCREEN_WIDTH - 2 * border_offset, 10),
        pygame.Rect(SCREEN_WIDTH - border_offset - 10, border_offset, 10, SCREEN_HEIGHT - 2 * border_offset),
    ])

    # "Pac-Dots" rectangular areas (smaller boxes)
    box_positions = [
        (80, 80), (250, 80), (450, 80), (620, 80),
        (80, 270), (620, 270),
        (80, 460), (250, 460), (450, 460), (620, 460)
    ]
    walls.extend([pygame.Rect(x, y, 80, 40) for x, y in box_positions])  # Reduced width and height

    # T-Shaped structures (shorter T-shapes)
    t_shape_positions = [
        (390, 140, 20, 80), (280, 180, 200, 20),  # Reduced height and width
        (390, 360, 20, 80), (280, 400, 200, 20)   # Reduced height and width
    ]
    walls.extend([pygame.Rect(*pos) for pos in t_shape_positions])

    # **Center Bar (Redesigned)**
    center_x = SCREEN_WIDTH // 2 - 70
    center_y = SCREEN_HEIGHT // 2 - 30
    center_bar = [
        pygame.Rect(center_x, center_y, 140, 10),  # Top
        pygame.Rect(center_x, center_y, 10, 50),   # Left (shortened height)
        pygame.Rect(center_x + 130, center_y, 10, 50),   # Right (shortened height)
        pygame.Rect(center_x, center_y + 40, 140, 10),  # Bottom (adjusted position)
    ]
    walls.extend(center_bar)

    # Vertical corridor walls (unchanged for now)
    corridor_positions = [
        (180, 172, 20, 70), (600, 172, 20, 70),
        (180, 360, 20, 70), (600, 360, 20, 70)
    ]
    walls.extend([pygame.Rect(*pos) for pos in corridor_positions])

    return walls