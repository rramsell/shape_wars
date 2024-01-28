import pygame
from bullets import Bullet
from utils import sound_effects

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_center_x, screen_center_y):
        super().__init__()

        # Create a white circle surface for the player
        border_width = 2
        self.radius = 15
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, (0, 0, 0, 0), (self.radius, self.radius), self.radius - border_width)

        self.rect = self.image.get_rect()
        self.rect.center = (screen_center_x, screen_center_y)
        self.speed = 5
        self.lives = 3
        self.original_lives = self.lives

        self.bullets = pygame.sprite.Group()
        self.shoot_cooldown = 0.3  # Set the initial cooldown time (in seconds)
        self.last_shot_time = pygame.time.get_ticks()  # Record the time of the last shot

    def shoot(self, direction_x, direction_y, screen_width, screen_height):
        current_time = pygame.time.get_ticks()
        # Check if enough time has passed since the last shot
        if (current_time - self.last_shot_time > (self.shoot_cooldown * 1000)) and self.speed > 0:  # Convert cooldown to milliseconds
            sound_effects('shoot','.wav')
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction_x, direction_y, screen_width, screen_height)
            self.bullets.add(bullet)

            # Update the last shot time
            self.last_shot_time = current_time

    def set_speed(self,speed_input):
        self.speed = speed_input

    def update(self):
        keys = pygame.key.get_pressed()

        # Get the width and height of the screen dynamically
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        # Player Movement
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

        # Bullet Movement
        direction_x, direction_y = 0, 0

        if keys[pygame.K_UP]:
            direction_y = -1
        if keys[pygame.K_DOWN]:
            direction_y = 1
        if keys[pygame.K_LEFT]:
            direction_x = -1
        if keys[pygame.K_RIGHT]:
            direction_x = 1

        # Check for diagonal movement and adjust bullet direction
        if direction_x != 0 or direction_y != 0:
            # Non-zero length vector
            bullet_direction = pygame.Vector2(direction_x, direction_y).normalize()
            self.shoot(bullet_direction.x, bullet_direction.y, screen_width, screen_height)


        self.check_boundary()
        self.bullets.update()  # Update bullets

        self.check_boundary()
        self.bullets.update()  # Update bullets

    def check_boundary(self):
        # Get the width and height of the screen dynamically
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        # Ensure the player stays within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def get_lives(self):
        return self.lives
    
    def reset_lives(self):
        self.lives = self.original_lives

    def update_lives(self,lives_modifier):
        self.lives += lives_modifier
    
    def reset_position(self, screen_center_x, screen_center_y):
        self.rect.center = (screen_center_x, screen_center_y)