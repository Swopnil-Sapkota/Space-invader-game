import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 20))
        self.image.fill(pygame.Color(255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
