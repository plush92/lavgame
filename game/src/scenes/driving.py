import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
ROAD_WIDTH = int(WIDTH * 0.7)  # 70% of the screen width for the road
MARGIN = (WIDTH - ROAD_WIDTH) // 2  # Space on left and right
LANE_WIDTH = ROAD_WIDTH // 4  # Divide road into 4 lanes
CAR_SPEED = 5
OBSTACLE_SPEED = 5
SPAWN_RATE = 30  # Frames between obstacle spawns

class DrivingScene:
    def __init__(self, game):
        self.game = game
        self.car = pygame.image.load("assets/car.png")
        self.car = pygame.transform.scale(self.car, (50, 100))
        self.car_rect = self.car.get_rect(midbottom=(MARGIN + LANE_WIDTH * 1.5, HEIGHT - 120))
        self.lane_positions = [MARGIN + LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(4)]
        self.current_lane = 1  # Second lane
        self.obstacles = []
        self.frame_count = 0  # Track frames for obstacle spawning
        self.running = True  # Game state
    
    def update(self):
        # Update car position
        self.car_rect.centerx = self.lane_positions[self.current_lane]
        
        # Move obstacles
        for obstacle in self.obstacles:
            obstacle.y += OBSTACLE_SPEED
        
        # Check for collisions
        for obstacle in self.obstacles:
            if self.car_rect.colliderect(obstacle):
                print("💥 Collision! Game Over!")
                self.running = False

        # Remove obstacles that go off-screen
        self.obstacles = [obs for obs in self.obstacles if obs.y < HEIGHT]

        # Spawn new obstacles at intervals
        self.frame_count += 1
        if self.frame_count % SPAWN_RATE == 0:
            self.spawn_obstacle()

    def draw(self, screen):
        screen.fill((30, 30, 30))  # Background color

        # Draw road
        pygame.draw.rect(screen, (50, 50, 50), (MARGIN, 0, ROAD_WIDTH, HEIGHT))

        # Draw lane lines
        for i in range(1, 4):
            pygame.draw.line(screen, (255, 255, 255), 
                             (MARGIN + LANE_WIDTH * i, 0), 
                             (MARGIN + LANE_WIDTH * i, HEIGHT), 5)
        
        # Draw car
        screen.blit(self.car, self.car_rect)

        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (0, 0, 255), obstacle)  # Blue obstacles
        
        # Draw UI elements in the margin
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Score: {self.frame_count // 10}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))  # Position top-left

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.current_lane > 0:
                    self.current_lane -= 1
                elif event.key == pygame.K_RIGHT and self.current_lane < 3:
                    self.current_lane += 1

    def spawn_obstacle(self):
        """Create an obstacle in a random lane at the top of the screen."""
        lane = random.randint(0, 3)
        x_position = self.lane_positions[lane] - 25  # Center in lane
        obstacle = pygame.Rect(x_position, -50, 50, 50)  # Blue square
        self.obstacles.append(obstacle)

# Game loop
def main():
    clock = pygame.time.Clock()
    driving_scene = DrivingScene(None)  # Pass None or game object

    while driving_scene.running:  # Run only while the scene is active
        events = pygame.event.get()
        driving_scene.handle_events(events)
        driving_scene.update()
        driving_scene.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    print("Exited driving scene. Returning to main menu...")
    return  # This will allow returning to the main menu

def start_driving():
    main()  # Runs the driving scene
    import src.main_menu  # Import main menu module
    src.main_menu.main_menu()  # Call the main menu again


if __name__ == "__main__":
    start_driving()
