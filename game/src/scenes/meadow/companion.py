import pygame
from src.scenes.meadow.character import Character

class Companion(Character):
    def follow(self, target):
        """Move the companion to follow the target character."""
        follow_speed = 2  # Speed at which Lav follows Tim
        tolerance = 5  # Dead zone to prevent jittering

        # Horizontal movement
        if abs(self.rect.x - (target.rect.x - 50)) > tolerance:
            if self.rect.x < target.rect.x - 50:
                self.rect.x += follow_speed
            elif self.rect.x > target.rect.x - 50:
                self.rect.x -= follow_speed

        # Vertical movement
        if abs(self.rect.y - target.rect.y) > tolerance:
            if self.rect.y < target.rect.y:
                self.rect.y += follow_speed
            elif self.rect.y > target.rect.y:
                self.rect.y -= follow_speed