import pygame
from src.scenes.fight.GameState import GameState

class KitchenFirstScene(GameState):
    def __init__(self):
        self.dialog_active = True  # Track if the dialogue is active

    def handle_events(self, event, game):
        """Handle events for the first kitchen scene."""
        if self.dialog_active:
            # Advance dialogue when SPACE is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Check for SPACE key
                result = game.dialog_system.next_dialog() # Advance dialogue
                if result is None: # No special transition
                    return  # Continue dialogue
                else: # Handle special transition
                    print("Dialogue finished. Player can now move.") # Debugging
                    self.dialog_active = False  # End dialogue and allow movement
        else:
            # Handle interaction with the fridge
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                fridge = next(prop for prop in game.props if prop.type == "fridge")
                if abs(game.player.x - fridge.x) < game.player.width + 20 and abs(game.player.y - fridge.y) < game.player.height + 20:
                    print("Player interacted with the fridge. Transitioning to FRIDGE_MINIGAME.")
                    game.change_state("FRIDGE_MINIGAME")

    def update(self, game):
        """Update the first kitchen scene."""
        if self.dialog_active == False:
            # Handle player movement
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_RIGHT]:
                dx = 1
            if keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_DOWN]:
                dy = 1
            game.player.move(dx, dy, game.props)

    def draw(self, screen, game):
        """Draw the first kitchen scene."""
        # Draw the kitchen background
        game.kitchen.draw(screen)

        # Draw props
        for prop in game.props:
            prop.draw(screen)

        # Draw player
        game.player.draw(screen)
        game.dad.draw(screen)

        if self.dialog_active:
            # Draw dialogue
            game.dialog_system.draw(screen, {"Tim": game.player, "Dad": game.dad})
        else:
            # Draw instructions
            instruction_text = game.small_font.render("Walk to the fridge and press SPACE to open it.", True, (0, 0, 0))
            screen.blit(instruction_text, (400 - instruction_text.get_width() // 2, 550))