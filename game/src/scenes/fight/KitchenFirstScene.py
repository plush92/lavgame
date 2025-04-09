import pygame
from src.scenes.fight.GameState import GameState

class KitchenFirstScene(GameState):
    def handle_events(self, event, game):
        """Handle events for the first kitchen scene."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Check if the player is near the fridge
            fridge = next(prop for prop in game.props if prop.type == "fridge")
            if abs(game.player.x - fridge.x) < game.player.width + 20 and abs(game.player.y - fridge.y) < game.player.height + 20:
                print("Player interacted with the fridge. Transitioning to FRIDGE_MINIGAME.")
                game.change_state("FRIDGE_MINIGAME")

    def update(self, game):
        """Update the first kitchen scene."""
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
        game.player.move(dx, dy, game.props)  # Pass the props list directly

    def draw(self, screen, game):
        """Draw the first kitchen scene."""
        # Draw the kitchen background
        game.kitchen.draw(screen)

        # Draw props and player
        for prop in game.props:
            prop.draw(screen)
        game.player.draw(screen)

        # Draw instructions
        instruction_text = game.small_font.render("Walk to the fridge and press SPACE to open it.", True, (0, 0, 0))
        screen.blit(instruction_text, (400 - instruction_text.get_width() // 2, 550))