import pygame
import sys
import random
import time
from pygame.math import Vector2
from src.scenes.vegas.brick import Brick

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
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
BRICK_COLOR = (165, 42, 42)
GRAY = (150, 150, 150)

# Fonts
font_small = pygame.font.SysFont('Arial', 20)
font_medium = pygame.font.SysFont('Arial', 28)
font_large = pygame.font.SysFont('Arial', 36)

# Game states
STATE_DIALOGUE = 0
STATE_WALL_GAME = 1
STATE_ENDING = 2
game_state = STATE_DIALOGUE

class Wall:
    def __init__(self):
        self.bricks = [] # List of bricks in the wall
        brick_width = 60 # Width of each brick
        brick_height = 30 # Height of each brick
        wall_x = WIDTH // 2 - (brick_width * 3) // 2 # X position of the wall (centered) 
        
        # Create brick pattern - 3 columns x 5 rows
        for row in range(5): # Loop through 5 rows
            for col in range(3): # Loop through 3 columns
                x = wall_x + col * brick_width # X position of the brick (centered)
                y = 150 + row * brick_height # Y position of the brick (150 is the top margin)
                # Assign a region: 0=left, 1=middle, 2=right based on column index
                region = col # Region based on column index
                self.bricks.append({ # Add brick to the list of bricks
                    "rect": pygame.Rect(x, y, brick_width, brick_height), # Create a rectangle for the brick (x, y, width, height)
                    "region": region, # Assign a region to the brick (0, 1, or 2)
                    "cracked": False, # Set the brick as not cracked initially
                    "broken": False # Set the brick as not broken initially
                })
                
        # Track hits per region
        self.hits_per_region = [0, 0, 0]  # [left, middle, right] regions
        self.required_hits_per_region = [1, 1, 1]  # 2 hits per region required
        
        # Wall breaking animation
        self.breaking = False # Set the wall as not breaking initially, will be set to True when breaking
        self.break_timer = 0 # Timer for the breaking animation, starts at 0, increases over
        self.break_duration = 1000  # Duration of the breaking animation in milliseconds, 1000ms = 1s
        self.shake_amount = 0 # Amount of shake effect during breaking, starts at 0 and increases
        
    def draw(self):
        # Apply shake effect during breaking
        shake_offset = Vector2(0, 0) # Initialize shake offset as (0, 0)
        if self.breaking: # If the wall is breaking
            shake_offset = Vector2( # Randomly offset the shake effect
                random.uniform(-self.shake_amount, self.shake_amount), # Random offset in x direction
                random.uniform(-self.shake_amount, self.shake_amount) # Random offset in y direction
            )
            
        for brick in self.bricks: # Loop through each brick
            if not brick["broken"]: # If the brick is not broken
                # Position with shake
                x = brick["rect"].x + shake_offset.x # Apply shake offset to x position
                y = brick["rect"].y + shake_offset.y # Apply shake offset to y position
                rect = pygame.Rect(x, y, brick["rect"].width, brick["rect"].height) # Create a rectangle with shake offset
                
                # Draw brick
                if brick["cracked"]: # If the brick is cracked
                    pygame.draw.rect(screen, (120, 30, 30), rect) # Draw a cracked brick
                    # Draw crack lines on the brick (top left to bottom right, top right to bottom left)
                    pygame.draw.line(screen, BLACK,  # Main crack
                                    (rect.x + 5, rect.y + 5), # Top left corner of the crack line
                                    (rect.x + rect.width - 5, rect.y + rect.height - 5), 2) # Bottom right corner of the crack line 
                    pygame.draw.line(screen, BLACK,  # Secondary crack 
                                    (rect.x + rect.width - 5, rect.y + 5), # Top right corner of the crack line 
                                    (rect.x + 5, rect.y + rect.height - 5), 2) # Bottom left corner of the crack line 
                else: # If the brick is not cracked 
                    pygame.draw.rect(screen, BRICK_COLOR, rect) # Draw a normal brick 
                pygame.draw.rect(screen, BLACK, rect, 2) # Draw an outline around the brick 
                
    def hit(self, x, y): # Function to hit a brick at a given position (x, y) on the screen 
        if self.breaking: # If the wall is breaking, return False (no hits allowed during breaking) 
            return False 
            
        for brick in self.bricks: # Loop through each brick 
            if not brick["broken"] and not brick["cracked"] and brick["rect"].collidepoint(x, y): # If the brick is not broken, not cracked, and the hit position is on the brick 
                region = brick["region"] # Get the region of the brick
                if self.hits_per_region[region] < self.required_hits_per_region[region]: # If the region has not reached the required hits 
                    # Crack the brick and update hits per region
                    brick["cracked"] = True # Crack the brick 
                    self.hits_per_region[region] += 1 # Increment hits for the region 
                    
                    # Check if all regions have required hits to break the wall
                    if all(self.hits_per_region[i] >= self.required_hits_per_region[i] for i in range(3)): # If all regions have required hits
                        # Start wall breaking animation
                        self.breaking = True # Set the wall as breaking 
                        self.break_timer = 0 # Reset the break timer
                        self.shake_amount = 5 # Set the initial shake amount
                        return True # Return True to indicate successful hit
                    return True # Return True to indicate successful hit
        return False # Return False if no brick was hit
        
    def update(self, dt): # Update the wall state with a time step (dt) 
        if self.breaking: # If the wall is breaking 
            self.break_timer += dt # Increment the break timer with the time step
            # Increase shake as time passes
            progress = self.break_timer / self.break_duration # Calculate the progress of the breaking animation
            
            if progress < 0.8: # During the first 80% of the animation
                # During the first 80%, increase shake
                self.shake_amount = 5 + 15 * (progress / 0.8)   # Gradually increase shake amount 
                
                # Gradually break bricks
                break_threshold = progress * 0.8 # Gradually increase the break threshold 
                for brick in self.bricks: # Loop through each brick 
                    if not brick["broken"]: # If the brick is not broken
                        # Randomly break bricks as animation progresses
                        if random.random() < (break_threshold * 0.1): # Randomly break bricks based on the break threshold 
                            brick["broken"] = True # Break the brick 
            else:
                # Final 20% - all bricks break quickly
                for brick in self.bricks: # Loop through each brick 
                    if not brick["broken"] and random.random() < 0.4: # If the brick is not broken and a random chance is met
                        brick["broken"] = True # Break the brick
            
            # Check if animation is complete
            if self.break_timer >= self.break_duration: # If the break timer exceeds the break duration
                return True  # Wall breaking complete
                
        return False # Wall breaking not complete
