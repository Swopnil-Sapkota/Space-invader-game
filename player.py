import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = window_width // 2
        self.rect.bottom = window_height - 10
        self.speed = 5
        self.window_width = window_width
        self.window_height = window_height
        self.health = 100 

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= self.speed

    def move_right(self):
        if self.rect.right < self.window_width:
            self.rect.x += self.speed

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > 100: 
            self.health = 100
