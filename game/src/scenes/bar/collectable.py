import pygame
import random
import sys
import time
from src.scenes.bar.walls import create_labyrinth_walls

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bar Escape: Hometown Honkey Tonk")
# Create the walls
WALLS = create_labyrinth_walls()

class Collectable:
    def __init__(self, x, y, type_name, image_path=None, image_size=(50, 50)):
        self.rect = pygame.Rect(x, y, image_size[0], image_size[1])
        self.collected = False
        self.type = type_name
        # self.color = color
        self.image = None  # Placeholder for the collectable's image

        # Load the image if a path is provided
        if image_path:
            self.load_image(image_path, image_size)

    def load_image(self, image_path, image_size):
        """Load the collectable's image from the specified file path and scale it."""
        try:
            self.image = pygame.image.load(image_path).convert_alpha()  # Load image with transparency
            self.image = pygame.transform.scale(self.image, image_size)  # Scale the image
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))  # Update rect to match image size
        except pygame.error as e:
            print(f"Error loading image: {e}")
            sys.exit(1)  # Exit the program if the image fails to load

    def draw(self, screen):
        """Draw the collectable on the screen."""
        if not self.collected:
            if self.image:
                screen.blit(self.image, self.rect)  # Draw the image if loaded
            else:
                # Fallback: Draw a rectangle if no image is loaded
                pygame.draw.rect(screen, self.rect)