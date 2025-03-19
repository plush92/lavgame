import pygame
import random
import sys
import time
from src.scenes.bar.walls import create_labyrinth_walls

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bar Scene")
# Create the walls
WALLS = create_labyrinth_walls()

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 4
        self.drunk_level = 0
        self.max_drunk_level = 3
        self.recovering = False
        self.recovery_timer = 3
        self.name = "Tim"

    def move(self):
        if self.recovering:
            if time.time() - self.recovery_timer >= 0.3:
                self.recovering = False
            else:
                return
            
        keys = pygame.key.get_pressed()
        # Base movement
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT]:
            dx -= self.speed
            print("Left arrow pressed")
        if keys[pygame.K_RIGHT]:
            dx += self.speed
            print("Right arrow pressed")
        if keys[pygame.K_UP]:
            dy -= self.speed
            print("Up arrow pressed")
        if keys[pygame.K_DOWN]:
            dy += self.speed
            print("Down arrow pressed")

        # Add drunk wobble
        if self.drunk_level > 0:
            dx += random.uniform(-self.drunk_level, self.drunk_level)
            dy += random.uniform(-self.drunk_level, self.drunk_level)

        # Try to move horizontally first
        if dx != 0:
            proposed_rect = self.rect.copy()
            proposed_rect.x += dx
            
            collision = False
            for wall in WALLS:
                if proposed_rect.colliderect(wall):
                    collision = True
                    break
                    
            if not collision:
                self.rect.x += dx
            else:
                self.recovering = True
                self.recovery_timer = time.time()
                
        # Then try to move vertically
        if dy != 0:
            proposed_rect = self.rect.copy()
            proposed_rect.y += dy
            
            collision = False
            for wall in WALLS:
                if proposed_rect.colliderect(wall):
                    print("Collision detected with:", wall)
                    collision = True
                    break
                    
            if not collision:
                self.rect.y += dy
            else:
                self.recovering = True
                self.recovery_timer = time.time()
                
        # Keep player in screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))