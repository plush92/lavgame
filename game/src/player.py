import pygame
import os

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/player.png"))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
