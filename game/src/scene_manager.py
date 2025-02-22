import pygame

class Scene:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class SceneManager:
    def __init__(self, game):
        self.game = game
        self.current_scene = None

    def set_scene(self, scene):
        """ Change to a new scene """
        self.current_scene = scene(self.game)

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)
