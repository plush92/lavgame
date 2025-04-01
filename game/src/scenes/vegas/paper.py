import pygame
import sys
import random
import time
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
font_small = pygame.font.SysFont('Arial', 12)
font_medium = pygame.font.SysFont('Arial', 28)
font_large = pygame.font.SysFont('Arial', 36)

# Game states
STATE_DIALOGUE = 0
STATE_WALL_GAME = 1
STATE_ENDING = 2
game_state = STATE_DIALOGUE

class Paper: # Paper class for the divorce papers
    def __init__(self): # Initialize the paper
        self.pos = Vector2(WIDTH // 2, HEIGHT // 2)  # Start from the center
        angle = random.uniform(0, 360)  # Random angle for outward movement
        speed = random.uniform(2, 5)  # Random speed
        self.vel = Vector2(speed, 0).rotate(angle)  # Convert speed to vector
        self.rotation = random.randint(0, 360)
        self.rot_speed = random.uniform(-2, 2)
        self.size = Vector2(60, 80)
        self.paper_img = self._create_paper_image()
        self.lifetime = random.uniform(2, 5)  # Each paper lasts 2-5 seconds
        self.start_time = time.time()  # Track when it was created
        
    def _create_paper_image(self): 
        # Create a simple paper with text and lines 
        surf = pygame.Surface((int(self.size.x), int(self.size.y)), pygame.SRCALPHA) # Create a transparent surface, SRCALPHA for transparency, RGBA for color, and RGB for no transparency, no alpha channel
        pygame.draw.rect(surf, WHITE, (0, 0, int(self.size.x), int(self.size.y))) # Draw a white rectangle for the paper, (surface, color, (x, y, width, height)), (0, 0) is the top left corner, (size.x, size.y) is the bottom right corner
        pygame.draw.rect(surf, BLACK, (0, 0, int(self.size.x), int(self.size.y)), 1) # Draw a black outline for the paper, (surface, color, (x, y, width, height), thickness), 1 for thin outline
        
        # Add "DIVORCE" text to the paper
        text = font_small.render("DIVORCE", True, BLACK) # Render the text "DIVORCE" with the font_small font and black color
        surf.blit(text, (int(self.size.x/2 - text.get_width()/2), 10)) # Blit the text to the surface at the center horizontally and 10 pixels from the top
        
        # Add some lines for text
        for i in range(3): # Loop 3 times
            pygame.draw.line(surf, BLACK, (10, 30 + i*15), (int(self.size.x) - 10, 30 + i*15), 1) # Draw a line from (10, 30 + i*15) to (size.x - 10, 30 + i*15), 1 for thin line
            # 30 + i*15 is the vertical position of the line, 30 for the first line, 45 for the second line, 60 for the third line
            # i*15 is the spacing between lines, 0 for the first line, 15 for the second line, 30 for the third line
            # 10 is the left margin, size.x - 10 is the right margin
            # (10, 30 + i*15) is the start position, (size.x - 10, 30 + i*15) is the end position
            # 1 is the thickness of the line
            # BLACK is the color of the line
        
        return surf # Return the paper surface
        
    def update(self): # Update the paper position and rotation
        self.pos += self.vel # Add the velocity to the position, move the paper, (x, y) + (x, y) = (x + x, y + y), (1, 2) + (3, 4) = (1 + 3, 2 + 4) = (4, 6)
        self.rotation += self.rot_speed # Add the rotation speed to the rotation angle, rotate the paper, 0 + 2 = 2, 90 + (-2) = 88, 180 + 0 = 180, 270 + 2 = 272
        return time.time() - self.start_time > self.lifetime  # Check if the paper's lifetime has expired
        
    def draw(self): # Draw the paper on the screen
        rotated = pygame.transform.rotate(self.paper_img, self.rotation)  # Create a new image by rotating the paper image to match its current rotation angle
        rect = rotated.get_rect(center=(int(self.pos.x), int(self.pos.y)))  # Get the bounding rectangle of the rotated image, centered at the paper's position
        screen.blit(rotated, rect) # Blit the rotated image to the screen at the rectangle position, (image, position), (rotated, rect)
        # The rotated image will be drawn centered at the position