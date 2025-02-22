import pygame
import random

class DrivingScene:
    def __init__(self, game):
        self.game = game
        self.car = pygame.image.load("assets/car.png")  # Load car sprite
        self.car = pygame.transform.scale(self.car, (50, 100))  # Resize
        self.car_rect = self.car.get_rect(center=(400, 500))  # Start position
        self.speed = 5
        self.obstacles = []
        self.spawn_obstacle()

    def spawn_obstacle(self):
        obstacle = pygame.Rect(random.randint(100, 700), -50, 50, 50)  # Random position
        self.obstacles.append(obstacle)

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.car_rect.x > 100:
            self.car_rect.x -= 5
        if keys[pygame.K_RIGHT] and self.car_rect.x < 700:
            self.car_rect.x += 5

    def update(self):
        for obstacle in self.obstacles:
            obstacle.y += self.speed
            if obstacle.y > 600:  # Remove obstacles that go off-screen
                self.obstacles.remove(obstacle)
                self.spawn_obstacle()

        # Collision detection
        for obstacle in self.obstacles:
            if self.car_rect.colliderect(obstacle):
                print("Collision! Game Over.")  # Replace with scene change or penalty

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Black background
        screen.blit(self.car, self.car_rect)  # Draw the car

        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle)  # Draw obstacles as red squares
