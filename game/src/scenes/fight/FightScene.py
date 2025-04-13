import pygame
import random
from src.scenes.fight.GameState import GameState
from src.scenes.fight.constants import WIDTH, HEIGHT, PLAY_AREA_LEFT, PLAY_AREA_RIGHT, PLAY_AREA_BOTTOM, PLAY_AREA_TOP

class FightScene(GameState):
    def handle_events(self, event, game):
        """Handle events in the fighting state."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game.player.punching = True
            game.player.punch_timer = 10  # Punch duration

            # Check if punch hits Dad and is in range
            if game.player.can_punch(game.dad):
                game.dad.health -= 10
                # Knockback effect
                if game.player.direction == 1:  # Facing right
                    game.dad.x += 20
                else:  # Facing left
                    game.dad.x -= 20

    def update(self, game):
        """Update the fighting state."""
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

        game.player.move(dx, dy, [])

        # Dad AI: move toward the player
        if abs(game.dad.x - game.player.x) > 100:  # If too far, move toward player
            dad_dx = 0.5 if game.dad.x < game.player.x else -0.5
        else:  # If close enough, move randomly
            dad_dx = random.choice([-0.5, 0, 0.5])

        dad_dy = random.choice([-0.5, 0, 0.5])
        game.dad.move(dad_dx, dad_dy, [])

        # Dad occasionally tries to punch the player
        if random.random() < 0.01 and game.dad.can_punch(game.player):
            game.dad.punching = True
            game.dad.punch_timer = 10
            game.player.health -= 5

        # Keep characters in the play area
        game.player.x = max(PLAY_AREA_LEFT, min(game.player.x, PLAY_AREA_RIGHT - game.player.width))
        game.player.y = max(PLAY_AREA_TOP, min(game.player.y, PLAY_AREA_BOTTOM - game.player.height))
        game.dad.x = max(PLAY_AREA_LEFT, min(game.dad.x, PLAY_AREA_RIGHT - game.dad.width))
        game.dad.y = max(PLAY_AREA_TOP, min(game.dad.y, PLAY_AREA_BOTTOM - game.dad.height))

        # Punch timers
        if game.player.punch_timer > 0:
            game.player.punch_timer -= 1
        else:
            game.player.punching = False

        if game.dad.punch_timer > 0:
            game.dad.punch_timer -= 1
        else:
            game.dad.punching = False

        # Check for game over conditions
        if game.player.health <= 0 or game.dad.health <= 0:
            game.change_state("GAME_OVER")

    def draw(self, screen, game):
        """Draw the fighting state."""
        # Draw the kitchen background for the fight
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, screen.get_width(), screen.get_height()))

        # Draw faded kitchen props
        s = pygame.Surface((screen.get_width(), screen.get_height()))
        s.set_alpha(128)
        s.fill((135, 206, 235))  # Light blue
        # Draw props and player
        for prop in game.props:
            prop.draw(screen)
        screen.blit(s, (0, 0))

        # Draw boundary for the fight area
        pygame.draw.rect(screen, (100, 100, 100), 
                         (PLAY_AREA_LEFT, PLAY_AREA_TOP, 
                          PLAY_AREA_RIGHT - PLAY_AREA_LEFT, 
                          PLAY_AREA_BOTTOM - PLAY_AREA_TOP), 2)

        # Draw health bars
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 204, 24), 2)
        pygame.draw.rect(screen, (0, 255, 0), (12, 12, game.player.health * 2, 20))

        pygame.draw.rect(screen, (0, 0, 0), (screen.get_width() - 214, 10, 204, 24), 2)
        pygame.draw.rect(screen, (0, 255, 0), (screen.get_width() - 212, 12, game.dad.health * 2, 20))

        player_label = game.small_font.render("Tim", True, (0, 0, 255))
        dad_label = game.small_font.render("Dad", True, (255, 0, 0))
        screen.blit(player_label, (10, 40))
        screen.blit(dad_label, (screen.get_width() - 214, 40))

        # Draw characters
        game.player.draw(screen)
        game.dad.draw(screen)

        # Draw instruction text

        fight_instruction = game.small_font.render("Fight your dad! Arrow keys to move, SPACE to punch!", True, (0, 0, 0))
        # Draw instruction text with a transparent purple border
        instruction_box_width = fight_instruction.get_width() + 20
        instruction_box_height = fight_instruction.get_height() + 10
        instruction_box_x = (screen.get_width() // 2) - (instruction_box_width // 2)
        instruction_box_y = screen.get_height() - 50

        # Create a semi-transparent purple background
        instruction_box_surface = pygame.Surface((instruction_box_width, instruction_box_height), pygame.SRCALPHA)
        instruction_box_surface.fill((128, 0, 128, 100))  # Semi-transparent purple
        screen.blit(instruction_box_surface, (instruction_box_x, instruction_box_y))

        # Draw a subtle light purple border
        pygame.draw.rect(screen, (200, 200, 255), (instruction_box_x, instruction_box_y, instruction_box_width, instruction_box_height), 2)

        # Blit the fight instruction text
        screen.blit(fight_instruction, (screen.get_width() // 2 - fight_instruction.get_width() // 2, screen.get_height() - 45))