import pygame
from pygame.math import Vector2
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, image):
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoints = 1
        self.speed = 2
        self.angle = 0
        self.original_image = image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        # Define a target waypoint
        if self.target_waypoints < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoints])
            self.movement = self.target - self.pos
        else:
            # Enemy has reached the end of the path
            self.kill()

        # Calculate distance to target
        dist = self.movement.length()
        # Check if remaining distance is greater than the enemy speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
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
