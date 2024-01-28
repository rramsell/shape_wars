import pygame
import random
from math import hypot
import time

def get_random_color():
    colors = [
        ('Red', 58, 230, 57),
        ('Blue', 230, 159, 57),
        ('Purple', 112, 0, 209),
        ('Brown', 46, 169, 255),
        ('Orange', 155, 0, 0),
    ]
    return random.choice(colors)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Create a square surface for the enemy
        self.border_width = 2
        self.color_tuple = get_random_color()[1:]
        self.side_length = random.randint(15, 80)
        self.original_image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)  # Use SRCALPHA for transparency
        pygame.draw.rect(self.original_image, self.color_tuple, \
                         (0, 0, self.side_length, self.side_length))  # Draw outer colored square
        pygame.draw.rect(self.original_image, (0, 0, 0, 0), \
                         (self.border_width, self.border_width, \
                          self.side_length - 2 * self.border_width, \
                            self.side_length - 2 * self.border_width))  # Draw inner colored square

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = max(2, int((1 - (self.side_length / 81)) * 5))
        self.original_speed = self.speed
        self.rotation_angle = 0  # Initialize rotation angle
        self.rotation_speed = max(5,(1-(self.side_length/81))*20)  # Adjust the rotation speed
        self.target_player = None  # Will store the player reference for movement
        self.hit_time = time.time()

        # enemy health by size
        if self.side_length <= 35:
            self.lives = 1
        elif self.side_length <= 55:
            self.lives = 2
        elif self.side_length <= 75:
            self.lives = 3
        else:
            self.lives = 4

        self.original_lives = self.lives
    
    def set_speed(self, input):
        self.speed = input
    
    def reset_speed(self):
        self.speed = self.original_speed

    def hit(self):
        pygame.draw.rect(self.original_image, 'white', \
                         (0, 0, self.side_length, self.side_length))  # Draw outer colored square
        self.hit_time = time.time()
    
    def reset_color(self):
        pygame.draw.rect(self.original_image, self.color_tuple, \
                         (0, 0, self.side_length, self.side_length)) 
        pygame.draw.rect(self.original_image, (0, 0, 0, 0), \
                         (self.border_width, self.border_width, \
                          self.side_length - 2 * self.border_width, \
                            self.side_length - 2 * self.border_width))  
        
    def update(self, player):
        # Rotate the original image and update the rect
        self.rotation_angle += self.rotation_speed  # Accumulate rotation angle
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.target_player = player

        # Calculate the vector from the enemy to the player
        dx = self.target_player.rect.centerx - self.rect.centerx
        dy = self.target_player.rect.centery - self.rect.centery

        # Normalize the vector to get a unit vector
        distance = hypot(dx, dy)
        
        try:
            # Try to normalize the vector to get a unit vector
            dx, dy = dx / distance, dy / distance
        except ZeroDivisionError:
            # Handle the case when the distance is zero (e.g., set a default direction)
            dx, dy = 1, 0

        # Update the enemy's position based on the direction and speed
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        # Reset color after being hit
        if time.time() - self.hit_time > .1:
            self.reset_color()