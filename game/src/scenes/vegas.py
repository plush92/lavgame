import pygame
import sys
import random
import time
from pygame.math import Vector2

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
DIALOGUE_SPEED = 1500  # milliseconds

# Wall Breaking Game
class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = 100
        self.cracked = False
        
    def hit(self, damage):
        self.health -= damage
        if self.health <= 50:
            self.cracked = True
        return self.health <= 0
        
    def draw(self):
        if self.cracked:
            pygame.draw.rect(screen, (120, 30, 30), self.rect)
            # Draw crack lines
            start_pos = (self.rect.x + 5, self.rect.y + 5)
            end_pos = (self.rect.x + self.rect.width - 5, self.rect.y + self.rect.height - 5)
            pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)
            pygame.draw.line(screen, BLACK, 
                            (self.rect.x + self.rect.width - 5, self.rect.y + 5),
                            (self.rect.x + 5, self.rect.y + self.rect.height - 5), 2)
        else:
            pygame.draw.rect(screen, BRICK_COLOR, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

class Wall:
    def __init__(self):
        self.bricks = []
        brick_width = 40
        brick_height = 20
        wall_x = WIDTH // 2 - (brick_width * 3) // 2
        
        # Create brick pattern
        for row in range(15):
            for col in range(3):
                # Stagger the bricks in alternating rows
                offset = brick_width // 2 if row % 2 else 0
                x = wall_x + col * brick_width + offset
                y = 100 + row * brick_height
                self.bricks.append(Brick(x, y, brick_width, brick_height))
    
    def draw(self):
        for brick in self.bricks:
            brick.draw()
            
    def hit(self, x, y):
        hit_any = False
        for brick in self.bricks[:]:
            if brick.rect.collidepoint(x, y):
                if brick.hit(random.randint(30, 60)):
                    self.bricks.remove(brick)
                hit_any = True
                break
        return hit_any, len(self.bricks) == 0

class Player:
    def __init__(self):
        self.pos = Vector2(WIDTH // 2, HEIGHT - 100)
        self.hammer_img = self._create_hammer_image()
        self.stamina = 100
        self.max_stamina = 100
        self.hammer_angle = 0
        self.swinging = False
        self.swing_timer = 0
        self.cooldown = False
        self.cooldown_timer = 0
        
    def _create_hammer_image(self):
        # Create a simple hammer shape
        surf = pygame.Surface((60, 20), pygame.SRCALPHA)
        pygame.draw.rect(surf, GRAY, (0, 5, 40, 10))  # Handle
        pygame.draw.rect(surf, (50, 50, 50), (40, 0, 20, 20))  # Head
        return surf
        
    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        # Point hammer toward mouse
        direction = Vector2(mouse_pos) - self.pos
        self.hammer_angle = direction.angle_to(Vector2(1, 0))
        
        # Handle swinging animation
        if self.swinging:
            self.swing_timer += dt
            if self.swing_timer >= 300:  # 300ms swing animation
                self.swinging = False
                self.swing_timer = 0
                self.cooldown = True
                self.cooldown_timer = 0
                
        # Handle cooldown
        if self.cooldown:
            self.cooldown_timer += dt
            self.stamina += dt * 0.05  # Recover stamina during cooldown
            if self.cooldown_timer >= 1000:  # 1 second cooldown
                self.cooldown = False
                
        # Cap stamina
        self.stamina = min(self.max_stamina, self.stamina)
        
    def move(self, direction):
        speed = 5
        self.pos += direction * speed
        # Keep player within bounds
        self.pos.x = max(50, min(WIDTH - 50, self.pos.x))
        self.pos.y = max(HEIGHT // 2, min(HEIGHT - 50, self.pos.y))
        
    def swing(self):
        if not self.cooldown and not self.swinging and self.stamina >= 20:
            self.swinging = True
            self.stamina -= 20
            return True
        return False
        
    def draw(self):
        # Draw player
        pygame.draw.circle(screen, GREEN, (int(self.pos.x), int(self.pos.y)), 20)
        
        # Draw hammer
        rotated_hammer = pygame.transform.rotate(self.hammer_img, self.hammer_angle)
        hammer_pos = self.pos + Vector2(30, 0).rotate(-self.hammer_angle)
        hammer_rect = rotated_hammer.get_rect(center=hammer_pos)
        screen.blit(rotated_hammer, hammer_rect)
        
        # Draw stamina bar
        bar_width = 100
        bar_height = 10
        stamina_rect = pygame.Rect(self.pos.x - bar_width // 2, self.pos.y + 30, bar_width, bar_height)
        pygame.draw.rect(screen, RED, stamina_rect)
        fill_width = int(bar_width * (self.stamina / self.max_stamina))
        fill_rect = pygame.Rect(self.pos.x - bar_width // 2, self.pos.y + 30, fill_width, bar_height)
        pygame.draw.rect(screen, GREEN, fill_rect)
        pygame.draw.rect(screen, BLACK, stamina_rect, 1)

# Create wall and player
wall = Wall()
player = Player()

# Papers (for ending)
class Paper:
    def __init__(self):
        self.pos = Vector2(random.randint(100, WIDTH - 100), random.randint(-200, -50))
        self.vel = Vector2(random.uniform(-1, 1), random.uniform(1, 3))
        self.rotation = random.randint(0, 360)
        self.rot_speed = random.uniform(-2, 2)
        self.size = Vector2(60, 80)
        self.paper_img = self._create_paper_image()
        
    def _create_paper_image(self):
        # Create a simple paper with text
        surf = pygame.Surface((int(self.size.x), int(self.size.y)), pygame.SRCALPHA)
        pygame.draw.rect(surf, WHITE, (0, 0, int(self.size.x), int(self.size.y)))
        pygame.draw.rect(surf, BLACK, (0, 0, int(self.size.x), int(self.size.y)), 1)
        
        # Add "DIVORCE" text to the paper
        text = font_small.render("DIVORCE", True, BLACK)
        surf.blit(text, (int(self.size.x/2 - text.get_width()/2), 10))
        
        # Add some lines for text
        for i in range(3):
            pygame.draw.line(surf, BLACK, (10, 30 + i*15), (int(self.size.x) - 10, 30 + i*15), 1)
        
        return surf
        
    def update(self):
        self.pos += self.vel
        self.rotation += self.rot_speed
        return self.pos.y > HEIGHT + 100
        
    def draw(self):
        rotated = pygame.transform.rotate(self.paper_img, self.rotation)
        pos = (int(self.pos.x), int(self.pos.y))
        rect = rotated.get_rect(center=pos)
        screen.blit(rotated, rect)

papers = []

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