import pygame
import random
import math
import sys

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
LIGHT_GRAY = (220, 220, 220)
YELLOW = (255, 255, 0)

# Game states
KITCHEN = 0
FRIDGE_MINIGAME = 1
DIALOG = 2
FIGHTING = 3
GAME_OVER = 4

# Character class
class Character:
    def __init__(self, x, y, color, is_player=False, image_path=None, name=None):
        self.x = x
        self.y = y
        self.color = color
        self.width = 75
        self.height = 75
        self.speed = 4
        self.health = 100
        self.is_player = is_player
        self.punching = False
        self.punch_timer = 0
        self.direction = 1  # 1 for right, -1 for left
        self.image = None
        self.name = name
        if image_path:
            self.load_image(image_path)

    def load_image(self, path):
        try:
            self.image = pygame.image.load(path).convert()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            # Create flipped version for left direction
            self.image_flipped = pygame.transform.flip(self.image, True, False)
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            self.image = None

    def draw(self, surface):
        if self.image:
            # Use the appropriate image based on direction
            img_to_draw = self.image_flipped if self.direction == -1 else self.image
            surface.blit(img_to_draw, (self.x, self.y))
        else:
            # Draw rectangle for player or if image failed to load
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            
            # Eyes (to show direction)
            eye_color = WHITE
            eye_size = 10
            eye_offset = 15 if self.direction == 1 else 25
            pygame.draw.circle(surface, eye_color, (self.x + eye_offset, self.y + 15), eye_size)
        
        # Draw punch effect when punching
        if self.punching:
            punch_color = (255, 165, 0)  # Orange
            punch_size = 20
            if self.direction == 1:  # Facing right
                pygame.draw.rect(surface, punch_color, 
                                (self.x + self.width, self.y + self.height//3, punch_size, self.height//3))
            else:  # Facing left
                pygame.draw.rect(surface, punch_color, 
                                (self.x - punch_size, self.y + self.height//3, punch_size, self.height//3))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Update direction based on movement
        if dx > 0:
            self.direction = 1
        elif dx < 0:
            self.direction = -1

    def check_collision(self, other):
        # Simple rectangle collision
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)
                
    def can_punch(self, other):
        # Check if in range to punch
        punch_range = 60
        if self.direction == 1:  # Facing right
            return (other.x > self.x and 
                    other.x - self.x < punch_range and
                    abs(self.y - other.y) < self.height)
        else:  # Facing left
            return (other.x < self.x and 
                    self.x - other.x < punch_range and
                    abs(self.y - other.y) < self.height)

# Kitchen Props Class
class KitchenProp:
    def __init__(self, x, y, width, height, color, prop_type, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.type = prop_type  # "fridge", "table", "cabinet"
        self.image = None
        if image_path:
            self.load_image(image_path)

    def load_image(self, path):
        try:
            self.image = pygame.image.load(path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            self.image = None

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            
            # Add details based on type
            if self.type == "fridge":
                # Door handle
                self.load_image("assets/fridge.png")
            elif self.type == "table":
                # Table legs
                leg_width = 10
                leg_height = 30
                pygame.draw.rect(surface, self.color, (self.x, self.y + self.height, leg_width, leg_height))
                pygame.draw.rect(surface, self.color, (self.x + self.width - leg_width, self.y + self.height, leg_width, leg_height))
                pygame.draw.rect(surface, self.color, (self.x, self.y + self.height + leg_height, self.width, 5))

            elif self.type == "cabinet":
                # Cabinet handles
                
                self.load_image("assets/cabinet.png")

    def check_collision(self, character):
        return (self.x < character.x + character.width and
                self.x + self.width > character.x and
                self.y < character.y + character.height and
                self.y + self.height > character.y)

# Fridge Minigame Items
class FridgeItem:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.item_type = item_type  # "tortellini" or "other"
        
        # Assign color based on type
        if item_type == "tortellini":
            self.color = YELLOW
        else:
            # Random food colors
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
            self.color = random.choice(colors)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
        # Add some visual distinction for tortellini
        if self.item_type == "tortellini":
            # Draw pasta shape
            pygame.draw.circle(surface, (220, 200, 150), (self.x + self.width//2, self.y + self.height//2), self.width//3)
            pygame.draw.circle(surface, self.color, (self.x + self.width//2, self.y + self.height//2), self.width//4)
        else:
            # Draw generic food shape - Fix: Ensure color values don't go below 0
            darker_color = (max(0, self.color[0]-40), max(0, self.color[1]-40), max(0, self.color[2]-40))
            pygame.draw.rect(surface, darker_color, (self.x + 5, self.y + 5, self.width - 10, self.height - 10))

# Dialog class
class DialogSystem:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.dialog_index = 0
        self.active = True
        self.dialogs = [
            {"speaker": "Tim", "text": "Oh hey dad"},
            {"speaker": "Dad", "text": "The prodigal son! I am a god and therefore you are the messiah, oh anointed one!"},
            {"speaker": "Tim", "text": "I am actually better and stronger than you"},
            {"speaker": "Tim", "text": "*opens fridge to look for tortellini*"},
            {"speaker": "Dad", "text": "You've done some innocuous thing that has made me irrationally angry!"},
            {"speaker": "Tim", "text": "Your anger has made me angry!"},
            {"speaker": "Dad", "text": "You are my son you must obey me!"},
            {"speaker": "Tim", "text": "I have an oppositionally defiant personality because I was both spoiled rotten and ignored!"},
            {"speaker": "Dad", "text": "I don't have the proper skills needed to manage my emotions so my anger is building!"},
            {"speaker": "Tim", "text": "And because you don't, I never learned them either and so my anger is also building!"},
            {"speaker": "Dad", "text": "Ahhh!"},
            {"speaker": "Tim", "text": "Grrrr!"},
            {"speaker": "Narrator", "text": "Fight ensues..."},
        ]

    def draw(self, surface):
        if not self.active or self.dialog_index >= len(self.dialogs):
            return False
            
        # Dialog box
        box_height = 150
        pygame.draw.rect(surface, WHITE, (50, self.height - box_height - 50, self.width - 100, box_height))
        pygame.draw.rect(surface, BLACK, (50, self.height - box_height - 50, self.width - 100, box_height), 2)
        
        dialog = self.dialogs[self.dialog_index]
        
        # Speaker label
        speaker_color = BLUE if dialog["speaker"] == "Tim" else RED if dialog["speaker"] == "Dad" else GREEN
        speaker_text = self.font.render(dialog["speaker"] + ":", True, speaker_color)
        surface.blit(speaker_text, (70, self.height - box_height - 40))
        
        # Dialog text - with word wrap
        words = dialog["text"].split(' ')
        line = ""
        y_offset = 0
        for word in words:
            test_line = line + word + " "
            text_width = self.font.size(test_line)[0]
            if text_width < self.width - 150:
                line = test_line
            else:
                text = self.font.render(line, True, BLACK)
                surface.blit(text, (70, self.height - box_height - 5 + y_offset))
                y_offset += 30
                line = word + " "
        
        text = self.font.render(line, True, BLACK)
        surface.blit(text, (70, self.height - box_height - 5 + y_offset))
        
        # Continue prompt
        continue_text = self.small_font.render("Press SPACE to continue...", True, GRAY)
        surface.blit(continue_text, (self.width - 230, self.height - 80))
        
        return True

    def next_dialog(self):
        self.dialog_index += 1
        if self.dialog_index >= len(self.dialogs):
            self.active = False
            return False
        
        # Special handling: When reaching the fridge dialog, trigger fridge minigame
        if self.dialog_index == 3:  # *opens fridge to look for tortellini*
            return "FRIDGE_MINIGAME"
        elif self.dialog_index == len(self.dialogs) - 1:  # Fight ensues
            return "FIGHTING"
        
        return True

def main():
    # Initialize Pygame
    pygame.init()

    # Screen setup
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fight Scene")

    # Game setup
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    # Game state
    game_state = KITCHEN
    
    # Create dialog system
    dialog_system = DialogSystem(WIDTH, HEIGHT)
    
    # Create characters 
    player = Character(200, HEIGHT//2, BLUE, is_player=True, image_path=("assets/character.png"), name="Tim")
    dad = Character(WIDTH - 250, HEIGHT//2, RED, is_player=False, name="Dad")
    
    # Create kitchen props
    fridge = KitchenProp(WIDTH - 150, 100, 100, 200, LIGHT_GRAY, "fridge")
    table = KitchenProp(WIDTH//2 - 125, HEIGHT//2, 250, 75, color=None, image_path=("assets/kitchentable.png"), prop_type="table")
    
    # Create cabinets
    cabinets = []
    # Upper cabinets
    for i in range(4):
        cabinets.append(KitchenProp(50 + i*125, 50, 100, 80, LIGHT_GRAY, "cabinet"))
    # Lower cabinets
    for i in range(4):
        cabinets.append(KitchenProp(50 + i*125, HEIGHT - 150, 100, 100, LIGHT_GRAY, "cabinet"))
    
    # Fridge minigame items
    fridge_items = []
    tortellini_found = False
    
    # Movement boundaries
    PLAY_AREA_TOP = 50
    PLAY_AREA_BOTTOM = HEIGHT - 50
    PLAY_AREA_LEFT = 50
    PLAY_AREA_RIGHT = WIDTH - 50

    # Instruction text
    instruction_text = small_font.render("Use ARROW KEYS to move, SPACE to interact", True, GRAY)
    
    # Fridge minigame setup
    def setup_fridge_minigame():
        nonlocal fridge_items, tortellini_found
        fridge_items = []
        tortellini_found = False
        
        # Create food items
        num_items = 12
        grid_cols = 3
        grid_rows = 4
        item_width = 40
        item_height = 40
        grid_spacing_x = (WIDTH - 200) // grid_cols
        grid_spacing_y = (HEIGHT - 200) // grid_rows
        
        # Place one tortellini randomly
        tortellini_pos = random.randint(0, num_items - 1)
        
        for i in range(num_items):
            col = i % grid_cols
            row = i // grid_cols
            x = 100 + col * grid_spacing_x
            y = 100 + row * grid_spacing_y
            
            item_type = "tortellini" if i == tortellini_pos else "other"
            fridge_items.append(FridgeItem(x, y, item_type))
    
    # Main game loop
    running = True
    fridge_collision_debounce = 0
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == KITCHEN:
                # Handle space to check for fridge interaction
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and fridge_collision_debounce == 0:
                    # Check if player is near fridge
                    if abs(player.x - fridge.x) < player.width + 20 and abs(player.y - fridge.y) < player.height + 20:
                        game_state = DIALOG
                        # Position characters for dialog
                        player.x = 200
                        player.y = HEIGHT//2
                        dad.x = WIDTH - 250
                        dad.y = HEIGHT//2
            
            elif game_state == DIALOG:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    result = dialog_system.next_dialog()
                    if result == "FRIDGE_MINIGAME":
                        setup_fridge_minigame()
                        game_state = FRIDGE_MINIGAME
                        # Don't advance dialog_index here
                    elif result == "FIGHTING":
                        game_state = FIGHTING
                        # Reset positions for fight
                        player.x = WIDTH // 3
                        player.y = HEIGHT // 2
                        dad.x = 2 * WIDTH // 3
                        dad.y = HEIGHT // 2
                    elif result == False:
                        game_state = FIGHTING
                        # Reset positions for fight
                        player.x = WIDTH // 3
                        player.y = HEIGHT // 2
                        dad.x = 2 * WIDTH // 3
                        dad.y = HEIGHT // 2
            
            elif game_state == FRIDGE_MINIGAME:
                if event.type == pygame.MOUSEBUTTONDOWN:  # Changed from KEYDOWN to MOUSEBUTTONDOWN
                    # Check if mouse is over any item
                    mouse_pos = pygame.mouse.get_pos()
                    for item in fridge_items:
                        if (mouse_pos[0] > item.x and mouse_pos[0] < item.x + item.width and
                            mouse_pos[1] > item.y and mouse_pos[1] < item.y + item.height):
                            if item.item_type == "tortellini":
                                tortellini_found = True
                                # Continue dialog after a brief pause
                                pygame.time.set_timer(pygame.USEREVENT, 1500)  # 1.5 seconds
                            break
                
                # Return to dialog after finding tortellini
                if event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, 0)  # Cancel the timer
                    game_state = DIALOG
                    dialog_system.dialog_index += 1  # Skip the fridge dialog
            
            elif game_state == FIGHTING:
                # Punch on space bar
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.punching = True
                    player.punch_timer = 10  # Punch duration
                    
                    # Check if punch hits dad and is in range
                    if player.can_punch(dad):
                        dad.health -= 10
                        # Knockback effect
                        if player.direction == 1:  # Facing right
                            dad.x += 20
                        else:  # Facing left
                            dad.x -= 20
            
            elif game_state == GAME_OVER:
                # Restart or quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game
                        player.health = 100
                        dad.health = 100
                        dialog_system.dialog_index = 0
                        dialog_system.active = True
                        game_state = KITCHEN
                        player.x = 200
                        player.y = HEIGHT//2
                        dad.x = WIDTH - 300
                        dad.y = HEIGHT//2
                    elif event.key == pygame.K_q:
                        running = False
        
        # Clear the screen
        screen.fill(WHITE)
        
        # Handle different game states
        if game_state == KITCHEN:
            # Draw kitchen background
            pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT))
            
            # Draw cabinets and kitchen props
            for cabinet in cabinets:
                cabinet.draw(screen)
            
            table.draw(screen)
            fridge.draw(screen)
            
            # Player movement with arrow keys
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_RIGHT]:
                dx = 1
            if keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_DOWN]:
                dy = 1
            
            player.move(dx, dy)
            
            # Keep player in play area
            player.x = max(PLAY_AREA_LEFT, min(player.x, PLAY_AREA_RIGHT - player.width))
            player.y = max(PLAY_AREA_TOP, min(player.y, PLAY_AREA_BOTTOM - player.height))
            
            # Collision detection with kitchen props
            fridge_collision = abs(player.x - fridge.x) < player.width + 20 and abs(player.y - fridge.y) < player.height + 20
            
            # Debounce for fridge interaction
            if fridge_collision_debounce > 0:
                fridge_collision_debounce -= 1
            
            # Draw dad in kitchen
            dad.x = WIDTH - 300
            dad.y = HEIGHT//2
            dad.draw(screen)
            
            # Draw player
            player.draw(screen)
            
            # Draw instruction
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 30))
            
            # Show interaction hint if near fridge
            if fridge_collision:
                hint_text = small_font.render("Press SPACE to open fridge", True, BLACK)
                screen.blit(hint_text, (player.x - 30, player.y - 30))
            
        elif game_state == DIALOG:
            # Draw kitchen background for dialog
            pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT))
            
            # Draw kitchen props in background
            for cabinet in cabinets:
                cabinet.draw(screen)
            
            table.draw(screen)
            fridge.draw(screen)
            
            # Draw characters for dialog
            player.draw(screen)
            dad.draw(screen)
            
            # Draw and process dialog
            dialog_system.draw(screen)
            
        elif game_state == FRIDGE_MINIGAME:
            # Draw fridge background
            pygame.draw.rect(screen, (230, 240, 250), (0, 0, WIDTH, HEIGHT))
            
            # Draw fridge shelves
            for i in range(4):
                pygame.draw.rect(screen, (200, 200, 200), (50, 150 + i*100, WIDTH - 100, 5))
            
            # Draw fridge items
            for item in fridge_items:
                item.draw(screen)
            
            # Draw cursor for selection
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, BLACK, mouse_pos, 5, 1)
            
            # Draw instructions
            instruction_text1 = small_font.render("Move your mouse over an item and click to select", True, BLACK)
            instruction_text2 = small_font.render("Find the tortellini!", True, BLACK)
            screen.blit(instruction_text1, (WIDTH//2 - instruction_text1.get_width()//2, 30))
            screen.blit(instruction_text2, (WIDTH//2 - instruction_text2.get_width()//2, 60))
            
            # If tortellini is found
            if tortellini_found:
                found_text = font.render("You found the tortellini!", True, GREEN)
                screen.blit(found_text, (WIDTH//2 - found_text.get_width()//2, HEIGHT//2 - 50))
        
        elif game_state == FIGHTING:
            # Draw kitchen background for fight
            pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT))
            
            # Draw kitchen props in background (faded)
            s = pygame.Surface((WIDTH, HEIGHT))
            s.set_alpha(128)
            s.fill(LIGHT_BLUE)
            
            for cabinet in cabinets:
                cabinet.draw(s)
            
            table.draw(s)
            fridge.draw(s)
            
            screen.blit(s, (0, 0))
            
            # Draw boundary for fight area
            pygame.draw.rect(screen, GRAY, 
                            (PLAY_AREA_LEFT, PLAY_AREA_TOP, 
                             PLAY_AREA_RIGHT - PLAY_AREA_LEFT, 
                             PLAY_AREA_BOTTOM - PLAY_AREA_TOP), 2)
            
            # Player movement with arrow keys
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_RIGHT]:
                dx = 1
            if keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_DOWN]:
                dy = 1
            
            player.move(dx, dy)
            
            # Dad AI: move toward player
            if abs(dad.x - player.x) > 100:  # If too far, move toward player
                dad_dx = 0.5 if dad.x < player.x else -0.5
            else:  # If close enough, move randomly
                dad_dx = random.choice([-0.5, 0, 0.5])
            
            dad_dy = random.choice([-0.5, 0, 0.5])
            dad.move(dad_dx, dad_dy)
            
            # Dad occasionally tries to punch player
            if random.random() < 0.01 and dad.can_punch(player):
                dad.punching = True
                dad.punch_timer = 10
                player.health -= 5
            
            # Keep characters in play area
            player.x = max(PLAY_AREA_LEFT, min(player.x, PLAY_AREA_RIGHT - player.width))
            player.y = max(PLAY_AREA_TOP, min(player.y, PLAY_AREA_BOTTOM - player.height))
            dad.x = max(PLAY_AREA_LEFT, min(dad.x, PLAY_AREA_RIGHT - dad.width))
            dad.y = max(PLAY_AREA_TOP, min(dad.y, PLAY_AREA_BOTTOM - dad.height))
            
            # Punch timer
            if player.punch_timer > 0:
                player.punch_timer -= 1
            else:
                player.punching = False
                
            if dad.punch_timer > 0:
                dad.punch_timer -= 1
            else:
                dad.punching = False
            
            # Draw health bars
            pygame.draw.rect(screen, BLACK, (10, 10, 204, 24), 2)
            pygame.draw.rect(screen, GREEN, (12, 12, player.health * 2, 20))
            
            pygame.draw.rect(screen, BLACK, (WIDTH - 214, 10, 204, 24), 2)
            pygame.draw.rect(screen, GREEN, (WIDTH - 212, 12, dad.health * 2, 20))
            
            player_label = small_font.render("Tim", True, BLUE)
            dad_label = small_font.render("Dad", True, RED)
            screen.blit(player_label, (10, 40))
            screen.blit(dad_label, (WIDTH - 214, 40))
            
            # Draw characters
            player.draw(screen)
            dad.draw(screen)

            # Draw instruction text
            fight_instruction = small_font.render("Arrow keys to move, SPACE to punch!", True, BLACK)
            screen.blit(fight_instruction, (WIDTH//2 - fight_instruction.get_width()//2, HEIGHT - 30))
            
            # Game over conditions
            if player.health <= 0 or dad.health <= 0:
                game_state = GAME_OVER
                
        elif game_state == GAME_OVER:
            # Display game over text
            if player.health <= 0:
                outcome_text = font.render("Dad wins! Your search for tortellini ends in defeat!", True, RED)
            else:
                outcome_text = font.render("You win! Dad respects your tortellini-finding skills!", True, BLUE)
                
            game_over_text = font.render("Game Over!", True, BLACK)
            restart_text = small_font.render("Press R to restart or Q to quit", True, GRAY)
            
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(outcome_text, (WIDTH//2 - outcome_text.get_width()//2, HEIGHT//2))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()
    sys.exit()

def start_fight():
    main()  # This runs the fight scene when called

if __name__ == "__main__":
    start_fight()