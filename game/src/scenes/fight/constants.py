import os

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
LIGHT_GRAY = (220, 220, 220)
YELLOW = (255, 255, 0)

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Movement boundaries
PLAY_AREA_TOP = 50
PLAY_AREA_BOTTOM = HEIGHT - 50
PLAY_AREA_LEFT = 50
PLAY_AREA_RIGHT = WIDTH - 50

FRIDGE_BACKGROUND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets", "fridge_background.png"))
