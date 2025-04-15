import pygame  # Import the pygame library for game development
import random  # Import the random library for random number generation
import os  # Import the os library for file path operations

# Constants
WIDTH, HEIGHT = 800, 600  # Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
ROAD_WIDTH = int(WIDTH * 0.7)  # Width of the road (70% of the screen width)
MARGIN = (WIDTH - ROAD_WIDTH) // 2  # Margin on the left and right of the road
LANE_WIDTH = ROAD_WIDTH // 4  # Width of each lane (road divided into 4 lanes)
OBSTACLE_SPEED = 2.5  # Speed at which obstacles move down the screen
SPAWN_RATE = 40  # Number of frames between spawning new obstacles

class DrivingScene:
    def __init__(self):
        assets_dir = os.path.join(os.path.dirname(__file__), "../../assets")
        self.car = pygame.image.load(os.path.join(assets_dir, "car.png"))
        self.car = pygame.transform.scale(self.car, (40, 80))
        self.car_rect = self.car.get_rect(midbottom=(MARGIN + LANE_WIDTH * 1.5, HEIGHT - 120))
        self.lane_positions = [MARGIN + LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(4)]
        self.current_lane = 1
        self.obstacles = []
        self.frame_count = 0
        self.running = True
        self.distance = 1000  # Start with 100 distance units
        self.won = False  # Track if the player has won

        self.player = pygame.image.load(os.path.join(assets_dir, "player.png"))
        self.player = pygame.transform.scale(self.player, (20, 30))
        self.girl = pygame.image.load(os.path.join(assets_dir, "girl.png"))
        self.girl = pygame.transform.scale(self.girl, (20, 30))
        self.gargoyle = pygame.image.load(os.path.join(assets_dir, "gargoyle.png"))
        self.gargoyle = pygame.transform.scale(self.gargoyle, (30, 30))

        obstacle_filenames = [
            "bar.png", "burgerking.png", "hooters.png", "mcdonalds.png", "wine.png", "wendys.png", "chicfila.png", "renegades.png", "culvers.png", "vegascasino.png", "casino2.png", "casino3.png", "casino4.png"
        ]
        self.obstacle_images = [
            pygame.transform.scale(pygame.image.load(os.path.join(assets_dir, filename)), (50, 50))
            for filename in obstacle_filenames
        ]

        self.highway_top = self.load_highway_top_image()
    
    def load_highway_top_image(self):
        """Loads and scales the highway top image."""
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src/assets"))  # Correct path
        highway_top_path = os.path.join(assets_dir, "highwaytop.png")
        
        try:
            highway_top = pygame.image.load(highway_top_path)
            highway_top = pygame.transform.scale(highway_top, (WIDTH, 100))  # Scale to fit the screen width
            return highway_top
        except pygame.error as e:
            print(f"Error loading highway top image: {e}")
            pygame.quit()
            exit()

    def update(self):
        self.car_rect.centerx = self.lane_positions[self.current_lane]

        for obstacle in self.obstacles:
            obstacle[0].y += OBSTACLE_SPEED

        for obstacle in self.obstacles:
            if self.car_rect.colliderect(obstacle[0].inflate(-10, -10)):  # Reduced collision sensitivity
                print("💥 Collision! Restarting...")
                self.restart_game()  # Restart the game on collision
                return

        self.obstacles = [obs for obs in self.obstacles if obs[0].y < HEIGHT]

        self.frame_count += 1
        if self.frame_count % (SPAWN_RATE + 20) == 0:  # Increase spawn rate slightly
            self.spawn_obstacle()

        # Decrease distance over time
        self.distance -= 1
        if self.distance <= 0:
            self.running = False
            self.won = True  # Mark the game as won
            self.show_win_screen(screen)

    def draw(self, screen):
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (50, 50, 50), (MARGIN, 0, ROAD_WIDTH, HEIGHT))
        # screen.blit(self.highway_top, (0, 0))

        for i in range(1, 4):
            pygame.draw.line(screen, (255, 255, 255), (MARGIN + LANE_WIDTH * i, 0), (MARGIN + LANE_WIDTH * i, HEIGHT), 5)

        screen.blit(self.car, self.car_rect)
        screen.blit(self.player, (self.car_rect.left + 10, self.car_rect.top + 10))
        screen.blit(self.girl, (self.car_rect.left + 10, self.car_rect.top + 10))
        screen.blit(self.gargoyle, (self.car_rect.left + 5, self.car_rect.top + 5))

        for obstacle_rect, obstacle_image in self.obstacles:
            screen.blit(obstacle_image, obstacle_rect.topleft)

        # Draw the distance meter
        font = pygame.font.Font(None, 36)
        distance_text = font.render(f"Distance to Illinois: {self.distance}", True, (255, 255, 255))
        screen.blit(distance_text, (10, 10))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.current_lane > 0:
                    self.current_lane -= 1
                elif event.key == pygame.K_RIGHT and self.current_lane < 3:
                    self.current_lane += 1
                elif event.key == pygame.K_SPACE and not self.running:
                    if self.won:
                        print("Continuing to the next scene...")
                        # Transition to the next scene
                    else:
                        self.restart_game()  # Restart the game if lost

    def spawn_obstacle(self):
        """Spawns a new obstacle in a random lane."""
        lane = random.randint(0, 3)
        x_position = self.lane_positions[lane] - 25
        obstacle_rect = pygame.Rect(x_position, -50, 50, 50)
        
        # Shuffle the obstacle images to ensure variety
        random.shuffle(self.obstacle_images)
        obstacle_image = self.obstacle_images[0]  # Select the first image after shuffling
        
        self.obstacles.append((obstacle_rect, obstacle_image))

    def restart_game(self):
        """Resets the game state after losing."""
        self.distance = 500  # Restart with 50 distance units
        self.obstacles = []
        self.frame_count = 0
        self.running = True
        self.won = False

    def show_win_screen(self, screen):
        """Displays the winning screen."""
        font = pygame.font.Font(None, 72)
        text = font.render("We made it!", True, (255, 255, 255))
        subtext = font.render("Press SPACE to continue", True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        screen.blit(subtext, subtext.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
