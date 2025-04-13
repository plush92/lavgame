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

class BarPatron:
    def __init__(self, x, y, color, image_path=None, image_size=(20, 30)):
        self.rect = pygame.Rect(x, y, image_size[0], image_size[1])
        self.color = color
        self.image = None  # Placeholder for the patron's image
        self.image_size = image_size  # Default size for scaling
        self.moving = random.choice([True, False])
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move_timer = 0
        self.move_interval = random.randint(30, 120)  # Frames between direction changes

        # Load the image if a path is provided
        if image_path:
            self.load_image(image_path, image_size)

    def load_image(self, image_path, image_size):
        """Load the patron's image from the specified file path and scale it."""
        try:
            self.image = pygame.image.load(image_path).convert_alpha()  # Load image with transparency
            self.image = pygame.transform.scale(self.image, image_size)  # Scale the image
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))  # Update rect to match image size
        except pygame.error as e:
            print(f"Error loading image: {e}")
            sys.exit(1)  # Exit the program if the image fails to load

    def update(self, bar_area):
        if not self.moving:
            self.move_timer += 1
            if self.move_timer >= self.move_interval:
                self.moving = True
                self.move_timer = 0
                self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            return
        
        # Move in current direction
        speed = random.uniform(0.5, 1.5)
        dx, dy = self.direction[0] * speed, self.direction[1] * speed
        
        # Check if next position is within bar area
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        
        if (bar_area.left < new_x < bar_area.right - self.rect.width and 
            bar_area.top < new_y < bar_area.bottom - self.rect.height):
            self.rect.x = new_x
            self.rect.y = new_y
        else:
            # Change direction if hitting boundary
            self.direction = (-self.direction[0], -self.direction[1])
        
        # Occasionally stop or change direction
        if random.random() < 0.01:  # 1% chance per frame
            self.moving = False
            self.move_timer = 0
            self.move_interval = random.randint(30, 120)
    
    def draw(self, screen):
        """Draw the patron on the screen."""
        if self.image:
            screen.blit(self.image, self.rect)  # Draw the image if loaded
        else:
            # Fallback: Draw a rectangle and a circle if no image is loaded
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.top - 5), 10)