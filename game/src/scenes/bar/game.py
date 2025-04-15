import pygame
import random
import sys
import time
import math
from src.scenes.bar.walls import create_labyrinth_walls
from src.scenes.bar.player import Player
from src.scenes.bar.bouncer import Bouncer
from src.scenes.bar.collectable import Collectable
from src.scenes.bar.patron import BarPatron
from src.scenes.bar.bartender import Bartender

# Initialize pygame
pygame.init()

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bar Escape: Hometown Honkey Tonk")
# Create the walls
WALLS = create_labyrinth_walls()

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
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (181, 101, 29)
LIGHT_GRAY = (200, 200, 200)
GOLD = (255, 215, 0)
DARK_GRAY = (50, 50, 50)

# Fonts
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 22)
player_bar_area_start_x = SCREEN_WIDTH // 2
player_bar_area_start_y = SCREEN_HEIGHT // 2
player_maze_start_x = 150
player_maze_start_y = 150

patron_images = [
    "src/assets/blonde.png",
    "src/assets/charizard.png",
    "src/assets/doom_guy.png",
    "src/assets/girl_patron1.png",
    "src/assets/girl_patron2.png",
    "src/assets/girl_patron3.png",
    "src/assets/guy_patron1.png",
    "src/assets/guy_patron2.png",
    "src/assets/guy_patron3.png",
    "src/assets/link.png",
    "src/assets/split_dye.png"
]

class Game:
    def __init__(self):
        # Start player in the bar area
        self.player = Player(player_bar_area_start_x, player_bar_area_start_y)
        self.player.load_image("src/assets/tim.png")
        
        # Create walls
        self.walls = WALLS
        print(f"Walls count: {len(self.walls)}")
        print(f"First wall type: {type(self.walls[0])}")
        self.exit = pygame.Rect(SCREEN_WIDTH - 75, SCREEN_HEIGHT - 75, 30, 30)
        
        # Place bouncer at a different location
        self.bouncer = Bouncer(SCREEN_WIDTH - 200, 200, image_path=("src/assets/bouncer.png"))
        
        # Game state and dialogue setup
        self.game_state = 'bar'
        self.drink_count = 0
        self.dialogue = [
            f"{self.player.name}: What a great night… I wonder if there's any hometown honkey tonk skanks I can leave this bar with…",
            f"{self.player.name}: Wow, I've had a lot to drink",
            f"{self.player.name}: Oh no… Where is my fanny pack?"
        ]
        self.current_dialogue = self.dialogue[0]
        self.dialogue_index = 0
        self.dialogue_timer = 0
        self.maze_start_time = None
        
        # Add fanny pack and hometown skanks to collect
        self.collectables = [
            Collectable(150, 150, "fanny_pack", image_path="src/assets/fanny_pack.png"),
            Collectable(350, 225, "skank", image_path="src/assets/skank1.png"),
            Collectable(550, 350, "skank", image_path="src/assets/skank2.png"),
            Collectable(250, 425, "skank", image_path="src/assets/skank3.png")
        ]
        
        # Tracking what's been collected
        self.fanny_pack_collected = False
        self.skanks_collected = 0
        self.total_skanks = 3
        
        # Add a timer for the maze
        self.maze_timer = 0
        self.time_limit = 90  # 90 seconds to complete the challenge
        
        # Bar scene setup
        self.bar_counter = pygame.Rect(50, 100, 500, 30)
        self.bartender = Bartender(300, 70)
        self.bartender.load_image("src/assets/teddanson.png")
        
        # Bar stools
        self.bar_stools = []
        for i in range(6):
            stool_x = 100 + i * 80
            self.bar_stools.append(pygame.Rect(stool_x, 140, 30, 30))
        
        # Tables
        self.tables = []
        table_positions = [(150, 250), (350, 250), (550, 250), (250, 400), (450, 400)]
        for pos in table_positions:
            self.tables.append(pygame.Rect(pos[0], pos[1], 60, 60))
        
        # Bar patrons
        self.bar_patrons = []
        for i in range(len(patron_images)):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.bar_patrons.append(BarPatron(x, y, (255, 255, 255), image_path=patron_images[i], image_size=(50, 50)))
        # patron_colors = [RED, BLUE, GREEN, YELLOW, PINK, WHITE]
        # for i in range(8):
        #     x = random.randint(100, SCREEN_WIDTH - 100)
        #     y = random.randint(200, SCREEN_HEIGHT - 100)
        #     color = random.choice(patron_colors)
        #     self.bar_patrons.append(BarPatron(x, y, color))
        
        # Drinks on the counter
        self.drinks = []
        for i in range(4):
            drink_x = 150 + i * 100
            self.drinks.append(pygame.Rect(drink_x, 110, 15, 15))
        
        # Define bar area for patron movement
        self.bar_area = pygame.Rect(50, 150, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200)
        
        # Initialize jukebox
        self.jukebox = pygame.Rect(700, 150, 50, 80)
        
        # Drink being consumed
        self.current_drink = None
        self.drinking_animation = 0
        
        # Game over flag and reason
        self.game_over_message = ""

    def draw(self, screen):
        screen.fill(BLACK)

        if self.game_state == 'bar':
            # Bar background
            screen.fill(DARK_BROWN)
            
            # Draw wooden floor
            for x in range(0, SCREEN_WIDTH, 50):
                for y in range(0, SCREEN_HEIGHT, 50):
                    wood_rect = pygame.Rect(x, y, 50, 50)
                    pygame.draw.rect(screen, BROWN, wood_rect)
                    pygame.draw.rect(screen, DARK_BROWN, wood_rect, 1)
            
            # Draw bar counter
            pygame.draw.rect(screen, LIGHT_BROWN, self.bar_counter)
            pygame.draw.rect(screen, DARK_BROWN, self.bar_counter, 3)
            
            # Draw bar back with bottles
            bar_back = pygame.Rect(50, 50, 500, 50)
            pygame.draw.rect(screen, DARK_BROWN, bar_back)
            
            # Draw bottles on the bar back
            for i in range(10):
                bottle_x = 75 + i * 45
                bottle_height = random.randint(20, 40)
                bottle = pygame.Rect(bottle_x, 30, 15, bottle_height)
                bottle_color = random.choice([RED, BLUE, GREEN, YELLOW, LIGHT_GRAY])
                pygame.draw.rect(screen, bottle_color, bottle)
            
            # Draw bar stools
            for stool in self.bar_stools:
                pygame.draw.circle(screen, LIGHT_GRAY, stool.center, 15)
                pygame.draw.circle(screen, DARK_BROWN, stool.center, 15, 2)
            
            # Draw tables
            for table in self.tables:
                pygame.draw.circle(screen, LIGHT_BROWN, table.center, 30)
                pygame.draw.circle(screen, DARK_BROWN, table.center, 30, 2)
            
            # Draw jukebox
            pygame.draw.rect(screen, RED, self.jukebox)
            jukebox_screen = pygame.Rect(self.jukebox.x + 5, self.jukebox.y + 10, 40, 25)
            pygame.draw.rect(screen, BLUE, jukebox_screen)
            
            # Draw bartender
            self.bartender.draw(screen)
            
            # Draw bar patrons
            for patron in self.bar_patrons:
                patron.draw(screen)
            
            # Draw drinks on counter
            for drink in self.drinks:
                pygame.draw.rect(screen, GOLD, drink)
            
            # Draw the player
            # pygame.draw.rect(screen, WHITE, self.player.rect)
            # pygame.draw.circle(screen, WHITE, (self.player.rect.centerx, self.player.rect.top - 5), 10)
            self.player.draw(screen)
            self.player.move()
            # Draw current drink if drinking
            if self.current_drink:
                drink_y = self.player.rect.y - 25 + self.drinking_animation
                drink_rect = pygame.Rect(self.player.rect.x + 5, drink_y, 10, 15)
                pygame.draw.rect(screen, GOLD, drink_rect)
            
            # Render drink prompt in a box
            prompt_box = pygame.Rect(SCREEN_WIDTH // 2 + 140, SCREEN_HEIGHT // 2 - 250, 260, 50)
            pygame.draw.rect(screen, GREEN, prompt_box)
            pygame.draw.rect(screen, WHITE, prompt_box, 2)
            drink_text = font.render("Press SPACE to drink", True, BLACK)
            screen.blit(drink_text, (SCREEN_WIDTH // 2 + 145, SCREEN_HEIGHT // 2 - 240))

            # Render dialogue box at bottom
            if self.current_dialogue:
                dialogue_bg = pygame.Rect(20, SCREEN_HEIGHT - 70, SCREEN_WIDTH - 40, 50)
                pygame.draw.rect(screen, BLACK, dialogue_bg)
                pygame.draw.rect(screen, WHITE, dialogue_bg, 2)
                dialogue_render = small_font.render(self.current_dialogue, True, WHITE)
                screen.blit(dialogue_render, (30, SCREEN_HEIGHT - 50))

        elif self.game_state == 'maze':
            # Draw walls
            for wall in self.walls:
                pygame.draw.rect(screen, GRAY, wall)

            # Draw exit
            exit_image = pygame.image.load("src/assets/exit.png")
            scaled_exit_image = pygame.transform.scale(exit_image, (30, 30))
            screen.blit(scaled_exit_image, (self.exit.x, self.exit.y))
            
            # Draw collectables
            for collectable in self.collectables:
                collectable.draw(screen)

            # Draw player
            self.player.resize_image(30, 30)
            self.player.draw(screen)
            # surface, color, rect, width
            # pygame.draw.rect(screen, WHITE, self.player.rect)

            # Draw bouncer
            self.bouncer.draw(screen)

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
                dialogue_bg = pygame.Rect(20, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 100, 50)
                pygame.draw.rect(screen, GOLD, dialogue_bg)
                pygame.draw.rect(screen, WHITE, dialogue_bg, 2)
                dialogue_render = small_font.render(self.current_dialogue, True, RED)
                screen.blit(dialogue_render, (30, SCREEN_HEIGHT - 30))
        
        elif self.game_state == 'game_over':
            # Draw game over screen
            screen.fill(BLACK)
            
            # Game over text
            game_over_text = font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
            
            # Display reason
            reason_text = small_font.render(self.game_over_message, True, WHITE)
            screen.blit(reason_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            
            # Restart instructions
            restart_text = small_font.render("Press R to restart or Q to quit", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50))
        
        elif self.game_state == 'victory':
            # Draw victory screen
            screen.fill(BLACK)
            
            # Victory text
            victory_text = font.render("Found my fanny pack! And three skanks!", True, GREEN)
            screen.blit(victory_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
            
            # Victory message
            # if self.skanks_collected >= self.total_skanks:
            #     message = f"You found your fanny pack and all {self.total_skanks} hometown skanks!"
            # elif self.fanny_pack_collected:
            #     message = f"You found your fanny pack but only {self.skanks_collected} skanks. Better than nothing!"
            # else:
            #     message = "You escaped, but forgot your fanny pack. Oh well!"
                
            # message_text = small_font.render(message, True, WHITE)
            # screen.blit(message_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
            
            # Restart instructions
            restart_text = small_font.render("Press SPACE to continue", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50))

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
                    
                    # Start drinking animation
                    self.current_drink = True
                    self.drinking_animation = 0
                    
                    # Update dialogue after each drink
                    if self.dialogue_index < len(self.dialogue) - 1:
                        self.dialogue_index += 1
                        self.current_dialogue = self.dialogue[self.dialogue_index]
                        self.dialogue_timer = 0
                    
                    if self.drink_count >= 3:
                        # Transition to maze after a short delay
                        pygame.time.delay(1000)  # 1 second delay
                        self.transition_to_maze()

            elif self.game_state in ['game_over', 'victory']:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart the game
                        self.__init__()
                    elif event.key == pygame.K_q:
                        return False

        return True

    def transition_to_maze(self):
        # Reset player position to bottom left of maze
        self.player.rect.x = SCREEN_WIDTH//2 - 60
        self.player.rect.y = SCREEN_HEIGHT//2 + 60
        
        # Reset bouncer position to top right
        self.bouncer.rect.x = SCREEN_WIDTH - 250
        self.bouncer.rect.y = 60
        
        # Visual transition effect - screen spin and blur to simulate drunkenness
        original_screen = screen.copy()
        max_spin = 10  # max rotation in degrees
        
        for i in range(30):  # 30 frames of transition
            # Clear screen
            screen.fill(BLACK)
            
            # Create spin effect
            spin_amount = (i / 30.0) * max_spin
            
            # Simple blur/rotation approximation
            for offset in range(-3, 4, 2):
                offset_surface = original_screen.copy()
                # Darken the copy slightly
                dark = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                dark.fill((0, 0, 0, 10))  # Slight transparency
                offset_surface.blit(dark, (0, 0))
                
                # Calculate rotated position
                angle = math.radians(spin_amount + offset)
                dx = math.sin(angle) * 5
                dy = math.cos(angle) * 5
                
                # Blit with offset for blur effect
                screen.blit(offset_surface, (dx, dy))
            
            # Add text overlay
            if i > 15:
                text = font.render("Finding your way out...", True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                screen.blit(text, text_rect)
            
            pygame.display.flip()
            pygame.time.delay(50)  # 50ms delay (20fps)
        
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
    
    def game_over(self, message):
        self.game_state = 'game_over'
        self.game_over_message = message

    def update(self):
        if self.game_state == 'bar':
            # Update bar patrons

            for patron in self.bar_patrons:
                patron.update(self.bar_area)
                
            # Update drinking animation
            if self.current_drink:
                self.drinking_animation += 1
                if self.drinking_animation > 20:
                    self.current_drink = None
            
            # Allow player to move in bar
            self.player.move()
            
            # Update dialogue timer
            if self.current_dialogue:
                self.dialogue_timer += 1
                if self.dialogue_timer > 180:  # 3 seconds
                    # Don't clear the last dialogue about the fanny pack
                    if self.dialogue_index < len(self.dialogue) - 1:
                        self.current_dialogue = None
                    self.dialogue_timer = 0

        elif self.game_state == 'maze':
            # Update maze timer
            self.maze_timer += 1/60  # Assuming 60 FPS
            
            # Check if time is up
            if self.maze_timer >= self.time_limit:
                self.game_over("Time's up! The bouncer called the police!")
                return
            
            # Allow player to move
            self.player.move()
            
            # Check for collisions with collectables
            self.check_collectable_collisions()
            
            # Start bouncer movement after 5 seconds
            if not self.bouncer.can_move and time.time() - self.maze_start_time >= 5:
                self.bouncer.start_moving()
                self.current_dialogue = "The bouncer is after you! Run!"
            
            # Move bouncer towards player
            if self.bouncer.can_move:
                self.bouncer.move_towards_player(self.player, self.walls)
            
            # Check if bouncer caught player
            if self.player.rect.colliderect(self.bouncer.rect):
                self.game_over("The bouncer caught you!")
                return
            
            # Check if player reached exit
            if self.player.rect.colliderect(self.exit):
                self.victory()
                return
            
            # Update dialogue timer
            if self.current_dialogue:
                self.dialogue_timer += 1
                if self.dialogue_timer > 180:  # 3 seconds
                    self.current_dialogue = None
                    self.dialogue_timer = 0
    
    def victory(self):
        self.game_state = 'victory'

def main():
    # Initialize pygame
    pygame.init()
    
    # Initialize the game
    game = Game()
    clock = pygame.time.Clock()
    
    # Main game loop
    running = True
    while running:
        # Process events
        running = game.handle_events()
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw(screen)
        
        # Cap the frame rate
        clock.tick(60)
    
    # Clean up
    pygame.quit()
    sys.exit()

def start_bar():
    main()

if __name__ == "__main__":
    start_bar()