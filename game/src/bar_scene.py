import pygame
import os
from .scene_manager import Scene
from .player import Player

class BarScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        assets_path = os.path.join(os.path.dirname(__file__), "../assets/bar_background.png")
        self.background = pygame.image.load(assets_path)

        # Create the player at starting position (x=100, y=300)
        self.player = Player(100, 300)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to switch scenes
                    self.game.scene_manager.set_scene(self.game.car_scene)

    def update(self):
        self.player.handle_keys()  # Move the player

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.player.draw(screen)  # Draw the player
