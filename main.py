import pygame
import json
from world import World
from enemy import Enemy
import sys

pygame.init()

# --- MAIN SETTINGS ---
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
pygame.display.set_caption("Tower Defense")

# Load and Scale the Background Image
background = pygame.image.load("Images/2304x1296.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load "Tower Defense" Title Image
title_img = pygame.image.load("Images/Tower_Defense.png").convert_alpha() # Update path

# Load Button Images
play_img = pygame.image.load("Images/Start_BTN.png").convert_alpha()
quit_img = pygame.image.load("Images/Exit_BTN.png").convert_alpha()

# Scale Images if necessary
button_width, button_height = 200, 50
play_img = pygame.transform.scale(play_img, (button_width, button_height))
quit_img = pygame.transform.scale(quit_img, (button_width, button_height))

# Define Positions
title_rect = title_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
play_rect = play_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
quit_rect = quit_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

# Shrift
FONT = pygame.font.SysFont("Arial", 32)

# Define map dimensions
original_map_width = 1440
original_map_height = 1080
# Load Game Map
game_map = pygame.image.load("Levels/Tower_Defense_Map.png").convert_alpha()  # Update with actual game map
map_width = int(SCREEN_WIDTH * 0.75)  # 75% of the screen for game
map_height = SCREEN_HEIGHT
game_map = pygame.transform.scale(game_map, (map_width, map_height))

# Shop & Stats Panel
shop_width = SCREEN_WIDTH - map_width
shop_height = SCREEN_HEIGHT
shop_bg_color = (50, 50, 50)  # Dark gray background

# Enemy images
enemy_image = pygame.image.load("Enemies/Enemy2/D_Walk2.png").convert_alpha()

# Load json data from Tower Defense Map tmj file
with open("Levels/Tower_Defense_Map.tmj") as file:
    map_data = json.load(file)

# Creating world
world_map = World(map_data, original_map_width, original_map_height, map_width, map_height)
world_map.process_data()

# Create groups of enemies
enemy_group = pygame.sprite.Group()

enemy = Enemy(world_map.waypoints, enemy_image)
enemy_group.add(enemy)


# --- MENU CYCLE ---
def main_menu():
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        screen.blit(background, (0, 0))

        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Checking events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # If left mouse button
                if event.button == 1:
                    if play_rect.collidepoint(event.pos):
                        # Start game
                        print("Starting game!")
                        game_loop()  # Here I can initiate game function

                    if quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            # Hover effects for play button
        if play_rect.collidepoint(pygame.mouse.get_pos()):
            # Make the button bigger
            play_img_hover = pygame.transform.scale(play_img, (button_width + 10, button_height + 10))
            # Adjust position to keep it centered
            screen.blit(play_img_hover, (play_rect.x - 5, play_rect.y - 5))
        else:
            screen.blit(play_img, play_rect)

        # Hover effects for quit button
        if quit_rect.collidepoint(mouse_pos):
            # Make the button bigger
            quit_img_hover = pygame.transform.scale(quit_img, (button_width + 10, button_height + 10))
            # Adjust position to keep it centered
            screen.blit(quit_img_hover, (quit_rect.x - 5, quit_rect.y - 5))
        else:
            screen.blit(quit_img, quit_rect)

        # Draw "Tower Defense" Title
        screen.blit(title_img, title_rect)

        pygame.display.update()


# --- SHOP PANEL ---
def draw_shop_panel():
    """Draws the shop and stats panel."""
    pygame.draw.rect(screen, shop_bg_color, (map_width, 0, shop_width, shop_height))

    # Example: Display stats text
    stats_text = FONT.render("Stats & Shop", True, (255, 255, 255))
    screen.blit(stats_text, (map_width + 20, 20))


# --- GAME CYCLE ---
def game_loop():
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        # screen.fill((0, 0, 0))  # Clear screen

        # Update enemy groups
        enemy.update()

        # Draw enemy group
        enemy_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Back to menu
                    main_menu()

        # Here drawing game objects, update game logic and ect.

        pygame.display.flip()

        # Draw game elements
        screen.blit(game_map, (0, 0))  # Game map
        draw_shop_panel()  # Shop/stats panel

        #pygame.display.update()

# --- START MENU ---
if __name__ == "__main__":
    main_menu()
