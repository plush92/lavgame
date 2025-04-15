import pygame
import random
from src.scenes.fight.fridgeitem import FridgeItem
import os

import sys

def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class FridgeMinigame:
    def __init__(self, screen_width, screen_height, background_image_path):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fridge_items = []
        self.tortellini_found = False
        self.background_image = None
        self.load_image(background_image_path)
        self.setup_items()

    def load_fridge_image(self, path):
        """Load the fridge background image."""
        try:
            # Resolve the correct path using resource_path
            full_path = resource_path(path)
            self.background_image = pygame.image.load(full_path).convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
            print(f"Successfully loaded fridge background image: {full_path}")
        except pygame.error as e:
            print(f"Error loading fridge background image {path}: {e}")
            self.background_image = None

        # Fallback: Use a solid color if the image fails to load
        if self.background_image is None:
            print("Falling back to solid color for fridge background.")
            self.background_image = pygame.Surface((self.screen_width, self.screen_height))
            self.background_image.fill((230, 240, 250))  # Light blue fallback color
    
    def load_image(self, image_path):
        """Load an image from the given path."""
        try:
            # Load the image and scale it to the screen dimensions
            full_path = os.path.join(image_path)
            image = pygame.image.load(full_path).convert_alpha()
            image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
            print(f"Successfully loaded image: {full_path}")
            return image
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")
            return None

 
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
        tortellini_image_path = resource_path("src/assets/tortellini.png")
        other_image_paths = [
            resource_path("src/assets/apple.png"),
            resource_path("src/assets/butter.png"),
            resource_path("src/assets/cheese.png"),
            resource_path("src/assets/chocomilk.png"),
            resource_path("src/assets/jelly.png"),
            resource_path("src/assets/ketchup.png"),
            resource_path("src/assets/reeses.png"),
            resource_path("src/assets/salad.png"),
            resource_path("src/assets/soda.png"),
            resource_path("src/assets/steak.png"),
            resource_path("src/assets/tomato.png"),
            resource_path("src/assets/yogurt.png"),
            resource_path("src/assets/icecream.png"),
            resource_path("src/assets/pickles.png"),
        ]

        for i in range(num_items):
            col = i % grid_cols
            row = i // grid_cols
            x = 100 + col * grid_spacing_x
            y = 175 + row * grid_spacing_y

            if i == tortellini_pos:
                # Add the tortellini item
                self.fridge_items.append(FridgeItem(x, y, "tortellini", tortellini_image_path))
            else:
                # Add a random "other" item
                other_image_path = random.choice(other_image_paths)
                self.fridge_items.append(FridgeItem(x, y, "other", other_image_path))

    def reset(self):
        """Reset the fridge minigame."""
        self.tortellini_found = False
        self.fridge_items = []
        self.setup_items()

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

    def handle_events(self, event, game=None):
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

    def update(self, game):
        """Update the fridge minigame."""
        # No specific updates needed for now
        pass

    def is_complete(self):
        """Check if the minigame is complete."""
        return self.tortellini_found