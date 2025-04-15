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

class Wall:
    def __init__(self, screen_width, screen_height):
        self.hit_count = 0  
        self.max_hits = 3  # Increase this to allow more hits
        self.is_destroyed = False  

        # Make sure you have all these images in your assets folder
        self.images = [
            pygame.image.load("src/assets/wall_normal.png"),
            pygame.image.load("src/assets/wall_cracked.png"),
            pygame.image.load("src/assets/wall_heavily_cracked.png")  # Add this 3rd image
        ]
        
        self.current_image = self.images[0]  
        
        self.width, self.height = self.current_image.get_size()
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        
        # Add a rect attribute for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.fade_alpha = 255
        self.fade_speed = 2  # Slow down fade for better effect  

    def hit(self):
        """Handles wall hit logic and destruction."""
        if self.is_destroyed:
            return False  # No more hits after destruction
        
        self.hit_count += 1
        print(f"Wall hit! Count: {self.hit_count}")  # Debug print
        
        if self.hit_count >= self.max_hits:
            print("Wall destroyed!")  # Debug print
            self.is_destroyed = True
            return True
        else:
            # Make sure we don't go out of bounds with image index
            image_index = min(self.hit_count, len(self.images) - 1)
            print(f"Changing to image {image_index}")  # Debug print
            self.current_image = self.images[image_index]
            return False

    def update(self, dt):
        """Handle fade-out effect when destroyed."""
        if self.is_destroyed and self.fade_alpha > 0:
            self.fade_alpha -= self.fade_speed
            if self.fade_alpha < 0:
                self.fade_alpha = 0
            
    def draw(self, screen, offset_x=0, offset_y=0):
        """Draw wall (fading out if destroyed) with applied offsets."""
        draw_x = self.x + offset_x
        draw_y = self.y + offset_y

        if self.is_destroyed:
            # Create a copy with adjusted alpha
            temp_image = self.current_image.copy()
            temp_image.set_alpha(self.fade_alpha)
            screen.blit(temp_image, (draw_x, draw_y))
        else:
            screen.blit(self.current_image, (draw_x, draw_y))