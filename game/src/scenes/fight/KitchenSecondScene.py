import pygame
from src.scenes.fight.GameState import GameState

class KitchenSecondScene(GameState):
    def __init__(self):
        self.dialog_active = True  # Track if the dialogue is active

    def handle_events(self, event, game):
        """Handle events for the second kitchen scene."""
        if self.dialog_active:
            # Advance dialogue when SPACE is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                result = game.dialog_system.next_dialog()
                if result == "FIGHTING":
                    print("Transitioning to FIGHTING state.")
                    game.change_state("FIGHT")

    def update(self, game):
        """Update the second kitchen scene."""
        # No additional updates needed for this scene
        pass

    def draw(self, screen, game):
        """Draw the second kitchen scene."""
        # Draw the kitchen background
        game.kitchen.draw(screen)

        # Draw props
        for prop in game.props:
            prop.draw(screen)

        # Draw characters
        game.player.draw(screen)
        game.dad.draw(screen)

        # Draw dialogue
        game.dialog_system.draw(screen, {"Tim": game.player, "Dad": game.dad})