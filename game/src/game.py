import pygame
from pygame.locals import *
from src.main_menu import main_menu

# Game window setup
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.init()

main_menu()
