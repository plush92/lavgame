import pygame
import random
from pygame.math import Vector2

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

class Wall: # Wall class for the wall game scene
    def __init__(self, screen_width, screen_height): # Initialize the wall with the screen width and height
        # Wall state tracking variables
        self.hit_count = 0 # Number of hits on the wall
        self.max_hits = 3 # Maximum hits before wall is destroyed
        self.is_destroyed = False # Flag for wall destruction
        
        # Load wall damage images
        try: # Try to load the wall images
            self.wall_stages = [ # List of wall damage images
                pygame.image.load('assets/wall_stage0.jpeg'),  # Pristine wall #game/assets/wall_stage0.jpeg
                pygame.image.load('assets/wall_stage1.png'),  # First hit damage #game/assets/wall_stage1.png
                pygame.image.load('assets/wall_stage0.jpeg'),  # Second hit damage
                pygame.image.load('assets/wall_stage1.png')   # Final destruction
            ]
        except pygame.error as e: # Handle image loading errors 
            print(f"Error loading wall images: {e}") # Print the error message
            self.wall_stages = None # Set wall stages to None
        
        # Wall positioning
        self.screen_width = screen_width # Screen width for positioning
        self.screen_height = screen_height # Screen height for positioning
        
        # Calculate wall position (centered)
        if self.wall_stages: # If wall images are loaded
            wall_image = self.wall_stages[0] # Get the first wall image
            self.x = (screen_width - wall_image.get_width()) // 2 # Calculate the x position to center the wall
            self.y = (screen_height - wall_image.get_height()) // 2 # Calculate the y position to center the wall
        else: # If wall images are not loaded
            self.x = screen_width // 2 - 100 # Set x position to center of the screen
            self.y = screen_height // 2 - 100 # Set y position to center of the screen
        
        # Shake effect for impact
        self.shake_offset = (0, 0) # Initial shake offset (x, y), no offset
        self.shake_duration = 0 # Shake duration
        self.shake_intensity = 5 # Shake intensity
    
    def draw(self, screen): # Draw the wall on the screen
        # Handle no images case
        if not self.wall_stages: # If wall images are not loaded
            return # Exit the function
        
        # Determine current wall stage
        current_stage = min(self.hit_count, self.max_hits) # Get the current wall damage stage
        
        # Apply shake if active
        offset_x, offset_y = 0, 0 # Initial offset values for shake effect (x, y)
        if self.shake_duration > 0:  # If the shake duration is active
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity) # Random offset within intensity range for x position 
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity) # Random offset within intensity range for y position
        
        # Draw wall with current damage stage
        screen.blit(self.wall_stages[current_stage],  # Blit the current wall image to the screen with the shake offset
                    (self.x + offset_x, self.y + offset_y)) # Position the wall image with the shake offset (x, y) 
    
    def hit(self, mouse_pos): # Handle wall hit detection with mouse position 
        # Check if hit is within wall image bounds
        if not self.wall_stages or self.is_destroyed: # If wall images are not loaded or wall is destroyed
            return False # Exit the function
        
        current_wall = self.wall_stages[min(self.hit_count, self.max_hits)] # Get the current wall image based on damage stage 
        wall_rect = current_wall.get_rect(topleft=(self.x, self.y)) # Get the rectangle of the wall image at the top left corner
        
        if wall_rect.collidepoint(mouse_pos):   # If the mouse position is within the wall image bounds
            # Increment hit count on successful hit
            self.hit_count += 1 # Increment the hit count
            
            # Trigger shake effect
            self.shake_duration = 10 # Set the shake duration to 10 milliseconds (0.01 seconds)
            
            # Check if wall is destroyed
            if self.hit_count >= self.max_hits: # If the hit count reaches the maximum hits 
                self.is_destroyed = True # Set the wall as destroyed
            
            return True # Return True if the hit is successful
        
        return False # Return False if the hit is not successful
    
    def update(self, dt): # Update the wall state based on time 
        # Manage shake duration
        if self.shake_duration > 0: # If the shake duration is active 
            self.shake_duration -= dt # Decrement the shake duration by the time passed (delta time) 
        
        # Return True if wall is completely destroyed
        return self.is_destroyed # Return True if the wall is destroyed, False otherwise 