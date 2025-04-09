from src.scenes.fight.FridgeMiniGame import FridgeMinigame

class FridgeMinigameScene:
    def __init__(self, screen_width, screen_height, background_image_path):
        self.fridge_minigame = FridgeMinigame(screen_width, screen_height, background_image_path)

    def handle_events(self, event, game):
        """Delegate event handling to the FridgeMinigame instance."""
        if self.fridge_minigame.handle_events(event):
            # Transition to the next state when tortellini is found
            game.change_state("KITCHEN_SECOND")

    def update(self, game):
        """Update the fridge minigame."""
        self.fridge_minigame.update(game)

    def draw(self, screen, game):
        """Draw the fridge minigame."""
        self.fridge_minigame.draw(screen)