from game_setup import *
from game_functions import *

while running:
    quit_events() # esc and quit set running variable to false

    # If player is still alive, process events that occur during a player's life
    if player.get_lives() >= 1:

        # Processes enemy, player, and bullet collisions
        score += process_collsions(player, enemies)

        # Processes enemy spawning        
        spawn_timer = spawn_enemy_invterval(spawn_timer)

        # Refresh player and enemy sprites
        player.update()
        enemies.update(player)

        refresh_screen(True, True, 60, True)
    # Otherwise process gameover game events
    else:
        score, game_timer = game_over(score)

    refresh_screen(True,True,60,True)
