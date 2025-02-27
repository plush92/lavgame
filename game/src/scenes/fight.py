import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight Scene")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Character settings
CHAR_WIDTH, CHAR_HEIGHT = 50, 100
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20

class Character:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, CHAR_WIDTH, CHAR_HEIGHT)
        self.color = color
        self.health = 100

    def move_to_cursor(self, pos):
        """ Moves the player toward the cursor position """
        self.rect.x = pos[0] - self.rect.width // 2  # Center on cursor

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def draw_health_bar(self, screen, x, y):
        """ Draws a health bar above the character """
        pygame.draw.rect(screen, RED, (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))  # Background
        pygame.draw.rect(screen, GREEN, (x, y, self.health * 2, HEALTH_BAR_HEIGHT))  # Current health

class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y, RED)
        self.direction = 1  # Move left/right
        self.speed = 2

    def move_randomly(self):
        """ Moves left and right randomly """
        self.rect.x += self.speed * self.direction
        if self.rect.left < 100 or self.rect.right > WIDTH - 100:
            self.direction *= -1  # Change direction

class FightScene:
    def __init__(self):
        self.dialogue_active = True  # Start with dialogue
        self.dialogue_text = "You're going down, old man!"
        self.player = Character(200, HEIGHT - 150, GREEN)
        self.enemy = Enemy(500, HEIGHT - 150)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.dialogue_active:  # If dialogue is active, disable it and start fight
                    self.dialogue_active = False
                else:
                    self.punch()


    def punch(self):
        """ Player attacks if close enough """
        if abs(self.player.rect.centerx - self.enemy.rect.centerx) < 60:
            self.enemy.health -= 10
            print("Hit!")

    def update(self):
        """ Update game logic """
        if not self.dialogue_active:
            self.enemy.move_randomly()
            self.player.move_to_cursor(pygame.mouse.get_pos())

            # Check win condition
            if self.enemy.health <= 0:
                print("You win!")

    def draw(self, screen):
        """ Render the scene """
        screen.fill(WHITE)
        
        if self.dialogue_active:
            self.draw_dialogue(screen)
        else:
            self.player.draw(screen)
            self.enemy.draw(screen)
            self.player.draw_health_bar(screen, 50, 50)
            self.enemy.draw_health_bar(screen, WIDTH - 250, 50)

    def draw_dialogue(self, screen):
        """ Draws a simple dialogue box """
        pygame.draw.rect(screen, BLACK, (100, HEIGHT - 150, 600, 100))
        text = font.render(self.dialogue_text, True, WHITE)
        screen.blit(text, (120, HEIGHT - 120))

    def start_fight(self):
        """ Start the fight after the dialogue """
        self.dialogue_active = False

# Game loop
def main():
    clock = pygame.time.Clock()
    fight_scene = FightScene()

    running = True
    while running:
        events = pygame.event.get()
        fight_scene.handle_events(events)
        fight_scene.update()
        fight_scene.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def start_fight():
    main()  # This runs the fight scene when called

if __name__ == "__main__":
    start_fight()
