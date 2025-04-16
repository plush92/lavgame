import pygame
from src.scene_wait_for_continue import scene_wait_for_continue

class GameOver:
    def __init__(self):
        self.finished = False

    def handle_events(self, event, game):
        """Handle events for the Game Over state."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.finished = True  # Signal that the Game Over state is finished
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

    def update(self, game):
        """No updates needed for the Game Over state."""
        pass

    def draw(self, screen, game):
        """Draw the Game Over screen."""
        screen.fill((0, 0, 0))  # Black background
        font = pygame.font.Font(None, 48)
        message = font.render("You killed your dad! Congratulations!", True, (255, 255, 255))
        screen.blit(message, 
                    (screen.get_width() // 2 - message.get_width() // 2, 
                     screen.get_height() // 2 - message.get_height() // 2))
        pygame.display.flip()  # Update the screen

    def run(self, screen):
        """Run the Game Over scene."""
        # Render the Game Over screen for 3 seconds
        self.draw(screen, None)
        pygame.time.delay(3000)

        # Transition to the "Press SPACE to continue" screen
        result = scene_wait_for_continue(screen)
        return result  # Return the result to the caller