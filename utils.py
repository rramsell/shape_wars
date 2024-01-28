import pygame
import csv
from datetime import datetime
import sys
import os
import time

game_timer = time.time()

def quit_game():
    pygame.quit()
    sys.exit()

def current_time():
    return time.time()

def elapsed_time():
    return current_time() - game_timer

def quit_events():
    for event in pygame.event.get(): # Quit events exit while loop
        if (event.type == pygame.QUIT or \
           (event.type in (pygame.KEYDOWN,pygame.KEYUP) and event.key == pygame.K_ESCAPE)):
            quit_game()

# Save high score with player name and date
def save_high_score(player_name, score):
    current_date = datetime.now().strftime('%Y-%m-%d')
    with open('high_score.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([score, player_name, current_date])

# Load high scores
def load_high_score():
    try:
        with open('high_score.csv', 'r') as file:
            reader = list(csv.reader(file))[0]
            return int(reader[0])
    except FileNotFoundError:
        return 1

def game_files_path(file, file_type):
    relative_path = 'game_files/' + file + file_type
    return os.path.join(os.path.dirname(__file__), relative_path)

def sound_effects(file, file_type):
    return pygame.mixer.Sound(game_files_path(file, file_type)).play()