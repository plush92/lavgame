import pygame
import random
import os

# Constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
ROAD_WIDTH = int(WIDTH * 0.7)
MARGIN = (WIDTH - ROAD_WIDTH) // 2
LANE_WIDTH = ROAD_WIDTH // 4
OBSTACLE_SPEED = 2.5
SPAWN_RATE = 40

class PreGameScene:
    """Displays a convertible moving across the screen."""
    def __init__(self):
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
        
        # Load and scale convertible
        self.convertible = pygame.image.load(os.path.join(assets_dir, "convertible.png"))
        self.convertible = pygame.transform.scale(self.convertible, (200, 100))
        self.convertible_rect = self.convertible.get_rect(midleft=(-200, HEIGHT // 2))  # Start off-screen left
        
        self.car_speed = 5  # Speed of the convertible
        self.show_scene = True  # Flag to keep scene running
    
    def update(self):
        """Moves the convertible across the screen."""
        if self.convertible_rect.left < WIDTH:  # Move until it's fully off-screen right
            self.convertible_rect.x += self.car_speed
        else:
            self.show_scene = False  # Exit the scene when the car moves off-screen
    
    def draw(self, screen):
        """Draws the convertible."""
        screen.fill((50, 50, 50))  # Gray background
        screen.blit(self.convertible, self.convertible_rect)  # Draw the convertible

    def handle_events(self, events):
        """Handles events and runs the pre-game animation."""
        clock = pygame.time.Clock()
        
        while self.show_scene:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.update()
            self.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)
        
        print("Convertible animation complete.")

# Start the animation
if __name__ == "__main__":
    pygame.init()
    pre_game = PreGameScene()
    pre_game.handle_events()
