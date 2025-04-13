import pygame
from src.scenes.fight.GameState import GameState

class GameOver(GameState):
    def handle_events(self, event, game):
        """Handle events for the game over state."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restart the game
                game.change_state("KITCHEN_FIRST")
            elif event.key == pygame.K_q:
                # Quit the game
                game.running = False

    def update(self, game):
        """No updates needed for the game over state."""
        pass

    def draw(self, screen, game):
        """Draw the game over screen."""
        screen.fill((0, 0, 0))  # Black background

        # Display the game over message
        font = pygame.font.Font(None, 48)
        message = font.render("You killed your dad! Congratulations!", True, (255, 255, 255))
        restart_message = font.render("Press SPACE to continue", True, (255, 255, 255))

        # Center the messages on the screen
        screen.blit(message, 
                    (screen.get_width() // 2 - message.get_width() // 2, 
                     screen.get_height() // 2 - message.get_height() // 2))
        screen.blit(restart_message, 
                    (screen.get_width() // 2 - restart_message.get_width() // 2, 
                     screen.get_height() // 2 + 50))