import pygame
import random
import math
import sys

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

# Game states
KITCHEN = 0
FRIDGE_MINIGAME = 1
DIALOG = 2
FIGHTING = 3
GAME_OVER = 4

class Kitchen:
    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        self.image = None
        self.image_path = image_path
        self.load_image()

    def load_image(self):
        try:
            self.image_path = "assets/kitchen.png"
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            print(f"Successfully loaded kitchen background: {self.image_path}")
        except pygame.error as e:
            print(f"Error loading kitchen background image {self.image_path}: {e}")
            self.image = None

    def draw(self, surface):
        if self.image:
            # print("Drawing kitchen background...")  # Debugging
            surface.blit(self.image, (0, 0))
        else:
            print("Falling back to solid color for kitchen background.")
            pygame.draw.rect(surface, LIGHT_GRAY, (0, 0, self.width, self.height))
    
    def draw_debug(self, surface, grid_size=50, color=(255, 0, 0)):
        """
        Draws debugging information on the kitchen, such as a grid.

        Args:
            surface (pygame.Surface): The surface to draw on.
            grid_size (int): The size of each grid square (default is 50).
            color (tuple): The color of the grid lines (default is red).
        """
        # Draw vertical grid lines
        for x in range(0, self.width, grid_size):
            pygame.draw.line(surface, color, (x, 0), (x, self.height), 1)

        # Draw horizontal grid lines
        for y in range(0, self.height, grid_size):
            pygame.draw.line(surface, color, (0, y), (self.width, y), 1)

        # Optionally, draw a border around the kitchen
        pygame.draw.rect(surface, color, (0, 0, self.width, self.height), 2)