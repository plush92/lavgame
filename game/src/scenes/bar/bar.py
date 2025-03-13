import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bar Escape: Hometown Honkey Tonk")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
PINK = (255, 105, 180)
YELLOW = (255, 255, 0)

# Define a more complex labyrinth but with more openings
def create_labyrinth_walls():
    # Outer boundaries
    walls = [
        # Outer walls
        pygame.Rect(0, 0, SCREEN_WIDTH, 20),
        pygame.Rect(0, 0, 20, SCREEN_HEIGHT),
        pygame.Rect(0, SCREEN_HEIGHT-20, SCREEN_WIDTH, 20),
        pygame.Rect(SCREEN_WIDTH-20, 0, 20, SCREEN_HEIGHT),
    ]
    
    # Vertical walls - with gaps for better navigation
    v_walls = [
        # Left section - shortened to create openings
        pygame.Rect(100, 60, 15, 100),      # Shortened
        pygame.Rect(100, 290, 15, 110),     # Gap created
        pygame.Rect(100, 450, 15, 130),
        pygame.Rect(200, 20, 15, 130),      # Shortened
        pygame.Rect(200, 250, 15, 150),     # Shortened
        pygame.Rect(200, 500, 15, 80),
        pygame.Rect(300, 100, 15, 150),     # Shortened
        pygame.Rect(300, 380, 15, 120),     # Gap created
        
        # Middle section - modified for better flow
        pygame.Rect(400, 50, 15, 110),      # Shortened
        pygame.Rect(400, 250, 15, 150),     # Shortened
        pygame.Rect(400, 500, 15, 80),
        
        # Right section - adjusted
        pygame.Rect(500, 100, 15, 50),     # Shortened
        pygame.Rect(500, 400, 15, 100),
        pygame.Rect(600, 20, 15, 130),      # Shortened
        pygame.Rect(600, 250, 15, 150),     # Shortened
        pygame.Rect(700, 350, 15, 150),     # Gap created
    ]
    
    # Horizontal walls - with more openings
    h_walls = [
        # Top section
        pygame.Rect(20, 100, 80, 15),       # Shortened
        pygame.Rect(200, 100, 100, 15),     # Shortened
        pygame.Rect(400, 100, 80, 15),      # Shortened
        pygame.Rect(600, 100, 80, 15),      # Shortened
        
        # Upper middle section - modified
        pygame.Rect(130, 200, 70, 15),      # Shortened
        pygame.Rect(250, 200, 100, 15),     # Shortened
        pygame.Rect(500, 200, 50, 15),      # Shortened
        pygame.Rect(650, 200, 130, 15),
        
        # Middle section - adjusted for more pathways
        pygame.Rect(20, 300, 80, 15),       # Shortened
        pygame.Rect(250, 300, 80, 15),      # Shortened
        pygame.Rect(430, 300, 70, 15),      # Adjusted position
        pygame.Rect(600, 300, 80, 15),      # Shortened
        
        # Lower middle section - more gaps
        pygame.Rect(150, 400, 100, 15),     # Adjusted position
        pygame.Rect(320, 400, 140, 15),      # Shortened
        pygame.Rect(500, 400, 35, 15),      # Shortened
        pygame.Rect(650, 400, 130, 15),
        
        # Bottom section - opened up starting area
        pygame.Rect(20, 500, 30, 15),       # Much shorter
        pygame.Rect(150, 500, 100, 15),     # Shortened
        pygame.Rect(400, 500, 100, 15),     # Shortened
        pygame.Rect(600, 500, 100, 15),     # Shortened
    ]
    
    # Add all walls
    walls.extend(v_walls)
    walls.extend(h_walls)
    
    return walls

# Create the walls
WALLS = create_labyrinth_walls()

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 4
        self.drunk_level = 0
        self.max_drunk_level = 3
        self.recovering = False
        self.recovery_timer = 0
        self.name = "Tim"

    def move(self):
        if self.recovering:
            if time.time() - self.recovery_timer >= 0.5:  # Reduced recovery time to 0.5 seconds
                self.recovering = False
            else:
                return
            
        keys = pygame.key.get_pressed()
        # Base movement
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed

        # Add drunk wobble
        if self.drunk_level > 0:
            dx += random.uniform(-self.drunk_level, self.drunk_level)
            dy += random.uniform(-self.drunk_level, self.drunk_level)

        # Try to move horizontally first
        if dx != 0:
            proposed_rect = self.rect.copy()
            proposed_rect.x += dx
            
            collision = False
            for wall in WALLS:
                if proposed_rect.colliderect(wall):
                    collision = True
                    break
                    
            if not collision:
                self.rect.x += dx
            else:
                self.recovering = True
                self.recovery_timer = time.time()
                
        # Then try to move vertically
        if dy != 0:
            proposed_rect = self.rect.copy()
            proposed_rect.y += dy
            
            collision = False
            for wall in WALLS:
                if proposed_rect.colliderect(wall):
                    collision = True
                    break
                    
            if not collision:
                self.rect.y += dy
            else:
                self.recovering = True
                self.recovery_timer = time.time()
                
        # Keep player in screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Bouncer:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 1.5  # Increased base speed for better pursuit
        self.can_move = False
        self.move_start_time = None
        self.path_finding_timer = 0
        self.stuck_timer = 0
        self.last_position = (x, y)
        self.path_direction = None
        self.alternative_routes = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.current_route_index = 0
        self.route_attempt_time = 0

    def start_moving(self):
        self.can_move = True
        self.move_start_time = time.time()

    def move_towards_player(self, player, walls):
        if not self.can_move:
            return

        # Check if bouncer is stuck
        current_pos = (self.rect.x, self.rect.y)
        if abs(current_pos[0] - self.last_position[0]) < 2 and abs(current_pos[1] - self.last_position[1]) < 2:
            self.stuck_timer += 1
        else:
            self.stuck_timer = 0
            
        # Update pathfinding direction periodically or when stuck
        self.path_finding_timer += 1
        if self.path_finding_timer >= 60 or self.stuck_timer >= 30:  # Update direction every second or when stuck
            self.path_finding_timer = 0
            
            # Calculate direct direction to player
            direct_x = 1 if player.rect.x > self.rect.x else -1 if player.rect.x < self.rect.x else 0
            direct_y = 1 if player.rect.y > self.rect.y else -1 if player.rect.y < self.rect.y else 0
            
            # If stuck, try alternative routes
            if self.stuck_timer >= 10:
                self.stuck_timer = 0
                # Try a different direction from our alternatives list
                self.current_route_index = (self.current_route_index + 1) % len(self.alternative_routes)
                self.path_direction = self.alternative_routes[self.current_route_index]
                self.route_attempt_time = time.time()
            else:
                # Prioritize the larger distance axis
                x_dist = abs(player.rect.x - self.rect.x)
                y_dist = abs(player.rect.y - self.rect.y)
                
                if x_dist > y_dist:
                    self.path_direction = (direct_x, 0)
                else:
                    self.path_direction = (0, direct_y)
        
        # If we've been trying an alternative route for too long, go back to direct pursuit
        if self.path_direction in self.alternative_routes and time.time() - self.route_attempt_time > 1.5:
            # Calculate direct direction to player
            direct_x = 1 if player.rect.x > self.rect.x else -1 if player.rect.x < self.rect.x else 0
            direct_y = 1 if player.rect.y > self.rect.y else -1 if player.rect.y < self.rect.y else 0
            
            x_dist = abs(player.rect.x - self.rect.x)
            y_dist = abs(player.rect.y - self.rect.y)
            
            if x_dist > y_dist:
                self.path_direction = (direct_x, 0)
            else:
                self.path_direction = (0, direct_y)

        # Apply movement based on current path direction
        dx, dy = 0, 0
        if self.path_direction:
            dx = self.path_direction[0] * self.speed
            dy = self.path_direction[1] * self.speed
        
        # Try to move horizontally
        if dx != 0:
            proposed_rect = self.rect.copy()
            proposed_rect.x += dx
            
            collision = False
            for wall in walls:
                if proposed_rect.colliderect(wall):
                    collision = True
                    break
                    
            if not collision:
                self.rect.x += dx
            else:
                # If horizontal movement is blocked, try vertical
                self.path_direction = (0, 1 if player.rect.y > self.rect.y else -1)
                        
        # Try to move vertically
        if dy != 0:
            proposed_rect = self.rect.copy()
            proposed_rect.y += dy
            
            collision = False
            for wall in walls:
                if proposed_rect.colliderect(wall):
                    collision = True
                    break
                    
            if not collision:
                self.rect.y += dy
            else:
                # If vertical movement is blocked, try horizontal
                self.path_direction = (1 if player.rect.x > self.rect.x else -1, 0)
                
        # Keep bouncer in screen bounds and handle boundary collisions
        if self.rect.left < 20:
            self.rect.left = 20
            self.path_direction = (1, 0)  # Move right
        elif self.rect.right > SCREEN_WIDTH - 20:
            self.rect.right = SCREEN_WIDTH - 20
            self.path_direction = (-1, 0)  # Move left
            
        if self.rect.top < 20:
            self.rect.top = 20
            self.path_direction = (0, 1)  # Move down
        elif self.rect.bottom > SCREEN_HEIGHT - 20:
            self.rect.bottom = SCREEN_HEIGHT - 20
            self.path_direction = (0, -1)  # Move up
        
        # Store current position for stuck detection
        self.last_position = (self.rect.x, self.rect.y)

class Collectable:
    def __init__(self, x, y, type_name, color):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.collected = False
        self.type = type_name
        self.color = color
    
    def draw(self, screen):
        if not self.collected:
            pygame.draw.rect(screen, self.color, self.rect)


class Game:
    def __init__(self):
        # Start player in the bar area
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Create walls
        self.walls = WALLS
        self.exit = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 30, 30)
        
        # Place bouncer at a different location
        self.bouncer = Bouncer(SCREEN_WIDTH - 100, 60)
        
        # Game state and dialogue setup
        self.game_state = 'bar'
        self.drink_count = 0
        self.dialogue = [
            f"{self.player.name}: what a great night… I wonder if there any hometown Honkey tonk skanks I can leave this bar with…",
            f"{self.player.name}: Wow, I've had a lot to drink",
            f"{self.player.name}: Oh no… Where is my fanny pack?"
        ]
        self.current_dialogue = self.dialogue[0]
        self.dialogue_index = 0
        self.dialogue_timer = 0
        self.maze_start_time = None
        
        # Add fanny pack and hometown skanks to collect
        self.collectables = [
            Collectable(150, 150, "fanny_pack", YELLOW),
            Collectable(350, 250, "skank", PINK),
            Collectable(550, 350, "skank", PINK),
            Collectable(250, 450, "skank", PINK)
        ]
        
        # Tracking what's been collected
        self.fanny_pack_collected = False
        self.skanks_collected = 0
        self.total_skanks = 3
        
        # Add a timer for the maze
        self.maze_timer = 0
        self.time_limit = 90  # 90 seconds to complete the challenge

    def draw(self, screen):
        screen.fill(BLACK)

        if self.game_state == 'bar':
            # Bar background
            screen.fill(BROWN)
            
            # Draw the player
            pygame.draw.rect(screen, WHITE, self.player.rect)
            
            # Render drink prompt
            drink_text = font.render("Press SPACE to drink", True, WHITE)
            screen.blit(drink_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

            # Render dialogue
            if self.current_dialogue:
                dialogue_bg = pygame.Rect(20, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 40, 30)
                pygame.draw.rect(screen, BLACK, dialogue_bg)
                dialogue_render = small_font.render(self.current_dialogue, True, WHITE)
                screen.blit(dialogue_render, (30, SCREEN_HEIGHT - 45))

        elif self.game_state == 'maze':
            # Draw walls
            for wall in self.walls:
                pygame.draw.rect(screen, GRAY, wall)

            # Draw exit
            pygame.draw.rect(screen, GREEN, self.exit)
            
            # Draw collectables
            for item in self.collectables:
                if not item.collected:
                    item.draw(screen)

            # Draw player
            pygame.draw.rect(screen, WHITE, self.player.rect)

            # Draw bouncer
            pygame.draw.rect(screen, RED, self.bouncer.rect)

            # Draw countdown or bouncer start message
            if not self.bouncer.can_move:
                seconds_left = 5 - int(time.time() - self.maze_start_time)
                if seconds_left < 0:
                    seconds_left = 0
                countdown_text = font.render(f"Bouncer moves in {seconds_left} seconds!", True, WHITE)
                screen.blit(countdown_text, (SCREEN_WIDTH // 2 - 150, 30))
            
            # Draw time remaining
            time_left = max(0, self.time_limit - int(self.maze_timer))
            time_text = font.render(f"Time: {time_left}s", True, WHITE)
            screen.blit(time_text, (30, 30))
            
            # Draw collection status
            status_text = ""
            if not self.fanny_pack_collected:
                status_text += "Fanny Pack: Missing | "
            else:
                status_text += "Fanny Pack: Found | "
            
            status_text += f"Skanks: {self.skanks_collected}/{self.total_skanks}"
            
            status_render = small_font.render(status_text, True, WHITE)
            screen.blit(status_render, (SCREEN_WIDTH - 280, 30))
            
            # Draw current dialogue if any
            if self.current_dialogue:
                dialogue_bg = pygame.Rect(20, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 40, 30)
                pygame.draw.rect(screen, BLACK, dialogue_bg)
                dialogue_render = small_font.render(self.current_dialogue, True, WHITE)
                screen.blit(dialogue_render, (30, SCREEN_HEIGHT - 45))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.game_state == 'bar':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.drink_count += 1
                    self.player.drunk_level = min(self.player.drunk_level + 0.5, 
                                                  self.player.max_drunk_level)
                    
                    # Update dialogue after each drink
                    if self.dialogue_index < len(self.dialogue) - 1:
                        self.dialogue_index += 1
                        self.current_dialogue = self.dialogue[self.dialogue_index]
                        self.dialogue_timer = 0
                    
                    if self.drink_count >= 3:
                        # Transition to maze
                        self.transition_to_maze()

            elif self.game_state == 'maze':
                pass

        return True

    def transition_to_maze(self):
        # Reset player position to bottom left of maze
        self.player.rect.x = 40
        self.player.rect.y = SCREEN_HEIGHT - 40
        
        # Reset bouncer position to top right
        self.bouncer.rect.x = SCREEN_WIDTH - 250
        self.bouncer.rect.y = 60
        
        # Set game state to maze
        self.game_state = 'maze'
        
        # Set maze start time for bouncer delay
        self.maze_start_time = time.time()
        
        # Set initial dialogue
        self.current_dialogue = "Find your fanny pack and collect the hometown skanks before the bouncer gets you!"
        self.dialogue_timer = 0
        
        # Reset maze timer
        self.maze_timer = 0
        
        # Reset collection status
        self.fanny_pack_collected = False
        self.skanks_collected = 0

    def check_collectable_collisions(self):
        for item in self.collectables:
            if not item.collected and self.player.rect.colliderect(item.rect):
                item.collected = True
                
                if item.type == "fanny_pack":
                    self.fanny_pack_collected = True
                    self.current_dialogue = "Found your fanny pack! Now find the hometown skanks!"
                elif item.type == "skank":
                    self.skanks_collected += 1
                    if self.skanks_collected < self.total_skanks:
                        self.current_dialogue = f"Found a hometown skank! {self.total_skanks - self.skanks_collected} more to go!"
                    else:
                        self.current_dialogue = "You've found all the hometown skanks! Head to the exit!"
                        
                # Increase drunk effect slightly with each item collected
                self.player.drunk_level = min(self.player.drunk_level + 0.2, 
                                            self.player.max_drunk_level)
                
                self.dialogue_timer = 0

    def update(self):
        if self.game_state == 'bar':
            # Update dialogue timer
            if self.current_dialogue:
                self.dialogue_timer += 1
                if self.dialogue_timer > 180:  # 3 seconds
                    # Don't clear the last dialogue about the fanny pack
                    if self.dialogue_index < len(self.dialogue) - 1:
                        self.dialogue_index += 1
                        self.current_dialogue = self.dialogue[self.dialogue_index]
                    self.dialogue_timer = 0

        elif self.game_state == 'maze':
            # Update maze timer
            self.maze_timer += 1/60  # Assuming 60 FPS
            
            # Check if time is up
            if self.maze_timer >= self.time_limit:
                self.game_over("Time's up! The bar is closed.")
            
            # Start bouncer after 5 seconds
            if self.maze_start_time and not self.bouncer.can_move:
                if time.time() - self.maze_start_time >= 5:
                    self.bouncer.start_moving()
                    self.current_dialogue = "The bouncer is after you! Hurry!"
                    self.dialogue_timer = 0

            self.player.move()
            
            # Check for collectable collisions
            self.check_collectable_collisions()
            
            # Move bouncer
            if self.bouncer.can_move:
                self.bouncer.move_towards_player(self.player, self.walls)

            # Check bouncer collision
            if self.player.rect.colliderect(self.bouncer.rect):
                self.game_over("The bouncer caught you!")

            # Check exit - only allow exit if fanny pack and all skanks collected
            if self.player.rect.colliderect(self.exit):
                if self.fanny_pack_collected and self.skanks_collected >= self.total_skanks:
                    self.win_game()
                else:
                    # Set dialogue to indicate what's still needed
                    missing_items = []
                    if not self.fanny_pack_collected:
                        missing_items.append("fanny pack")
                    if self.skanks_collected < self.total_skanks:
                        missing_items.append(f"{self.total_skanks - self.skanks_collected} hometown skanks")
                    
                    if missing_items:
                        item_list = " and ".join(missing_items)
                        self.current_dialogue = f"You still need to find your {item_list}!"
                        self.dialogue_timer = 0
                    
            # Clear dialogue after a while
            if self.current_dialogue:
                self.dialogue_timer += 1
                if self.dialogue_timer > 180:  # 3 seconds
                    self.current_dialogue = None
                    self.dialogue_timer = 0

    def game_over(self, message):
        print(f"Game Over! {message}")
        pygame.quit()
        sys.exit()

    def win_game(self):
        time_taken = int(self.maze_timer)
        print(f"Congratulations! You escaped with your fanny pack and {self.skanks_collected} hometown skanks in {time_taken} seconds!")
        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            running = self.handle_events()
            self.update()
            self.draw(screen)
            clock.tick(60)

        pygame.quit()

def start_bar():
    game = Game()
    game.run()

if __name__ == "__main__":
    start_bar()