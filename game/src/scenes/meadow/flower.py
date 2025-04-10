import pygame
import math

class Flower(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images  # List of 4 flower images
        self.state = 0  # Start with the wilted state (0)
        self.image = self.images[self.state]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bloomed = False  # Whether the flower is fully bloomed

    def update(self, character):
        """Update the flower's state based on proximity to the character."""
        if not self.bloomed:  # Only update if not fully bloomed
            distance = math.sqrt((self.rect.centerx - character.rect.centerx) ** 2 +
                                 (self.rect.centery - character.rect.centery) ** 2)
            if distance < 100:  # Close proximity
                self.state = min(3, self.state + 1)  # Advance bloom state
                self.image = self.images[self.state]
                if self.state == 3:  # Fully bloomed
                    self.bloomed = True