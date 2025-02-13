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

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

# Shrift
FONT = pygame.font.SysFont("Arial", 32)


# --- FUNCTION: MENU BUTTON ---
def draw_button(surface, text, rect, base_color, hover_color):
    """
    text       - text on a button
    rect       - pygame.Rect object (x, y, width, height)
    base_color - color, when mouse not on button
    hover_color- color, when mouse is on button
    """
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        color = hover_color
    else:
        color = base_color

    # rectangle
    pygame.draw.rect(surface, color, rect)

    # preparing and showing text
    text_surf = FONT.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


# --- MENU CYCLE ---
def main_menu():
    clock = pygame.time.Clock()

    # Creating buttons (x, y, w, h)
    play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 110, 200, 50)
    options_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10, 200, 50)

    running = True
    while running:
        clock.tick(60)
        screen.blit(background, (0, 0))

        # Checking events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # If left mouse button
                if event.button == 1:
                    if play_button.collidepoint(event.pos):
                        # Start game
                        print("Starting game!")
                        game_loop()  # Here I can initiate game function

                    if options_button.collidepoint(event.pos):
                        print("Option menu")

                    if quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        # Menu text
        title_surf = FONT.render("Main Meniu", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_surf, title_rect)

        # Buttons
        draw_button(screen, "Start game", play_button, GRAY, RED)
        draw_button(screen, "Options", options_button, GRAY, RED)
        draw_button(screen, "Exit", quit_button, GRAY, RED)

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

        screen.fill((0, 100, 100))  # static color
        # Here drawing game objects, update game logic and ect.

        # Example: simple in game text
        info_surf = FONT.render("Game Scene. ESC to get back to main menu", True, WHITE)
        info_rect = info_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(info_surf, info_rect)

        pygame.display.update()


# --- START MENU ---
if __name__ == "__main__":
    main_menu()
