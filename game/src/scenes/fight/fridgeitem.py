import pygame
import os

class FridgeItem:
    def __init__(self, x, y, item_type, image_path):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 100
        self.item_type = item_type  # "tortellini" or "other"
        self.image = None

        # Load the image for the item
        self.image = self.load_image(image_path)

    def load_image(self, image_path):
        """Load an image from the given path."""
        try:
            # Load the image directly from the provided path
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (self.width, self.height))
            print(f"Successfully loaded image: {image_path}")
            return image
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")
            return None

    def draw(self, surface):
        """Draw the fridge item."""
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            # Fallback: Draw a rectangle if the image fails to load
            pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))