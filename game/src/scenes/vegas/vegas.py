import pygame
import sys
import random
import time
from pygame.math import Vector2
from src.scenes.vegas.brick import Brick
from src.scenes.vegas.paper import Paper
from src.scenes.vegas.player import Player
from src.scenes.vegas.wall import Wall

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tim and Lav in Vegas")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
BRICK_COLOR = (165, 42, 42)
GRAY = (150, 150, 150)

# Fonts
font_small = pygame.font.SysFont('Arial', 20)
font_medium = pygame.font.SysFont('Arial', 28)
font_large = pygame.font.SysFont('Arial', 36)

# Game states
STATE_DIALOGUE = 0
STATE_WALL_GAME = 1
STATE_ENDING = 2
game_state = STATE_DIALOGUE

# Characters
class Character:
    def __init__(self, name, x, y, color):
        self.name = name
        self.pos = Vector2(x, y)
        self.color = color
        self.size = 40
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.size)
        name_text = font_small.render(self.name, True, WHITE)
        screen.blit(name_text, (int(self.pos.x - name_text.get_width() / 2), 
                               int(self.pos.y + self.size + 5)))

# Create characters
tim = Character("Tim", WIDTH * 0.3, HEIGHT * 0.5, BLUE)
lav = Character("Lav", WIDTH * 0.7, HEIGHT * 0.5, RED)
# Create wall and player
brick = Brick(WIDTH//2 - 50, HEIGHT//2 - 100, 100, 200)
paper = Paper()
player = Player()
wall = Wall()
papers = []

# Dialogue system
dialogues = [
    {"speaker": "Lav", "text": "I don't know about this tim…"},
    {"speaker": "Lav", "text": "This is obviously an extremely unideal situation for me"},
    {"speaker": "Lav", "text": "But I feel….like…. I don't know"},
    {"speaker": "Tim", "text": "I love you"},
    {"speaker": "Lav", "text": "you are crazy and I don't trust you… yet."},
]
current_dialogue = 0
dialogue_timer = 0
DIALOGUE_SPEED = 1000  # milliseconds

# Flash effect
flash_active = False
flash_timer = 0
flash_duration = 500  # ms

# Vegas background elements
slot_machines = []
for i in range(5):
    slot_machines.append({
        'pos': Vector2(random.randint(50, WIDTH-50), random.randint(HEIGHT-200, HEIGHT-100)),
        'size': Vector2(40, 60),
        'color': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    })

lights = []
for i in range(20):
    lights.append({
        'pos': Vector2(random.randint(0, WIDTH), random.randint(0, 100)),
        'radius': random.randint(3, 8),
        'color': (random.randint(200, 255), random.randint(200, 255), 0),
        'blink_timer': random.randint(0, 1000),
        'on': True
    })

# Game loop
def vegas():
    global game_state, current_dialogue, dialogue_timer, flash_active, flash_timer, wall_broken
    global papers
    clock = pygame.time.Clock()
    last_time = pygame.time.get_ticks()
    wall_broken = False

    running = True
    while running:
        # Calculate delta time
        current_time = pygame.time.get_ticks()
        dt = current_time - last_time
        last_time = current_time
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                # Skip dialogue with space
                elif event.key == pygame.K_SPACE and game_state == STATE_DIALOGUE:
                    current_dialogue += 1
                    if current_dialogue >= len(dialogues):
                        flash_active = True
                        flash_timer = 0
                        
            elif event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_WALL_GAME:
                if player.swing():
                    hit, completed = wall.hit(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    if completed:
                        wall_broken = True
                        game_state = STATE_ENDING
                        # Create divorce papers
                        for _ in range(50):
                            papers.append(Paper())
        
        # Update
        if game_state == STATE_DIALOGUE:
            dialogue_timer += dt
            if dialogue_timer >= DIALOGUE_SPEED:
                dialogue_timer = 0
                current_dialogue += 1
                if current_dialogue >= len(dialogues):
                    flash_active = True
                    flash_timer = 0
                    
            # Handle flash effect
            if flash_active:
                flash_timer += dt
                if flash_timer >= flash_duration:
                    flash_active = False
                    game_state = STATE_WALL_GAME
                    
        elif game_state == STATE_WALL_GAME:
            # Movement controls
            keys = pygame.key.get_pressed()
            direction = Vector2(0, 0)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                direction.x = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                direction.x = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                direction.y = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                direction.y = 1
                
            if direction.length() > 0:
                direction = direction.normalize()
                
            player.move(direction)
            player.update(dt)
            
        elif game_state == STATE_ENDING:
            # Update papers
            for paper in papers[:]:
                if paper.update():
                    papers.remove(paper)
        
        # Update blinking lights
        for light in lights:
            light['blink_timer'] += dt
            if light['blink_timer'] > 1000:
                light['blink_timer'] = 0
                light['on'] = not light['on']
                
        # Drawing
        # Draw casino background
        screen.fill(BLACK)
        
        # Draw carpet pattern
        for y in range(0, HEIGHT, 40):
            for x in range(0, WIDTH, 40):
                if (x + y) % 80 == 0:
                    pygame.draw.rect(screen, (100, 0, 100), (x, y, 40, 40))
        
        # Draw ceiling lights
        for light in lights:
            if light['on']:
                pygame.draw.circle(screen, light['color'], 
                                (int(light['pos'].x), int(light['pos'].y)), 
                                light['radius'])
                # Light glow
                pygame.draw.circle(screen, (255, 255, 100, 50), 
                                (int(light['pos'].x), int(light['pos'].y)), 
                                light['radius'] * 3)
        
        # Draw slot machines
        for machine in slot_machines:
            pygame.draw.rect(screen, machine['color'], 
                            (machine['pos'].x, machine['pos'].y, 
                            machine['size'].x, machine['size'].y))
            # Screen
            pygame.draw.rect(screen, BLACK, 
                            (machine['pos'].x + 5, machine['pos'].y + 5, 
                            machine['size'].x - 10, machine['size'].y / 2 - 5))
        
        # Draw state-specific elements
        if game_state == STATE_DIALOGUE:
            # Draw characters
            tim.draw()
            lav.draw()
            
            # Draw dialogue
            if current_dialogue < len(dialogues):
                dialogue = dialogues[current_dialogue]
                speaker_text = font_medium.render(f"{dialogue['speaker']}:", True, WHITE)
                dialogue_text = font_medium.render(dialogue['text'], True, WHITE)
                
                # Background for dialogue
                text_box = pygame.Rect(WIDTH//2 - 300, HEIGHT - 150, 600, 100)
                pygame.draw.rect(screen, (0, 0, 50), text_box)
                pygame.draw.rect(screen, GOLD, text_box, 3)
                
                # Display text
                screen.blit(speaker_text, (text_box.x + 20, text_box.y + 20))
                screen.blit(dialogue_text, (text_box.x + 20, text_box.y + 50))
            
            # Draw flash
            if flash_active:
                alpha = max(0, min(255, 255 - (flash_timer / flash_duration) * 255))
                flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                flash_surface.fill((255, 255, 255, alpha))
                screen.blit(flash_surface, (0, 0))
                
        elif game_state == STATE_WALL_GAME:
            # Draw characters on either side of wall
            tim.pos.x = WIDTH * 0.2
            lav.pos.x = WIDTH * 0.8
            tim.draw()
            lav.draw()
            
            # Draw wall
            wall.draw()
            
            # Draw player
            player.draw()
            
            # Instructions
            instr1 = font_small.render("Break the wall! Move with WASD/Arrows", True, WHITE)
            instr2 = font_small.render("Click to swing the hammer", True, WHITE)
            screen.blit(instr1, (10, 10))
            screen.blit(instr2, (10, 40))
            
        elif game_state == STATE_ENDING:
            # Draw papers
            for paper in papers:
                paper.draw()
                
            # Draw characters reunited
            tim.pos.x = WIDTH * 0.4
            lav.pos.x = WIDTH * 0.6
            tim.draw()
            lav.draw()
            
            # Draw ending text
            congrats = font_large.render("Congratulations!", True, GOLD)
            screen.blit(congrats, (WIDTH//2 - congrats.get_width()//2, 100))
            
            earned = font_medium.render("You've earned....her love", True, WHITE)
            screen.blit(earned, (WIDTH//2 - earned.get_width()//2, 150))
            
            stuck = font_medium.render("and now you're stuck with her!", True, WHITE)
            screen.blit(stuck, (WIDTH//2 - stuck.get_width()//2, 190))
            
            cvs = font_medium.render("Hope you like CVS runs at midnight!", True, WHITE)
            screen.blit(cvs, (WIDTH//2 - cvs.get_width()//2, 230))
            
            restart = font_small.render("Press ESC to quit", True, WHITE)
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT - 50))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)

# Main function
def start_vegas():
    try:
        app = vegas()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    start_vegas()