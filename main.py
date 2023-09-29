import pygame
from player import Player
from laser import Laser
from enemy import Enemy
import random

# Initialize pygame
pygame.init()
window_x = 1000
window_y = 700

# Defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

# Initialize game window
pygame.display.set_caption('Space Invaders')
game_window = pygame.display.set_mode((window_x, window_y))

# Create player sprite
player = Player(window_x, window_y)

# Create a group for lasers
lasers = pygame.sprite.Group()

# Create a group for enemies
enemies = pygame.sprite.Group()

# Shooting flag
shooting = False

# Enemy spawn timer and interval
enemy_spawn_timer = pygame.time.get_ticks()
enemy_spawn_interval = 800

# Font for displaying text
font = pygame.font.Font(None, 36)

# Load the player dead image
player_dead_image = pygame.image.load("playerdead.png")

# Variable to track player life status
player_alive = True

# Initialize score
score = 0

def game_over_screen():
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (window_x // 2, window_y // 2 - 50)

    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(f"Final Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect()
    score_rect.center = (window_x // 2, window_y // 2 + 50)

    game_window.fill(white)
    game_window.blit(player_dead_image, player.rect)
    game_window.blit(game_over_text, game_over_rect)
    game_window.blit(score_text, score_rect)
    pygame.display.update()
    

    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting_for_click = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                waiting_for_click = False


# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not shooting:
                new_laser = Laser(player.rect.centerx, player.rect.top)
                lasers.add(new_laser)
                shooting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shooting = False

  
    if player_alive:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()

        # Update the player and lasers
        player.update()
        lasers.update()

        # Check for collisions between player lasers and enemies
        collisions = pygame.sprite.spritecollide(player, enemies, True)
        for collision in collisions:
            player.take_damage(10)
             
        laser_enemy_collisions = pygame.sprite.groupcollide(lasers, enemies, True, True)

        for _ in laser_enemy_collisions:
            score += 10  

     
        if player.health <= 0:
            player_alive = False  # Set player status to dead
            game_over_screen()  # Show game over screen

    # Spawn new enemies
    current_time = pygame.time.get_ticks()
    if current_time - enemy_spawn_timer >= enemy_spawn_interval:
        enemy_x = random.randint(0, window_x - 1)
        new_enemy = Enemy(enemy_x, 0)
        enemies.add(new_enemy)
        enemy_spawn_timer = current_time

    # Move the enemies
    for enemy in enemies:
        enemy.move()

    # Clear the screen
    game_window.fill(white)

    # Draw the player, lasers, and enemies
    if player_alive:
        game_window.blit(player.image, player.rect)
    else:
        game_window.blit(player_dead_image, player.rect)  
    lasers.draw(game_window)
    enemies.draw(game_window)

    
    pygame.draw.rect(game_window, (255, 0, 0), (10, 10, player.health * 2, 20)) 
    pygame.draw.rect(game_window, (0, 128, 0), (10, 10, 200, 20), 2)  

    # Display health text
    health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))
    game_window.blit(health_text, (10, 40))

    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    game_window.blit(score_text, (window_x - 150, 10))

    # Update the display
    pygame.display.update()

pygame.quit()
