import pygame
from src.scene_manager import SceneManager
from src.bar_scene import BarScene

# Initialize Pygame
pygame.init()

# Game Settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D RPG Game")

# Game Class
class Game:
    def __init__(self):
        self.running = True
        self.scene_manager = SceneManager(self)
        self.scene_manager.set_scene(BarScene)  # Start with bar scene

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.scene_manager.handle_events(events)
            self.scene_manager.update()

            SCREEN.fill((0, 0, 0))  # Clear screen
            self.scene_manager.draw(SCREEN)
            pygame.display.flip()

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
