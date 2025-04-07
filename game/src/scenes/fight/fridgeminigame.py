import pygame
import random
from src.scenes.fight.fridgeitem import FridgeItem
import os

class FridgeMinigame:
    def __init__(self, screen_width, screen_height, background_image_path):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fridge_items = []
        self.tortellini_found = False
        self.background_image = None
        self.load_fridge_image(background_image_path)
        self.setup_items()

    def load_fridge_image(self, path):
        """Load the fridge background image."""
        try:
            self.background_image = pygame.image.load(path).convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
            print(f"Successfully loaded fridge background image: {path}")
        except pygame.error as e:
            print(f"Error loading fridge background image {path}: {e}")
            self.background_image = None
        if self.background_image is None:
            print("Falling back to solid color for fridge background.")
            self.background_image = pygame.Surface((self.screen_width, self.screen_height))
            self.background_image.fill((230, 240, 250))  # Light blue fallback color

    def setup_items(self):
        """Set up the fridge items for the minigame."""
        num_items = 12
        grid_cols = 3
        grid_rows = 4
        grid_spacing_x = (self.screen_width - 300) // grid_cols
        grid_spacing_y = (self.screen_height - 300) // grid_rows

        # Place one tortellini randomly
        tortellini_pos = random.randint(0, num_items - 1)

        # Define paths to item images
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        tortellini_image = os.path.join(assets_dir, "tortellini.png")
        other_images = [
            os.path.join(assets_dir, "apple.png"),
            os.path.join(assets_dir, "butter.png"),
            os.path.join(assets_dir, "cheese.png"),
            os.path.join(assets_dir, "chocomilk.png"),
            os.path.join(assets_dir, "jelly.png"),
            os.path.join(assets_dir, "ketchup.png"),
            os.path.join(assets_dir, "reeses.png"),
            os.path.join(assets_dir, "salad.png"),
            os.path.join(assets_dir, "soda.png"),
            os.path.join(assets_dir, "steak.png"),
            os.path.join(assets_dir, "tomato.png"),
            os.path.join(assets_dir, "yogurt.png"),
            os.path.join(assets_dir, "icecream.png"),
            os.path.join(assets_dir, "pickles.png"),
        ]

        for i in range(num_items):
            col = i % grid_cols
            row = i // grid_cols
            x = 100 + col * grid_spacing_x
            y = 175 + row * grid_spacing_y

            if i == tortellini_pos:
                # Add the tortellini item
                self.fridge_items.append(FridgeItem(x, y, "tortellini", tortellini_image))
            else:
                # Add a random "other" item
                other_image = random.choice(other_images)
                self.fridge_items.append(FridgeItem(x, y, "other", other_image))

    def draw(self, surface):
        """Draw the fridge minigame."""
        # Draw the fridge background
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill((230, 240, 250))  # Fallback color

        # Draw fridge items
        for item in self.fridge_items:
            item.draw(surface)

        # Draw instructions
        font = pygame.font.Font(None, 24)
        instruction_text1 = font.render("Move your mouse over an item and click to select", True, (0, 0, 0))
        instruction_text2 = font.render("Find the tortellini!", True, (0, 0, 0))
        surface.blit(instruction_text1, (self.screen_width // 2 - instruction_text1.get_width() // 2, 30))
        surface.blit(instruction_text2, (self.screen_width // 2 - instruction_text2.get_width() // 2, 60))

        # If tortellini is found
        if self.tortellini_found:
            found_text = font.render("Found it!", True, (0, 255, 0))
            surface.blit(found_text, (self.screen_width // 2 - found_text.get_width() // 2, self.screen_height // 2 - 50))

    def handle_event(self, event):
        """Handle events for the fridge minigame."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if mouse is over any item
            mouse_pos = pygame.mouse.get_pos()
            for item in self.fridge_items:
                if (mouse_pos[0] > item.x and mouse_pos[0] < item.x + item.width and
                    mouse_pos[1] > item.y and mouse_pos[1] < item.y + item.height):
                    if item.item_type == "tortellini":
                        self.tortellini_found = True
                        print("Tortellini found!")  # Debugging
                        return True  # Tortellini found
                    else:
                        print("Wrong item clicked!")  # Debugging
        return False  # Tortellini not found