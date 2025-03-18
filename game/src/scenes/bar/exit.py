import pygame



class Exit(self, image):
    self.image = ("assets/exit.png")
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)


    def load_image(self, path):
    try:
        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # Create flipped version for left direction
        self.image_flipped = pygame.transform.flip(self.image, True, False)
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        self.image = None