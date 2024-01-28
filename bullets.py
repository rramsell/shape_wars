import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y, screen_width, screen_height):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Create a circular surface for the bullet
        radius = 5  # Bullet radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, 'white', (radius, radius), radius)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 5  # Bullet speed
        self.direction = pygame.math.Vector2(direction_x, direction_y).normalize()  # Normalize the direction vector

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Remove the bullet under certain conditions
        # if it goes off screen
        if self.rect.y < 0 or \
            self.rect.y > self.screen_height or\
            self.rect.x < 0 or \
            self.rect.x > self.screen_width:
            self.kill()
        
