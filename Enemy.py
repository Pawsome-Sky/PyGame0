import pygame
from pygame.math import Vector2
import math
from enemy_data import ENEMY_DATA

KILL_REWARD = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoints = 1
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world_map):
        self.move(world_map)
        self.rotate()
        self.check_alive(world_map)

    def move(self, world_map):
        # Define a target waypoint
        if self.target_waypoints < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoints])
            self.movement = self.target - self.pos
        else:
            # Enemy has reached the end of the path
            self.kill()
            world_map.health -= 1
            world_map.missed_enemies += 1

        # Calculate distance to target
        dist = self.movement.length()
        # Check if remaining distance is greater than the enemy speed
        if dist >= (self.speed * world_map.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world_map.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoints += 1

    def rotate(self):
        # Calculate distance to next way point
        dist = self.target - self.pos
        # Use distance to calculate angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        # Rotate image and update rectangle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += KILL_REWARD
            self.kill()
