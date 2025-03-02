import pygame

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Maze Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Game Map: 0 = wall, 1 = path, 2 = exit
MAP = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        new_x, new_y = self.x + dx, self.y + dy
        if MAP[new_y][new_x] != 0:  # Prevent walking into walls
            self.x, self.y = new_x, new_y

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Game loop
def main():
    player = Player(1, len(MAP) - 2)  # Start at bottom-left (1, second-last row)
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill(BLACK)
        
        # Draw map
        for y, row in enumerate(MAP):
            for x, tile in enumerate(row):
                color = WHITE if tile == 1 else BLACK
                if tile == 2:
                    color = GREEN  # Goal
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        player.draw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                elif event.key == pygame.K_UP:
                    player.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1)
        
        if MAP[player.y][player.x] == 2:
            running = False  # End game when reaching goal
        
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()

# if __name__ == "__main__":
#     Game().run()

# def main():
#     clock = pygame.time.Clock()
#     running = True
#     while running:
#         pygame.display.flip()
#         clock.tick(60)

def start_bar_game():
    main()  # This runs the fight scene when called

if __name__ == "__main__":
    start_bar_game()