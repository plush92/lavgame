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
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 20, 30)
        self.color = color
        self.moving = random.choice([True, False])
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move_timer = 0
        self.move_interval = random.randint(30, 120)  # Frames between direction changes
    
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
        # Draw body
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw head
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.top - 5), 10)