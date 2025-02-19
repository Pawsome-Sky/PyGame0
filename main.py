import pygame
import sys

pygame.init()

# --- MAIN SETTINGS ---
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Load and Scale the Background Image
background = pygame.image.load("Images/2304x1296.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load "Tower Defense" Title Image
title_img = pygame.image.load("Images/Tower_Defense.png")  # Update path

# Load Button Images
play_img = pygame.image.load("Images/Start_BTN.png")
quit_img = pygame.image.load("Images/Exit_BTN.png")

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


# --- GAME CYCLE (EXAMPLE) ---
def game_loop():
    """
    Game logic here. For now press ESC to exit.
    """
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Back to menu
                    main_menu()

        # Here drawing game objects, update game logic and ect.

        # Example: simple in game text
        info_surf = FONT.render("Game Scene. ESC to get back to main menu", True, (255, 255, 255))
        info_rect = info_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(info_surf, info_rect)

        pygame.display.update()


# --- START MENU ---
if __name__ == "__main__":
    main_menu()
