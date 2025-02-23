import pygame


class Button():
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                # if button is a single click type, then set clicked to True
                if self.single_click:
                    self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, self.rect)

        return action





        # # Hover effects for play button
        # if play_rect.collidepoint(pygame.mouse.get_pos()):
        #     # Make the button bigger
        #     play_img_hover = pygame.transform.scale(play_img, (button_width + 10, button_height + 10))
        #     # Adjust position to keep it centered
        #     screen.blit(play_img_hover, (play_rect.x - 5, play_rect.y - 5))
        # else:
        #     screen.blit(play_img, play_rect)
        #
        # # Hover effects for quit button
        # if quit_rect.collidepoint(mouse_pos):
        #     # Make the button bigger
        #     quit_img_hover = pygame.transform.scale(quit_img, (button_width + 10, button_height + 10))
        #     # Adjust position to keep it centered
        #     screen.blit(quit_img_hover, (quit_rect.x - 5, quit_rect.y - 5))
        # else:
        #     screen.blit(quit_img, quit_rect)