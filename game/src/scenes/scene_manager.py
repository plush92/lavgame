class SceneManager:
    def __init__(self, game):
        self.game = game
        self.scene = None

    def set_scene(self, scene):
        """ Set the active scene """
        self.scene = scene

    def handle_events(self, events):
        """ Forward events to the current scene """
        if self.scene:
            self.scene.handle_events(events)

    def update(self):
        """ Update the current scene """
        if self.scene:
            self.scene.update()

    def draw(self, screen):
        """ Draw the current scene """
        if self.scene:
            self.scene.draw(screen)

