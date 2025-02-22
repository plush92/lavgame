import pygame
from src.scenes.scene_manager import SceneManager
# from src.scenes.bar_scene import BarScene
from src.scenes.driving_scene import DrivingScene

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lav's Game")

# Game Class
class Game:
    def __init__(self):
        self.running = True
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = SCREEN
        self.clock = pygame.time.Clock()
        self.scene_manager = SceneManager(self)
        self.scene_manager.set_scene(DrivingScene)

    def run(self):
        while self.running:
            # Cap the frame rate
            self.clock.tick(60)
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # Update and draw
            self.scene_manager.handle_events(events)
            self.scene_manager.update()

            self.screen.fill((0, 0, 0))  # Clear screen
            self.scene_manager.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
