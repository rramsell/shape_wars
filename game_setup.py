import pygame
from player import Player
from title_screen import get_player_name_input
from utils import *

pygame.init()

screen_width = 1200
screen_height = 600
screen_center_x = screen_width // 2
screen_center_y = screen_height // 2
center_screen = screen_width, screen_height

# Set up the display in fullscreen mode
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Survival of the Shapes!")

# Load the font from the TTF file
font = pygame.font.Font(game_files_path('Moonhouse-yE5M','.ttf'), 40)

player_name = get_player_name_input(screen, screen_width, screen_height)

player = Player(screen_center_x, screen_center_y)
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

spawn_timer = current_time()

clock = pygame.time.Clock()
running = True
score = 0
