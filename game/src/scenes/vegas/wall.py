import pygame
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tim and Lav in Vegas")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (150, 150, 150)
BROWN = (165, 42, 42)

# Game states
STATE_DIALOGUE = 0
STATE_WALL_GAME = 1
STATE_ENDING = 2
game_state = STATE_DIALOGUE

import pygame

class Wall:
    def __init__(self, screen_width, screen_height):
        self.hit_count = 0  
        self.max_hits = 3  
        self.is_destroyed = False  

        self.images = [
            pygame.image.load("assets/wall_normal.png"),
            pygame.image.load("assets/wall_cracked.png"),
            # pygame.image.load("assets/wall_heavily_cracked.png")
        ]
        
        self.current_image = self.images[0]  
        
        self.width, self.height = self.current_image.get_size()
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.fade_alpha = 255  

    def hit(self):
        """Handles wall hit logic and destruction."""
        if self.is_destroyed:
            return False  # No more hits after destruction
        
        self.hit_count += 1
        if self.hit_count >= self.max_hits:
            self.is_destroyed = True
            self.fade_alpha = 255
            return True  # Return True only when wall is completely destroyed
        else:
            # Use min to avoid index errors if hit_count exceeds image count
            self.current_image = self.images[min(self.hit_count, len(self.images) - 1)]
            return False  # Not completely destroyed yet

    def update(self, dt):
        """Handle fade-out effect when destroyed."""
        if self.is_destroyed and self.fade_alpha > 0:
            self.fade_alpha -= 5  
            
    def draw(self, screen, offset_x=0, offset_y=0):
        """Draw wall (fading out if destroyed) with applied offsets."""
        draw_x = self.x + offset_x
        draw_y = self.y + offset_y

        if self.is_destroyed:
            faded_image = self.current_image.copy()
            faded_image.fill((255, 255, 255, self.fade_alpha), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(faded_image, (draw_x, draw_y))
        else:
            screen.blit(self.current_image, (draw_x, draw_y))


