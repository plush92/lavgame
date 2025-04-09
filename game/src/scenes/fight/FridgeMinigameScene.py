from src.scenes.fight.FridgeMiniGame import FridgeMinigame

class FridgeMinigameScene:
    def __init__(self, screen_width, screen_height, background_image_path):
        self.fridge_minigame = FridgeMinigame(screen_width, screen_height, background_image_path)

    def handle_events(self, event, game):
        """Handle events for the fridge minigame."""
        if self.fridge_minigame.handle_events(event):
            # Tortellini found, transition to KitchenSecondScene
            print("Tortellini found!")
            game.dialog_system.dialogs = game.dialog_system.dialog_second  # Switch to dialog_second
            game.dialog_system.dialog_index = 0  # Reset dialogue index
            game.dialog_system.active = True  # Activate dialogue system
            game.change_state("KITCHEN_SECOND")

    def update(self, game):
        """Update the fridge minigame."""
        self.fridge_minigame.update(game)

    def draw(self, screen, game):
        """Draw the fridge minigame."""
        self.fridge_minigame.draw(screen)