import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define a more complex labyrinth but with more openings
def create_labyrinth_walls():
    # Outer boundaries
    walls = [
        # Outer walls
        pygame.Rect(0, 0, SCREEN_WIDTH, 20),
        pygame.Rect(0, 0, 20, SCREEN_HEIGHT),
        pygame.Rect(0, SCREEN_HEIGHT-20, SCREEN_WIDTH, 20),
        pygame.Rect(SCREEN_WIDTH-20, 0, 20, SCREEN_HEIGHT),
    ]
    
    # Vertical walls - with gaps for better navigation
    v_walls = [
        # Left section - shortened to create openings
        pygame.Rect(100, 60, 15, 100),      # Shortened
        pygame.Rect(100, 290, 15, 110),     # Gap created
        pygame.Rect(100, 450, 15, 130),
        pygame.Rect(200, 20, 15, 130),      # Shortened
        pygame.Rect(200, 250, 15, 150),     # Shortened
        pygame.Rect(200, 500, 15, 80),
        pygame.Rect(300, 100, 15, 150),     # Shortened
        pygame.Rect(300, 380, 15, 120),     # Gap created
        
        # Middle section - modified for better flow
        pygame.Rect(400, 50, 15, 110),      # Shortened
        pygame.Rect(400, 250, 15, 150),     # Shortened
        pygame.Rect(400, 500, 15, 80),
        
        # Right section - adjusted
        pygame.Rect(500, 100, 15, 50),     # Shortened
        pygame.Rect(500, 400, 15, 100),
        pygame.Rect(600, 20, 15, 130),      # Shortened
        pygame.Rect(600, 250, 15, 150),     # Shortened
        pygame.Rect(700, 350, 15, 150),     # Gap created
    ]
    
    # Horizontal walls - with more openings
    h_walls = [
        # Top section
        pygame.Rect(20, 100, 80, 15),       # Shortened
        pygame.Rect(200, 100, 100, 15),     # Shortened
        pygame.Rect(400, 100, 80, 15),      # Shortened
        pygame.Rect(600, 100, 80, 15),      # Shortened
        
        # Upper middle section - modified
        pygame.Rect(130, 200, 70, 15),      # Shortened
        pygame.Rect(250, 200, 100, 15),     # Shortened
        pygame.Rect(500, 200, 50, 15),      # Shortened
        pygame.Rect(650, 200, 130, 15),
        
        # Middle section - adjusted for more pathways
        pygame.Rect(20, 300, 80, 15),       # Shortened
        pygame.Rect(250, 300, 80, 15),      # Shortened
        pygame.Rect(430, 300, 70, 15),      # Adjusted position
        pygame.Rect(600, 300, 80, 15),      # Shortened
        
        # Lower middle section - more gaps
        pygame.Rect(150, 400, 100, 15),     # Adjusted position
        pygame.Rect(320, 400, 140, 15),      # Shortened
        pygame.Rect(500, 400, 35, 15),      # Shortened
        pygame.Rect(650, 400, 130, 15),
        
        # Bottom section - opened up starting area
        pygame.Rect(20, 500, 30, 15),       # Much shorter
        pygame.Rect(150, 500, 100, 15),     # Shortened
        pygame.Rect(400, 500, 100, 15),     # Shortened
        pygame.Rect(600, 500, 100, 15),     # Shortened
    ]
    
    # Add all walls
    walls.extend(v_walls)
    walls.extend(h_walls)
    
    return walls