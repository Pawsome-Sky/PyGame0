import pygame
import math
from turret_data import TURRET_DATA

TILE_SIZE = 30
ANIMATION_STEPS = 8
ANIMATION_DELAY = 100
DAMAGE = 5


class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheets, tile_x, tile_y, shot_fx):
        pygame.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.last_shot = pygame.time.get_ticks()
        self.selected = False
        self.target = None

        # Position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        # Calculate center coordinates
        self.x = (self.tile_x + 0.5) * TILE_SIZE
        self.y = (self.tile_y + 0.5) * TILE_SIZE
        # Shot sound effect
        self.shot_fx = shot_fx


        # Animation variables
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Update image
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Create transparent circle showing range
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self, sprite_sheet):
        # extract images from spritesheet
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group, world_map):
        # If target picked, play firing animation
        if self.target:
            self.play_animation()
        else:
            # Search for new target once turret has cooled down
            if pygame.time.get_ticks() - self.last_shot > (self.cooldown / world_map.game_speed):
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        # Find an enemy to target
        x_dist = 0
        y_dist = 0
        # Check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    # Damage enemy
                    self.target.health -= DAMAGE
                    # Play sound effect
                    self.shot_fx.play()
                    break

    def play_animation(self):
        # Update image
        self.original_image = self.animation_list[self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # Check if the animation has finished and reset to idle
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # Record completed time and clear target so cooldown can begin
                self.last_shot = pygame.time.get_ticks()
                self.target = None

    def upgrade(self):
        self.upgrade_level += 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        # Upgrade turret image
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]

        # Upgrade range circle
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
