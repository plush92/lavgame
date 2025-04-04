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
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))  # Path to the assets directory
        self.car = pygame.image.load(os.path.join(assets_dir, "car.png"))  # Load the car image
        self.car = pygame.transform.scale(self.car, (40, 80))  # Scale the car image
        self.car_rect = self.car.get_rect(midbottom=(MARGIN + LANE_WIDTH * 1.5, HEIGHT - 120))  # Position the car
        self.lane_positions = [MARGIN + LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(4)]  # Calculate lane positions
        self.current_lane = 1  # Start in the second lane
        self.obstacles = []  # List to store obstacles
        self.frame_count = 0  # Frame counter for obstacle spawning
        self.running = True  # Flag to indicate whether the driving scene is active
        
        self.player = pygame.image.load(os.path.join(assets_dir, "player.png"))  # Load the player image
        self.player = pygame.transform.scale(self.player, (20, 30))  # Scale the player image
        self.girl = pygame.image.load(os.path.join(assets_dir, "girl.png"))  # Load the girl image
        self.girl = pygame.transform.scale(self.girl, (20, 30))  # Scale the girl image
        self.gargoyle = pygame.image.load(os.path.join(assets_dir, "gargoyle.png"))  # Load the gargoyle image
        self.gargoyle = pygame.transform.scale(self.gargoyle, (30, 30))  # Scale the gargoyle image, 
        
        # Load obstacle images
        obstacle_filenames = [
            "bar.png",  # Filename for bar obstacle
            "burgerking.png",  # Filename for Burger King obstacle
            "casino.png",  # Filename for casino obstacle
            "hooters.png",  # Filename for Hooters obstacle
            "mcdonalds.png",  # Filename for McDonald's obstacle
            "wine.png"  # Filename for wine obstacle
        ]
        self.obstacle_images = [
            pygame.transform.scale(pygame.image.load(os.path.join(assets_dir, filename)), (50, 50))  # Load and scale each obstacle image
            for filename in obstacle_filenames
        ]
        self.highway_top = self.load_highway_top_image()  # Load the highway top image
    
    def load_highway_top_image(self):
        """Load and return the highway top image."""
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))  # Path to the assets directory
        highway_top = pygame.image.load(os.path.join(assets_dir, "highwaytop.png"))  # Load the highway top image
        return pygame.transform.scale(highway_top, (WIDTH, 100))  # Scale the image to fit the screen width
    
    def update(self):
        self.car_rect.centerx = self.lane_positions[self.current_lane]  # Update the car's position based on the current lane
        
        for obstacle in self.obstacles:  # Move each obstacle down the screen
            obstacle[0].y += OBSTACLE_SPEED
        
        for obstacle in self.obstacles:  # Check for collisions with the car
            if self.car_rect.colliderect(obstacle[0]):  # If a collision occurs
                print("💥 Collision! Game Over!")  # Print a collision message
                self.running = False  # Stop the game
        
        self.obstacles = [obs for obs in self.obstacles if obs[0].y < HEIGHT]  # Remove obstacles that are off-screen
        
        self.frame_count += 1  # Increment the frame counter
        if self.frame_count % SPAWN_RATE == 0:  # Check if it's time to spawn a new obstacle
            self.spawn_obstacle()  # Spawn a new obstacle
    
    def draw(self, screen):
        screen.fill((30, 30, 30))  # Fill the screen with a dark gray background
        pygame.draw.rect(screen, (50, 50, 50), (MARGIN, 0, ROAD_WIDTH, HEIGHT))  # Draw the road

        highway_top = self.load_highway_top_image()  # Load the highway background
        screen.blit(highway_top, (0, 0))  # Draw the highway background
        
        for i in range(1, 4):  # Draw lane dividers
            pygame.draw.line(screen, (255, 255, 255), (MARGIN + LANE_WIDTH * i, 0), (MARGIN + LANE_WIDTH * i, HEIGHT), 5)
        
        screen.blit(self.car, self.car_rect)  # Draw the car
        screen.blit(self.player, (self.car_rect.left + 10, self.car_rect.top + 10))  # Draw the player on the car
        screen.blit(self.girl, (self.car_rect.left + 10, self.car_rect.top + 10))  # Draw the girl on the car
        screen.blit(self.gargoyle, (self.car_rect.left + 5, self.car_rect.top + 5))  # Draw the gargoyle on the car
        
        for obstacle_rect, obstacle_image in self.obstacles:  # Draw each obstacle
            screen.blit(obstacle_image, obstacle_rect.topleft)  # Draw the obstacle image at its position
    
    def handle_events(self, events):
        for event in events:  # Iterate through all events
            if event.type == pygame.KEYDOWN:  # Check if a key is pressed
                if event.key == pygame.K_LEFT and self.current_lane > 0:  # Move left if not in the leftmost lane
                    self.current_lane -= 1
                elif event.key == pygame.K_RIGHT and self.current_lane < 3:  # Move right if not in the rightmost lane
                    self.current_lane += 1
    
    def spawn_obstacle(self):
        lane = random.randint(0, 3)  # Randomly select a lane for the obstacle
        x_position = self.lane_positions[lane] - 25  # Calculate the x-position of the obstacle
        obstacle_rect = pygame.Rect(x_position, -50, 50, 50)  # Create a rectangle for the obstacle
        obstacle_image = random.choice(self.obstacle_images)  # Randomly select an obstacle image
        self.obstacles.append((obstacle_rect, obstacle_image))  # Add the obstacle to the list