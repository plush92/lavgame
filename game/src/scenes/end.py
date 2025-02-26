class BaseScene:
    def __init__(self, game):
        """Initialize the scene with a reference to the game instance."""
        self.game = game

    def update(self):
        """Update scene logic. Override in child classes."""
        pass

    def draw(self, screen):
        """Draw scene elements. Override in child classes."""
        pass

    def handle_events(self, events):
        """Handle pygame events. Override in child classes."""
        pass