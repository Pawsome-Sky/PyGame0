import pygame
import json
from world import World
from enemy import Enemy
from turret import Turret
from button import Button
import sys

pygame.init()

# --- MAIN SETTINGS ---
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
pygame.display.set_caption("Tower Defense")

# Constant
ROWS = 36
COLS = 48
TILE_SIZE = 30
original_map_width = TILE_SIZE * COLS
original_map_height = TILE_SIZE * ROWS
HEALTH = 100
MONEY = 650
TOTAL_LEVELS = 15

# Enemy constant
SPAWN_COOLDOWN = 400

# Turret constants
TURRET_LEVELS = 4
BUY_COST = 200
UPGRADE_COST = 100
KILL_REWARD = 1
LEVEL_COMPLETE_REWARD = 100
ANIMATION_STEPS = 8
ANIMATION_DELAY = 15
DAMAGE = 5

# Game variables
game_over = False
game_outcome = 0 # -1 is loss & 1 is win
level_started = False
last_enemy_spawn = pygame.time.get_ticks()
placing_turrets = False
selected_turret = None

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
large_font = pygame.font.SysFont("Arial", 36)


# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  txt = font.render(text, True, text_col)
  screen.blit(txt, (x, y))


# Load Game Map
game_map = pygame.image.load("Levels/Tower_Defense_Map1.png").convert_alpha()  # Update with actual game map
map_width = int(SCREEN_WIDTH * 0.75)  # 75% of the screen for game
map_height = SCREEN_HEIGHT
game_map = pygame.transform.scale(game_map, (map_width, map_height))

# Shop & Stats Panel
shop_width = SCREEN_WIDTH - map_width
shop_height = SCREEN_HEIGHT
shop_bg_color = (50, 50, 50)  # Dark gray background

# Shop button images
buy_turret_image = pygame.image.load("Images/buy_turret.png").convert_alpha()
cancel_image = pygame.image.load("Images/cancel.png").convert_alpha()
begin_image = pygame.image.load("Images/begin.png").convert_alpha()
fast_forward_image = pygame.image.load("Images/fast_forward.png").convert_alpha()
restart_image = pygame.image.load("Images/restart.png").convert_alpha()
upgrade_image = pygame.image.load("Images/upgrade_turret.png").convert_alpha()

# Create shop button images
begin_button = Button(map_width + 20, 60, begin_image, True)
turret_button = Button(map_width + 20, 120, buy_turret_image, True)
cancel_button = Button(map_width + 20, 180, cancel_image, True)
upgrade_button = Button(map_width + 20, 180, upgrade_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_forward_button = Button(map_width + 200, 240, fast_forward_image, False)

# gui
heart_image = pygame.image.load("Images/heart.png").convert_alpha()
coin_image = pygame.image.load("Images/coin.png").convert_alpha()

# Load sounds
shot_fx = pygame.mixer.Sound("Sounds/shot.wav")
shot_fx.set_volume(0.5)

# Turret spritesheets
turret_sprite_sheets = []
for x in range(1, TURRET_LEVELS + 1):
    turret_sheet = pygame.image.load(f"Images/turret_{x}.png").convert_alpha()
    turret_sprite_sheets.append(turret_sheet)

# Enemy images
enemy_images = {
  "weak": pygame.image.load("Enemies/enemy_1.png").convert_alpha(),
  "medium": pygame.image.load("Enemies/enemy_2.png").convert_alpha(),
  "strong": pygame.image.load("Enemies/enemy_3.png").convert_alpha(),
  "elite": pygame.image.load("Enemies/enemy_4.png").convert_alpha()
}

# Load json data from Tower Defense Map tmj file
with open("Levels/Tower_Defense_Map1.tmj") as file:
    map_data = json.load(file)


def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // TILE_SIZE
    mouse_tile_y = mouse_pos[1] // TILE_SIZE
    # calculate the sequential number of the tile
    mouse_tile_num = (mouse_tile_y * COLS) + mouse_tile_x

    # Ensure within valid tile range
    if 0 <= mouse_tile_x < COLS and 0 <= mouse_tile_y < ROWS:
        tile_value = world_map.tile_map[mouse_tile_num]
        print(f"Clicked Tile Value: {tile_value}")  # Debugging

        # Check if tile is grass (allowed placement)
        if tile_value in [38, 19]:  # Fix incorrect logic
            space_is_free = all(
                (mouse_tile_x, mouse_tile_y) != (turret.tile_x, turret.tile_y)
                for turret in turret_group
            )

            if space_is_free and world_map.money >= BUY_COST:
                new_turret = Turret(turret_sprite_sheets, mouse_tile_x, mouse_tile_y, shot_fx)
                turret_group.add(new_turret)
                world_map.money -= BUY_COST  # Deduct only if placed
                print(f"Turret placed at ({mouse_tile_x}, {mouse_tile_y})")
            else:
                print("Turret placement failed: Not enough money or space occupied.")


def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // TILE_SIZE
    mouse_tile_y = mouse_pos[1] // TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret


def clear_selection():
    for turret in turret_group:
        turret.selected = False


# Creating world
world_map = World(map_data, original_map_width, original_map_height, map_width, map_height)
world_map.process_data()
world_map.process_enemies()

# Create groups
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()


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
    screen.blit(stats_text, (map_width + 120, 20))

    draw_text("LEVEL: " + str(world_map.level), FONT, (255, 255, 255), map_width + 10, 240)
    screen.blit(heart_image, (map_width + 5, 270))
    draw_text(str(world_map.health), FONT, (255, 255, 255), map_width + 40, 270)
    screen.blit(coin_image, (map_width + 5, 300))
    draw_text(str(world_map.money), FONT, (255, 255, 255), map_width + 40, 300)


# --- GAME CYCLE ---
def game_loop():
    # Tell Python to use the global variable
    global world_map
    global game_over
    global game_outcome
    global level_started
    global last_enemy_spawn
    global placing_turrets
    global selected_turret
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        # screen.fill((0, 0, 0))  # Clear screen

        #########################
        # UPDATING SECTION
        #########################

        if game_over == False:
            # check if player has lost
            if world_map.health <= 0:
                game_over = True
                game_outcome = -1  # loss
            # check if player has won
            if world_map.level > TOTAL_LEVELS:
                game_over = True
                game_outcome = 1  # win

            # Update groups
            enemy_group.update(world_map)
            turret_group.update(enemy_group, world_map)

            # Highlight selected turret
            if selected_turret:
                selected_turret.selected = True

        #########################
        # DRAWING SECTION
        #########################

        # Draw group
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        # Shop/stats panel
        draw_shop_panel()

        if game_over == False:
            # Check if the level has been started or not
            if level_started == False:
                if begin_button.draw(screen):
                    level_started = True
            else:
                # Fast-forward option
                world_map.game_speed = 1
                if fast_forward_button.draw(screen):
                    world_map.game_speed = 2
                # Spawn enemies
                if pygame.time.get_ticks() - last_enemy_spawn > SPAWN_COOLDOWN:
                    if world_map.spawned_enemies < len(world_map.enemy_list):
                        enemy_type = world_map.enemy_list[world_map.spawned_enemies]
                        enemy = Enemy(enemy_type, world_map.waypoints, enemy_images)
                        enemy_group.add(enemy)
                        world_map.spawned_enemies += 1
                        last_enemy_spawn = pygame.time.get_ticks()

            # Check if the wave is finished
            if world_map.check_level_complete() == True:
                world_map.money += LEVEL_COMPLETE_REWARD
                world_map.level += 1
                level_started = False
                last_enemy_spawn = pygame.time.get_ticks()
                world_map.reset_level()
                world_map.process_enemies()

            # Draw buttons
            # Button for placing towers
            draw_text(str(BUY_COST), FONT, (255, 255, 255), map_width + 240, 127)
            screen.blit(coin_image, (map_width + 200, 130))
            if turret_button.draw(screen):
                placing_turrets = True
            # if placing turrets then show the cancel button as well
            if placing_turrets == True:
                # show cursor turret
                cursor_pos = pygame.mouse.get_pos()

                # Use turret_1_sheet for the cursor preview
                turret_1_sheet = turret_sprite_sheets[0]

                # Extract only the first frame (assuming 6 frames in a row)
                frame_width = turret_1_sheet.get_width() // 8  # Adjust if needed
                frame_height = turret_1_sheet.get_height()

                # Crop the first frame
                first_frame = turret_1_sheet.subsurface(pygame.Rect(0, 0, frame_width, frame_height))

                # Center the cropped frame on the cursor
                cursor_rect = first_frame.get_rect(center=cursor_pos)

                if cursor_pos[0] <= map_width:
                    screen.blit(first_frame, cursor_rect)
                if cancel_button.draw(screen):
                    placing_turrets = False
            # If a turret is selected then show the upgrade button
            if selected_turret:
                # If a turret can be upgraded then show the upgrade button
                if selected_turret.upgrade_level < TURRET_LEVELS:
                    draw_text(str(UPGRADE_COST), FONT, (255, 255, 255), map_width + 290, 187)
                    screen.blit(coin_image, (map_width + 250, 187))
                    if upgrade_button.draw(screen):
                        if world_map.money >= UPGRADE_COST:
                            selected_turret.upgrade()
                            world_map.money -= UPGRADE_COST
        else:
            pygame.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
            if game_outcome == -1:
                draw_text("GAME OVER", large_font, "grey0", 310, 230)
            elif game_outcome == 1:
                draw_text("YOU WIN!", large_font, "grey0", 315, 230)
            # Restart level
            if restart_button.draw(screen):
                game_over = False
                level_started = False
                placing_turrets = False
                selected_turret = None
                last_enemy_spawn = pygame.time.get_ticks()
                world_map = World(map_data, original_map_width, original_map_height, map_width, map_height)
                world_map.process_data()
                world_map.process_enemies()
                # Empty groups
                enemy_group.empty()
                turret_group.empty()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # Check if mouse is on the game area
                if mouse_pos[0] < map_width and mouse_pos[1] < map_height:
                    # Clear selected turrets
                    selected_turret = None
                    clear_selection()
                    if placing_turrets == True:
                        # Check if there is enough money for a turret
                        if world_map.money >= BUY_COST:
                            create_turret(mouse_pos)
                    else:
                        selected_turret = select_turret(mouse_pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Back to menu
                    main_menu()

        # Here drawing game objects, update game logic and ect.

        pygame.display.flip()

        # Draw game elements
        screen.blit(game_map, (0, 0))  # Game map

        # pygame.display.update()


# --- START MENU ---
if __name__ == "__main__":
    main_menu()
