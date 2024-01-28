import pygame
from enemy import Enemy
from game_setup import *
from utils import *
import random
import math



def spawn_enemy_invterval(spawn_timer):
    spawn_interval = max(5 * math.cos(elapsed_time() / 10),1) # Adjust amplitude and frequency as needed

     # Spawn a new enemy if enough time has passed
    if (current_time() - spawn_timer) >= spawn_interval:
        return spawn_enemy()
    else:
        return spawn_timer

def spawn_enemy():
    new_enemy_x = screen_center_x + random.choice([-1, 1]) * (screen_center_x + random.randrange(50,100))
    new_enemy_y = screen_center_y + random.choice([-1, 1]) * (screen_center_y + random.randrange(50,100))
    new_enemy = Enemy(new_enemy_x, new_enemy_y)
    enemies.add(new_enemy)
    all_sprites.add(new_enemy)
    return current_time()

def reset_viz(player):
    player.reset_position(screen_center_x, screen_center_y)
    player.set_speed(0)
    kill_all_enemies(enemies)
    for b in player.bullets:
        b.kill()
    refresh_screen(False, True, 60, True)
    wait(3, current_time(), True, True, 60, True)
    player.set_speed(5)

def wait(seconds, rest_start, player_refresh, enemy_refresh, fps, screen_fill):
    while abs(rest_start - current_time()) <= seconds:
        refresh_screen(player_refresh, enemy_refresh, fps, screen_fill)

def refresh_screen(player_refresh, enemy_refresh, fps, screen_fill):
    clock.tick(fps)  # Limit the frame rate to 60 frames per second
    if player_refresh and enemy_refresh:
        player.update()
        enemies.update(player)
    elif player_refresh:
        player.update()
    elif enemy_refresh:
        enemies.update(player)
    
    if screen_fill:
        screen.fill((0, 0, 0))  # black

    all_sprites.draw(screen)
    player.bullets.draw(screen)
    pygame.display.flip() 

def game_over(score_in):
    for sprite in all_sprites:
        sprite.set_speed(0)
    game_over_text = font.render('GAME OVER', True, 'red')
    current_high_score = load_high_score()
    if score_in > current_high_score:
        sound_effects('new_high_score','.wav')
        print(score_in)
        save_high_score(player_name,score_in)
        second_block_text = font.render(f'NEW HIGH SCORE!!', True, 'green')
    else:
        sound_effects('loser_game_over','.wav')
        second_block_text = font.render(f'High Score: {current_high_score}', True, 'green')
    
    third_block_text = font.render('Player' + f' Score: {score_in}', True, 'white')
    
    game_over_text_rect = game_over_text.get_rect(center=(screen_center_x, screen_center_y - 20))
    second_block_text_rect = second_block_text.get_rect(center=(screen_center_x, screen_center_y + 15))
    third_block_text_rect = third_block_text.get_rect(center=(screen_center_x, screen_center_y + 50))

    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(second_block_text, second_block_text_rect)
    screen.blit(third_block_text, third_block_text_rect)

    refresh_screen(True, True, 60, False)

    return game_over_menu()

def game_over_menu():
    make_selection = True

    while make_selection:
        quit_events()

        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.KEYUP) and event.key == pygame.K_RETURN:
                player.reset_lives()
                player.reset_position(screen_center_x, screen_center_y)
                kill_all_enemies(enemies)
                refresh_screen(True, True, 60, True)
                player.set_speed(5)
                make_selection = False
    return 0, current_time()

def kill_all_enemies(enemies):
    for e in enemies:
        e.kill()

def player_collisions(player, enemies):
    if pygame.sprite.spritecollide(player, enemies, False):
        sound_effects('explosion','.wav')
        player_lives = player.get_lives()
        player_lives -= 1
        player.update_lives(-1)

        if player_lives >= 1:
            for e in enemies:
                e.set_speed(0)
            wait(1, current_time(), False, True, 60, True)
            reset_viz(player)

def enemy_bullet_collisions(player, enemies):
    add_score = 0
    for bullet in player.bullets:
        enemy_hit = pygame.sprite.spritecollideany(bullet, enemies)
        if enemy_hit:
            enemy_hit.lives -= 1 
            sound_effects('boing2','.wav')
            enemy_hit.hit()
            refresh_screen(False,True,60,True)
            bullet.kill()
            if enemy_hit.lives < 1:
                sound_effects('explosion','.wav')
                enemy_hit.kill()
                add_score += 10*enemy_hit.original_lives
    return add_score

def process_collsions(player, enemies):
    score_out = enemy_bullet_collisions(player, enemies)
    player_collisions(player, enemies)
    return score_out
